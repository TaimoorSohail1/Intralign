# Governance Proposal (DRAFT) — Prototype Simulation ⇒ Backend Obligation

> **Status: DRAFT for owner ratification.** AI-authored proposal under Framework 001. Only the repository owner may ratify, and the owner lands it (dl-land / Founder Console). AI drafts and recommends; it does not decide. This packet is self-contained: Backlog framing → Proposed canon → Review (Framework 001A five outputs) → Decision body for dl-land → landing steps.

---

## 1. Backlog entry (framing)
The R2 prototype (`oslo-prototype-r2.html`) deliberately *simulates* backend behavior (in-memory state, setTimeouts, authored demo content). Without a binding rule, a capability that is demoed but never built would ship a product that is dishonest about what it does — a direct violation of OSLO's honesty-first doctrine. Today the obligation is tracked only in a working audit doc (`release-2/canon/audits/OSLO_BACKEND_CAPABILITIES.md`) and assistant memory; it does not *bind* engineering. This proposal elevates it to owner-ratified build governance.

## 2. Proposed canon
**Intended path:** `00_owner/build_governance/PROTOTYPE_SIMULATION_BACKEND_OBLIGATION_V1.md`
**Proposed body:**

> # Prototype Simulation ⇒ Backend Obligation (V1)
> _Owner-ratified build governance. Binds engineering (engineering proposes realization; owner ratifies policy intent)._
>
> ## Policy
> Any capability the OSLO prototype **simulates or demonstrates** MUST be designed and built by the backend to actually support it before it is exposed to users. A demonstrated behavior is a **product commitment**, not a shortcut.
>
> ## Rules
> 1. A prototype stub proves **UX intent only**. It is never the spec for behavior and never a substitute for a real implementation.
> 2. **No prototype-demonstrated capability ships to users** without a backing real build: design + implementation + tests + the doctrine boundaries the capability entails.
> 3. Every capability the prototype simulates or demonstrates MUST be registered in the backend-capabilities registry (`release-2/canon/audits/OSLO_BACKEND_CAPABILITIES.md`) at the moment it appears in the prototype, with a "Prototype stub" and a "Backend must provide" entry. That registry IS the backend backlog.
> 4. The registry is a **living, load-bearing** artifact — engineering plans the real build from it; the owner ratifies each capability's realization. Divergence between a shipped surface and its registered backend capability is a defect.
>
> ## Scope & authority
> Applies to all OSLO prototypes and demo surfaces. Consistent with DR-7 (freemium gates capacity, never judgment quality) and the honesty-first doctrine. Engineering authors realization and proposes; the owner ratifies policy intent (ratify ≠ author).

## 3. Review (Framework 001A — five outputs)
- **Findings:** The prototype already simulates 19 registered backend capabilities; the obligation to build them is currently non-binding (working doc + memory only). The rule is a natural extension of honesty-first doctrine and the existing "capture for the R2 build" intent of the registry.
- **Concerns:** (a) Risk of the registry becoming stale if not maintained per-change — mitigated by Rule 3 (register at the moment of appearance). (b) "Demonstrates" is broad; a purely illustrative mock with no user-facing promise could be over-scoped — mitigated by tying the obligation to capabilities *exposed to users* (Rule 2). (c) The registry currently lives under `release-2/`; long-term it may belong in a release-agnostic build-governance location — flagged, not resolved here.
- **Dependencies:** The backend-capabilities registry (`OSLO_BACKEND_CAPABILITIES.md`); the R2 build/engineering handoff; DR-7 and honesty-first doctrine.
- **Recommendation:** **Adopt** as `00_owner/build_governance/PROTOTYPE_SIMULATION_BACKEND_OBLIGATION_V1.md`, ratified by a Class-A decision. No prototype/UX change required; this binds the build.
- **Status:** Ready for owner ratification. Blocking questions: none. Open (non-blocking): the release-agnostic home for the registry.

## 4. Decision record body (for dl-land)
```
title: Prototype simulation ⇒ backend obligation — build-governance policy V1
slug: prototype-simulation-backend-obligation
class: A
decided_by: Idris (Founder Console)

## Decision
Ratify `00_owner/build_governance/PROTOTYPE_SIMULATION_BACKEND_OBLIGATION_V1.md` as owner build governance: any capability the OSLO prototype simulates or demonstrates must be designed and built by the backend to actually support it before user exposure; a stub proves UX intent only and is never the behavioral spec; every simulated/demonstrated capability must be registered in the backend-capabilities registry, which is the binding backend backlog. Binds engineering (engineering proposes realization; owner ratifies intent). Consistent with DR-7 and honesty-first doctrine.

## Status
Ratified.
```

## 5. Landing steps (owner runs — AI does not land canon)
1. Commit the policy doc to `00_owner/build_governance/PROTOTYPE_SIMULATION_BACKEND_OBLIGATION_V1.md` on the canon line (main), per the Git/Branch workflow (branch → PR → green doc-integrity → owner merge).
2. Land the decision via dl-land (numbers at merge, one canon PR in flight):
   `gh workflow run dl-land.yml -R idris-manley/oslo-knowledge-base -f title="Prototype simulation ⇒ backend obligation — build-governance policy V1" -f slug="prototype-simulation-backend-obligation" -f class="A" -f decided_by="Idris (Founder Console)" -f body="$(cat body.md)"`
   (Pass the §4 body via `$(cat file)` — the Actions web form strips newlines and fails `dl_records.py`.)
3. Owner approves the bot PR (approve-workflows → code-owner review → squash) to merge.

_Note on placement: this proposal is staged under `release-2/` because that is the active working line; the ratified policy + DL target the canon line (`00_owner/build_governance/` + `main`). Landing to main vs. R2-isolated staging is an owner call, consistent with the open decision-log staging thread (canon main tops at DL-156; R2 DLs staged in `release-2/`)._
