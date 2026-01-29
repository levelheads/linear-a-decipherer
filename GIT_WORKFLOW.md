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

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
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

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

```
Fix negative evidence data pipeline bug

Changed word_frequencies → top_words to match statistics.json schema.
Added robust corpus extraction method as fallback.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
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

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
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
tools/*.py              # Analysis scripts
analyses/*.md           # Research outputs
linear-a-decipherer/    # Core methodology
README.md               # Project documentation
.gitignore              # Ignore patterns
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

## Agent Integration

When working with Claude Code, the git workflow should be:

1. **Task completion** → Check if commit needed
2. **Multiple related changes** → Single atomic commit
3. **Phase completion** → Comprehensive commit with summary
4. **Session end** → Always verify sync status

The agent can call `python tools/git_manager.py sync` at any time to check repository status.
