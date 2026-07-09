# Finding Presentation Specification v1

**Type:** Presentation specification — authoritative Release 1 Finding presentation reference
**Status:** Active Release 1 · **Date:** 2026-05-31
**Sits below (authoritative — presents, must not modify):** `FINDING_SYSTEM_SPECIFICATION_V1.md` · Finding Model · CAF Scoring v2 · Reliability v2 · Confidence v2 · `RECOMMENDATION_SYSTEM_SPECIFICATION_V1.md` · `RECOMMENDATION_FINDING_COUPLING_SPECIFICATION_V1.md`.
**Consistent with:** `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` · Data Model v1.1 · State Model · Event Model · Architecture Audit 001/002 · `RECOMMENDATION_OPTION_MULTIPLICITY_RECONCILIATION_V1.md`.

> **Non-negotiable.** **Presentation only.** This spec defines how Findings are *shown*; it does **not** modify Finding/Recommendation behavior, lifecycle, CAF/Reliability/Confidence, or Impact Assessment, and introduces **no** new objects, lifecycles, events, governance, automation, agents, scoring, ranking, probability, or calibration. **Findings are descriptive, evidence-based, explainable — never prescriptive/advisory/actionable.** Recommendations remain the advisory object. **Findings contribute to CAF only via Impact Assessment and never modify CAF/Reliability/Confidence** — the presentation must not imply otherwise. **Possible Resolution Paths** are a UI pattern over multiple Recommendations (AMB-1 resolved) and are **not** reintroduced as objects.

---

## A. Executive Summary

- **Purpose:** the canonical way Findings are presented to users in Release 1 — visual structure, organization, prioritization, explainability, status/history, and their presentation relationships to Recommendations, CAF, and Outcome Confidence.
- **Scope:** presentation only. No behavior, lifecycle, generation, or assessment logic.
- **Architectural role:** the **descriptive surface** of the product. Findings tell the user *what OSLO understands to be unclear/conflicting/unsupported/constrained/incomplete* — the basis from which Recommendations (advisory) and the user's actions follow. Findings are the user's window into **understanding integrity**, not a to-do list.

---

## B. Finding Presentation Philosophy

- **Understand immediately:** *what* the finding is (a clear title + type + one-line summary), *which* dimension of understanding it affects, *how* significant it is (severity), and *that* it is descriptive (an observation, not an instruction).
- **Progressively disclose:** *why* OSLO identified it (rationale), its *supporting evidence*, its *Impact Assessment* relationship to CAF (qualitative), its *related Recommendations*, and its *history*.
- **Support understanding, not action:** a Finding helps the user **see** a gap in understanding. It never tells the user what to do — that is the Recommendation's role, surfaced **beneath** the finding (§I). The presentation frames findings as **insight**, with action reachable but clearly separate.

---

## C. Finding Card Specification

The canonical Release 1 **Finding card**:

**Required elements:**
- **Title** — concise human-readable name of the condition.
- **Finding type** — the canonical type (user-friendly label).
- **Finding summary** — one-line description of the observed condition.
- **Affected CAF dimensions** — which of Clarity / Alignment / Feasibility it bears on.
- **Supporting evidence summary** — a brief indicator of the evidence it's grounded in (count/source), expandable to the full basis.
- **Status** — current lifecycle state (§G), as an indicator.
- **Recommendation count** — number of **active** Recommendations addressing it (e.g., "3 possible resolution paths"), entry point to §I.

**Optional elements (on expand):**
- Severity emphasis, artifact location, first-seen context, history/supersession link.

*No scores, percentages, indices, or computed magnitudes appear on a card. Severity and dimensions are qualitative. The card never shows an action verb as a directive (descriptive framing).*

---

## D. Finding Organization Model

**Canonical Release 1 grouping: by CAF Dimension** (Clarity · Alignment · Feasibility), with **severity as the in-group ordering** (§E).

**Evaluation of options:**
- **CAF Dimension grouping (chosen):** maps each finding to the dimension of understanding it degrades, directly connecting the findings surface to the CAF/Confidence the user already sees. It answers the user's natural question — *"what is weakening my Clarity / Alignment / Feasibility?"* — and supports targeted improvement.
- **Severity grouping (secondary, as ordering):** great for "what needs attention," but as the *primary* grouping it detaches findings from the understanding model; used instead as the **ordering within** each dimension.
- **Artifact grouping (alternate view):** useful for "where in the plan," offered as an optional alternate/filter view, not the default.
- **Finding-type grouping (alternate view):** useful analytically but less meaningful to a planner; optional view.

**Rationale:** Release 1's thesis is understanding integrity expressed as CAF; organizing findings by the dimension they affect makes the surface coherent with confidence and recommendations, while severity ordering keeps the most important items first. Artifact/type/severity remain available as **alternate views/filters** (presentation choices, not the canonical default).

---

## E. Finding Priority Presentation

Ordering is **qualitative — no scores, percentages, or ranking formulas:**
- **Within a dimension group:** **critical → moderate → warning** (severity), then **most-recent first** (`first_seen`) as a tiebreak.
- **Across dimension groups:** the dimension containing the **highest-severity** findings is shown first (e.g., a dimension with a critical finding precedes one with only warnings); otherwise a consistent canonical dimension order is used.
- **What appears first:** the most-severe findings in the most-affected dimension. **What appears later:** lower-severity findings, then resolved/superseded (in history, §H).

This is a **presentation ordering**, derived from the qualitative severity already on each finding — **no numeric priority is computed or shown.**

---

## F. Finding Explainability Presentation

Progressive disclosure:
```text
Finding (card)
 → Why OSLO identified it        (rationale)
 → Supporting evidence           (the evidence/context it's grounded in)
 → Impact Assessment summary     (which CAF dimension(s) it affects — qualitative)
 → Related Recommendations       (§I)
 → History / supersession        (§H)
```

- **Collapsed state:** the card (§C) — essentials only.
- **Expanded state:** the full basis — rationale, evidence, qualitative Impact-Assessment relationship, related recommendations, and history.
- **Traceability:** from a finding the user can reach its **evidence** and its **recommendations**, and from a superseded finding the one that replaced it. **No finding is opaque** (Finding System Spec FND-7). Explanation reduces to **basis**, never to a number.

---

## G. Finding Status Presentation

*(Visual presentation only — lifecycle behavior owned by Finding System Spec §C / State Model §10; not redefined.)*

| Status | Presentation |
|---|---|
| **detected** | shown as **new / open**, prominent |
| **acknowledged** | marked as **seen/accepted** by the user |
| **addressed** | marked **in progress** (work targeting it has begun) |
| **closed** | shown as **resolved**, moved toward history |
| **reopened** | shown as **returned to open**, with a "reopened" indicator |
| **superseded** | collapsed into **history** (retained), links to the superseding finding |

Status is an **indicator**, never an action. The UI must not present `addressed`/`closed` as "solved by the user" beyond what the lifecycle states — resolution (success) is shown when reanalysis weakens/removes the finding.

---

## H. Finding History Presentation

- **Current surface** shows **active** findings (detected/acknowledged/addressed/reopened).
- **Superseded findings** are shown in **history** (retained, never deleted), reachable from the current finding with an explanation of what changed.
- **Historical/closed findings** are viewable in a history/timeline view; they are not deleted and not shown as active.
- **Append-only:** the presentation reflects supersession-over-deletion — the user can always trace a finding's lineage. Counts and the active surface reflect **active** findings only.

---

## I. Finding → Recommendation Presentation

- **Placement:** Recommendations appear **beneath** their Finding (the canonical hierarchy: Project → Finding → Recommendation(s)). A Recommendation **never contains a Finding**.
- **Recommendation count:** the finding card shows the count of **active** Recommendations (presented as "N possible resolution paths" where appropriate).
- **OSLO Recommended:** the primary Recommendation is shown first, labeled **"OSLO Recommended"** (per `RECOMMENDATION_PRESENTATION_SPECIFICATION_V1.md` §C) — advisory, no score.
- **Possible Resolution Paths:** the other Recommendations for the finding are grouped under **"Possible Resolution Paths"** — a **presentation grouping of multiple Recommendations**, **not** an object/lifecycle (AMB-1; `RECOMMENDATION_OPTION_MULTIPLICITY_RECONCILIATION_V1.md`). Collapsible.
- **Selection:** selecting one is **accepting a Recommendation** (**Selected Path**), which may differ from OSLO Recommended.
- **No new recommendation behavior** is introduced here; this section only places recommendations within the finding surface.

---

## J. Finding → CAF Presentation

- **Affected dimensions:** the finding shows which CAF dimension(s) it bears on (Clarity/Alignment/Feasibility).
- **Impact Assessment relationship (qualitative):** the finding may present *that* it contributes to the affected dimension's assessment (e.g., "affects Clarity") and, on expand, a **qualitative** Impact-Assessment summary (significance/scope in words). **No magnitudes, indices, or formulas.**
- **Must not imply:** that the finding **modifies** CAF or **owns** CAF. The framing is **"contributes to the CAF assessment via Impact Assessment"** — CAF is assessed by CAF Scoring, changing only through assessment/reanalysis (Finding System Spec FND-2). The presentation never shows a finding "setting" a CAF value.

---

## K. Finding → Outcome Confidence Presentation

- **Chain shown correctly:** the presentation may connect a finding to the assessment it informs — **Finding → CAF → (with Reliability) → Outcome Confidence** — to help the user see *why* confidence sits where it does.
- **Must not imply direct influence:** a finding **does not** modify Confidence (it reaches Confidence **only through CAF**, FND-4) and **does not** influence Reliability at all (Reliability is determined independently of findings, RR-2). The UI must **never** depict a finding as directly moving the confidence or reliability signal.
- **Reliability framing:** reliability is presented as a **qualifier** of confidence (its own basis: coverage/evidence/assessability), **not** as something findings change.
- This section relates findings to the assessment signals **for comprehension only**; it asserts no causal direct-write path.

---

## L. Empty-State Presentation

*(Especially important for Tier 1 trust-building.)*
- **No findings exist:** present positively — e.g., "No issues found in this area yet" / "Understanding looks clear here" — never alarmingly, and never implying the analysis is incomplete when it is complete. If analysis is **pending**, show a non-blocking "Analyzing…" state instead of an empty void.
- **Findings resolved:** present as **success** — the conditions were addressed; resolved findings move to history with a positive resolution affordance. Reassures the user that improvement happened.
- **Findings hidden by filters:** clearly indicate that **filters are active** (e.g., "X findings hidden by filters") with a one-tap clear, so an empty list is never mistaken for "no findings."
- Empty states must **build trust**: distinguish *"nothing found"* from *"not yet analyzed"* from *"filtered out,"* and never imply a finding is resolved when it is not.

---

## M. Presentation Integrity Rules

*Objective, structurally testable, non-numeric.*

- **FPRS-1.** Findings are presented as **descriptive observations**, never as recommendations, instructions, or actions.
- **FPRS-2.** Findings remain **finding-anchored**: Recommendations appear **beneath** their Finding; a Recommendation never visually contains a Finding.
- **FPRS-3.** Findings remain **explainable**: rationale, evidence, affected dimensions, and history are reachable; **no opaque finding**.
- **FPRS-4.** A finding's presentation **never implies it modifies CAF/Reliability/Confidence**; it is framed as **contributing via Impact Assessment**.
- **FPRS-5.** A finding **never implies direct Confidence/Reliability influence**; only the **Finding → CAF → Confidence** chain is depicted, with Reliability as an independent qualifier.
- **FPRS-6.** **Possible Resolution Paths** are presented as **grouped Recommendations**, never as objects, lifecycles, or entities.
- **FPRS-7.** Finding **status** is **visualized** per §G **without redefining** lifecycle behavior; superseded/closed are retained in **history** (append-only).
- **FPRS-8.** Ordering/priority is **qualitative** (severity-based) — **no score, percentage, or ranking number** is shown or computed.
- **FPRS-9.** Resolution (success) is presented **only** when reanalysis weakens/removes the finding — never merely because a status changed or a recommendation was acted upon.
- **FPRS-10.** Empty states distinguish **none-found / not-yet-analyzed / filtered**, and never imply an unresolved finding is resolved.
- **FPRS-11.** No governance, execution, automation, or agent affordance appears on any finding surface.
- **FPRS-12.** Presentation introduces **no** new object/state/event and causes **no** CAF/Reliability/Confidence change.

---

## N. Conformance Requirements

A conforming UI MUST (structural, **non-numeric**, no pass-rate language):
- **C-1.** Render findings as descriptive cards (§C) grouped by **CAF dimension** with **severity ordering** (§D/§E); offer artifact/type/severity as alternate views (FPRS-1/FPRS-8).
- **C-2.** Place Recommendations **beneath** their Finding with count, **OSLO Recommended**, and **Possible Resolution Paths** grouping per the Recommendation Presentation Spec (FPRS-2/FPRS-6).
- **C-3.** Provide reachable explainability (rationale, evidence, qualitative Impact-Assessment summary, related recommendations, history) from every finding (FPRS-3).
- **C-4.** Frame Finding→CAF as **contribution via Impact Assessment**; never depict a finding setting/modifying CAF, Reliability, or Confidence (FPRS-4/FPRS-5).
- **C-5.** Visualize finding **status** per §G; retain superseded/closed findings in **history** (FPRS-7).
- **C-6.** Present **resolution only on reanalysis** (FPRS-9).
- **C-7.** Implement empty states that distinguish none-found / pending / filtered (FPRS-10).
- **C-8.** Expose **no** governance/execution/automation/agent affordance; introduce **no** object/state/event; cause **no** assessment change (FPRS-11/FPRS-12).

Conformance is **all-or-nothing on these rules**; any prescriptive/opaque/unanchored finding, any implied direct assessment write, any displayed score, any deleted history, any resolution-without-reanalysis, or any governance/execution affordance **fails conformance**.

---

*This specification defines the canonical Release 1 presentation of Findings: descriptive, evidence-based, explainable, CAF-dimension-organized, finding-anchored surfaces with Recommendations beneath, and correct (non-causal) depiction of the Finding → CAF → Confidence relationship. It modifies no model, lifecycle, object, event, or assessment behavior, reintroduces no Resolution Path object, and introduces no governance, execution, automation, scoring, or ranking.*

## O. Ratified update — Findings workspace & filters (DL-088, 2026-07-02)

Ratified by **DL-088** (presentation-only). The **Findings list is a center-pane workspace** (the canonical "Findings Workspace") reachable from the left rail — consistent with Overview/History; the **finding detail remains a contextual Panel** (Panel Model preserved). Adds **Dimension / Severity / Section filters** and a **Group-by (Dimension | Section)** control; default grouping is **Dimension** (findings map to the CAF dimensions that drive Confidence). Finding cards stay scannable (title · severity · location · status); type, evidence count, and resolution paths live in the finding detail. No new object, scoring, or ranking. Visual reference of record: `product-design/oslo_r1_experience_mockup_v3.html`.

## P. Ratified update — Finding type + epistemic basis (DL-093, 2026-07-02)

Ratified by **DL-093** (presentation-only; realizes RB-033 Phase R1; **amends §O** re: card content — the type now appears on the card). A Finding is presented on **two independent axes**:

- **Type** (the §C required "Finding type") — *what the observation is*: the canonical **Gap / Conflict / Risk** family (Architecture Foundation M-3; `WAVE_B_CONTRACT_PACKAGES_UNDERSTANDING`), shown with its finer user-facing kind (Coverage gap, Missing information, **Assumption**, **Ambiguity**). Type is a **label, not a coefficient** — severity comes from the Impact Assessment, never from type (`OUTCOME_CONFIDENCE_CALIBRATION_DECISION_001`).
- **Basis** — *how grounded the finding is*: **stated (Attested)** — anchored in something the plan states — vs **inferred (Derived)** — OSLO's read of a not-yet-stated gap/assumption. This is the canonical **Attested/Derived** distinction (`RELEASE_1_EPISTEMIC_STATE_MODEL_DECISION_001`) applied at the finding level; **"inferred" is a basis, never a type.**

The **card** carries the type plus a compact **basis tag** (`stated` / `inferred`); the **finding detail** (§F; Finding-Panel §E/§F) states the basis in plain language ("OSLO inferred this — it isn't stated in your inputs" / "Grounded in a stated item in your plan"), discharging the Epistemic-State-Model **Disclose obligation** at the finding level (Derived understanding surfaced *as* Derived). Basis colour is calm/neutral — **never** the action/attention accent. Presentation-only: no object, scoring, or ranking. Formal sub-typing of the finer kinds under Gap/Conflict/Risk and the **basis-assignment contract** (which of Infer/Evaluate sets a finding's Attested/Derived basis) are **deferred to R2** (RB-033 Phase R2). Visual reference of record: `product-design/oslo_r1_experience_mockup_v3.html` (baseline `03-findings`).

**Finding Presentation Specification v1 complete.**
