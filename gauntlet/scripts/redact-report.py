#!/usr/bin/env python3
"""Redact common secret shapes from Gauntlet reports and logs."""

import argparse
import json
import re
import sys
from pathlib import Path


SECRET_KEY_PATTERN = (
    r"(?:[a-z0-9]+[_-])*"
    r"(?:api[_-]?key|secret|token|password|passwd|pwd|access[_-]?key|private[_-]?key)"
)
SECRET_KEY_RE = re.compile(SECRET_KEY_PATTERN, re.IGNORECASE)
KEY_VALUE_RE = re.compile(
    r"(?im)^([ \t]*(?:export[ \t]+)?" + SECRET_KEY_PATTERN
    + r"[ \t]*[:=][ \t]*)([^\r\n]+)"
)
JSON_STRING_PATTERN = r'"(?:\\(?:["\\/bfnrt]|u[0-9a-fA-F]{4})|[^"\\\x00-\x1f])*"'
JSON_FIELD_RE = re.compile(
    r"(" + JSON_STRING_PATTERN + r")([ \t\r\n]*:[ \t\r\n]*)(?:"
    + JSON_STRING_PATTERN + r"|-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?|true|false|null)"
    + r"(?=[ \t\r\n]*[,}\]]|$)"
)
AUTH_RE = re.compile(r"(?i)(Authorization\s*:\s*Bearer\s+)([A-Za-z0-9._~+/\-=]+)")
OPENAI_RE = re.compile(r"\b(sk-[A-Za-z0-9_-]{8,})\b")


def redact_json_field(match):
    if SECRET_KEY_RE.fullmatch(json.loads(match.group(1))):
        return match.group(1) + match.group(2) + '"[REDACTED]"'
    return match.group(0)


def redact(text):
    text = KEY_VALUE_RE.sub(lambda m: m.group(1) + "[REDACTED]", text)
    text = JSON_FIELD_RE.sub(redact_json_field, text)
    text = AUTH_RE.sub(lambda m: m.group(1) + "[REDACTED]", text)
    return OPENAI_RE.sub("[REDACTED]", text)


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
