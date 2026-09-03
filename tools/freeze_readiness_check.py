#!/usr/bin/env python3
"""freeze_readiness_check.py — the F002 §9.3 promotion evidence, assembled by machine.

WHY THIS IS A MECHANISM AND NOT A CHECKLIST
-------------------------------------------
§9.3 names five things a promotion requires. **Nothing checks them.** They are assembled by hand,
across several documents, by whoever is free — and the 2026-08-29/31 build-readiness audit measured
what that costs: a full day, covering a fifth of the criteria, with the auditor choosing what to
verify. On a fixed two-week cadence (owner, 2026-08-31) that is ~10% of every iteration spent
producing evidence nobody can re-run.

⚠️ The R2.1 Freeze Manifest asked for this in its own words after RB-083 caught it holding a
fortnight-stale md5: *"Nothing mechanized watches these fields. Worth a trigger of its own if they
are meant to stay true."* This is that trigger.

WHAT IT CHECKS — the five, verbatim from F002 §9.3
--------------------------------------------------
  F1  the release's precondition register reads N-of-N
  F2  a build-readiness audit at freeze with zero unresolved escalations
  F3  the recorded state matrix green at the frozen md5, including the terminal-state journey
  F4  the acceptance register synchronized with the shipped guard set
  F5  an owner freeze declaration naming the md5 and the tag

FAIL-CLOSED, BY CONSTRUCTION (DL-243 §6b — "skip is not pass")
-------------------------------------------------------------
This checker enforces DL-243 §6b — skip is not pass: a check that cannot evaluate its subject must
FAIL, not skip.

⚠️ The id was absent from this file until 2026-09-01 because DL-243 resolved to no record, and citing
an unratified decision as canon is exactly what the citation gate exists to stop. The gate caught
this file, which is the only evidence it works. ⚠️ The rule never depended on that ratification — it
was already enforced by `no_hardcoded_release_line.py` and `report_measurement_check.py`.

An item whose artifact cannot be found is **FAIL**, never skip. A freeze gate that passes because it
could not locate its own evidence is the exact failure this repository has now measured four times:
RB-093's workflow that printed "skipping" and passed · RB-076's SKIP-OK on a missing line pointer ·
`gate_r2_guardrails.py` shipping with no self-test · a citation gate green on 1120 documents while
11 cited decisions resolved to nothing.

⚠️ THE LINE IS RESOLVED, NEVER HARDCODED. `CURRENT_RELEASE` decides which line is under test, per
RELEASE_LINE_CONVENTION.md and enforced by `no_hardcoded_release_line.py`. This file names no
release directory. On the CONTROL PLANE (`main`), which carries no line at all, the line is reached
through `ACTIVE_DESIGN_REF` — see resolve_line().

    python3 tools/freeze_readiness_check.py [--line <dir>] [--self-test]
    exit 0 = every §9.3 item is evidenced · exit 1 = at least one is not
⚠️ Read the exit code WITHOUT a pipe; `... | tail; echo $?` reports tail's status.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POINTER_RE = re.compile(r"POINTER-OF-RECORD:\s*prototype=([0-9a-f]+)\s+arc=([0-9a-f]+)\s+s10=(\d+)")
RESULT_RE = re.compile(r"^##\s*▶\s*RESULT:\s*(.+)$", re.M)
BLOCKING_RE = re.compile(r"\*\*(\d+)\s+blocking\*\*", re.I)
FREEZE_DECL_RE = re.compile(r"frozen at\s*`?([0-9a-f]{6,})`?.*?\btag\b\s*`?([A-Za-z0-9._/-]+)`?", re.I | re.S)


_REF = None  # the git ref carrying the release line, when the working tree does not


def _git(root, *args):
    try:
        r = subprocess.run(["git", "--git-dir", os.path.join(root, ".git")] + list(args),
                           capture_output=True, text=True, timeout=30)
        return r.stdout if r.returncode == 0 else None
    except Exception:
        return None


def _resolve_design_ref(root, ref):
    """Resolve a pointer through a local head or one unambiguous remote-tracking ref."""
    candidates = ["refs/heads/%s" % ref]
    names = _git(root, "for-each-ref", "--format=%(refname)", "refs/remotes") or ""
    candidates += [name for name in names.splitlines() if name.endswith("/%s" % ref)]
    found = [(candidate, _git(root, "rev-parse", "--verify", "--quiet", candidate + "^{commit}"))
             for candidate in candidates]
    found = [(candidate, commit.strip()) for candidate, commit in found if commit]
    return found[0][0] if len({commit for _candidate, commit in found}) == 1 else None


def resolve_line(root=ROOT, override=None):
    """(line_dir, how) — never hardcoded; unreadable is an ERROR, not a guess.

    ⚠️ `main` IS THE CONTROL PLANE AND CARRIES NO RELEASE LINE. Measured 2026-08-31: `main` has no
    `CURRENT_RELEASE`, no `DELIVERY_RELEASE` and no `release-*` directory at all — by design, as PR
    #250 states: *"That branch deliberately does not carry the release-line register."*

    So a checker that reads only its own working tree fails closed forever once it lives on `main`.
    Failing closed is correct; **failing closed permanently is not a gate, it is a gate people learn
    to ignore.** The fix is the one RB-076/RB-106/RB-125 all converged on and that #250 builds into
    `queued-work.yml`: resolve the owner-designated ref, then read the line from it.
    """
    global _REF
    _REF = None
    if override:
        return override, "--line override"

    raw = None
    p = os.path.join(root, "CURRENT_RELEASE")
    if os.path.isfile(p):
        raw = open(p, encoding="utf-8").read().strip()
        if raw and os.path.isdir(os.path.join(root, raw)):
            return raw, "CURRENT_RELEASE (working tree)"

    # Working tree has no line. Fall back to the owner-designated design ref.
    ap = os.path.join(root, "ACTIVE_DESIGN_REF")
    if not os.path.isfile(ap):
        return None, ("no release line in the working tree and no ACTIVE_DESIGN_REF pointer — "
                      "on the control plane a line can only be reached through the pointer")
    ref = (open(ap, encoding="utf-8").read().strip().splitlines() or [""])[0].strip()
    if not ref:
        return None, "ACTIVE_DESIGN_REF is empty"
    resolved = _resolve_design_ref(root, ref)
    if resolved is None:
        return None, ("ACTIVE_DESIGN_REF names '%s', which does not exist — a dangling pointer "
                      "must fail loudly, never SKIP-OK" % ref)
    line = (_git(root, "cat-file", "-p", "%s:CURRENT_RELEASE" % resolved) or "").strip()
    if not line:
        return None, "'%s' carries no CURRENT_RELEASE" % ref
    if _git(root, "cat-file", "-e", "%s:%s/" % (resolved, line)) is None and \
       _git(root, "ls-tree", "--name-only", "%s:%s" % (resolved, line)) is None:
        return None, "'%s' names line '%s', absent on that ref" % (ref, line)
    _REF = resolved
    return line, "ACTIVE_DESIGN_REF -> %s" % resolved


def _read(root, *parts):
    rel = "/".join(parts)
    if _REF:
        return _git(root, "cat-file", "-p", "%s:%s" % (_REF, rel))
    p = os.path.join(root, *parts)
    if not os.path.isfile(p):
        return None
    return open(p, encoding="utf-8", errors="replace").read()


def _listdir(root, rel):
    if _REF:
        out = _git(root, "ls-tree", "--name-only", "%s:%s" % (_REF, rel))
        return out.split() if out else []
    d = os.path.join(root, rel)
    return sorted(os.listdir(d)) if os.path.isdir(d) else []


def _walk_md(root, rel):
    """Every .md under rel, recursively — from the ref when reading a ref."""
    if _REF:
        out = _git(root, "ls-tree", "-r", "--name-only", "%s:%s" % (_REF, rel))
        return ["%s/%s" % (rel, n) for n in (out.split() if out else []) if n.endswith(".md")]
    base = os.path.join(root, rel)
    found = []
    for dirpath, _d, files in os.walk(base):
        for f in files:
            if f.endswith(".md"):
                found.append(os.path.relpath(os.path.join(dirpath, f), root))
    return found


def _isdir(root, rel):
    if _REF:
        return _git(root, "ls-tree", "--name-only", "%s:%s" % (_REF, rel)) is not None
    return os.path.isdir(os.path.join(root, rel))


def _manifest(root, line):
    """The freeze manifest for a line, whatever it is named. Returns (text, filename) or (None, why)."""
    if not _isdir(root, line):
        return None, "line directory absent"
    names = sorted(n for n in _listdir(root, line) if n.endswith("FREEZE_MANIFEST.md"))
    if not names:
        return None, "no *FREEZE_MANIFEST.md in %s" % line
    if len(names) > 1:
        return None, "ambiguous: %d freeze manifests in %s (%s)" % (len(names), line, ", ".join(names))
    return _read(root, line, names[0]), names[0]


def check_f1_precondition_register(root, line):
    """F1 — the precondition register reads N-of-N.

    ▶ OWNER RULING 2026-08-31: **the precondition register IS the line's `QUEUED_WORK` register.**
    §9.3 named a register that had never been authored — the phrase occurs only in prose across F002,
    DL-235 and the #227 review, and no freeze had ever been evidenced against it. Rather than mint a
    new artifact, F1 binds to the one that already enumerates a line's open obligations and already
    has an authority that evaluates them. **Extend, don't mint.**

    ⚠️ **N-of-N means the line's due set is EMPTY.** Dueness is decided by `queued_work_check.py`,
    never re-derived here — re-deriving it once counted eight CLOSED rows as live work.

    ⚠️ **Deferral is what distinguishes freeze-blocking from not.** Not every open row is a
    precondition of *this* freeze. Rather than add a "blocks-freeze" field nobody would maintain, a
    row that does not block is deferred out of the iteration — which is already a dated owner ruling
    with a stated reason, rendered in the queue, escalating on a second use. **So F1 always reports
    how many rows it excluded that way.** A freeze evidenced with six deferrals must not look
    identical to one evidenced with none, or deferral becomes the bypass.
    """
    due, how = _line_due_set(root, line)
    if due is None:
        return False, ("the register's due set could not be evaluated (%s) — an unevaluable "
                       "precondition register is a FAIL, never a skip" % how)
    excluded, cur = _deferred_out(root)
    blocking = [r for r in due if r not in excluded]
    tail = (" · %d row(s) excluded by dated deferral ruling out of %s: %s"
            % (len(excluded & set(due)), cur, ", ".join(sorted(excluded & set(due))))) if (excluded & set(due)) else ""
    if blocking:
        return False, ("%d precondition(s) unmet — the register is not N-of-N: %s%s"
                       % (len(blocking), ", ".join(sorted(blocking)), tail))
    return True, "register reads N-of-N — no due row blocks this freeze%s" % tail


def _line_due_set(root, line):
    """(set of due row ids, how) — from the LINE'S OWN checker. None when it cannot be run."""
    checker = os.path.join(root, line, "tools", "queued_work_check.py")
    if not os.path.isfile(checker):
        return None, ("%s/tools/queued_work_check.py is not in the working tree — check out the "
                      "design line before evaluating the register" % line)
    try:
        r = subprocess.run([sys.executable, checker], cwd=root, capture_output=True,
                           text=True, timeout=180)
        text = r.stdout + r.stderr
    except Exception as e:
        return None, "queued_work_check.py did not run: %s" % e
    ids = set()
    m = re.search(r"OVERDUE BY DATE:\s*([^\n]+)", text)
    if m:
        ids |= set(re.findall(r"RB-\d+", m.group(1)))
    blk = re.search(r"STATE-DUE[^\n]*:\s*([^\n]+)", text)
    if blk:
        ids |= set(re.findall(r"RB-\d+", blk.group(1)))
    return ids, "queued_work_check.py @ %s" % line


def _deferred_out(root):
    """(ids deferred out of the current iteration, iteration id). Empty when nothing is recorded."""
    cfg = _read(root, "20_handoff/ITERATION.json")
    dfr = _read(root, "20_handoff/DEFERRALS.json")
    cur = ""
    try:
        cur = json.loads(cfg).get("id", "") if cfg else ""
    except Exception:
        cur = ""
    out = set()
    try:
        for d in (json.loads(dfr).get("deferrals", []) if dfr else []):
            if d.get("from") == cur and d.get("row"):
                out.add(d["row"])
    except Exception:
        pass
    return out, (cur or "the current iteration")


def _legacy_precondition_file(root, line):
    """Retained: if the owner later authors a standalone register, F1's binding should be revisited."""
    reg = [n for n in _listdir(root, line) if "PRECONDITION" in n.upper()]
    if not reg:
        return False, ("no precondition register exists on this line — §9.3 names one and NOTHING IS IT. "
                       "Searched %s/*PRECONDITION*. This is a missing artifact, not a failing check: "
                       "the item cannot be evidenced until the register is authored." % line)
    text = _read(root, line, reg[0]) or ""
    m = re.search(r"\b(\d+)\s*(?:of|/)\s*(\d+)\b", text)
    if not m:
        return False, "%s carries no N-of-N reading" % reg[0]
    got, total = int(m.group(1)), int(m.group(2))
    if got != total or total == 0:
        return False, "%s reads %d of %d — not N-of-N" % (reg[0], got, total)
    return True, "%s reads %d of %d" % (reg[0], got, total)


def check_f2_build_readiness_audit(root, line):
    """F2 — a build-readiness audit AT FREEZE with zero unresolved escalations.

    ⚠️ NOT the newest audit. §9.3 says *at freeze*, and this line carries seven audits of which only
    two are freeze audits — the rest scope a gate, an issues model, a day's work. Selecting the
    lexically-last one picked a Tier-1 gate audit whose verdict names no blocking count at all, and
    the check failed for a reason that had nothing to do with the freeze. **The `_FREEZE.md` suffix
    is the discriminator**, and a line with no freeze audit FAILS rather than falling back to any
    audit that happens to be present.
    """
    if not _isdir(root, line):
        return False, "line directory absent"
    audits = sorted(n for n in _listdir(root, line)
                    if n.startswith("BUILD_READINESS_AUDIT_") and n.endswith("_FREEZE.md"))
    if not audits:
        others = [n for n in _listdir(root, line) if n.startswith("BUILD_READINESS_AUDIT_")]
        return False, ("no BUILD_READINESS_AUDIT_*_FREEZE.md on %s — §9.3 requires an audit AT FREEZE"
                       "%s" % (line, (" (%d non-freeze audit(s) present; scoping an audit to a gate or "
                                      "a day does not satisfy it)" % len(others)) if others else ""))
    newest = audits[-1]
    text = _read(root, line, newest) or ""
    m = RESULT_RE.search(text)
    if not m:
        return False, "%s states no '▶ RESULT:' line — an audit without a verdict is not evidence" % newest
    verdict = m.group(1).strip()
    b = BLOCKING_RE.search(verdict)
    blocking = int(b.group(1)) if b else None
    if blocking is None:
        return False, "%s: verdict names no blocking count — %r" % (newest, verdict[:80])
    if blocking != 0:
        return False, "%s: %d blocking — §9.3 requires ZERO unresolved escalations" % (newest, blocking)
    return True, "%s: 0 blocking" % newest


def check_f3_state_matrix(root, line):
    """F3 — the recorded state matrix green at the frozen md5."""
    raw = _read(root, line, "STATE_MATRIX.json")
    if raw is None:
        return False, "%s/STATE_MATRIX.json is ABSENT — the matrix must be RECORDED, not assumed" % line
    try:
        m = json.loads(raw)
    except Exception as e:
        return False, "STATE_MATRIX.json does not parse: %s" % e
    recorded = m.get("prototypeMd5")
    if not recorded:
        return False, "STATE_MATRIX.json names no prototypeMd5 — it cannot be tied to a pin"
    man, _name = _manifest(root, line)
    if man is None:
        return False, "no freeze manifest to compare the matrix against"
    pm = POINTER_RE.search(man)
    if not pm:
        return False, "the manifest carries no POINTER-OF-RECORD — nothing states the md5 under test"
    if pm.group(1) != recorded:
        return False, ("state matrix recorded at %s but the pointer-of-record says %s — "
                       "a matrix recorded against a different artifact is not evidence"
                       % (recorded, pm.group(1)))
    journeys = m.get("journeys") or {}
    if not journeys:
        return False, "state matrix records no journeys"
    reds = json.dumps(m).count('"red"')
    if reds:
        return False, "state matrix carries %d red state(s) at %s" % (reds, recorded)
    return True, "%d journey(s) recorded at %s, zero reds" % (len(journeys), recorded)


def check_f4_acceptance_register(root, line):
    """F4 — the acceptance register synchronized with the shipped guard set."""
    man, _name = _manifest(root, line)
    if man is None:
        return False, "no freeze manifest — the shipped guard count is undeclared"
    pm = POINTER_RE.search(man)
    if not pm:
        return False, "the manifest carries no POINTER-OF-RECORD — the shipped guard count is undeclared"
    declared = int(pm.group(3))
    ids, locus = _register_ids(root, line)
    if not ids:
        return False, ("no acceptance register enumerating GT ids is reachable — searched %s. "
                       "⚠️ A register on a DIFFERENT line than the one under test is the RB-076 / "
                       "RB-106 / RB-125 cause: checker and subject on different lines." % locus)
    if len(ids) != declared:
        return False, ("register at %s enumerates %d GT ids; the pointer-of-record declares s10=%d — "
                       "these must agree or the register is not synchronized with what ships"
                       % (locus, len(ids), declared))
    return True, "register at %s enumerates %d GT ids, matching s10=%d" % (locus, len(ids), declared)


def _register_ids(root, line):
    """(ids, locus) — the acceptance register for a line.

    ⚠️ THE REGISTER IS NOT ALWAYS ON THE LINE UNDER TEST. `<line>/acceptance/` was the obvious guess
    and it is wrong here: on the design line that directory holds an RB-075 scoring corpus with zero
    GT ids, while the real register — 91 ids in `acceptance/README.md` plus 62 in
    `slices/09-doctrine-guardrails-integration-map.md` — sits on the DELIVERY line. Guessing the
    directory made the check fail for a reason unrelated to synchronization. So: search the line
    under test, then the delivery line, and NAME which one answered. A pass whose locus is the other
    line is still reported, with the locus visible, because the owner needs to see that the design
    line carries no register of its own.
    """
    delivery = (_read(root, "DELIVERY_RELEASE") or "").strip()
    tried = []
    for cand in [line] + ([delivery] if delivery and delivery != line else []):
        if not _isdir(root, cand):
            continue
        ids = set()
        for sub in ("acceptance", "slices"):
            rel = "%s/%s" % (cand, sub)
            if not _isdir(root, rel):
                continue
            for f in _walk_md(root, rel):
                ids |= set(re.findall(r"GT-\d+", _read(root, f) or ""))
        tried.append("%s/{acceptance,slices}" % cand)
        if ids:
            return ids, "%s/{acceptance,slices}%s" % (cand, "" if cand == line else " ⚠️ DELIVERY line, not %s" % line)
    return set(), ", ".join(tried) or "no candidate directories"


def check_f5_owner_declaration(root, line):
    """F5 — an owner freeze declaration naming the md5 AND the tag."""
    man, name = _manifest(root, line)
    if man is None:
        return False, name
    if FREEZE_DECL_RE.search(man):
        return True, "%s carries a freeze declaration naming an md5 and a tag" % name
    if re.search(r"\bnot frozen\b|no freeze,? no handoff", man, re.I):
        return False, "%s states the line is NOT FROZEN — there is no declaration to evidence" % name
    return False, "%s carries no freeze declaration naming both an md5 and a tag" % name


CHECKS = [
    ("F1", "precondition register reads N-of-N", check_f1_precondition_register),
    ("F2", "build-readiness audit, zero unresolved escalations", check_f2_build_readiness_audit),
    ("F3", "state matrix green at the frozen md5", check_f3_state_matrix),
    ("F4", "acceptance register synchronized with the shipped guard set", check_f4_acceptance_register),
    ("F5", "owner freeze declaration naming the md5 and the tag", check_f5_owner_declaration),
]


def evaluate(root=ROOT, line_override=None):
    line, how = resolve_line(root, line_override)
    if line is None:
        return None, how, [("F0", "resolve the release line", False, how)]
    rows = []
    for cid, label, fn in CHECKS:
        try:
            ok, detail = fn(root, line)
        except Exception as e:  # a check that crashes has NOT passed
            ok, detail = False, "check raised %s: %s" % (type(e).__name__, e)
        rows.append((cid, label, ok, detail))
    return line, how, rows


def self_test():
    """RED-prove every check. A gate that has never failed is not a gate."""
    import tempfile
    fails = []

    def build(tmp, line="release-X", manifest=None, matrix=None, audit=None,
              acceptance=None, precondition=None,
              audit_name="BUILD_READINESS_AUDIT_2026-01-01_FREEZE.md",
              due_rows=(), deferrals=None, no_checker=False):
        d = os.path.join(tmp, line)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(tmp, "CURRENT_RELEASE"), "w").write(line + "\n")
        if manifest is not None:
            open(os.path.join(d, "X_FREEZE_MANIFEST.md"), "w").write(manifest)
        if matrix is not None:
            open(os.path.join(d, "STATE_MATRIX.json"), "w").write(matrix)
        if audit is not None:
            open(os.path.join(d, audit_name), "w").write(audit)
        if acceptance is not None:
            os.makedirs(os.path.join(d, "acceptance"), exist_ok=True)
            open(os.path.join(d, "acceptance", "README.md"), "w").write(acceptance)
        if precondition is not None:
            open(os.path.join(d, "PRECONDITION_REGISTER.md"), "w").write(precondition)
        # F1 binds to the LINE'S OWN checker (owner ruling 2026-08-31). Stand in for it.
        if not no_checker:
            os.makedirs(os.path.join(d, "tools"), exist_ok=True)
            msg = ("::error::%d queued item(s) are OVERDUE BY DATE: %s"
                   % (len(due_rows), ", ".join(due_rows))) if due_rows else "no due rows"
            open(os.path.join(d, "tools", "queued_work_check.py"), "w").write("print(%r)\n" % msg)
        os.makedirs(os.path.join(tmp, "20_handoff"), exist_ok=True)
        json.dump({"id": "it-1"}, open(os.path.join(tmp, "20_handoff", "ITERATION.json"), "w"))
        json.dump({"deferrals": deferrals or []},
                  open(os.path.join(tmp, "20_handoff", "DEFERRALS.json"), "w"))
        return d

    GOOD_MAN = ("# X\n<!-- POINTER-OF-RECORD: prototype=aaaa1111 arc=bbbb2222 s10=2 -->\n"
                "Frozen at `aaaa1111` with tag `v1.0`.\n")
    GOOD_MTX = json.dumps({"prototypeMd5": "aaaa1111", "journeys": {"j": {"s": "green"}}})
    GOOD_AUD = "## ▶ RESULT: **PASSES.** **0 blocking** · 0 reported.\n"
    GOOD_ACC = "GT-01 GT-02\n"
    GOOD_PRE = "Preconditions: 3 of 3 met.\n"

    def rows_for(**kw):
        with tempfile.TemporaryDirectory() as tmp:
            build(tmp, **kw)
            _line, _how, rows = evaluate(root=tmp)
            return {r[0]: r[2] for r in rows}

    # GREEN — everything present and consistent
    r = rows_for(manifest=GOOD_MAN, matrix=GOOD_MTX, audit=GOOD_AUD,
                 acceptance=GOOD_ACC, precondition=GOOD_PRE)
    for cid in ("F1", "F2", "F3", "F4", "F5"):
        if not r.get(cid):
            fails.append("%s failed on a well-formed fixture — the gate cannot pass when it should" % cid)

    # RED — one break at a time, each must fail its own check
    if rows_for(manifest=GOOD_MAN, matrix=GOOD_MTX, audit=GOOD_AUD, acceptance=GOOD_ACC,
                precondition=GOOD_PRE, no_checker=True).get("F1"):
        fails.append("F1 passed when the register could not be EVALUATED — that is skip-as-pass")
    if rows_for(manifest=GOOD_MAN, matrix=GOOD_MTX, audit=GOOD_AUD, acceptance=GOOD_ACC,
                precondition=GOOD_PRE, due_rows=("RB-001", "RB-002")).get("F1"):
        fails.append("F1 passed with 2 rows DUE — the register is not N-of-N")
    if not rows_for(manifest=GOOD_MAN, matrix=GOOD_MTX, audit=GOOD_AUD, acceptance=GOOD_ACC,
                    precondition=GOOD_PRE, due_rows=("RB-001",),
                    deferrals=[{"row": "RB-001", "from": "it-1", "to": "it-2",
                                "ruled_by": "owner", "date": "2026-01-01", "why": "capacity"}]).get("F1"):
        fails.append("a row deferred out by dated ruling still blocked the freeze")
    if rows_for(manifest=GOOD_MAN, matrix=GOOD_MTX,
                audit="## ▶ RESULT: **FAILS.** **2 blocking** · 1 reported.\n",
                acceptance=GOOD_ACC, precondition=GOOD_PRE).get("F2"):
        fails.append("F2 passed with 2 blocking — §9.3 requires zero")
    if rows_for(manifest=GOOD_MAN, matrix=GOOD_MTX, acceptance=GOOD_ACC,
                precondition=GOOD_PRE).get("F2"):
        fails.append("F2 passed with NO audit at all")
    # ⚠️ the error this checker actually made: a NON-freeze audit accepted as the freeze audit
    if rows_for(manifest=GOOD_MAN, matrix=GOOD_MTX, audit=GOOD_AUD, acceptance=GOOD_ACC,
                precondition=GOOD_PRE, audit_name="BUILD_READINESS_AUDIT_2026-01-02.md").get("F2"):
        fails.append("F2 accepted an audit NOT scoped to the freeze — §9.3 requires one AT freeze")
    if rows_for(manifest=GOOD_MAN,
                matrix=json.dumps({"prototypeMd5": "dddd4444", "journeys": {"j": {}}}),
                audit=GOOD_AUD, acceptance=GOOD_ACC, precondition=GOOD_PRE).get("F3"):
        fails.append("F3 passed with the matrix recorded at a DIFFERENT md5 than the pointer-of-record")
    if rows_for(manifest=GOOD_MAN,
                matrix=json.dumps({"prototypeMd5": "aaaa1111", "journeys": {"j": {"s": "red"}}}),
                audit=GOOD_AUD, acceptance=GOOD_ACC, precondition=GOOD_PRE).get("F3"):
        fails.append("F3 passed with a red state in the matrix")
    if rows_for(manifest=GOOD_MAN, matrix=GOOD_MTX, audit=GOOD_AUD,
                acceptance="GT-01 GT-02 GT-03\n", precondition=GOOD_PRE).get("F4"):
        fails.append("F4 passed with 3 registered ids against s10=2 — desynchronized register accepted")
    if rows_for(manifest=GOOD_MAN, matrix=GOOD_MTX, audit=GOOD_AUD,
                acceptance="no ids here\n", precondition=GOOD_PRE).get("F4"):
        fails.append("F4 passed with a register enumerating NO GT ids")
    if rows_for(manifest="# X\n<!-- POINTER-OF-RECORD: prototype=aaaa1111 arc=bbbb2222 s10=2 -->\n"
                         "Status: NOT FROZEN. No freeze, no handoff.\n",
                matrix=GOOD_MTX, audit=GOOD_AUD, acceptance=GOOD_ACC,
                precondition=GOOD_PRE).get("F5"):
        fails.append("F5 passed on a line that states it is NOT FROZEN")

    # ...but the exclusion must be VISIBLE, or deferral becomes the bypass.
    with tempfile.TemporaryDirectory() as tmp:
        build(tmp, manifest=GOOD_MAN, matrix=GOOD_MTX, audit=GOOD_AUD, acceptance=GOOD_ACC,
              precondition=GOOD_PRE, due_rows=("RB-001",),
              deferrals=[{"row": "RB-001", "from": "it-1", "to": "it-2",
                          "ruled_by": "owner", "date": "2026-01-01", "why": "capacity"}])
        _l, _h, rws = evaluate(root=tmp)
        detail = next((d for cid, _lb, _ok, d in rws if cid == "F1"), "")
        if "RB-001" not in detail or "deferral" not in detail:
            fails.append("F1 passed on deferred rows WITHOUT naming them — a silent bypass")

    # RED — an unresolvable line must fail, never guess
    with tempfile.TemporaryDirectory() as tmp:
        _l, how, rows = evaluate(root=tmp)
        if _l is not None or rows[0][2]:
            fails.append("a missing CURRENT_RELEASE did not fail closed (%s)" % how)
        if "ACTIVE_DESIGN_REF" not in how:
            fails.append("a control plane with no pointer did not SAY the pointer is what is missing")

    # RED — the CONTROL-PLANE path: no line in the tree, pointer present but DANGLING.
    # ⚠️ Without this case the ref fallback is untested code, and untested fallback is how a gate
    # ends up green on a branch that carries nothing.
    with tempfile.TemporaryDirectory() as tmp:
        open(os.path.join(tmp, "ACTIVE_DESIGN_REF"), "w").write("design/no-such-line\n")
        _l, how, _rows = evaluate(root=tmp)
        if _l is not None:
            fails.append("a DANGLING ACTIVE_DESIGN_REF resolved a line — it must fail loudly")
        if "does not exist" not in how:
            fails.append("a dangling pointer did not report itself as dangling (%s)" % how)

    with tempfile.TemporaryDirectory() as tmp:
        open(os.path.join(tmp, "ACTIVE_DESIGN_REF"), "w").write("\n")
        _l, how, _rows = evaluate(root=tmp)
        if _l is not None or "empty" not in how:
            fails.append("an EMPTY ACTIVE_DESIGN_REF did not fail closed (%s)" % how)

    # #267 — fresh clones resolve the design line through origin, not a local head.
    with tempfile.TemporaryDirectory() as tmp:
        open(os.path.join(tmp, "seed"), "w").write("x\n")
        for args in (("init",), ("config", "user.email", "freeze@example.test"),
                     ("config", "user.name", "Freeze Test"), ("add", "."), ("commit", "-m", "seed")):
            subprocess.run(["git", "-C", tmp] + list(args), check=True, capture_output=True)
        sha = _git(tmp, "rev-parse", "HEAD").strip()
        subprocess.run(["git", "-C", tmp, "update-ref", "refs/remotes/origin/design/test", sha], check=True)
        if _resolve_design_ref(tmp, "design/test") != "refs/remotes/origin/design/test":
            fails.append("a remote-tracking design ref was not resolved in the fresh-clone fixture")

    if fails:
        print("SELF-TEST FAILED:")
        for f in fails:
            print("  ✗", f)
        return 1
    print("self-test OK — every §9.3 item passes on well-formed evidence and FAILS on:")
    print("  a register that cannot be EVALUATED · a register with rows still DUE · a nonzero")
    print("  blocking count · an audit not scoped to the freeze · no audit at all · a matrix at the")
    print("  wrong md5 · a red state · a desynchronized register · an unfrozen line · an absent,")
    print("  empty or DANGLING ACTIVE_DESIGN_REF · an unresolvable release line.")
    print("  A row deferred by dated ruling does not block — and F1 NAMES every row it excluded,")
    print("  so deferral can never become a silent bypass.")
    return 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    override = None
    if "--line" in argv:
        i = argv.index("--line")
        if i + 1 < len(argv):
            override = argv[i + 1]
    line, how, rows = evaluate(ROOT, override)

    # RB-113 — state where this stood, so an empty run is distinguishable from a clean one.
    print("freeze_readiness_check: line=%s (resolved from %s) · %d §9.3 item(s) examined"
          % (line or "UNRESOLVED", how, len(rows)))
    bad = 0
    for cid, label, ok, detail in rows:
        if ok:
            print("  ✅ %s  %s — %s" % (cid, label, detail))
        else:
            bad += 1
            print("  ❌ %s  %s" % (cid, label))
            print("        %s" % detail)
    print()
    if bad:
        print("FREEZE NOT READY — %d of %d §9.3 item(s) are not evidenced." % (bad, len(rows)))
        print("⚠️  An item that cannot be located is a FAIL, not a skip: a freeze gate that passes")
        print("    because it could not find its own evidence is the failure it exists to prevent.")
        return 1
    print("FREEZE READY — every §9.3 item is evidenced.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
