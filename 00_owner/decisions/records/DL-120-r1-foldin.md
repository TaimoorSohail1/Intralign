# DL-120 — R1.x intermediate enhancements fold into the R1 build; R1 feature-freezes before dev handoff

- **Date:** 2026-07-16 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# DL-PENDING — The R1.x intermediate enhancements fold into the R1 build; R1 feature-freezes before dev handoff

**Class:** A (release-scope decision) · **Framework 001A** (AI drafts recommendation; **owner ratifies**; numbered at land per DL-065)
**Decided by:** Idris (Founder) · **Drafted:** 2026-07-16 · Analysis: `DECISION-PACKET-r1-foldin.md`. Grill record: intermediate-release track (R1.x).

## Problem
The R1.x intermediate track was opened (2026-07-14) on the premise that R1 was **already in build**, so owner-directed enhancements had to wait for a release *between* R1 and R2. That premise no longer holds: the **dev team has not started R1 implementation and will not begin until next week**. With no in-flight R1 to protect, holding the ratified, already-built enhancements back only forces the dev team to build the same surfaces (Confidence card, Progress panel, CAF, Start-here) twice — once for R1, again for R1.x.

## Decision
The ratified R1.x enhancements **fold into the R1 build**, and R1 **feature-freezes before dev handoff**. Specifically:

1. **Fold in (Q1).** The ratified + built enhancements — **DL-113, DL-114 (+ erratum DL-115), DL-116, DL-117, DL-118, DL-119** — become part of the **R1 build scope**. They are already canon and already realized in the deliverable prototype (`slice-10`, boot self-check 145/145); folding in is a **scope + consolidation** decision, not new build.

2. **Two clocks — ratify now, execute at freeze (Q6).** This decision fixes the *destination* immediately, so the next few days of enhancement are authored **directly into R1** as one target. The consolidation is a **freeze activity**, run **once** against the final spec set. The freeze line is **R1 feature-freeze before dev handoff** (target: before dev starts next week). Everything landed before the line folds into R1; anything after it becomes the first **R1-test-driven-fix** cycle.

3. **Consolidate for a clean handoff (Q2, Q3).** At freeze, dev receives **one self-consistent R1**:
   - amendments/errata are folded into their **parents in the build spec** — DL-115 → DL-114's effective statement; DL-119 → D253's effective statement — while the **append-only decision record stays untouched** (merged canon is never rewritten);
   - the **doc-integrity debt** surfaced during the DL-117 land is cleared as a named workstream — the DL-053 banned terms ("Context Plane," "Judgment Layer," "Outcome Management") across the R1 product/scope/API/data-model/analysis-engine specs, the superseded cross-references (FINDING_PANEL → FINDING_WORKSPACE, RECOMMENDATION_PANEL → RECOMMENDATION_WORKSPACE, DATA_MODEL V1.2 → V1.1), and the renamed term (`canonical_key` → `dedup_key`);
   - reopened slices (Overview / Progress / slice-10) are **re-signed** as part of R1 signoff;
   - a single consolidated R1 build-spec is assembled from the folded canon + the slice-10 prototype as the visual reference.

4. **"R1.x" is repurposed (Q5).** The label no longer carries enhancement content; it becomes the bucket for **post-handoff, test-driven fixes** only.

## Scope boundary (explicitly NOT folded into R1) (Q4)
- **Enhancement #4 — notification router / global bar:** the proposal is ratified but the **router build awaits owner commission** (Framework 001). Not built, not in the prototype. Stays out.
- **Confidence-architecture "revisit at a tripwire":** a deferred decision — the composite band **stays** for R1 (adoption-first). Not a build item.
- **R1-test-driven fixes bucket:** already deferred to a later session. Unaffected.

## Conditions of record
Timeline is re-scoped, not free: an **updated dev estimate** is to be obtained against the folded R1 scope before a delivery date is committed. QA coverage of the enhanced surfaces moves into R1's single test pass (verified in the prototype at 145/145, not yet through dev's own pass).

## Governance
Route via `dl-land` (owner ratifies; numbered at land per DL-065). This is a **release-scope ruling** (which ratified canon rides in which build); the **consolidated build-spec is product realization** assembled from ratified canon + the prototype, and does not require its own DL. The R1.x intake track is re-scoped by this decision (recorded here so the track history stays coherent rather than dissolving silently). AI recommends; only the owner ratifies.

## Provenance
Owner proposed folding the post-R1 enhancements into R1 (2026-07-16), citing that dev has not started R1 and will not until next week. Packet drafted (`DECISION-PACKET-r1-foldin.md`) with six recommendation-bearing points; owner asked whether to ratify now or after the remaining days of enhancement, which surfaced the two-clocks framing and the freeze line; packet amended (§7 + Q6) and **accepted as-is** (Q1–Q6 all ratified as recommended). AI recommends; only the owner ratifies.

### Sources
- Analysis: `DECISION-PACKET-r1-foldin.md` (six decision points, all accepted).
- Folded canon: **DL-113 / DL-114 / DL-115 / DL-116 / DL-117 / DL-118 / DL-119** (all landed on `main`, all realized at `slice-10` 145/145).
- Track: intermediate-release (R1.x) intake log; doc-integrity warnings surfaced during the DL-117 land.
