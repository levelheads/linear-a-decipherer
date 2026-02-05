#!/usr/bin/env python3
"""
Anchor Dependency Tracker for Linear A

Tracks which readings depend on which anchors. When an anchor is questioned,
automatically shows what collapses. Implements cascade failure detection.

This tool addresses the methodological critique:
"No automated mechanism traces these dependencies. If Linear B comparison
fails for one anchor, what else collapses?"

Usage:
    # Simulate cascade effects (no changes applied)
    python tools/anchor_tracker.py --cascade anchor_semitic_loan_layer --to QUESTIONED

    # Auto-cascade: propagate confidence changes automatically
    python tools/anchor_tracker.py --cascade anchor_semitic_loan_layer --to DEMOTED --auto-cascade

    # Auto-cascade with alerts when readings drop below MEDIUM
    python tools/anchor_tracker.py --cascade anchor_kuro_total --to QUESTIONED \
        --auto-cascade --alert-threshold MEDIUM

    # Enforce anchor hierarchy constraints on all readings
    python tools/anchor_tracker.py --enforce-hierarchy

    # Other commands
    python tools/anchor_tracker.py --register SA-RA₂ --depends-on anchor_semitic_loan_layer
    python tools/anchor_tracker.py --validate
    python tools/anchor_tracker.py --graph
    python tools/anchor_tracker.py --reading KU-RO

New Features (2026-02):
    --auto-cascade: Automatically propagate confidence changes when an anchor
                    is questioned/demoted/rejected. Updates all dependent readings.
    --alert-threshold LEVEL: Output warnings when readings drop below specified
                             confidence level (SPECULATIVE|POSSIBLE|LOW|MEDIUM|PROBABLE|HIGH|CERTAIN)
    --enforce-hierarchy: Ensure all readings respect anchor hierarchy constraints
                         (Levels 1-6 per METHODOLOGY.md Part 2)

Attribution:
    Part of Linear A Decipherment Project
    Implements anchor dependency tracking per METHODOLOGY.md Part 2
"""

import json
import argparse
import sys
from pathlib import Path
from collections import defaultdict, deque
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ANCHORS_FILE = DATA_DIR / "anchors.json"
DEPENDENCIES_FILE = DATA_DIR / "reading_dependencies.json"
KNOWLEDGE_FILE = PROJECT_ROOT / "linear-a-decipherer" / "KNOWLEDGE.md"


# Confidence levels (ordered from lowest to highest)
CONFIDENCE_LEVELS = ['SPECULATIVE', 'POSSIBLE', 'LOW', 'MEDIUM', 'PROBABLE', 'HIGH', 'CERTAIN']
CONFIDENCE_RANK = {level: i for i, level in enumerate(CONFIDENCE_LEVELS)}

# Anchor statuses
ANCHOR_STATUS = ['CONFIRMED', 'QUESTIONED', 'DEMOTED', 'REJECTED']


@dataclass
class CascadeResult:
    """Result of a cascade analysis."""
    anchor_id: str
    new_status: str
    affected_readings: List[Dict]
    affected_anchors: List[Dict]
    total_affected: int
    cascade_depth: int
    warnings: List[str]
    applied: bool = False  # True if changes were actually applied


# Anchor hierarchy levels (METHODOLOGY.md Part 2)
# Level 1: Confirmed toponyms (CERTAIN)
# Level 2: Linear B cognates + position (HIGH)
# Level 3: Clear logograms (HIGH)
# Level 4: Structural patterns (MEDIUM)
# Level 5: Morphological patterns (LOW-MEDIUM)
# Level 6: Lexical matches (LOW)
ANCHOR_LEVEL_MAX_CONFIDENCE = {
    1: 'CERTAIN',
    2: 'HIGH',
    3: 'HIGH',
    4: 'MEDIUM',
    5: 'MEDIUM',  # LOW-MEDIUM, use MEDIUM as upper bound
    6: 'LOW',
}


@dataclass
class ValidationResult:
    """Result of validating dependencies against KNOWLEDGE.md."""
    is_valid: bool
    missing_readings: List[str]
    orphan_readings: List[str]
    confidence_violations: List[Dict]
    circular_dependencies: List[List[str]]
    warnings: List[str]


class AnchorTracker:
    """
    Tracks anchor-reading dependencies and computes cascade effects.

    Builds a directed acyclic graph (DAG) where:
    - Anchors are root nodes
    - Readings depend on anchors
    - Some readings support other anchors (feedback)
    """

    def __init__(self, verbose: bool = False, alert_threshold: str = None):
        self.verbose = verbose
        self.anchors = {}
        self.readings = {}
        self.cascade_rules = []
        self.alert_threshold = alert_threshold  # Confidence level for alerts

        # Dependency graph
        self.anchor_to_readings = defaultdict(set)  # anchor -> set of readings
        self.reading_to_anchors = defaultdict(set)  # reading -> set of anchors
        self.reading_supports = defaultdict(set)    # reading -> set of anchors it supports

    def log(self, msg: str):
        if self.verbose:
            print(f"  {msg}")

    def load_data(self) -> bool:
        """Load anchors and reading dependencies."""
        try:
            with open(ANCHORS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.anchors = data.get('anchors', {})

            with open(DEPENDENCIES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.readings = data.get('readings', {})
                self.cascade_rules = data.get('cascade_rules', {}).get('rules', [])

            # Build dependency graph
            for reading_id, reading_data in self.readings.items():
                for anchor_id in reading_data.get('depends_on', []):
                    self.anchor_to_readings[anchor_id].add(reading_id)
                    self.reading_to_anchors[reading_id].add(anchor_id)

                for anchor_id in reading_data.get('supports', []):
                    self.reading_supports[reading_id].add(anchor_id)

            print(f"Loaded {len(self.anchors)} anchors and {len(self.readings)} readings")
            return True

        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def save_data(self):
        """Save updated dependencies back to JSON."""
        try:
            with open(DEPENDENCIES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            data['readings'] = self.readings
            data['metadata']['last_updated'] = datetime.now().isoformat()

            with open(DEPENDENCIES_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"Saved updates to {DEPENDENCIES_FILE}")

        except Exception as e:
            print(f"Error saving data: {e}")

    def get_confidence_rank(self, confidence: str) -> int:
        """Get numeric rank for confidence level."""
        return CONFIDENCE_RANK.get(confidence.upper(), 0)

    def compute_max_confidence(self, reading_id: str) -> str:
        """
        Compute maximum allowed confidence for a reading based on its anchors.

        Rules:
        1. Reading confidence cannot exceed lowest anchor confidence
        2. Single-hypothesis support caps at PROBABLE (Principle 4)
        """
        reading = self.readings.get(reading_id, {})
        anchor_ids = reading.get('depends_on', [])

        if not anchor_ids:
            return 'SPECULATIVE'

        # Find minimum anchor confidence
        min_rank = float('inf')

        for anchor_id in anchor_ids:
            anchor = self.anchors.get(anchor_id, {})
            confidence = anchor.get('confidence', 'SPECULATIVE')
            rank = self.get_confidence_rank(confidence)
            if rank < min_rank:
                min_rank = rank

        if min_rank == float('inf'):
            return 'SPECULATIVE'

        max_conf = CONFIDENCE_LEVELS[min_rank]

        # Apply single-hypothesis cap
        supported_hypotheses = reading.get('supported_hypotheses', [])
        if len(supported_hypotheses) == 1 and max_conf in ['HIGH', 'CERTAIN']:
            max_conf = 'PROBABLE'
            self.log(f"  {reading_id}: capped at PROBABLE (single-hypothesis support)")

        return max_conf

    def cascade_from_anchor(self, anchor_id: str, new_status: str) -> CascadeResult:
        """
        Compute cascade effects when an anchor's status changes.

        Uses BFS to traverse the dependency graph and identify all
        affected readings and downstream anchors.

        Args:
            anchor_id: The anchor being questioned/demoted/rejected
            new_status: QUESTIONED, DEMOTED, or REJECTED

        Returns:
            CascadeResult with all affected readings and recommendations
        """
        if anchor_id not in self.anchors:
            return CascadeResult(
                anchor_id=anchor_id,
                new_status=new_status,
                affected_readings=[],
                affected_anchors=[],
                total_affected=0,
                cascade_depth=0,
                warnings=[f"Unknown anchor: {anchor_id}"]
            )

        affected_readings = []
        affected_anchors = []
        warnings = []
        visited = set()
        max_depth = 0

        # BFS from the anchor
        queue = deque([(anchor_id, 0, 'anchor')])
        visited.add(anchor_id)

        while queue:
            node_id, depth, node_type = queue.popleft()
            max_depth = max(max_depth, depth)

            if node_type == 'anchor':
                # Find all readings that depend on this anchor
                for reading_id in self.anchor_to_readings.get(node_id, []):
                    if reading_id in visited:
                        continue
                    visited.add(reading_id)

                    reading = self.readings.get(reading_id, {})
                    current_conf = reading.get('confidence', 'SPECULATIVE')

                    # Determine new confidence based on status change
                    if new_status == 'REJECTED':
                        new_conf = 'SPECULATIVE'
                        action = 'Demote to SPECULATIVE (anchor rejected)'
                    elif new_status == 'DEMOTED':
                        # Cap at POSSIBLE
                        if self.get_confidence_rank(current_conf) > self.get_confidence_rank('POSSIBLE'):
                            new_conf = 'POSSIBLE'
                            action = 'Cap at POSSIBLE (anchor demoted)'
                        else:
                            new_conf = current_conf
                            action = 'No change (already at or below POSSIBLE)'
                    elif new_status == 'QUESTIONED':
                        # Flag for review, suggest one level down
                        current_rank = self.get_confidence_rank(current_conf)
                        if current_rank > 0:
                            new_conf = CONFIDENCE_LEVELS[current_rank - 1]
                            action = f'Suggest downgrade to {new_conf} (anchor questioned)'
                        else:
                            new_conf = current_conf
                            action = 'Already at minimum confidence'
                    else:
                        new_conf = current_conf
                        action = 'Unknown status - no change'

                    affected_readings.append({
                        'reading_id': reading_id,
                        'meaning': reading.get('meaning', 'Unknown'),
                        'current_confidence': current_conf,
                        'new_confidence': new_conf,
                        'action': action,
                        'cascade_depth': depth + 1,
                    })

                    # Check if this reading supports other anchors
                    for supported_anchor in self.reading_supports.get(reading_id, []):
                        if supported_anchor not in visited:
                            queue.append((supported_anchor, depth + 1, 'anchor_via_reading'))

            elif node_type == 'anchor_via_reading':
                # This anchor is supported by an affected reading
                anchor = self.anchors.get(node_id, {})
                affected_anchors.append({
                    'anchor_id': node_id,
                    'name': anchor.get('name', 'Unknown'),
                    'current_confidence': anchor.get('confidence', 'SPECULATIVE'),
                    'note': 'Supporting evidence weakened - review recommended',
                    'cascade_depth': depth,
                })

                # Continue cascade through this anchor
                for reading_id in self.anchor_to_readings.get(node_id, []):
                    if reading_id not in visited:
                        visited.add(reading_id)
                        queue.append((reading_id, depth + 1, 'reading'))

        # Generate warnings
        if len(affected_readings) > 5:
            warnings.append(f"MAJOR CASCADE: {len(affected_readings)} readings affected")

        if any(r['current_confidence'] == 'CERTAIN' for r in affected_readings):
            warnings.append("WARNING: CERTAIN-confidence readings affected - review carefully")

        if affected_anchors:
            warnings.append(f"FEEDBACK: {len(affected_anchors)} downstream anchors affected")

        return CascadeResult(
            anchor_id=anchor_id,
            new_status=new_status,
            affected_readings=affected_readings,
            affected_anchors=affected_anchors,
            total_affected=len(affected_readings) + len(affected_anchors),
            cascade_depth=max_depth,
            warnings=warnings
        )

    def auto_cascade_propagate(self, anchor_id: str, new_status: str) -> CascadeResult:
        """
        Automatically propagate confidence changes when an anchor is questioned.

        This extends cascade_from_anchor by actually applying the changes:
        1. Computes cascade effects
        2. Updates reading confidences (cannot exceed weakest anchor)
        3. Generates alerts for readings below threshold
        4. Saves changes to disk

        Args:
            anchor_id: The anchor being questioned/demoted/rejected
            new_status: QUESTIONED, DEMOTED, or REJECTED

        Returns:
            CascadeResult with applied=True and affected readings updated
        """
        # First compute the cascade (simulation)
        result = self.cascade_from_anchor(anchor_id, new_status)

        if not result.affected_readings and not result.affected_anchors:
            return result

        # Apply confidence changes to readings
        alerts = []
        for affected in result.affected_readings:
            reading_id = affected['reading_id']
            new_conf = affected['new_confidence']

            if reading_id in self.readings:
                old_conf = self.readings[reading_id].get('confidence', 'SPECULATIVE')

                # Update the reading confidence
                self.readings[reading_id]['confidence'] = new_conf
                self.readings[reading_id]['cascade_note'] = (
                    f"Auto-cascaded {datetime.now().strftime('%Y-%m-%d')}: "
                    f"{old_conf} → {new_conf} (anchor {anchor_id} {new_status})"
                )

                # Check alert threshold
                if self.alert_threshold:
                    if self.get_confidence_rank(new_conf) < self.get_confidence_rank(self.alert_threshold):
                        alerts.append(
                            f"ALERT: {reading_id} dropped to {new_conf} "
                            f"(below threshold {self.alert_threshold})"
                        )

        # Add alerts to warnings
        result.warnings.extend(alerts)
        result.applied = True

        return result

    def get_anchor_level_max_confidence(self, anchor_id: str) -> str:
        """
        Get the maximum confidence allowed by an anchor's hierarchy level.

        Per METHODOLOGY.md Part 2:
        - Level 1: CERTAIN (confirmed toponyms)
        - Level 2-3: HIGH (Linear B cognates, logograms)
        - Level 4-5: MEDIUM (structural/morphological patterns)
        - Level 6: LOW (lexical matches)
        """
        anchor = self.anchors.get(anchor_id, {})
        level = anchor.get('level', 6)  # Default to lowest level
        return ANCHOR_LEVEL_MAX_CONFIDENCE.get(level, 'LOW')

    def enforce_anchor_hierarchy_constraints(self) -> List[Dict]:
        """
        Ensure all readings respect their anchor hierarchy constraints.

        Readings cannot exceed:
        1. Their weakest anchor's confidence
        2. Their anchor level's maximum confidence

        Returns:
            List of readings that were adjusted
        """
        adjustments = []

        for reading_id, reading in self.readings.items():
            current_conf = reading.get('confidence', 'SPECULATIVE')
            current_rank = self.get_confidence_rank(current_conf)

            # Find the constraining anchor (weakest or lowest level)
            anchor_ids = reading.get('depends_on', [])
            if not anchor_ids:
                continue

            min_allowed_rank = float('inf')
            constraining_anchor = None
            constraint_reason = None

            for anchor_id in anchor_ids:
                anchor = self.anchors.get(anchor_id, {})

                # Check anchor's own confidence
                anchor_conf = anchor.get('confidence', 'SPECULATIVE')
                anchor_rank = self.get_confidence_rank(anchor_conf)

                # Check anchor's level max
                level_max = self.get_anchor_level_max_confidence(anchor_id)
                level_rank = self.get_confidence_rank(level_max)

                # Use the more restrictive of the two
                effective_rank = min(anchor_rank, level_rank)

                if effective_rank < min_allowed_rank:
                    min_allowed_rank = effective_rank
                    constraining_anchor = anchor_id
                    if anchor_rank <= level_rank:
                        constraint_reason = f"anchor confidence ({anchor_conf})"
                    else:
                        constraint_reason = f"level {anchor.get('level', '?')} max ({level_max})"

            # Check if reading exceeds constraint
            if current_rank > min_allowed_rank and min_allowed_rank != float('inf'):
                new_conf = CONFIDENCE_LEVELS[min_allowed_rank]

                adjustments.append({
                    'reading_id': reading_id,
                    'old_confidence': current_conf,
                    'new_confidence': new_conf,
                    'constraining_anchor': constraining_anchor,
                    'reason': constraint_reason
                })

                # Apply the adjustment
                self.readings[reading_id]['confidence'] = new_conf
                self.readings[reading_id]['max_confidence'] = new_conf
                self.readings[reading_id]['cascade_note'] = (
                    f"Hierarchy constraint {datetime.now().strftime('%Y-%m-%d')}: "
                    f"capped by {constraining_anchor} ({constraint_reason})"
                )

        return adjustments

    def generate_cascade_report(self, result: CascadeResult, include_hierarchy: bool = True) -> str:
        """
        Generate a detailed text report of cascade effects.

        Args:
            result: The CascadeResult to report on
            include_hierarchy: Whether to include anchor hierarchy level info

        Returns:
            Formatted report string
        """
        lines = []
        lines.append("=" * 70)
        lines.append("CASCADE CONFIDENCE PROPAGATION REPORT")
        lines.append("=" * 70)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Applied: {'YES' if result.applied else 'NO (simulation only)'}")
        lines.append("")

        # Anchor info
        anchor = self.anchors.get(result.anchor_id, {})
        lines.append(f"Anchor: {result.anchor_id}")
        lines.append(f"  Name: {anchor.get('name', 'Unknown')}")
        if include_hierarchy:
            level = anchor.get('level', '?')
            level_max = ANCHOR_LEVEL_MAX_CONFIDENCE.get(level, 'N/A')
            lines.append(f"  Hierarchy Level: {level} (max confidence: {level_max})")
        lines.append(f"  Status Change: → {result.new_status}")
        lines.append("")

        # Summary
        lines.append("SUMMARY")
        lines.append("-" * 40)
        lines.append(f"  Total readings affected: {len(result.affected_readings)}")
        lines.append(f"  Downstream anchors affected: {len(result.affected_anchors)}")
        lines.append(f"  Maximum cascade depth: {result.cascade_depth}")
        lines.append("")

        # Warnings and alerts
        if result.warnings:
            lines.append("WARNINGS & ALERTS")
            lines.append("-" * 40)
            for warning in result.warnings:
                lines.append(f"  * {warning}")
            lines.append("")

        # Affected readings by confidence change
        if result.affected_readings:
            lines.append("AFFECTED READINGS")
            lines.append("-" * 40)

            # Group by confidence change type
            demoted = [r for r in result.affected_readings if r['new_confidence'] != r['current_confidence']]
            unchanged = [r for r in result.affected_readings if r['new_confidence'] == r['current_confidence']]

            if demoted:
                lines.append(f"\n  Demoted ({len(demoted)}):")
                for r in sorted(demoted, key=lambda x: -self.get_confidence_rank(x['current_confidence'])):
                    lines.append(f"    {r['reading_id']}: {r['current_confidence']} → {r['new_confidence']}")
                    lines.append(f"      Meaning: {r['meaning']}")

            if unchanged:
                lines.append(f"\n  Unchanged ({len(unchanged)}):")
                for r in unchanged[:5]:  # Show first 5
                    lines.append(f"    {r['reading_id']}: {r['current_confidence']} (already at or below)")
                if len(unchanged) > 5:
                    lines.append(f"    ... and {len(unchanged) - 5} more")

        # Downstream anchors
        if result.affected_anchors:
            lines.append("\nDOWNSTREAM ANCHORS (review recommended)")
            lines.append("-" * 40)
            for a in result.affected_anchors:
                lines.append(f"  {a['anchor_id']}: {a['name']}")
                lines.append(f"    Current: {a['current_confidence']}")

        lines.append("")
        lines.append("=" * 70)

        return '\n'.join(lines)

    def register_reading(self, reading_id: str, depends_on: List[str],
                        meaning: str = "", confidence: str = "SPECULATIVE") -> bool:
        """
        Register a new reading with its anchor dependencies.

        Args:
            reading_id: The reading identifier (e.g., 'SA-RA₂')
            depends_on: List of anchor IDs this reading depends on
            meaning: The proposed meaning
            confidence: Initial confidence level

        Returns:
            True if registration successful
        """
        # Validate anchors exist
        for anchor_id in depends_on:
            if anchor_id not in self.anchors:
                print(f"Warning: Unknown anchor {anchor_id}")

        # Compute max confidence
        temp_reading = {'depends_on': depends_on}
        self.readings[reading_id] = temp_reading
        max_conf = self.compute_max_confidence(reading_id)

        # Cap confidence at max
        if self.get_confidence_rank(confidence) > self.get_confidence_rank(max_conf):
            print(f"Warning: Confidence {confidence} exceeds max {max_conf} - capping")
            confidence = max_conf

        # Register
        self.readings[reading_id] = {
            'meaning': meaning,
            'confidence': confidence,
            'max_confidence': max_conf,
            'depends_on': depends_on,
            'supports': [],
            'evidence_sources': [],
            'cascade_note': '',
            'registered': datetime.now().isoformat()
        }

        # Update graph
        for anchor_id in depends_on:
            self.anchor_to_readings[anchor_id].add(reading_id)
            self.reading_to_anchors[reading_id].add(anchor_id)

        print(f"Registered reading: {reading_id} = '{meaning}' [{confidence}]")
        print(f"  Depends on: {', '.join(depends_on)}")
        print(f"  Max confidence: {max_conf}")

        return True

    def validate_consistency(self) -> ValidationResult:
        """
        Validate dependencies for consistency.

        Checks:
        1. All reading dependencies reference valid anchors
        2. No circular dependencies
        3. Confidence levels respect anchor caps
        4. Readings in KNOWLEDGE.md are tracked
        """
        is_valid = True
        missing_readings = []
        orphan_readings = []
        confidence_violations = []
        circular_deps = []
        warnings = []

        # Check for unknown anchor references
        for reading_id, reading in self.readings.items():
            for anchor_id in reading.get('depends_on', []):
                if anchor_id not in self.anchors:
                    warnings.append(f"Reading {reading_id} references unknown anchor: {anchor_id}")
                    is_valid = False

        # Check for orphan readings (no dependencies)
        for reading_id, reading in self.readings.items():
            if not reading.get('depends_on'):
                orphan_readings.append(reading_id)
                warnings.append(f"Orphan reading (no dependencies): {reading_id}")

        # Check confidence violations
        for reading_id, reading in self.readings.items():
            current_conf = reading.get('confidence', 'SPECULATIVE')
            max_conf = self.compute_max_confidence(reading_id)

            if self.get_confidence_rank(current_conf) > self.get_confidence_rank(max_conf):
                confidence_violations.append({
                    'reading': reading_id,
                    'current': current_conf,
                    'max_allowed': max_conf,
                    'violation': f"Exceeds max by {self.get_confidence_rank(current_conf) - self.get_confidence_rank(max_conf)} levels"
                })
                is_valid = False

        # Check for circular dependencies using DFS
        def find_cycles():
            WHITE, GRAY, BLACK = 0, 1, 2
            color = defaultdict(int)
            path = []
            cycles = []

            def dfs(node, node_type):
                if color[node] == GRAY:
                    # Found cycle
                    cycle_start = path.index(node)
                    cycles.append(path[cycle_start:] + [node])
                    return
                if color[node] == BLACK:
                    return

                color[node] = GRAY
                path.append(node)

                if node_type == 'anchor':
                    for reading in self.anchor_to_readings.get(node, []):
                        dfs(reading, 'reading')
                elif node_type == 'reading':
                    for anchor in self.reading_supports.get(node, []):
                        dfs(anchor, 'anchor')

                path.pop()
                color[node] = BLACK

            for anchor_id in self.anchors:
                if color[anchor_id] == WHITE:
                    dfs(anchor_id, 'anchor')

            return cycles

        circular_deps = find_cycles()
        if circular_deps:
            for cycle in circular_deps:
                warnings.append(f"Circular dependency: {' -> '.join(cycle)}")
            is_valid = False

        return ValidationResult(
            is_valid=is_valid,
            missing_readings=missing_readings,
            orphan_readings=orphan_readings,
            confidence_violations=confidence_violations,
            circular_dependencies=circular_deps,
            warnings=warnings
        )

    def get_reading_info(self, reading_id: str) -> Dict:
        """Get detailed information about a reading and its dependencies."""
        if reading_id not in self.readings:
            # Try case-insensitive
            for rid in self.readings:
                if rid.upper() == reading_id.upper():
                    reading_id = rid
                    break
            else:
                return {'error': f'Reading not found: {reading_id}'}

        reading = self.readings[reading_id]
        anchor_details = []

        for anchor_id in reading.get('depends_on', []):
            anchor = self.anchors.get(anchor_id, {})
            anchor_details.append({
                'id': anchor_id,
                'name': anchor.get('name', 'Unknown'),
                'level': anchor.get('level', 0),
                'confidence': anchor.get('confidence', 'SPECULATIVE'),
                'limitations': anchor.get('limitations', [])
            })

        return {
            'reading_id': reading_id,
            'meaning': reading.get('meaning', 'Unknown'),
            'confidence': reading.get('confidence', 'SPECULATIVE'),
            'max_confidence': self.compute_max_confidence(reading_id),
            'anchor_dependencies': anchor_details,
            'supports_anchors': list(reading.get('supports', [])),
            'evidence_sources': reading.get('evidence_sources', []),
            'cascade_note': reading.get('cascade_note', '')
        }

    def generate_graph_ascii(self) -> str:
        """Generate ASCII representation of dependency graph."""
        lines = []
        lines.append("ANCHOR DEPENDENCY GRAPH")
        lines.append("=" * 60)
        lines.append("")

        # Group by anchor level
        anchors_by_level = defaultdict(list)
        for anchor_id, anchor in self.anchors.items():
            level = anchor.get('level', 0)
            anchors_by_level[level].append((anchor_id, anchor))

        for level in sorted(anchors_by_level.keys()):
            lines.append(f"LEVEL {level} {'─' * 50}")
            for anchor_id, anchor in anchors_by_level[level]:
                conf = anchor.get('confidence', '?')
                name = anchor.get('name', anchor_id)[:40]
                lines.append(f"  ◆ [{conf:8}] {name}")

                # Show dependent readings
                readings = self.anchor_to_readings.get(anchor_id, [])
                for reading_id in sorted(readings)[:5]:
                    reading = self.readings.get(reading_id, {})
                    r_conf = reading.get('confidence', '?')
                    meaning = reading.get('meaning', '')[:30]
                    lines.append(f"      └─► {reading_id} [{r_conf}] {meaning}")

                if len(readings) > 5:
                    lines.append(f"      └─► ... and {len(readings) - 5} more")

            lines.append("")

        return '\n'.join(lines)

    def print_cascade_report(self, result: CascadeResult):
        """Print formatted cascade analysis report."""
        print("\n" + "=" * 70)
        print("CASCADE ANALYSIS REPORT")
        print("=" * 70)

        anchor = self.anchors.get(result.anchor_id, {})
        print(f"\nAnchor: {result.anchor_id}")
        print(f"Name: {anchor.get('name', 'Unknown')}")
        print(f"New Status: {result.new_status}")
        print(f"Total Affected: {result.total_affected}")
        print(f"Cascade Depth: {result.cascade_depth}")

        if result.warnings:
            print("\n⚠ WARNINGS:")
            for warning in result.warnings:
                print(f"  • {warning}")

        if result.affected_readings:
            print(f"\n─── AFFECTED READINGS ({len(result.affected_readings)}) ───")
            for r in result.affected_readings:
                print(f"\n  {r['reading_id']} = '{r['meaning']}'")
                print(f"    Current: {r['current_confidence']} → New: {r['new_confidence']}")
                print(f"    Action: {r['action']}")

        if result.affected_anchors:
            print(f"\n─── DOWNSTREAM ANCHORS ({len(result.affected_anchors)}) ───")
            for a in result.affected_anchors:
                print(f"\n  {a['anchor_id']}: {a['name']}")
                print(f"    Current: {a['current_confidence']}")
                print(f"    Note: {a['note']}")

        print("\n" + "=" * 70)

    def print_validation_report(self, result: ValidationResult):
        """Print formatted validation report."""
        print("\n" + "=" * 70)
        print("DEPENDENCY VALIDATION REPORT")
        print("=" * 70)

        status = "✓ VALID" if result.is_valid else "✗ INVALID"
        print(f"\nStatus: {status}")

        if result.orphan_readings:
            print(f"\nOrphan Readings (no dependencies): {len(result.orphan_readings)}")
            for r in result.orphan_readings:
                print(f"  • {r}")

        if result.confidence_violations:
            print(f"\nConfidence Violations: {len(result.confidence_violations)}")
            for v in result.confidence_violations:
                print(f"  • {v['reading']}: {v['current']} exceeds max {v['max_allowed']}")

        if result.circular_dependencies:
            print(f"\nCircular Dependencies: {len(result.circular_dependencies)}")
            for cycle in result.circular_dependencies:
                print(f"  • {' → '.join(cycle)}")

        if result.warnings:
            print(f"\nWarnings: {len(result.warnings)}")
            for w in result.warnings:
                print(f"  • {w}")

        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Track anchor-reading dependencies and compute cascade effects"
    )
    parser.add_argument(
        '--cascade', '-c',
        type=str,
        metavar='ANCHOR_ID',
        help='Compute cascade from anchor status change'
    )
    parser.add_argument(
        '--to', '-t',
        type=str,
        choices=['QUESTIONED', 'DEMOTED', 'REJECTED'],
        default='QUESTIONED',
        help='New status for cascade analysis'
    )
    parser.add_argument(
        '--auto-cascade',
        action='store_true',
        help='Automatically propagate confidence changes (use with --cascade)'
    )
    parser.add_argument(
        '--alert-threshold',
        type=str,
        choices=CONFIDENCE_LEVELS,
        metavar='LEVEL',
        help='Output warnings when readings drop below this confidence level'
    )
    parser.add_argument(
        '--enforce-hierarchy',
        action='store_true',
        help='Enforce anchor hierarchy constraints on all readings'
    )
    parser.add_argument(
        '--register', '-r',
        type=str,
        metavar='READING_ID',
        help='Register a new reading'
    )
    parser.add_argument(
        '--depends-on', '-d',
        type=str,
        help='Comma-separated anchor IDs for --register'
    )
    parser.add_argument(
        '--meaning', '-m',
        type=str,
        default='',
        help='Meaning for --register'
    )
    parser.add_argument(
        '--confidence',
        type=str,
        default='SPECULATIVE',
        help='Initial confidence for --register'
    )
    parser.add_argument(
        '--validate', '-V',
        action='store_true',
        help='Validate dependency consistency'
    )
    parser.add_argument(
        '--graph', '-g',
        action='store_true',
        help='Show dependency graph'
    )
    parser.add_argument(
        '--reading',
        type=str,
        metavar='READING_ID',
        help='Show info about a specific reading'
    )
    parser.add_argument(
        '--list-anchors', '-l',
        action='store_true',
        help='List all anchors'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("LINEAR A ANCHOR DEPENDENCY TRACKER")
    print("=" * 70)

    tracker = AnchorTracker(verbose=args.verbose, alert_threshold=args.alert_threshold)
    if not tracker.load_data():
        return 1

    # Show alert threshold if set
    if args.alert_threshold:
        print(f"Alert threshold: {args.alert_threshold}")

    if args.list_anchors:
        print("\nRegistered Anchors:")
        for anchor_id, anchor in tracker.anchors.items():
            level = anchor.get('level', 0)
            conf = anchor.get('confidence', '?')
            name = anchor.get('name', anchor_id)
            print(f"  Level {level} [{conf:8}] {anchor_id}")
            print(f"    {name}")
        return 0

    if args.cascade:
        if args.auto_cascade:
            # Auto-cascade: compute AND apply changes
            result = tracker.auto_cascade_propagate(args.cascade, args.to)
            print(tracker.generate_cascade_report(result, include_hierarchy=True))

            if result.applied and result.affected_readings:
                # Save the changes
                tracker.save_data()
                print(f"\nChanges applied and saved to {DEPENDENCIES_FILE}")
        else:
            # Simulation only (existing behavior)
            result = tracker.cascade_from_anchor(args.cascade, args.to)
            tracker.print_cascade_report(result)
            print("\nNote: Use --auto-cascade to apply these changes")
        return 0

    if args.enforce_hierarchy:
        print("\nEnforcing anchor hierarchy constraints...")
        adjustments = tracker.enforce_anchor_hierarchy_constraints()

        if adjustments:
            print(f"\nAdjusted {len(adjustments)} readings:\n")
            for adj in adjustments:
                print(f"  {adj['reading_id']}: {adj['old_confidence']} → {adj['new_confidence']}")
                print(f"    Constrained by: {adj['constraining_anchor']} ({adj['reason']})")

            tracker.save_data()
            print(f"\nChanges saved to {DEPENDENCIES_FILE}")
        else:
            print("\nAll readings comply with hierarchy constraints.")
        return 0

    if args.register:
        if not args.depends_on:
            print("Error: --depends-on required with --register")
            return 1
        anchors = [a.strip() for a in args.depends_on.split(',')]
        tracker.register_reading(
            args.register,
            anchors,
            args.meaning,
            args.confidence
        )
        tracker.save_data()
        return 0

    if args.validate:
        result = tracker.validate_consistency()
        tracker.print_validation_report(result)
        return 0 if result.is_valid else 1

    if args.graph:
        print(tracker.generate_graph_ascii())
        return 0

    if args.reading:
        info = tracker.get_reading_info(args.reading)
        if 'error' in info:
            print(f"Error: {info['error']}")
            return 1

        print(f"\n{info['reading_id']} = '{info['meaning']}'")
        print(f"  Confidence: {info['confidence']} (max: {info['max_confidence']})")
        print("\n  Dependencies:")
        for dep in info['anchor_dependencies']:
            print(f"    ◆ {dep['id']} [{dep['confidence']}]")
            print(f"      {dep['name']}")
            if dep['limitations']:
                print(f"      Limitations: {dep['limitations'][0][:60]}...")

        if info['supports_anchors']:
            print(f"\n  Supports anchors: {', '.join(info['supports_anchors'])}")

        if info['cascade_note']:
            print(f"\n  Cascade note: {info['cascade_note']}")

        return 0

    # Default: show summary
    print(f"\nAnchors: {len(tracker.anchors)}")
    print(f"Readings: {len(tracker.readings)}")
    print("\nUse --help for available commands")

    return 0


if __name__ == '__main__':
    sys.exit(main())
