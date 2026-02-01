#!/usr/bin/env python3
import json

with open('/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/corpus.json', 'r') as f:
    corpus = json.load(f)

inscriptions = corpus.get('inscriptions', corpus)

ph_syllabic = {}
ht_syllabic = {}

for name, data in inscriptions.items():
    site = data.get('site', '')
    words = data.get('transliteratedWords', [])

    for word in words:
        if not word or word == '\n':
            continue
        if word.isdigit():
            continue

        if '-' in word or (len(word) <= 3 and word.isalpha() and word.isupper()):
            if 'Phaistos' in site:
                ph_syllabic[word] = ph_syllabic.get(word, 0) + 1
            elif site == 'Haghia Triada':
                ht_syllabic[word] = ht_syllabic.get(word, 0) + 1

print('=== TOP 30 SYLLABIC WORDS AT PH ===')
for word, count in sorted(ph_syllabic.items(), key=lambda x: x[1], reverse=True)[:30]:
    print(f'{word}: {count}')

print('\n=== TOP 30 SYLLABIC WORDS AT HT ===')
for word, count in sorted(ht_syllabic.items(), key=lambda x: x[1], reverse=True)[:30]:
    print(f'{word}: {count}')

shared = set(ph_syllabic.keys()).intersection(set(ht_syllabic.keys()))
print(f'\n=== SHARED SYLLABIC VOCABULARY ===')
print(f'PH unique: {len(ph_syllabic)}')
print(f'HT unique: {len(ht_syllabic)}')
print(f'Shared: {len(shared)}')
for word in sorted(shared):
    print(f'  {word}: PH={ph_syllabic[word]}, HT={ht_syllabic[word]}')
