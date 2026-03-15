# Week 2 Blocker Routing Memo

**Date**: 2026-03-15
**Agents**: B, C, Lead
**Status**: ACTIVE

---

## Purpose

Route the remaining week-2 blocker-led items into concrete lane-C work without letting them consume the admin reading budget.

Targets:

- `HTWb229`
- `PYR2`
- `KHWa1013`
- `I-PI-NA-MA` status check

---

## 1. HTWb229

### Source packet

- `data/reading_briefs/week2/HTWb229.json`

### Raw reading

```text
*188  CYP+D
```

### Current evidence

- `*188` occurs at HT and HTW, including:
  - `HT15`
  - `HT56a`
  - `HT98b`
  - `HT103`
  - `HT123+124b`
  - `HTW231b`
  - `HTWb229`
  - `HTWc3009`
  - `HTWc3013`
- project knowledge currently treats `*188` as an **administrative / classifier-style marker** with strong roundel/admin associations
- `CYP+D` is the lower-grade copper qualifier in the KH/warehouse-grade system
- `*188-DU` occurs directly before `*304+PA-CYP+D` on `HTWeWc3020`

### Routing decision

**Lane C should treat HTWb229 as a warehouse-classifier problem, not a translation problem.**

### Immediate work

1. Compare `HTWb229` directly against:
   - `HTWeWc3020` (`*188-DU *304+PA-CYP+D`)
   - `HTWc<3018>` (`KA CYP+D`)
2. Test whether `*188` is functioning as:
   - classifier / category marker before `CYP+D`
   - warehouse transaction marker
   - sign family parallel to the HT/KH administrative stamp system

### Output expectation

Short sign-function note, not a connected reading.

---

## 2. PYR2

### Source packet

- `data/reading_briefs/week2/PYR2.json`

### Raw reading

```text
*304  1/2
```

### Current evidence

- `*304` is already strong at the function level:
  - `42` occurrences
  - `5` sites
  - `HIGH` confidence as a **commodity logogram**
- single PYR occurrence:
  - `PYR2 = *304 1/2`
- compound evidence:
  - `*304+PA` on `HT100`, `KH7b`, `KH73`
  - `*304+PA-CYP+D` on `HTWa1021bis`, `HTWc3016`, `HTWeWc3020`

### Routing decision

**PYR2 is not a decipherment bottleneck for `*304` function.** The function is already stable enough: unidentified commodity logogram with quantity `1/2`.

### Immediate work

1. Keep `*304` identity work separate from reading throughput.
2. Use PYR2 as a **site-expansion control**: it confirms `*304` at Pyrgos with the same commodity-like syntax.
3. Do not prioritize a full connected reading unless a second PYR parallel appears.

### Output expectation

Add PYR2 to sign-distribution tracking; no promotion activity.

---

## 3. KHWa1013

### Source packet

- `data/reading_briefs/week2/KHWa1013.json`

### Raw reading

```text
*86-RO
```

### Current evidence

- four occurrences total:
  - `KHWa1013`
  - `KHWa1014`
  - `KHWa1015`
  - `KHWa1016`
- KH-only distribution
- existing analysis (`2026-02-17_khania_star86_star188_system.md`) treats `*86+*188` as a KH administrative stamp family
- `*86-RO` was already flagged there as a **possible structural parallel** to `KU-RO`, but not a promoted decipherment
- integrated results keep `*86-RO` at effectively **non-lexical / eliminated** language-testing status

### Routing decision

**KHWa1013 belongs to the KH administrative stamp subsystem.**

### Immediate work

1. Keep the four `*86-RO` pieces grouped as one blocker family.
2. Compare them against:
   - KH roundel `*86+*188`
   - KH transaction-level tablets
   - any `-RO` completion/closure behavior elsewhere
3. Do not assign lexical meaning or language-family weight.

### Output expectation

One sign-subsystem memo covering `KHWa1013-1016`, not four separate readings.

---

## 4. I-PI-NA-MA

### Current promotion status

- Packet: `analysis/active/promotion_packets/I-PI-NA-MA.md`
- Board decision: `HOLD`

### Blocking gate

`cross_corpus_consistency` still fails:

- positional consistency: `0.333`
- functional consistency: `0.417`
- rule: `min >= 0.55 and max >= 0.70`

### Routing decision

**No status movement.**

The sprint should continue treating `I-PI-NA-MA` as a bounded ritual evidence-review item only.

---

## Priority Order for Remaining Week 2 Blockers

1. `KHWa1013-1016` as one KH sign-subsystem family
2. `HTWb229` as warehouse/classifier routing problem
3. `PYR2` as site-expansion control for already-stable `*304` function
4. `I-PI-NA-MA` remains HOLD unless lane-B gates change

---

## Practical Outcome

This routing preserves the sprint split:

- admin translation capacity stays on readable tablets
- sign work stays tightly scoped
- no speculative promotion work is opened for weak candidates
