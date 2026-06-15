# App code lives in `code/` inside the knowledge base

The ratified default (DL-044, starter-kit README) is a separate, owner-owned `oslo`
application repo, kept apart from this constitutional knowledge base. We instead placed
the application under `code/` in the knowledge-base repo, as a monorepo, to move faster
while the build is small and the canon and code change together.

This is a deliberate deviation from canon. It contradicts "the knowledge base is not a
software project" and the DL-051 ownership-zone taxonomy, and it changes the Deployment
Governance model (branch protection / CI gates were designed for the app repo). It is
**not** owner-ratified — it needs to be recorded as a decision and ratified, or reversed
by extracting `code/` into its own repo. AI cannot ratify; only the owner can.

## Status

proposed — pending owner ratification

## Consequences

- CI gates from `starter_kit/ci-pipeline.yml` must run scoped to `code/`, not the whole repo.
- If reversed, `code/` extracts cleanly to an `oslo` repo (it is already self-contained:
  its own `pyproject.toml`, `CLAUDE.md`, `CONTEXT.md`, `docs/adr/`).
