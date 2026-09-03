#!/bin/bash
# git_preflight.sh — assert the branch and clear a genuinely stale index.lock, before any git write.
#
# WHY THIS EXISTS
# ---------------
# `.git/index.lock` has blocked a commit FOUR times in four days (2026-08-28 .. 2026-08-31). The first
# instance silently blocked every commit for ~24 hours. Each time the fix was retyped as shell inside a
# chat message, and each time it was retyped slightly differently — which is the same "prose instead of
# apparatus" failure the owner named on 2026-08-31 about IMs to engineering. A mechanism that lives in a
# message is not a mechanism.
#
# ⚠️ THREE DIAGNOSES WERE OFFERED BEFORE THE EVIDENCE SETTLED IT. Recorded because the wrong turns are
# instructive:
#   1. "stale crash artifact"  — right, but asserted from a single sample.
#   2. "a live periodic writer" (an editor running `git status`) — WRONG. Ruled out by measurement:
#      10 retries across ~24s, the lock never cleared and no holder ever appeared. A periodic writer
#      releases between samples; this did not.
#   3. back to stale — and the retry-only block written under diagnosis 2 could not fix it, because
#      **retry handles a LIVE holder; removal handles a DEAD one.** The condition needed both.
#
# THE TEST IS EMPIRICAL, NOT A GUESSED THRESHOLD. The old rule ("older than 2 minutes") was arbitrary.
# What was actually proved is: *no holder across a sampling window, and the file is 0 bytes.* A git
# process mid-write holds an OPEN, NON-EMPTY lock; a crashed one leaves an empty file with no owner.
#
# ⚠️ NEVER removes a non-empty lock, and never removes one while any `git` process is running.
#
#   tools/git_preflight.sh <expected-branch>     exit 0 = safe to proceed
#   tools/git_preflight.sh --self-test
set -u

# ⚠️ `stat -f %m` is BSD/macOS. On GNU/Linux `-f` means FILESYSTEM stat and SUCCEEDS with non-numeric
# output, so a naive `stat -f %m || stat -c %Y` silently yields garbage and the arithmetic that follows
# aborts the script. Validate that the result is a number instead of trusting the exit code — the exit
# code is a proxy; the value is the subject.
mtime_of() {
  local m
  m=$(stat -f %m "$1" 2>/dev/null)
  case "$m" in (*[!0-9]*|"") m=$(stat -c %Y "$1" 2>/dev/null) ;; esac
  case "$m" in (*[!0-9]*|"") m="" ;; esac
  printf '%s' "$m"
}

# Who, if anyone, might own the lock. ⚠️ DELIBERATELY GLOBAL: a git process working on this repo can
# be invoked from anywhere and need not name the repo on its command line, so scoping the scan by path
# would miss real holders — and missing a live holder is the failure that corrupts an index. The cost
# is that an unrelated git process elsewhere on the machine makes this refuse. **Refusing too often is
# recoverable; removing a live lock is not.**
#
# ⚠️ It is injectable ONLY so the self-test can be deterministic. Reading the real process table made
# the same self-test pass and then fail within a minute — a test whose result depends on what else the
# machine happens to be doing proves nothing in either direction.
holder_probe() {
  if [ -n "${GIT_PREFLIGHT_FAKE_HOLDER+x}" ]; then printf '%s' "$GIT_PREFLIGHT_FAKE_HOLDER"; return 0; fi
  ps -Ao pid,etime,command 2>/dev/null | grep "[g]it " | grep -v grep
}

age_minutes() {
  local m; m=$(mtime_of "$1")
  if [ -z "$m" ]; then printf 'unknown'; else printf '%s' $(( ( $(date +%s) - m ) / 60 )); fi
}

preflight() {
  local repo="$1" expected="${2:-}" lock="$1/.git/index.lock" branch hold p
  local sample="${GIT_PREFLIGHT_SAMPLE:-10}"
  if [ -n "$expected" ]; then
    branch=$(git -C "$repo" rev-parse --abbrev-ref HEAD 2>/dev/null)
    if [ "$branch" != "$expected" ]; then
      echo "ABORT: on '$branch', expected '$expected'"; return 1
    fi
    echo "branch OK: $branch"
  fi
  [ -f "$lock" ] || { echo "no index.lock"; return 0; }

  echo "index.lock present: $(wc -c <"$lock" | tr -d ' ') bytes, $(age_minutes "$lock")m old"

  # A NON-EMPTY lock may be a real operation mid-write. Never touch it.
  if [ -s "$lock" ]; then
    echo "REFUSING: lock is non-empty — a real git operation may own it."; return 1
  fi

  hold=""
  for _ in $(seq 1 "$sample"); do
    p=$(holder_probe)
    if [ -n "$p" ]; then hold="$p"; break; fi
    sleep 1
  done
  if [ -n "$hold" ]; then
    echo "REFUSING: a git process is running — the lock may be live:"; echo "$hold"; return 1
  fi

  rm -f "$lock" && echo "stale lock removed (0 bytes, no holder across ${sample}s)"
}

self_test() {
  local t fails=0
  t=$(mktemp -d); mkdir -p "$t/.git"

  export GIT_PREFLIGHT_SAMPLE=1

  # GREEN: empty lock, provably no holder → removed.
  : > "$t/.git/index.lock"
  GIT_PREFLIGHT_FAKE_HOLDER="" preflight "$t" >/dev/null 2>&1
  [ -f "$t/.git/index.lock" ] && { echo "  ✗ an empty, unheld lock was NOT removed"; fails=1; }

  # RED: empty lock but a holder IS present → must refuse AND leave it.
  : > "$t/.git/index.lock"
  if GIT_PREFLIGHT_FAKE_HOLDER="1234 00:03 git commit" preflight "$t" >/dev/null 2>&1; then
    echo "  ✗ a lock was accepted while a git process was running"; fails=1
  fi
  [ -f "$t/.git/index.lock" ] || { echo "  ✗ a HELD lock was REMOVED — this is how an index corrupts"; fails=1; }

  # RED: non-empty lock → refuse regardless of holder.
  echo "not empty" > "$t/.git/index.lock"
  if GIT_PREFLIGHT_FAKE_HOLDER="" preflight "$t" >/dev/null 2>&1; then
    echo "  ✗ a NON-EMPTY lock was accepted — it must refuse"; fails=1
  fi
  [ -f "$t/.git/index.lock" ] || { echo "  ✗ a NON-EMPTY lock was REMOVED — never do this"; fails=1; }

  rm -f "$t/.git/index.lock"
  GIT_PREFLIGHT_FAKE_HOLDER="" preflight "$t" >/dev/null 2>&1 || { echo "  ✗ a clean repo did not pass"; fails=1; }

  if preflight "$(pwd)" "definitely-not-a-real-branch-xyz" >/dev/null 2>&1; then
    echo "  ✗ a wrong branch did not abort"; fails=1
  fi

  rm -rf "$t"
  if [ "$fails" -ne 0 ]; then echo "SELF-TEST FAILED"; return 1; fi
  echo "self-test OK — removes an empty UNHELD lock; REFUSES and preserves a lock while a git process"
  echo "is running; REFUSES and preserves a NON-EMPTY lock; passes a clean repo; aborts on the wrong"
  echo "branch. Both refusal guards are RED-proved: sabotaging either one fails this test."
}

if [ "${1:-}" = "--self-test" ]; then self_test; exit $?; fi
preflight "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" "${1:-}"
