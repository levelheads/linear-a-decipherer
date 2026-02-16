# Git Workflow for Linear A Decipherment Project

This document establishes consistent git practices to ensure project success.

## Quick Reference

```bash
# Check status at any time
python tools/git_manager.py status

# Before committing
python tools/git_manager.py pre-commit

# Generate commit message
python tools/git_manager.py summary

# Full sync check
python tools/git_manager.py sync
```

---

## When to Commit

### Commit Triggers (DO commit after):

| Trigger | Example |
|---------|---------|
| **Tool created/modified** | New `regional_analyzer.py` |
| **Analysis completed** | `TY3a_COMPLETE_ANALYSIS.md` |
| **Bug fixed** | Fixed data pipeline in `negative_evidence.py` |
| **Documentation updated** | README changes |
| **Data schema changed** | New fields in output JSON |
| **Phase/milestone completed** | "Phase 2 complete" |

### Don't Commit:

| Item | Reason |
|------|--------|
| `data/*.json` | Generated files (gitignored) |
| `__pycache__/` | Python bytecode (gitignored) |
| `external/lineara/` changes | Submodule managed separately |
| Work-in-progress | Wait until stable |

---

## Commit Message Format

```
<type>: <short description>

<body - what changed and why>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

### Types:

| Type | Use For |
|------|---------|
| `Add` | New tools, analyses, features |
| `Fix` | Bug fixes |
| `Update` | Modifications to existing code |
| `Refactor` | Code restructuring (no behavior change) |
| `Docs` | Documentation only |

### Examples:

```
Add regional vocabulary analyzer

New tool compares vocabulary across major Linear A sites (HT, KH, ZA, PH).
Key finding: LOW vocabulary overlap (Jaccard <0.03) suggests regional
administrative independence.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

```
Fix negative evidence data pipeline bug

Changed word_frequencies → top_words to match statistics.json schema.
Added robust corpus extraction method as fallback.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

---

## Workflow Checkpoints

### Start of Session

```bash
# 1. Check current state
python tools/git_manager.py sync

# 2. Pull latest if behind
git pull
```

### During Work

```bash
# Periodically check status
python tools/git_manager.py status
```

### Before Ending Session

```bash
# 1. Check what needs committing
python tools/git_manager.py status

# 2. Run pre-commit checks
python tools/git_manager.py pre-commit

# 3. Stage files
git add <specific files>

# 4. Commit with proper message
git commit -m "$(cat <<'EOF'
<type>: <description>

<body>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"

# 5. Push to remote
git push

# 6. Verify
python tools/git_manager.py sync
```

---

## Pre-Commit Checklist

The `git_manager.py pre-commit` command checks:

- [ ] No `data/` files staged (should be gitignored)
- [ ] No `__pycache__` files staged
- [ ] Python files have valid syntax
- [ ] README.md updated if tools/ changed
- [ ] Analysis files have proper structure

---

## File Categories

### Always Commit:

```
tools/*.py                          # Analysis scripts
analysis/completed/**/*.md          # Finished analyses
analysis/sessions/*.md              # Session logs
linear-a-decipherer/*.md            # Core methodology + knowledge management
templates/*.md                      # Document templates
README.md                           # Project documentation
.gitignore                          # Ignore patterns
```

### Never Commit (Gitignored):

```
data/                   # Generated JSON files
__pycache__/            # Python bytecode
*.log                   # Log files
.DS_Store               # macOS metadata
```

### Submodule (Managed Separately):

```
external/lineara/       # Corpus data submodule
```

---

## Recovery Procedures

### Accidentally Staged Wrong Files

```bash
# Unstage specific file
git restore --staged <file>

# Unstage all
git restore --staged .
```

### Need to Amend Last Commit

```bash
# Only if NOT pushed yet
git commit --amend
```

### Discard Local Changes

```bash
# Discard changes to specific file
git restore <file>

# Discard all changes (DANGEROUS)
git restore .
```

---

## Knowledge Management Updates

After analysis work, update these files before committing:

| Document | When to Update |
|----------|----------------|
| `linear-a-decipherer/MASTER_STATE.md` | For any current metric/status/campaign changes (**canonical**) |
| `linear-a-decipherer/ANALYSIS_INDEX.md` | After each analysis (add entry) |
| `linear-a-decipherer/KNOWLEDGE.md` | When readings, hypotheses, or anchors change |
| `linear-a-decipherer/CHANGELOG.md` | When discoveries are made (chronological log) |
| `linear-a-decipherer/LESSONS_LEARNED.md` | When methodology is refined |

**Note**: `MASTER_STATE.md` is canonical for current operations. `CHANGELOG.md` is the historical narrative.

---

## Agent Integration

When working with Claude Code, the git workflow should be:

1. **Task completion** → Check if commit needed
2. **Multiple related changes** → Single atomic commit
3. **Phase completion** → Comprehensive commit with summary
4. **Session end** → Update knowledge management docs, then verify sync status

The agent can call `python tools/git_manager.py sync` at any time to check repository status.

---

## Release Management

### Version Format

This project uses **semantic versioning** (MAJOR.MINOR.PATCH):

| Component | When to Increment |
|-----------|-------------------|
| MAJOR | Breaking methodology changes, corpus schema changes |
| MINOR | New tools, significant methodology updates, milestone analyses |
| PATCH | Bug fixes, documentation updates, minor refinements |

Current version is tracked in `CITATION.cff`.

### Creating Releases

**Tag a release** after significant milestones:

```bash
# 1. Ensure everything is committed and pushed
python tools/git_manager.py sync

# 2. Update version in CITATION.cff
# version: 0.3.0

# 3. Create annotated tag
git tag -a v0.3.0 -m "Add quantitative methodology tools (Feb 2026)"

# 4. Push tag to remote
git push origin v0.3.0
```

### Release Triggers

Create a new release when:

| Trigger | Version Type |
|---------|--------------|
| New methodology framework | MINOR |
| Major corpus milestone | MINOR |
| Suite of new tools | MINOR |
| Bug fixes only | PATCH |
| Breaking changes | MAJOR |

### GitHub Releases

After creating a tag, create a GitHub Release:

1. Go to repository → Releases → "Draft a new release"
2. Select the tag you just pushed
3. Title: `v0.3.0 - Quantitative Methodology Tools`
4. Description: Extract relevant sections from CHANGELOG.md
5. Publish release

This creates a citable research snapshot for academic reference.

### Release Notes Template

```markdown
## What's New

- [Brief description of major changes]

## Tools Added/Modified

- `tool_name.py` - Description

## Methodology Updates

- [Key methodology changes]

## Full Changelog

See [CHANGELOG.md](linear-a-decipherer/CHANGELOG.md) for detailed history.
```

---

## Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) for automated checks.

### Setup

```bash
# Install pre-commit
pip install pre-commit

# Install hooks in this repository
pre-commit install

# (Optional) Run on all files once
pre-commit run --all-files
```

### What Gets Checked

| Hook | Purpose |
|------|---------|
| check-added-large-files | Prevents files >500KB |
| trailing-whitespace | Removes trailing spaces |
| end-of-file-fixer | Ensures files end with newline |
| check-yaml | Validates YAML syntax |
| check-json | Validates JSON syntax |
| check-ast | Validates Python syntax |
| ruff | Python linting (advisory) |

### Bypassing Hooks (Emergency Only)

```bash
# Skip all hooks for one commit
git commit --no-verify -m "Emergency fix"
```

Use sparingly—hooks exist to maintain quality.

---

## Release Checklist

Complete before creating any release tag:

```
[ ] 1. CITATION.cff updated
    - version: matches tag (e.g., "0.4.0")
    - date-released: today's date

[ ] 2. Pre-commit hooks current
    - Run: pre-commit autoupdate
    - Commit any updates

[ ] 3. CHANGELOG.md has new version section

[ ] 3b. MASTER_STATE.md updated
    - Current metrics and release readiness snapshot refreshed

[ ] 4. All changes committed
    - git status shows clean

[ ] 5. Tests pass
    - pre-commit run --all-files

[ ] 6. Tag AFTER committing release changes
    - Commit first, tag second, push both

If any box unchecked → DO NOT TAG
```

---

## Pre-commit Hygiene Checklist

Quarterly or before releases:

```
[ ] Run: pre-commit autoupdate
[ ] Review .pre-commit-config.yaml for duplicates
[ ] Test: pre-commit run --all-files
```

---

## Plan Verification Checklist

After implementing any plan:

```
For each file in plan:
[ ] File exists
[ ] Changes match plan
[ ] No syntax errors

Overall:
[ ] All steps completed
[ ] git status clean or staged
```
