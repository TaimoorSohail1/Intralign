# OSLO Chat — Integration Gap Analysis (cross-cutting; introduced Slice 2)
Date: 2026-07-09 · Scope: the OSLO chat rail across the cumulative build (latest = Slice 8). Severity: **S1** blocks · **S2** meaningful · **S3** polish.

## Headline finding — chat is non-functional
The chat rail today has exactly three functions: `toggleChat()`, `pushChat()`, `seedChat()`. That is: OSLO can *push* messages **to** the user, and the user can hide the panel. Nothing else.

- The composer `<textarea>` has **no id, no handler, no keydown binding**.
- The **Send button has no `onclick`** — it is completely inert.
- There is **zero** send / reply / simulated-response logic anywhere in the file.

**So OSLO chat is a read-only notification feed with a dead input box.** The user cannot ask OSLO anything — which undercuts the product's core premise ("OSLO reads and explains; you decide") and contradicts canon, where chat is an **always-available surface** ("inline diagnostics · **ask OSLO** · orientation") and the Chat spec calls for a "global persistent panel **+ engage in context from a finding**."

## S1 — Blocking

1. **No conversation at all.** Wire the composer + Send: the user sends a message, OSLO replies (simulated, grounded in current state — confidence band, reliability, open issues, the active artifact). Enter to send, Shift+Enter for newline. Without this, the whole surface is decorative.

2. **No "engage in context" from anywhere.** Canon explicitly requires engaging chat *from a finding*. Today no surface hands context to chat. Nothing in the app says "ask OSLO about this."

## S2 — Meaningful (the integration the workflows actually need)

3. **Issue Panel → Ask / Discuss.** An issue should offer "Ask OSLO about this issue" — chat opens with that issue as context and OSLO explains the why, the evidence, and the trade-offs between resolution paths.

4. **Recommendations → Discuss.** The v4 workflow lists recommendation actions as *Accept · Modify · Reject · **Discuss** · Apply · Share for review*. **Discuss is missing entirely.** A resolution path should be discussable in chat before the user commits to a Selected Path.

5. **Artifact editor → ask about a span/section.** From an annotation (or the artifact toolbar): "Ask OSLO about this" — chat opens with the artifact + weak span as context. This is the natural bridge between *seeing* a weakness and *understanding* it.

6. **Confidence read → ask why.** From the Overview confidence card / "how this is calculated": "Ask OSLO why" → chat explains the current read (which dimension is the limit, what reliability rests on, what would move it). Today the user can read a tooltip but not interrogate the read.

7. **Attention map cell → ask about it.** A heatmap cell should be able to hand its artifact×dimension context to chat.

8. **No context indicator.** Chat needs a visible "what are we talking about" pill (e.g. *Context · ISS-01 · Resources*) with a way to clear it — otherwise contextual answers are ambiguous.

9. **Clarification requests should be conversational.** OSLO *asks* the user questions (clarifications). Today that only happens inside the Issue Panel. Chat is the natural place for OSLO to raise them and for the user to answer — and the answer must still flow to the same project-info update + History entry.

10. **Chat must not become a side-channel that bypasses governance.** Anything decided in chat (answering a clarification, choosing a path) must route through the same state + land in **History**. Chat *advises and offers actions as links*; the user still acts. Chat must never mutate the plan or resolve an issue on its own (advisory-only, D001; issues close only via an analysis update).

## S3 — Polish
11. **Suggested prompts / quick chips** ("What should I do next?", "Why is Feasibility low?", "Explain this issue") — chat is currently undiscoverable as an interactive surface.
12. **Empty/first-run state** for the chat rail.
13. **Message affordances** — OSLO replies should be able to link to the surface they reference (open the issue, open the artifact) rather than describing it in prose.
14. **Accessibility** — composer labelled (it is), but the message list needs live-region semantics so replies are announced.

## Recommended integration plan
1. **Make chat work** (S1): composer + Send + simulated, state-grounded OSLO replies; advisory guardrails.
2. **Context handoff + context pill**: one shared `askOslo(context)` entry point.
3. **Wire the entry points**: Issue Panel ("Ask about this issue"), Recommendations (**Discuss**), artifact annotation/toolbar ("Ask about this"), confidence card ("Ask why"), Attention cell.
4. **Clarifications in chat** (raise + answer → same update + History entry).
5. Polish: suggested prompts, reply→surface links, empty state, live region.

## Canon notes
- Chat is an always-available surface (CAF overlay · **OSLO chat** · MRI) per the v4 workflow.
- "Discuss" is a canonical recommendation action and is currently absent.
- Advisory-only (D001): chat explains and recommends; it never acts. Issues close only via an analysis update (D088). Anything decided in chat is recorded in History (D096).
