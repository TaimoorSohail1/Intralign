# All LangGraph orchestration lives in one `backend/orchestration/` folder

The ratified code-tree names no home for LangGraph or durable runs, even though the
environment profile (§1) mandates both. Rather than scatter a `graph.py` into each of the
eight responsibility modules, we put all workflow wiring — StateGraphs, the durable
checkpointer, the run registry, and the runner — in a single top-level
`backend/orchestration/` folder. Domain logic stays in the responsibility modules; a graph
node is thin and delegates to a responsibility.

This separates *wiring* (orchestration) from *work* (responsibilities). It gives one
place to read the whole workflow (the stated goal: avoid over-modularity) without breaking
hard rule #1 — orchestration is a conductor, not a producer, so every governed output is
still produced in exactly one responsibility.

## Status

accepted

## Considered Options

- **`graph.py` per responsibility** — rejected: scatters one workflow across eight folders;
  no single place to read the flow; the over-modularity we set out to avoid.
- **`backend/services/orchestration/`** — rejected: smaller deviation, but buries the most-
  opened folder and reads as a leaf service rather than the peer-of-responsibilities conductor.

## Consequences

- `backend/orchestration/` is a deviation from the literal ratified tree (which names no
  orchestration home); recorded here so it isn't "tidied" back into the responsibilities.
- The durable checkpointer binds to Supabase Postgres via `services.persistence` (DL-054).
