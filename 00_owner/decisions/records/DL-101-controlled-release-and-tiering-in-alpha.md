# DL-101 — VOID (duplicate of DL-102; landed outside the serializer)

- **Date:** 2026-07-10 · **Status:** Void · **Decided by:** — (never ratified)
- **Class:** A

## Decision

**Void. This record carries no decision content.**

**See `DL-102-controlled-release-and-tiering-in-alpha.md` — Controlled Release & Tiering-in-Alpha — which is the decision of record.**

## Why this record exists

DL-101 carried the **same decision content** as DL-102. It was **hand-authored and hand-numbered by an AI contributor from a stale local clone**, then merged via PR #137 — a **breach of DL-065 §5**:

> *"One serializer. The Founder Console is the sole path that authors, numbers, and releases decisions to `main`. No parallel stream merges canon."*

It was also **incomplete under Framework 001**: it never received a **Changelog Entry**, the final step of the lifecycle (Backlog → Proposal → Review → Decision → Repository Change → **Changelog Entry**).

Separately, while it sat open it had to be renumbered twice — drafted DL-099, renumbered DL-100, then DL-101 — as other decisions landed beneath it. That is **exactly the failure the `dl-land` workflow (DL-067) exists to prevent**, per its own header: *"Numbering happens here, off current `main`, so a stale local clone can never mis-number (the failure this workflow prevents)."*

The decision was re-landed correctly through the serializer as **DL-102** (changelog **CHG-136**), which **voids this record**.

**Retained rather than deleted**, so that the breach — a parallel stream briefly merging canon — stays inspectable in the decision history. The number **DL-101 is permanently retired** and must not be reused.

## Supersedes / Amends

- **Superseded by:** `DL-102` (Controlled Release & Tiering-in-Alpha).
- **Supersedes:** nothing.
- **Affected artifacts:** none — all decision content lives in DL-102.
