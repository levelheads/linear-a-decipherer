#!/usr/bin/env python3
"""
Linear A Corpus Parser

Parses data from the lineara.xyz repository (external/lineara/) into clean JSON
format for analysis. This script extracts inscription data, Linear B cognates,
and generates corpus statistics.

Attribution:
    Data source: https://github.com/mwenge/lineara.xyz (mwenge)
    Upstream sources: GORILA (Godart & Olivier), George Douros, John Younger
    See ATTRIBUTION.md for full attribution chain.

Usage:
    python tools/parse_lineara_corpus.py

Output:
    data/corpus.json          - Full inscription corpus
    data/cognates.json        - Linear B cognate mappings
    data/statistics.json      - Corpus statistics
"""

import json
import re
import os
from pathlib import Path
from collections import Counter
from datetime import datetime


# Paths relative to project root
PROJECT_ROOT = Path(__file__).parent.parent
LINEARA_DIR = PROJECT_ROOT / "external" / "lineara"
OUTPUT_DIR = PROJECT_ROOT / "data"


def extract_js_map_entries(content: str) -> list:
    """
    Extract Map entries using regex pattern matching.
    Returns list of (key, json_object_str) tuples.
    """
    entries = []

    # Pattern: ["KEY",{ ... }]
    # We find the start of each entry and then balance braces
    entry_start_pattern = re.compile(r'\["([^"]+)",\s*\{')

    for match in entry_start_pattern.finditer(content):
        key = match.group(1)
        start = match.end() - 1  # Position of opening brace

        # Balance braces to find the end of the object
        brace_count = 1
        pos = start + 1

        while brace_count > 0 and pos < len(content):
            char = content[pos]
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
            elif char == '"':
                # Skip string content
                pos += 1
                while pos < len(content):
                    if content[pos] == '\\':
                        pos += 2
                        continue
                    if content[pos] == '"':
                        break
                    pos += 1
            pos += 1

        obj_str = content[start:pos]
        entries.append((key, obj_str))

    return entries


def parse_js_object_safe(obj_str: str) -> dict:
    """
    Parse a JavaScript object string to Python dict.
    Uses json.loads after preprocessing.
    """
    try:
        # The object is already mostly JSON-compatible
        # Just need to handle potential issues
        return json.loads(obj_str)
    except json.JSONDecodeError:
        # Try some fixups
        fixed = obj_str
        # Remove trailing commas before closing braces/brackets
        fixed = re.sub(r',\s*}', '}', fixed)
        fixed = re.sub(r',\s*\]', ']', fixed)
        try:
            return json.loads(fixed)
        except json.JSONDecodeError as e:
            # Return a minimal dict with error info
            return {'_parse_error': str(e), '_raw_snippet': obj_str[:200]}


def load_inscriptions() -> dict:
    """Load and parse LinearAInscriptions.js."""
    js_path = LINEARA_DIR / "LinearAInscriptions.js"

    if not js_path.exists():
        raise FileNotFoundError(
            f"LinearAInscriptions.js not found at {js_path}\n"
            "Run 'git submodule update --init' to initialize the submodule."
        )

    print(f"Loading inscriptions from {js_path}...")
    content = js_path.read_text(encoding='utf-8')

    entries = extract_js_map_entries(content)
    print(f"  Found {len(entries)} inscription entries")

    inscriptions = {}
    parse_errors = 0

    for key, obj_str in entries:
        parsed = parse_js_object_safe(obj_str)
        if '_parse_error' in parsed:
            parse_errors += 1
        inscriptions[key] = parsed

    if parse_errors > 0:
        print(f"  Warning: {parse_errors} entries had parse errors")

    print(f"  Successfully parsed {len(inscriptions)} inscriptions")
    return inscriptions


def extract_cognate_map(content: str, var_name: str) -> dict:
    """Extract a simple cognate map (word -> [attestations])."""
    result = {}

    # Find the variable declaration
    pattern = rf'var\s+{var_name}\s*=\s*new\s+Map\s*\(\s*\['
    match = re.search(pattern, content)
    if not match:
        return result

    start = match.end()

    # Find entries: ["WORD", ['attestation1', 'attestation2', ...]]
    # Pattern for each entry
    entry_pattern = re.compile(r'\["([^"]+)",\s*\[([^\]]*)\]\]')

    for entry_match in entry_pattern.finditer(content[start:]):
        word = entry_match.group(1)
        attestations_str = entry_match.group(2)

        # Parse attestations
        attestations = re.findall(r"'([^']*)'", attestations_str)
        result[word] = attestations

    return result


def extract_similar_words(content: str) -> list:
    """Extract similar word pairs."""
    pairs = []

    # Find the variable declaration
    pattern = r'var\s+similarWords\s*=\s*new\s+Map\s*\(\s*\['
    match = re.search(pattern, content)
    if not match:
        return pairs

    start = match.end()

    # Find pairs: ["WORD_A", "WORD_B"]
    pair_pattern = re.compile(r'\["([^"]+)",\s*"([^"]+)"\]')

    for pair_match in pair_pattern.finditer(content[start:]):
        pairs.append({
            'wordA': pair_match.group(1),
            'wordB': pair_match.group(2)
        })

    return pairs


def load_cognates() -> dict:
    """Load and parse words_in_linearb.js."""
    js_path = LINEARA_DIR / "words_in_linearb.js"

    if not js_path.exists():
        raise FileNotFoundError(f"words_in_linearb.js not found at {js_path}")

    print(f"Loading Linear B cognates from {js_path}...")
    content = js_path.read_text(encoding='utf-8')

    result = {
        'identicalWords': extract_cognate_map(content, 'identicalWords'),
        'identicalRoots': extract_cognate_map(content, 'identicalRoots'),
        'similarWords': extract_similar_words(content)
    }

    print(f"  Identical words: {len(result['identicalWords'])}")
    print(f"  Identical roots: {len(result['identicalRoots'])}")
    print(f"  Similar word pairs: {len(result['similarWords'])}")

    return result


def compute_statistics(inscriptions: dict) -> dict:
    """Compute corpus statistics from parsed inscriptions."""
    print("Computing corpus statistics...")

    stats = {
        'generated': datetime.now().isoformat(),
        'attribution': {
            'source': 'lineara.xyz (https://github.com/mwenge/lineara.xyz)',
            'upstream': ['GORILA (Godart & Olivier)', 'George Douros', 'John Younger']
        },
        'total_inscriptions': len(inscriptions),
        'by_site': Counter(),
        'by_support': Counter(),
        'by_context': Counter(),
        'scribes': set(),
        'word_frequency': Counter(),
        'sites_full_names': {}
    }

    for name, data in inscriptions.items():
        if '_parse_error' in data:
            continue

        # Extract site from name (e.g., "HT1" -> "HT")
        site_match = re.match(r'^([A-Z]+)', name)
        if site_match:
            site_code = site_match.group(1)
            stats['by_site'][site_code] += 1

            # Track full site names
            site_name = data.get('site', '')
            if site_name and site_code not in stats['sites_full_names']:
                stats['sites_full_names'][site_code] = site_name

        # Count by support type
        support = data.get('support', 'Unknown')
        if support:
            stats['by_support'][support] += 1

        # Count by context/period
        context = data.get('context', 'Unknown')
        if context:
            stats['by_context'][context] += 1

        # Track scribes
        scribe = data.get('scribe', '')
        if scribe and scribe.strip():
            stats['scribes'].add(scribe)

        # Count word frequencies from transliterated words
        transliterated = data.get('transliteratedWords', [])
        for word in transliterated:
            if not word:
                continue
            word = str(word).strip()
            # Skip newlines, separators, pure numerals, fractions
            if word in ['\n', '𐄁', '', '—']:
                continue
            if re.match(r'^[\d\s.]+$', word):
                continue
            if word.startswith('𐝫'):  # Lacuna marker
                continue
            # Include meaningful words
            stats['word_frequency'][word] += 1

    # Convert sets and Counters to serializable formats
    stats['scribes'] = sorted(stats['scribes'])
    stats['by_site'] = dict(stats['by_site'].most_common())
    stats['by_support'] = dict(stats['by_support'].most_common())
    stats['by_context'] = dict(stats['by_context'].most_common())

    # Top 100 most frequent words
    stats['top_words'] = dict(stats['word_frequency'].most_common(100))
    stats['unique_words'] = len(stats['word_frequency'])
    del stats['word_frequency']

    print(f"  Sites: {len(stats['by_site'])}")
    print(f"  Scribes identified: {len(stats['scribes'])}")
    print(f"  Support types: {len(stats['by_support'])}")
    print(f"  Unique words: {stats['unique_words']}")

    return stats


def main():
    """Main entry point."""
    print("=" * 60)
    print("Linear A Corpus Parser")
    print("=" * 60)
    print()
    print("Attribution:")
    print("  Source: lineara.xyz (https://github.com/mwenge/lineara.xyz)")
    print("  Upstream: GORILA, George Douros, John Younger")
    print("  See ATTRIBUTION.md for full details")
    print()

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Load and parse data
    try:
        inscriptions = load_inscriptions()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1

    try:
        cognates = load_cognates()
    except FileNotFoundError as e:
        print(f"Warning: {e}")
        cognates = {}

    # Compute statistics
    statistics = compute_statistics(inscriptions)

    # Write output files
    print()
    print("Writing output files...")

    corpus_path = OUTPUT_DIR / "corpus.json"
    with open(corpus_path, 'w', encoding='utf-8') as f:
        json.dump({
            'attribution': {
                'source': 'lineara.xyz (https://github.com/mwenge/lineara.xyz)',
                'upstream': ['GORILA (Godart & Olivier)', 'George Douros', 'John Younger'],
                'license': 'See ATTRIBUTION.md',
                'generated': datetime.now().isoformat()
            },
            'inscriptions': inscriptions
        }, f, ensure_ascii=False, indent=2)
    print(f"  {corpus_path} ({corpus_path.stat().st_size / 1024:.1f} KB)")

    cognates_path = OUTPUT_DIR / "cognates.json"
    with open(cognates_path, 'w', encoding='utf-8') as f:
        json.dump({
            'attribution': {
                'source': 'lineara.xyz (https://github.com/mwenge/lineara.xyz)',
                'note': 'Linear B cognate mappings for anchor verification',
                'generated': datetime.now().isoformat()
            },
            **cognates
        }, f, ensure_ascii=False, indent=2)
    print(f"  {cognates_path} ({cognates_path.stat().st_size / 1024:.1f} KB)")

    stats_path = OUTPUT_DIR / "statistics.json"
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(statistics, f, ensure_ascii=False, indent=2)
    print(f"  {stats_path} ({stats_path.stat().st_size / 1024:.1f} KB)")

    print()
    print("=" * 60)
    print("Parsing complete!")
    print(f"  Inscriptions: {len(inscriptions)}")
    print(f"  Sites: {len(statistics['by_site'])}")
    print(f"  Cognate words: {len(cognates.get('identicalWords', {}))}")
    print(f"  Cognate roots: {len(cognates.get('identicalRoots', {}))}")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    exit(main())
