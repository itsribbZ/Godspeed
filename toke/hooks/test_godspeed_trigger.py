#!/usr/bin/env python3
"""Test harness for godspeed_fuzzy_trigger.py.

Runs a table of positive and negative cases against fuzzy_match() and reports
pass/fail. Exits non-zero if any case fails so CI can gate on it.

Run from the hooks/ directory:
    python test_godspeed_trigger.py
"""
from __future__ import annotations

import sys

from godspeed_fuzzy_trigger import fuzzy_match

# (prompt, expected_match, case_description)
TESTS: list[tuple[str, bool, str]] = [
    # ----- POSITIVE: must fire -----
    ("godspeed", True, "exact"),
    ("Godspeed fix this", True, "exact title-case + trailing"),
    ("GODSPEED", True, "uppercase"),
    ("yo godspeed please", True, "mid-prompt"),
    ("what if we godspeed this?", True, "end-of-prompt with punctuation"),
    ("godspeede", True, "the user typo: trailing e"),
    ("godepge", True, "the user typo: heavy scramble"),
    ("godspede", True, "the user typo: missing middle e"),
    ("godspd", True, "truncated"),
    ("godspeeed", True, "extra e"),
    ("god speed", True, "two-word"),
    ("god-speed", True, "hyphen"),
    ("god_speed", True, "underscore"),
    ("god.speed", True, "period"),
    ("god's speed", True, "apostrophe possessive"),
    ("god speedy fix", True, "god + 'speedy' (L=1 from speed)"),
    ("god spede please", True, "god + typo"),
    ("fire godspeed and then keep going", True, "mid-sentence"),
    ("godspeed.", True, "trailing period"),
    ("!godspeed", True, "leading punctuation"),
    ("  godspeed  ", True, "padded whitespace"),

    # ----- NEGATIVE: must NOT fire -----
    ("hello world", False, "unrelated"),
    ("refactor my distributed cache", False, "unrelated code task"),
    ("god of war references", False, "'god of X' phrase"),
    ("godfrey is an elden ring boss", False, "'godfrey' Elden Ring"),
    ("godlike performance", False, "'godlike' adjective"),
    ("goddess statue", False, "'goddess'"),
    ("godzilla vs kong", False, "'godzilla'"),
    ("god save us all", False, "'god save' phrase"),
    ("god bless you", False, "'god bless' phrase"),
    ("good speed on the highway", False, "'good speed' (wrong prefix)"),
    ("godforsaken timeline", False, "'godforsaken'"),
]


def main() -> int:
    passed = 0
    failed: list[tuple[str, bool, bool, str, str]] = []

    for prompt, expected, desc in TESTS:
        matched, evidence = fuzzy_match(prompt)
        if matched == expected:
            passed += 1
            status = "PASS"
        else:
            failed.append((prompt, expected, matched, evidence, desc))
            status = "FAIL"
        print(f"{status} [{desc:40}] {prompt!r:50} -> matched={matched}, evidence={evidence!r}")

    total = len(TESTS)
    print(f"\n{passed}/{total} passed")
    if failed:
        print("\nFailures:")
        for prompt, exp, got, ev, desc in failed:
            print(f"  [{desc}] {prompt!r}: expected={exp}, got={got}, evidence={ev!r}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
