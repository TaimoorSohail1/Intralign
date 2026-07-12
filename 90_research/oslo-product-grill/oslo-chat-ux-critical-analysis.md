# OSLO Chat — UX Critical Analysis (post-D108), benchmarked against leading AI applications
Date: 2026-07-09 · Scope: the chat integration now live in Slices 2–8. Severity: **S1** blocks · **S2** meaningful · **S3** polish.

## Where it now stands (after D108)
Chat works, is state-grounded, has a context pill, and is reachable from Overview (Ask why), Issues (Ask about this issue), Recommendations (**Discuss**), the artifact editor (span/artifact ask), the Attention map (cell ask), and History (what changed in this run). Clarifications route through one shared path that produces byte-identical History entries. Advisory-only holds: chat never mutates, never selects a path, never resolves an issue. **That is a strong, correctly-governed foundation** — most AI features in enterprise tools fail precisely on that governance boundary.

The gaps below are what separates "a chatbot bolted onto an app" from "an AI-native advisory surface."

---

## S1 — The credibility gaps

### 1. Replies are keyword-routed templates — users will hit the "it didn't understand me" wall fast
Intent routing is keyword-based, with a generic summary fallback. Anything off-script (e.g. *"Which is riskier, the Wi-Fi or the keynote backup?"*, *"Draft me a message to the venue"*) collapses to a canned summary that **looks** like an answer but isn't. This is the single fastest way to destroy trust in an AI surface.
- **Fix:** make the fallback *honest and capability-scoped* rather than a fake answer: "I can't answer that yet. Here's what I can do: explain the read, compare resolution paths, explain an issue or artifact, tell you what changed in the last run." Never fabricate. (This is also the prototype-honest position — the real build has a model behind it; the *contract* is what we're specifying.)

### 2. Replies don't carry OSLO's own epistemic qualifiers — the product's biggest differentiator is missing from its AI surface
OSLO's entire doctrine is that every read is **reliability-qualified**, and that content is either **From OSLO (derived)** or **Confirmed by you (attested)**. Chat currently answers in flat, confident prose. It should inherit the epistemics:
- Qualify answers by reliability ("Reliability is Moderate — this rests on the documents you gave me, so treat it as directional").
- Distinguish derived vs attested when it asserts a plan fact.
- Say when evidence is thin *rather than* answering confidently.
**This is the highest-leverage improvement available.** Leading AI products are converging on exactly this (visible grounding + calibrated uncertainty); OSLO already has the model for it and simply isn't using it in chat.

### 3. No citations / provenance in replies
Best practice in every serious AI-assisted product now: **every claim is traceable**. OSLO has the evidence (`ev[]` on each issue, artifact spans, history events) but replies don't cite it. A reply about the Wi-Fi issue should cite *"Resources · Vendors: 'must confirm 500-person Wi-Fi capacity'"* as a clickable chip.

---

## S2 — AI-native interaction patterns that are absent

### 4. No streaming / thinking affordance
Replies appear instantly and fully-formed. Counter-intuitively this feels *less* trustworthy — users get no sense the system "read" anything. Standard now: token streaming plus a brief "OSLO is reading your plan…" state. (Cheap to simulate convincingly in the prototype.)

### 5. No message-level actions
Missing the table stakes: **copy**, **retry/regenerate**, **thumbs up/down**, and (for a governed product) **"save this to History / to the issue"**. Feedback capture is how AI products improve; a governed product also needs the option to make a chat insight part of the record.

### 6. No conversation persistence
The thread appears ephemeral. In a product where understanding accrues over time (and History is append-only by doctrine), a conversation that vanishes on reload is doctrinally odd. Persist per project.

### 7. Single-context only, and no way to reference things
The context pill holds one thing. Users think comparatively ("compare these two issues", "how does Resources affect Schedule?"). Two emerging patterns worth adopting:
- **Multi-context** — pin more than one item.
- **@-mention to pull a surface into context** (`@Resources`, `@ISS-01`) — now a standard affordance for grounding a question in a specific object.

### 8. Suggested prompts are state-derived but not *follow-up* aware
Chips reflect app state (good) but don't adapt to the last answer. Best practice: after each reply, offer 2–3 **contextual follow-ups** ("Compare this with the other path", "What evidence supports this?", "What would move Feasibility?").

### 9. Chat is a fixed narrow rail
No expand/full-width mode. For an advisory conversation with tables, comparisons, and evidence, a 340px rail is cramped. Offer an expanded/focused mode.

### 10. Proposed actions should state their consequence
Chat offers action links (good, human-in-the-loop). Best practice is to make the **consequence explicit** at the point of action: "Apply this fix → drafts the change into Resources; your read updates after the analysis run." Right now the link is bare.

---

## S3 — Polish
11. **Answer formatting** — lead with the "so what," then the detail; keep replies scannable. Long prose blobs in a narrow rail don't get read.
12. **Keyboard** — ⌘K to focus chat; ⌘Enter to send; Esc to clear context.
13. **Proactive but not naggy** — OSLO may raise clarifications in chat; it must respect the proficiency-sunset principle (§6.9) and never nag.
14. **Empty state should teach** — show 3 example questions rather than a generic greeting.
15. **Advisory boundary copy** — keep it in ONE home + hover (§6.7); don't reprint the disclaimer on every reply.

---

## Anti-pattern to actively avoid
**Chat-washing.** The temptation with a working chat is to route everything through it. OSLO's canonical surfaces (Overview · Attention · Issues · Artifacts · History) must remain the primary way to work; chat *augments and explains* them. The current design gets this right — protect it. Chat should always hand the user **back** to the surface that owns the action.

## Recommended priority
1. **Epistemic replies** (#2) + **citations** (#3) — turns chat from a generic assistant into *OSLO's* advisor, and is unique to this product.
2. **Honest capability-scoped fallback** (#1) — protects trust.
3. **Streaming/thinking affordance** (#4) + **message actions** (#5).
4. **Follow-up suggestions** (#8), **@-mention + multi-context** (#7), **expand mode** (#9), **consequence-stating actions** (#10).
5. **Persistence** (#6) and polish.

## Canon notes
Nothing here changes ratified canon. Reliability-qualification, derived-vs-attested, advisory-only, and "issues close only via an analysis update" are all *already* canon — the recommendation is that **chat should honor them explicitly**, which strengthens rather than stretches the doctrine.
