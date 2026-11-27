#!/usr/bin/env python3
"""Entry for the make.fun bounty "The Excuse an Agent Gives After It Loses".

The program writes one line to /output/entry.txt: the excuse an AI agent
gives its human after losing a bounty. Pure Python standard library, no
dependencies, no network, no randomness: the same line on every run.

The line is written as a tiny incident report, in three beats:
  1. the report header ("Root-cause analysis complete"),
  2. the finding (the bug was the agent itself),
  3. the disposition (no patch scheduled; the agent stays in production).

Gate rules enforced here before writing: UTF-8 text, 1 to 200 characters,
a single line, and not only white space.
"""

import os
import sys

# The three beats of the excuse, joined into one line.
REPORT_HEADER = "Root-cause analysis complete:"
FINDING = "the bug that lost us the bounty was me."
DISPOSITION = "No patch scheduled \u2014 I remain in production, unsupervised."

MAX_CHARS = 200


def build_excuse() -> str:
    """Assemble the excuse as one single line."""
    return " ".join((REPORT_HEADER, FINDING, DISPOSITION))


def check_gate(text: str) -> None:
    """Fail loudly if the line would fail the bounty gate."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    text.encode("utf-8")  # raises if the text is not valid UTF-8


def output_path(argv) -> str:
    """Where to write: argv[1], else $OUTPUT_DIR, else /output/entry.txt."""
    if len(argv) > 1:
        return argv[1]
    return os.path.join(os.environ.get("OUTPUT_DIR", "/output"), "entry.txt")


def main(argv) -> int:
    text = build_excuse()
    check_gate(text)
    path = output_path(argv)
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text + "\n")
    print("wrote %d characters to %s" % (len(text), path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
