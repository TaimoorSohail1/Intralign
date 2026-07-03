# tools/ — repository integrity tooling

## `doc_integrity_check.py` — knowledge-integrity gate (KIA2-1)

The mechanical enforcement layer the Knowledge Integrity Audit (KIA-002) identified as the
**#1 lever** to move repository knowledge health into the upper-90s: it keeps the score there
*as the corpus grows*, rather than relying on human/agent vigilance.

### What it is (and isn't)
- **A read-only verification gate.** It runs automatically (CI on push/PR, or locally) and reports **pass/fail**.
- It **never** edits content, auto-fixes, merges, or deploys. It is the **detector, not the fixer** — flagged issues are fixed by a human or an agent under the normal governance (escalate-don't-invent, human review, human-only production). This preserves OSLO's "never autonomously writes" posture.

### What it checks
| Tier | Check | Policy |
|---|---|---|
| **ERROR** (fails build) | Broken internal doc links in the **active tree** (markdown + `` `backtick.md` `` refs), resolving the repo's bare-filename convention. Prose/glob/ellipsis/shorthand patterns and the reasoning/governance trail (decisions, changelog, research, audits) are exempt — they legitimately cite history. |
| **WARN** (reports) | (a) Active-tree docs referencing a **superseded/legacy/historical** doc; (b) **retired terminology** in the active tree (`Judgement Layer`, `Context Plane`, `Outcome Management`); (c) **stale operative-DL-range** claims vs the actual ledger max. |

### Run it
```bash
python3 tools/doc_integrity_check.py            # errors fail; warns report
python3 tools/doc_integrity_check.py --strict   # warns fail too (use after the warn backlog is cleared)
```

### CI
`.github/workflows/doc-integrity.yml` runs it on every push/PR to `main`. A broken active-tree link **fails the build**; warnings are surfaced in the log as a cleanup worklist (these feed the KIA2-2 residue-archival work). Flip to `--strict` once warnings reach zero to lock the upper-90s in.

### Tuning
Allowlists and the retired-term list live at the top of the script (`HIST_REF_ALLOW`, `BANNED`).
Keep the **ERROR tier near-zero-false-positive** so a red build always means a real problem.
