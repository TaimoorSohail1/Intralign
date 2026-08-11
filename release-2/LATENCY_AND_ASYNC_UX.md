# OSLO R2 — Latency & Async UX Requirements

*The prototype (`oslo-prototype-r2.html`) simulates every backend interaction as instantaneous. In production, three sources of delay — **Fast Pass analysis**, **Deep Pass analysis**, and **LLM/connector round-trips** — introduce lag that shapes UI behavior. This document inventories every surface where that lag requires a UX enhancement so the wait reads as intentional, honest, and calm — never as frozen or broken.*

**Already handled (do not re-spec):** the act → reanalysis loop (Slice 3) — "recorded · pending reanalysis" + Undo, the band "updating…" flash, and the durable "your read moved" banner. This doc covers everything *else*.

**Honesty extension:** OSLO's spine already says *recorded ≠ resolved* and *only reanalysis moves the read*. Latency UX is the same principle applied everywhere: **"working" must never read as "done."** Never show a band as moved before reanalysis lands, never show *sent / filed / paid* before the server confirms.

---

## 1. The four latency classes and the pattern each demands

- **A · Fast Pass analysis** (intake → first read, target ≤60s). → *Staged progress + skeleton read*; progressive artifact reveal; a degrade/provisional message if it runs long.
- **B · Deep Pass analysis** (background, minutes, supersedes). → *Non-blocking ambient indicator* + a "your read was refined" supersession notice on landing. Never blocks interaction.
- **C · LLM text generation** (chat, report drafts, fix/option drafting, rationale, narrative). → *Thinking indicator → token streaming*; input disabled while generating; cancel affordance; timeout→retry.
- **D · Network / connector round-trips** (route, share, export render, PM-tool push, checkout, feedback file). → *Action-pending state → async confirmation with a server id/result*; explicit error + retry; the action disabled while in flight.

Plus three cross-cutting requirements (§3): error/timeout/offline states, double-submit prevention, and the optimistic-vs-server-authoritative distinction.

---

## 2. Surface-by-surface inventory

### Intake → first read — Fast Pass (Slice 3 / 5)
- **The analysis wait itself.** Today the reveal is a timed animation; drive it from real Fast-Pass completion. Show **staged progress** ("reading your plan → extracting outcomes → assessing viability, grounding, adaptability → preparing your read") over a **skeleton read**, revealing artifacts progressively as they land.
- **Degrade path.** If it approaches the ceiling or over-budget, show "still working — preparing a provisional read" and stamp the result **Provisional** (ties to Slice 3 degrade-to-fit). Never a blank spinner that could hang.
- **The confirm/outcome reveal card** must be gated on the Fast-Pass outcome + rationale actually being ready, not a fixed delay.

### Deep Pass refinement (Slice 3)
- A quiet **ambient "deeper read in progress"** indicator, non-blocking — the user can act while it runs.
- On landing, a **"your read was refined"** supersession notice (sibling to "your read moved"), attributing what changed. Must never silently rewrite the read under the user's cursor.

### OSLO chat / reasoning rail (Slice 2 surfaces; your example)
- Send → **animated "OSLO is thinking…"** indicator, then **stream the response** token-by-token rather than popping the whole answer.
- **Disable/queue the input** while a response is generating; offer a **stop/cancel** for long answers; **timeout → graceful error + retry**.
- Reference chips resolve as/after the stream completes.
- Distinguish **"answering" vs "preparing a change"** — when a chat turn will propose a plan action, its pending state should read differently from a plain answer, and the resulting act still flows through the recorded→reanalysis loop (never an instant read change from chat).

### Fix / option / clarify drafting — LLM (Slice 2)
- **`fixFromFlag` / apply-fix**: OSLO drafts the plan change with an LLM. Show **"drafting your fix…"** before the mitigated/celebration state appears; then the normal reanalysis loop.
- **Option/path generation**: "OSLO is working out your options…" before the choices render.
- **Clarify answers**: same pending treatment before the item updates.

### Reports (Slice 7)
- **Executive Briefing generate / regenerate**: "drafting your briefing…" with **streamed draft**; a spinner on regenerate; **autosave-pending** indicator on edits.
- **Generated reports** (Outcome Readiness / Assumptions / Decision Record): **skeleton on open** while the projection computes; the **depth toggle → Full** may recompute → loading state.

### Export & hand-off (Slice 7)
- **Reanalyze-if-pending is a two-phase wait**: `_exportGuard` re-reads first → "re-reading for currency…" **then** "generating your export…". The user must see both phases, not one long opaque spinner.
- **PDF render**: "preparing your PDF…" → download-ready state.
- **PM-tool hand-off (Asana/etc.)**: "pushing to [tool]…" with **per-task progress** and an explicit **success/failure + retry** — connector calls fail and must not fail silently.
- **Copy summary**: near-instant, but confirm "copied."

### Multi-outcome (Slice 5)
- **Ranking rationale** generation rides on the Fast Pass (see Intake). **Primary edit → downstream re-flag → reanalysis**: optimistic mark + pending, resolved on the batch. Disclosure nudge is client-state (no latency).

### Collaboration (Slice 6)
- **Route to reviewer (`routeTo`)**: delivery is an async network send. "Sending your request to [name]…" → "Requested — awaiting them," **confirmed by the server** (handle delivery failure + retry). The awaiting-evidence *state* exists; the **send latency** is new.
- **Share**: creating the snapshot is a server op → "creating a view-only link…"; copy-link confirm; add-recipient may send an invite (latency); revoke confirm. All need failure paths.
- **Invite (k-factor)**: OSLO drafts the invite → "drafting your invite…"; then send latency.
- **Roll-up / grounding-map**: opening computes a projection over the whole read → **skeleton/loading** for large plans.

### Freemium / checkout (Slice 4)
- **Checkout (`_commitPay`)**: real hosted checkout (external provider). **Blocking modal** with "processing your payment…", **submit disabled** (no double-charge), success → "unlocking [capability]…" (the entitlement grant may lag the payment), failure → clear error + retry.
- **Archive / reactivate**: server op → pending + confirm.

### Feedback / survey (Slice 8)
- **Submit feedback**: egress-sanitize + tracker delivery → "filing your feedback…" → "Filed" **with the server-minted ticket id** (the "Filed this session" list depends on the round-trip). Handle failure.
- **Submit survey**: save → confirm (minor).

---

## 3. Cross-cutting requirements (apply to every async surface)

- **Error / timeout / offline states.** The prototype never fails; production will. Every async action needs a failure message + retry, a timeout, and an offline behavior (queue acts, block server-authoritative ops gracefully). This is the single biggest gap — it's absent everywhere today.
- **Double-submit prevention.** Disable the control while its op is in flight — send, commit-to-pay, export, route, submit-feedback. Especially anything that charges, delivers, or creates a durable record.
- **Optimistic vs server-authoritative.** Acts are optimistic (already: recorded → resolved on the batch). But **checkout, export, share-create, feedback-file, reviewer-send are server-authoritative** — show blocking/pending progress and wait for the server's truth; never fake success. Keeping these two classes distinct is what preserves the honesty spine under latency.

---

## 4. Where this plugs into the build

- These are **front-end enhancements that ride on the Slice 9 FE↔BE integration map.** Recommend adding one column to that map — **"async state / latency treatment"** (idle · pending · streaming · error) — so every dynamic surface declares its loading behavior, held to the same rule as the rest of the map (a surface without a declared async state isn't shippable).
- **Slice 3** owns the analysis-latency *mechanics* (Fast/Deep passes, degrade-to-fit); this document is the *UI* side of those, plus the LLM- and connector-round-trip surfaces the slices currently treat as instant.
- Worth a few new acceptance guards: e.g. *no server-authoritative surface shows success before confirmation*; *chat shows a thinking/streaming state before a response*; *a plan act never moves a band before reanalysis*. These extend the existing honesty guards into the latency dimension.
