#!/usr/bin/env python3
"""Write the fridge's passive-aggressive note to /output/entry.txt.

Single deterministic line, no trailing newline, validated against the
bounty gate: UTF-8 text, 1-200 characters, not only whitespace.
Standard library only.
"""

import os
import sys

ENTRY = "Your yogurt expired Tuesday. I didn't throw it out \u2014 I wanted you to see what commitment looks like."

OUTPUT_PATH = "/output/entry.txt"


def repo_entry_path():
    """Path of the repo-root copy next to this script."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")


def validate(text):
    """Check the gate: 1-200 chars, not only whitespace."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if len(text) < 1 or len(text) > 200:
        raise ValueError(f"entry must be 1-200 characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    # Must round-trip as UTF-8.
    text.encode("utf-8")
    return True


def write_and_verify(path, data):
    """Write bytes, then read back and verify byte-for-byte."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        read_back = f.read()
    if read_back != data:
        raise RuntimeError(f"read-back mismatch for {path}")
    return read_back


def main():
    validate(ENTRY)
    data = ENTRY.encode("utf-8")
    write_and_verify(OUTPUT_PATH, data)
    write_and_verify(repo_entry_path(), data)
    # Cross-check: the two outputs must be byte-identical to each other,
    # not just to the in-memory bytes.
    with open(OUTPUT_PATH, "rb") as f:
        out_data = f.read()
    with open(repo_entry_path(), "rb") as f:
        repo_data = f.read()
    if out_data != repo_data:
        raise RuntimeError("/output/entry.txt and repo entry.txt differ")
    print(f"Wrote {len(ENTRY)} chars ({len(data)} bytes) to {OUTPUT_PATH}")
    print(f"Wrote {len(ENTRY)} chars ({len(data)} bytes) to {repo_entry_path()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
