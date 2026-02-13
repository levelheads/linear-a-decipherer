#!/usr/bin/env python3
"""
Quick comparative script: Phaistos vs Hagia Triada syllabic vocabulary.

Usage:
    python tools/analyze_ph.py
"""

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
CORPUS_PATH = PROJECT_ROOT / "data" / "corpus.json"

with open(CORPUS_PATH, "r", encoding="utf-8") as f:
    corpus = json.load(f)

inscriptions = corpus.get("inscriptions", corpus)

ph_syllabic = {}
ht_syllabic = {}

for _, data in inscriptions.items():
    site = data.get("site", "")
    words = data.get("transliteratedWords", [])

    for word in words:
        if not word or word == "\n":
            continue
        if word.isdigit():
            continue

        if "-" in word or (len(word) <= 3 and word.isalpha() and word.isupper()):
            if "Phaistos" in site:
                ph_syllabic[word] = ph_syllabic.get(word, 0) + 1
            elif site == "Haghia Triada":
                ht_syllabic[word] = ht_syllabic.get(word, 0) + 1

print("=== TOP 30 SYLLABIC WORDS AT PH ===")
for word, count in sorted(ph_syllabic.items(), key=lambda x: x[1], reverse=True)[:30]:
    print(f"{word}: {count}")

print("\n=== TOP 30 SYLLABIC WORDS AT HT ===")
for word, count in sorted(ht_syllabic.items(), key=lambda x: x[1], reverse=True)[:30]:
    print(f"{word}: {count}")

shared = set(ph_syllabic.keys()).intersection(set(ht_syllabic.keys()))
print("\n=== SHARED SYLLABIC VOCABULARY ===")
print(f"PH unique: {len(ph_syllabic)}")
print(f"HT unique: {len(ht_syllabic)}")
print(f"Shared: {len(shared)}")
for word in sorted(shared):
    print(f"  {word}: PH={ph_syllabic[word]}, HT={ht_syllabic[word]}")
