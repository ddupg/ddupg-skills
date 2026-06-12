#!/usr/bin/env python3
"""Lightweight shape checks for Gauntlet YAML files.

This is not a YAML parser. It deliberately checks only key presence so the
skill can stay dependency-free. Agents must still read and validate the
semantic contract before execution.
"""

import argparse
import re
import sys
from pathlib import Path


REQUIRED_PROJECT_KEYS = [
    "project:",
    "repositories:",
    "runtimes:",
    "dependencies:",
    "test_profiles:",
]

REQUIRED_RUN_KEYS = [
    "run:",
    "requirement:",
    "acceptance_criteria:",
    "remote:",
    "resources:",
    "sync:",
    "execution:",
    "reporting:",
]


def has_key(text, key):
    name = re.escape(key.rstrip(":"))
    return re.search(r"(?m)^\s*%s\s*:" % name, text) is not None


def check(path, required):
    text = Path(path).read_text(encoding="utf-8")
    missing = [key for key in required if not has_key(text, key)]
    return missing


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=["project", "run"])
    parser.add_argument("path")
    args = parser.parse_args(argv)
    required = REQUIRED_PROJECT_KEYS if args.kind == "project" else REQUIRED_RUN_KEYS
    missing = check(args.path, required)
    if missing:
        for key in missing:
            print("missing required key: %s" % key, file=sys.stderr)
        return 1
    print("ok: %s" % args.path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
