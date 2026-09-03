# Slice 2 prototype-parity design QA

Date: 23 July 2026

## Source of truth

- Golden prototype: `C:\Users\Hp\Downloads\oslo-knowledge-base-main\oslo-knowledge-base-main\oslo-product-grill\vertical-slices\slice-02-intake-fastpass-orientation\prototype.html`
- Reference captures: `C:\Users\Hp\Downloads\oslo-app\docs\design-qa\prototype-parity-audit`

## Verified states

- Fast Pass loading, including the scanner, four stages, live trace and timing note
- First-use orientation and account-menu replay
- Current and provisional Overview hierarchy
- Confidence read, CAF dimensions, issue list, progress and project summary
- OSLO advisor open and collapsed states
- Attention heatmap and issue investigation panel
- “Answer the first” clarification and Extended re-analysis trigger
- Desktop, tablet and mobile layouts
- Keyboard focus, reduced motion, refresh recovery and last-good behavior

## Visual comparison

| Area | Result |
|---|---|
| Dark OSLO palette and restrained orange emphasis | Passed |
| Loading layout, type hierarchy and stage feedback | Passed |
| Compact project navigation and desktop advisor rail | Passed |
| Confidence, Start here, Progress and More hierarchy | Passed |
| Attention heatmap and replacement issue panel | Passed |
| Four-part orientation modal | Passed |
| Responsive tablet and mobile reflow | Passed |

## Defects resolved during QA

- P1: orientation content could overflow on a mobile-height viewport; the overlay now scrolls safely.
- P2: the account menu remained visible behind the replayed orientation; opening orientation now closes it.
- P2: Overview density, advisor width, loading hierarchy and Attention spacing were aligned to the golden prototype.
- P2: the Attention count rendered on a second grid row; the navigation links now use a shared
  centered flex baseline, keeping the label and badge aligned.
- Remaining P0/P1/P2 visual defects: none found.

## Automated evidence

- Web unit/component tests: 14 passed.
- API tests: 84 passed.
- Slice 2 E2E: 3 passed across desktop, tablet and mobile.
- Slice 1 invite-to-Overview desktop regression: passed.
- Web lint: passed.
- API Ruff checks: passed.
- Next.js production build: passed.
- PostgreSQL issue-answer migration: applied locally.

final result: passed
