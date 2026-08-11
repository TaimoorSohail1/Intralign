# DL-197 — The Grounding false-confidence issue type (completes the three-pillar issue layer)

**Status:** ⛔ **RATIFIED 2026-07-27 by Idris** (sole ratifier, Framework 001) — canon **for the R2 track**. Built + green (183/183 guards). Executes DL-196 §2/§7.7 (the staged third issue type). The three-pillar issue layer is now complete: Viability→CAF issues · Adaptability→checkpoint issues · **Grounding→false-confidence issues.**
> _Scribe-drafted + built 2026-07-26 (owner-directed "address false confidence issue type next"), ratified 2026-07-27._ Consumes DL-196 (integrity resolves through the issue layer), DL-194 (three-pillar integrity), DL-190 (limiter-standalone / level ≠ trust), and D181a clause (c) (the false-confidence definition already in the build).
**Origin:** DL-196's principle — "all three integrity pillars resolve through the issue management layer." Two of three shipped (Viability→CAF issues, Adaptability→checkpoint issues). This packet is the third: **Grounding→false-confidence issues.**

---

## 1. What a false-confidence issue *is* — and what it is not
A false-confidence issue is **not** a substantive risk. ISS-01 "Venue Wi-Fi capacity is unconfirmed" is a real **Feasibility** threat — the dependency might actually fail — so it correctly stays a **CAF/Viability** issue; confirming it de-risks Feasibility.

A false-confidence issue is the distinct, sharper case the load-bearing machinery was built to catch (**D181a clause (c)**, already in the code): **an artifact that *reads strong* — High reliability, nothing critical open — but whose confidence rests mostly on OSLO's inference, not the user's evidence.** *"Scope reads fine **because** OSLO invented a coherent story — and coherence is not evidence."* Nobody is looking at it, precisely because it looks fine. That is a **Grounding** threat (unearned trust — `level ≠ trust`), not a CAF threat. On the DevNorth fixture there is exactly one: **Scope** (reads High; 7 of its statements are inference).

## 2. The one-door construction (non-negotiable — D181a)
The issue is **computed**, not authored, from **`_ciFalseConfidentArtifacts()`** — the *same* function the Inference-map flag and load-bearing clause (c) already read. So the flag, the load-bearing count, and the issue can **never disagree**, and **grounding the artifact retires all three together** (that is the user's success, not a guard breaking). There is no second definition of "false confidence" anywhere. → guard `falseConfidenceIsOneDoor`.

## 3. Structure
- **One issue per false-confident artifact.** `ISS-FC-<art>` (DevNorth → `ISS-FC-Scope`). `{ dim:'Grounding', dims:['Grounding'], ftype:'False Confidence', sec:<art>, status:'open' }`. Title names the trap honestly: *"Scope reads solid — but on OSLO's inference, not your evidence."*
- **Recommendation (From OSLO, confirmable):** *"Confirm what Scope rests on — or flag it. Its read is strong, but most of it is OSLO's inference; confirming grounds it, flagging is just as good if it doesn't hold."* (DL-190 D5 symmetry: confirm and flag both settle it.)
- **Resolving = grounding the artifact.** Applying the rec attests the artifact (the existing `applyFix` `sec`-attestation path: `PLAN_SECTIONS[sec].basis='attested'`), which flips its inferences to grounded → **Grounding rises**, `_ciFalseConfidentArtifacts()` drops the artifact, the flag and the issue retire. Same live-recompute behaviour as checkpoints raise Adaptability — now for Grounding.
- **Provenance preserved:** the read was OSLO's inference until the user attests it (From OSLO → Confirmed by you). `level ≠ trust` intact.

## 4. The load-bearing discipline (why this doesn't resurrect the treadmill) — DL-196 §3 / DL-190 D2
Only the **high-exposure** case becomes an active issue: an artifact that reads **strong on inference** is dangerous *because it's invisible*. The **benign inference tail** — the ordinary "OSLO inferred this, marked honestly unconfirmed" items — **stays on the Inference map, never issue-ified, never nagged.** `_ciFalseConfidentArtifacts()` is already this gate by construction (`readsStrong && inferred > grounded`): an artifact that reads *appropriately* uncertain, or is mostly grounded, never qualifies. Uncertainty ≠ defect; only *unearned confidence* is.

## 5. The care point (the guarded invariant — DL-196 §5, extended to Grounding)
**⛔ Grounding-dim issues feed Grounding ONLY.** `dim:'Grounding'` keeps them out of `_cafOf`, the CAF rows, and the Attention heat map (which iterate `_HEATDIMS` = Clarity · Alignment · Feasibility) — exactly as Adaptability issues are kept out. They feed **Grounding + the exposure queue** only. → guard `groundingIssuesDoNotTouchCAF` (the twin of `adaptabilityIssuesDoNotTouchCAF`).

## 6. Queue integration (DL-193 exposure)
False-confidence issues rank in **"Your next move"** by outcome-exposure alongside CAF (Viability) and checkpoint (Adaptability) issues — one queue, prioritising *across* all three pillars. `_issueExposure` gets a Grounding path: a strong-reading artifact resting on inference is a **high-exposure** integrity threat (the read is trusted more than it has earned), so it surfaces prominently — but below an *open critical CAF* gap when one exists (a thing that might actually fail outranks a thing that merely isn't yet verified, foundation-first).

## 7. Relationship to DL-190 (the existing limiter-standalone confirm)
DL-190's ratified Start-here move — *confirm the limiter's load-bearing support* — is the **clause (a)/(b)** case (a CAF dimension's read rests on an unconfirmed support). That remains a **Viability** concern surfaced against the CAF issue it de-risks; DL-190 is untouched. This packet adds the **clause (c)** case as its own Grounding issue. Together the load-bearing definition (all three clauses) is now fully represented in the issue layer: (a)/(b) via the CAF issues they support, (c) via the false-confidence issue. *(A later reconciliation could route DL-190's standalone surface through a Grounding issue too; not required here and not proposed.)*

## 8. Build plan
1. `_syncFalseConfidenceIssues()` — for each `art` in `_ciFalseConfidentArtifacts()`, create `ISS-FC-<art>` if absent (open); idempotent. Call at boot (after the model + functions exist) and inside `_refreshIssueSurfaces()` so the set stays one-door with the flag.
2. Confirm/resolve — reuse the existing `applyFix` `sec`-attestation (grounds the artifact → raises Grounding, retires flag+issue). No new resolution mechanic; the false-confidence issue's `sec` is the artifact.
3. `_issueExposure` — Grounding path (high; below open-critical-CAF, foundation-first).
4. Care-point — `dim:'Grounding'` (already excluded from `_HEATDIMS`); add the explicit guard.
5. Guards — `falseConfidenceIsOneDoor`, `falseConfidenceOnGrounding`, `falseConfidenceCarriesProvenance`, `confirmGroundsRaisesGrounding`, `groundingIssuesDoNotTouchCAF`.
6. Verify — the queue now carries a Grounding false-confidence issue (`ISS-FC-Scope`) beside CAF and checkpoint issues; confirming it raises Grounding + retires the Inference-map flag together; care-point holds; suite green.

## 9. Open for ratification
- Confirm §1 — false confidence is a **Grounding** issue (unearned trust), distinct from a substantive CAF risk; ISS-01 stays CAF.
- Confirm the **one-door** construction (§2) — computed from `_ciFalseConfidentArtifacts()`, no second definition.
- Confirm the **load-bearing discipline** (§4) — only strong-on-inference qualifies; the benign tail stays on the map.
- Confirm the **care-point** (§5) as a guarded invariant.
- Confirm **DL-190 left as-is** (§7) — the (c) case is additive; no rework of the ratified standalone confirm this packet.
