# Lessons Learned

**Methodological insights from completed analysis work**

**Last Updated**: 2026-01-31

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

## Tool-Specific Lessons

### corpus_lookup.py

- Always verify occurrence counts against multiple sources
- Cross-reference with SigLA for palaeographic details

### hypothesis_tester.py

- Don't trust single-hypothesis high scores
- Multi-hypothesis convergence is stronger than single high score

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
