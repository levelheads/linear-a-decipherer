# Engineering Practices

Project management lessons for the Linear A Decipherment Project.

**Last Updated**: 2026-02-02

---

## Release Management Lessons

### CITATION.cff Synchronization (2026-02-02)

**Lesson**: Update CITATION.cff BEFORE creating release tags

**Problem**: Created v0.3.0 tag with CITATION.cff still showing v0.2.0.

**Fix**: CITATION.cff update must be part of the release commit, not a follow-up.

### Pre-commit Hook Versions (2026-02-02)

**Lesson**: Run `pre-commit autoupdate` before releases

**Problem**: Hardcoded v4.5.0 when v6.0.0 was available.

**Fix**: Quarterly or before each release, run autoupdate.

### Configuration Hygiene (2026-02-02)

**Lesson**: Review configs for duplicate blocks

**Problem**: Duplicate repo entries in .pre-commit-config.yaml.

**Fix**: Scan config files before committing changes.

---

## Plan Verification Lessons

### File-by-File Verification (2026-02-02)

**Lesson**: Explicitly verify every file mentioned in implementation plans

**Problem**: Plan mentioned CITATION.cff but verification was incomplete.

**Fix**: After implementation, check each file against plan.

---

## Checklists

See GIT_WORKFLOW.md for:
- Release Checklist
- Pre-commit Hygiene Checklist
- Plan Verification Checklist

## Canonical State Practice

Current operational truth (metrics, active campaigns, release readiness) must be
maintained in `linear-a-decipherer/MASTER_STATE.md`.

Historical detail belongs in `linear-a-decipherer/CHANGELOG.md`.
