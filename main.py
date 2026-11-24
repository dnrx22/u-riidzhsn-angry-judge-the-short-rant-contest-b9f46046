#!/usr/bin/env python3
"""Angry Judge: The Short Rant — The Printer That Ate My Monday.

Writes one short rant about a broken printer to entry.txt in the
output directory (MAKEFUN_OUTPUT_DIR, or /output when that is unset).
Deterministic, stdlib only, no network, no reads outside this repo.
"""

import hashlib
import os
import sys

MAX_CHARS = 400

LINE = (
    "My printer has one job - print - and it chose violence instead. "
    "It eats paper, drinks ink like it is free, and blinks 'error' "
    "at me like I am the problem. I have spent more on cartridges "
    "than the printer itself cost. Monday, 8 a.m., deadline in ten minutes, "
    "and this plastic traitor just sits there, smug, flashing orange. "
    "I do not need a printer. I need an exorcist."
)


def validate(line: str) -> None:
    """Enforce the competition rules for the rant."""
    if not line:
        raise ValueError("line is empty")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line (no newline characters)")
    if "  " in line:
        raise ValueError("line must not contain double spaces")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"line is {len(line)} characters, over the {MAX_CHARS} limit"
        )


def main() -> int:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    # Round-trip check: what landed on disk must be exactly the line.
    with open(path, "rb") as fh:
        if fh.read() != data:
            raise RuntimeError("written entry.txt does not match the line")
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {len(data)} bytes to {path}")
    print(f"characters: {len(LINE)}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
