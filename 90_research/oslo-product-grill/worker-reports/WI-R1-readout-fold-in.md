# Worker Report — WI-R1: Strategic Readout composer fold-in

**Date:** 2026-07-12 · **Worker:** OSLO product-grill WORKER subagent
**Task:** Fold the Strategic Readout composer (DL-107 spine + DL-108 tailor-the-ask + DL-104 P1 guards) into the
Slice 10 Reports surface. Governed, non-canonical prototype update.

---

## What changed

Target: `vertical-slices/slice-10-tiering-limits/prototype.html` (~19,600 lines after edits).

The slice-10 prototype already had a **far richer** Reports surface than the v5 reference draft: a full editable
**Readout document** (`#rptDoc`) with seven fixed sections (D150), a memo that travels, send/schedule, and ~30 boot
guards — and it **already encodes DL-108** as "D145 — tailor the ask, never the read" (`_memoRead()` is blind to the
recipient; `_memoDecisions()` is the only audience-addressed section).

So this was an **enhancement of the existing surface**, mapped exactly as the reference itself mapped it: the
reference upgraded **only the export surface** (`#exportModal` / `openExport()`). Slice-10's equivalent is the
**export/snapshot modal** (`#exportScrim` / `openExport()` / `renderExport()`). I folded the DL-107 five-section
**composer** into that modal, wired to slice-10's own data — and left the seven-section editable Readout document
and every one of its guards **untouched** (cumulative-prototype / non-regression rule).

**Why the export modal and not `#rptDoc`.** The composer must, per DL-104 P1, speak OSLO's epistemic vocabulary
openly ("understanding maturity", "not health/RAG/readiness/probability", "From OSLO" / "Confirmed by you"). That
vocabulary is **banned inside the reader-facing memo** by D149 and its health-framing scanner (`REPORT_SURFACES`).
The two are genuinely different surfaces: `#rptDoc` = what a sponsor reads (doctrine-free); the export composer =
OSLO-facing packaging metadata. The composer renders into `#sroDoc` and is **intentionally kept out of
`REPORT_SURFACES`**, so the §7j / D149 document scanners do not (and must not) grade it. This is the correct
semantic separation, not a workaround.

### Edits (six, all in prototype.html)
1. **CSS** — a namespaced `.sro-*` block (the workspace already owns `.ro-*`; `.ro-cur`/`.ro-foot` would collide,
   so all new classes are `.sro-*`).
2. **HTML** — the composer inside `#exportScrim .wm-b`: draft ribbon, DL-108 binding banner, audience selector
   (Practitioner/Sponsor/Executive), `#sroDoc`, four optional-section checkboxes (Basic), Free/Basic tier caption.
3. **`renderExport()`** — now calls `sroRender()` so the spine paints when the modal opens.
4. **JS composer** — `const SRO`, builders `sroRead/sroLimit/sroUnknowns/sroAsk/sroHow/sroOpt`, `sroRender`,
   `sroSetAudience`, `sroToggleOpt`. Wired to slice-10's **own** model: `ISSUES`, `_istatus`, `_readCurrency`,
   `_chatState().limiting`, `_openClarIds`, `_epiOf`, `_ARTORDER`, `dispName`, `TREND`, `_sevrank`. v4 was NOT
   imported. **Only `sroAsk()` reads `SRO.aud`.**
5. **Two boot guards** — `_assertReadIdenticalAcrossAudience()` and `_assertReadoutRunsNoAnalysis()`.
6. **Registration** — both guards added to the `_s10SelfCheck()` return object, right after `reportsNoHealth`.

### Docs updated (append-only)
`product-detail.md`, `frontend-ui.md`, `user-experience.md`, `success-criteria.md`,
`e2e-test-scenarios.md` (3 scenarios: S-WIR1-1/2/3), `open-items.md` (WI-R1 completion + O-WIR1-1..4).

---

## Verification (headless Chromium via Playwright, `file://`)

| Check | Before | After |
|-------|--------|-------|
| Boot self-check (`window._S10`) total | 58 | **60** |
| Failing checks | 0 | **0** |
| `reportsNoHealth` | ✅ | ✅ (unchanged) |
| `readIdenticalAcrossAudience` | (absent) | **✅** |
| `readoutRunsNoAnalysis` | (absent) | **✅** |
| Page errors (`pageerror`) | 0 | **0** |

**DL-108 invariance proof** (opened the modal, captured `#sroDoc .sro-sec` innerHTML per §):
- §1, §2, §3, §5 innerHTML **byte-identical** across Practitioner ≡ Executive ≡ Sponsor. `readIdentP_E = true`,
  `readIdentP_S = true`.
- §4 **differs** across every pair: `ask_P_E_differ = true`, `ask_P_S_differ = true`, `ask_E_S_differ = true`.
  (P: "Confirm the venue's 500-person Wi-Fi throughput…"; E: "One go/no-go input… in-person network readiness…";
  S: "Two decisions gate what was sold…".)
- §1 renders: "Understanding of this plan is Moderate, held with moderate reliability. This is understanding
  maturity — not project health, readiness, a RAG status, or the probability of success…"

**Console errors:** the only console message was `net::ERR_TUNNEL_CONNECTION_FAILED` — the external Google Fonts
stylesheet failing to load in the offline sandbox. It is **environmental (no outbound to fonts.googleapis.com)**,
not an application/JS error (0 `pageerror` events). It would not appear in a networked browser.

`node --check` on an extracted script was not run in isolation (the JS is inline across many `<script>` blocks and
depends on the surrounding globals); the headless load with **0 page errors** is the stronger equivalent.

---

## Guardrails honored (out-of-scope items confirmed NOT built)
- **No** cognitive-event / Understanding-Debt feed (R2-F/AE-06).
- **No** assumption validated/invalidated lifecycle, re-validation prompts, or "which assumptions failed" (RB-017).
  The "Unvalidated assumptions" optional section is **presentation-only** and says so, citing RB-017.
- **No** cross-project / portfolio pattern call-outs (R2-E).
- **No** Uncertainty / Trade-off first-class objects.
- **No** audience-reframed *reads* — the read is structurally audience-independent (proven by guard).
- Report **names** kept owner/glossary: descriptive label + "naming pending"; no "status report" / health name.
- Free = read snapshot (§1–§5, PDF); Basic = optional sections + branding + scheduling; **seed never gated**.
- Theme untouched (slice-10 tokens only); no backend/server/API/db/auth; only the slice-10 prototype + its docs
  were touched; the reference draft and v4 were not modified.

---

## Residue / open items (honest)
- **Owner re-signoff** of the Reports portion of Slice 10 is required (WI-R1 reopened a signed-off surface).
- **Two audience models now coexist:** the composer uses Practitioner/Sponsor/Executive (the WI-R1 axis); the
  workspace Readout uses Sponsor/Programme/Operations/Executive (`REPORT_RECIPIENTS`). Convergence is left open
  (O-WIR1-2) — deliberately not forced, to avoid disturbing the signed-off document.
- **§4 asks are curated demo strings** grounded in the live open issues, not generated from a decision model
  (O-WIR1-3). Matches the reference's approach; the real ownership mapping is an M4 spec item.
- The composer's `readoutRunsNoAnalysis` guard proves no `HISTORY`/`TREND` mutation; it does not attempt to prove
  the (separate, already-guarded) send/schedule paths — those keep their own D146/D172 guards.
