# Release 1 — Template Intake Specification v1

**Document Type:** Product experience specification (intake capability) · **Status:** 🟡 **Proposed — pending owner ratification (DL-056)** · **Date:** 2026-06-10 · **Zone:** `10_product` (product-authoritative)
**Authorizing decision:** DL-056 (scope ruling: **Start From Template → in scope for Release 1**; **Guided Intake → deferred to Release 2**).
**Resolves:** Capability Matrix V2 §22 #3 ("Templates referenced but undefined"). **Supersedes** the prior deferral of templates in `ONBOARDING_AND_PROJECT_CREATION_EXPERIENCE_SPECIFICATION_V1` §L.

> **Governance.** Proposed spec authored at owner direction; the owner ratifies via DL-056 merge (Authority Constraint). UX/interaction + content-structure only — it **computes nothing, generates nothing, governs nothing**; adopted template content is ordinary evidence the user owns and edits. Honors the onboarding invariant *"ingestion adds content only."*

---

## 1. Purpose

Give a user starting a project a faster on-ramp than a blank page by letting them **adopt a pre-authored planning document** as their first artifact, then edit it and run analysis exactly as with an uploaded or pasted artifact. Templates lower the activation cost of the **name + one artifact** minimum-to-value without OSLO ever generating content.

## 2. What a Template Is (and is not)

- A template is **owner-curated, pre-authored content** — a single planning document with headed sections and brief inline guidance prompts.
- Adopting a template **copies that content into the project as one editable Artifact**; the user then edits it freely.
- A template is **not** AI-generated, not a wizard/question flow (that is Guided Intake, R2), not a project-structure engine, and not user-creatable in R1.
- **Hard rule (carried from Onboarding OB-C3):** the system must not *generate* starting content. A template is **static pre-provided** content; copying it is not generation.

## 3. Form (DL-056 Q1 — single planning document)

Adopting a template produces **one Artifact** whose body is the template's pre-authored document: a set of **headed sections** (markdown), each with a one- or two-line **guidance prompt** the user replaces with their own content. It satisfies minimum-to-value (name + one artifact) on its own.

## 4. Catalog (DL-056 Q2 — curated five, owner-authored)

Release 1 ships **five** owner-curated templates. Each is a single planning document; section sets below are the R1 baseline (owner may refine the body copy before GA):

| Template | `project_type` pre-fill | Baseline sections |
|---|---|---|
| **Generic Project Plan** | `generic` | Intent / Outcome · Context · Scope (in/out) · Key Requirements · Milestones · Risks & Assumptions · Stakeholders |
| **Product / Software Launch** | `product_launch` | Outcome & Success Metrics · Target Users · Scope & Non-Goals · Requirements · Release Milestones · Dependencies & Risks · Stakeholders |
| **Marketing Campaign** | `marketing_campaign` | Campaign Goal · Audience · Channels & Messaging · Scope · Timeline & Milestones · Budget Assumptions · Success Metrics |
| **Event** | `event` | Event Goal · Audience & Attendance · Scope (program/logistics) · Timeline & Milestones · Vendors & Dependencies · Risks · Success Metrics |
| **Strategic Initiative (OKR/Plan)** | `strategic_initiative` | Objective · Key Results · Context & Rationale · Scope · Workstreams & Milestones · Dependencies & Risks · Stakeholders |

Catalog content is **canon** under `10_product/` (template bodies maintained as owner-curated source); engineering renders the picker and copies the chosen body in — it authors no template content.

## 5. Adoption Flow

```text
Choose Start Method → Start From Template
  ↓
Pick a template (catalog of 5; each shows name + one-line description)
  ↓
Project created with project_type pre-filled (non-gating; user-editable)
  ↓
Template body copied in as ONE editable Artifact (source = "template")
  ↓
User edits the artifact in the Artifact Workspace (adopt-and-edit)
  ↓
User starts analysis → standard Fast Pass (no special path)
```

Selecting a template is equivalent, downstream, to uploading/pasting a document — it joins the **standard intake → Fast Pass** pipeline with no template-specific analysis behavior.

## 6. Data & Epistemic Handling (canon-settled defaults)

- The adopted document is an ordinary **Artifact**: `source = "template"`, `template_id` recorded in `provenance`, `content_ref` = the copied body. Append-only/versioned like any artifact.
- It is an **evidence-class** artifact (analyzed like an upload). It carries **no special epistemic status**; OSLO self-attests nothing on adoption and **generates nothing**.
- Subsequent user edits follow normal artifact versioning and trigger event-driven Deep Pass like any edit.

## 7. `project_type` Behavior (DL-056 Q4 — pre-fill, non-gating)

Choosing a template **pre-fills the project's optional `project_type`** with the value in §4. It **never gates behavior** and the user may change or clear it, consistent with the ratified onboarding ruling (project type optional/non-gating).

## 8. Acceptance Criteria

- A user can start a project by choosing **Start From Template** and selecting one of the **five** catalog templates.
- Selection **copies the template body into one editable Artifact** (`source="template"`); no content is generated.
- The project's `project_type` is **pre-filled** from the template and remains **editable and non-gating**.
- The template artifact is **fully editable** in the Artifact Workspace and is **analyzed by Fast Pass on the standard path**.
- A template start **satisfies minimum-to-value** (name + one artifact) with no upload required.
- **Fail conditions:** any system-*generated* starting content; a template choice that gates/locks behavior; a template artifact treated as anything other than ordinary evidence; users able to create/save templates in R1.

## 9. Out of Scope (Release 1)

- **Guided Intake** — deferred to **Release 2** (DL-056). The named-but-unspecified question flow (Capability Matrix §22 #4) is not built in R1.
- **User-created / "save project as template"** — deferred (DL-056 Q3; owner-curated only in R1).
- **AI-generated starting content** — remains out of scope (Onboarding OB-C3).
- Template **versioning UI**, marketplaces, or per-org custom catalogs.

## 10. Traceability

Capability Matrix V2 PF-02 / EI-03 (intake paths) · §22 #3 (resolved by this spec) · §22 #4 (Guided Intake → R2) · Onboarding Spec §L (templates moved from Deferred → in scope) · Master Spec §15A/§15B (Start From Template) · Logical Data Model §2.3 (Artifact). Authorized by **DL-056**.
