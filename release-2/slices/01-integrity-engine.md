# R2 Slice 1 — Outcome-Integrity Engine — Build Design

*Grill artifact · authored 2026-08-06 · derived from ratified DL-193/194/195/196/197 + the 2026-08-06 owner constraints. Status: **DRAFT — awaiting slice sign-off.** This specifies the REAL three-pillar engine and flags where `oslo-prototype-r2.html` is a fixture-bound approximation to be replaced.*

**Scope:** the three-pillar Outcome-Integrity engine (Viability × Grounding × Adaptability), moment-in-time (State 1), computed entirely from the exposure-gated issue layer. This is Slice 1 of the R2 delta and the foundation every read renders from (State-1 Phase A).

**Two prototype-vs-canon discrepancies this design corrects (flagged for you):**
1. The prototype ships a **4-step** band scale (`Very Low · Low · Moderate · Sound`); DL-195 §6 ratifies a **5-step Fragile→Sound**.
2. The prototype's weakest-gates tie-break is **Grounding-first** (`_gate()` = `{grd:0,via:1,ada:2}`); canon is **foundation-first Viability→Grounding→Adaptability** (DL-195 §6). This is a small prototype deviation from canon that should also be corrected in the prototype.

**Doctrine anchor (DL-193 §1):** Outcome integrity = CAF (clear · coherent · feasible) × Grounding (real/evidenced) × Adaptability (steerable) on the outcome-bearing path. Maturity, never a health/success forecast (D003/D183b).

---

## 1. Locked decisions

| # | Decision | Tag / Source |
|---|---|---|
| L1 | Integrity is a **three-pillar model**: Viability (CAF is the computation *under* it), Grounding (own axis), Adaptability (new peer axis). Not a 4th CAF dimension. | ratified-DL · DL-195 §1, §6 |
| L2 | Composition = **weakest-gates `min(Viability, Grounding, Adaptability)`**; the indicator **names** the limiting pillar; decomposition always recoverable. Never a weighted blend, never a 0–100 number. | ratified-DL · DL-195 §2; DL-194 §3 |
| L3 | Weakest-gates **tie-break = foundation-first `Viability → Grounding → Adaptability`**. | ratified-DL · DL-195 §6 |
| L4 | **State 1 (moment-in-time outcome integrity) is committed R2 scope**; always-visible "ongoing pending" marker; live tracking is State 2 (post-R2). | ratified-DL · DL-194 status, §4 |
| L5 | **Adaptability v1 = checkpoint COVERAGE** (presence of outcome-checkpoints across workstreams) — ordinal maturity: "does the plan have checkpoints to adapt." Full DL-195 steerability (runway-weighted, lever-linked) deferred. | Locked · owner 2026-08-06; DL-195 §3 |
| L6 | **All three pillars resolve through one exposure-gated issue layer**; issue shape `{dim, dims, ftype, sec, sev, status}`; one lifecycle, one queue ranked by outcome-exposure. | ratified-DL · DL-196 §1–2 |
| L7 | **Grounding false-confidence issues** `ISS-FC-<art>`, computed one-door; resolving = attesting the artifact. | ratified-DL · DL-197 §1–3 |
| L8 | **Band endpoints = Fragile → Sound**, five-step, commensurable across all three pillars. Maturity framing, never RAG. | ratified-DL · DL-195 §6; build plan §2b |
| L9 | **Bands normalize to plan size** — grounded ÷ load-bearing, coverage ÷ needed, sound ÷ load-bearing artifacts — never absolute counts. | Locked · owner 2026-08-06 |
| L10 | **Viability moves from real per-issue weakness reduction, never a fix count.** Retire the prototype's `_fixedCount()>=2 → +1` bump. | Locked · owner 2026-08-06 |
| L11 | **A flag credits Grounding at the item level but NEVER firms Viability** — a named gap keeps the linked statement weak. | Locked · owner 2026-08-06 |
| L12 | **Care-point filter:** `dim:'Adaptability'` / `dim:'Grounding'` issues feed their own pillar + the exposure queue ONLY; never `_cafOf` / CAF rows / Attention heat map. | ratified-DL · DL-196 §5; DL-197 §5 |
| L13 | Reanalysis is **event-driven only**; only reanalysis changes the assessment; last-good preserved on failure. | Locked · canonical-truth §6.3/6.4 |

---

## 2. Data / object model
*(Product/data concepts only — no storage technology.)*

**`Issue`** — the single resolution unit for all three pillars (DL-196 §1).
- `id` · `dim` (`Clarity | Alignment | Feasibility` → Viability `| Adaptability | Grounding`) · `dims[]` (pillar set) · `ftype` (`No deadline`, `Unowned`, `Single point of failure`, `Inference gap`, `Coverage Gap`, `False Confidence`, …) · `sec` (locus; checkpoint→`Schedule`, false-confidence→`<artifact>`) · `sev` (`critical|moderate|warning`) · `status` (`open→resolved`) · `t` (fix target) · `rec` (From-OSLO recommendation).

Two subtypes are **computed**, not authored:
- **Checkpoint issue** (Adaptability, DL-196 §4): `{dim:'Adaptability', ftype:'Coverage Gap', sec:'Schedule', sev, status}` — one per checkpoint gap; severity scales with urgency-by-runway. Resolving = registering the checkpoint.
- **False-confidence issue** (Grounding, DL-197 §3): `ISS-FC-<art>` = `{dim:'Grounding', ftype:'False Confidence', sec:<art>, status:'open'}` — one per artifact that reads strong but rests on inference (`readsStrong && inferred > grounded`). Resolving = attesting the artifact.

**`Pillar`** — computed ordinal read (never stored as a number): `key`, `band` (5-step Fragile→Sound), `basis` (the normalized fraction), `why[]` (legible drivers).

**`Integrity`** — the composite (DL-194 §3): `level = min(pillars.band)`, `limitingPillar` (foundation-first tie-break), `decomposition {viability, grounding, adaptability}` (always recoverable), `posture` (`moment-in-time` + pending marker).

---

## 3. Computation spec, per pillar
All thresholds are **size-normalized fractions** mapped to the 5-step band by fixed cutpoints. The prototype's 4-step bands and absolute cutoffs (`/6`, `/4`, `>=3`) are DevNorth-fixture artifacts to replace.

**Shared band mapping (commensurability, DL-195 §6):** let `f ∈ [0,1]`; map to Fragile(0)→Weak(1)→Developing(2)→Solid(3)→Sound(4) by cutpoints `[c1,c2,c3,c4]` (placeholder, §7). Same mapping for all three so `min()` is apples-to-apples.

**3.1 Viability (= CAF composite).** Reuse R1 CAF primitives. Denominator = load-bearing understanding artifacts (prototype `UND` — replace the hard-coded set with "artifacts on the outcome-bearing path"). Numerator = artifacts with no open load-bearing CAF weakness (`!artWeak`). `f_V = sound ÷ load-bearing`. Movement only from **real per-issue weakness reduction** — retire the `_fixedCount>=2 → +1` bump (L10). Flagging leaves the linked statement weak → Viability does not firm (L11).

**3.2 Grounding.** `f_G = grounded ÷ load-bearing items` (replace the fixture `/6`). Keep the **outcome-root cap**: if the primary outcome is still inference, cap Grounding at the second band. Each open `ISS-FC-<art>` is a Grounding threat; attesting the artifact flips its inferences to grounded, drops the detector, retires flag + issue together (one-door, L7).

**3.3 Adaptability v1 (checkpoint coverage).** `f_A = registered checkpoints ÷ checkpoints needed`; only **resolved** checkpoint issues count (open = proposals). "Needed" is plan-derived (prototype hard-codes `3` — replace, §7). Runway-adequacy + lever-linkage deferred to full DL-195.

**3.4 Composite.**
```
level          = min(band_V, band_G, band_A)
limitingPillar = argmin, tie-broken Viability → Grounding → Adaptability   (DL-195 §6)
decomposition  = {band_V, band_G, band_A}   (always shown)
```
**Prototype correction:** `_gate()` currently tie-breaks Grounding-first `{grd:0,via:1,ada:2}`; implement foundation-first `{via:0,grd:1,ada:2}`.

---

## 4. Honesty invariants (testable)
- **INV-1 flag ≠ Viability** — flagging credits item-level Grounding but leaves `artWeak(artifact)` true → Viability band unchanged. (L11)
- **INV-2 Viability-from-weakness-reduction** — Viability rises iff a load-bearing CAF weakness is genuinely resolved; no fix/flag-count path. (L10)
- **INV-3 maturity-not-forecast** — no 0–100 number/dial/probability anywhere; endpoints Fragile→Sound; pending marker present. (L4, L8)
- **INV-4 bands normalize to plan size** — every band is a function of a normalized fraction; proportional scaling leaves bands unchanged. (L9)
- **INV-5 integrity decomposed not blended** — `level === min(decomposition)`, all three recoverable; no averaging. (L2)
- **INV-6 weakest-gates + tie-break** — `limitingPillar` = floor; ties resolve Viability→Grounding→Adaptability. (L3)
- **INV-7 care-point isolation** — no `Adaptability`/`Grounding` issue touches `_cafOf` / CAF rows / heat map. (L12)
- **INV-8 one-door false confidence** — flag, load-bearing count, and `ISS-FC-<art>` all from one detector; grounding the artifact retires all three. (L7)

---

## 5. FE ↔ BE integration bindings
*(Reanalysis is the ONLY event that changes any read — L13.)*

| FE surface | Reads (BE) | Changed by (event) |
|---|---|---|
| Masthead integrity indicator (ordinal band + pending) | `Integrity.level`, `.posture` | Reanalysis recompute of `min()` |
| Named limiting pillar | `Integrity.limitingPillar` (+ tie-break) | Reanalysis (new floor) |
| 3-pillar decomposition chips | `Integrity.decomposition[*].band` | Reanalysis after any issue resolves |
| Pillar drill (chip → its issues) | `openIssues()` by `dim` (Viability→CAF; Adaptability→checkpoint; Grounding→false-confidence + inference tail) | Resolve/attest → reanalysis |
| Read worklist ("Your next move", exposure-ranked) | `openIssues()` sorted by `_issueExposure` desc | Issue open/resolve → reanalysis re-ranks |
| Viability value | `f_V` → band | CAF issue resolved (real weakness reduction) |
| Grounding value | `f_G` → band (+ outcome-root cap, `ISS-FC` set) | Item grounded / artifact attested |
| Adaptability value | `f_A` → band | Checkpoint issue resolved (registered) |

Exposure ranking (DL-193 proxy): `sev` floor, `+1.5` when the issue's `dim` is the gating pillar; false-confidence ranks high but below an open critical CAF gap (foundation-first). Full propagation model deferred (§7).

---

## 6. R1 reuse vs net-new
**Reuse (don't re-spec):** CAF/Reliability primitives (`_cafOf`, `artWeak`, the band scale, the false-confidence detector `_ciFalseConfidentArtifacts`); Grounding/provenance (`grounded()`, From-OSLO/Confirmed-by-you, the `sec`-attestation path); issue lifecycle & apply-fix (Open→Resolved, event-driven reanalysis, last-good-on-failure).
**Build net-new:** the Adaptability pillar + checkpoint issues; the weakest-gates composite `Integrity{level,limitingPillar,decomposition}` with foundation-first tie-break; size-normalized denominators; the false-confidence issue type `ISS-FC-<art>`; the care-point filter guards (INV-7); the decomposed indicator + pending marker.

---

## 7. Open items / placeholders

**✅ FINALIZED 2026-08-08 (owner-ratified, single-outcome tuning — Owner-Open O-1 closed; applied to the oracle `oslo-prototype-r2.html`, guard `integrityTuningFinalized`):**
- **[RESOLVED] Band cutpoints `[0.25, 0.50, 0.75, 1.00]`** — one commensurable set for all three pillars via `bandOf(f)`. Fragile `<.25` · Weak `[.25,.5)` · Developing `[.5,.75)` · Solid `[.75,1)` · **Sound `f===1`**. The top band is anchored at **full completion** deliberately: it makes "resolve every issue ⇒ Sound" hold AND stops a pillar reading Sound while an issue is still open (reconciliation). This diverges from "evenly-spaced 5 bins" (which would put Sound at 0.8) precisely to preserve that invariant.
- **[RESOLVED] Load-bearing denominators** — ratio-based & size-normalized (INV-4): Grounding `grounded ÷ ITEMS(load-bearing items)`, Viability `clear ÷ UND(load-bearing understanding artifacts)`, Adaptability `registered ÷ needed`. DevNorth fixture counts = 6 / 4 / 3; the formula generalizes (proportional scaling leaves bands unchanged).
- **[RESOLVED] Checkpoint-needed target** — **one checkpoint per outcome-bearing workstream** (DL-195 §5). DevNorth = 3 (sponsorship · registration · venue).
- **[RESOLVED] 5-step interior labels** — **Weak · Developing · Solid** (endpoints Fragile · Sound). The oracle already ships 5-step; the older 4-step note is superseded.
- **[APPLIED to oracle] The two prototype-vs-canon corrections (§0 note, §3.4):** foundation-first tie-break `{via:0,grd:1,ada:2}` and retirement of the `_fixedCount`-bump are now in `oslo-prototype-r2.html`. Adaptability ladder is now linear (no tier skip).

**Still open (as before):**
- **[deferred, ratified] Full DL-195 Adaptability** (runway + lever weighting) and the **full DL-193 exposure-propagation model** — v1 uses coverage + the severity proxy.
- **[carry-forward] D184.3 reversal** (DL-193 §5) for explicit ratification.

---

## 8. Acceptance criteria
1. **AC-1** `Integrity.level === min(band_V,band_G,band_A)`; three decomposition bands rendered individually. (INV-5)
2. **AC-2** With two pillars tied at the floor, `limitingPillar` follows Viability→Grounding→Adaptability; verified each pairing. (INV-6)
3. **AC-3** Flagging a load-bearing item raises Grounding's item credit but leaves Viability unchanged (artifact stays `artWeak`). (INV-1)
4. **AC-4** Resolving a CAF weakness raises Viability; N fix-clicks with no genuine resolution leave Viability flat. (INV-2)
5. **AC-5** No numeric score/dial on any integrity surface; pending marker always shown; endpoints Fragile→Sound. (INV-3)
6. **AC-6** Proportionally scaling the plan (×k issues and load-bearing) leaves every band unchanged. (INV-4)
7. **AC-7** An Adaptability/Grounding-dim issue never appears in `_cafOf`/CAF rows/heat map; it does appear in its pillar drill + exposure queue. (INV-7)
8. **AC-8** For a strong-reading inference-backed artifact, the flag, load-bearing count, and `ISS-FC-<art>` co-exist; attesting retires all three in one recompute. (INV-8)
9. **AC-9** Registering a checkpoint raises Adaptability only after reanalysis (open = proposals); coverage = resolved ÷ needed. (L5)
10. **AC-10** Every integrity surface changes only via a reanalysis event; a failed reanalysis preserves last-good. (L13)

---

*Slice 1 of the R2 delta. On sign-off → Slice 2 (Issue lifecycle & grounding acts). The two flagged prototype corrections (5-step bands, foundation-first tie-break) are small edits that can be applied to `oslo-prototype-r2.html` alongside.*
