# Proposal — "Findings" → "Issues" user-facing label (RB-036)

- **Status:** Proposed — awaiting owner decision (Framework 001 · Review complete, Decision pending)
- **Class:** A (user-facing terminology; Disambiguation Register + presentation-spec realization). **Presentation-only; no object-model, contract, or doctrine change.**
- **Backlog:** RB-036 (this proposal)
- **Author (analysis/recommendation only):** AI contributor under Framework 001A / DL-033. **AI does not ratify.**
- **Owner decision:** required to adopt, reject, or amend.

> Governance note: this is an **analysis + recommendation** routed through Framework 001 (Backlog → Proposal → **Review** → Decision → Change → Changelog). No canonical artifact is changed by this document; the `DL-PENDING-findings-as-issues-user-facing-label` record carries the ratifiable decision text, and the glossary/spec edits are **realization landed with the decision at owner merge** — not here.

---

## 1. Problem

The Release-1 UI exposes users to **three overlapping vocabularies for the same underlying signal**: "Findings" (Finding Panel), "Issues" (Issue cards / IssuePanel), and "weaknesses" (inline CAF overlays / "what's weakening understanding"). This is friction and cognitive load for the user, and it is *unnecessary* because canon already nominates one of them as the user-facing concept:

- **ISS-01** states plainly: *"Issues are user-facing; findings are first-class."*
- The Issue Engine already forms **exactly one Issue per Finding** (`evaluate/engine.py`: `form_issue(f) for f in findings`); the built `issues` router describes an Issue as *"the first-class, prioritized Finding — severity an attribute — with source-Finding lineage."* The mapping is **already 1:1**.
- Inline "weaknesses" are CAF overlays (OVL-01, *"Expose CAF findings directly within artifact content"*) — i.e. the same Findings surfaced in context, already carrying finding lineage.

So the user is shown three names for what is, underneath, one first-class object (Finding) and its 1:1 user-facing projection (Issue).

## 2. Proposed change (one decision)

**Adopt "Issues" as the single user-facing label; retire "Findings" and "weaknesses" from the user-facing vocabulary. Internals unchanged.** This is the same **user-facing presentation-label** mechanism already ratified under **DL-087** (e.g. CAF → "Clarity · Alignment · Feasibility"; Fast/Deep Pass → "Initial/Extended Analysis") — a friendly label mapping to an **unchanged** canonical/internal term.

Add to the `CANONICAL_GLOSSARY` Disambiguation Register (DL-087 user-facing-label table):

| User-facing label | Canonical / internal term (unchanged) | Note |
|---|---|---|
| **Issues** / **Issue** | **Finding** (first-class object; Infer) surfaced to users via the **1:1 Issue projection** (ISS-01, Evaluate) | UI label; replaces user-facing "Finding". Finding stays authoritative in specs, code, contracts |
| **Issue** (in place of "weakness") | CAF-overlay "weak/weakness" language (OVL-01, findings-in-context) | UI label; inline overlays read as "Issues" |

Realization (landed with the decision): the **Finding Panel becomes the Issue detail view**; user-facing surfaces route through the Issue projection; UI copy replaces "Finding"/"weakness" with "Issue" across Overview, IssuePanel, OvlPanel, Finding Panel, MRI copy, and export copy. **Internal objects, code, analysis, and contracts are untouched.** The finding→issue mapping stays **1:1 for R1**; any future aggregation is a separate, deliberate decision (out of scope here).

## 3. Framework 001A Review

**Findings.**
- Canon already designates Issue as the user-facing surface of a Finding (ISS-01) and the engine already produces a 1:1 Issue-per-Finding projection — so this is **conformance to an existing model**, not a new ontology.
- The change is mechanically identical to ratified DL-087 user-facing-label entries (CAF, Fast/Deep); the mechanism, precedent, and owner-ratification pattern already exist.
- "Weakness" is **not** a governed object — it is descriptive UI language for CAF-flagged weak areas (Confidence/MRI/overlay), so folding it into "Issues" has zero object impact.

**Concerns.**
- **C1 — dual sense of "Issue."** "Issue" is both an internal object *and* now the user-facing umbrella label. The Disambiguation Register entry must state this precisely (done above) so specs/code keep "Finding" as the first-class term and do not silently treat "Issue" as replacing the Finding object. Recommend the register note be explicit that Finding is preserved.
- **C2 — 1:1 assumption.** The relabel is only clean while finding→issue is 1:1 (true today). If issues ever aggregate findings, the user-facing "one issue" would stop equalling "one finding" — flagged as a **separate future decision**, not adopted here.
- **C3 — surface consolidation scope.** Retiring the user-facing "Finding Panel" name into "Issue detail" is presentation realization touching `FINDING_PANEL_SPECIFICATION_V1` / `FINDING_PRESENTATION_SPECIFICATION_V1`; confirm no contract keys on the user-facing string "Finding" (it should not — contracts key on the object).

**Dependencies.**

| Artifact | Zone | Impact | Action |
|---|---|---|---|
| `CANONICAL_GLOSSARY` Disambiguation Register (DL-087 label table) | 00_owner | **HARD** | Add the two user-facing-label rows (§2) |
| `FINDING_PRESENTATION_SPECIFICATION_V1` / `FINDING_PANEL_SPECIFICATION_V1` | 10_product/experience | **MED** | Relabel to "Issues"; Finding Panel → Issue detail |
| Issue presentation / IssuePanel + overlay copy | 10_product/experience | **MED** | "Weakness"/"Finding" copy → "Issue" |
| Finding object / Issue Engine / contracts | 10_product/domain, 20_handoff | **CHECK — none** | Confirm internal object model + contracts unchanged (presentation-only) |

**Recommendation.** Adopt. It reduces three user vocabularies to one, follows the ratified DL-087 mechanism exactly, preserves the Finding object and every contract, and is near-zero-cost because the 1:1 Issue projection already exists. Pair with **RB-035** (finding-flow lifecycle) since both touch the Issue surface and should land together to avoid churn.

**Status.** Proposed — Review complete; **owner Decision pending**. Not ratified; not canon.

## 4. Relationship to RB-035

RB-035 (finding-flow simplification / lifecycle) and this proposal both alter the Issue surface. Recommend they are ratified and realized **together**: this proposal fixes what the user *calls* the object; RB-035 fixes the *lifecycle* the user sees on it. Sequencing them together avoids relabeling twice.
