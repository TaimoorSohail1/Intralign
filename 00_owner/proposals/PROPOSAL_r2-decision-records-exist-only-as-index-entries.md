# PROPOSAL — The R2 decision series exists as an INDEX, not as records, and that blocks every graduation

**Raised:** 2026-09-02, from the DL-210 graduation (link 2 of the chain that would let #220 cite R8).
**Class (anticipated):** to be ruled. Touches no doctrine and no contract; it decides how the R2 decision
series reaches the control plane.
**Status:** BACKLOG → PROPOSAL. **Not resolved unilaterally. AI drafted; owner ratifies.**

---

## 1 · The finding

Graduating the DL-210 record to `00_owner/decisions/records/` fails the citation gate. Following the
failure to its end produces the real result:

**The R2 decision series was maintained as an index plus a readjudication worksheet, and only some of its
entries were ever promoted to standalone record files.** `dl_records.py` resolves citations against
**record files only**, so every index-only decision reads as *"resolves to no record."*

**MEASURED-BY** — iterative closure: add the DL-210 record, run `tools/dl_records.py citations` against
the **staged** corpus, graduate every cited record that exists on any ref, repeat.

| Round | Records added | Still unresolved |
|---|---|---|
| 1 | DL-184, 193, 196, 197, 209, 215 | 7 |
| 2 | DL-172, 206, 214 | 13 |
| 3 | DL-158, 211, 213 | 13 |
| 4 | DL-201, 219 | 13 |
| 5 | DL-200, 202, 216 | 14 |
| 6 | DL-203, 204, 205, 208 | 14 |

**22 records graduated; the closure does not converge.** 14 ids remain, and they are three different
things — which is the reason this is a proposal and not a bug report.

### 1a · Twelve are catalogued, never promoted

`DL-164 · 171 · 173 · 179 · 180 · 181 · 182 · 183 · 189 · 190 · 191 · 192`

Every one appears in `release-2/R2_DECISION_INDEX_PHASE_A.md` and/or
`release-2/canon/decisions/R2_DL_READJUDICATION_WORKSHEET.md` — between **1 and 10 mentions each**. They
are catalogued canon without record files.

⚠️ **The first draft of this finding said these were "decisions that exist nowhere in the repository."
That was wrong**, and it was wrong in the direction that would have caused the most damage — it invited
reconstruction of records that are already catalogued. The correction came from reading `RB-055` instead
of reasoning from a filename sweep.

### 1b · DL-198 is a ratified renumber that was never executed

`RB-055` records it: **DL-172 → DL-198** (freemium / value moments), ratified **2026-08-04**, deliberately
queued rather than done, with a machine-checkable trigger (`stack-empty` AND the old filename present).
DL-201 and DL-202 already cite **DL-198** while the file is still `DL-172_…`. **One decision, two live
numbers** — RB-055's own words. Not a gap; an unexecuted, correctly-deferred change.

### 1c · DL-199 is closed and must not be written

**Owner-closed 2026-08-14.** A **reserved number, never issued**; the ratified owner-activation content
was absorbed into **DL-205 §0/§0a**. Writing a DL-199 record would contradict a closed owner decision.

---

## 2 · Why it matters beyond DL-210

**No R2 decision can graduate to `main` in isolation.** Any one of them drags its citation closure, and
the closure terminates only at index-only entries. This is the same shape as R8: the record was never
missing, it was never *reachable* — one level down and across a whole series.

⚠️ **`20_handoff/QUEUED_WORK.md` is NOT on `main`**, yet `tools/queued_work_check.py` evaluates it on
every push to `main`. RB-055's deferral is therefore invisible to the control plane that is supposed to
enforce it. That is the checker-and-subject-on-different-branches family again (RB-076 · RB-106 · RB-125),
and it should be ruled with this proposal rather than after it.

---

## 3 · Options (owner ruling required — I recommend C)

**A · Promote all twelve to record files.** Complete and slow. ⚠️ Each would be *authored from an index
entry*, which is reconstruction — the thing C-2 forbids. Only viable if the index entries are themselves
substantive enough to be the record, which must be read before it is assumed.

**B · Enter the twelve in `UNRECORDED_DECISIONS.md`.** The register exists for exactly this. ⚠️ But the
gate's own error text names an added row as *"the failure the register exists to prevent"*, and a row
asserting "no record" would be false — they are catalogued. This needs the register's semantics ruled
before it is used, not after.

**C · Rule that an INDEX ENTRY IS A RESOLVABLE RECORD, and teach the resolver.** ⭐ The index is where
this series was actually maintained; the gate simply cannot see it. Extend `dl_records.py` to resolve a
citation against a decision index as well as a record file, with the index named explicitly rather than
by glob. **Extend, don't mint** — and it makes the corpus honest instead of making the gate quiet.
⚠️ Must be RED-proved in both directions: a citation to an id absent from *both* must still fail.

**Not in scope for any option:** DL-198 (execute RB-055 on its trigger) and DL-199 (closed; leave it).

---

## 3a · Option C, built and measured — and why it must NOT ship as drafted

The mechanism is implemented in `patches/05-index-entry-resolves-a-citation.patch` (132 lines):
`DECISION_INDEX_RELS` (**declared, never globbed**), `INDEX_ROW_RE` (a **structured row**, not a mention),
`indexed_ids()`, and four self-test cases. **RED-proved five ways** — an indexed id resolves; an id absent
from the index still fails; a bare *mention* still fails; a declared-but-absent index fails closed; and on
the real corpus a fabricated `DL-NNN` still fails while the tree is otherwise green.

**Measured result: the closure converges at ROUND 1 with TWO files** — the index and the DL-210 record.
The 22 record graduations are unnecessary. 47 citations resolve through index entries, each announced by
a `[citation-indexed]` notice so the shape stays visible.

⚠️ **And it must not ship in this form.** Reading the index rather than trusting the measurement:

1. **The first row records ABSENCE and would be read as resolution:**
   `| DL-157, 159, 160, 161, 163 | **Occur nowhere** — no record, no reference, on any branch or in
   history |`. Resolving a citation against a row that exists to say *this decision does not exist* is
   the same defect as the 08-17 file citing artifacts without `.md` to mark them absent. **A row that
   records absence must never resolve.**
2. **Multi-id rows resolve only their first id** — `DL-157, 159, …` and `DL-200–205` catalogue several
   decisions; `INDEX_ROW_RE` captures one. Arbitrary, and arbitrary is not a rule.
3. **Nine of 53 rows are not ✅** — 5 are ⚠️ *needs owner action*, 4 are ⛔ *do-not-land*. Whether a
   deferred or retired decision resolves a citation is a ruling, not an implementation detail.
4. **The index is AI-assembled**: *"Author: AI (assembled from ratified sources; owner ratifies the ⚠️
   rows)"*. Making it a citation authority promotes AI-assembled content to resolving canon — the same
   act as C-13, and it needs the same explicit ratification.
5. **Its header is stale.** It states `decision_log.md` *"today tops at DL-156"*. Measured on `main`:
   the log reaches **DL-242**, with **101 record files** up to **DL-243**. Written 2026-08-09 and not
   re-measured since.

⇒ **Option C′ (what I now recommend):** adopt index resolution, but require an **explicit per-row
resolvable marker** rather than inferring from row shape, exclude absence rows by construction, and rule
separately on ⚠️ and ⛔ dispositions. That makes the index say what it means instead of the resolver
guessing — and the index is AI-authored, so adding the marker costs a ratification, not a rewrite.

⚠️ **Executing Phase B does not solve this.** `recorded_ids()` resolves by **FILENAME** across the record
homes, and reads `decision_log.md` only for the frozen legacy range (≤ DL-064). Appending the delta to the
log would not resolve one citation. Worth stating because the index's own purpose line invites exactly
that assumption.

---

## 4 · Review — the five outputs

- **Findings.** The R2 series is index-maintained; 22 records graduate cleanly; 12 ids are index-only;
  DL-198 is a deferred renumber; DL-199 is closed. The DL-210 graduation is blocked, not broken.
- **Concerns.** Option A risks reconstructing canon. Option B risks recording a falsehood to turn a gate
  green. Option C changes a gate and must be proved red before it is trusted green.
- **Dependencies.** `canon/dl-210-graduation` (branch reset to `origin/main`, nothing pushed) ·
  `canon/graduate-owner-rulings-2026-08-17` (#pushed, red, must not merge) · `canon/dl-214-graduation`
  (`faa0438`, clean, independent of this) · RB-055's trigger · `QUEUED_WORK.md`'s absence from `main`.
- **Recommendation.** **Option C**, with the `QUEUED_WORK.md` locus ruled alongside it.
- **Status.** **RULED 2026-09-02 — see §6.** Option C adopted **with an amendment**; the dependencies
  above are superseded by §6a, three of them having been measured false.

---

## 5 · How this was nearly missed, and the mechanism

The chain was reported as *"verified end-to-end, rc=0"* earlier the same day. **That verification was
void.** The files were copied into a working tree **untracked**, and `dl_records.py` enumerates the
**tracked corpus** — `git ls-files`, as its own comment states: *"THE SUBJECT IS THE TRACKED CORPUS, NOT
THE FILESYSTEM."* An untracked file is never scanned, so `PASS` meant **not examined**, not **clean**.
RED-proved afterwards: identical file, untracked → `PASS`; staged → `FAIL (8 citation errors)`.

⇒ **A verification must place the subject where the checker looks.** For any gate that reads the tracked
corpus, the simulation must `git add` before it asserts anything — and a green result on a corpus the
gate never enumerated is indistinguishable from a green result on a clean one. **Third instance today of
a check that could not fail; the mechanism adopted is that graduation scripts gate a COMMIT in a clean
worktree, never a working directory.**

---

## 6 · OWNER RULING — 2026-09-02

**RULED: Option C is adopted, AMENDED — a declared index resolves a citation, and a declared index may
not cite itself.** Decided by Idris (Founder Console), 2026-09-02. Merging this branch is the
ratifying act.

**The amendment, and why it was needed.** As drafted, Option C admitted the index to the corpus as both
authority and citer. Measured on the merged chain: **45 of 51 resolutions were the index citing its own
rows** — demand the document authored for itself. Only **six** ids had a citer outside the index
(`DL-209 · DL-210 · DL-211 · DL-213` from `DL-214`'s record and the 08-17 rulings; `DL-200 · DL-205` from
`dl_records.py`'s own commentary). A narrower ratification was attempted first and **does not work**:
the 45 cannot be trimmed as rows, because they exist only to satisfy the file's self-citation.

**The mechanism is an EXTENSION, not a new one.** `cited_ids_canonical()` already refuses to let
`REGISTER_REL` cite its own rows, immediately above. `DECISION_INDEX_RELS` now receives the same
treatment, in the same form, for the same reason.

`MEASURED-BY:` `python3 tools/dl_records.py citations` in a clean worktree, corpus staged, on
`origin/main` + this branch + `canon/dl-214-graduation` + `canon/graduate-owner-rulings-2026-08-17`,
the three merges performed (not simulated), 0 conflicts —

```
before the amendment   rc=0   51 [citation-indexed]   45 self-cited
after  the amendment   rc=0   13 [citation-indexed]    0 self-cited
control: origin/main   rc=0    0
```

**RED-proved in both directions**, as I1…I6 already were:
- **I7 GREEN** — a tree whose only mention of an id is the index row cataloguing it passes, and emits
  **no** resolution notice, because nothing cited it.
- **I8 RED** — the same id cited by a real canonical file and absent from the index still ERRORs. I7 and
  I8 differ only in *who does the citing*, so a green I7 cannot be a fixture that always passes.

### 6a · Three dependencies in §4 were measured FALSE — recorded, not tidied away

1. **`canon/dl-214-graduation` `faa0438` is not "clean".** It is **RED with four** `citation-unresolved`
   (`DL-209 · DL-210 · DL-211 · DL-213`), and it is **10 commits behind `origin/main`** — the "clean"
   reading was taken on a stale base. ⇒ **a gate result is bound to a BASE as well as a SHA.**
2. **`canon/dl-210-graduation` is unnecessary**, not merely blocked. Under this ruling DL-210 resolves
   through the index. The chain is **three** merges — index → dl-214 → 08-17 — not four.
3. **This branch was itself RED** on the fabricated three-digit id its own §3a *narrates* while
   describing a RED-proof. `CITE_RE` cannot distinguish narration from citation. Fixed by adopting the
   corpus's existing `DL-NNN` placeholder convention rather than adding an escape to the gate: **an
   exemption for a "declared non-citation" is a way to make any citation invisible.**
   ⚠️ **This section reproduced the defect while documenting it** — the first draft of this very
   paragraph named the fabricated id literally and turned the branch RED a second time. **A document
   that discusses a citation defect is a canonical surface like any other. Write the placeholder, never
   the example.**

⚠️ **This ruling does not promote anything.** An id resolved by an index entry still has no record file,
and every resolution says so on every run. Graduation to a record remains owed.
