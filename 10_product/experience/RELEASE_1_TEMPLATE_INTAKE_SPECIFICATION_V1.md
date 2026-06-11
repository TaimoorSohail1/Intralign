# Release 1 — Template Intake Specification v1

**Document Type:** Product experience specification (intake capability) · **Status:** 🟡 **Proposed — pending owner ratification (DL-056)** · **Date:** 2026-06-10 · **Zone:** `10_product` (product-authoritative)
**Authorizing decision:** DL-056 (scope ruling: **Start From Template → in scope for Release 1**; **Guided Intake → deferred to Release 2**).
**Resolves:** Capability Matrix V2 §22 #3 ("Templates referenced but undefined"). **Supersedes** the prior deferral of templates in `ONBOARDING_AND_PROJECT_CREATION_EXPERIENCE_SPECIFICATION_V1` §L.

> **Governance.** Proposed spec authored at owner direction; the owner ratifies via DL-056 merge (Authority Constraint). UX/interaction + content-structure only — it **computes nothing, generates nothing, governs nothing**; adopted template content is ordinary evidence the user owns and edits. Honors the onboarding invariant *"ingestion adds content only."*

---

## 1. Purpose

Let a new user reach value in **~60 seconds** by selecting a **pre-authored, fully worked fictitious sample project** of a familiar type. Selecting a template **instantly instantiates a populated sample project** (one filled planning artifact) that Fast Pass analyzes immediately — so the user sees a realistic Project MRI on a believable example **without writing anything**, then edits it into their own project or starts fresh. This directly serves the 60-second Time-to-First-MRI / "Prove Understanding" value path. The sample content is **pre-authored and static** — instantiating it is copying, **not** system generation (Onboarding OB-C3 preserved).

## 2. What a Template Is (and is not)

- A template is an **owner-curated, pre-authored, fully worked fictitious sample plan** of a given type — a single planning document with realistic example content already filled in (**no blank prompts**).
- Selecting a template **instantiates a populated sample project** by copying that content into **one editable Artifact**; the project is **flagged as a sample** so the user knows it's fictitious. The user then edits it into their own project, or starts a fresh blank project instead.
- A template is **not** AI-generated, not a wizard/question flow (that is Guided Intake, R2), not a project-structure engine, and not user-creatable in R1.
- **Hard rule (carried from Onboarding OB-C3):** the system must not *generate* starting content. The sample is **static pre-authored** content; instantiating it is copying, **not** generation.

## 3. Form (DL-056 Q1 — single planning document)

Selecting a template produces **one Artifact** whose body is the template's **fully worked fictitious sample plan** — headed sections (markdown) with realistic example content already written (e.g., a sample "Office Relocation" or "Spring Cold Brew Launch"), **no prompts to fill**. It satisfies minimum-to-value (name + one artifact) on its own and is **immediately analyzable** by Fast Pass; the instantiated project is marked a **sample**.

## 4. Catalog (DL-056 Q2 — curated five, owner-authored)

Release 1 ships **five** owner-curated templates — each a **fully worked fictitious sample plan** (full bodies in `templates/`). Sample scenarios: **Office Relocation** (generic), **"Pulse" team check-in app launch** (product), **"Brew & Co" cold-brew campaign** (marketing), **"DevNorth 2026" developer conference** (event), and **EU market expansion** (strategic/OKR). Section sets below; owner may refine body copy before GA:

| Template | `project_type` pre-fill | Baseline sections |
|---|---|---|
| **Generic Project Plan** | `generic` | Intent / Outcome · Context · Scope (in/out) · Key Requirements · Milestones · Risks & Assumptions · Stakeholders |
| **Product / Software Launch** | `product_launch` | Outcome & Success Metrics · Target Users · Scope & Non-Goals · Requirements · Release Milestones · Dependencies & Risks · Stakeholders |
| **Marketing Campaign** | `marketing_campaign` | Campaign Goal · Audience · Channels & Messaging · Scope · Timeline & Milestones · Budget Assumptions · Success Metrics |
| **Event** | `event` | Event Goal · Audience & Attendance · Scope (program/logistics) · Timeline & Milestones · Vendors & Dependencies · Risks · Success Metrics |
| **Strategic Initiative (OKR/Plan)** | `strategic_initiative` | Objective · Key Results · Context & Rationale · Scope · Workstreams & Milestones · Dependencies & Risks · Stakeholders |

Catalog content is **canon** under `10_product/experience/templates/` (one markdown body per template; see that folder's `README.md` for the index); engineering renders the picker and copies the chosen body in — it authors no template content. Starter body copy for all five is provided there (proposed; owner may refine before GA without a new decision, per DL-056).

## 5. Adoption Flow

```text
Choose Start Method → Start From Template
  ↓
Pick a template (catalog of 5; each shows name + a one-line "what this sample shows")
  ↓
Sample project instantiated: project_type pre-filled (non-gating); worked sample
  copied in as ONE editable Artifact (source="template"); project flagged "sample"
  ↓
Fast Pass runs on the populated sample → Project MRI in ~60s (value immediately)
  ↓
User explores the MRI, then edits the artifact into their own project (or starts fresh)
```

Selecting a template is equivalent, downstream, to uploading a complete document — it joins the **standard intake → Fast Pass** pipeline with no template-specific analysis behavior. The only differences: the content is pre-authored and the project is flagged a **sample**.

## 6. Data & Epistemic Handling (canon-settled defaults)

- The adopted document is an ordinary **Artifact**: `source = "template"`, `template_id` recorded in `provenance`, `content_ref` = the copied body. Append-only/versioned like any artifact.
- The instantiated **project carries a `sample` flag** so the fictitious content is clearly distinguished from the user's real data (UX surfacing is a build detail; the flag does not change analysis behavior).
- It is an **evidence-class** artifact (analyzed like an upload). It carries **no special epistemic status**; OSLO self-attests nothing on adoption and **generates nothing**.
- Subsequent user edits follow normal artifact versioning and trigger event-driven Deep Pass like any edit.

## 7. `project_type` Behavior (DL-056 Q4 — pre-fill, non-gating)

Choosing a template **pre-fills the project's optional `project_type`** with the value in §4. It **never gates behavior** and the user may change or clear it, consistent with the ratified onboarding ruling (project type optional/non-gating).

## 8. Acceptance Criteria

- A user can start a project by choosing **Start From Template** and selecting one of the **five** catalog templates.
- Selection **instantiates a populated sample project** — the worked sample is copied into **one editable Artifact** (`source="template"`); **no content is generated** by the system.
- The instantiated project is **flagged as a sample** (fictitious content clearly distinguished from the user's own data).
- The project's `project_type` is **pre-filled** from the template and remains **editable and non-gating**.
- The populated sample is **immediately analyzable** — Fast Pass runs on it on the **standard path**, producing a Project MRI within the **60-second** Time-to-First-MRI target.
- The artifact is **fully editable** in the Artifact Workspace; the user can adapt it into their own project or start a fresh blank project instead.
- **Fail conditions:** any system-*generated* starting content; a template that ships **empty or prompt-only** instead of a worked sample; a template choice that gates/locks behavior; a sample project not distinguishable from real data; users able to create/save templates in R1.

## 9. Out of Scope (Release 1)

- **Guided Intake** — deferred to **Release 2** (DL-056). The named-but-unspecified question flow (Capability Matrix §22 #4) is not built in R1.
- **User-created / "save project as template"** — deferred (DL-056 Q3; owner-curated only in R1).
- **AI-generated starting content** — remains out of scope (Onboarding OB-C3).
- Template **versioning UI**, marketplaces, or per-org custom catalogs.

## 10. Traceability

Capability Matrix V2 PF-02 / EI-03 (intake paths) · §22 #3 (resolved by this spec) · §22 #4 (Guided Intake → R2) · Onboarding Spec §L (templates moved from Deferred → in scope) · Master Spec §15A/§15B (Start From Template) · Logical Data Model §2.3 (Artifact). Authorized by **DL-056**.
