#!/usr/bin/env bash
# ship_canon.sh — land the current uncommitted canon decision end-to-end, and
# record the outcome to a file the agent can read (no copy-paste).
#
# Flow it replaces (per decision):
#   rm stale lock → checkout -b → add the right files → commit → push → gh pr create → gh pr merge
# Now: just `bash tools/ship_canon.sh`
#
# Usage:
#   bash tools/ship_canon.sh                 ship the current canon change
#   bash tools/ship_canon.sh "DL-0NN: title" ship with an explicit title override
#   bash tools/ship_canon.sh --dry-run       print the full plan; change nothing
#
# Assumes: the DL record + decision_log/changelog/backlog edits are already in the
# working tree (uncommitted) — i.e. `dl_records.py land` has run.
# Requires (non-dry-run): gh CLI, authenticated (`gh auth login`).
#
# Outputs (read by the agent via the mounted repo — you paste nothing):
#   tools/.last_ship.log   full transcript of this run
#   tools/.last_ship.json  PR number / state / merge SHA / checks rollup
#
# Safety: the script CREATES the PR but does NOT admin-merge when either
#   (a) the change touches code/ (the six-gate app-ci must run first), or
#   (b) any touched path has a CODE OWNER OTHER THAN THE REPO OWNER -- a reviewer
#       whose approval the change actually needs (Framework 002 section 8c: the
#       dev-lead approver). An --admin merge bypasses required review, so this
#       guard is what stops the script silently defeating the review gate.
#       Owner-only canon (00_owner/** etc.) is still create-and-admin-merged:
#       GitHub will not let an owner approve their own PR, and doc-integrity
#       still gates the merge. You run it, so the merge is an owner action.

set -uo pipefail

DRY=0
if [ "${1:-}" = "--dry-run" ]; then DRY=1; shift; fi

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "ERROR: not inside a git repo"; exit 1; }
cd "$ROOT"
mkdir -p tools
LOG="tools/.last_ship.log"; JSON="tools/.last_ship.json"
: > "$LOG"
exec > >(tee "$LOG") 2>&1

echo "== ship_canon $(date -u +%Y-%m-%dT%H:%M:%SZ) ${DRY:+}$( [ "$DRY" = 1 ] && echo '[DRY-RUN]') =="

if [ "$DRY" = 0 ]; then
  command -v gh >/dev/null 2>&1 || { echo "ERROR: gh CLI not found. Install it and run 'gh auth login'."; exit 1; }
  gh auth status >/dev/null 2>&1 || { echo "ERROR: gh not authenticated. Run 'gh auth login'."; exit 1; }
fi

# 0) clear the recurring stale lock (held by the sandbox VM)
if [ -f .git/index.lock ]; then
  if [ "$DRY" = 1 ]; then echo "[dry] would clear stale .git/index.lock";
  else echo "clearing stale .git/index.lock"; rm -f .git/index.lock; fi
fi

# 1) find the newest DL record and confirm it is not yet committed
rec="$(ls 00_owner/decisions/records/DL-*.md 2>/dev/null | sort -V | tail -1)"
if [ -z "${rec:-}" ]; then echo "ERROR: no DL record found under 00_owner/decisions/records/"; exit 1; fi
if git cat-file -e "HEAD:$rec" 2>/dev/null; then
  echo "ERROR: newest record ($rec) is already committed — nothing to ship."; exit 1
fi
base="$(basename "$rec" .md)"
branch="decision/$(printf '%s' "$base" | tr '[:upper:]' '[:lower:]')"
title="${1:-$(sed -n 's/^#[[:space:]]*\(DL-[0-9].*\)$/\1/p' "$rec" | head -1)}"
[ -z "$title" ] && title="$base"
echo "record : $rec"
echo "branch : $branch"
echo "title  : $title"

# 2) stage the change; exclude known junk + this tool's own files
DENY=(
  "tools/ship_canon.sh" "tools/.last_ship.log" "tools/.last_ship.json"
  00_owner/decisions/DL060_RATIFICATION_STUB_DRAFT.md
  00_owner/decisions/PROPOSAL_PHASE1_PROVE_UNDERSTANDING_EXIT_GATE_DL060_DRAFT.md
)
git add -A
git reset -q -- "${DENY[@]}" 2>/dev/null || true
git rm -r --cached -q --ignore-unmatch tools/__pycache__ >/dev/null 2>&1 || true
staged="$(git diff --cached --name-only)"
echo "-- staged files --"; printf '%s\n' "$staged" | sed 's/^/  /'
if [ -z "$staged" ]; then echo "ERROR: nothing staged."; [ "$DRY" = 1 ] && git reset -q; exit 1; fi

# 3) doc-integrity gate locally
if [ -f tools/doc_integrity_check.py ]; then
  echo "-- doc-integrity --"
  if python3 tools/doc_integrity_check.py >/dev/null 2>&1; then echo "doc-integrity PASS";
  else
    echo "doc-integrity FAILED locally"; python3 tools/doc_integrity_check.py 2>&1 | grep -i error | head
    if [ "$DRY" = 0 ]; then echo "ERROR: fix doc-integrity before shipping."; exit 1; fi
  fi
fi

# 4) safety split: create-only if code/ is touched, OR if any touched path has a
#    code owner other than the repo owner (that review must not be bypassed).
OWNER_LOGIN="idris-manley"
MERGE="yes"; MERGE_WHY=""
if printf '%s\n' "$staged" | grep -q '^code/'; then MERGE="no"; MERGE_WHY="touches code/ (app-ci must run first)"; fi
if [ "$MERGE" = "yes" ] && [ -f .github/CODEOWNERS ]; then
  while read -r rule; do
    case "$rule" in ''|'#'*) continue;; esac
    pat="$(printf '%s' "$rule" | awk '{print $1}')"
    others="$(printf '%s' "$rule" | tr ' ' '\n' | grep '^@' | grep -v "^@${OWNER_LOGIN}$" || true)"
    [ -z "$others" ] && continue
    clean="$(printf '%s' "$pat" | sed 's#^/##; s#/$##')"
    if printf '%s\n' "$staged" | grep -q "^${clean}\(/\|$\)"; then
      MERGE="no"
      MERGE_WHY="touches ${pat} - code owner(s) $(printf '%s' "$others" | tr '\n' ' ') must review (Framework 002 section 8c)"
      break
    fi
  done < .github/CODEOWNERS
fi
echo "merge-mode: $MERGE${MERGE_WHY:+  ($MERGE_WHY)}"

# 5-7) commit / push / open PR / merge   (printed only in dry-run)
if [ "$DRY" = 1 ]; then
  echo "-- would run --"
  echo "  git checkout -b $branch"
  echo "  git commit -m \"$title\""
  echo "  git push -u origin $branch"
  echo "  gh pr create --base main --head $branch --fill"
  if [ "$MERGE" = "yes" ]; then echo "  gh pr merge <#> --squash --admin --delete-branch   (canon-only)";
  else echo "  create only (${MERGE_WHY:-guarded}) - merge only after the required review/CI"; fi
  git reset -q                       # restore index — no side effects
  echo "[dry] index restored; nothing committed/pushed/merged."
  echo "== done [DRY-RUN] =="
  exit 0
fi

git checkout -b "$branch" 2>/dev/null || git checkout "$branch"
git commit -q -m "$title"
git push -q -u origin "$branch"
echo "pushed $branch ($(git rev-parse --short HEAD))"

gh pr create --base main --head "$branch" --fill >/dev/null
num="$(gh pr view "$branch" --json number -q .number)"
echo "opened PR #$num"

if [ "$MERGE" = "yes" ]; then
  if gh pr merge "$num" --squash --admin --delete-branch >/dev/null 2>&1; then echo "MERGED PR #$num (admin, canon-only)";
  else echo "WARN: auto-merge failed for PR #$num — run: gh pr merge $num --squash --admin --delete-branch"; fi
else
  echo "PR #$num created; NOT merged - ${MERGE_WHY:-guarded}."
  echo "  Do NOT --admin past a required review. Merge once approved and green."
fi

gh pr view "$num" --json number,title,state,mergedAt,mergeCommit,headRefName,url,statusCheckRollup > "$JSON" 2>/dev/null || true
echo "wrote $JSON"
echo "== done =="
