#!/usr/bin/env python3
"""
Shared word filtering and normalization contract for hypothesis pipelines.

This module centralizes token eligibility rules so the following tools operate
on the same lexical population:
- hypothesis_tester.py
- batch_pipeline.py
- integrated_validator.py
"""

from __future__ import annotations

import re
from typing import Any


CONTRACT_VERSION = "2026-02-15.v1"

# Non-lexical separators and known non-word placeholders.
NON_WORD_TOKENS = {
    "",
    "\n",
    "|",
    "—",
    "𐄁",
    "≈",
}

# Numeric/fraction-only tokens (including superscripts/subscripts used in corpus).
NUMERIC_TOKEN_RE = re.compile(r"^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/₀₁₂₃₄₅₆₇₈○◎—|]+$")

# Tokens that contain only logographic/sign inventory symbols and no hyphen.
# These are excluded from lexical hypothesis testing.
PURE_SYMBOL_TOKEN_RE = re.compile(r"^[A-Z*\d+\[\]₀₁₂₃₄₅₆₇₈₉]+$")


def normalize_word_token(word: Any) -> str:
    """Normalize corpus token to canonical uppercase representation."""
    if word is None:
        return ""
    if not isinstance(word, str):
        word = str(word)
    return word.strip().upper()


def is_numeric_or_fraction_token(word: str) -> bool:
    """Return True if token is numeric/fractional, not lexical."""
    return bool(NUMERIC_TOKEN_RE.match(word))


def is_damaged_or_uncertain_token(word: str) -> bool:
    """Return True if token represents damaged/uncertain sign markers."""
    return word.startswith("𐝫")


def is_hypothesis_eligible_word(word: Any) -> bool:
    """
    Shared lexical eligibility contract for hypothesis pipelines.

    Included:
    - Hyphenated lexical sequences (e.g., KU-RO, SA-RA₂, *411-VS)

    Excluded:
    - Non-word separators/placeholders
    - Pure numeric/fraction tokens
    - Pure symbol/logogram-like tokens without hyphen (e.g., VIN, GRA, OLE+KI)
    - Damaged markers
    """
    token = normalize_word_token(word)
    if not token or token in NON_WORD_TOKENS:
        return False
    if is_numeric_or_fraction_token(token):
        return False
    if is_damaged_or_uncertain_token(token):
        return False
    if "-" not in token:
        return False
    if PURE_SYMBOL_TOKEN_RE.match(token) and "-" not in token:
        return False
    return True
