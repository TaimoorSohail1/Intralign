# DL-123 — Option C — CAF with reliability per dimension

- **Date:** 2026-07-17 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# Option C — CAF with reliability *per dimension*: the read consolidates onto one construct

**Class:** A (foundational read-architecture) · **Framework 001** — AI drafts; **owner ratifies at land.** · **Amendment set with explicit supersession** — not a silent rewrite.
**Decided by:** Idris (Founder Console) · **Ratified:** 2026-07-17 · **Packet:** `DECISION-PACKET-evidence-vs-caf.md` · **Reference mock:** `caf-reliability-per-dimension-mock.html`

---

## Decision

The Overview leads on **CAF as one construct**, and **evidence/inference is absorbed into it as a per-dimension attribute** — no longer a competing, co-primary framework. Each CAF dimension (Clarity · Alignment · Feasibility) now carries **both** its **level** (how sound — neutral maturity, no RAG) **and** how **grounded** it is (your evidence vs OSLO's inference), computed from `_ciDimInferenceStats()`. The three surfaces that previously said this three different ways — the **global reliability qualifier**, the **Progress grounding ledger**, and the **CAF band** — collapse into **the CAF rows**. Issue counts stay **drivers under each dimension**, never the CAF headline. The **load-bearing count** relocates to the **Inference map** as its one home.

**No invariant is weakened.** Reliability is **preserved** (moved, not removed); it is never folded into a level (no hidden discount); no composite/formula is introduced (evidence stays a *shown attribute*); levels stay neutral (D003); issue counts stay drivers, never a burndown headline (D180c). This is a **realization** of the doctrine's own hierarchy, executed as one construct — not a repeal.

---

## What this supersedes / amends (explicit)

- **D002 / D051 — "the read never stands bare" (the reliability qualifier).** *Amended, not repealed.* Reliability moves from a **global** qualifier on the read to a **per-dimension** cue on the CAF rows. The invariant HOLDS: the read still never stands bare — it is now qualified by **the limiter** (which, post-Phase-2, names the limiting dimension *and* flips its action confirm-vs-fix by that dimension's grounding) plus the per-dimension cues. The **overall grounding word survives on-demand** in the Confidence popover (the "Why"), so the summary reliability is reachable — just not resident on the primary read, where it read as a contradiction against the per-dimension cues. The global qualifier element (`#ov-rel`) and its phrase (`_groundingPhrase`) are retired.

- **D180 / D180c — Progress is grounding, not clearing; more issues can mean a deeper read.** *Amended.* The Progress **grounding ledger** (proportional foundation-bar + two-state provenance legend + statement-type decomposition + load-bearing line) is **retired** — grounding now lives per-dimension on the CAF rows. Progress keeps its **issue counts** and a **compact grounded summary** (the hero that names the statement unit + both ratified epistemic classes + a pointer to the read). The **anti-burndown doctrine is untouched**: issue counts remain drivers under dimensions, never the CAF metric.

- **D183 / D183b / D183c — no composite score; grounding language.** *Reaffirmed + amended.* No composite/forecast is reintroduced (the per-dimension cue is an attribute, not a rolled-up number). The **grounding language** (D183c) moves per-dimension; the grounding **word** survives in the Confidence popover, still computed, still in the ratified vocabulary — graded there by the D183c/D196b qualifier guards on `#cp-grd` / `#cpp-grdword`.

- **D194 / D253 / DL-111 (erratum) — the grounding-ledger unit + the two-provenance-states doctrine.** *Amended.* The **two provenance states** (grounded / inferred) now read **per dimension** on the CAF rows (solid = your evidence, hatched = OSLO's inference — Phase 1). The Progress bar / legend / decomposition are retired. The **STATEMENT unit** (D253) and the **honest-subset** invariant (K ≤ inferred statements) **survive** — the compact Progress hero still names the statement unit, and the model-level guards (`pgxHeroNamesTheUnit`, `stmtDecompSumsToTotal`, `loadBearingHonestSubset`) remain registered.

- **DL-118 — Progress owns the grounding ledger; the four-surface role model.** *Amended.* Progress **no longer owns** the grounding ledger; the **CAF rows own the per-dimension evidence**. The four-surface role model otherwise stands. The **load-bearing count** — the K inferences the read most rests on — **relocates to the Inference map** as its one home (**owner fork 3a, ratified 2026-07-17**), where the "See them →" pointer already led; it is not dissolved.

- **DL-113 (statement unit) — preserved.** **DL-121 (confirm the inferred assumption) — still valid** and now sharper: the per-dimension cue + the grounding-aware limiter are exactly what tell the user *which* dimension to confirm.

- **The foundation-bar owner-LOCK ("blend / 29-hero", `_progressHTML` amendment note).** *Retired* with the Progress bar it governed. Recorded here explicitly. (The `WI-R5 progress-panel-foundation-bar` work item is superseded.)

---

## Scope boundary — what did NOT change

Neutral maturity levels (D003 / D175 — no RAG on the CAF levels; the evidence cue is grounded/inferred, also neutral). The false-confidence machinery (`_ciFalseConfidentArtifacts`, the Inference-map flag, the popover "Why"). The statement model, the load-bearing definition (D181a clauses a/b/c), and every count's computed-from-state guarantee (D173). The issue-count guards on the Overview. Confidence-as-maturity (never health/readiness/RAG).

---

## Build (Phases 1–4, verified — boot self-check 142/142, zero failures)

1. **Per-dimension evidence on the CAF rows** — each dimension shows level + how-grounded (neutral, computed). Never folded into the level.
2. **Limiter flips fix-vs-evidence** — the limiting dimension's grounding drives the verb: thinly-evidenced → "Confirm it to lift the read"; well-grounded → "A plan gap to fix"; no evidence → "Bring evidence to firm it." ≤8 words, verb present, limit named (D186/D186c).
3. **Progress grounding ledger dissolved** to a compact summary (hero names the unit + both epistemic classes + read-pointer); load-bearing count **relocated to the Inference map** (fork 3a).
4. **Global reliability qualifier retired** (`#ov-rel`); "never bare" carried by the limiter + per-dimension cues; the overall grounding word survives in the popover — resolving the global-vs-per-dimension contradiction.

**Guards:** three surface-structural guards retired with the surface they graded (`pgxBarComputed`, `pgxBarStructure`, `pgxTwoStates` — the DL-111 erratum) plus the foundation-bar owner-lock. Five count/vocab guards **repointed** (not retired) to load-bearing's new home (`loadBearingComputed`, `provenanceOneHome`, `noHoldingIt`, `d183Inferences`, `risingInferenceOK`). Model-level invariants kept (`pgxHeroNamesTheUnit`, `stmtDecompSumsToTotal`, `loadBearingHonestSubset`). The D002/D051 "never bare" hero check and the CAF-coupling guard now prove the **limiter** as the required read; the D196b grounding-vocabulary negative control repointed to `#cpp-grdword`.

---

## Governance

**Slice-3 (Overview)** and **Slice-10** reopen; **re-signoff required** after this lands. Lands as **Class A canon via `dl-land`**, as an **amendment set with explicit supersession**. AI drafted + built on ratification; **only the owner ratifies.**
