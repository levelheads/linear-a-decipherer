#!/usr/bin/env python3
"""
compare_results.py - Compare pre-fix and post-fix hypothesis testing results.

Analyzes differences in:
  - hypothesis_results (per-word scores, confidence, best hypothesis)
  - batch_analysis_results (high-confidence lists, hypothesis rankings)

Usage:
    python3 tools/compare_results.py
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

# File paths
BASE = Path("/Users/home/AI/Disciplines/Deciphering Ancient Languages/data")

HYPO_PRE  = BASE / "hypothesis_results_prefix.json"
HYPO_POST = BASE / "hypothesis_results.json"
BATCH_PRE  = BASE / "batch_analysis_results_prefix.json"
BATCH_POST = BASE / "batch_analysis_results.json"

# K-R paradigm words of special interest
KR_WORDS = {"KU-RO", "KI-RO", "SA-RA\u2082"}  # SA-RA followed by subscript 2

# Confidence tiers (ordered low -> high)
CONFIDENCE_ORDER = {
    "SPECULATIVE": 0,
    "LOW": 1,
    "MEDIUM": 2,
    "POSSIBLE": 3,
    "PROBABLE": 4,
    "HIGH": 5,
    "CERTAIN": 6,
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def confidence_rank(label):
    return CONFIDENCE_ORDER.get(label.upper(), -1) if label else -1


def fmt_delta(val):
    if val > 0:
        return f"+{val:.2f}"
    return f"{val:.2f}"


# ===========================================================================
# 1. Hypothesis Results Comparison
# ===========================================================================

def compare_hypothesis_results(pre, post):
    pre_words = pre["word_analyses"]
    post_words = post["word_analyses"]

    words_only_pre = sorted(set(pre_words.keys()) - set(post_words.keys()))
    words_only_post = sorted(set(post_words.keys()) - set(pre_words.keys()))
    common_words = sorted(set(pre_words.keys()) & set(post_words.keys()))

    confidence_demotions = []
    confidence_promotions = []
    best_hyp_changes = []
    score_changes = defaultdict(list)
    kr_diffs = []
    pregreek_changes = []

    for word in common_words:
        syn_pre = pre_words[word].get("synthesis", {})
        syn_post = post_words[word].get("synthesis", {})

        conf_pre = syn_pre.get("max_confidence", "")
        conf_post = syn_post.get("max_confidence", "")
        best_pre = syn_pre.get("best_hypothesis", "")
        best_post = syn_post.get("best_hypothesis", "")
        score_pre = syn_pre.get("best_score", 0)
        score_post = syn_post.get("best_score", 0)

        r_pre = confidence_rank(conf_pre)
        r_post = confidence_rank(conf_post)
        if r_post < r_pre:
            confidence_demotions.append((word, conf_pre, conf_post, score_pre, score_post))
        elif r_post > r_pre:
            confidence_promotions.append((word, conf_pre, conf_post, score_pre, score_post))

        if best_pre != best_post:
            best_hyp_changes.append((word, best_pre, best_post, score_pre, score_post))

        hyps_pre = pre_words[word].get("hypotheses", {})
        hyps_post = post_words[word].get("hypotheses", {})
        for hyp in sorted(set(hyps_pre.keys()) | set(hyps_post.keys())):
            s_pre = hyps_pre.get(hyp, {}).get("score", 0)
            s_post = hyps_post.get(hyp, {}).get("score", 0)
            if s_pre != s_post:
                score_changes[hyp].append((word, s_pre, s_post))

        if word in KR_WORDS:
            kr_entry = {
                "word": word,
                "conf_pre": conf_pre, "conf_post": conf_post,
                "best_pre": best_pre, "best_post": best_post,
                "score_pre": score_pre, "score_post": score_post,
                "hyp_scores_pre": {h: hyps_pre.get(h, {}).get("score", 0) for h in sorted(set(hyps_pre) | set(hyps_post))},
                "hyp_scores_post": {h: hyps_post.get(h, {}).get("score", 0) for h in sorted(set(hyps_pre) | set(hyps_post))},
            }
            kr_diffs.append(kr_entry)

        pg_pre = hyps_pre.get("pregreek", {}).get("score", 0)
        pg_post = hyps_post.get("pregreek", {}).get("score", 0)
        if pg_pre != pg_post:
            pregreek_changes.append((word, pg_pre, pg_post))

    hs_pre = pre.get("hypothesis_summaries", {})
    hs_post = post.get("hypothesis_summaries", {})

    # ── Print Report ──

    sep = "=" * 78
    thin = "-" * 78

    print(sep)
    print("  HYPOTHESIS RESULTS COMPARISON: PRE-FIX vs POST-FIX")
    print(sep)
    print()

    print(f"  Total words (pre-fix):  {len(pre_words)}")
    print(f"  Total words (post-fix): {len(post_words)}")
    print(f"  Words in common:        {len(common_words)}")
    if words_only_pre:
        print(f"  Words only in pre-fix:  {len(words_only_pre)} -> {words_only_pre}")
    if words_only_post:
        print(f"  Words only in post-fix: {len(words_only_post)} -> {words_only_post}")
    print()

    print(thin)
    print(f"  CONFIDENCE DEMOTIONS ({len(confidence_demotions)} words)")
    print(thin)
    if confidence_demotions:
        print(f"  {'Word':<25} {'Pre-Fix':<14} {'Post-Fix':<14} {'Score Change'}")
        for word, cp, cpo, sp, spo in sorted(confidence_demotions, key=lambda x: confidence_rank(x[1]) - confidence_rank(x[2]), reverse=True):
            print(f"  {word:<25} {cp:<14} {cpo:<14} {fmt_delta(spo - sp)}")
    else:
        print("  (none)")
    print()

    print(thin)
    print(f"  CONFIDENCE PROMOTIONS ({len(confidence_promotions)} words)")
    print(thin)
    if confidence_promotions:
        print(f"  {'Word':<25} {'Pre-Fix':<14} {'Post-Fix':<14} {'Score Change'}")
        for word, cp, cpo, sp, spo in sorted(confidence_promotions, key=lambda x: confidence_rank(x[2]) - confidence_rank(x[1]), reverse=True):
            print(f"  {word:<25} {cp:<14} {cpo:<14} {fmt_delta(spo - sp)}")
    else:
        print("  (none)")
    print()

    print(thin)
    print(f"  BEST HYPOTHESIS CHANGES ({len(best_hyp_changes)} words)")
    print(thin)
    if best_hyp_changes:
        print(f"  {'Word':<25} {'Pre-Fix Best':<14} {'Post-Fix Best':<14} {'Score Pre':>10} {'Score Post':>10}")
        for word, bp, bpo, sp, spo in sorted(best_hyp_changes, key=lambda x: abs(x[4] - x[3]), reverse=True):
            print(f"  {word:<25} {bp:<14} {bpo:<14} {sp:>10.2f} {spo:>10.2f}")
    else:
        print("  (none)")
    print()

    print(thin)
    print("  K-R PARADIGM WORDS (ku-ro, ki-ro, sa-ra2)")
    print(thin)
    if kr_diffs:
        for entry in kr_diffs:
            w = entry["word"]
            print(f"\n  {w}:")
            print(f"    Best hypothesis:  {entry['best_pre']:<14} -> {entry['best_post']}")
            print(f"    Confidence:       {entry['conf_pre']:<14} -> {entry['conf_post']}")
            print(f"    Best score:       {entry['score_pre']:<14.2f} -> {entry['score_post']:.2f}  ({fmt_delta(entry['score_post'] - entry['score_pre'])})")
            print("    Per-hypothesis scores:")
            all_hyps = sorted(set(entry["hyp_scores_pre"]) | set(entry["hyp_scores_post"]))
            for h in all_hyps:
                s_pre = entry["hyp_scores_pre"].get(h, 0)
                s_post = entry["hyp_scores_post"].get(h, 0)
                delta = s_post - s_pre
                marker = " ***" if delta != 0 else ""
                print(f"      {h:<14} {s_pre:>8.2f} -> {s_post:>8.2f}  ({fmt_delta(delta)}){marker}")
    else:
        found_words = [w for w in KR_WORDS if w in common_words]
        if not found_words:
            print("  K-R words not found in common word set.")
            print(f"  Searched for: {KR_WORDS}")
            for target in KR_WORDS:
                matches = [w for w in common_words if target.replace('\u2082', '2').lower() in w.lower() or target.lower() in w.lower()]
                if matches:
                    print(f"  Possible matches for {target}: {matches}")
    print()

    print(thin)
    print(f"  PRE-GREEK SCORE CHANGES ({len(pregreek_changes)} words)")
    print(thin)
    if pregreek_changes:
        print(f"  {'Word':<25} {'Pre-Fix':>10} {'Post-Fix':>10} {'Delta':>10}")
        for word, sp, spo in sorted(pregreek_changes, key=lambda x: abs(x[2] - x[1]), reverse=True):
            print(f"  {word:<25} {sp:>10.2f} {spo:>10.2f} {fmt_delta(spo - sp):>10}")
    else:
        print("  (none)")
    print()

    print(thin)
    print("  HYPOTHESIS AGGREGATE SUMMARIES (supported/contradicted/neutral)")
    print(thin)
    all_hyps = sorted(set(hs_pre.keys()) | set(hs_post.keys()))
    for h in all_hyps:
        pre_s = hs_pre.get(h, {})
        post_s = hs_post.get(h, {})
        print(f"\n  {h.upper()}:")
        for metric in ["supported", "contradicted", "neutral"]:
            v_pre = pre_s.get(metric, 0)
            v_post = post_s.get(metric, 0)
            delta = v_post - v_pre
            marker = " ***" if delta != 0 else ""
            print(f"    {metric:<15} {v_pre:>5} -> {v_post:>5}  ({fmt_delta(delta)}){marker}")

    print()

    print(thin)
    print("  PER-HYPOTHESIS SCORE CHANGE SUMMARY")
    print(thin)
    for hyp in sorted(score_changes.keys()):
        changes = score_changes[hyp]
        increases = [(w, o, n) for w, o, n in changes if n > o]
        decreases = [(w, o, n) for w, o, n in changes if n < o]
        total_delta = sum(n - o for _, o, n in changes)
        print(f"\n  {hyp.upper()}:")
        print(f"    Words with score increase: {len(increases)}")
        print(f"    Words with score decrease: {len(decreases)}")
        print(f"    Net total score delta:     {fmt_delta(total_delta)}")
        biggest = sorted(changes, key=lambda x: abs(x[2] - x[1]), reverse=True)[:5]
        if biggest:
            print("    Top changes:")
            for w, o, n in biggest:
                print(f"      {w:<25} {o:>8.2f} -> {n:>8.2f}  ({fmt_delta(n - o)})")

    print()
    return {
        "demotions": len(confidence_demotions),
        "promotions": len(confidence_promotions),
        "best_hyp_changes": len(best_hyp_changes),
        "pregreek_changes": len(pregreek_changes),
    }


# ===========================================================================
# 2. Batch Analysis Results Comparison
# ===========================================================================

def compare_batch_results(pre, post):
    sep = "=" * 78
    thin = "-" * 78

    print(sep)
    print("  BATCH ANALYSIS RESULTS COMPARISON: PRE-FIX vs POST-FIX")
    print(sep)
    print()

    sum_pre = pre.get("summary", {})
    sum_post = post.get("summary", {})
    print(thin)
    print("  SUMMARY COUNTS")
    print(thin)
    for metric in ["total_words_analyzed", "high_confidence", "medium_confidence", "needs_review"]:
        v_pre = sum_pre.get(metric, 0)
        v_post = sum_post.get(metric, 0)
        delta = v_post - v_pre
        marker = " ***" if delta != 0 else ""
        print(f"  {metric:<25} {v_pre:>5} -> {v_post:>5}  ({fmt_delta(delta)}){marker}")
    print()

    hcf_pre = pre.get("high_confidence_findings", [])
    hcf_post = post.get("high_confidence_findings", [])

    hc_pre_words = {e["word"] for e in hcf_pre}
    hc_post_words = {e["word"] for e in hcf_post}

    demoted = sorted(hc_pre_words - hc_post_words)
    promoted = sorted(hc_post_words - hc_pre_words)
    stayed = sorted(hc_pre_words & hc_post_words)

    print(thin)
    print("  HIGH-CONFIDENCE LIST CHANGES")
    print(thin)
    print(f"  Pre-fix high-confidence count:  {len(hcf_pre)}")
    print(f"  Post-fix high-confidence count: {len(hcf_post)}")
    print(f"  Net change:                     {fmt_delta(len(hcf_post) - len(hcf_pre))}")
    print(f"  Words retained:                 {len(stayed)}")
    print()

    if demoted:
        print(f"  DEMOTED (removed from high confidence): {len(demoted)}")
        pre_lookup = {e["word"]: e for e in hcf_pre}
        post_med = {e["word"]: e for e in post.get("medium_confidence_findings", [])}
        post_nr = {e["word"]: e for e in post.get("needs_review", [])}
        for w in demoted:
            pe = pre_lookup.get(w, {})
            dest = "medium" if w in post_med else ("needs_review" if w in post_nr else "unknown")
            print(f"    {w:<25} was {pe.get('confidence','?'):<12} best={pe.get('best_hypothesis','?'):<12} -> {dest}")
    else:
        print("  DEMOTED: (none)")
    print()

    if promoted:
        print(f"  PROMOTED (added to high confidence): {len(promoted)}")
        post_lookup = {e["word"]: e for e in hcf_post}
        pre_med = {e["word"]: e for e in pre.get("medium_confidence_findings", [])}
        pre_nr = {e["word"]: e for e in pre.get("needs_review", [])}
        for w in promoted:
            poe = post_lookup.get(w, {})
            origin = "medium" if w in pre_med else ("needs_review" if w in pre_nr else "unknown")
            print(f"    {w:<25} now {poe.get('confidence','?'):<12} best={poe.get('best_hypothesis','?'):<12} <- {origin}")
    else:
        print("  PROMOTED: (none)")
    print()

    print(thin)
    print("  CHANGES WITHIN HIGH-CONFIDENCE LIST")
    print(thin)
    pre_lookup = {e["word"]: e for e in hcf_pre}
    post_lookup = {e["word"]: e for e in hcf_post}
    hc_changes = []
    for w in stayed:
        pe = pre_lookup[w]
        poe = post_lookup[w]
        if pe.get("confidence") != poe.get("confidence") or pe.get("best_hypothesis") != poe.get("best_hypothesis"):
            hc_changes.append((w, pe, poe))
    if hc_changes:
        print(f"  {'Word':<25} {'Conf Pre':<12} {'Conf Post':<12} {'Best Pre':<14} {'Best Post':<14}")
        for w, pe, poe in sorted(hc_changes):
            print(f"  {w:<25} {pe.get('confidence','?'):<12} {poe.get('confidence','?'):<12} {pe.get('best_hypothesis','?'):<14} {poe.get('best_hypothesis','?'):<14}")
    else:
        print("  (no changes for words that remained in high confidence)")
    print()

    hr_pre = pre.get("hypothesis_rankings", {})
    hr_post = post.get("hypothesis_rankings", {})

    print(thin)
    print("  HYPOTHESIS RANKING CHANGES")
    print(thin)
    all_hyps = sorted(set(hr_pre.keys()) | set(hr_post.keys()))
    print(f"\n  {'Hypothesis':<14} {'Rank Pre':>10} {'Rank Post':>10} {'Score Pre':>12} {'Score Post':>12} {'Words Pre':>11} {'Words Post':>11}")
    print(f"  {'-'*14} {'-'*10} {'-'*10} {'-'*12} {'-'*12} {'-'*11} {'-'*11}")
    for h in sorted(all_hyps, key=lambda x: hr_post.get(x, {}).get("rank", 99)):
        rp = hr_pre.get(h, {})
        rpo = hr_post.get(h, {})
        rank_pre = rp.get("rank", "?")
        rank_post = rpo.get("rank", "?")
        score_pre = rp.get("total_score", 0)
        score_post = rpo.get("total_score", 0)
        ws_pre = rp.get("words_supporting", 0)
        ws_post = rpo.get("words_supporting", 0)
        rank_marker = ""
        if isinstance(rank_pre, int) and isinstance(rank_post, int):
            if rank_post < rank_pre:
                rank_marker = " [UP]"
            elif rank_post > rank_pre:
                rank_marker = " [DOWN]"
        print(f"  {h:<14} {str(rank_pre):>10} {str(rank_post):>10} {score_pre:>12.1f} {score_post:>12.1f} {ws_pre:>11} {ws_post:>11}{rank_marker}")
    print()

    print("  Score deltas:")
    for h in sorted(all_hyps, key=lambda x: hr_post.get(x, {}).get("rank", 99)):
        rp = hr_pre.get(h, {})
        rpo = hr_post.get(h, {})
        score_delta = rpo.get("total_score", 0) - rp.get("total_score", 0)
        words_delta = rpo.get("words_supporting", 0) - rp.get("words_supporting", 0)
        print(f"    {h:<14}  score: {fmt_delta(score_delta):>10}   words_supporting: {fmt_delta(words_delta):>5}")
    print()

    mcf_pre = pre.get("medium_confidence_findings", [])
    mcf_post = post.get("medium_confidence_findings", [])
    mc_pre_words = {e["word"] for e in mcf_pre}
    mc_post_words = {e["word"] for e in mcf_post}

    print(thin)
    print("  MEDIUM-CONFIDENCE LIST CHANGES")
    print(thin)
    print(f"  Pre-fix count:  {len(mcf_pre)}")
    print(f"  Post-fix count: {len(mcf_post)}")
    print(f"  Net change:     {fmt_delta(len(mcf_post) - len(mcf_pre))}")
    mc_added = sorted(mc_post_words - mc_pre_words)
    mc_removed = sorted(mc_pre_words - mc_post_words)
    if mc_added:
        print(f"  Added ({len(mc_added)}): {mc_added[:20]}{'...' if len(mc_added) > 20 else ''}")
    if mc_removed:
        print(f"  Removed ({len(mc_removed)}): {mc_removed[:20]}{'...' if len(mc_removed) > 20 else ''}")
    print()

    nr_pre = pre.get("needs_review", [])
    nr_post = post.get("needs_review", [])
    nr_pre_words = {e["word"] for e in nr_pre}
    nr_post_words = {e["word"] for e in nr_post}

    print(thin)
    print("  NEEDS-REVIEW LIST CHANGES")
    print(thin)
    print(f"  Pre-fix count:  {len(nr_pre)}")
    print(f"  Post-fix count: {len(nr_post)}")
    print(f"  Net change:     {fmt_delta(len(nr_post) - len(nr_pre))}")
    nr_added = sorted(nr_post_words - nr_pre_words)
    nr_removed = sorted(nr_pre_words - nr_post_words)
    if nr_added:
        print(f"  Added ({len(nr_added)}): {nr_added[:20]}{'...' if len(nr_added) > 20 else ''}")
    if nr_removed:
        print(f"  Removed ({len(nr_removed)}): {nr_removed[:20]}{'...' if len(nr_removed) > 20 else ''}")
    print()


# ===========================================================================
# 3. Overall Summary
# ===========================================================================

def print_overall_summary(hypo_stats):
    sep = "=" * 78
    print(sep)
    print("  OVERALL IMPACT SUMMARY")
    print(sep)
    print()
    print(f"  Confidence demotions:        {hypo_stats['demotions']}")
    print(f"  Confidence promotions:       {hypo_stats['promotions']}")
    print(f"  Best hypothesis reassigned:  {hypo_stats['best_hyp_changes']}")
    print(f"  Pre-Greek score changes:     {hypo_stats['pregreek_changes']}")
    print()
    if hypo_stats["demotions"] > hypo_stats["promotions"]:
        print("  Net effect: The fix was CONSERVATIVE -- more words were demoted than promoted.")
        print("  This aligns with the bug-fix intent of correcting inflated scores.")
    elif hypo_stats["promotions"] > hypo_stats["demotions"]:
        print("  Net effect: The fix was EXPANSIVE -- more words gained confidence than lost it.")
    else:
        print("  Net effect: BALANCED -- equal demotions and promotions.")
    print()
    print(sep)
    print("  END OF COMPARISON REPORT")
    print(sep)


# ===========================================================================
# Main
# ===========================================================================

def main():
    for path in [HYPO_PRE, HYPO_POST, BATCH_PRE, BATCH_POST]:
        if not path.exists():
            print(f"ERROR: File not found: {path}")
            sys.exit(1)

    hypo_pre = load_json(HYPO_PRE)
    hypo_post = load_json(HYPO_POST)
    batch_pre = load_json(BATCH_PRE)
    batch_post = load_json(BATCH_POST)

    print()
    hypo_stats = compare_hypothesis_results(hypo_pre, hypo_post)
    print()
    compare_batch_results(batch_pre, batch_post)
    print()
    print_overall_summary(hypo_stats)


if __name__ == "__main__":
    main()
