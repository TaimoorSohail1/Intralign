# OBLIGATION — R2.0 · B0 · Findings must keep their identity across re-analyses

**Zone:** `20_handoff/` — co-governed. **Engineering authors the fix; the owner accepts it.**
**Fix:** TaimoorSohail1 (author of `issue_identity.py`, owner of #248).
**Accepts:** HamzaSohailCodes, against §4 below. ⚠️ **Author does not accept their own work** — that
separation is the point of ruling 4, and the absence of it is how the constructed-to-pass test shipped.

**Status:** OPEN · raised 2026-08-31 · **blocking for production.**
**Closes when §4 is satisfied. Nothing else closes it.**

**Origin:** `20_handoff/audits/BUILD_READINESS_AUDIT_2026-08-29_R2.0_STAGING.md` §B0–B3.
**Invariants violated:** GT-10 (only reanalysis resolves) · GT-35 (only verify moves Grounding) ·
GT-67 (settled never regresses on landing).

---

## 1 · What is wrong

**A finding's identity is a hash of the model's own prose.**

MEASURED-BY: `git show origin/codex/r2-uat-remediation:code/services/api/src/oslo_api/analysis/issue_identity.py`,
2026-08-31.

```python
# issue_identity.py:135-142, 225-230
def _tokens(issue):
    text = f"{issue.title} {issue.why}".casefold()
    return {t.rstrip("s") for t in re.findall(r"[a-z0-9]+", text)
            if len(t) > 2 and t not in _STOP_WORDS}

def _deterministic_id(issue):
    normalized = " ".join(sorted(_tokens(issue)))
    digest = hashlib.sha256(f"{issue.artifact_type.value}|{normalized}".encode()).hexdigest()[:12].upper()
    return f"ISS-{issue.artifact_type.value.upper()}-{digest}"
```

**Nothing in that identity names the plan element the finding is about.** Reword the sentence and it
becomes a different finding.

**Identity is not carried across runs — it is re-guessed.** At `AnalysisPhase.PUBLISH`
(`workflow.py:306-320`), `stabilize_issue_ids` re-matches by token overlap: **+0.15 for shared
evidence refs, same `artifact_type` only, threshold `>= 0.38`** (`issue_identity.py:119-132`). Below
threshold, a new id is minted and the previous finding drops out of the set.

**When identity is lost, the user's attestation is orphaned.** `Attestation` is keyed `issue_id`
(`issue_lifecycle.py:52-59`), persisted as `"issue_stable_key": issue.id` (`persistence.py:1602`) —
the content hash itself, with no separate durable key. Reads join
`issue.stable_key = attestation.issue_stable_key` (`service.py:882`). When the hash changes, that
join finds nothing. **The record survives; the live read cannot see it.**

⚠️ **`_best_match` requires identical `artifact_type`**, so a finding that moves artifact between runs
loses identity **unconditionally**, however identically worded.

---

## 2 · What it costs, measured

MEASURED-BY: live staging session on `DevNorth 2026`, plan documents never edited, 2026-08-29/31.

| observed | mechanism |
|---|---|
| A **settled** finding returned as **open at rank #1**, reworded — *"No venue dependency is secured or bounded…"* → *"Venue dependency is unsecured and unbounded"* | rewording fell below 0.38; new id minted; the attestation still points at the old hash |
| Totals churned **24 → 23 → 29** across three runs; the app reported **16 opened / 16 resolved** against three user acts | the set is re-derived, not re-identified |
| Grounding read **1 of 24 → 1 of 23 → 0 of 29 → 2 of 29**; the numerator fell to **0** after two successful attestations | grounding credit attaches to ids that vanished |
| The Executive Briefing told a sponsor **"8 opened · 2 resolved"** on a plan nobody edited | **the defect reaches outside the product** |

---

## 3 · What must become true

**Identity derives from what a finding is ABOUT, not how it was phrased.**

The obligation is the property, not the implementation: an identity that survives rewording, derived
from the **artifact + the plan element + the weakness class**. Engineering chooses the mechanism.

⚠️ **Threshold-tuning does not satisfy this.** Moving `0.38` relocates where identity breaks; it does
not stop it breaking. **The `DET-` branch already in `stabilize_issue_ids` shows deterministic
identity is a first-class concept in this module** — the fix is to extend that path, not to improve
the guess.

⚠️ **A durable attestation key is part of the obligation.** While `issue_stable_key` stores the
content hash, any identity change orphans user work regardless of how good the matcher becomes.

---

## 4 · DONE CONDITION — both halves required

**Neither half alone closes this.** A green unit test does not prove the churn is gone; a clean
staging run does not stop it returning.

### 4a · A RED-proved server twin

A twin asserting the invariant, **demonstrated to fail when it is violated** (ruling 4 · DL-243 §6c).
**Three paths nothing currently covers, all measured as gaps 2026-08-31:**

1. identity **at** the matching threshold
2. identity **below** it — the case that produced every defect in §2
3. an **`artifact_type` mismatch** — where identity is lost unconditionally

⚠️ **Note for whoever writes it:** `test_issue_identity.py` carries **nine** well-formed negative
tests for `deduplicate_issues`, and the **one** test guarding `stabilize_issue_ids` was constructed
so it could not fail — both fixtures share the helper's default `evidence_refs`, handing the matcher
its **+0.15** bonus for free. **Negative coverage elsewhere in the file did not protect the function
carrying the doctrine.**

### 4b · The measured defects no longer reproduce

Re-run §2 against the deployed build:

- a settled finding **stays settled** across re-analyses it was not acted on
- totals do **not** churn on an unedited plan
- the Grounding numerator **never falls** after a successful attestation
- the generated briefing does **not** attribute engine churn to plan change

**Cited per DL-243 §6d** — each result names `MEASURED-BY:` or `NOT-MEASURABLE:`.

---

## 5 · What this closes, and what it does not

**Closes on acceptance:** B1 · B2 · B3, and the mechanism behind **R3** (near-duplicate findings) and
**R6** (churn reported to stakeholders).

**Does NOT close — separate work, do not fold in:**
- **B5** — the first-run progress screen never hands off to a completed read. Unrelated mechanism.
- **R2** — `high` collapsing into `Critical` in `result_contract.py`. A ratified contract; needs an
  owner ruling, not a fix.
- **R1 · R5 · R7** — composite vocabulary and generated-report defects.
- The other **60** GT twins and the **61** unregistered invariants (`GT-58…GT-118`).

---

> **This is an obligation, not a decision record.** It states work and its acceptance condition.
> It carries no ratification and creates no canon. **AI drafted it; the owner tasks it.**
