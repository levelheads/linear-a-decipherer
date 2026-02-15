#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

DATE_STAMP="$(date -u +%Y-%m-%d)"
OUTPUT_PATH=""
SKIP_PARSE=0
SKIP_MASTER_STATE=0
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage: tools/run_corpus_refresh_cycle.sh [options]

Options:
  --date YYYY-MM-DD      Override output date stamp
  --output PATH          Override readiness audit JSON output path
  --skip-parse           Skip parse_lineara_corpus step
  --skip-master-state    Skip refresh_master_state step
  --dry-run              Print commands without executing
  -h, --help             Show help

Exit behavior:
  - validate_corpus exit code 0 or 2 is treated as non-fatal (2 = warnings).
EOF
}

run_cmd() {
  echo "+ $*"
  if [[ "$DRY_RUN" -eq 0 ]]; then
    "$@"
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --date)
      DATE_STAMP="$2"
      shift 2
      ;;
    --output)
      OUTPUT_PATH="$2"
      shift 2
      ;;
    --skip-parse)
      SKIP_PARSE=1
      shift
      ;;
    --skip-master-state)
      SKIP_MASTER_STATE=1
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$OUTPUT_PATH" ]]; then
  OUTPUT_PATH="$ROOT_DIR/analysis/active/${DATE_STAMP}_corpus_access_readiness_audit.json"
fi

if [[ "$SKIP_PARSE" -eq 0 ]]; then
  run_cmd python3 "$ROOT_DIR/tools/parse_lineara_corpus.py"
fi

echo "+ python3 $ROOT_DIR/tools/validate_corpus.py --report-only"
if [[ "$DRY_RUN" -eq 0 ]]; then
  set +e
  python3 "$ROOT_DIR/tools/validate_corpus.py" --report-only
  VALIDATE_STATUS=$?
  set -e
  if [[ "$VALIDATE_STATUS" -ne 0 && "$VALIDATE_STATUS" -ne 2 ]]; then
    echo "validate_corpus failed with exit code $VALIDATE_STATUS" >&2
    exit "$VALIDATE_STATUS"
  fi
  if [[ "$VALIDATE_STATUS" -eq 2 ]]; then
    echo "validate_corpus returned warnings (exit 2); continuing."
  fi
fi

if [[ "$SKIP_MASTER_STATE" -eq 0 ]]; then
  run_cmd python3 "$ROOT_DIR/tools/refresh_master_state.py"
fi

run_cmd python3 "$ROOT_DIR/tools/corpus_readiness_auditor.py" --output "$OUTPUT_PATH" --markdown

echo "Corpus refresh cycle complete."
echo "Readiness audit: $OUTPUT_PATH"
