# R2 Slice 2 — Issue Lifecycle & Grounding Acts — Build Design

*Grill artifact · authored 2026-08-06 · derived from ratified DL-204 (phased-resolution + D088 amendment), DL-205 (route-as-act), D133/CR-2 (evidence≠comment), capabilities #1/#2/#4/#5/#6, audit §4.2 (R2-I1…R2-I8), and the 2026-08-06 owner fixes in `oslo-prototype-r2.html`. Status: **DRAFT — awaiting slice sign-off.** Builds directly on Slice 1's `Issue` object and the reanalysis-only invariant (L13).*

**Scope:** the item/issue **lifecycle** (Inferred → Settled → "Settled — needs a fix" → Resolved), the **grounding acts** that drive it (confirm / flag / fix / route / answer / withdraw), and the **append-only attestation ledger** recording who acted, on what basis, with what evidence. The honesty backbone: a manual act only *enqueues*; only the batch re-read *resolves* (cap #1; D088 amendment).

**Prototype-vs-canon correction this design lands (audit R2-I2):** the prototype historically treated `you` (grounded) and `fixed` (plan-changed) as mutually-exclusive terminals, so a confirmed-yet-infeasible item could read "Resolved" — the false-confidence failure DR-5 exists to kill. The 2026-08-06 owner fixes added the **flag fork** (`_needsFixItems`/`_needsFixGroup`/`fixFromFlag`) and made `_syncArtFromItem` keep a flagged item's linked statement `inferred`. This design ratifies that fork as the canonical lifecycle.

**Second correction, symmetric to the first (owner 2026-08-06):** a **mitigated** item (`fixed` — a plan change was drafted) was still landing in the **Resolved** tray with a closure (✚) icon, even though its figure is *still OSLO's inference* and it does not firm Grounding until separately grounded. A user chasing Sound grounding was thus told an incomplete item was done. The fix routes **both** partial states — needs-a-fix (a flag with a Viability gap) **and** needs-grounding (a mitigation with an ungrounded figure) — out of Resolved into a single shared catch-all folder, **"Acted on · not yet closed"** (`_needsFixItems`/`_needsFixGroup` generalized; `_nfKind(it)` returns `'fix'` for a flagged item, `'ground'` for a mitigated one). Resolved now holds **only** genuinely-closed items (`you`+`!flagged`, firmed Viability checkpoints). The governing presentation invariant: **a mitigated-but-ungrounded item never reads as closed.**

---

## 1. Locked decisions

| # | Decision | Tag / Source |
|---|---|---|
| L1 | Lifecycle = **Inferred → Settled → "Settled — needs a fix" → Resolved.** | ratified-DL · DL-204 §1 |
| L2 | **Only re-analysis moves an item to a resolution state** — the click handler only enqueues. | ratified-DL · DL-204 §2 (D088); cap #1 |
| L3 | A **flag** is **Settled-but-needs-a-fix**; resolves only via a *fix* that closes it, or a *confirm-with-evidence*. | ratified-DL · DL-204 §1; owner 2026-08-06 (`fixFromFlag`) |
| L4 | A flag **credits Grounding at the item level but NEVER firms Viability** — the linked statement stays `inferred`. | Locked · owner 2026-08-06; Slice 1 L11 |
| L5 | **A fix firms Viability but does NOT fabricate Grounding** — the figure stays inference until separately grounded. | Locked · cap #6 |
| L6 | **BASIS is a defined enum:** `documented \| vendor-or-owner-verified \| verified-directly \| answered`. | ratified-DL · cap #2; resolves R2-I3 |
| L7 | **FLAG is a first-class ledger attestation** — recorded symmetrically with confirm. | Locked · resolves R2-I7; D133 |
| L8 | **Withdraw appends, never erases** — a withdrawal is a NEW event that rolls back live state; prior retained. | Locked · cap #2; resolves R2-I4; DL-L9 |
| L9 | **Evidence ≠ comment** — a comment can never ground the read or resolve an issue. Structural. | ratified-DL · D133/CR-2; cap #4; resolves R2-I6 |
| L10 | **A route counts as a grounding act** on the same `grounding_act` stream; a reviewer answer enqueues like the user's own call. | ratified-DL · DL-205 §3; resolves R2-I5/R2-I8 |

---

## 2. State Model

| Phased state | Proto state | Meaning |
|---|---|---|
| **Inferred** | `inf` | Open; rests on OSLO's inference. |
| **Settling** (enqueued) | `addressed` | Act recorded; optimistic in tray, **stale** until the batch runs. `addr.kind ∈ {confirm, flag, option, fix}`. |
| **Routed** | `routed` | Handed to a reviewer; `routedTo` set. Inference until they answer. |
| **Resolved · grounded** | `you` (`!flagged`) | Truth known + evidenced; linked artifact → `prov:'you'`. The **only** issue terminal that reads as closed. |
| **Acted on · needs grounding** | `fixed` | Plan changed; Viability firmed. Figure still OSLO's inference — **not Resolved** until grounded. Renders in the "Acted on · not yet closed" folder (`_nfKind→'ground'`), never in Resolved. |
| **Acted on · needs a fix** | `you` + `flagged` | Truth known (Grounding credited) but a Viability gap remains; **not Resolved**. Same folder (`_nfKind→'fix'`). |

**The catch-all folder** ("Acted on · not yet closed", `_needsFixGroup`) holds every item that has been *acted on but is not yet closed* — both partial states above, per-row typed by pillar (a needs-a-fix row shows a **Viability** pill + `fixFromFlag`; a needs-grounding row shows a **Grounding** pill + `groundMitigated`). Its count reads "N to fix · M to ground". Transient reconcile (`addressed`) rows show "settling…" with no act until the batch lands.

**Transition table** (trigger → guard → effect; "only-reanalysis-resolves" holds throughout):

| # | From | Trigger (fn) | Guard | Effect |
|---|---|---|---|---|
| T1 | Inferred | `itemAct(k,'confirm')` | `state==='inf'` | → Settling; basis+evidence captured; `confirmCount++`; `_scheduleReanalysis()`. |
| T2 | Inferred | `itemAct(k,'flag')` | `state==='inf'` | → Settling; `flagged=true`; enqueue. |
| T3 | Inferred | `itemAct(k,'fix')` / `'option'` | `state==='inf'` | → Settling; plan-change queued; enqueue. |
| T4 | Inferred | `routeTo(k,tier)` | — | → **Routed**; `routedTo` set; enqueue on reviewer reply only. |
| T5 | Routed | `respondRoute(k,verdict)` | `state==='routed'` | → Settling; `attestedBy=reviewer`; `flagged=(verdict==='reject')`; reanalyze. |
| T6 | Settling | `_completeReanalysis→_resolveTransition` | `state==='addressed'` | **Batch re-read** resolves: planFix→`fixed`; else→`you` (flagged stays needs-a-fix). **The only terminal transition.** |
| T7 | Needs-a-fix | `fixFromFlag(k)` | `flagged && state==='you'` | → Settling w/ plan change; routes through reanalysis, never terminal directly (L2). |
| T8 | resolved/settling | `withdrawItem(k)` | `state ∈ {addressed,you,fixed}` | → Inferred; clears flag/basis/evidence/attestedBy; `confirmCount--`; if `fixed`→`_undoPlanChange`; append withdrawal. |
| T9 | Routed | `withdrawRoute(k)` | `state==='routed'` | → Inferred; `routedTo=null`; `confirmCount--`; append. |
| T10 | Resolved·mitigated | `groundMitigated(k)` | `state==='fixed'` | → Inferred + attest gate open (plan change retained, figure re-opened). |
| T11 | Settling | `undoPending(k)` | `state==='addressed'` | → Inferred; cancels the batch if nothing else pending (pre-resolution undo). |

**Invariant:** T6 is the *only* transition into a resolution state. Every click ends at `addressed`/`routed` + `_scheduleReanalysis()`; the debounced batch resolves and steps integrity once (cap #1).

---

## 3. Data / Object model — the attestation ledger
*(Build ON R1's Cognition/User-Acceptance/StakeholderResponse primitives — audit §6 — extend with the basis enum, flag-as-attestation, reversal record.)*

**`Attestation`** (append-only, one per act): `id` · `issueRef` · `act ∈ {confirm,flag,fix,route,answer,withdraw}` · `basis ∈ BASIS` (nullable only for `fix`/`route-pending`/`withdraw`) · `attributedTo` (self | `{name,role,tier}` reviewer — the "Confirmed by you" vs "Confirmed by {name}" class) · `evidenceRef` (nullable; **never** a comment) · `ts` · `supersedes` (nullable; the record it reverses). Never mutated in place.

**`BASIS` enum** (L6; resolves R2-I3): `documented` · `vendor-or-owner-verified` · `verified-directly` · `answered` (**net-new** — a reviewer/clarify answer grounds the item; prototype currently stores `null`). A **flag** attestation carries `act:'flag'` + `attributedTo` + optional `basis` (first-class, symmetric with confirm — L7). A **fix** carries `act:'fix'` + plan-change ref, `basis:null` (firms Viability, does not evidence the figure — L5).

**`Issue` lifecycle fields** (extend Slice 1's `Issue`): `state`, `flagged`, `attestedBy`, `basisNote`, `evidence`, `routedTo`, `fixInfo`, `link`. `_syncArtFromItem` projects item resolution onto the linked statement's `prov`, holding it `inferred` when `flagged` (L4).

**`HISTORY`** — append-only event log; every act, resolution, withdrawal is one timestamped entry, never overwritten (cap #2).

**Withdrawal-as-new-event** (L8; resolves R2-I4): a withdrawal is a NEW `Attestation{act:'withdraw', supersedes:<priorId>}` + a `HISTORY` append; live `Issue` reverts to Inferred; prior records **remain**. Legible, not silent.

---

## 4. Event Model

**A. Grounding-act events (ENQUEUE only — never resolve):** `confirm`, `flag`, `fix`, `answer`, `route`, `withdraw` — each emits on the single durable `grounding_act` stream (DL-205 §2; resolves R2-I5) and calls `_scheduleReanalysis()`. Withdraw also decrements the live gate; the activation *event* stays immutable (DL-205 §4; DL-L9).

**B. Reanalysis-completion event (RESOLVES):** `_completeReanalysis` consolidates the batch, runs `_resolveTransition` per item, recomputes `min(V,G,A)`, steps integrity once. Sole resolver (cap #1).

**Which act moves which pillar** (resolves R2-RE-6 for Slice-2 acts):

| Act | Pillar | Mechanism |
|---|---|---|
| `confirm` (w/ basis) | **Grounding** | item→`you`; statement→`prov:'you'`; `grounded()` counts it. |
| `flag` | **Grounding only** — never Viability | item→`you`+`flagged`; statement stays `inferred` (L4). |
| `fix`/`option`(plan) | **Viability** — never fabricates Grounding | item→`fixed`; `_applyPlanChange`; figure inferred (L5). |
| `answer` (clarify) | **Grounding** (`basis:'answered'`) | may update the underlying value (cap #5). |
| `route`→reviewer confirm | **Grounding**, attributed to reviewer | grounds on their evidence. |
| `route`→reviewer reject | **needs-a-fix** (flag) | `flagged=true`, Grounding-credit only. |

---

## 5. Honesty invariants (testable)
- **INV-1 only-reanalysis-resolves** — the sole terminal transition is `_resolveTransition`, called only from `_completeReanalysis` (L2; D088).
- **INV-2 flag-is-first-class-attestation** — a flag writes a full `Attestation{act:'flag',attributedTo,basis}`, not a bare `flagged=true` (L7; R2-I7).
- **INV-3 flag ≠ Viability** — after a flag, the linked statement stays `inferred`; `artWeak` stays true; Viability unchanged (L4; Slice 1 INV-1).
- **INV-4 comment-never-grounds** — comments push to `comments[]`/`HISTORY` as discussion; no write path to `prov`/`basis`/state; issue stays open (L9; D133/CR-2).
- **INV-5 withdraw-appends-never-erases** — withdraw creates `Attestation{act:'withdraw',supersedes}` + `HISTORY` entry; prior records persist; only live state reverts (L8).
- **INV-6 needs-a-fix-not-Resolved-while-weighing** — a `you`+`flagged` item is excluded from the Resolved tray and appears in `_needsFixGroup`; reaches Resolved only via `fixFromFlag`→reanalysis (L3; R2-I2).
- **INV-7 basis-required-and-typed** — every confirm/answer carries `basis ∈ BASIS`; reviewer-answered sets `answered`, never `null` (L6; R2-I3).
- **INV-8 fix ≠ Grounding** — a `fixed` item's figure stays inferred; grounding requires the separate `groundMitigated` path (L5).
- **INV-9 a-mitigated-ungrounded-item-never-reads-as-closed** *(presentation invariant)* — a `fixed` item is **excluded from the Resolved tray** and renders in "Acted on · not yet closed" (`_nfKind→'ground'`) offering `groundMitigated`; the Resolved tray admits only `you`+`!flagged` (and firmed Viability/Adaptability checkpoints). No closure (✚-in-Resolved) affordance is shown for an item whose figure is still inferred. Symmetric twin of INV-6.

---

## 6. FE ↔ BE integration bindings
*(Reanalysis is the ONLY event that changes a resolution/band — Slice 1 L13, INV-1.)*

| FE surface | Reads (BE) | Written by (act) | Resolved by (event) |
|---|---|---|---|
| Read item card (Inferred) | `openIssues()` `state='inf'` | `decide`/`quickConfirm`/`applyFix`/`routeTo` → enqueue | reanalysis batch |
| Basis picker | `BASIS` enum | `confirmBasis`→`itemAct('confirm',{basis,evidence})` | reanalysis |
| **"Acted on · not yet closed" folder** | `_needsFixItems()` (both kinds; `_nfKind`) | `fixFromFlag` (fix) / `groundMitigated` (ground) / `withdrawItem` | reanalysis → Resolved |
| **Resolved tray** | `state === you(!flagged)` only (+ firmed V/A checkpoints) — **`fixed` excluded** (INV-9) | `withdrawItem` | reanalysis (settle) |
| **Awaiting-evidence group** | `state='routed'` | `respondRoute` / `withdrawRoute` | reviewer reply → reanalysis |
| Withdraw control | `Attestation` history | `withdrawItem`/`withdrawRoute` → append | live state reverts; ledger retained |
| Discussion panel | `comments[]` (isolated) | `postComment`/`cmMention` | **never** changes a band (INV-4) |
| Provenance line ("Confirmed by you/{name}") | `attestedBy`, `basisNote`, `flagged` | resolved-state render | reanalysis |

---

## 7. R1 reuse vs net-new
**Reuse (audit §6, don't re-spec):** attestation primitives (Cognition/User-Acceptance/evidence sub-classes, append-only immutability — the `Attestation`/`BASIS` are columns *on* these); apply-fix path (cap #6, `_applyPlanChange`/`_undoPlanChange`, Viability-firms-not-Grounding); StakeholderResponse seam (DL-049 reviewer-response-as-evidence); comment/@mention objects + "comment never grounds" (R1 WAVE_I) — Slice 2 only enforces the boundary.
**Net-new:** the **"Settled — needs a fix"** state + flag fork (R2-I2); the **BASIS enum completion** (`answered`, typed on every path — R2-I3); **flag-as-attestation** (R2-I7); the **reversal-record contract** across the three shapes `withdrawItem`/`withdrawRoute`/`groundMitigated` (R2-I4); the **act→enqueue→resolve split** as an explicit event contract (D088; R2-RE-6).

---

## 8. Open items / placeholders (later owner ratification)
- **[placeholder] Reanalysis batch window** — `REANALYSIS_DEBOUNCE`/`REANALYSIS_MS` are stubs; the real debounce/cooldown/consolidation-key is audit R2-RE-1, deferred to the batch slice (Slice 3).
- **[owner] `answered` basis strength** — does a reviewer/clarify `answered` rank with `verified-directly` or below it for exposure/provenance display?
- **[owner] Reviewer-reject → flag authority** — does a reject create a flag *attributed to them* with fix-authority routing, or only a Grounding-credit gap? (R2-I8.)
- **[owner] Withdraw → re-analysis** — should a withdrawal trigger a confirming re-read (recommended) so integrity recomputes off the reverted state? (Prototype's `withdrawItem` re-opens live state but doesn't re-analyze.)
- **[carry-forward] Activation-survives-withdraw** (DL-L9/DL-205 §4) — the live gate may re-lock on `confirmCount--`, but the activation *event* is immutable; asserted in the freeze/telemetry slice.
- **[deferred] `groundMitigated` ledger shape** — supersede the fix attestation or append a paired grounding record (lean: append, keep both).

---

## 9. Acceptance criteria
1. **AC-1** Flagging a load-bearing item lands it in the needs-a-fix folder, never the Resolved tray; its linked statement stays `inferred`. (INV-3, INV-6)
2. **AC-2** `fixFromFlag` enqueues a plan change; only after `_completeReanalysis` does the item read `fixed`/Resolved; no click sets the terminal directly. (INV-1, L3)
3. **AC-3** For every act, the item is `addressed`/`routed` immediately and resolves only on the batch; a cancelled batch (`undoPending`) leaves it Inferred. (INV-1)
4. **AC-4** `withdrawItem` reverts live state to Inferred, rolls back the plan change if `fixed`, decrements the gate, and **appends** a withdrawal event; prior records remain in `HISTORY`. (INV-5, L8)
5. **AC-5** `withdrawItem`, `withdrawRoute`, and `groundMitigated` each produce a legible reversal record with the correct live-state effect. (T8–T10)
6. **AC-6** Posting a comment/@mention leaves state, `prov`, basis, and every band unchanged; the issue stays open. (INV-4; D133)
7. **AC-7** Every confirm/answer writes `basis ∈ BASIS`; a reviewer answer sets `answered` (never `null`); a flag writes a first-class attestation. (INV-2, INV-7)
8. **AC-8** A flag raises Grounding's item credit but leaves Viability's band flat. (INV-3)
9. **AC-9** A fix firms Viability but leaves the figure inferred; Grounding rises only via `groundMitigated` + a basis. (INV-8, L5)
10. **AC-10** A routed item shows in Awaiting-evidence until `respondRoute`; a reviewer confirm grounds it (attributed, `answered`), a reject forks it to needs-a-fix — both via the batch. (L10, INV-6)
11. **AC-11** A mitigated (`fixed`) item is **never in the Resolved tray** — it renders in "Acted on · not yet closed" with a Grounding pill and a `groundMitigated` act; the tray's "N settled" count excludes it; only `groundMitigated`→reanalysis moves it toward closure. A user scanning Resolved is never shown an ungrounded item as done. (INV-9, INV-8)

---

*Slice 2 of the R2 delta. Depends on Slice 1's `Issue` object + reanalysis-only invariant; feeds Slice 3 (grounding-act batch window) and the freeze/activation slice (DL-205, DL-L9). On sign-off, the flag-fork + BASIS corrections **and the symmetric mitigated→needs-grounding fork** (the "Acted on · not yet closed" catch-all, owner 2026-08-06) already in `oslo-prototype-r2.html` become the ratified reference implementation. Verified green: `_S10` = 59 checks, `needsFixFork` + `mitigatedNeedsGrounding` both true, no page errors.*

---

## Addendum — DL-211: proposal-resolution model + cross-surface resolution sync (ratified 2026-08-09)

A finding and the proposal(s) that resolve it are **one object**; resolving from any surface writes the one finding through the single reanalysis path.

- **Proposals are three kinds.** **Build** — adds a missing structural element (task, owner, deadline, KPI, requirement); accepting is a *build act* that resolves the structural finding and may firm Viability/Adaptability via reanalysis. **Inference** — accept OSLO's guessed value/assumption; **additive**, grounds nothing (the Grounding finding resolves only by *verifying* the real value — the only-verify-moves-Grounding invariant). **Optional** — rounds out the plan; additive.
- **Cross-surface sync.** Accepting a build proposal from the issue card, the artifact, or the folded read row marks the same resolver accepted (shared state); the finding closes when **all** its build-resolvers are accepted, through reanalysis (only-reanalysis-resolves). Resolved once, reflected everywhere; a finding is never re-presented after it resolves.
- **Multiple resolvers.** A finding may require several resolvers (e.g. a backup needs both its *requirement* and its *task*); partial acceptance keeps it **honestly open**; it resolves only when the last resolver lands.
- **Itemized atomic findings.** Findings render as individual, independently-resolvable rows under a shared container — **never merged into one prose row** (which cannot show one resolving while its sibling stays open). Load-bearing-gated; distinct from DL-210 precedence-deferral.
- **Amends `proposalsFoldedIntoRead`.** The additive / no-band-move invariant holds for inference and optional proposals; **build proposals resolve their finding and may firm the band** (a real user-accepted structural change — not manufactured confidence).

**Acceptance (server twins):** `buildProposalResolvesFinding` (GT-51) · `inferenceProposalStaysAdditive` (GT-52, pinned) · `resolutionSyncedAcrossSurfaces` (GT-53) · `findingsItemizedNotMerged` (GT-54, pinned). Realized in `oslo-prototype-r2.html` (`_REQ_RESOLVERS`/`_acceptedResolvers`/`_allResolversAccepted`, `resolves` on build proposals; `_S10` = 82). See `canon/decisions/DL-211_PROPOSAL_RESOLUTION_MODEL_AND_CROSS_SURFACE_SYNC.md`.
