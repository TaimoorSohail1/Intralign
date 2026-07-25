# Slice 4 Design QA

## Reference

- Golden prototype: `slice-04-attention-map/prototype.html`
- Implementation: `http://localhost:3000/projects/1950a68e-0a85-4fb8-a5c3-0ebe76d5c751/attention`
- Comparison state: desktop Attention Map using the current published analysis snapshot
- Comparison viewport: identical in-app browser viewport for both captures
- Reference capture: `.qa-slice4-prototype.png`
- Implementation capture: `.qa-slice4-implementation.png`
- Side-by-side capture: `.qa-slice4-side-by-side.png`

## Verified

- Fixed seven-artifact by three-dimension matrix with Understanding and Execution grouping
- Calm, Warning, Moderate and Critical visual hierarchy with count and multi-finding markers
- Single-finding cells open issue detail directly
- Multi-finding cells open a scoped list before issue detail
- Artifact rows open scoped finding lists and removable scope chips
- Contextual OSLO entry points for the map, cells, scopes and issues
- Current-snapshot-only semantics: resolved findings are excluded while open and addressed remain
- Natural all-clear state when the current read has no unresolved findings
- Keyboard activation, focus management, escape behavior and reduced-motion treatment
- Responsive desktop and mobile layouts
- Overview navigation preserves the user’s prior scroll position

## Intentional differences

- Prototype-only release preview and simulation controls are omitted.
- Counts, severities and issue copy come from the live current analysis snapshot rather than prototype fixtures.
- Reports, sharing, export and plan-upgrade surfaces remain later-slice capability seams.
- The implementation adds a visible map-level OSLO action while preserving the prototype’s contextual cell actions.

## Automated evidence

- Web component suite: 34 tests passed
- Slice 4 Playwright desktop flow: passed
- Slice 4 Playwright mobile flow: passed
- ESLint: passed with zero warnings
- Production build and TypeScript validation: passed

final result: passed
