# R2 DL Re-adjudication Worksheet — DL-164…197 against the AI-first spine

*2026-08-04 · The DR-1 follow-on. DR-1 ruled the AI-first prototype (`oslo-prototype-r2.html`) the canonical R2 source of truth; this worksheet adjudicates every earlier R2 decision (DL-164…197, the `DL-1xx_NAMED_IN_CAPS` "canon track" ratified against `prototype-r2_15.html`) against that spine + the six DR rulings. Framework 001: verdicts are AI-drafted; **Idris ratifies.***

## What this changed about the audit (read first — it's good news)

The underspecification audit called the two lineages a "divergence" and flagged the integrity/issue-layer computation as **undefined** (OI-3 Adaptability, OI-4 issue→pillar, OI-7 false-confidence). Reading the actual DLs corrects that:

- **These are not a rival product.** DL-164…197 are the *earlier* R2 canon track. The AI-first prototype is a *newer reimplementation* that carried some of it (three pillars, weakest-gate, grounding, issue worklist) and hasn't yet absorbed the rest. The relationship is "carry the canon into the newer shell," not "pick a winner."
- **Several audit "blockers" are already specified in canon**, just not carried into the AI-first prototype or the backend-caps doc (and not all were staged for the audit's subagents):
  - **DL-195** *is* the Adaptability computation spec (the "outcome-checkpoint-optimization assessment," State-1 keystone) → downgrades audit **OI-3** from "undefined" to "defined-in-canon, carry + finish."
  - **DL-196** *is* the exposure-gated issue-layer spec (issue shape `{dim, dims, ftype, sec, sev, status}`, all three pillars resolve through it) → downgrades **OI-4**.
  - **DL-197** *is* the Grounding false-confidence issue type (`ISS-FC-<art>`) → downgrades **OI-7**.
  - **DL-194** (indicator variant) *is* the three-state integrity model; **State 1 is the committed R2 scope** → this is the ratified spec behind DR-4.
- **Net:** the integrity model isn't unspecified — it's specified in DL-193/194/195/196/197 and needs to be **carried into the AI-first prototype + the R2 delta contracts**, then reconciled with the DR-4 rulings (which are consistent with it). The real gap is *implementation + contract-writing*, not *decision-making*. That's a materially better position than the audit implied.

## Verdict legend
- **CARRY** — compatible with the AI-first spine + rulings; keep/implement as-is (may not yet be built in the AI-first prototype).
- **CARRY-MODS** — carry the intent, adapt to the AI-first model (mod noted).
- **SUPERSEDE** — replaced by the AI-first reimagining or a DR ruling; retire (record the successor).
- **RENUMBER** — decision-number collision with a Lineage-B ruling; keep content, reassign ID.
- **OWNER** — needs your call before it can be classified cleanly.

*First-pass classification for your ratification. Load-bearing CARRY items (esp. DL-184/193/194/195/196/197) get a full deep-read at implementation; this worksheet fixes their disposition, not their final spec text.*

---

## Adjudication

### A. Guidance, coaching, notifications, collaboration asks (DL-164–170)
| DL | Decided | Verdict | Rationale |
|---|---|---|---|
| 164 Guidance system (coaching + lifecycle) | In-app coaching arms + lifecycle comms | **CARRY-MODS** | Doctrine compatible; re-realize the coaching moments on the AI-first surfaces. |
| 165 Confidence-pill redesign | Redesign the Outcome-Confidence popover | **CARRY-MODS** *(ruled 08-04)* | No confidence ring/pill in the AI-first prototype — the headline is the Outcome-Integrity masthead and the explainer role is served by the pillar-drill (`_pillarDrill`/`focusPillar`). Carry the "why this band?" explainer intent onto the integrity band; retire the ring visual. |
| 166 Notifications quiet mode | Quiet mode, panel-aware suppression, burst coalescing | **CARRY** | This *is* the salience/quiet-mode spec the audit wanted (R2G8). Carry. |
| 167 Coaching triggers = earned events | Trigger on earned events, not dwell | **CARRY** | Compatible; refines DL-164. |
| 168 Soliciting input as utility | The evidence-forward review ask | **CARRY** | The reviewer-ask surface (audit R2G2 workflow). Carry. |
| 169 Loop-close + k-factor invite | Tie payoff to the ask; invite-to-own-read | **CARRY** | Matches prototype `inviteToRead` (audit R2G10). |
| 170 Evidence vs comment legible | Make the choice legible; mechanics unchanged | **CARRY** | Audit confirmed covered; present in the AI-first prototype. |

### B. Onboarding / first-run / reveal (DL-171, 172_FR, 173_FOLD, 174, 175, 186, 187, 188, 191)
| DL | Decided | Verdict | Rationale |
|---|---|---|---|
| 171 Grounding framing + onboarding | Grounding framing, viz, onboarding, Reports use | **CARRY-MODS** | Carry the grounding framing + Reports-graph use; adapt onboarding to the AI-first reveal. |
| **172_FIRST_RUN** orchestration | Curate + sequence first-run prompts | **RENUMBER + CARRY-MODS** | Number collides with Lineage-B **DL-172 (freemium)**. Keep content (reconcile with the AI-first reveal); reassign ID. |
| **173_FOLDED** first-run | Fold strategic chain into the grounding reveal | **RENUMBER + CARRY** | Number collides with Lineage-B **DL-173 (owner-activation)**. The AI-first reveal already folds the chain; consistent. Reassign ID. |
| 174 Optimize reveal | The Ground→Optimize crossing moment | **CARRY-MODS** | AI-first has the reveal; reconcile the crossing beat. |
| 175 Onboarding identity + inference framing | OSLO/Intralign identity, inference reframe, orienting intake | **CARRY** | Compatible with AI-first onboarding. |
| 186 Onboarding consolidation (Mock A) | Continuous "your plan" reveal | **CARRY-MODS** | Reworks DL-171/173; reconcile with the AI-first continuous reveal. |
| 187 First-run activation rework + role capture | Isolate the move, replay reward, capture role at invite/intake | **CARRY-MODS** | Carry role-capture; reconcile the activation piece with **DR-6** (Activated = 2nd act). |
| 188 Post-activation hand-off (unlock→engaged) | The unlock→engaged hand-off | **CARRY** | Directly matches the AI-first freeze→unlock→engaged and **DR-6** milestones. |
| 191 Issue-forward onboarding lead | Hook = issue, confirm act, grounding reward | **CARRY** | Matches the AI-first issue-forward first-run. |

### C. Overview / read structure / vocabulary (DL-176, 177, 178, 189, 190)
| DL | Decided | Verdict | Rationale |
|---|---|---|---|
| 176 Overview anchored tabs, stage-aware | Anchored core + stage-aware tabbed depth | **SUPERSEDE** | DL-189 retired stages and the AI-first went **read-primary**; the stage-aware tabbed Overview is replaced. Record AI-first read-primary as successor. |
| 177 Read vs interpretation vocabulary | Label/prose split rule | **CARRY** | Vocabulary rule still governs copy. |
| 178 Compact confidence hero | Compact the confidence hero | **SUPERSEDE** | Replaced by the Outcome-Integrity masthead; the compaction concern is moot in the AI-first layout. |
| 189 Retire the stage model | Stages are not user-facing | **CARRY** | The AI-first is post-stage; consistent (internal `_planStage` only). |
| 190 Limiter standalone confirmation | Post-issues next move, cap=1, rotation | **CARRY** | The next-move contract (audit RE-7). Carry. |

### D. Grounding web / plan map / graph (DL-179–185)
| DL | Decided | Verdict | Rationale |
|---|---|---|---|
| 179 Grounding web full 1:1 render | Real statements/structure/lineage | **CARRY-MODS** | The richer target; the AI-first grounding map is simpler. Carry as the target render; adapt. |
| 180 Optimize lens two-layer web | Two-layer read on the plan web | **DEFER (post-R2 / optional)** *(ruled 08-04)* | Its substance — where the plan is weak — is already delivered by the issue worklist + grounding map, and under DL-196 the issue layer is the canonical surface for weaknesses across all pillars, making a separate two-layer graph largely redundant. Nice-to-have viz, not load-bearing for R2. Revisit post-R2 only if a visual "optimize lens" proves wanted. |
| 181 Severity colour on optimize marks | Bounded severity colour on optimize lens | **CARRY** | Severity-colour intent carries onto the issue marks wherever they render (worklist / map) — it does **not** depend on the deferred two-layer web (DL-180); the guard still bounds it (orange stays actions elsewhere). |
| 182 Linked-highlight + hover tip on map | Map interaction, both lenses | **CARRY** | Map interaction; adapt to the AI-first map. |
| 183 What-to-strengthen group-by | Group by dimension/document/deliverable | **CARRY** | The AI-first has group-by; consistent. |
| **184 R2 graph schema ratification** | The blocking schema/binding decisions | **CARRY** | **Load-bearing backend.** The graph schema/binding is the data foundation for the map + issue layer. Carry into the R2 data model. Deep-read at implementation. |
| 185 Grounding list group-by + deliverable issue CTA | Group-by + real-issue CTA | **CARRY** | Consistent with the AI-first grounding list. |

### E. Positioning + the integrity model (DL-192–197 + the two drafts) — the core
| DL | Decided | Verdict | Rationale |
|---|---|---|---|
| 192 Positioning (outcome-based risk intelligence) | Category term + credibility framing | **CARRY** | Positioning of record; compatible with the AI-first product. |
| 193 Priority re-anchor | Limiter governs the *read*; integrity de-risk governs the *queue* | **CARRY** | Underpins **DR-4** + the worklist ordering; consistent. |
| 194 (drift stub) | Continuous drift detection | **SUPERSEDE** | Absorbed as **State 2** of the indicator variant below. |
| **194 (integrity indicator, 3-state)** | State 1 (moment-in-time integrity) committed to R2 | **CARRY** *(confirm ratify)* | The ratified spec behind **DR-4a**. State 1 = R2; States 2/3 post-R2. Status was "pending ratification" — **DR-4 effectively ratifies its core; confirm.** |
| **195 Adaptability checkpoint-optimization** | The Adaptability computation (State-1 keystone) | **CARRY** | This *is* the DR-4b computation spec (answers audit OI-3). Key calls owner-ratified; finish the spec. |
| **196 Integrity via issue layer** | All three pillars resolve through the exposure-gated issue layer | **CARRY** | The issue-layer/backend model behind the pillars (answers OI-4). **Not yet in the AI-first prototype → carry + implement.** |
| **197 False-confidence issue type** | Grounding issues = `ISS-FC-<art>` | **CARRY** | The DR-4c Grounding mechanism (answers OI-7). Carry + implement. |
| DRAFT: collapse Outcome-Confidence → Viability | The old single confidence = the Viability pillar | **CARRY / RATIFY** | Consistent with **DR-4** (Viability = the CAF composite). Ratify as part of the DR-4 DL. |
| DRAFT: phased resolution (Inferred→Settled→Resolved) | The phased issue lifecycle | **CARRY / = DR-5** | This *is* **DR-5** (ratified 2026-07-30). Land it + the D088 amendment. |

---

## The number collisions (RENUMBER)

Two Lineage-B rulings share IDs with canon-track DLs:

| Number | Canon-track (earlier) | Lineage-B ruling (newer) | Recommended resolution |
|---|---|---|---|
| **DL-172** | First-run prompt orchestration (07-22) | Freemium value moments / unit=outcome (08-04) | Canon-track keeps 172 (assigned first). **Renumber the freemium DL → DL-198.** |
| **DL-173** | Fold strategic chain into grounding reveal (07-23) | Owner activation = first grounding act (08-04) | Canon-track keeps 173. **Renumber the owner-activation DL → DL-199** (and note DR-6 amends it to "2nd act"). |

*Alternative if you'd rather the strategically-central freemium/activation decisions hold the lower numbers: swap — renumber the two canon-track DLs instead. Mechanical; your preference. Recommendation above keeps chronological assignment.*

---

## Summary (RATIFIED 2026-08-04, Idris)

- **Carry / carry-mods: 28** — the large majority (incl. DL-165 → carry-mods). The canon track is mostly compatible; the work is *implementing* it in the AI-first shell + writing the R2 contracts, not re-deciding.
- **Supersede: 3** — DL-176 (stage-aware Overview), DL-178 (confidence hero), DL-194 drift-stub. Replaced by the AI-first read-primary layout + integrity masthead + the indicator variant.
- **Defer (post-R2 / optional): 1** — DL-180 (two-layer optimize web); redundant with the issue layer + grounding map for R2.
- **Renumber: 2** — the newer Lineage-B pair: **freemium DL-172 → DL-198**, **owner-activation DL-173 → DL-199** (the canon-track DL-172/173 keep their numbers — they're cross-referenced by DL-186/187 and the reveal chain, so renumbering them would cascade; the newer pair is referenced only by this session's artifacts).
- **The integrity core (DL-193/194/195/196/197 + both drafts): all CARRY** and are the ratified specs the audit thought were missing. Carrying them is the single highest-value action — it converts audit blockers OI-3/OI-4/OI-7 into "implement the existing spec."

## Owner ratification — ✅ RATIFIED 2026-08-04 (Idris)
- **Verdicts accepted** as drafted, with the two owner calls ruled:
  - **DL-165 = CARRY-MODS** — explainer intent carries onto the integrity band's pillar-drill; ring visual retired.
  - **DL-180 = DEFER (post-R2 / optional)** — redundant with the issue layer + grounding map; DL-181 severity-colour still carries independently.
- **Renumber = newer pair renumbered:** freemium → **DL-198**, owner-activation → **DL-199**.

*Ratified. This + the six DR rulings (DL-200…205 drafts) are the single source of truth. Product-grill is paused per your note (enhancements first).*
