# Proposal / Disposition (DRAFT) — DL-053: Terminology Disambiguation (process-word collisions & semantic landmines)

> **Status:** **DRAFT · Pending Owner Ratification** — AI-drafted recommendation; ratifies nothing.
> Per `00_owner` `CLAUDE.md`: **preserve canonical terminology, do not introduce drift, do not resolve
> ontology conflicts unilaterally.** This proposal is **additive** — it *qualifies* colliding words; it does
> **not** redefine any existing canonical concept. Rename-grade calls are flagged ⚠ for explicit owner decision.
>
> **Proposed Decision ID:** **DL-053** · **Date drafted:** 2026-06-09 · **Layer:** Canon / ontology (terminology).
> **Origin:** Engineering-lead analysis (process-word collisions + semantic landmines) → owner review → this disposition.
> **Affects:** `00_owner/CANONICAL_GLOSSARY.md` (adds a Disambiguation Register section). No concept redefinition.

---

## 1. Problem

Several words carry **multiple distinct concepts** across three frames — OSLO-the-**product**'s behavior, the
**build/engineering** process, and the **repository governance** process. An autonomous builder reading the bare
word can conflate senses. The most dangerous instance: **"Authority"/"Governance"** — OSLO's *product* governance
(the Authority Plane) is **specified-but-INACTIVE in R1**, yet "governance" appears everywhere meaning build/repo
process (which *is* active). A builder can read it as a live product feature and **build the forbidden Authority
module** — a direct violation of the repo's #1 hard rule (`No Authority engine in R1`).

The glossary today enforces "one canonical term per concept." It does **not** yet handle the inverse —
**one word, many concepts.** DL-053 closes that gap with a **Disambiguation Register**.

---

## 2. Fix (additive; no redefinition)

Add a new section to `CANONICAL_GLOSSARY.md` — **"Disambiguation Register — one word, many senses."** For each
colliding word, register its distinct senses, each with a **canonical qualified name** and where it lives.
**Rule:** *never use the bare colliding word where the frame is ambiguous; use the qualified canonical form.*
The underlying concepts are unchanged — only a disambiguating qualifier is added.

### 2a. Process-word collisions (same word, different frame)

| Bare word | Sense → **canonical qualified name** | Frame / home |
|---|---|---|
| **Governance** | OSLO governing its own outputs → **Authority-Plane Governance** *(specified, INACTIVE R1)* | product · `10_product/domain`, `00_owner/doctrine` |
| | how engineering ships (CI gates, deploy) → **Build-Governance** | build · `00_owner/build_governance` |
| | how repo decisions get ratified (Framework 001 / DL-) → **Repository Governance** | repo-process · `00_owner/frameworks` |
| **Gate** | integrity-gated admission into canonical (Wave A) / inactive Authority gate → **Integrity Gate** | product |
| | CI gate · exit gate · owner gate · readiness gate → **Build Gate** | build |
| **Review** | OSLO CAF stakeholder review → **ReviewRequest (CRR)** *(already canonical)* | product |
| | governance review (Framework 001A) → **Governance Review** | repo-process |
| | code review → **Code Review** | build |
| **Decision** | OSLO governance-decision object → **Governance Decision (object)** | product |
| | ratified repo decision → **Ratified Decision (DL-)** | repo-process |
| **Authority** | OSLO Authority Plane → **Authority Plane** *(INACTIVE R1 — do not build)* | product |
| | owner's ratification right → **Owner Authority** | repo-process |
| **Validation** | OSLO validation response → **Validation (Recommendation type)** | product |
| | QA validation → **QA Validation** | build |
| **Acceptance** | user-attested acceptance → **UserAcceptanceRecord** *(already canonical)* | product |
| | NFR/outcome target met → **NFR Acceptance** | build/handoff |
| **State** | product maturity (Initial→Mature) → **Understanding State** *(already canonical)* | product |
| | machine status (`run_status`, `ConfidenceState`) → **run state** | engineering |
| **Policy** | OSLO product policies → **Product Policy** | product |
| | build constraints → **Build-Policy** | build (owner-ratified) |

### 2b. Semantic landmines (same word, unrelated / opposite meaning)

| Bare word | Sense A | Sense B | Recommended handling |
|---|---|---|---|
| **Canonical** | doctrine: "Canonical = Attested" (truth tier) | engineering: `canonical_key` (dedup hash) | Keep "Canonical" for the truth tier; **⚠ rename** the hash field to `dedup_key` (or keep `canonical_key` but never call the *act* "make canonical"). Owner call. |
| **Drift** | product: **Outcome Drift** — understanding changed, *surfaced as value* (a feature) | engineering: **Determinism Drift** / confidence inflation — *a bug to fail the build on* | Always qualify: **Outcome Drift** vs **Determinism Drift**. Bare "Drift" banned. |
| **Model** | **Domain Model** (e.g. `CONFIDENCE_MODEL` — conceptual, no formula) | **Data Model** (schema) · **Scoring Model** (the V2 formula) · **LLM model** (the AI) | Always qualify which: Domain / Data / Scoring / LLM. Bare "Model" banned in specs. |
| **Attested / Derived** | doctrine concepts (truth vs interpretation) *(canonical)* | `epistemic_state` field value | Concept stays capitalized **Attested/Derived**; the column is `epistemic_state`. |

---

## 3. Framework 001A Review

**Findings.** (1) The collisions are real and file-grounded (e.g. `GOVERNANCE_MODEL_V1` vs `*_GOVERNANCE_SPECIFICATION_V1`
vs `framework_001`; `No Authority engine in R1` vs ubiquitous "governance/gate"). (2) The risk is acute for an
autonomous builder — "Authority/Governance" can trigger building an inactive product feature. (3) The fix is
**additive** (qualifiers), so it carries near-zero drift risk and needs no concept redefinition.

**Concerns.** (1) **Rename-grade items are different in kind** — changing `canonical_key`, or renaming
`GOVERNANCE_MODEL_V1` → `AUTHORITY_PLANE_MODEL_V1`, *redefines a canonical surface* and must be an explicit owner
decision, not bundled silently (⚠). (2) The register must be **enforced**, or it's decorative — recommend the
doc-integrity checker add a WARN for bare colliding words in active specs (a follow-on, not this proposal).
(3) Scope discipline: this proposal **only adds the register + qualifiers**; it does not move files or rename
canonical artifacts.

**Dependencies.** `00_owner/CANONICAL_GLOSSARY.md` (add the register); optional follow-on CI rule; the realization→
app-repo relocation (separate proposal) would *reduce* collision surface but is **not** required for this fix.

**Recommendation.** **Adopt** the Disambiguation Register (§2a + §2b qualifiers) into the glossary as additive
canon. **Defer** the ⚠ rename-grade items (`canonical_key`, any `*_MODEL` artifact rename) to explicit owner
decision — list them, don't execute them. Optionally queue a CI-enforcement WARN as a backlog item.

**Status.** **DRAFT — pending owner ratification.** No glossary edit applied, no artifact renamed. AI does not ratify.

---

## 4. Owner decision

- **(A)** Ratify §2 register as additive glossary canon; defer the ⚠ renames to a later owner pass. *(Recommended.)*
- **(B)** Ratify §2 **and** decide the ⚠ rename-grade items now (tell me each call) → I fold them in.
- **(C)** Adjust specific rows, then ratify.

**⚠ rename-grade calls (owner only):** (i) `canonical_key` dedup field — keep vs rename to `dedup_key`;
(ii) whether `GOVERNANCE_MODEL_V1` / Authority-Plane artifacts get renamed to make the product/build split
structural; (iii) whether to ban bare "Model"/"Drift"/"Gate" in specs via CI WARN (enforcement).
