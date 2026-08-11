# OSLO R2 — Start Here (developers)

**What this is:** the signed-off build design for OSLO R2 — ten vertical slices, a reference prototype, an acceptance suite, and the decision canon behind it.

**Resuming implementation:** read [`R2_VERTICAL_SLICE_STATUS_LEDGER.md`](./R2_VERTICAL_SLICE_STATUS_LEDGER.md) first. It is the operational source of truth for what is implemented, reviewed, tested, manually regressed, and verified against the prototype. Update it in the same change that produces new delivery evidence.

**Where it lives:** repo `oslo-knowledge-base`, branch **`release-2`**, folder **`release-2/`**. `main` is frozen R1 — don't build from it.

**Get it:**
```bash
git fetch origin
git checkout release-2
cd release-2
```

**Read in this order:**
1. `README.md` — what OSLO is + the honesty spine: *only reanalysis resolves · maturity, not a forecast · capacity is gated, judgment quality never*.
2. `WORK_BREAKDOWN.md` — the full scope in build order. A **sequence, not a schedule** — iterate however your team works.
3. `BUILD_SEQUENCE.md` — the reasoning and dependencies behind that order.
4. `slices/` — the spec you build against (one per stage of work). `oslo-prototype-r2.html` is the reference implementation — open it in a browser; it settles any ambiguity the prose leaves.
5. `acceptance/` → Slice 9 — the FE↔BE integration map (**a surface not in it isn't shippable**), including each surface's **Async** state, and the doctrine-guardrail suite that gates the build.
6. `LATENCY_AND_ASYNC_UX.md` — how backend delay (Fast Pass, Deep Pass, LLM, connectors) shapes every surface's loading behavior; the integration map's Async column keys to it. **The build assumes zero latency today — this closes that gap.**
7. `canon/` — the "why" behind every locked decision.
8. `BACKLOG.md` — full ticket detail + the owner-open decisions register (O-1…O-10).

**Where to start:** Stage 0 in `WORK_BREAKDOWN.md` — the six corrections that make the prototype a faithful oracle. Needs one owner input at kickoff (the three interior band labels).

**Rule of thumb:** if a build choice seems to violate the spine, check `canon/` before proceeding — it's usually the exact wrong-default a ratified decision exists to prevent.
