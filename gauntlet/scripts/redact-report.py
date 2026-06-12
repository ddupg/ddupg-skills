#!/usr/bin/env python3
"""Redact common secret shapes from Gauntlet reports and logs."""

import argparse
import re
import sys
from pathlib import Path


KEY_VALUE_RE = re.compile(
    r"(?im)^(\s*(?:api[_-]?key|secret|token|password|passwd|pwd|access[_-]?key|private[_-]?key)\s*[:=]\s*)(.+?)\s*$"
)
AUTH_RE = re.compile(r"(?i)(Authorization\s*:\s*Bearer\s+)([A-Za-z0-9._~+/\-=]+)")
OPENAI_RE = re.compile(r"\b(sk-[A-Za-z0-9_-]{8,})\b")
UUID_KEY_RE = re.compile(
    r"\b([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})\b"
)


def redact(text):
    text = KEY_VALUE_RE.sub(lambda m: m.group(1) + "[REDACTED]", text)
    text = AUTH_RE.sub(lambda m: m.group(1) + "[REDACTED]", text)
    text = OPENAI_RE.sub("[REDACTED]", text)
    return UUID_KEY_RE.sub("[REDACTED-UUID]", text)


def read_input(path):
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def write_output(path, text):
    if path:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(text, encoding="utf-8")
        return
    sys.stdout.write(text)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", help="input file; stdin when omitted")
    parser.add_argument("-o", "--output", help="output file; stdout when omitted")
    args = parser.parse_args(argv)
    write_output(args.output, redact(read_input(args.input)))


if __name__ == "__main__":
    main()
