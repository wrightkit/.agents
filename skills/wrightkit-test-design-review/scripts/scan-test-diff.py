#!/usr/bin/env python3
"""Report advisory test-design candidates from a unified diff.

This scanner is intentionally narrow. It identifies changed test lines that may
encode task-oriented taxonomy or unstable expectations. Its output is a lead
for review, not a correctness verdict.
"""

from __future__ import annotations

import re
import sys

TASK_NAME_RE = re.compile(
    r"\b(?:fn|def|function)\s+[A-Za-z0-9_]*(?:issue|pr|task|ticket)[_-]?\d+[A-Za-z0-9_]*",
    re.IGNORECASE,
)
SEMVER_RE = re.compile(r"(?<![\w.])v?\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?(?![\w.])")
RUST_LEN_ASSERT_RE = re.compile(
    r"\bassert(?:_eq|_ne)?!\s*\([^;\n]*\.len\(\)[^;\n]*\b\d+\b"
    r"|\bassert(?:_eq|_ne)?!\s*\([^;\n]*\b\d+\b[^;\n]*\.len\(\)"
)
GENERIC_LEN_ASSERT_RE = re.compile(
    r"\bassert\s+len\([^)\n]+\)\s*(?:==|!=|<=|>=|<|>)\s*\d+\b"
    r"|\bexpect\([^;\n]+\)\.toHaveLength\(\s*\d+\s*\)"
)
ASSERTION_RE = re.compile(
    r"\b(?:assert(?:_[A-Za-z]+)?!?|expect|snapshot)\b",
    re.IGNORECASE,
)


def main() -> int:
    current_path: str | None = None
    new_line = 0
    found = 0

    for raw in sys.stdin:
        line = raw.rstrip("\n")

        if line.startswith("+++ "):
            target = line[4:].strip()
            if target == "/dev/null":
                current_path = None
            elif target.startswith("b/"):
                current_path = target[2:]
            else:
                current_path = target
            continue

        if line.startswith("@@ "):
            match = re.search(r"\+(\d+)(?:,\d+)?", line)
            if match:
                new_line = int(match.group(1)) - 1
            continue

        if line.startswith("+") and not line.startswith("+++"):
            new_line += 1
            if current_path is None:
                continue

            code = line[1:]
            kinds: list[str] = []

            if TASK_NAME_RE.search(code):
                kinds.append("task-id-test-name")
            if RUST_LEN_ASSERT_RE.search(code) or GENERIC_LEN_ASSERT_RE.search(code):
                kinds.append("hard-coded-length")
            if ASSERTION_RE.search(code) and SEMVER_RE.search(code):
                kinds.append("hard-coded-version")

            if kinds:
                found += 1
                print(f"{current_path}:{new_line}: {','.join(kinds)}: {code.strip()}")
            continue

        if line.startswith("-") and not line.startswith("---"):
            continue

        if current_path is not None:
            new_line += 1

    if found:
        print(
            f"\n{found} advisory candidate(s). "
            "Review each against the stable feature contract; these are not findings.",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
