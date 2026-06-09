# UI-to-Inference Decision Table v1.1

---

**Purpose**

Defines the **binding contract** between UI actions and OSLO inference behavior, including effects on:

- human-readable artifacts
- canonical representation
- judgment and scoring

---

## **How to read this table**

- **Inference Mode** controls whether OSLO may infer/expand.
- **Human-Readable Impact** describes what appears in artifacts.
- **Canonical Impact** describes what becomes structured meaning.
- **Judgment Impact** describes scoring and issue behavior.

---

## **A. Onboarding & Draft Creation (Corrected)**

| **UI Action** | **Inference Mode** | **Human-Readable Impact** | **Canonical Impact** | **Judgment Impact** |
| --- | --- | --- | --- | --- |
| Paste free-text project description | Assisted Expansion | OSLO generates **full draft artifacts across default workflow** (Intent → Context → Scope → Requirements → WBS → Resource Plan → Schedule), all labeled *inferred* | Canonical objects/edges created with source_state = inferred | Discounted; issues expected |
| **Upload documents (PRD, Charter, Decks, Notes, PDFs)** | **Assisted Expansion** | **OSLO generates full draft artifacts across default workflow using documents as semantic input (not partial mappings)**; all content labeled *inferred* | **Inferred canonical snapshot derived from document meaning** | **Discounted; issues expected** |
| Click “Draft a plan with AI” | Assisted Expansion | Full draft artifacts generated, labeled *inferred* | Inferred canonical snapshot | Discounted; confidence reduced |
| Start blank plan (no AI) | Pass-Through | Empty artifacts | Canonical empty | Issues for gaps |

> Rule:
> 
> 
> **all unstructured inputs**
> 
> **semantic intent signals**
> 
> **no parse-only onboarding path**
> 

---

## **B. Structured Field Entry (Any Phase)**

| **UI Action** | **Inference Mode** | **Human-Readable Impact** | **Canonical Impact** | **Judgment Impact** |
| --- | --- | --- | --- | --- |
| Fill a structured form field | Pass-Through | Field saved exactly as typed | Explicit canonical update | Full weight |
| Edit specific fields | Pass-Through | Only edited fields change | Incremental canonical delta | Local re-score |
| Bulk paste into structured fields | Pass-Through | Fields populated as explicit | Deterministic derivation only | Full weight |
| Save with all required fields present | Pass-Through | No augmentation | Explicit canonical | Stable |

---

## **C. Steady-State Edits (Post-Onboarding)**

| **UI Action** | **Inference Mode** | **Human-Readable Impact** | **Canonical Impact** | **Judgment Impact** |
| --- | --- | --- | --- | --- |
| Edit field via standard UI | Pass-Through | Edited field explicit | Incremental delta only | Local impact only |
| Edit WBS node | Pass-Through | Node updated | Tree revalidated | Local issues only |
| Change milestone date | Pass-Through | Date updated | Dependency checks | Schedule-only |
| Remove linkage | Pass-Through | Link removed | Orphan detection | Issues raised |

---

## **D. Explicit AI Invocation (Opt-In)**

| **UI Action** | **Inference Mode** | **Human-Readable Impact** | **Canonical Impact** | **Judgment Impact** |
| --- | --- | --- | --- | --- |
| Click “Ask OSLO to update related artifacts” | Assisted Expansion | OSLO proposes drafts (labeled *inferred*) | Inferred canonical additions | Discounted |
| Use “Draft with AI” section | Assisted Expansion | AI writes within scoped area | Inferred within scope | Discounted |
| Accept OSLO suggestion | Promotion Path | New artifact version; fields become explicit | Canonical upgraded | Full weight |
| Reject OSLO suggestion | Pass-Through | No change | No change | No change |

---

## **E. Validation-Driven Scenarios**

| **UI Action** | **Inference Mode** | **Human-Readable Impact** | **Canonical Impact** | **Judgment Impact** |
| --- | --- | --- | --- | --- |
| Save with missing required fields | Gap-Flagging | Fields remain empty | Canonical incomplete | Issues raised |
| Break invariant (e.g., WBS cycle) | Gap-Flagging | Save blocked or flagged | Canonical rejected | No score change |
| Resolve issue manually | Pass-Through | Explicit fix | Canonical updated | Score may improve |

---

## **F. Governance & Enterprise Controls**

| **UI Action / Policy** | **Inference Mode** | **Human-Readable Impact** | **Canonical Impact** | **Judgment Impact** |
| --- | --- | --- | --- | --- |
| Enterprise policy: no AI drafting | Pass-Through only | No AI content allowed | Explicit-only canonical | Full weight |
| Governance allows auto-proposals | Assisted Expansion (scoped) | Proposals labeled *inferred* | Inferred canonical | Discounted |
| Lock artifact for review | Pass-Through | Read-only | No changes | No change |

---

## **G. Reports & Read-Only Views**

| **UI Action** | **Inference Mode** | **Human-Readable Impact** | **Canonical Impact** | **Judgment Impact** |
| --- | --- | --- | --- | --- |
| View report (auth / anon) | N/A | Read-only snapshot | None | None |
| Comment on report | N/A | Comment stored | No canonical change | None |
| Share report version | N/A | Version-bound snapshot | Bound to versions | None |

---

## **Global Hard Rules (Enforced Everywhere)**

1. **No silent inference**
2. **Inference requires explicit UI intent or policy**
3. **All inferred content is labeled**
4. **Inferred content cannot improve scores**
5. **Promotion requires explicit confirmation + new version**

---

## **Canonical one-liner**

> UI intent determines inference mode: onboarding inputs trigger Assisted Expansion; standard edits are pass-through; canonical meaning never expands without permission.
> 

If you want next, I can:

- add **endpoint-level guards** (API → inference mode),
- produce **CI assertions** for onboarding uploads vs edits, or
- generate a **designer checklist** to ensure UI affordances map correctly to inference modes.