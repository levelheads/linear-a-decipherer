# Lessons Learned

**Methodological insights from completed analysis work**

**Last Updated**: 2026-02-01

---

## Methodology Refinements

### From SA-RA₂ Investigation (2026-01-31)

**Lesson**: Check commodity distribution BEFORE proposing meanings

**Problem Encountered**: Initial hypothesis (še'u "barley") failed because SA-RA₂ appears with multiple commodity types (GRA, CYP, OLE).

**Application**: If a word appears with multiple commodity types, it's NOT a commodity name — it must be a transaction category, qualifier, or administrative term.

**Added to Workflow**:
- Step: Before proposing lexical meaning, check all contexts
- If appears with multiple commodity types → exclude commodity name hypothesis
- Look for transaction/administrative semantics instead

---

### From K-R Paradigm Analysis (2026-01-31)

**Lesson**: Don't assume "complementary distribution" — verify by finding counter-examples

**Problem Encountered**: Assumed KU-RO and KI-RO were mutually exclusive (complementary distribution). Actually found 5 inscriptions with BOTH forms.

**Application**: Before claiming complementary distribution, actively search for co-occurrence. Finding even one counter-example changes the interpretation.

**Added to Workflow**:
- kr_paradigm_validator.py now checks for co-occurrence
- Any claim of complementary distribution requires explicit counter-example search

---

### From Proto-Greek Downgrade (2026-01-05)

**Lesson**: Negative evidence can be decisive

**Problem Encountered**: Needed to formally downgrade Proto-Greek hypothesis despite some supporters.

**Evidence used**:
1. Low /o/ frequency (2.9% vs. Greek higher)
2. KU-RO ≠ Linear B *to-so* for "total"
3. Absence of Greek case endings (-os, -on, -ōn)

**Application**: When multiple independent negative evidence points converge, hypothesis should be downgraded regardless of prior expectations.

**Added to Workflow**: Explicit negative evidence section in all hypothesis testing

---

### From Knossos Scepter Analysis (2026-01-09)

**Lesson**: Different registers on same object can have different scribes and different scripts

**Problem Encountered**: Assumed single inscription = single scribe. Scepter shows two distinct hands (ceremonial ring vs. administrative handle).

**Application**: Always check for paleographic variation within documents. Different sections may represent different scribal traditions.

**Added to Workflow**: Paleographic analysis step before linguistic interpretation

---

### From Tool Parity Bug (2026-02-01)

**Lesson**: All tools analyzing the same corpus must use identical filtering logic

**Problem Encountered**: `batch_pipeline.py` showed Proto-Greek at rank #2 while `hypothesis_tester.py` showed it at 2.5%. The 75% discrepancy came from batch_pipeline including single-syllables (KU, KA, SI) and logograms (OLIV, GRA) that hypothesis_tester filtered out.

**Impact**: Single-syllables match multiple hypothesis patterns by chance, inflating scores for all hypotheses but especially those with short morphemes.

**Application**: Before trusting comparative results from multiple tools:
1. Verify identical word filtering logic
2. Verify identical normalization (case, Unicode)
3. Verify identical counting methodology

**Added to Workflow**: Tool parity check when running multiple analysis tools

---

### From Cambridge 2026 Review (2026-02-01)

**Lesson**: Check scholarly literature for internal contradictions before adopting claims

**Problem Encountered**: Cambridge publication claims both:
- "-RU/-RE corresponds to Greek -os masculine ending" (implies relationship)
- "Minoan is an isolated language" (implies no relationship)

These are mutually contradictory. If Minoan shares morphological endings with Greek, it either borrowed from Greek, loaned to Greek, or shares a common ancestor — none of which is "isolated."

**Application**: When reviewing literature, explicitly check if claims are mutually consistent. Flag contradictions rather than adopting both sides.

**Added to Workflow**: Internal consistency check for all new scholarly claims

---

### From Evidence Level Discipline (2026-02-01)

**Lesson**: Maintain strict evidence hierarchy; don't let speculation become fact through repetition

**Problem Encountered**: Claims like NI = 'fig' (single scholar, Greek etymology) were being treated as established. Then KI-KI-NA = 'sycamore figs' was built on this, compounding speculation.

**Application**: Track dependency chains explicitly:
- If Claim A depends on Claim B
- And Claim B is SPECULATIVE
- Then Claim A cannot be higher than SPECULATIVE

**Evidence Levels** (strict hierarchy):
| Level | Criteria |
|-------|----------|
| CERTAIN | Multiple independent evidence lines |
| PROBABLE | Single strong evidence + supporting context |
| POSSIBLE | Reasonable inference, limited evidence |
| SPECULATIVE | Single scholar interpretation |
| CONTROVERSIAL | Contradicts other accepted claims |

**Added to Workflow**: Dependency tracking in KNOWLEDGE.md entries

---

## Red Flags Encountered

### Pattern: Single-Hypothesis Support Only

| When Encountered | What It Indicated | How We Caught It |
|------------------|-------------------|------------------|
| SA-RA₂ = Semitic only | Overconfidence risk | First Principles #4 check |
| KU-RO = Semitic only | Need multi-hypothesis | Required testing all four |

**Resolution**: First Principles #4 mandates testing all four hypotheses. Single-hypothesis support caps confidence at PROBABLE.

---

### Pattern: Semantic Stretching

| When Encountered | What It Indicated | How We Caught It |
|------------------|-------------------|------------------|
| KU-RO = Greek *kyrios* | Forcing evidence | Semantic mismatch with context |
| SA-RA₂ = "barley" | Ignoring multi-commodity | Distribution analysis |

**Resolution**: Peer review through FINDINGS_LOG.md. Document rejected interpretations to prevent re-discovery.

---

### Pattern: Citing Sources Not Actually Fetched

| When Encountered | What It Indicated | How We Caught It |
|------------------|-------------------|------------------|
| Referencing "Gordon 1966" | Need to verify claims | Web fetch to check actual content |

**Resolution**: Always fetch and verify sources. Document source quality in analysis.

---

### Pattern: Internal Contradictions in Literature (2026-02-01)

| When Encountered | What It Indicated | How We Caught It |
|------------------|-------------------|------------------|
| "-RU/-RE = Greek -os" + "isolated language" | Scholarly hedging, not rigorous finding | Explicit contradiction check |
| Greek etymologies for "isolated" language | Circular methodology | Logical analysis |

**Resolution**: Do not automatically adopt scholarly consensus. Check for internal consistency. "We don't know" ≠ "It has no relatives."

---

### Pattern: Dependency Chain Blindness (2026-02-01)

| When Encountered | What It Indicated | How We Caught It |
|------------------|-------------------|------------------|
| KI-KI-NA depends on NI = 'fig' | Compounding speculation | Traced claim dependencies |
| Greek etymology chains | Building on unverified base | Evidence level audit |

**Resolution**: Track what each claim depends on. A claim cannot be more certain than its weakest dependency.

---

## Best Practices Established

### 1. Pre-Flight Checklist (Always Run Before Analysis)

```
☑ [P1] I will analyze patterns BEFORE assuming a language
☑ [P2] I am prepared to abandon hypotheses if contradicted
☑ [P3] I have identified/will identify all available anchors
☑ [P4] I will test against ALL FOUR linguistic hypotheses
☑ [P5] I will consider what the data DOESN'T show
☑ [P6] I will verify readings across the ENTIRE corpus
```

---

### 2. Hypothesis Testing Order

1. Establish structural/positional pattern first
2. Identify anchor level (1-6)
3. Test ALL four hypotheses with explicit evidence
4. Rank by evidence strength
5. Check for negative evidence
6. Assign confidence based on highest anchor reached

---

### 3. Documentation Standards

| Document | When to Update | What to Include |
|----------|----------------|-----------------|
| ANALYSIS_INDEX.md | After each analysis | ID, status, confidence, file link |
| FINDINGS_LOG.md | When interpretation changes | Previous, new, evidence, implications |
| CONFIRMED_READINGS.md | When reading reaches HIGH+ | Word, meaning, evidence, occurrences |
| STATE_OF_KNOWLEDGE.md | After major findings | Update hypothesis scorecard, open questions |
| LESSONS_LEARNED.md | When methodology improved | Problem, solution, workflow change |

---

### 4. Session Logging

- Use templates/SESSION_TEMPLATE.md for all sessions
- Log objectives, methods, findings
- Run First Principles verification at end
- Update knowledge management docs before committing

---

## Anti-Patterns to Avoid

### 1. "Greek First" Bias

**Wrong**: "What would this mean in Greek?"
**Right**: "What patterns does this show? How does it test against all hypotheses?"

---

### 2. Anchor-Skipping

**Wrong**: Jump from logogram (L3) to lexical match (L6) without structural analysis (L4-5)
**Right**: Build incrementally through hierarchy

---

### 3. Confirmation Bias

**Wrong**: Accumulate supporting evidence, ignore contradictions
**Right**: Actively seek disconfirming evidence; document rejections

---

### 4. Hapax Overconfidence

**Wrong**: "This unique word proves X"
**Right**: Hapax legomenon = max POSSIBLE confidence; flag for corpus-wide verification

---

### 5. Session Amnesia

**Wrong**: Start each session fresh, potentially rediscovering same things
**Right**: Check ANALYSIS_INDEX.md first; build on prior work

---

### 6. Score Inflation via Noise (2026-02-01)

**Wrong**: Include single-syllables (KU, KA, SI) and logograms in hypothesis testing
**Right**: Filter to multi-syllable words only; single syllables match patterns by chance

**Example**: 98/130 findings (75%) were single-syllables, completely inverting hypothesis rankings.

---

### 7. Circular Methodology Detection (2026-02-01)

**Wrong**: Use Greek to decode Minoan → claim Minoan is unrelated to Greek
**Right**: If using Language X to decode, you're implicitly claiming a relationship

**Example**: NI = 'fig' based on Greek νικύλεον, then claiming Minoan is "isolated."

---

### 8. Tool Inconsistency (2026-02-01)

**Wrong**: Same query returning different results based on case or tool choice
**Right**: Normalize all inputs; verify tool parity before comparative analysis

**Example**: "ku-ro" → 0 results; "KU-RO" → 37 results (case sensitivity bug)

---

### 9. Parallel Session Confusion (2026-02-01)

**Wrong**: Assume your edits are uncommitted without checking git
**Right**: When running multiple sessions, always `git status` before assuming state

**Example**: Edits appeared uncommitted but another session had already committed them.

---

## Tool-Specific Lessons

### corpus_lookup.py

- Always verify occurrence counts against multiple sources
- Cross-reference with SigLA for palaeographic details
- **2026-02-01 Fix**: Case sensitivity — all searches now normalize to uppercase

### hypothesis_tester.py

- Don't trust single-hypothesis high scores
- Multi-hypothesis convergence is stronger than single high score
- **AUTHORITATIVE** for hypothesis rankings (filters logograms, ensures multi-syllable words)

### batch_pipeline.py

- **2026-02-01 Fix**: Now filters single-syllables and pure logograms
- Use `--verbose` to see filtering statistics
- Check parity with hypothesis_tester.py before trusting results

### corpus_auditor.py

- **2026-02-01 Fix**: Now accepts `*NNN-XX` patterns as valid entity names
- Only bare `*` is rejected
- Verification rate should improve after fix

### kr_paradigm_validator.py

- Run co-occurrence check before claiming complementary distribution
- Document exceptions, not just patterns

---

## Future Improvements Needed

### Identified Gaps

1. **Chronological analysis**: No systematic checking if patterns change MMII → LMIB
2. **Regional variation**: HT vs. KH vs. ZA not systematically compared
3. **Automated index updates**: Currently manual; could script
4. **Citation management**: No formal bibliography tool

### Proposed Solutions

1. Add date-range filtering to corpus tools
2. Create regional comparison module
3. Script to update ANALYSIS_INDEX.md from tool outputs
4. Integrate Zotero or similar for references

---

## Related Documents

- [FIRST_PRINCIPLES.md](FIRST_PRINCIPLES.md) - Inviolable methodological rules
- [ANALYSIS_INDEX.md](ANALYSIS_INDEX.md) - What's been analyzed
- [FINDINGS_LOG.md](FINDINGS_LOG.md) - What's been discovered
- [STATE_OF_KNOWLEDGE.md](STATE_OF_KNOWLEDGE.md) - Current understanding

---

*Lessons documented as part of the Linear A Decipherment Project knowledge management system.*
