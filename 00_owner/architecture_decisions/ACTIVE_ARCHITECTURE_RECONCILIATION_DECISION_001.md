# Active Architecture Reconciliation Decision 001

**Document Type:** Architecture Reconciliation Decision (resolves ESC-0) · **Status:** **Ratified with Conditions under DL-043 (2026-06-04)** · **Date:** 2026-06-03
**Resolves:** the Critical same-tier conflict identified in `AUTONOMOUS_IMPLEMENTATION_CONTROL_SYSTEM_V1.md` (ESC-0). **Authoritative inputs (read, not re-opened):** `CURRENT_TRUTH.md` · `OSLO_RELEASE_1_CANONICAL_SCOPE_V1` · `OSLO_ARCHITECTURE_BASELINE_V1` · `OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1` (§14 layer map) · `OSLO_COGNITIVE_RESPONSIBILITY_VS_LAYER_ARCHITECTURE_REVIEW_001` · `OSLO_RUNTIME_LAYER_RECONCILIATION_DECISION_001` · Contract Inventory · Wave-A Packages 001/002 (+003 pending).

> **Mode:** independent reconciliation. **This document does not unilaterally adopt an architecture** — same-tier conflicts resolve only by owner Proposal (`CLAUDE.md`, `REPOSITORY_ARCHITECTURE.md`). It states the conflict precisely, separates what is *already settled* from what is *genuinely open*, presents options with downstream consequences, gives a recommendation, and routes ratification to the owner. **No new responsibility, object, or concept is introduced.**

---

## 1. The Conflict, Stated Precisely

ESC-0 was framed as "two architectures." On inspection it is **two documents answering two different questions**, with exactly **one** genuine substantive collision:

- **`CURRENT_TRUTH.md`** answers a **scope** question — *what ships in Release 1.* It declares the active set (Context Plane, Knowledge Layer, Planning Intelligence, 8 Understanding Domain Models, Notification, Collaboration, Reporting), a milestone plan (M0–M6), and that **"Governance is deferred… Knowledge Layer — not governance-gated,"** with Disposition/Accepted-Understanding/Review-Request/Agent-Governance/Execution as **Future**.
- **`OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1`** answers a **representation** question — *how cognition is structured.* It makes the **responsibility** primary (Perceive→Retain→Intend→Infer→Evaluate→Advise→Disclose→Act), treats **Authority** as a cross-cutting plane, and **explicitly states it supersedes the layer-as-primary representation of the Baseline** (mapping layers in §14), pending owner ratification.

**These are largely orthogonal.** Representation (how to name/structure cognition) and scope (what to build first) do not inherently conflict. The collision is narrow and specific:

> **The genuine conflict:** the recent contract thread built an **Authority promotion gate** (Pkg 003) and **exposure governance** (Wave D) **into Release 1**, whereas `CURRENT_TRUTH` says R1 knowledge is **"not governance-gated"** and **"governance is deferred."** *Is R1 governance-gated, or not?*

Everything else attributed to the conflict is **vocabulary**, and vocabulary is already mapped (below), not contradictory.

## 2. What Is Already Settled (representation + vocabulary)

The **responsibility-vs-layer representation question is effectively decided** and should simply be ratified:

- The Cognitive Responsibility spec **already claims supersession** of the layer-as-primary Baseline and **retains layers as a secondary dependency-ordering view** (§14). The prior `…VS_LAYER_REVIEW_001` and `RUNTIME_LAYER_RECONCILIATION_DECISION_001` reached the same place. This is the architecture the owner has been actively developing across the entire contract thread.
- **Vocabulary maps cleanly** (no semantic conflict):

| CURRENT_TRUTH / layer term | Cognitive Responsibility term |
|---|---|
| Context Plane (extraction/enrichment) | **Perception / Perceive** (cross-cutting intake) |
| Knowledge Layer | **Retain** |
| Planning Intelligence (assessment) | **Infer** (findings) + **Evaluate** (CAF/Confidence/Reliability) |
| Finding (Understanding model) | **Infer → Finding** |
| CAF · Confidence · Reliability | **Evaluate** attributes |
| Recommendation (Understanding model) | **Advise → Recommendation** |
| MRI · Overlay | **Disclose / Render** surfaces |
| Communication / presentation | **Disclose** (cognitive) + **Render** (service) |
| Notification Service | **Render/Disclose** supporting surface |

The 8 Understanding Domain Models land cleanly on Infer/Evaluate/Advise/Disclose. **No content is lost; no concept is renamed into a contradiction.** Adopting the responsibility representation does **not** invalidate the CURRENT_TRUTH capability set — it **re-expresses** it.

**Conclusion of §2:** the representation/vocabulary half of ESC-0 is reconcilable now by ratifying the Cognitive Responsibility model as the canonical representation, with layers retained as a secondary view. The CURRENT_TRUTH capability inventory survives, re-expressed.

## 3. The One Open Question — Is Release 1 Governance-Gated?

This is the part that **must not** be settled unilaterally, because the two documents genuinely disagree and it changes scope.

Two senses of "governance/Authority" are being conflated:

- **(a) Outcome / Agent Governance** — controlled *acceptance of understanding*: Disposition, Accepted Understanding, Review Request, execution authorization. **Both documents agree this is Future** (CURRENT_TRUTH §7; the Cognitive Responsibility spec tags Act/Coordinate/execution-authorization as evolution/posture-gated). **No conflict here.**
- **(b) Promotion / Exposure Authority** — admitting intake→canonical knowledge (the Pkg 002→003 admission gate) and expose/suppress/defer/block of cognitive outputs (Wave D). **The contract thread put this in R1; CURRENT_TRUTH's "not governance-gated" excludes it.** **This is the conflict.**

The decision the owner must make: **does Release 1 include the lightweight (b) Promotion/Exposure Authority, or not?**

### Resolution Options

| | Option 1 — Defer (b) | Option 2 — Update CURRENT_TRUTH | **Option 3 — Hybrid (recommended)** |
|---|---|---|---|
| **Representation** | Adopt Cognitive Responsibility | Adopt Cognitive Responsibility | Adopt Cognitive Responsibility |
| **R1 Authority** | **None** — Retain admission is non-gated in R1 (matches CURRENT_TRUTH literally) | **Full (b)** promotion + exposure in R1 | **Minimal (b):** promotion-readiness + exposure of cognitive outputs only; **no** acceptance/disposition |
| **Outcome/Agent Governance (a)** | Future | Future | Future |
| **Downstream contract impact** | **Pkg 003 + Wave D drop out of R1**; Pkg 002 admission becomes non-gated; Coverage/Classification/Contract-Plan need rescoping | Pkg 003 + Wave D stay; CURRENT_TRUTH §1–§3,§7 must be edited (governance no longer "deferred") | Pkg 003 reduced to **promotion-readiness** (not acceptance); Wave D = **exposure only**; CURRENT_TRUTH language clarified, not reversed |
| **Risk** | Re-work of recent Wave-A/D contracts; possible re-introduction of the orphaned-governance gap the responsibility model closed | Expands R1 scope; contradicts a ratified-tier scope doc; scope-creep risk | Requires a precise definitional line between *exposure* and *acceptance* |
| **Fit with evidence** | Most faithful to CURRENT_TRUTH's literal words | Most faithful to the contract thread | Reconciles both: representation adopted, scope minimally touched, Future-governance preserved |

**Why Option 3 is recommended (for the owner's consideration, not as a ruling):** it adopts the strictly-better representation, keeps the contract thread *mostly* intact, and honors CURRENT_TRUTH's real intent — which is to defer **Outcome/Agent Governance (a)** (acceptance/disposition/execution), **not** necessarily to forbid *exposure control* of what OSLO shows. Read that way, "Knowledge Layer not governance-gated" means *no acceptance gate on understanding*, which Option 3 preserves (promotion-readiness ≠ acceptance). It minimizes rescoping while closing the orphaned-governance gap. **But if CURRENT_TRUTH's "not governance-gated" is meant literally and absolutely, Option 1 is the faithful reading — and that is the owner's call.**

## 4. Downstream Consequences (so the decision is made with eyes open)

- **Everything I generated this thread assumed Authority-in-R1** (Cognitive Responsibility representation + (b) Authority): the Capability Coverage Review, Classification Decision 001, Contract Generation Plan Wave A/D, Pkg 002's admission gate, and the pending Pkg 003.
- **Option 1** ⇒ rescope: Pkg 003 and Wave D exit R1; Pkg 002 admission becomes non-gated; the Coverage/Classification/Plan documents need a scope patch.
- **Option 2** ⇒ edit CURRENT_TRUTH §1–§3/§7 (governance no longer "deferred"); contract thread unchanged.
- **Option 3** ⇒ Pkg 003 narrows to *promotion-readiness*; Wave D narrows to *exposure*; CURRENT_TRUTH gets a clarifying note distinguishing **acceptance-governance (deferred)** from **exposure-control (R1)**; minimal rework.

## 5. What This Decision Unblocks

Once the owner ratifies (any option), ESC-0 clears and the following become unambiguous: the canonical representation (responsibility-primary), the legacy-corpus disposition (Baseline → secondary view; `raw/notion` → Source), the scope of R1 Authority, and therefore the correct target for **every** contract and the Runtime Environment Constraint Profile. **This is the gate that converts the whole repository from "two targets" to "one target."**

---

> ### Proposed Owner Resolution
> **Resolution requested (two parts):**
>
> **Part A — Representation (recommended: ratify now).** Adopt the **Cognitive Responsibility Architecture** as OSLO's canonical architectural representation; retain the layer model as a **secondary dependency-ordering view** (§14); reclassify `OSLO_ARCHITECTURE_BASELINE_V1` as a secondary representation and `raw/notion/**` layer specs as non-binding Source. Ratify GOV-ARCH-001 accordingly. The `CURRENT_TRUTH` capability inventory is **preserved, re-expressed** in responsibility vocabulary (§2 map).
>
> **Part B — Release 1 Authority scope (owner must choose one):**
> - **Option 1 — Defer all Authority gating from R1** (faithful to CURRENT_TRUTH literal; rescopes out Pkg 003 + Wave D).
> - **Option 2 — Include full promotion + exposure Authority in R1** (edits CURRENT_TRUTH; keeps contracts).
> - **Option 3 — Hybrid (recommended):** R1 includes only **promotion-readiness + exposure-control** Authority; **Outcome/Agent Governance (acceptance/disposition/execution) stays Future**; clarify CURRENT_TRUTH's "not governance-gated" to mean "no acceptance gate," not "no exposure control." Pkg 003 narrows to promotion-readiness; Wave D narrows to exposure.
>
> **On ratification:** update `CURRENT_TRUTH` and the affected Coverage/Classification/Contract-Plan documents to the chosen scope; clear ESC-0; proceed to the Runtime Environment Constraint Profile and Wave-A completion against the single ratified target.
>
> **Out of bounds / not done here:** this document adopts nothing and edits no canonical content; it resolves the conflict *for the owner to ratify* and invents no new concept.

---

*This Active Architecture Reconciliation Decision resolves ESC-0 by showing that the apparent two-architecture conflict is, in substance, a settled representation question plus one genuine open scope question. The representation half — responsibility-primary (Cognitive Responsibility Architecture) vs layer-primary (Baseline/CURRENT_TRUTH vocabulary) — is reconcilable now: the Cognitive Responsibility spec already supersedes the layer-as-primary model while retaining layers as a secondary dependency-ordering view, the vocabularies map cleanly (Context Plane→Perceive, Knowledge Layer→Retain, Planning Intelligence→Infer+Evaluate, Finding→Infer, CAF/Confidence/Reliability→Evaluate, Recommendation→Advise, Communication→Disclose/Render), and the CURRENT_TRUTH capability inventory is preserved and re-expressed rather than invalidated. The one genuine conflict is whether Release 1 is governance-gated: the recent contract thread built a promotion/exposure Authority (Package 003, Wave D) into R1, while CURRENT_TRUTH defers governance and declares the Knowledge Layer not governance-gated; the document separates Outcome/Agent Governance (acceptance/disposition/execution — agreed Future by both) from Promotion/Exposure Authority (the actual collision), and offers three owner options — defer all R1 Authority (faithful to CURRENT_TRUTH, rescopes out Pkg 003/Wave D), include full promotion+exposure in R1 (edits CURRENT_TRUTH), or a recommended hybrid (R1 = promotion-readiness + exposure only, Outcome/Agent Governance stays Future) — with explicit downstream consequences for the Coverage Review, Classification Decision, Contract Generation Plan, and Packages 002/003. It recommends ratifying the representation now and choosing the hybrid scope, unblocking ESC-0 and giving every downstream contract and the Runtime Environment Constraint Profile a single canonical target, while adopting nothing unilaterally and routing all ratification to the owner.*

**Active Architecture Reconciliation Decision 001 complete.**
