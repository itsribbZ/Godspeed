#!/usr/bin/env python3
"""Godspeed fuzzy-trigger hook — UserPromptSubmit.

Fires Sacred Rule #10 deterministically when ANY close variant of 'godspeed'
appears ANYWHERE in the prompt, regardless of Claude's own interpretation.

Covered patterns (case-insensitive):
  - Exact:       godspeed, Godspeed, GODSPEED
  - Trailing/missing chars (Levenshtein <= 3 from 'godspeed'):
      godspeede, godspede, godspeeed, godspd, godepge
  - Two-word forms: 'god speed', 'god-speed', 'god_speed', 'god.speed', "god's speed"
  - Positioning: anywhere in the prompt (start, middle, end)

Emits a single line to stdout when matched. Claude Code injects stdout from
UserPromptSubmit hooks as context, so the trigger marker becomes visible to
the model before it processes the user's prompt.

Non-blocking: exits 0 on no-match, on errors, or on empty input.
"""
from __future__ import annotations

import json
import re
import sys

TARGET = "godspeed"
SPEED = "speed"

# Word-pair bigram check: 'god' or 'gods' followed by a speed-like token
GOD_PREFIXES = ("god", "gods")

# Separators allowed between 'god' and 'speed' in two-word normalization.
# Matches "god speed", "god-speed", "god_speed", "god.speed", "god's speed",
# "god`speed" and runs of these characters.
SEPARATOR_CLASS = r"[\s\-_'`.]+"


def levenshtein(a: str, b: str) -> int:
    """Standard DP Levenshtein distance. Stdlib-only."""
    if len(a) < len(b):
        a, b = b, a
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        curr = [i + 1]
        for j, cb in enumerate(b):
            curr.append(
                min(
                    prev[j + 1] + 1,          # deletion
                    curr[j] + 1,              # insertion
                    prev[j] + (ca != cb),     # substitution
                )
            )
        prev = curr
    return prev[-1]


def fuzzy_match(prompt: str) -> tuple[bool, str]:
    """Return (matched, evidence_token_or_phrase)."""
    lower = prompt.lower()

    # Fast path: direct substring hit (handles 'godspeed', 'godspeede', etc.
    # because 'godspeed' is a substring of 'godspeede').
    if TARGET in lower:
        return True, TARGET

    # Two-word normalization: collapse 'god' + separator + 's...' → 'gods...'
    # then re-test. Only merges when the next word starts with 's' so we don't
    # merge 'god of war' or 'god bless' into false-positive tokens.
    normalized = re.sub(rf"\bgod{SEPARATOR_CLASS}(?=s)", "god", lower)
    if TARGET in normalized:
        return True, TARGET

    # Fuzzy token check: any token starting with 'god' within Levenshtein 3.
    # 8-char target, threshold 3 = up to ~37% char-level distance.
    # Eliminates 'godfrey' (L=4), 'godlike' (L=4), 'godzilla' (L=5), 'goddess' (L=5).
    tokens = re.findall(r"\b[a-z]+\b", lower)
    for token in tokens:
        if len(token) >= 4 and token.startswith("god"):
            if levenshtein(TARGET, token) <= 3:
                return True, token

    # Bigram check: "god X" or "gods X" where X resembles 'speed' (L <= 2).
    # Catches "god's speed" (after tokenization → ['god', 's', 'speed']) via
    # a forward-scan that skips short tokens between 'god' and the speed-like word.
    for i, tok in enumerate(tokens):
        if tok not in GOD_PREFIXES:
            continue
        # Look at the next 1-2 tokens for a speed-like match.
        for j in (i + 1, i + 2):
            if j >= len(tokens):
                break
            cand = tokens[j]
            if len(cand) >= 3 and levenshtein(SPEED, cand) <= 2:
                return True, f"{tok} {cand}"

    return False, ""


def read_prompt() -> str:
    """UserPromptSubmit hooks receive JSON on stdin with a 'prompt' field."""
    raw = sys.stdin.read()
    if not raw.strip():
        return ""
    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        return raw.strip()
    # Claude Code payload keys have shifted across versions; check both.
    return (payload.get("prompt") or payload.get("user_prompt") or "").strip()


def main() -> int:
    prompt = read_prompt()
    if not prompt:
        return 0

    matched, evidence = fuzzy_match(prompt)
    if matched:
        # ASCII-only output so the message survives Windows cp1252 console encoding
        # when Claude Code captures stdout from this hook.
        print(
            f"GODSPEED TRIGGER (fuzzy match: {evidence!r}) "
            f"-- Sacred Rule #10: invoke the /godspeed skill immediately, "
            f"before any other work, no exceptions."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
