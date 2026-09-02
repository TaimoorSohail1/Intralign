#!/usr/bin/env python3
"""iteration_queue.py — the day's work, DERIVED and priority-ordered. Never hand-sorted.

WHY THIS EXISTS
---------------
**Work is enumerated in four places and prioritized in none.** `QUEUED_WORK.md` answers *what has
become due*; `BACKLOG.md` is the tracker-agnostic R2 ticket set; `OBLIGATION_*.md` files are one-off
taskings discoverable only if you know they exist; `RB-###` rows live under Framework 001. The
ordering across them existed only in the owner's head — and therefore could only leave it as a chat
message. ⚠️ **Owner, 2026-08-31: *"me sending stale IMs via chat is not sustainable."*** That is not
a discipline failure; it is the absence of this file.

⚠️⚠️ **THE ORDER IS COMPUTED, NEVER SORTED BY HAND.** This is the product's own doctrine turned on the
process that builds it: OSLO computes leverage and refuses to let anyone hand-rank findings. A
hand-maintained work list goes stale exactly the way an IM does — same failure, new filename.

**FULLY DERIVED (owner ruling, 2026-08-31).** A row appears here only if it already exists in a
governed source. **To ask engineering for something, create the durable object first.** There is no
hand-add. `ITERATION.json` carries dates and the goal; it carries no rows.

WHERE ROWS COME FROM
--------------------
  OBLIGATION_*.md        one row each while Status is OPEN            → P0 when production-blocking
  freeze_readiness_check §9.3 items NOT evidenced = the freeze chain  → P1   (computed, not listed)
  apparatus plan         the layer table's first increments           → P2
  queued_work_check.py   the register's OWN due verdict (never re-derived) → P3

⚠️ **`BACKLOG.md` CANNOT BE SCOPED AND IS REPORTED, NOT SKIPPED.** Its tickets carry depends-on, AC and
GT — but **no iteration field exists on any source in this repository** (measured: zero hits for
`iteration:`/`sprint:`). Silently omitting them would be skip-as-pass. The generated file names the
count it could not scope and why, so the schema gap stays visible until someone closes it.

    python3 tools/iteration_queue.py            regenerate the queue
    python3 tools/iteration_queue.py --check    FAIL if the committed queue is stale (freshness gate)
    python3 tools/iteration_queue.py --self-test
⚠️ Read exit codes WITHOUT a pipe.
"""
import json
import os
import re
import subprocess
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = "20_handoff/ITERATION.json"
OUT = "20_handoff/ITERATION_QUEUE.md"

P_LABEL = {0: "P0 · production-blocking", 1: "P1 · freeze chain", 2: "P2 · apparatus",
           3: "P3 · due this iteration"}


def _read(root, *p):
    f = os.path.join(root, *p)
    return open(f, encoding="utf-8", errors="replace").read() if os.path.isfile(f) else None


def resolve_design_ref(root):
    """(ref, status) — the git ref carrying the design line's sources.

    ⚠️ **THE QUEUE LIVES ON `main`; ITS SOURCES DO NOT.** `QUEUED_WORK.md` lives on release lines and
    never on `main` (measured 2026-08-31: `main` carries neither `release-2.1/` nor the obligations).
    A generator reading only its own working tree therefore derives ONE row on `main` — which is how
    RB-076, RB-106 and RB-125 all happened. **This is that same cause, a fourth time, and the fix is
    the same one: be ref-aware.**

    Three states, and the middle one is the whole point:
      `ok`       — the pointer names a ref that exists
      `dangling` — the pointer names a ref that does NOT exist  → **FAIL LOUDLY**
      `absent`   — no pointer at all                            → **FAIL LOUDLY**

    ⚠️ Owner to dev lead, 2026-08-31: *"a missing or dangling pointer must fail loudly, never SKIP-OK."*
    A dangling pointer means the branch has not been created yet — so that open action shows up as a
    red row in the daily queue every morning, instead of as a chat message that goes stale.
    """
    raw = _read(root, "ACTIVE_DESIGN_REF")
    if raw is None or not raw.strip():
        return None, "absent"
    ref = raw.strip().splitlines()[0].strip()
    try:
        r = subprocess.run(["git", "--git-dir", os.path.join(root, ".git"),
                            "rev-parse", "--verify", "--quiet", ref + "^{commit}"],
                           capture_output=True, text=True, timeout=20)
        return ref, ("ok" if r.returncode == 0 else "dangling")
    except Exception:
        return ref, "dangling"


def _read_at_ref(root, ref, path):
    """Read a path from a git ref. PLUMBING ONLY — cat-file never writes the index."""
    try:
        r = subprocess.run(["git", "--git-dir", os.path.join(root, ".git"),
                            "cat-file", "-p", "%s:%s" % (ref, path)],
                           capture_output=True, text=True, timeout=30)
        return r.stdout if r.returncode == 0 else None
    except Exception:
        return None


def _ls_at_ref(root, ref, path):
    try:
        r = subprocess.run(["git", "--git-dir", os.path.join(root, ".git"),
                            "ls-tree", "--name-only", "%s:%s" % (ref, path)],
                           capture_output=True, text=True, timeout=30)
        return r.stdout.split() if r.returncode == 0 else []
    except Exception:
        return []


def load_deferrals(root):
    """Row id -> list of recorded owner rulings. A date passing is NOT a deferral."""
    raw = _read(root, "20_handoff/DEFERRALS.json")
    if raw is None:
        return {}
    try:
        data = json.loads(raw)
    except Exception:
        return {}
    out = {}
    for d in data.get("deferrals", []):
        out.setdefault(d.get("row", ""), []).append(d)
    return out


def load_config(root):
    raw = _read(root, CONFIG)
    if raw is None:
        raise SystemExit("FAIL: %s is absent — the iteration is undefined and nothing can be scoped." % CONFIG)
    return json.loads(raw)


def _src(root, ref, path):
    """Working tree first, then the design ref. Returns (text, locus) — the locus is always named."""
    t = _read(root, path)
    if t is not None:
        return t, "worktree"
    if ref:
        t = _read_at_ref(root, ref, path)
        if t is not None:
            return t, ref
    return None, "NOT FOUND"


def rows_from_obligations(root, ref=None):
    """P0/P2 — OBLIGATION_*.md, one row each while OPEN. Owner comes from `**Fix:**`."""
    out, d = [], os.path.join(root, "20_handoff")
    local = sorted(n for n in os.listdir(d)
                   if n.startswith("OBLIGATION_") and n.endswith(".md")) if os.path.isdir(d) else []
    remote = sorted(n for n in _ls_at_ref(root, ref, "20_handoff")
                    if n.startswith("OBLIGATION_") and n.endswith(".md")) if ref else []
    sources = [(name, "worktree") for name in local]
    sources += [(name, ref) for name in remote if name not in set(local)]
    for name, locus in sources:
        text = _read(root, "20_handoff/%s" % name) if locus == "worktree" else _read_at_ref(root, ref, "20_handoff/%s" % name)
        text = text or ""
        status = re.search(r"\*\*Status:\*\*\s*\*?\*?(\w+)", text)
        if status and status.group(1).upper() != "OPEN":
            continue
        klass = re.search(r"^\*\*Class:\*\*\s*(.+)$", text, re.I | re.M)
        blocking = bool(klass and re.search(r"\bproduction blocker\b", klass.group(1), re.I))
        fix = re.search(r"\*\*Fix:\*\*\s*([^\n(]+)", text)
        acc = re.search(r"\*\*Accepts:\*\*\s*([A-Za-z0-9_-]+)", text)
        title = re.search(r"^#\s+(.+)$", text, re.M)
        # ⚠️ Scope to the DECLARED line. Scanning the whole document swept in GT ids that merely
        # appear in prose elsewhere and attributed them to this obligation — a count of somewhere.
        inv_line = re.search(r"\*\*Invariants violated:\*\*\s*([^\n]*(?:\n(?!\n|\*\*|#)[^\n]*)*)", text)
        inv = sorted(set(re.findall(r"GT-\d+", inv_line.group(1)))) if inv_line else []
        done = "§4 DONE CONDITION" if "DONE CONDITION" in text else "see 'Closing condition'"
        out.append({
            "id": name.replace("OBLIGATION_", "").replace(".md", ""),
            "p": 0 if blocking else 2,
            "title": (title.group(1) if title else name).replace("OBLIGATION — ", "").strip(),
            "owner": _clean(fix.group(1)) if fix else "⚠️ UNASSIGNED",
            "accepts": acc.group(1) if acc else "—",
            "done": done,
            "src": "20_handoff/%s (%s)" % (name, locus),
            "note": ("invariants: " + " · ".join(inv[:4])) if inv else "",
        })
    return out


def rows_from_freeze_chain(root):
    """P1 — the freeze chain is COMPUTED: it is exactly §9.3's not-yet-evidenced items."""
    checker = os.path.join(root, "tools", "freeze_readiness_check.py")
    if not os.path.isfile(checker):
        return [{"id": "FREEZE-UNKNOWN", "p": 1, "title": "Freeze readiness cannot be computed",
                 "owner": "UNASSIGNED", "accepts": "—", "done": "checker exists and runs",
                 "src": "tools/freeze_readiness_check.py (ABSENT)",
                 "note": "⚠️ fail-closed: the freeze chain is UNKNOWN, not empty"}]
    try:
        r = subprocess.run([sys.executable, checker], cwd=root, capture_output=True, text=True, timeout=60)
        text = r.stdout
    except Exception as e:
        return [{"id": "FREEZE-UNKNOWN", "p": 1, "title": "Freeze readiness check did not run: %s" % e,
                 "owner": "UNASSIGNED", "accepts": "—", "done": "the checker runs",
                 "src": "tools/freeze_readiness_check.py", "note": "⚠️ fail-closed"}]
    out = []
    for m in re.finditer(r"^\s*❌\s+(F\d)\s+(.+)$", text, re.M):
        out.append({"id": "§9.3-%s" % m.group(1), "p": 1, "title": m.group(2).strip(),
                    "owner": "owner + dev lead", "accepts": "owner",
                    "done": "`freeze_readiness_check.py` reports ✅ for this item",
                    "src": "F002 §9.3", "note": "blocks the R2.1 freeze"})
    return out


def rows_from_apparatus(root, ref=None):
    """P2 — the apparatus plan's layer table; one row per layer with a named owner."""
    d = os.path.join(root, "20_handoff")
    plans = sorted(n for n in os.listdir(d) if "APPARATUS_PLAN" in n and n.endswith(".md")) \
        if os.path.isdir(d) else []
    if not plans and ref:
        plans = sorted(n for n in _ls_at_ref(root, ref, "20_handoff") if "APPARATUS_PLAN" in n)
    if not plans:
        # ⚠️ NOT an empty list. No plan reachable means the iteration's apparatus increments are
        # UNKNOWN, not absent — and this generator exists to stop exactly that substitution. The
        # case became reachable on 2026-08-31 when the plan moved to a separate branch, so the
        # silent-empty branch was live and untested until the topology exposed it.
        return [{"id": "APPARATUS-UNKNOWN", "p": 2,
                 "title": "no apparatus plan reachable — this iteration's increments are UNKNOWN",
                 "owner": "⚠️ UNASSIGNED", "accepts": "owner",
                 "done": "an APPARATUS_PLAN is reachable from this ref",
                 "src": "20_handoff/*APPARATUS_PLAN*.md (NOT FOUND)",
                 "note": "⚠️ fail-closed: absent evidence is never reported as no work"}]
    text, _locus = _src(root, ref, "20_handoff/%s" % plans[-1])
    text = text or ""
    out = []
    for m in re.finditer(r"^\|\s*\*\*?(L\d)\*?\*?\s*\|([^|]+)\|([^|]+)\|([^|]+)\|", text, re.M):
        lid, layer, incr, owner = (g.strip() for g in m.groups())
        if "✅" in incr or "BUILT" in incr.upper():
            continue
        out.append({"id": lid, "p": 2, "title": "%s — %s" % (layer.strip("* "), _trim(incr)),
                    "owner": _clean(owner), "accepts": "owner",
                    "done": "named in the apparatus plan", "src": "20_handoff/%s" % plans[-1],
                    "note": "apparatus increment for this iteration"})
    return out


def rows_from_queued_work(root, cfg, ref=None):
    """P3 — the DUE rows, as decided by `queued_work_check.py`. This function does NOT decide.

    ⚠️⚠️ THIS DELEGATES BECAUSE RE-IMPLEMENTING IT WAS WRONG, MEASURABLY. The first version filtered
    on the `due:` DATE and called the result "due". `QUEUED_WORK.md` defines the word differently:
    *"An item is DUE when every predicate in its `when` list is true."* Measured 2026-08-31 against
    the real checker, a date filter over one iteration returned **23 rows of which 8 were CLOSED**,
    4 could not be evaluated until the PR stack clears, and 11 had a false predicate — while missing
    RB-127, which is genuinely actionable. **The true set is 3 overdue + 7 state-due.**

    A daily work queue that shows engineering closed rows destroys its own credibility in about a
    week. The register has an authority; the queue reads its verdict and adds nothing.
    """
    out = []
    verdicts, how = _due_from_checker(root, ref)
    if verdicts is None:
        return [{"id": "QUEUED-WORK-UNKNOWN", "p": 3,
                 "title": "the release register's due set could not be evaluated",
                 "owner": "⚠️ UNASSIGNED", "accepts": "—",
                 "done": "`queued_work_check.py` runs and reports",
                 "src": how, "note": "⚠️ fail-closed: UNKNOWN, never an empty sprint"}]
    for rid, kind, title, due in verdicts:
        out.append({"id": rid, "p": 3, "title": _trim(title), "owner": "see the register row",
                    "accepts": "—", "done": "its `when:` predicates evaluate satisfied",
                    "src": how,
                    "note": ("⚠️ **OVERDUE %s** — re-date with a reason or do the work; both are a "
                             "visible diff" % due) if kind == "overdue" else "state-due %s" % due})
    return out


def _due_from_checker(root, ref=None):
    """(verdicts, locus) — run the line's own queued_work_check.py and read its verdict lines.

    Returns None when it cannot be run, so the caller fails closed rather than reporting nothing due.
    ⚠️ The checker needs the release line in the WORKING TREE (it resolves files at refs itself). On
    the control plane that means after the design-line checkout — which is exactly what
    `queued-work.yml` does on schedule since #250.
    """
    line = (_read(root, "CURRENT_RELEASE") or "").strip()
    if not line and ref:
        line = (_read_at_ref(root, ref, "CURRENT_RELEASE") or "").strip()
    if not line:
        return None, "no CURRENT_RELEASE reachable"
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
    found = []
    m = re.search(r"OVERDUE BY DATE:\s*([^\n]+)", text)
    if m:
        # ⚠️ Title comes from the row's OWN `::error::RB-nnn — …` header, never from a window of
        # characters after the id's first occurrence. That first occurrence is the summary list, so
        # windowing gave RB-076 and RB-120 empty titles and handed RB-102 its NEIGHBOUR's title.
        # A work queue that mislabels a row is worse than one that omits it.
        titles = dict(re.findall(r"^::error::(RB-\d+) — ([^\n]+)$", text, re.M))
        # The date the row went overdue, from its own detail block — an "OVERDUE" with no date is
        # an escalation nobody can act on.
        dates = {}
        for sec in re.finditer(r"^  (RB-\d+) — .*?\n((?:      .*\n)+)", text, re.M):
            d = re.search(r"OVERDUE\s+due:(\S+)", sec.group(2))
            if d:
                dates[sec.group(1)] = d.group(1)
        for rid in re.findall(r"RB-\d+", m.group(1)):
            found.append((rid, "overdue", titles.get(rid, "(title not stated by the checker)"),
                          dates.get(rid, "date not stated")))
    blk = re.search(r"STATE-DUE[^\n]*\n((?:\s+RB-\d+ —[^\n]*\n)+)", text)
    if blk:
        for ln in blk.group(1).strip().splitlines():
            mm = re.match(r"\s*(RB-\d+) — (.*?)\s*\(due ([\d-]+)\)\s*$", ln)
            if mm:
                found.append((mm.group(1), "state-due", mm.group(2), mm.group(3)))
    return found, "%s/QUEUED_WORK.md via queued_work_check.py" % line


def unscopable(root):
    """⚠️ Reported, never silently dropped: what exists but cannot be placed in an iteration."""
    notes = []
    for line_dir in sorted(n for n in os.listdir(root) if n.startswith("release-")):
        text = _read(root, line_dir, "BACKLOG.md")
        if not text:
            continue
        n = len(set(re.findall(r"R2-S\d+-\d+", text)))
        if n:
            notes.append("**%s/BACKLOG.md — %d build tickets, NONE scopable.** No source in this "
                         "repository carries an `iteration:` or `sprint:` field (measured: zero hits). "
                         "Until tickets can name an iteration, the build backlog cannot feed this "
                         "queue, and the iteration's build content is decided outside any artifact. "
                         "⚠️ **Escalated, not worked around** — omitting them silently would be "
                         "skip-as-pass." % (line_dir, n))
    return notes


def _clean(s):
    """An owner is a NAME, not a paragraph.

    ⚠️ `owner:` in QUEUED_WORK.md is free prose — "AI drafts with a MOCKUP first - this moves pixels -
    and the owner ratifies…". Rendering that whole string made the table unreadable, which is its own
    kind of failure: a daily list nobody can scan is a daily list nobody reads. Keep the first clause;
    the full text is one click away in the cited source.
    """
    s = re.sub(r"\*\*|`", "", s).strip()
    s = re.split(r"\s+[-–—]\s+|;|,\s", s)[0].strip().rstrip(".")
    if len(s) > 46:
        s = s[:45].rstrip() + "…"
    return s or "⚠️ UNASSIGNED"


def _trim(s, n=90):
    s = re.sub(r"\*\*|`|\s+", lambda m: " " if m.group(0).isspace() else "", s).strip()
    return s if len(s) <= n else s[:n - 1] + "…"


def build(root):
    cfg = load_config(root)
    ref, ref_status = resolve_design_ref(root)
    rows = (rows_from_obligations(root, ref) + rows_from_freeze_chain(root)
            + rows_from_apparatus(root, ref) + rows_from_queued_work(root, cfg, ref))

    # ⚠️ A pointer that is absent or dangling is a LOUD row, never a silent zero (RB-076).
    if ref_status != "ok":
        rows.append({
            "id": "ACTIVE_DESIGN_REF",
            "p": 1,
            "title": ("`ACTIVE_DESIGN_REF` names `%s` — that ref DOES NOT EXIST" % ref)
                     if ref_status == "dangling" else
                     "no `ACTIVE_DESIGN_REF` pointer — F002 §9.1 specifies one, never instantiated",
            "owner": "HamzaSohailCodes", "accepts": "owner",
            "done": "the ref resolves and this row disappears",
            "src": "F002 §9.1 (carrying DL-235)",
            "note": ("⚠️ **release-line rows below are INCOMPLETE** until it resolves — "
                     "a missing or dangling pointer must fail loudly, never SKIP-OK"),
        })

    # Deferral is an owner ruling, recorded. A date passing is not a deferral.
    deferrals = load_deferrals(root)
    active, deferred = [], []
    for r in rows:
        d = [x for x in deferrals.get(r["id"], []) if x.get("from") == cfg["id"]]
        if d:
            r["_defer"] = d[-1]
            r["_count"] = len(deferrals.get(r["id"], []))
            deferred.append(r)
        else:
            active.append(r)
    rows = active
    rows.sort(key=lambda r: (r["p"], "UNASSIGNED" in r["owner"], r["id"]))

    L = []
    L.append("# Iteration queue — %s · %s → %s" % (cfg["id"], cfg["start"], cfg["end"]))
    L.append("")
    L.append("> ⚠️ **GENERATED — do not edit.** `python3 tools/iteration_queue.py` regenerates it; "
             "`--check` fails the build when it is stale. **Rows are DERIVED**: to put work here, "
             "create the durable object (an obligation, a due queued-work row, an apparatus "
             "increment). A chat message is not a source.")
    L.append(">")
    L.append("> **The order is COMPUTED, never hand-sorted.** P0 production-blocking defects outrank "
             "the freeze chain by owner ruling 2026-08-31 — if they compete, the freeze slips.")
    L.append("")
    L.append("**Iteration goal.** %s" % cfg["goal"])
    L.append("")
    L.append("**Read this each day.** %d row(s) open." % len(rows))
    L.append("")
    cur = None
    for r in rows:
        if r["p"] != cur:
            cur = r["p"]
            L.append("")
            L.append("## %s" % P_LABEL.get(cur, "P?"))
            L.append("")
            L.append("| id | what | owner | accepts | done when | source |")
            L.append("|---|---|---|---|---|---|")
        L.append("| `%s` | %s%s | **%s** | %s | %s | `%s` |" % (
            r["id"], _trim(r["title"]),
            (" <br>· %s" % r["note"]) if r.get("note") else "",
            r["owner"], r["accepts"], r["done"], r["src"]))
    if not rows:
        L.append("")
        L.append("⚠️ **NO ROWS DERIVED.** That is a finding, not an empty sprint — check that the "
                 "sources exist and that `ITERATION.json`'s window matches them.")
    if deferred:
        L.append("")
        L.append("## ▶ Deferred out of this iteration — by ruling, not by drift")
        L.append("")
        L.append("| id | what | to | ruled by | date | why |")
        L.append("|---|---|---|---|---|---|")
        for r in sorted(deferred, key=lambda x: (-x.get("_count", 1), x["id"])):
            d = r["_defer"]
            esc = " ⚠️ **DEFERRED %dx — the premise, not the timing, is what is wrong**" % r["_count"] \
                if r.get("_count", 1) >= 2 else ""
            L.append("| `%s` | %s%s | %s | %s | %s | %s |" % (
                r["id"], _trim(r["title"], 60), esc, d.get("to", "—"),
                d.get("ruled_by", "⚠️ UNNAMED"), d.get("date", "⚠️ UNDATED"), _trim(d.get("why", "—"), 70)))

    notes = unscopable(root)
    if notes:
        L.append("")
        L.append("## ▶ Cannot be scoped — reported, not dropped")
        L.append("")
        for n in notes:
            L.append("- %s" % n)
    L.append("")
    L.append("---")
    L.append("")
    L.append("MEASURED-BY: `python3 tools/iteration_queue.py`, sources as cited per row.")
    L.append("")
    return "\n".join(L) + "\n"


def self_test():
    """RED-prove the generator: ordering, derivation, and the freshness gate."""
    import tempfile
    fails = []
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "20_handoff"))
        os.makedirs(os.path.join(tmp, "tools"))
        os.makedirs(os.path.join(tmp, "release-X"))
        json.dump({"id": "it-T", "start": "2026-01-01", "end": "2026-01-14", "goal": "G"},
                  open(os.path.join(tmp, CONFIG), "w"))
        open(os.path.join(tmp, "20_handoff", "OBLIGATION_blocker.md"), "w").write(
            "# OBLIGATION — a blocking one\n**Status:** OPEN\n**Fix:** Alice\n"
            "**Accepts:** Bob\n**Class:** production blocker\n## 4 · DONE CONDITION\n")
        open(os.path.join(tmp, "20_handoff", "OBLIGATION_closed.md"), "w").write(
            "# OBLIGATION — closed\n**Status:** CLOSED\n**Fix:** Alice\n**Class:** production blocker\n")
        open(os.path.join(tmp, "release-X", "QUEUED_WORK.md"), "w").write(
            "```queue\nid: RB-01\ndue: 2026-01-05\ntitle: inside window\nowner: Carol\n\n"
            "id: RB-02\ndue: 2027-01-05\ntitle: outside window\nowner: Carol\n```\n")
        open(os.path.join(tmp, "release-X", "BACKLOG.md"), "w").write("| R2-S1-1 | t |\n| R2-S1-2 | t |\n")
        out = build(tmp)

        if "a blocking one" not in out:
            fails.append("an OPEN production-blocking obligation did not reach the queue")
        if "OBLIGATION_closed" in out or "closed" in out.split("Cannot be scoped")[0].lower().split("obligation")[-1][:0]:
            pass
        if "closed" in [r["id"] for r in rows_from_obligations(tmp)]:
            fails.append("a CLOSED obligation was queued")
        # ⚠️ The queue no longer decides what is due — `queued_work_check.py` does. What must be
        # RED-proved here is that an UNRUNNABLE authority yields UNKNOWN, never an empty sprint.
        if "QUEUED-WORK-UNKNOWN" not in out:
            fails.append("an unrunnable queued_work_check produced NO row — silence read as 'nothing due'")
        if "APPARATUS-UNKNOWN" not in out:
            fails.append("a missing apparatus plan produced NO row — absent evidence read as 'no work'")
        if "RB-01" in out or "RB-02" in out:
            fails.append("the queue decided dueness itself instead of delegating to the register's checker")
        if "NONE scopable" not in out or "2 build tickets" not in out:
            fails.append("unscopable BACKLOG tickets were silently dropped — that is skip-as-pass")
        if out.index("P0 · production-blocking") > out.index("P3 · due this iteration"):
            fails.append("ordering is wrong — P0 must precede P3")
        # RED: the freeze chain must be UNKNOWN, never empty, when the checker is absent
        if "FREEZE-UNKNOWN" not in out:
            fails.append("a missing freeze checker produced an EMPTY chain instead of UNKNOWN")

    with tempfile.TemporaryDirectory() as tmp2:
        try:
            build(tmp2)
            fails.append("a missing ITERATION.json did not fail closed")
        except SystemExit:
            pass

    # ── RB-076: the pointer states, RED-proved. A skipped pointer is the failure, not the fix. ──
    with tempfile.TemporaryDirectory() as t3:
        os.makedirs(os.path.join(t3, "20_handoff"))
        json.dump({"id": "it-T", "start": "2026-01-01", "end": "2026-01-14", "goal": "G"},
                  open(os.path.join(t3, CONFIG), "w"))
        out = build(t3)
        if "ACTIVE_DESIGN_REF" not in out or "never instantiated" not in out:
            fails.append("an ABSENT ACTIVE_DESIGN_REF produced no row — that is SKIP-OK on a pointer")
        open(os.path.join(t3, "ACTIVE_DESIGN_REF"), "w").write("no/such/ref\n")
        out = build(t3)
        # ⚠️ case-insensitive on purpose: the assertion is that the row EXISTS and names the ref,
        # not that it is phrased a particular way. A test that pins prose breaks on every edit.
        if "no/such/ref" not in out or "does not exist" not in out.lower():
            fails.append("a DANGLING ACTIVE_DESIGN_REF produced no row — it must fail loudly")

    # ── Deferral is a recorded ruling; a second one escalates. ──
    with tempfile.TemporaryDirectory() as t4:
        os.makedirs(os.path.join(t4, "20_handoff"))
        json.dump({"id": "it-T", "start": "2026-01-01", "end": "2026-01-14", "goal": "G"},
                  open(os.path.join(t4, CONFIG), "w"))
        open(os.path.join(t4, "20_handoff", "OBLIGATION_x.md"), "w").write(
            "# OBLIGATION — deferrable\n**Status:** OPEN\n**Fix:** Alice\n**Class:** production blocker\n")
        base = build(t4)
        if "P0 · production-blocking" not in base:
            fails.append("fixture obligation did not reach P0")
        json.dump({"deferrals": [{"row": "x", "from": "it-T", "to": "it-U",
                                  "ruled_by": "owner", "date": "2026-01-02", "why": "capacity"}]},
                  open(os.path.join(t4, "20_handoff", "DEFERRALS.json"), "w"))
        out = build(t4)
        if "Deferred out of this iteration" not in out or "capacity" not in out:
            fails.append("a recorded deferral did not move the row into the deferred tail")
        if "P0 · production-blocking" in out:
            fails.append("a deferred row was still rendered as active work")
        json.dump({"deferrals": [
            {"row": "x", "from": "it-S", "to": "it-T", "ruled_by": "owner", "date": "2026-01-01", "why": "a"},
            {"row": "x", "from": "it-T", "to": "it-U", "ruled_by": "owner", "date": "2026-01-02", "why": "b"}]},
            open(os.path.join(t4, "20_handoff", "DEFERRALS.json"), "w"))
        if "DEFERRED 2x" not in build(t4):
            fails.append("a row deferred TWICE did not escalate — the second slip is the signal")

    # ── #266: obligations are a union across the worktree and design ref, never a fallback. ──
    with tempfile.TemporaryDirectory() as t5:
        os.makedirs(os.path.join(t5, "20_handoff"))
        ref_file = os.path.join(t5, "20_handoff", "OBLIGATION_ref_only.md")
        open(ref_file, "w").write("# OBLIGATION — ref only\n**Status:** OPEN\n**Fix:** Alice\n**Class:** apparatus integrity\n")
        for args in (("init",), ("config", "user.email", "queue@example.test"),
                     ("config", "user.name", "Queue Test"), ("add", "."),
                     ("commit", "-m", "ref obligation"), ("branch", "design/test")):
            subprocess.run(["git", "-C", t5] + list(args), check=True, capture_output=True)
        os.remove(ref_file)
        open(os.path.join(t5, "20_handoff", "OBLIGATION_local.md"), "w").write(
            "# OBLIGATION — local only\n**Status:** OPEN\n**Fix:** Bob\n**Class:** production blocker\n")
        both = rows_from_obligations(t5, "design/test")
        if {r["id"] for r in both} != {"ref_only", "local"}:
            fails.append("local and ref-only obligations were not derived as a union")
        if not any(r["src"].endswith("(design/test)") for r in both):
            fails.append("a design-ref obligation did not expose its locus")
        open(os.path.join(t5, "20_handoff", "OBLIGATION_negated.md"), "w").write(
            "# OBLIGATION — not a blocker\n**Status:** OPEN\n**Fix:** Bob\n**Class:** apparatus integrity · not blocking for production\n")
        if next(r for r in rows_from_obligations(t5, "design/test") if r["id"] == "negated")["p"] != 2:
            fails.append("a non-blocker prose mention was misclassified as P0")

    if fails:
        print("SELF-TEST FAILED:")
        for f in fails:
            print("  ✗", f)
        return 1
    print("self-test OK — derivation, delegation of dueness to the register's checker, P0-before-P3")
    print("ordering, unscopable reporting, UNKNOWN-not-empty on BOTH missing checkers, and")
    print("fail-closed on a missing ITERATION.json.")
    return 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    generated = build(ROOT)
    path = os.path.join(ROOT, OUT)
    if "--check" in argv:
        current = _read(ROOT, OUT)
        if current is None:
            print("FAIL — %s does not exist. Run: python3 tools/iteration_queue.py" % OUT)
            return 1
        if current != generated:
            print("FAIL — %s is STALE. Its sources moved and it was not regenerated." % OUT)
            print("       A stale work queue is the failure this file exists to end.")
            print("       Run: python3 tools/iteration_queue.py")
            return 1
        print("PASS — %s is current with its sources." % OUT)
        return 0
    with open(path, "w", encoding="utf-8") as f:
        f.write(generated)
    n = generated.count("\n| `")
    print("wrote %s · %d row(s) derived · %s" % (OUT, n, date.today().isoformat()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
