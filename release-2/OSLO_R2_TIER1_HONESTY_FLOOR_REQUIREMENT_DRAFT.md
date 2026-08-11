# DRAFT — R2 / Tier-1 Requirement: Honesty Floor for Primary-Dragging Trade-offs

> **Status: DRAFT for owner ratification.** AI-authored proposal; only the repository owner may ratify (CLAUDE.md authority constraint). Route through Framework 001 (Backlog → Proposal → Review → Decision → Change → Changelog). This is Tier-1 (Free / R2) scope — it belongs on the R2 single-outcome line, NOT in the deferred Tier-2 multi-outcome work.

## Origin
Owner discussion, 2026-08-08. While reconciling why the Intent nav badge counted a *held* secondary outcome as "needs work" (fixed separately), a sharper question surfaced: the freemium doctrine (**DR-7: freemium gates capacity, never judgment quality**) means OSLO cannot paywall a genuine weakness in the **primary** outcome's read. A trade-off dragging the primary is a judgment-quality signal — so *surfacing* it must be free (Tier-1), even when the tension's root is a secondary outcome OSLO read but the user has not adopted. Hiding it behind the multi-outcome (Basic) gate would be gating judgment quality and a dark pattern.

## Requirement (statement)
**R2's single-outcome read must not reach `Sound` while a genuine, detectable trade-off is dragging the primary outcome — including a trade-off whose root is read-but-unadopted secondary work — and OSLO must surface that trade-off in *primary-outcome terms*.**

## Scope boundary (what is Tier-1 vs Tier-2)
- **Tier-1 (Free / R2) — REQUIRED here:** *detecting and surfacing* any real weakness in the **primary** outcome's read, expressed in single-outcome vocabulary (e.g. "the sponsor-pipeline work in your plan is competing with your sold-out, well-rated goal"). No second outcome is named or modeled; it reads as a plan-internal trade-off against the one outcome being steered. Gating: the read cannot be `Sound` while such a trade-off is un-surfaced or unresolved.
- **Tier-2 (Basic) — NOT here:** the multi-outcome *machinery* — treating the secondary as a first-class co-equal outcome, the named **cross-outcome conflict** issue type (T2-MO-7) between two *adopted* outcomes, and *resolving* the conflict by steering/optimizing both. That capacity is legitimately gated.

## Rationale (why the split lands where it does)
A *cross*-outcome conflict presupposes two **adopted** outcomes. Until the user adopts the second, there is no cross-outcome conflict — only a plan-internal trade-off against the single outcome they are steering, and catching that is already the single-outcome read's job. So doctrine forces the *honesty* into Tier-1 (expressible without the multi-outcome engine), but does **not** force the multi-outcome engine itself into Tier-1.

The free user is not dead-ended: the honest, no-cost resolution is to **drop / de-scope the secondary** (stay single-outcome). What Basic buys is the capacity to *keep both* and steer the trade-off — value (the real problem) is visible free; the capability to act on it without sacrificing an outcome is paid. Clean, honest PLG.

## Acceptance criteria (candidate)
1. When the plan contains work/assumptions that genuinely compete with the primary outcome, OSLO surfaces a **load-bearing issue** for it, framed in primary terms, on the Free tier.
2. Integrity cannot read `Sound` while that issue is open (it gates like any other load-bearing weakness).
3. The issue is **resolvable with no dead-end** (consistent with the verified invariant): the user can resolve by an explicit call — accept the trade-off on the record, or adjust the plan — and doing so lets integrity reach `Sound`.
4. The framing never names or models a second outcome; no multi-outcome capability is implied or required to *surface* it.
5. Guard candidate (for `_S10`): `noSoundWhileUnsurfacedPrimaryTradeoff` — the read cannot be `Sound` if a primary-dragging trade-off exists un-surfaced/unresolved.

## Open question (anti-assumption — do NOT resolve unilaterally)
Whether R2 **as built** already honors this is unverified. It is possible the sample's two outcomes are complementary (a great event feeds the sponsor pipeline) and there is no real trade-off to surface; it is equally possible the read can reach `Sound` over a genuine trade-off, which would be a live doctrine gap. This requires an owner/spec determination before the build's terminal `Sound` state is changed.

## Realization in the R2 prototype (built 2026-08-08, owner-directed)
Built into `oslo-prototype-r2.html` (all four copies synced; harness **65/65** via headless jsdom):
- **Scope edge item `s3`** (`prov:'inferred'`, `side:'edge'`) — the trade-off, framed in primary terms: *"Sponsor activation footprint on-site … vs. protecting a sold-out, well-rated, right-audience day. Where the line sits isn't drawn."* No second outcome named. Being inferred keeps Scope weak ⇒ pulls `viaLevel` down ⇒ integrity cannot be Sound until resolved. Scope has no `VSTATE` fix shortcut, so the ONLY clearance is grounding the item (the owner draws the line) — resolvable, no dead-end.
- **Surfaced issue `sponsor-tradeoff`** (`dim:'via'`, `t:{artifact:'scope'}`) in the `ISSUES` layer — appears in the Issues panel, resolves when Scope is grounded; static entry suppresses a duplicate false-confidence issue.
- **Guard `noSoundWhileUnsurfacedPrimaryTradeoff`** — drives the model to prove: unresolved ⇒ issue open + Scope weak + `viaLevel < 4`; grounded ⇒ issue closed + Scope clear. Empirical probe on clean load confirmed: scope-weak=true, issue-open=true, integrity min < Sound; after grounding, both clear.

**Anti-assumption call made (owner may veto):** this asserts the sample's sponsor-emphasis genuinely trades off against the primary (sponsor floor space / agenda slots / attendee attention competing with a well-rated, right-audience day) — a realistic, defensible tension, not fabricated. If the owner deems the two complementary, revert the three additions (item `s3`, issue `sponsor-tradeoff`, guard) — they are self-contained.

## Related
- `release-2/oslo-integrity-architecture.md` — integrity model + verified invariant.
- Tier-2 deferral + PLG framing: multi-outcome recall anchor (T2-MO epic; cross-outcome conflict issue = T2-MO-7).
- Freemium doctrine: DR-7 (gates capacity, not judgment quality).
