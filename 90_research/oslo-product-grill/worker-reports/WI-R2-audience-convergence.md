# Worker Report — WI-R2: Audience-model convergence

**Date:** 2026-07-13 · **Worker:** OSLO product-grill WORKER subagent
**Builds on:** WI-R1 (Strategic Readout composer fold-in).
**Goal:** Unify the composer's audience model onto the workspace Readout's `REPORT_RECIPIENTS`
(Sponsor / Programme lead / Operations / Executive-board) so the composer (`#sroDoc`) and the memo (`#rptDoc`)
share ONE audience taxonomy — while keeping the two SURFACES distinct. Share the MODEL, not the rendering register.

---

## What changed (all in `slice-10-tiering-limits/prototype.html`, applied surgically in place)

1. **`SRO.aud` default** `'practitioner'` → `'sponsor'` (first `REPORT_RECIPIENTS` entry).
2. **Audience selector** — was three static buttons (Practitioner / Sponsor / Executive). Now a container
   `#sroAud` whose buttons `sroRender()` builds from `REPORT_RECIPIENTS`, keyed by `.k`
   (`sponsor` / `programme` / `ops` / `exec`). **"Practitioner" dropped** — it is the PM's own view, not a memo
   recipient; §4 is addressed to actual recipients.
3. **`sroAsk()` rewritten** to key on the selected `REPORT_RECIPIENTS` entry: it reuses the recipient→issue
   MAPPING (`MEMO_ASKS[rcp.k]`, the taxonomy only) and the recipient's ASK INTENT (`REPORT_RECIPIENTS[].ask`),
   grounds them in the LIVE open `ISSUES` (recommendation + dimension), and renders them in the composer's
   OSLO-facing register. **It does NOT call `_memoDecisions()`** — that is the memo's doctrine-free prose, a
   different register. Share the model, not the rendering.
4. **`sroRender()`** now builds the four buttons from `REPORT_RECIPIENTS` and syncs the active one.
5. **`_assertReadIdenticalAcrossAudience()`** now iterates ALL FOUR `REPORT_RECIPIENTS`: asserts §1/§2/§3/§5
   byte-identical across every recipient AND §4 distinct across every pair (message updated to the four recipients).
6. **`_assertReadoutRunsNoAnalysis()`** iterates the four `REPORT_RECIPIENTS` when proving no History/Trend mutation.

DL-107/108/104 preserved: §1–§3 and §5 read no audience state (structurally audience-independent); only §4 reads
`SRO.aud`. The binding banner + citation stay. No conditional-stop condition was hit — convergence shares only the
taxonomy + intent and did not touch `#rptDoc` or its guards.

### Docs updated (in place, on device)
- `product-detail.md` — §4 spine row now names the shared `REPORT_RECIPIENTS` taxonomy.
- `frontend-ui.md` — audience selector described as four buttons built from `REPORT_RECIPIENTS`.
- `user-experience.md` — the audience-toggle step lists the four recipients.
- `success-criteria.md` — C-WIR1-2 updated to four recipients / six pairs.
- `e2e-test-scenarios.md` — S-WIR1-1 switches across all four recipients.
- `open-items.md` — **O-WIR1-2 closed: RESOLVED by WI-R2** (audience taxonomy unified).

---

## Verification (headless Chromium / Playwright, on the ACTUAL patched device file)

| Check | Result |
|-------|--------|
| Boot self-check total | **87** (WI-R1 left it at 60; a concurrent prototype expansion added ~27 more — see note) |
| Failing checks | **0** |
| `reportsNoHealth` | ✅ |
| `readIdenticalAcrossAudience` (now 4 recipients) | ✅ |
| `readoutRunsNoAnalysis` | ✅ |
| Page errors | **0** |

**4-recipient DL-108 invariance proof** (opened the modal, captured `#sroDoc .sro-sec` innerHTML per §):
- Buttons rendered: **Sponsor · Programme lead · Operations · Executive / board**; **no Practitioner**.
- §1, §2, §3, §5 **byte-identical across ALL pairs** of the four recipients (`readAllIdentical = true`).
- §4 **distinct across ALL six pairs** (`askAllDistinct = true`): sponsor / programme / ops / exec each address a
  different recipient with a different ask intent.

Two surfaces stayed distinct: the composer still renders into `#sroDoc` in the export modal (`#exportScrim`),
still outside `REPORT_SURFACES`, still in OSLO's epistemic register; `#rptDoc` (the doctrine-free memo) was not
touched. Practitioner was dropped cleanly (0 occurrences anywhere in the composer or the WI-R1 doc sections).

---

## ⚠ Concurrency note (important, honest)

Between the WI-R1 commit and WI-R2, **another process substantially edited the same files on the device**:
`prototype.html` grew ~1.60 MB → ~1.90 MB (+~300 KB; boot checks 60 → 87), and the `.md` docs grew as well
(e.g. `frontend-ui.md` 74 KB → 116 KB). The `/mnt` upload mount was serving **stale cached copies**, so a naive
re-commit of my WI-R1-based file would have **clobbered ~300 KB of that concurrent work**.

To avoid that, WI-R2 was applied as a **surgical in-place patch on the real device file** (via `device_bash` +
a self-validating Python patch that asserts each OLD block occurs exactly once and writes atomically, else aborts).
The prototype was backed up first, patched (7/7 blocks), copied to a fresh filename, re-staged (fresh, uncached),
and verified with the full Playwright battery before finishing. My WI-R1 composer + guards were confirmed intact in
the device file prior to patching. The concurrent 300 KB is preserved; the final file is 1,905,030 bytes and boots
87/87 green.

---

## Residue / open items
- **O-WIR1-1** (report NAME is owner/glossary, "naming pending") — still open; not a WI-R2 concern.
- **O-WIR1-3** (§4 asks grounded in live issues but curated, not from a decision model) — still open. WI-R2 keeps
  this: the recipient→issue mapping comes from `MEMO_ASKS` (taxonomy) and OSLO's recommendation text; a formal
  "who owns which decision" model remains an M4 spec item.
- **Note on §4 overlap:** `sponsor` and `exec` map to overlapping issues (ISS-01/02) in `MEMO_ASKS`; their §4
  outputs still differ because the addressing line carries each recipient's distinct label + `.ask` intent. The
  distinctness guard (`askAllDistinct`) passes, but the differentiation for those two is intent-framing, not a
  different issue set — faithful to "tailor the ask," and flagged here for transparency.
- The boot-check total moving 60 → 87 is the concurrent worker's expansion, not WI-R2 (WI-R2 added no new guards;
  it extended two existing ones to four recipients).
