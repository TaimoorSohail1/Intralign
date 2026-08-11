# R2 Refinement Ledger — post-freeze changes (R2.x)

**Framework 002 · §5.** Every change to the R2 line since the 2026-08-06 freeze (`R2_FREEZE_MANIFEST.md`), classified by dev-contract impact. From here forward each row is generated from its **labeled PR** (`neutral` / `additive` / `altering`); `altering` merges only with the dev lead's approval (convention). This is dev's authoritative "what changed since freeze / what to absorb" view.

**Classes:** **Neutral** (no guard/slice/interface change) · **Additive** (extends without invalidating signed work — absorb new scope) · **Altering** (changes an existing slice/GT/interface — needs impact assessment + dev-lead sign-off).

| Date | Change | Class | PR / commit | Traces to | Guard delta | Reference md5 after | Dev absorb |
|---|---|---|---|---|---|---|---|
| 2026-08-09 | Execution-monitoring tier split; Pro program scope + $79; plan-export tiering | Neutral | DL-206/207/208 commits | DL-206 · DL-207 · DL-208 | — | — | No build change (pricing/tier canon; applies at graduation) |
| 2026-08-09 | Slice 10 — load-bearing sensitivity + issue-classification engine | **Additive** | `744fb3f`, `4e1bb7f` (signoff) | DL-209 | +GT-34…GT-44 | 72068597 | New slice to build; existing work stands |
| 2026-08-09 | Prototype L3: derived resolution + escalate-on-new | Additive | `744fb3f` | DL-209 | (in the GT-34…44 set) | 72068597 | Reference-oracle update |
| 2026-08-09 | CAF dimension boundaries + deterministic structural-target assignment | **Additive** | `744fb3f` | DL-210 | +GT-45…GT-50 | 72068597 | New scope; amends main CAF at graduation (see reconciliation catalog) |
| 2026-08-09 | Prototype dim derived from structural target (retire authored dim) | Additive | `9054706` | DL-210 | +GT-46 (oracle) | 0ef33b3c | Reference-oracle update |
| 2026-08-09 | Proposal-resolution model + cross-surface sync + itemized findings (tray + card) | **Additive** | `840e853`→`b07893f` | DL-211 | +GT-51…GT-55 | 1b564dd8 | New scope; existing work stands |
| 2026-08-09 | Start-here guides cleared-worklist/pending state | Neutral→Additive | `b07893f` | (prototype fix) | +GT-56 | 3a2fe943 | Reference-oracle update |
| 2026-08-09 | Export rebuild · masthead two-column · read-reflow · terminal completion card | Neutral | (earlier commits) | (prototype UX passes) | various (readReflow/terminalDone/exportMultiFormat) | — | Reference-oracle update |
| 2026-08-09 | DEV_NEXT_STEPS · README source-of-truth · CAF reconciliation catalog · Slice 10 sign-off | Neutral | `1a5e136`, `45956fb`, `4e1bb7f` | (handoff docs) | — | — | Handoff/build-governance docs |

| 2026-08-09 | Fix build-readiness gap: tag the export simulation `SIM:#24` + re-tag Asana push #10→#24 + bump `SIM_MAX_CAP` 23→24 (found by build-readiness-audit) | **Neutral** | (PR: `neutral`) | build-readiness-audit finding | — (`demoSimsTagged` still green) | fae63e40 | Traceability fix — export/PM-push sim now links to capability #24; no build-contract change |

| 2026-08-09 | Reverse-coverage guard `capabilityHasSim` — every declared capability 1..SIM_MAX_CAP has a sim (or `_SIM_ELSEWHERE`); closes the #24 blind spot in the harness | **Additive** | (PR: `additive`) | build-readiness-audit follow-on | +GT-57 | 3ba88049 | New guard in the acceptance register (GT-57); dev absorbs the test |

| 2026-08-09 | Intralign service mark (white horizontal logo) placed in the app masthead **+ onboarding funnel screens + onboarding arc** — replaces the text marks; embedded as one shared self-contained webp data URI (no external dependency) | **Neutral** | (PR: `neutral`) | branding (owner) | — | main `28fef04a` · arc `b375fd75` | Static brand asset — no build-contract, guard, or simulation change |

**Note.** Rows above predate the labeled-PR convention (they landed as direct commits during the same session as the freeze-to-change-control transition) and are classified retroactively per DL-212 §9. **None is _Altering_** — no shipped GT (GT-01…GT-33) changed or was removed, and no signed slice's behavior was reversed — which is why the dev build's in-flight work is unaffected. All post-freeze GT additions are GT-34+ (net-new). From the next change forward, each row is a labeled PR.

---

_Framework 002 realization (DL-212). Current reference prototype: md5 `28fef04a` (+ arc `b375fd75`), `_S10` 85 / arc 2, register GT-01…GT-57._
