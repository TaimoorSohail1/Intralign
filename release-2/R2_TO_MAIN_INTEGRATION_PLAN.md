# R2 → main Integration Plan (blueprint — nothing merged)

**Date:** 2026-08-09 · **Author:** AI (analysis/plan only — owner ratifies; owner/dev execute git) · **Status:** review-ready blueprint.
**Owner directive (2026-08-09):** decide the *strategy* now; **hold execution until the development team approves.** Do NOT land to `main` yet.

---

## 1. Strategy — RATIFIED 2026-08-09 (owner)
- **Vehicle:** a curated **`integration/r2-to-main`** branch — mirroring how R1 landed (`integration/r1-to-main`, now fully merged into main). **Not** a raw `release-2 → main` merge; **not** leaving the decisions in the parallel store indefinitely.
- **Scope:** only **ratified canon** lands — the R2 decisions + the ratified R2 spec content, integrated into their real canonical homes. **Working/prototype artifacts do NOT become canon** (see §7 exclusion list).
- **Route:** `integration/r2-to-main` → PR → green doc-integrity gate → **owner merge**, on dev-team approval (Framework 001).

## 2. Precedent (grounds the strategy)
R1 landed via **`integration/r1-to-main`** — a dedicated, curated integration branch, now merged into main (0 commits ahead; present in `git branch --merged main`). R2 follows the same shape.

## 3. Current state
- `00_owner/decisions/decision_log.md` tops at **DL-156 on BOTH main and release-2.** No R2 decision is in the canonical ledger yet.
- R2 decisions live as **separate staged files under `release-2/canon/decisions/`** — a parallel store, never integrated into the ledger, and **incomplete/mixed-status** (§4).

## 4. The R2 decision corpus — inventory & readiness  ⚠️ NOT landing-ready as-is
| Bucket | Items | Action before landing |
|---|---|---|
| **Ratified records (ready)** | DL-172, DL-184, DL-193, DL-196, DL-197, DL-206, DR-7 | Land as-is (integrate + promote). |
| **Drafts — need owner ratification** | DL-194, DL-195 (scribe-drafted, pending); **DL-200–205 (= DR-1…DR-6)** (drafts for ratification); `R2_DL_READJUDICATION_WORKSHEET` (draft) | **Owner ratifies or excludes** each before landing. AI cannot ratify. |
| **Numbers with NO formal record** | DL-157–163, 164–171, 173–183, 185–192, 198–199 (referenced in audits/backlog only) | **Reconcile:** for each — is it renumbered (e.g. record shows DL-172→198, DL-173→199), re-adjudicated in the worksheet, an R1.x-track decision, superseded, or a real gap needing a record? Escalate; do not infer. |
| **DR series** | DR-7 = own ratified record; **DR-1…DR-6 = captured as DL-200–205** (draft) | Ratify DL-200–205, or keep DR-1…6 as the canonical form — owner decides the mapping. |

**Consequence:** there is **no authoritative, ordered R2 ledger** yet. One must be built (§5 Phase A) before integration.

## 5. Two-phase plan
### Phase A — CONSOLIDATE the R2 ledger (on `release-2`; owner-led; before dev approval is even needed)
1. **Ratify or exclude** every draft (DL-194, DL-195, DL-200–205/DR-1…6, the worksheet). Owner-only.
2. **Reconcile the numbering** — resolve DL-157–163, 164–171, 173–183, 185–192, 198–199 (renumbered / re-adjudicated / R1.x / superseded / real). Produce a definitive map.
3. **Author an authoritative, ordered R2 decision INDEX** (DL-157…206 + DR-1…7) with, per entry: number, title, status, one-line ruling, record path, and supersede/amend pointers. This becomes the ledger delta for Phase B.

### Phase B — INTEGRATE into main (on dev-team approval; the git-mechanical step)
1. Create `integration/r2-to-main` **off `main`** (not off release-2 — keep working artifacts out).
2. Append the consolidated R2 entries to `00_owner/decisions/decision_log.md` after DL-156, in order.
3. Promote the ratified decision **records** from `release-2/canon/decisions/` → `00_owner/decisions/`.
4. Promote the **ratified R2 spec content** into the canon tree (`10_product` / `20_handoff` / `30_engineering`) at its canonical home; retire the `release-2/canon/**` staging copies.
5. Apply the **supersession reconciliation** (§6).
6. Add a **changelog** batch entry.
7. Run the doc-integrity gate green → PR → **owner merge**.

**Phase-B changelog delta — STAGED (append to `00_owner/changelog/changelog.md` at graduation; CHG ids assigned then — main stays untouched until then):**
- **DL-211** (ratified 2026-08-09) — *Proposal-resolution model + cross-surface resolution sync + itemized atomic findings.* Proposals split into **build** (adds a missing structural element — accepting is a build act that resolves the structural finding and may firm the band via reanalysis), **inference** (accept OSLO's guess — additive; grounding resolves only by verifying, GT-35), and **optional** (additive). A finding and its resolving proposals are one object: resolving from any surface (card/artifact/read row) closes it once through the single reanalysis path (GT-10). Multiple resolvers close only when all accepted (keynote-backup needs its requirement + its task). Findings render itemized, never merged into one prose row. **Amends the ratified `proposalsFoldedIntoRead` invariant** (band-movement now permitted for build proposals — a real structural change, not manufactured confidence). Guards GT-51…GT-54. **At graduation:** reconcile with `FINDING_MODEL_V1` / `RECOMMENDATION_MODEL_V1` (proposal-as-build-fix) per the reconciliation catalog. No R2 freemium-build impact.
- **DL-210** (ratified 2026-08-09) — *CAF dimension boundaries + deterministic structural-target dimension assignment (with the escalation model).* Boundary cut (Clarity=definition · Alignment=edge/relational · Feasibility=achievability) with Clarity→Alignment→Feasibility precedence; **Alignment is relational**, assessed top-down outcome→roots (optimization + per-edge misalignment; tangent check; metric-mismatch folded in). Dimension assignment becomes **deterministic from the finding's structural target**, judgment quarantined at L0 extraction and surfaced via escalation — **amends CAF Assessment Model Positions #10/#11** (preserves #2/#13). Escalation lifecycle: runtime→user clarify/verify issue, model-gap→owner/governance + a **leverage-gated known-unknown**; a load-bearing model gap **ceilings integrity as incomplete, never Fragile** (unknown ≠ bad). Reconciles DL-209's decompose-never-dual-class with CAF's multi-dimension findings by layer (`dim` primary + `dims[]`). Extends DL-209/Slice 10; guards GT-45…GT-50. **At graduation:** the CAF/Finding reconciliation is catalogued in **`R2_TO_MAIN_CAF_RECONCILIATION_CATALOG.md`** (per-doc checklist): `CAF_ASSESSMENT_MODEL_V1` §9/Positions #10/#11 (primary amendment), `FINDING_MODEL_V1` + `FINDING_SYSTEM_SPECIFICATION_V1` (surgical — dimension from structural target; add `structural_target` field), `PLANNING_INTELLIGENCE_SPECIFICATION_V1` §10 (enrich the Alignment evaluation with the relational top-down model), and lens-reconciliation for `RECOMMENDATION`/`CONFIDENCE`/`RELIABILITY`/`MRI`/`MODEL_LINEAGE_INDEX`. Most edits are surgical (finding-type-independence and the flat taxonomy are preserved); DL-196 CARE-POINT filter preserved throughout. **After** the amendments land, run a full product-grill pass to verify whole-canon coherence. No R2 freemium-build impact.
- **DL-209** (ratified 2026-08-09) — *Load-bearing sensitivity + issue-classification/resolution model.* Five first principles (issue = load-bearing threat; **load-bearing = magnitude of integrity-sensitivity ≥ calibrated threshold**, two-sided; diagnosis ≠ resolution; **only verify moves Grounding**; three closing acts verify/build/decide). L0–L4 architecture ("quarantine the fuzziness": LLM extraction only at L0, deterministic sensitivity/classification above; thin learnable L2 calibration). Threshold: global-at-launch, dormant hierarchical-shrinkage segmentation (stage→L1 runway, stakes→explicit knob, domain→learned), zero-data-equals-global guard. Retires ad-hoc `primaryMove` → L3 derivation; multi-aspect decomposes (not dual-class). Completes DL-196/197; consumes DL-184/193/190; bounded by DR-7/DL-103. No R2 freemium-build impact. At graduation: `00_owner/decisions/` record + the finding-type→resolution table + Demo-Config L2 params + firewall guards land with the build.
- **DL-208** (ratified 2026-08-09) — *Pro program / cross-plan execution-cognition scope + Pro price $79.* Pro program layer = Bundle A (roll-up · cross-plan dependency mapping · program monitoring, under a program-envelope cap); roll-up is a decomposable aggregate, never a health score/forecast. **Pro price ratified $79** (amends DR-7 — drops placeholder/provisional; closes the $69 option). Adopts US **"program"** over "programme" (DL-053 register + repo find-replace). At graduation: `RELEASE_1_TIER_DEFINITIONS_V1` §1/§2c/§2d, `CANONICAL_GLOSSARY` DL-053, DR-7 pricing + prototype `_PRICING.pro` → $79 / `ph:false`.
- **DL-207** (ratified 2026-08-09) — *Plan export & PM-tool tiering.* File export (CSV/Excel/text/PDF) = **Free**; one-way push/import into a PM tool (view-only) = **Basic**; two-way sync + execution monitoring = **Pro**. Realizes DL-206 §2/§4; extends DR-7 / DL-083; never "auto-sync" for Basic. Affected at graduation: `RELEASE_1_TIER_DEFINITIONS_V1` (export/integration rows) · `CANONICAL_GLOSSARY` DL-053 register · DR-7 pricing page · backend obligation `OSLO_BACKEND_CAPABILITIES.md` #24.
- **DL-206** (ratified 2026-08-09) — *Execution-monitoring tier split* (manual → Basic; continuous / two-way sync / programme → Pro; amends DL-083).

## 6. Supersession / amendment reconciliation (known; confirm during Phase A)
- **DR-3** (enforce via commitment gate) **supersedes** DL-172's "nothing gated in Alpha / intent-capture only / neutral-copy" clauses.
- **DL-172** extends DL-158 (pricing unit); supersedes "project-as-unit / analyses-as-limit."
- **DL-206** amends **DL-083**; resolves DL-172 §7 ↔ DR-7.
- **DR-1** made `oslo-prototype-r2.html` the single canonical R2 prototype (retires the two-lineage divergence).
- (Full list produced in the Phase-A index.)

## 7. Exclusion list — these are NOT canon; they stay R2-scoped / working
Prototypes (`oslo-prototype-r2.html`, `onboarding-arc-prototype.html`), `DEMO_VS_PRODUCTION_AUDIT_2026-08-09.md`, `DEMO_CONFIG_REGISTER.md`, the `OSLO_BACKEND_CAPABILITIES` register, `R2_*_AUDIT`/checklist docs, `*_DRAFT.md`, `DL-PENDING-*`, dev-handoff/backlog docs. (The ratified *decisions* these reference land; the working docs themselves do not.)

## 8. Execution recipe (Phase B — owner runs on their Mac, after dev approval)
```
cd ~/GitHub/oslo-knowledge-base
git checkout main && git pull
git checkout -b integration/r2-to-main
# apply the Phase-A consolidated ledger delta + record/spec promotions (curated, per §5B)
git add 00_owner/decisions/ 10_product/ 20_handoff/ 30_engineering/ 00_owner/changelog*
git commit -m "integration(r2→main): land ratified R2 decisions DL-157…206 + DR-1…7 + specs (curated)"
python3 tools/doc_integrity_check.py    # must be 0 errors
git push origin integration/r2-to-main  # open PR → doc-integrity gate → owner merge
```

## 9. Owner / dev open items (blockers before Phase B)
1. **Ratify or exclude** the draft decisions (DL-194, 195, 200–205/DR-1…6, worksheet).
2. **Reconcile** the DL-157–163 / 164–171 / 173–183 / 185–192 / 198–199 numbering & missing records.
3. Confirm the **DR-1…6 ↔ DL-200–205** canonical mapping.
4. Approve the **exclusion list** (§7) — what is canon vs working.
5. **Dev-team approval** to run Phase B.

_AI recommends and can author the Phase-A index + the curated delta once the drafts are ratified and the numbering is reconciled by the owner. AI does not ratify canon and cannot run git in this environment._
