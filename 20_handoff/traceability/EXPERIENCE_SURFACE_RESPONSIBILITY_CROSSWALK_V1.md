# Experience-Surface ↔ Responsibility Crosswalk v1 (the §0 crosswalk)

**Type:** Co-governed seam artifact (`20_handoff`) — traceability/interface mapping. · **Status:** Ratified — DL-064 (2026-06-16). To be incorporated as **§0** of `OSLO_ARCHITECTURE_BASELINE_V2` when authored.
**Resolves:** C-3 (MASTER_SPEC_ALIGNMENT_REVIEW — owner working-doc, non-repo) — the missing mapping between the Master Spec's *experience* vocabulary and the engineering *architecture* vocabulary. C-3 was a **gap, not a contradiction.**

> **Orientation, primary axis (DL-043 / glossary).** The canonical architecture model is **responsibility-primary** — the seven cognitive responsibilities (`Perceive · Retain · Infer · Evaluate · Advise · Disclose · Act/Adapt`, with `Render` a non-cognitive service). The legacy seven-**layer** names (Context Plane, Knowledge Layer, Reasoning, Judgment, Governance, Communication, Execution Coordination) are **banned as primary identifiers** (`CANONICAL_GLOSSARY.md`, DL-053) and are shown here **only as a deprecated secondary column for orientation**. Map work to responsibilities, not layers.

---

## 1. Experience surface → responsibility (primary, canonical)

| Master Spec experience surface | Canonical responsibility | Grounding (ratified) |
|---|---|---|
| Project intake (Upload / Describe / Template) | **Perceive** (intake + source-attributed claim extraction) | glossary; DL-056 (templates) |
| Planning Synthesis (Intent/Context/Scope/Requirements/WBS/Resources/Schedule) | **Infer** (synthesis/generation as Derived) | DL-047 |
| Findings | **Infer** | glossary |
| Issues · CAF · Confidence · Reliability · Outcome Confidence · False-Confidence · Understanding State | **Evaluate** | glossary; DL-062 (CAF first-class) |
| Recommendations · Clarification Requests · Suggested Fixes (Daily Fix) | **Advise** (candidate only; user applies — no autonomous OSLO write) | glossary |
| CAF Review Requests (CRR) | **Advise** + collaboration affordance | DL-047; DL-055 |
| Project MRI | **Disclose** (per-project understanding surface) | DL-061 |
| CAF Overlay | **Disclose** | glossary (presentation) |
| OSLO Chat | **Disclose** (presentation incl. Chat surface) | glossary |
| Artifact Workspace | **Render** (non-cognitive) + **Disclose** | glossary; runtime ownership spec (render) |
| Fast Pass / Deep Pass | **analysis modes** spanning Perceive → Infer → Evaluate → Disclose (progressive confidence) | DL-046 |
| Recompute / stale-backbone | **Act/Adapt** | glossary |

## 2. Commodity surfaces (intentionally non-cognition — do not map to a cognitive responsibility)

Monetization, Telemetry, Collaboration (comments/mentions), Sharing/Export, Notifications, Project CRUD, Settings, Auth — **commodity plumbing** (DL-043 Categories C/E/F; `ANTI_ASSUMPTION_BUILD_PROTOCOL`). Built with normal engineering judgment; they touch no cognitive contract. (`Render` services them.) *If unsure whether something is commodity, treat it as cognitive and escalate.*

## 3. Responsibility ↔ deprecated layer (secondary, orientation only)

| Canonical responsibility | Deprecated layer name (do not use as primary) | Note |
|---|---|---|
| Perceive | Context Plane | intake/orientation |
| Retain | Knowledge Layer | canonical append-only store |
| Infer | Reasoning Layer | Findings + synthesis |
| Evaluate | Judgment Layer | Issues/CAF/Confidence |
| Advise | *(none — the layer model never assigned Recommendation production; flagged "Conflicting" in the runtime layer-ownership spec)* | **gap closed by responsibility-primary**: Advise owns it |
| Disclose | Communication Layer (+ Governance Layer exposure: expose/suppress/defer/block) | render + exposure governance |
| Act/Adapt | Execution Coordination | recompute/stale |
| Render (non-cognitive) | Communication Layer (render) | service, not cognition |

## 4. Status & notes

- **No invented mappings.** Every row in §1 traces to ratified canon (glossary responsibilities, DL-043/046/047/055/061). The Master Spec "Authority Plane" surface is **out of R1** (no `Authority` engine; DL-043) and is intentionally absent.
- **Why C-3 is a close-out, not a doctrine call:** the vocabulary conflict was already settled by DL-043 (responsibility-primary; layer-names deprecated). This crosswalk documents the bridge; it adds no new structure.
- **Adjacent, not resolved here:** the *Outcome Integrity States* conflict (Doctrine 04 vs Article 33 vs Spec 08) is tracked separately.

---
*Ratified via DL-064. This crosswalk is the authoritative experience↔responsibility mapping for Release 1 and is the source for §0 of Architecture Baseline V2.*
