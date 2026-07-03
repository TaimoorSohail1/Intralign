# Release 1 Specification Roadmap

**Type:** Recommended sequence for producing the remaining engineering specifications (dependency-driven)
**Date:** 2026-05-31
**Source:** `RELEASE_1_ENGINEERING_READINESS_AUDIT.md` · `RELEASE_1_SPECIFICATION_BACKLOG.md`

> Recommends the order in which to produce the missing specifications, by dependency. **No artifact is created here.**

---

## Recommended sequence

```text
1. Data Model Specification  (incl. Tenancy & Permission entities)
        ↓
2. State Model Specification
        ↓
3. API / Service Contract Specification
        ↓                         ↘ (parallel)
4. UI Specification               5. Performance / NFR Specification
        ↓                         ↙
6. Testing Strategy   +   7. Operational / Observability Specification
```

**Verdict on the proposed order (Data Model → State Models → API Contracts → UI Specification → Testing):** **endorsed, with two refinements** — fold **Tenancy/Permission** into the Data Model (step 1), and allow **UI Specification** and **Performance/NFR** to proceed **in parallel** rather than strictly after API.

---

## Rationale (dependency analysis)

1. **Data Model first.** Everything persistent depends on it — the Knowledge Layer (canonical storage, versioning, relationship graph), the objects the analysis passes read/write, and tenancy/permission entities. It is the highest-risk gap and has **no upstream dependency** (its conceptual source, Master Spec §18, already exists). Building anything else first risks rework against an undefined schema. **Include tenancy/permission entities here** — workspace/user/role/permission are data entities, and the permission model is currently unenumerated.

2. **State Models second.** States attach to entities, so they need the Data Model. They define the **Fast→Deep analysis flow** and **event-driven recompute** that the two horizons depend on, and the lifecycles (Finding, Recommendation, Notification, Project, Analysis Run, Artifact). Without them, the analysis flow and recompute are ambiguous.

3. **API / Service Contracts third.** Contracts express commands/queries over the entities and states, so they depend on both. They are currently **Missing** and gate inter-service and front/back-end work — but they cannot be defined coherently before the data and state foundations exist.

4. **UI Specification — parallelizable (start early).** The UI can begin from Master Spec §15 + existing wireframes **as soon as the Data Model exists** (so screens reflect real entities), and be refined once API contracts land. It need not wait for testing. Running it parallel to steps 2–3 shortens the path.

5. **Performance / NFR — parallel with API.** SLO/latency targets (60-second size envelope, Deep Analysis latency, availability) inform contract and infrastructure design, so define them alongside the API contracts.

6. **Testing Strategy — after API + State + NFR.** Test scenarios map to acceptance criteria (§16) and validate states, contracts, and NFR targets, so it follows them.

7. **Operational / Observability — alongside Testing.** Logging/monitoring/failure-handling depend on the architecture + contracts and are needed for launch readiness; sequence them with testing.

**Calibration track (parallel, owner-owned):** the CAF scoring method / CAF→Confidence formula (Matrix §22 g1) should be resolved on a separate owner track during steps 1–3, since the analysis engine needs it to produce values — but it is calibration, not an engineering spec.

---

## Why not a different order

- **API-first** would define contracts over undefined entities/states → churn.
- **UI-first (fully)** would design screens over an undefined data model → rework; partial parallelization (from §15/wireframes) captures the benefit without the risk.
- **Testing-first** has nothing concrete to test against.

The Data → State → API spine is the critical chain; UI and NFR parallelize; Testing and Operational close out. This is the shortest dependency-respecting path from *defined* to *buildable*.

---

*Sequencing recommendation only. The artifacts themselves are not created here.*
