# Release 1 Application / Platform Classification Decision 001

**Document Type:** Governance Classification Decision · **Status:** **Ratified with Conditions under DL-043 (2026-06-04)** · **Date:** 2026-06-03
**Authoritative Inputs (accepted; not re-opened):** Cognitive Responsibility Architecture · Runtime Ownership Update · Runtime Object Model · Runtime Behavior Model · Contract Inventory · Contract Generation Plan · QA Governance · Observability Governance · Runtime Environment Constraint Profile · Release 1 Capability Coverage Review v1.

> **Mode:** independent governance & architecture review board. Purpose is **not** to redesign OSLO, but to determine which Release 1 capabilities belong inside the **governed OSLO contract domain** (and therefore require contracts) versus the application/platform shell, commodity infrastructure, or deferred scope. **Challenge assumptions; identify over-engineering; prevent unnecessary governance expansion.** **No** new responsibility, object, plane, layer, runtime/governance concept, service, or architecture is introduced. Per `CLAUDE.md`, **only the owner ratifies.**

> ### ⚠ DL-043 RECONCILIATION (2026-06-04) — supersedes the "Governance"/"User Interaction" rows below
> Under ratified **DL-043** (Integrity-not-Authority + User Acceptance), the classification's **core conclusion holds** (most uncovered capability is platform/commodity, not governed; no P1–P5 governance track). **But the rows that route disposition through *Authority / Wave D / Pkg 003* are superseded:**
> - **Promotion Authorization (Pkg 003) → integrity, not governance.** Authority plane is **inactive in R1**; admission is integrity-gated (Perceive readiness + Retain provenance). Pkg 003-as-governance is **dropped from R1**.
> - **Exposure Decisions / Wave D → out of R1** (Future). No Governance Decision object in R1.
> - **Recommendation/Clarification/Resolution Disposition → reclassified.** In R1 these are **user-acceptance events** recorded as attested project history (User Acceptance Record + Acceptance-Impact Assessment, the **Wave U** capability) — **NOT** an "Authority Governance Decision in Wave D." The matrix's "governed disposition = Authority" cells should read **"user-acceptance attestation + reconciliation (non-governance)."**
> - **Access Control** remains correctly distinct from the (deferred) Authority/exposure plane.
> The §1 matrix rows and §2 "Authority Governance Decision in Wave D" language below are **historical (pre-DL-043)** to that extent; the platform/commodity classification and the "no over-engineering" verdict stand.

---

## Headline Finding

**The Coverage Review's "~32% uncovered" is real as a *product-scope* number but largely *should not* be governed by contracts.** When each uncovered capability is classified, the overwhelming majority is **platform shell (Category C)** or **commodity infrastructure (Category E)** — capabilities that *enable* OSLO but neither perform nor alter cognition and therefore **correctly require no governance-grade contract**. The genuinely governance-relevant part of the gap — the **human disposition decisions** (issue/recommendation/clarification/resolution) — is **already owned by Authority within Wave D**; only the *UI that collects* those decisions is platform.

**Net result:** the governance-domain gap is **not ~32% — it is roughly ~10%**, and it does **not** justify a five-wave P1–P5 platform-contract track. Proposed Wave **P0 (this classification) is necessary; P1–P5 as governance waves are over-engineering and should not be created.** Continue Wave A–E; fold the one governed seam (disposition input) into the existing Wave D.

---

## Deliverable 1 — Classification Matrix

Categories: **A** Cognitive Core · **B** Cognitive Presentation · **C** Platform Shell · **D** Human Interaction · **E** Commodity Infrastructure · **F** Deferred.

| Capability | Category | Requires Contract? | Rationale |
|---|---|---|---|
| **Project Management** | | | |
| Project Creation | C | **No** (implementation) | Enables use; no cognition; doesn't alter cognitive outcomes |
| Project List | C | No | Platform shell listing |
| Project Dashboard | C | No (B for any cognitive widgets it embeds) | Shell; embedded cognitive summaries are Wave-E Disclose, not the dashboard itself |
| Project Workspace | C | No | Container shell |
| Project Metadata | C | No | Platform attributes; not canonical knowledge (Retain owns knowledge, not project chrome) |
| Project Status | C | No | Platform state; **not** Outcome/Confidence (which is cognitive) |
| **Artifact Management** | | | |
| Artifact Workspace | C | No | Shell for viewing/working artifacts |
| Artifact Navigation | C | No | Platform navigation |
| Artifact Editing | C (UI) + **A (trigger)** | UI No; **trigger already Wave A** | Edit UI is platform; the resulting **stale→recompute trigger** is Act/Adapt, already owned in Wave A |
| Artifact Comparison | C | No | Platform view |
| Artifact Organization | C | No | Platform foldering/tagging |
| Version History View | **B** | **Yes (Disclose, Wave E)** | Presents Retain's History Records; consumes governed data |
| **Cognitive Features** | | | |
| Artifact Intake | A | **Yes** (Pkg 001 ✅) | Cognition entry |
| Canonical Knowledge | A | **Yes** (Pkg 002 ✅) | Retain core |
| Findings | A | **Yes** (Wave B) | Infer output |
| Issues | A | **Yes** (Wave B) | Evaluate output |
| Recommendations | A | **Yes** (Wave C) | Advise output |
| Clarifications | A | **Yes** (Wave C) | Advise output |
| Confidence | A | **Yes** (Wave B) | Evaluate attribute |
| CAF | A | **Yes** (Wave B) | Evaluate |
| Outcome Confidence | A | **Yes** (Wave B) | Evaluate |
| Recompute | A | **Yes** (Wave A backbone) | Cross-cutting cognition trigger |
| **Governance** | | | |
| Promotion Authorization | A | **Yes** (Pkg 003 — mandatory, pending) | Authority decision |
| Exposure Decisions | A | **Yes** (Wave D) | Authority decision |
| Recommendation Disposition | A (decision) + D (UI) | **Decision Yes (Wave D);** UI No | Governed disposition = Authority; review UI = platform |
| Clarification Disposition | A (decision) + D (UI) | **Decision Yes (Wave D);** UI No | Same seam |
| **User Interaction** | | | |
| Issue Review | D | **No new contract** (governed decision already Wave D) | UI collects a disposition that Authority governs in Wave D |
| Recommendation Review | D | No new contract | Same |
| Clarification Workflow | D | No new contract | The clarification *response* feeds Advise/Authority (Wave C/D); UI is platform |
| Resolution Workflow | D | No new contract | Resolution disposition = governed state via Wave D; UI is platform |
| **Notifications** | | | |
| Notification Surface | B | **Yes (Disclose, Wave E)** | Presents awareness of governed events |
| Notification State (read/unread/dismiss) | E | **No** | Commodity per-user UI state; no cognition/governance/trust impact |
| Awareness Surfaces | B | **Yes (Disclose, Wave E)** | Presentation |
| **Collaboration** | | | |
| Comments | F | No (deferred) | Not required for R1 cognition |
| Mentions | F | No (deferred) | Deferred |
| Sharing | F | No (deferred; basic invite = E) | Advanced sharing deferred |
| Review Workflow (collab) | F | No (deferred) | Deferred |
| **Reporting** | | | |
| MRI | B | **Yes (Wave E)** | Cognitive presentation |
| Overview | B | **Yes (Wave E)** | Cognitive presentation |
| Exports | B | **Yes (Wave E)** | Presentation; **must honor Authority exposure** (already governed) |
| History Timeline | B | **Yes (Wave E)** | Presentation over History |
| **Administration** | | | |
| Settings | E | **No** | Commodity configuration |
| Preferences | E | **No** | Commodity per-user config |
| Access Control | E | **No** (governance contract) | Identity/permission commodity — **distinct from Authority exposure**; must not be conflated with cognitive governance |
| Authentication | E | **No** | Commodity infrastructure |

---

## Deliverable 2 — Contract Eligibility Assessment

- **Full contract triads (mandatory):** the **Category A** cognitive core (Intake ✅, Canonical ✅, Findings, Issues, Recommendations, Clarifications, Confidence, CAF, Outcome Confidence, Recompute, Promotion Authorization [Pkg 003 pending], Exposure Decisions) and the **Category B** presentation surfaces (MRI, Overview, Version History View, Notification/Awareness Surface, History Timeline, Exports) as Disclose/Render contracts in Wave E.
- **Lightweight platform contracts:** **none required.** Category C shell capabilities do not touch cognition, governed outputs, or invariants; modeling them as governance contracts is over-engineering. They are **implementation concerns** governed by ordinary engineering practice, not the OSLO contract domain.
- **Workflow contracts:** **none as new packages.** The only governance-relevant element of Category D (the **disposition decision**) is already an **Authority Governance Decision in Wave D**. What remains (the review/resolution UI) is platform. *Action:* Wave D's Authority disposition contracts should **explicitly model the user-disposition action as a governed input** to the Governance Decision — a **clarification inside Wave D**, not a new contract.
- **No governance contracts:** all **Category E** commodity (auth, login, password reset, session, preferences, access control, settings) and **Category F** deferred (advanced collaboration/sharing/team admin/advanced notifications). Notification *state* is Category E.

---

## Deliverable 3 — Coverage Recalculation

Measured as **governance-domain** coverage (capabilities that *should* be governed, that *are* covered/planned) — distinct from the Coverage Review's *product-scope* figure.

```text
Cognitive Coverage %        ~95%   (full Category A spine sequenced; Pkg 003 pending)
Presentation Coverage %     ~90%   (Category B surfaces in Wave E)
Platform Coverage %          n/a   (Category C/E are correctly OUT of governance scope;
                                    governance-relevant platform decisions already in Wave D ≈ 100%)
Workflow Coverage %         ~90%   (governed disposition decisions in Wave D; review UI is platform/implementation)
Overall Release 1 (governance-domain) Coverage %  ~90%
```

**Is the previous 68% still valid?** **Yes — as a *product-scope* descriptor** ("how much of the whole product the contract roadmap touches"). **No — as a governance gap.** Of the ~32 uncovered points, roughly **~22 are Category C/E/F** (platform/commodity/deferred) that **correctly need no governance contract**, and the governed remainder (~10) is **already inside Wave D**. The 68% figure should therefore **not drive contract generation**; the governance-domain coverage is **~90%**, with the residual being Pkg 003 + the Wave D disposition-input clarification.

---

## Deliverable 4 — Over-Engineering Assessment

- **Currently at risk of being over-modeled:** the proposed **P1–P5 platform-contract waves** (project shell, identity/access, artifact-management UI, notification state, settings, collaboration). Generating governance-grade triads for these would **expand governance into commodity software** — invariant-bound contracts, QA positive/negative sets, exact-replay observability for *login* and *foldering* — pure over-engineering with no cognition or trust at stake.
- **Currently under-modeled (genuine gap):** the **disposition input seam** — how a user's issue/recommendation/clarification/resolution review action becomes a **governed input** to an Authority Governance Decision. This is governance-relevant and should be **named explicitly in Wave D** (not left implicit), so the human decision enters the audit/replay chain.
- **Do not justify governance-grade contracts:** authentication, login, password reset, session management, user preferences, access control, workspace settings, project CRUD, navigation, comparison, organization, comments, mentions, sharing, notification read/unread/dismiss. *(Note: access control is identity/permission commodity and must remain **distinct** from Authority exposure governance — they are different concerns and conflating them would be an architectural error.)*

---

## Deliverable 5 — Release 1 Roadmap Impact

- **Wave P0 (classification):** **Necessary** — and satisfied by *this* document. It is the gate that prevents the over-expansion below.
- **Waves P1–P5 (platform governance track):** **Should not exist as governance waves.** Reclassify their contents:
  - **P1 Project & App Shell → Category C → implementation concern** (no governance contract).
  - **P2 Identity & Access → Category E → commodity** (no governance contract; kept distinct from exposure).
  - **P3 Artifact Management → Category C (UI) + already-Wave-A (stale/recompute trigger)** — no new governance wave; confirm the trigger is covered by Wave A's Act/Adapt backbone.
  - **P4 Interaction & Disposition → governed decision already in Wave D**; **no new wave** — add an explicit Wave D clarification that user-disposition is a governed input. UI is implementation.
  - **P5 Notification State / Collaboration / Settings → Category E/F** — commodity (no contract) or deferred.
- **Explicitly deferred (Category F):** advanced collaboration, advanced sharing, team administration, advanced notification management.
- **Confirmed proceeding (unchanged):** **Waves A–E** exactly as planned; **Package 003 (Authority Promotion Authorization)** is **Category A, mandatory** and remains pending generation — this classification does not affect it.

**Net roadmap change:** Wave A–E unchanged; **no P-track of governance contracts is created**; one **Wave D clarification** added; all Category C/E capability routed to ordinary implementation; Category F deferred.

---

## Deliverable 6 — Final Recommendation

**Recommended: Option C — treat the platform/commodity capabilities as implementation concerns and continue Wave A–E — with a single explicit carve-out.**

**Justification.** Classification shows the "uncovered 32%" is dominated by capabilities that *enable* OSLO without participating in or altering cognition. The OSLO contract domain exists to make **cognition and its governance** traceable, deterministic, and trustworthy; extending governance-grade contracts to login, settings, navigation, and project CRUD would **dilute governance, multiply low-value artifacts, and contradict the proportionality the architecture implies** (Render is the only acknowledged non-cognitive Service precisely because OSLO is cognition-scoped). The one genuinely governed element in the gap — the **disposition decision** — is **already owned by Authority in Wave D**; it needs *recognition*, not a new wave.

This is **Option C augmented by one carve-out**, not pure Option A or B: Option A (full P-track) is over-engineering; Option B (a subset of platform contracts) still over-commits, because *no* standalone platform governance contract is justified — the only governed seam folds into existing Wave D. Hence Option C + the Wave D clarification.

---

## Deliverable 7 — Proposed Owner Resolution

> **Resolution:** Adopt the classification; continue Wave A–E; do **not** create a P1–P5 platform-governance track.
>
> **Decisions:**
> 1. **Classify** all Release 1 capabilities per Deliverable 1 (A cognitive core; B cognitive presentation; C platform shell; D human interaction; E commodity; F deferred).
> 2. **Governance-domain coverage is ~90%**, not 68%-uncovered; the 68% remains valid only as a *product-scope* descriptor and **does not** drive contract generation.
> 3. **No governance contracts** for Category C (platform shell), Category E (commodity: auth/login/session/preferences/access-control/settings), or Category F (deferred). These are implementation concerns or deferred scope.
> 4. **Access control remains distinct from Authority exposure** — not to be conflated as cognitive governance.
> 5. **Category D disposition decisions** (issue/recommendation/clarification/resolution) are already **Authority Governance Decisions in Wave D**; add an explicit **Wave D clarification** that the user-disposition action is a **governed input** to those decisions. The review/resolution **UI is implementation**.
> 6. **Confirm proceeding:** Wave A–E unchanged; **Package 003 (Authority Promotion Authorization)** is **Category A, mandatory, pending generation**.
> 7. **Defer (Category F):** advanced collaboration, advanced sharing, team administration, advanced notification management.
>
> **Effect:** prevents governance over-expansion; preserves the accepted architecture, ownership, object, and behavior models; produces a defensible Release 1 scope boundary where contracts exist only where cognition or its governance is genuinely at stake.

---

## Success-Criteria Self-Check

Preserves accepted architecture ✅ · Prevents unnecessary governance expansion ✅ (P1–P5 rejected) · Prevents unnecessary contract generation ✅ (Category C/E/F → no contracts) · Distinguishes cognition / platform / commodity ✅ (A/B vs C vs E) · Produces a defensible scope boundary ✅ (governance = where cognition/trust is at stake) · Identifies only genuine governance-grade additions ✅ (Pkg 003 + the Wave D disposition-input clarification — nothing else). **Invents no responsibility, object, plane, or governance concept.**

---

*This Release 1 Application/Platform Classification Decision determines, as an independent governance board, that the Coverage Review's ~32% uncovered scope is largely platform shell (Category C) and commodity infrastructure (Category E) that correctly require no governance-grade contracts — so the governance-domain coverage is ~90%, not a 32% gap, and the proposed P1–P5 platform-contract track would constitute governance over-expansion and should not be created. It classifies every Release 1 capability into the cognitive core (A, full triads), cognitive presentation (B, Disclose/Render), platform shell (C, implementation concern), human interaction (D, whose governed disposition decisions already belong to Authority in Wave D while the UI is platform), commodity infrastructure (E, no governance contract, with access control kept distinct from Authority exposure), and deferred (F). It recalculates coverage by governance domain (Cognitive ~95%, Presentation ~90%, Workflow ~90%, Overall ~90%), assesses over-engineering (over-modeled: a platform governance track; under-modeled: the user-disposition input seam, to be named explicitly inside Wave D), and concludes Wave P0 is necessary while P1–P5 are not. Final recommendation: Option C — continue Wave A–E and treat platform/commodity capabilities as implementation concerns — augmented by a single Wave D clarification that user-disposition is a governed input, with Package 003 (Authority Promotion Authorization) confirmed as Category A mandatory and pending. It preserves all accepted architecture and invents no new concept; only the owner ratifies.*

**Release 1 Application / Platform Classification Decision 001 complete.**
