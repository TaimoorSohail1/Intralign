# DL-095 — Findings to Issues user-facing label (RB-036)

- **Date:** 2026-07-08 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

- **Source:** Owner-directed R1 UX refinement, 2026-07-07. Proposal: `00_owner/decisions/PROPOSAL_FINDINGS_AS_ISSUES_USER_FACING_LABEL_DRAFT.md` (RB-036). Grounded in ISS-01 (*"Issues are user-facing; findings are first-class"*), the built 1:1 Issue projection (`evaluate/engine.py` `form_issue(f) for f in findings`; `issues` router), OVL-01 (overlays = findings-in-context), and the **DL-087** user-facing-label mechanism.
- **Layer:** `00_owner` (Disambiguation Register) + `10_product/experience` (Finding/Issue presentation). Presentation-only per DL-087.

## Decision (ratifiable text)

Adopt **"Issues" as the single user-facing label** for what is internally the **Finding** (first-class object; Infer), surfaced to users via the existing **1:1 Issue projection** (ISS-01). Retire user-facing **"Findings"** and **"weaknesses"**; both read as **"Issues."** Internal object model, code, analysis, and contracts are **unchanged** (presentation-only, per DL-087).

Add to the `CANONICAL_GLOSSARY` Disambiguation Register user-facing-label table:

1. **Issues / Issue** → **Finding** (first-class, Infer) surfaced via the 1:1 Issue projection (ISS-01, Evaluate). UI label; **Finding stays authoritative** in specs, code, contracts.
2. **Issue** (in place of **"weakness"**) → CAF-overlay "weak/weakness" language (OVL-01). UI label; inline overlays read as "Issues."

## Conditions

- **Presentation-only.** Finding remains the canonical first-class object; the Issue object remains its 1:1 prioritized projection. Nothing in the object model, Issue Engine, or contracts changes.
- **1:1 held for R1.** The relabel is valid because finding→issue is 1:1 today. Any future aggregation of findings into fewer issues is a **separate, deliberate decision** — explicitly out of scope.
- **Disambiguation precision.** The register entry must preserve the distinction that "Issue" is the *user-facing label* while "Finding" stays the internal first-class term (prevents terminology drift — the register's own purpose).

## Realization (landed with the decision)

Add the two register rows above; amend `FINDING_PRESENTATION_SPECIFICATION_V1` / `FINDING_PANEL_SPECIFICATION_V1` so the Finding Panel presents as the **Issue detail view** and user copy reads "Issues"; update IssuePanel/OvlPanel/Overview/MRI/export copy from "Finding"/"weakness" to "Issue." Confirm no contract keys on the user-facing string "Finding."

## Supersedes / Amends

Amends the `CANONICAL_GLOSSARY` Disambiguation Register (DL-087 label table) and the Finding presentation/panel specs (presentation only). No canonical model, doctrine, object, or contract superseded. Extends the DL-087 user-facing-label pattern.

## Pairing

Recommend ratifying and realizing **with RB-035** (finding-flow lifecycle simplification) — both touch the Issue surface; landing together avoids relabeling twice.

## Provenance

Owner direction 2026-07-07 (simplify UI labels; users see only "Issues," weaknesses read as issues). AI surveyed canon, confirmed the change is conformance to ISS-01 + the existing 1:1 Issue projection under the ratified DL-087 mechanism, and drafted this record. **AI drafted and recommended; the owner ratifies.** Number assigned at landing (DL-065 records discipline); effect on canon at owner merge.
