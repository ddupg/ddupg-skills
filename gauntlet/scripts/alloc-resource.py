#!/usr/bin/env python3
"""Allocate Gauntlet run users, ports, and work directories.

This script intentionally stores state as JSON so it has no third-party
dependency. Use it on the remote host under root, normally with:

  /opt/gauntlet/state/allocations.json
"""

import argparse
import datetime as dt
import fcntl
import json
import os
import re
import sys
from pathlib import Path


DEFAULT_STATE = "/opt/gauntlet/state/allocations.json"
DEFAULT_WORK_ROOT = "/home"
DEFAULT_PORTS = "30000-30999"


def now_iso():
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def slugify(value):
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "run"


def parse_ports(spec):
    ports = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            if end < start:
                raise ValueError("invalid descending port range: %s" % part)
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
    if not ports:
        raise ValueError("empty port range")
    return ports


def load_state(path):
    if not path.exists():
        return {"version": 1, "allocations": []}
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def save_state(path, state):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2, sort_keys=True)
        fh.write("\n")
    os.replace(str(tmp), str(path))


def with_lock(path, fn):
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.with_suffix(path.suffix + ".lock")
    with lock_path.open("w", encoding="utf-8") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        state = load_state(path)
        result = fn(state)
        save_state(path, state)
        return result


def active_allocations(state):
    return [item for item in state.get("allocations", []) if item.get("status") == "active"]


def next_name(base, existing):
    if base not in existing:
        return base
    index = 2
    while "%s-%d" % (base, index) in existing:
        index += 1
    return "%s-%d" % (base, index)


def allocate(args):
    state_path = Path(args.state)
    ports = parse_ports(args.ports)
    base_slug = slugify(args.slug)
    base_user = "gauntlet-%s" % base_slug

    def mutate(state):
        active = active_allocations(state)
        used_users = {item["user"] for item in state.get("allocations", [])}
        used_workdirs = {item["workdir"] for item in active}
        used_ports = set()
        for item in active:
            used_ports.update(item.get("ports", []))

        user = next_name(base_user, used_users)
        suffix = user.replace("gauntlet-", "", 1)
        workdir = os.path.join(args.work_root, user)
        if workdir in used_workdirs:
            raise SystemExit("workdir already active: %s" % workdir)

        available = [port for port in ports if port not in used_ports]
        if len(available) < args.port_count:
            raise SystemExit("not enough free ports in %s" % args.ports)

        allocation = {
            "id": "%s-%s" % (suffix, now_iso().replace(":", "").replace("-", "")),
            "slug": args.slug,
            "user": user,
            "workdir": workdir,
            "ports": available[: args.port_count],
            "status": "active",
            "created_at": now_iso(),
        }
        state.setdefault("allocations", []).append(allocation)
        return allocation

    return with_lock(state_path, mutate)


def release(args):
    state_path = Path(args.state)

    def mutate(state):
        for item in state.get("allocations", []):
            if item.get("user") == args.user and item.get("status") == "active":
                item["status"] = "released"
                item["released_at"] = now_iso()
                return {"released": args.user}
        raise SystemExit("active allocation not found: %s" % args.user)

    return with_lock(state_path, mutate)


def show(args):
    return load_state(Path(args.state))


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    alloc = sub.add_parser("allocate", help="allocate a run user, ports, and workdir")
    alloc.add_argument("--state", default=DEFAULT_STATE, help="JSON state path")
    alloc.add_argument("--slug", required=True, help="human-readable requirement slug")
    alloc.add_argument("--ports", default=DEFAULT_PORTS, help="port ranges, e.g. 30000-30999")
    alloc.add_argument("--port-count", type=int, default=1, help="number of ports to reserve")
    alloc.add_argument("--work-root", default=DEFAULT_WORK_ROOT, help="parent directory for isolated user homes")

    rel = sub.add_parser("release", help="mark an allocation released")
    rel.add_argument("--state", default=DEFAULT_STATE, help="JSON state path")
    rel.add_argument("--user", required=True)

    show_parser = sub.add_parser("show", help="print state")
    show_parser.add_argument("--state", default=DEFAULT_STATE, help="JSON state path")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "allocate":
        result = allocate(args)
    elif args.command == "release":
        result = release(args)
    elif args.command == "show":
        result = show(args)
    else:
        parser.error("unknown command")
    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
