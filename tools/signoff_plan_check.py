#!/usr/bin/env python3
"""
R2.0 sign-off plan checker.

The plan (20_handoff/R2.0_SIGNOFF_PLAN.md) is an operational record, and a record that nothing
re-derives becomes a status column — a snapshot that reads as a status. This checker asserts the
things a human eye reliably misses:

  C1  ID PARITY   — the plan's subset ids are EXACTLY the subset ids in
                    R2.0_PRODUCTION_ACCEPTANCE_CRITERIA.md §4b. Either drifting is an ERROR.
  C2  VOCABULARY  — every state is one of pass/fail/untested/unclassified. Nothing else is a state.
  C3  VERIFY      — every row names a non-empty re-derivation route. A row that cannot be re-checked
                    is a claim.
  C4  EVIDENCE    — no row may read `pass` with an empty evidence cell.
  C5  TOTALS      — the declared IDS/ROWS/PASS/FAIL/UNTESTED/UNCLASSIFIED equal what the rows
                    actually contain. A hand-edited count may not drift from its own table.
  C6  SCOPE       — §4 may not contain a corpus-debt id (DL-*, RB-*), per the plan's own §1 ruling.
  C7  DEFERRAL    — every §3 `tracking` id has a live row in 20_handoff/DEFERRALS.json. A deferral
                    that nothing carries is a comment; this is what stops D1-D3 being forgotten at
                    the R2.1 boundary. Dropping one turns this gate red.

⚠️ This checker REPORTS the plan's internal integrity. It cannot know whether a row's `verify` route
was actually RUN, or whether its answer is still true on the ref you care about. It is a guard
against silent drift, NOT evidence of product state. Do not read a green here as "R2.0 is fine".

Usage:  python3 tools/signoff_plan_check.py [--self-test]
Exit:   0 = plan is internally consistent · 1 = ERRORs found
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN_REL = "20_handoff/R2.0_SIGNOFF_PLAN.md"
CRIT_REL = "20_handoff/R2.0_PRODUCTION_ACCEPTANCE_CRITERIA.md"
DEFER_REL = "20_handoff/DEFERRALS.json"

STATES = {"pass", "fail", "untested", "unclassified"}
ID_RE = re.compile(r"\b(?:GT-\d{2,3}|N-\d{1,2})\b")
DEBT_RE = re.compile(r"\b(?:DL-\d{3,}|RB-\d{2,})\b")
TOTALS_RE = re.compile(
    r"`IDS=(\d+)`\s*`ROWS=(\d+)`\s*`PASS=(\d+)`\s*`FAIL=(\d+)`"
    r"\s*`UNTESTED=(\d+)`\s*`UNCLASSIFIED=(\d+)`")


def parse_plan(text):
    """Rows of the §4 table -> [{ids, tier, state, evidence, verify}]. Header/rule lines skipped."""
    rows, in_table = [], False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("| ids ") or s.startswith("|ids"):
            in_table = True
            continue
        if in_table:
            if not s.startswith("|"):
                if rows:
                    break
                continue
            if re.match(r"^\|[\s|:-]+\|$", s):
                continue
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) < 5:
                continue
            rows.append({"raw_ids": cells[0], "ids": ID_RE.findall(cells[0]), "tier": cells[1],
                         "state": cells[2].lower(), "evidence": cells[3], "verify": cells[4]})
    return rows


def subset_ids_from_criteria(text):
    """Ids in the §4b gating-subset tables — the section that declares the named subset."""
    start = text.find("Tier 1 — honesty of the read")
    end = text.find("Subset total:")
    if start == -1 or end == -1 or end <= start:
        return None
    ids = set()
    for line in text[start:end].splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        first = s.strip("|").split("|")[0]
        ids.update(ID_RE.findall(first))
    return ids


def tracking_ids(plan_text):
    """Ids in the `tracking` column of the §3 deferral table — the rows that must be carried."""
    start = plan_text.find("## 3.")
    end = plan_text.find("## 4.")
    if start == -1 or end == -1 or end <= start:
        return None
    ids = []
    for line in plan_text[start:end].splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 2 or not re.fullmatch(r"D\d+", cells[0]):
            continue
        m = re.fullmatch(r"RB-\d{2,}", cells[1])
        if m:
            ids.append(cells[1])
        else:
            ids.append("<no tracking id for %s>" % cells[0])
    return ids


def check(plan_text, crit_text, defer_text=None):
    errors = []
    rows = parse_plan(plan_text)
    if not rows:
        return ["[no-rows] the §4 table parsed to zero rows — the plan cannot be checked"]

    plan_ids = [i for r in rows for i in r["ids"]]

    # C1 — id parity against the criteria document
    crit_ids = subset_ids_from_criteria(crit_text)
    if crit_ids is None:
        errors.append("[parity-unavailable] could not locate the §4b subset in the criteria "
                      "document — an unresolvable comparison is a broken check, never a skip")
    else:
        missing = crit_ids - set(plan_ids)
        extra = set(plan_ids) - crit_ids
        for i in sorted(missing):
            errors.append(f"[missing-from-plan] {i} is in the gating subset but not in the plan")
        for i in sorted(extra):
            errors.append(f"[not-in-subset] {i} is in the plan but not in the gating subset")

    for r in rows:
        label = ",".join(r["ids"]) or "<no id>"
        # C2 — vocabulary
        if r["state"] not in STATES:
            errors.append(f"[bad-state] {label} has state '{r['state']}' — "
                          f"not one of {sorted(STATES)}")
        # C3 — every row re-derivable
        if not r["verify"]:
            errors.append(f"[no-verify] {label} names no re-derivation route — it is a claim")
        # C4 — no unevidenced pass
        if r["state"] == "pass" and not r["evidence"]:
            errors.append(f"[unevidenced-pass] {label} reads pass with no evidence")
        # C6 — scope: a corpus-debt id may not appear in the ids column at all
        debt = DEBT_RE.findall(r["raw_ids"])
        if debt:
            errors.append(f"[scope-violation] {', '.join(debt)} is corpus debt — "
                          f"§1 bars it from §4")

    # C5 — declared totals must equal the rows
    m = TOTALS_RE.search(plan_text)
    if not m:
        errors.append("[no-totals] the plan declares no totals line — nothing to reconcile")
    else:
        want = dict(zip(("IDS", "ROWS", "PASS", "FAIL", "UNTESTED", "UNCLASSIFIED"),
                        (int(x) for x in m.groups())))
        got = {"IDS": len(plan_ids), "ROWS": len(rows)}
        for st in ("pass", "fail", "untested", "unclassified"):
            got[st.upper()] = sum(len(r["ids"]) for r in rows if r["state"] == st)
        for k in want:
            if want[k] != got[k]:
                errors.append(f"[totals-drift] declared {k}={want[k]} but the rows contain {got[k]}")

    # C7 — every deferred change is carried by a live deferral row
    if defer_text is not None:
        tracked = tracking_ids(plan_text)
        if tracked is None:
            errors.append("[deferral-unreadable] could not locate the §3 table — an unresolvable "
                          "comparison is a broken check, never a skip")
        elif not tracked:
            errors.append("[no-deferrals] §3 declares no deferred changes — if D1-D3 were dropped, "
                          "say so explicitly rather than deleting the rows")
        else:
            try:
                carried = {r.get("row") for r in json.loads(defer_text).get("deferrals", [])}
            except (ValueError, AttributeError) as e:
                errors.append(f"[deferral-unparsable] {DEFER_REL}: {e}")
                carried = None
            if carried is not None:
                for t in tracked:
                    if t.startswith("<"):
                        errors.append(f"[untracked-deferral] {t} — a deferral with no tracking row "
                                      f"is a comment")
                    elif t not in carried:
                        errors.append(f"[uncarried-deferral] {t} is deferred in §3 but has no row in "
                                      f"{DEFER_REL} — nothing will remember it at the R2.1 boundary")
    return errors


# ---------------------------------------------------------------- self-test
GOOD_PLAN = """
## 3. DEFERRED
| # | tracking | change | RED condition | why deferred |
|---|---|---|---|---|
| D1 | RB-128 | ratchet | fires both ways | saves last week |

## 4. THE SUBSET
| ids | tier | state | evidence | verify |
|---|---|---|---|---|
| GT-10 | 1 | pass | twin registered | run the twin |
| N-1 | 3 | fail | stalls | staging |

`IDS=2` `ROWS=2` `PASS=1` `FAIL=1` `UNTESTED=0` `UNCLASSIFIED=0`
"""
GOOD_DEFER = '{"deferrals":[{"row":"RB-128","from":"iteration-1","to":"iteration-2"}]}'
GOOD_CRIT = """
Tier 1 — honesty of the read
| **GT-10** only reanalysis resolves | spine | ok |
| **N-1** a completed analysis reaches the user | loop | fails |
**Subset total: 2 criteria across 2 rows.**
"""


def self_test():
    """RED-prove every assertion: each mutation must produce the error it targets."""
    P, C, D = GOOD_PLAN, GOOD_CRIT, GOOD_DEFER
    cases = [
        ("C1 missing-from-plan", P.replace("| GT-10 | 1 | pass | twin registered | run the twin |\n", "")
                                  .replace("`IDS=2` `ROWS=2` `PASS=1`", "`IDS=1` `ROWS=1` `PASS=0`"),
         C, D, "missing-from-plan"),
        ("C1 not-in-subset", P.replace("| GT-10 |", "| GT-99 |"), C, D, "not-in-subset"),
        ("C2 bad-state", P.replace("| 3 | fail |", "| 3 | partial |"), C, D, "bad-state"),
        ("C3 no-verify", P.replace("| stalls | staging |", "| stalls |  |"), C, D, "no-verify"),
        ("C4 unevidenced-pass", P.replace("| twin registered |", "|  |"), C, D, "unevidenced-pass"),
        ("C5 totals-drift", P.replace("`PASS=1`", "`PASS=2`"), C, D, "totals-drift"),
        # ⚠️ The fixture id is deliberately RB-999 (already this repo's reserved test id), NOT a real
        # DL id. An earlier cut used one, and `dl_records` duly recorded THIS FILE as its citer — a
        # document describing a citation defect is a canonical surface like any other.
        ("C6 scope-violation", P.replace("| GT-10 |", "| RB-999 |"), C, D, "scope-violation"),
        ("C7 uncarried-deferral", P, C, '{"deferrals":[]}', "uncarried-deferral"),
        ("C7 untracked-deferral", P.replace("| D1 | RB-128 |", "| D1 | later |"), C, D,
         "untracked-deferral"),
        ("C7 dropped-rows", P.replace("| D1 | RB-128 | ratchet | fires both ways | saves last week |\n", ""),
         C, D, "no-deferrals"),
    ]
    ok = True
    base = check(P, C, D)
    if base:
        print("  self-test FAIL — the clean fixture must produce no errors, got:")
        for e in base:
            print("     " + e)
        ok = False
    else:
        print("  GREEN  clean fixture -> 0 errors")
    for name, plan, crit, defer, token in cases:
        if (plan, defer) == (P, D):
            print(f"  FAIL   {name} -> the mutation changed nothing; an unfired mutation "
                  f"looks like a robust system")
            ok = False
            continue
        errs = check(plan, crit, defer)
        hit = any(token in e for e in errs)
        print(f"  {'RED   ' if hit else 'FAIL  '} {name} -> {'fires' if hit else 'DID NOT FIRE'}")
        ok = ok and hit
    return ok


def main():
    if "--self-test" in sys.argv:
        print("signoff_plan_check --self-test")
        sys.exit(0 if self_test() else 1)

    plan_p, crit_p, defer_p = ROOT / PLAN_REL, ROOT / CRIT_REL, ROOT / DEFER_REL
    for p, rel in ((plan_p, PLAN_REL), (crit_p, CRIT_REL), (defer_p, DEFER_REL)):
        if not p.exists():
            print(f"::error::missing {rel} — an absent subject is a broken check, never a skip")
            sys.exit(1)

    errors = check(plan_p.read_text(encoding="utf-8"), crit_p.read_text(encoding="utf-8"),
                   defer_p.read_text(encoding="utf-8"))
    print(f"R2.0 sign-off plan: {len(errors)} error(s)\n")
    for e in errors:
        print("ERROR  " + e)
    print("\n⚠️  This checks the plan's INTERNAL consistency only. It does not know whether any "
          "`verify` route was run, or whether its answer still holds on your ref.")
    print(f"\n{'FAIL' if errors else 'PASS'}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
