#!/usr/bin/env bash
# resolve_release_line.sh — ONE resolver for "which release line does this ref carry?"
#
# RB-107. Release-scoped gates (queued-work, the graduation index, resolution conformance) need a
# release line to point at. `main` carries none — and after graduation it will. Both are legitimate
# states, and they are DIFFERENT from the state where a line exists but its checker is missing, which
# is a broken gate. Every caller must be able to tell those three apart, so the telling happens HERE
# once rather than in a copy per workflow step. RELEASE_LINE_CONVENTION.md already says tools must
# resolve the line rather than hardcode it; this is that rule with an exit code.
#
# ⚠️ Callers must NOT infer "no line" from an empty stdout. Read the EXIT CODE.
#
# ⚠️ SCOPE IS AN ARGUMENT, NOT A DEFAULT — and getting this wrong is a regression I shipped into my own
#    RED-proof before catching it. RELEASE_LINE_CONVENTION.md separates two scopes, and the design line's
#    own doc-integrity comment says so in as many words: the graduation index is DELIVERY-scoped
#    ("point it at the design line and it looks for a decision corpus that isn't there"), while
#    queued-work / resolution-conformance are LINE-scoped. A single DELIVERY-first order resolved
#    queued-work to `release-2` on the design line, where the checker lives at `release-2.1/tools/` —
#    turning a passing gate red. Measured end to end, not reasoned about.
#
#   usage: resolve_release_line.sh current    (line under active change control — CURRENT, then DELIVERY)
#          resolve_release_line.sh delivery   (the frozen delivery line — DELIVERY, then CURRENT)
#
#   0  a line was resolved; its directory is on stdout
#   3  NO release line exists on this ref — the check DOES NOT APPLY (a legitimate skip, and the
#      caller must say so and cite this rule; RB-095)
#   1  the ref is INCONSISTENT — a pointer names a line that is not here. That is a broken gate,
#      never a skip: a pointer to nothing is the loudest possible signal that something moved.
set -uo pipefail

emit_err() { echo "resolve_release_line: $*" >&2; }

SCOPE="${1:-}"
case "$SCOPE" in
  current|delivery) ;;
  *) echo "resolve_release_line: scope must be 'current' or 'delivery', got '${SCOPE}'." >&2
     echo "resolve_release_line: refusing to guess — picking the wrong scope silently sends a gate at the wrong line." >&2
     exit 1 ;;
esac

DELIVERY_FILE="DELIVERY_RELEASE"
CURRENT_FILE="CURRENT_RELEASE"

DELIVERY=""; CURRENT=""
[ -f "$DELIVERY_FILE" ] && DELIVERY="$(tr -d '[:space:]' < "$DELIVERY_FILE")"
[ -f "$CURRENT_FILE" ]  && CURRENT="$(tr -d '[:space:]' < "$CURRENT_FILE")"

# ── no pointer at all ⇒ this ref has no release line. Legitimate: main is like this today.
if [ -z "$DELIVERY" ] && [ -z "$CURRENT" ]; then
  # Belt and braces: a ref with release-* directories but no pointer is NOT "no line", it is a ref
  # that lost its pointer — inconsistent, and it must not skip.
  if ls -d release-* >/dev/null 2>&1; then
    emit_err "release-* directories exist but neither $DELIVERY_FILE nor $CURRENT_FILE is present."
    emit_err "That is a ref that LOST its pointer, not a ref without a release line. Refusing to skip."
    exit 1
  fi
  exit 3
fi

# ── a pointer exists: it must name a directory that is actually here. Order follows the SCOPE.
if [ "$SCOPE" = "current" ]; then ORDER="$CURRENT|$DELIVERY"; else ORDER="$DELIVERY|$CURRENT"; fi
IFS='|' read -r FIRST SECOND <<< "$ORDER"
for CAND in "$FIRST" "$SECOND"; do
  [ -n "$CAND" ] || continue
  if [ -d "$CAND" ]; then
    echo "$CAND"
    exit 0
  fi
done

emit_err "scope '$SCOPE': pointer names a release line that is not on this ref: DELIVERY='$DELIVERY' CURRENT='$CURRENT'"
emit_err "A pointer to nothing is a broken gate, not an absent one. Refusing to skip."
exit 1
