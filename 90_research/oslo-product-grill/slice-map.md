# Slice Map — OSLO R1 (high-level, APPROVED 2026-07-09)

> **Amended 2026-07-20:** **Slice 11 — Execution-Ready Planning & Export** added (realizes DL-145→151; owner-approved as its own slice, boundaries A/B). See it below Slice 10.

**Baseline:** `oslo_r1_experience_mockup_v4.html`. Fat vertical slices. Each is a complete module with multiple related features and all major use cases. Prototypes are cumulative (Slice N prototype = Slices 1…N). Actors: **U** User (PM) · **S** System · **AI** OSLO analysis/chat · **C** Collaborator/Viewer.

### Slice 1: Access & Onboarding  ·  *R1 = Alpha, invite-only (D021)*
- Invite-gated Alpha access / account activation / welcome (simulated) — U, S
- Choose start method: Upload · Describe · Templates (5) · Sample *(all phases, user-initiated — D030; Guided Q&A out, D023)* — U, S
- **[GA-phase]** Anonymous first run (no-signup Fast-Pass-only) + save-to-keep — U, AI, S
- **[GA-phase]** Save-to-keep gate after orientation (signup) + claim-through — U, S
- One-time strategic-chain orientation + advisory framing (all phases) — U, AI
- Session management / logout + illustrative persistence — U, S

### Slice 2: Intake & Fast-Pass Orientation
- Provide evidence (paste/upload/template/guided) → synthesized artifacts — U, AI, S
- Fast Pass ≈60s (Extract·Infer·Construct·Evaluate) — AI, S
- In-flow interstitials + streaming trace — S
- 60-second orientation lands on MRI/Overview — U, AI
- Deep Pass auto-runs (non-blocking) and supersedes — AI, S
- Analysis-state honesty (Still updating ↔ current, error/last-good/retry) — S

### Slice 3: Project Overview & Understanding Console  ·  *v4: confidence-led redesign (DL-096)*
- Confidence focal score + meaning line + reliability qualifier (ring/green box/pills removed) — AI, U
- CAF **maturity bars** (Clarity·Alignment·Feasibility; 5-band word + hover; lowest = "the limit") — AI
- Quiet change-delta trend + "Why" disclosure — AI
- Reliability qualifier (Coverage·Evidence·Assessability) + false-confidence flag — AI
- "Start here → top issue" + Progress ledger — U, AI
- Recommendations summary (pointer into Issue panel) + collapsed "More" (Project summary) — AI

### Slice 4: Attention Map (MRI)
- Heatmap (plan-section × CAF), field view secondary — AI, U
- Cell → findings routing (openFindingsFor: single→finding, else scoped list) — U, S
- Severity coloring on cells; neutral confidence elsewhere — S
- Co-primary vs nested placement (see C-001) — U

### Slice 5: Plan Sections / Artifact Workspace
- Explorer of 7 plan artifacts; artifact editor (prose / type-aware tables) — U
- Live edit + autosave + event-driven reanalysis (Saved→stale→Reanalyzing→Up to date) — U, AI, S
- Inline weakness annotations (severity ramp) + hover → Finding panel — U, AI
- Epistemic notation (From OSLO / Confirmed by you) — U, AI
- Weakness stepper (jump to weakness k of N) — U

### Slice 6: Issues & Recommendations (Panel Model)  ·  *v4: "Issues" label (DL-095)*
- All-issues list + filters (section / dimension / severity) + "By dimension / By severity" toggle — U
- Issue Panel (Header→Why→Evidence→CAF impact→Recommendations→History→Reanalysis) — U, AI
- Lifecycle **Open → Addressed → Resolved** (Acknowledge removed, DL-094; never resolved by hand) — U, AI, S
- Resolution paths → Selected Path (Attested); single-action **"Apply this fix"** → reanalysis resolves issue — U, AI
- Clarification Requests (OSLO asks; you answer → reanalysis) — U, AI
- Empty states (four honest distinctions) — S

### Slice 7: History & Confidence Trend
- Append-only timeline (analysis runs, versions, lifecycle, selected path, comments) — S
- Confidence/reliability trend sparkline (direction-only; can fall = better understanding) — AI
- Confidence stages (Orientation ▸ Expanded ▸ Validated) — AI
- Current/prior labels; last-good preserved — S

### Slice 8: Multi-Project Workspace & Awareness
- Workspace Home / Dashboard (Pinned + Recent, per-project status incl. stale) — U, S
- Project switcher + three-context shell + command palette (⌘K) — U
- Notification / awareness panel (routes-to-source, never triggers reanalysis) — U, S
- Settings (Account, Profile, Workspace, Defaults, Collaboration, Notifications, Subscription, Billing, Integrations, Membership; visibility-first) — U
- Appearance (dark/light toggle) + accessibility controls — U

### Slice 9: Collaboration, Sharing & Export (Alpha-scope)
- Sharing dialog (Owner/Collaborator/Viewer + view-only snapshot link) — U, C
- Threaded comments / @mentions on findings (append-only; never change assessment) — U, C
- Export / share-out (currency marker + required disclaimer; Free = PDF-only) — U, S
- *CRR (CAF Review Requests virality loop): OUT OF SCOPE — escalated spec gap.*

### Slice 10: Tiering & Limits (visibility-first)
- At-cap upgrade-or-archive modal (non-destructive archive frees slot) — U, S
- Persistent quiet "Free · Upgrade" chip — U
- Settings → Subscription (plan/usage as facts) — U
- Save-to-keep + anonymous cap (Fast-Pass-only) — U, S
- *All tier numbers/prices illustrative (owner-TBD); billing/enforcement deferred.*

### Slice 11: Execution-Ready Planning & Export  ·  *NEW 2026-07-20 — realizes DL-145→151*
- Authored, graded task model — Work breakdown as a task tree (workstreams → tasks → subtasks; From OSLO until confirmed; neutral `low confidence` grade) — AI, U
- Task-altitude assessment — task-level findings on the deeper read (ISS-10 undated-freeze, ISS-11 inferred-breakdown), via the existing issue engine — AI
- Sequencing + **computed critical path** (`_criticalPath`; From OSLO; outside editable plan content) — AI
- The **eighth "Full plan" consolidated view** — execution readiness (named validation-progress state, non-blocking) · critical path · confirm-before-hand-off · the consolidated plan (14 tasks × 5 workstreams) — U, S
- **Structured Asana export** — mapping preview → simulated hand-off; only the plan crosses, OSLO's analysis stays in OSLO; provenance as an OSLO-owned custom field + OSLO Task ID anchor; tag fallback (free-tier) — U, S
- **Execution-ready identity** (DL-145): OSLO both authors & certifies; readiness = coverage of the execution-critical set → a named state, never a will-succeed verdict; export non-blocking — doctrine layer
- *Boundaries (owner-accepted 2026-07-20): task-tree editing mechanics → Slice 5; generic share/reader-export → Slice 9 (D107, distinct object). Execution MONITORING (Execute → In execution → Outcome) is a future phase, out of R1.*

---

**Note on ordering:** Slices 3, 4, 5, 6 are the descriptive-model core and could be sequenced tightly. Slices 8–10 are shell/scope wrappers already present in the v2 mockup, delegated as fat slices.

## Approval request

Do you approve this high-level slice map?

**Recommended answer:**
Yes, approve this slice map and start Slice 1.
