# R2 integrity header design QA

Date: 2026-08-18

Viewport: 1280 × 720

Scope: shared R2 Outcome Integrity header, maturity rail, collapse control, and maturity explanation disclosure.

## Reference and implementation

- Prototype, expanded: `01-prototype-expanded.png`
- Prototype, disclosure open: `02-prototype-disclosure-open.png`
- Implementation, expanded: `03-implementation-expanded.png`
- Implementation, disclosure open: `04-implementation-disclosure-open.png`
- Same-state comparison: `05-open-comparison.png`

## Verification

- The limiting-pillar sentence and Collapse control retain a 12 px gap and do not overlap.
- The maturity rail has one explicit Fragile/Sound label pair; duplicate pseudo-element labels are removed.
- “Why a maturity read, not a probability?” opens inline in normal document flow, matching the prototype interaction.
- The disclosure no longer floats over the issue list or navigation.
- With the disclosure open, the content grid begins at the integrity header boundary.
- Closing the disclosure restores the compact expanded-header state.
- The layout has no horizontal overflow at 1280 × 720.
- The interaction remains a native keyboard-accessible `details`/`summary` disclosure.
- Focused component regression test passed.

Final result: passed
