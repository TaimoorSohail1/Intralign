# App code lives in `code/` inside the knowledge base

The ratified default (DL-044, starter-kit README) is a separate, owner-owned `oslo`
application repo, kept apart from this constitutional knowledge base. We instead placed
the application under `code/` in the knowledge-base repo, as a monorepo, to move faster
while the build is small and the canon and code change together.

This is a deliberate deviation from canon. It contradicts "the knowledge base is not a
software project" and the DL-051 ownership-zone taxonomy, and it changes the Deployment
Governance model (branch protection / CI gates were designed for the app repo). It is a
**time-boxed deviation**, not a retirement of the separate-repo default: the empty
`idris-manley/oslo` repo remains the ratified destination.

## Status

**Ratified with conditions** — owner, via **DL-057** (2026-06-13); reaffirmed at the
Phase III / Wave B authorization gate (owner, 2026-06-16). Supersedes the prior
`proposed — pending owner ratification` state. AI records; the owner ratified.

## Conditions (DL-057)

1. **Zone declaration:** `code/` is **engineering-authoritative, non-canonical** (DL-051
   appendix; `ZONE_GROUNDING_RULES.md` amended). Nothing under `code/` is canon.
2. **Doc-integrity isolation:** the doc-integrity gate excludes `code/`; app-ci stays
   path-scoped to `code/**`. Neither gate weakens the other.
3. **Review-authority split:** CODEOWNERS assigns `/code/` to engineering review; owner
   review applies to canon zones; per-wave build authorization and production deploy
   (Gate 8) stay owner-gated; branch protection on `main` stays ON.
4. **Extraction trigger (binding):** `code/` extracts to the `oslo` repo at the **earlier
   of** (a) the Release 1 exit gate, or (b) a second regular committer/agent on `code/`.
   Pre-authorized; execution needs only a changelog entry, no new proposal.

## Consequences

- CI gates run scoped to `code/**`, not the whole repo (condition 2).
- The documented reversal path is retained: `code/` extracts cleanly to an `oslo` repo (it
  is already self-contained — its own `pyproject.toml`, `CLAUDE.md`, `CONTEXT.md`,
  `docs/adr/`). The extraction trigger above makes that reversal a scheduled event, not an
  open question.
