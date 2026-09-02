# Unrecorded decisions — cited canon with no record

**Zone:** `00_owner/decisions/` — owner-governed.

**What this file is:** the enumerated, dated list of `DL-` ids that **canon on `main` cites but cannot
resolve.** It exists so the gate in `tools/dl_records.py` can fail a PR for any citation that is *not*
on this list, while the debt already incurred stays visible instead of hidden.

⚠️ **This is a debt register, not an exemption.** An id on this list is a defect that has been
measured, not a citation that has been approved. **Nothing may be added without an owner
ratification**, and the only correct way to remove a row is to make the record resolve.

---

## Why it exists

**Measured on `main` at `a2c1732`, 2026-08-23: 172 `DL-` ids are cited; 161 resolve; 11 do not —
across 50 citations.** `doc_integrity` passed on all 1120 documents throughout.

Two of those citations were caught by hand the same day, hours apart:

1. **Framework 002** had been cited by section number since 2026-08-14 and was never written
   (ratified fresh as `DL-241`).
2. **The pillar triad** was about to be entered in `CANONICAL_GLOSSARY.md` citing `DL-195 §1/§2/§3/§6`
   — a spec the project's own R2 decision index records as *"key calls ratified, spec unfinished."*

⚠️ **The second instance is why this is a mechanism rather than a third note.** A citation that
resolves to nothing should fail a PR exactly as a missing ripple section does (Framework 002 §8b).

---

## ⚠️ These are TWO defects, not eleven

**Measured per id against both lines, 2026-08-23.** The split decides the remedy, so it is stated
before the rows.

| | count | what is true | remedy |
|---|---|---|---|
| **A · Graduation debt** | **6** | the record **exists** — on the R2.1 design line — and has never reached `main` | **graduate the record.** No new canon is authored. |
| **B · Genuinely unwritten** | **5** | no record on **either** line | **write it, or retire the citation.** Requires an owner ratification. |

⚠️⚠️ **Class A is one defect with six instances, and it is the topology question.** `DL-235` §9 declares
`main` the only delivery truth while `DL-235`'s own record is not on `main`. **Do not open six fixes.**
It belongs to the SDLC / branching work.

---

## A · Graduation debt — the record exists on the design line

| DL | cited | what it is | where the record is |
|---|---|---|---|
| **DL-235** | 14× | two lines, one truth — `main` is the only delivery truth | `00_owner/decisions/records/DL-235-framework-002-section-9-two-lines-one-truth.md` ⚠️⚠️ **the decision declaring `main` the only delivery truth is itself absent from `main`** |
| **DL-228** | 5× | corrective vs evolutionary | `release-2/canon/decisions/DL-228_CORRECTIVE_VS_EVOLUTIONARY.md` |
| **DL-230** | 5× | deferred ships no governed behaviour | `00_owner/decisions/records/DL-230-deferred-ships-no-governed-behaviour.md` |
| **DL-227** | 4× | two trains — delivery and design | `release-2/canon/decisions/DL-227_TWO_TRAINS_DELIVERY_AND_DESIGN.md` |
| **DL-231** | 2× | *engaged* re-ratified fresh; engagement is server-derived | `00_owner/decisions/records/DL-231-engaged-re-ratified.md` ⚠️ cited as the governing **precedent for fresh re-ratification**, including by `DL-241` |
| **DL-162** | 2× | durable funnel/event telemetry | `release-2/canon/decisions/DL-162_FUNNEL_TELEMETRY.md` — already carries its own *"back-reconstruction, not the authoritative original"* warning |

⚠️ **Two of the six sit in `release-2/canon/decisions/` under an UPPER_SNAKE filename**, which the
canonical `DL-nnn-slug.md` pattern does not match. That is a fourth decision home, and it is why
`next_number()` once returned an id already in use.

---

## B · Genuinely unwritten — no record on either line

| DL | cited | what it is | status |
|---|---|---|---|
| **DL-212** | 12× | Framework 002's founding decision | ⚠️ **wording UNRECOVERABLE.** Superseded in effect by `DL-241`, which ratifies the framework directly. Must **never** be reconstructed from downstream citations — that is how `DL-162` earned its warning. **This row is permanent.** |
| **DL-220** | 3× | graduation ripple must be generated, not hand-maintained | ⚠️⚠️ **cited inside `.github/workflows/doc-integrity.yml` — a live, blocking gate enforces a decision that has no record anywhere.** The gate is real; its authority is not written down. |
| **DL-195** | 1× | pillar triad · Adaptability checkpoint-optimization | ⚠️ R2 decision index: *"key calls ratified, **spec unfinished**."* `CANONICAL_GLOSSARY.md`'s `Pillar` row cites it **and says so**. ⚠️ **No section number may be cited until the spec is written.** |
| **DL-194** | 1× | integrity indicator, 3-state | ⚠️ R2 decision index: *"record is scribe-drafted"* — flagged **confirm ratification**. |
| **DL-157** | 1× | — | ⚠️ **no record on either line and no index entry.** Cited once, by `DL-238`. **Identify it or remove the citation.** |

---

## ⚠️ How this list may change

**Removing a row** — make it resolve (write the record, or graduate it), and drop the row in the same
PR. `python3 tools/dl_records.py citations` reports which rows have become resolvable.

**Adding a row** — requires an owner ratification. ⚠️ **A PR that adds a row to turn a red gate green
is the exact failure this register exists to prevent.** The correct response to a red citation gate is
to write the record.

---

## C · Index-catalogued but not ratifiable — the `[R]` marker withdrawn 2026-09-02

**Owner ratification 2026-09-02**, alongside the ruling that a declared index resolves a citation
(`PROPOSAL_r2-decision-records-exist-only-as-index-entries.md` §6). Two index rows carried the `[R]`
marker while their own text disqualified them. The marker was withdrawn and the debt recorded here.
⚠️ **These rows did not turn a red gate green — they replace an authority that should not have
existed.** Before this change all six ids resolved through the index; the gate was already green. The
debt was invisible, not absent.

| DL | cited by | what it is | why it may not resolve |
|---|---|---|---|
| **DL-199** | the proposal, describing its own closure | owner activation = first grounding act | **CLOSED 2026-08-14**, absorbed into DL-205 §0/§0a. The index row (2026-08-09) predates the closure and still answered for it. Writing a DL-199 record would contradict a closed owner decision — **this citation is correct and must stay unresolved.** |
| **DL-200** | the proposal; `tools/dl_records.py` commentary | DR-1 outcome-first | the index row's own status column reads **"DRAFTS for ratification"**. A draft may not be a citation authority. |
| **DL-201** | the proposal | DR-2 enforce via commitment gate | as DL-200 |
| **DL-202** | the proposal | DR-3 integrity indicator | as DL-200 |
| **DL-203** | the proposal | DR-4 phased resolution | as DL-200 |
| **DL-205** | the proposal §1c; `tools/dl_records.py` commentary | DR-6 activation = 2nd act; absorbed DL-199 | as DL-200 — and §1c cites it substantively, so a placeholder would destroy the claim rather than record it |

**Remedy — one act, not six:** ratify DR-1…DR-6 as formal records. Every row above clears together and
`[citation-debt-paid]` will say so on the next run. ⚠️ **Do not restore the `[R]` marker to clear them.**
That is this register's own failure mode, one level up: not a row added to go green, but an authority
restored to go green.

`MEASURED-BY:` `python3 tools/dl_records.py citations`, clean worktree, corpus staged — index
resolutions fall **16 → 10**, rc=0. **RED-proved:** deleting the DL-205 row alone returns
`[citation-unresolved] DL-205 … (the proposal, tools/dl_records.py)`, rc=1.

★ **Five of the six are cited only by documents ABOUT the citation machinery.** `CITE_RE` cannot
distinguish a mention from a citation, so the documents most likely to name an id are the ones
explaining how ids resolve. **Third instance 2026-09-02**, after the fabricated id narrated inside the
proposal's own RED-proof. ⇒ **the mention-vs-citation distinction needs a mechanism, not a third
placeholder.** The shape already exists in #284: declare the path in a manifest, default-deny, an
undeclared file still scanned, a declaration resolving to nothing an ERROR.
