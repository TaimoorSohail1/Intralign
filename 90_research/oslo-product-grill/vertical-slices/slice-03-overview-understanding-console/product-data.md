# Slice 3 — Project Overview & Understanding Console · Product Data

Client-side only (D016): all state is in-memory JS + `localStorage`. **No database, no server, no API, no real AI.** "Persistence" below means browser localStorage; tech choices for a real store are owner-TBD and out of scope.

---

## ConfidenceReading (Slice 3 focal object)
Illustrative shape used by the prototype (`READ.provisional` / `READ.current` / `READ.falseconf`):

| Field | Type / values | Notes |
|---|---|---|
| `index` | integer 0–100 | Maturity index. **Never shown bare** — always with band + reliability + cause (D002). |
| `band` | 5-band: **Very Low · Low · Moderate · High · Very High** | Shared scale for confidence and CAF (D020/DL-086/098). |
| `stage` | **Orientation · Expanded · Validated** | Understanding-maturity stage (D053). Fast Pass = Orientation; Extended Analysis = Expanded. |
| `ustate` (`ANALYSIS_STATE`) | `provisional · current · error` | Provisional↔current chip (D040); `error` = last-good after a failed deep pass (D041). |
| `feasLvl`, `feasW` | band word + bar % | The limiting CAF dimension (illustrative). |
| `rel` / `relWord` | qualifier text / reliability level word | Inline reliability qualifier on the Confidence card + pill. |
| `reliability` | Reliability object (below) | Independent of CAF. |

### CAF dimensions (each)
`{ name: Clarity|Alignment|Feasibility, level: <5-band word>, width: 0–100, limit: bool }`. Neutral maturity ramp; the lowest is flagged "the limit."

---

## Reliability (D051) — independent of CAF
| Field | Type / values | User label |
|---|---|---|
| `coverage` | **High · Moderate · Low** | Coverage |
| `evidence` | **High · Moderate · Low** | Evidence availability |
| `assessable` | **High · Moderate · Low** | **How assessable** (plain label for Assessability, D012) |

- Reliability uses a **3-level** scale (High/Moderate/Low), distinct from the 5-band maturity scale — it is a **qualifier**, not a maturity index.
- Rendered in the pill popover; also summarized in prose in the Overview "Why."

### falseConfidence flag (D052 / CONF-06)
Derived, not stored: `holds = (band ∈ {High, Very High}) AND (reliability level ∈ {Low, Very Low})`.
- When `holds`: render a **neutral** advisory flag naming the **cause** (`reliability shortfall` vs `CAF weakness`).
- When not: flag absent everywhere. Never carries health/severity color (D003).

---

## "How this is calculated" copy (D054)
Static explainer strings (not computed):
- **CAF-derived** — the lowest of Clarity/Alignment/Feasibility sets the ceiling.
- **Reliability-qualified** — a strong read on thin evidence is flagged, not hidden.
- **Cause-bound** — every move names a reason; movement is **direction-only** (D056).
- **Below-band jitter (±band) not dramatized** — only a band change is meaningful.

## Confidence movement (D056)
- Stored/shown as **direction + cause** only: `{ dir: up|down, cause: <string> }`. **No magnitude** is treated as canonical. Illustrative internal `index` values may change under the hood, but the **surfaced** movement is direction-only.

---

## PlanArtifact ×7 (INHERITED, D035) — unchanged
`Intent · Context · Scope · Requirements · Work breakdown (WBS) · Schedule · Resources`, each `{ id, grp, name, basis: derived|attested, rel: reliability word, body }`. User-facing term **"Plan artifacts"** (D048/D049). Internal keys (`WBS`, `artifact`) unchanged.

## IssueSummary set (INHERITED, D008/D017) — unchanged
Internal object = **Finding**; user-facing label = **Issues**. `{ title, sev: critical|moderate|warning, dim, sec, status: open|resolved, why, ev[], clar?, fixes[] }`. Lifecycle **Open → Addressed → Resolved** (D018); only reanalysis moves an issue.

---

## localStorage keys (namespace `oslo-s1-`) — preserved from Slice 1/2
`phase · orientSeen · tourSeen · account · staySignedIn`. **No new persisted keys in Slice 3** — the console state (popover open, false-confidence demo, how-calc open) is ephemeral UI state, not persisted. Reset via the phase-bar **Restart** clears `orientSeen · tourSeen · account · staySignedIn`.
