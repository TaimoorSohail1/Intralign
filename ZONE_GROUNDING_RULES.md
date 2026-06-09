# Zone Grounding Rules

> **Status:** Working draft (proposed) — not ratified canonical governance.
> **Purpose:** Deterministically classify any document, section, or paragraph into exactly one
> ownership **zone**, so that an LLM (or a person) never files product content under engineering,
> or vice versa. This is a **filing + authoring rulebook**, not a spec of the product.
> **Operates alongside:** `ANTI_ASSUMPTION_BUILD_PROTOCOL.md` (escalation), `CANONICAL_GLOSSARY.md`
> (naming), `CLAUDE.md` (authority — owner ratifies).
> **Scope guard:** This is the classification *method* only. It does NOT enact the zone restructure
> or supersede `DL-037` (the 01–05 split) — those are separate Framework 001 decisions. Rolling the
> front-matter (§3) across existing docs is a separate effort with its own doc-integrity-CI update.

---

## 1. The single axis everything resolves to

Every sentence is one of:

- **WHAT / WHY / RULE** → Product
- **HOW / MECHANISM** → Engineering
- **THE AGREED INTERFACE** between them → Handoff
- **A binding decision, unresolved owner choice, foundational doctrine / epistemic invariant, or binding build-governance policy** → Owner
- **Non-binding exploration** → Research

> If a sentence answers *"what must be true / why / for whom"* → **Product**.
> If it answers *"how is it built / with what structure"* → **Engineering**.
> If it is *the negotiated agreement that lets engineering start from product* → **Handoff**.
> If it is a **foundational invariant that must hold system-wide** (an epistemic/doctrinal rule —
> e.g. *Canonical = Attested*, *confidence ≠ probability*, *OSLO never self-accepts*) it is **Owner
> doctrine**, not product domain meaning. Product owns the *expression* of domain meaning; the Owner
> owns the *invariants*. Likewise, a rule that constrains *how* engineering must build is **Owner
> build-policy**, even though it concerns mechanism.

> **Ratify ≠ author (the boundary that keeps Owner authority from becoming Engineering authorship).**
> Owner authority over doctrine and build-governance is a **ratification gate over policy *intent***,
> not a licence to author **realization**. The Owner *ratifies* intent ("there MUST be a QA gate that
> can fail the build"; "production is human-gated"); **Engineering authors the mechanism and proposes
> policy** ("the gate runs these checks"). The Owner never writes schema, API shapes, stage
> decompositions, or build mechanics; Engineering never sets policy unilaterally. Default authoring of
> any `00_owner` build-policy is **Engineering proposes → Owner ratifies**.

---

## 2. The five zones

| Zone | Owner | Holds | Binds whom |
|---|---|---|---|
| `00_owner` | Owner only | ratified decisions, owner decision queue, open-TBD register, frameworks/manifest, **doctrine, constitution, epistemic invariants, glossary/ontology, binding build-governance policy** | both sides |
| `10_product` | Product / PM | problem, users, strategy, **domain meaning (the product *expression* of owner invariants)**, scope, experience intent, outcome acceptance + NFR **targets** | engineering |
| `20_handoff` | Shared (co-signed; **owner breaks ties**) | Impl/QA/Obs **contracts**, traceability matrix, agreed **interface** (API/event/state surface) | both sides |
| `30_engineering` | Engineering | architecture, schema, analysis-engine stages, rule-vs-LLM, stack, QA tests, delivery/CI, code | itself |
| `90_research` | Either | explorations, transcripts, legacy/raw, drafts | **no one (non-binding)** |

> **Who holds each role (resolve before applying).** `00_owner` = the **repository owner** (the sole
> ratifying authority per `CLAUDE.md`). `10_product` = the **Product Owner / PM**. These are **distinct
> roles even if one person holds both.** A single person wearing both hats MUST still file content by
> zone and declare which hat authored it (`owner:` front-matter). The Owner role must be named
> explicitly in the repo; "the PM said so" never by itself makes content `00_owner`.

---

## 3. Front-matter schema (stamp on every document)

Every doc MUST begin with this block so the zone is machine-checkable:

```yaml
---
zone: 10_product            # one of: 00_owner | 10_product | 20_handoff | 30_engineering | 90_research
owner: product              # product | engineering | owner | shared
status: binding             # binding | advisory | proposed | ratified | non-binding
source_refs: [DL-043, CAP-12, IC-WA-001]   # ids this doc traces UP to (rules/decisions/capabilities/contracts)
supersedes: null            # doc id this replaces, or null
---
```

**Field rules:**
- `zone` — exactly one. If content spans zones, the doc must be **split** (see §9), not multi-tagged.
- `owner` — who may *edit*. `shared` only valid in `20_handoff`.
- `status`:
  - `binding` — constrains what the other side must do (only valid in `00_owner`, `10_product`, `20_handoff`).
  - `advisory` — a cross-boundary opinion the receiving side may adopt, replace, or ignore.
  - `proposed` — drafted, not yet ratified.
  - `ratified` — owner-approved (only `00_owner` may set this).
  - `non-binding` — `90_research` default.
- `source_refs` — **mandatory for every doc in `20_handoff` and `30_engineering`.** A build/interface
  doc with no upstream source is an authoring error → escalate, do not invent the source.
- Doctrine, epistemic invariants, and binding build-governance use `zone: 00_owner`, `owner: owner`,
  `status: ratified` (set only by the owner). Product/engineering docs **reference** them via `source_refs`.
- For a `00_owner` build-policy doc, the realization detail it implies is **authored in `30_engineering`
  and referenced back**; the `00_owner` doc carries policy *intent* only (ratify ≠ author, §1).

---

## 4. Deterministic router (top-to-bottom, FIRST match wins)

For any unit of content (doc, section, or paragraph):

1. **Foundational doctrine / epistemic invariant, ratified decision, owner-only ruling, unresolved
   owner decision/TBD, OR binding build-governance policy** (a constraint the owner imposes on *how*
   engineering must build — e.g. deployment/QA/observability governance, the Anti-Assumption Protocol,
   implementation constraints, AI-First delivery rules)? → `00_owner`
2. **Prescribes mechanism?** (schema, field, endpoint impl, data structure, algorithm, stage
   decomposition, tech/library, test code, build step, CI) → `30_engineering`
3. **Is it the agreed interface or capability↔build mapping?** (API surface, event/state contract,
   Impl/QA/Obs contract, traceability) → `20_handoff`
4. **Defines problem, user, scope, domain meaning, behavior, or an outcome target — with NO mechanism?** → `10_product`
5. **Exploratory, historical, transcript, or explicitly non-binding?** → `90_research`

> Because this is first-match, the mechanism step (2) now catches only **engineering's own realization
> choices**, not owner-imposed build policy or doctrine (which step 1 already claimed).

> **Precedence:** *owner doctrine & owner-imposed build-policy win over mechanism; mechanism wins over
> topic; binding wins over convenient; decision wins over spec; interface wins over both sides; unsure
> wins nothing → `90_research` + escalate.*

---

## 5. Per-zone grounding cards

### `00_owner` — Decisions, Doctrine & Authority
- **Includes:** "DL-0XX ratifies…", "Owner must decide X", "TBD — owner decision required", precedence rules.
- **Includes:** Foundational epistemic invariants / doctrine (*Canonical = Attested*, *confidence ≠ probability*,
  *OSLO never self-accepts*, *Derived never shown as settled* **as a system rule**).
- **Includes:** Binding build-governance **policy intent** (deployment/QA/observability governance, Anti-Assumption
  Protocol, implementation constraints, AI-First delivery rules). Engineering *authors/proposes* the realization;
  the owner *ratifies* the intent (ratify ≠ author, §1).
- **MUST NOT contain:** the *content* of a product spec or engineering design, **nor build realization detail**
  (schema/API/stages/CI mechanics) — only the **ruling / invariant / policy intent**.
- **Litmus:** *"Is this a choice only the owner can make, a system-wide invariant, or a record that one was made?"*
- **Signals:** ratify, supersede, adopt, decision, DL-, TBD, invariant, doctrine, must-hold-system-wide, owner-approval-required.

### `10_product` — Product Ownership (WHAT / WHY / RULES)
- **Includes:** "A user needs to…", the *product expression* of domain meaning ("users must see
  uncertainty labeled", "a finding must be traceable to its basis"), "In scope: … Out: …", outcome targets.
- **NOT here:** the **invariants themselves** (e.g. *confidence ≠ probability*, *Derived never shown as
  settled* as a binding system rule) — those are **Owner doctrine (`00_owner`)**, referenced here, not authored here.
- **MUST NOT contain:** schemas, field names, endpoints, object models, stage lists, rule-vs-LLM splits,
  tech choices, test assertions, component markup. **No "how."**
- **Litmus:** *"If the entire tech stack changed, would this sentence still be true?"* Yes → Product (or Owner if it's an invariant).
- **Signals:** user, value, must/should (behavioral), scope, capability, journey, target, in/out of scope.

### `20_handoff` — The Seam (Contract & Interface)
- **Includes:** "Capability X → contract IC-WA-001, verified by QA-WA-001, observed by OBS-WA-001",
  "`POST /v1/projects` ↔ `project_created`".
- **MUST NOT contain:** the *reason* a capability exists (Product) **or** the *implementation* behind the
  interface (Engineering). Holds the **boundary, not either side of it.**
- **Two-half rule:** the *what/acceptance* half traces up to `10_product`; the *interface/shape* half
  traces down to `30_engineering`. A paragraph serving only one half belongs in that zone, not here.
- **Litmus:** *"Does this need BOTH a product source AND a build to make sense?"* Yes → Handoff.
- **Signals:** contract, traceability, interface, endpoint↔event, conformance, acceptance-trace.

### `30_engineering` — Engineering (HOW / MECHANISM)
- **Includes:** field lists, store bindings (PG/Neo4j/Mongo/Qdrant/Redis), `.py` contracts, "Stage 3 = hybrid",
  determinism tiers, migrations, build steps, CI.
- **Includes:** the **realization** of owner build-policy (the actual pipeline/gates/tests that satisfy a
  `00_owner` policy), authored here and referenced back.
- **MUST NOT contain:** new product scope, new domain rules, or new user value not sourced from
  `10_product`/`00_owner`. Needed-but-missing rule → **escalate, don't author it here.**
- Build-governance *policy* is Owner (`00_owner`); engineering holds build *realization* and may **propose**
  policy changes for owner ratification, never set them unilaterally.
- **Litmus:** *"Could a PM with no engineering background validate this?"* No → Engineering.
- **Signals:** schema, table, field, endpoint impl, object model, stage, pipeline, store, library, fixture, migration, CI.

### `90_research` — Non-canonical
- **Rule:** never binding; may inform either side; cited as **source**, never authority.
- **Litmus:** *"Is this an input/draft rather than a committed position?"* Yes → Research.

---

## 6. The five hard confusions (the boundary cuts THROUGH the topic)

| Topic | Owner / Product split | Engineering half (`30_engineering`) |
|---|---|---|
| **Domain model** (Confidence/CAF/Reliability) | the **invariant** = Owner doctrine (`00_owner`); the **user-facing meaning/banding semantics** = `10_product` | scoring realization, formulas, fields, computation |
| **API** | *nothing* — PM doesn't own APIs | interface → `20_handoff/interfaces`; impl → `30_engineering` |
| **Acceptance** | outcome-level, `10_product` ("user sees uncertainty labeled") | test assertions, fixtures, determinism tolerances |
| **UX** | behavior & intent, `10_product` ("user can trace a finding to its basis") | component markup, layout, framework, screen↔endpoint wiring |
| **NFR** | the *target*, `10_product` ("<60s") | the *mechanism* to hit it (stage budgets, parallelism, caching) |
| **Build-governance** | policy *intent* = Owner (`00_owner`) ("a QA gate MUST be able to fail the build") | the gate/pipeline *realization* = `30_engineering` |

**Cutting rule:** when a doc mixes both halves, **split it**; the invariant/intent goes to Owner, the
meaning/target/behavior goes to Product, the realization goes to Engineering, with one-line references linking them.

---

## 7. Tie-breakers (apply in order)

1. **Owner doctrine & owner build-policy beat mechanism.** A foundational invariant, or a binding
   constraint on *how* to build, is `00_owner` — even if it names a mechanism. (Owner holds the *intent*;
   Engineering still authors the *realization* — ratify ≠ author, §1.)
2. **Mechanism beats topic.** Any field name, endpoint, algorithm, or tech reference forces `30_engineering`.
3. **Binding beats convenient.** If it constrains what engineering must build → authority zone, never `30_engineering`.
4. **Decision beats spec.** "We chose X" → `00_owner`. "X works like this" → wherever the mechanism/rule lives.
5. **Interface beats both sides.** Anything two teams must agree on → `20_handoff`.
6. **Owner breaks seam *deadlocks*.** When product and engineering cannot agree on a `20_handoff` contract,
   the Owner decides (precedence: Doctrine > Constitution > Implementation). This is **deadlock-breaking,
   not routine authorship** — the contract stays co-authored; the owner does not rewrite it at will.
7. **Unsure → `90_research` + escalate.** Never guess a binding zone.

---

## 8. Global grounding invariants (every doc, every zone)

1. **One zone per document.** Spanning docs are split; cross-references replace copied content.
2. **No downward authoring.** Product may not write mechanism; Engineering may not write scope/domain rules.
   Cross-boundary opinions enter the *other* zone tagged `status: advisory`.
3. **Ratify ≠ author.** Owner authority is a ratification gate over policy intent and invariants; it does not
   author realization. Engineering authors mechanism and *proposes* policy; Owner *ratifies* it (§1).
4. **Cite the source, don't restate it.** Lower-zone docs reference upper-zone rules by id; never re-derive
   them (the source wins on conflict).
5. **Stamp front-matter** (§3) so the zone is machine-checkable.
6. **Gap → escalate, never assume.** A missing upstream rule blocks the downstream doc; raise to `00_owner`.
7. **Forbidden-content guard (hard fails):**
   - `10_product` rejects any schema/endpoint/tech token, **and any system-wide invariant** (that's Owner).
   - `30_engineering` rejects any new capability/scope with no `source_ref`, **and any unilateral policy-setting**.
   - `20_handoff` rejects any pure-rationale or pure-implementation paragraph.
   - `00_owner` rejects any build *realization* detail (schema/API/stage/CI mechanics) — intent only.

---

## 9. Worked example — splitting a mixed doc

**Input:** `05_execution/.../Phase_III_Wave_B_Understanding/IMPLEMENTATION_PLAN.md` — a single doc that
currently mixes several zones. Below, each original element is routed.

| Original element (paraphrased) | Zone | Why | Goes to |
|---|---|---|---|
| "Produce OSLO's *understanding* of the canonical record (Findings, Issues) — the user starts to learn something about a project." | `10_product` | Problem/value, no mechanism | `10_product/scope` (capability) |
| "Confidence = trust-in-understanding, **never** project health/readiness/score." | `00_owner` (epistemic invariant / doctrine) | A binding system-wide invariant, not a product choice | `00_owner` doctrine; product *expresses* it via `10_product/domain` referencing the invariant |
| "Time-to-First-MRI **< 60s** (only owner-approved numeric target)." | `00_owner` (target ratified) → referenced by `10_product` | A ratified numeric target | `00_owner` decision; cited from `10_product/acceptance` |
| "Build order: `IC-WB-INFER` then `IC-WB-EVAL`; each is a contract." | `20_handoff` | Capability↔contract mapping | `20_handoff/contracts` |
| "Findings stored as **Derived**, carry `epistemic_state=derived`, band 0–49/50–74/75–100, ±3 edge-guard." | `30_engineering` | Field names + thresholds = mechanism | `30_engineering/data` |
| "Fast Pass = 8 stages; Stage 4 CAF Eval = hybrid; rule-derived values replay exactly, AI-numeric ±7 & same band." | `30_engineering` | Stage decomposition + determinism mechanism | `30_engineering/analysis_engine` + `/qa` |
| "Negative test: reject a Derived value written to canonical as Attested." | `30_engineering` (QA) | Test-level assertion (realizing the owner invariant) | `30_engineering/qa`, `source_ref` → the `00_owner` invariant |
| "Acceptance: a recompute produces a new CHR; drift surfaced at ≥10 pts or band change." | **split** | *"drift is surfaced to the user"* = `10_product/acceptance`; *"new CHR / ≥10 pts"* = `30_engineering` | both, linked by ref |

**Result:** one mixed doc becomes (a) a product capability + user-facing expression + acceptance in `10_product`,
(b) a contract mapping in `20_handoff`, (c) an engineering realization + QA spec in `30_engineering`,
(d) the **invariants and the `<60s` target recorded once in `00_owner`** and referenced by the rest. Each new
doc carries front-matter and `source_refs` linking back up.

---

## 10. Reviewer checklist (run against any incoming doc)

- [ ] Has valid front-matter (§3); `zone`, `owner`, `status`, `source_refs` all present.
- [ ] Content is **single-zone** — no paragraph belongs to a different zone (run §4 router on each).
- [ ] **No downward authoring**: product doc contains no mechanism; engineering doc invents no scope/rule.
- [ ] Doctrine / epistemic invariants and binding build-governance live in `00_owner` — product/engineering
      **reference** them (by `source_ref`), never author them.
- [ ] **Ratify ≠ author** honored: any `00_owner` build-policy carries intent only; its realization is authored in `30_engineering`.
- [ ] The **Owner role is named** and distinct from the PM; content isn't `00_owner` merely because the PM authored it.
- [ ] Every `20_handoff`/`30_engineering` doc has a real upstream `source_ref` (not invented).
- [ ] Domain rules are **cited, not restated** from their `00_owner`/`10_product` source.
- [ ] Any cross-boundary opinion is tagged `status: advisory`, not `binding`.
- [ ] Where a `20_handoff` contract is contested, the Owner is named as **deadlock** tie-breaker (not routine author).
- [ ] Hard-fail tokens absent from the wrong zone (§8.7).
- [ ] Unresolved/ambiguous items routed to `90_research` with an escalation note (not guessed).
- [ ] If the doc mixed zones, it was **split** (§9), not relabeled whole.

---

## 11. How to use with an LLM

Paste **§3 (front-matter) + §4 (router) + §5 (cards) + §8 (invariants)** as the system rule. For any input the model must:
1. Run the §4 router **per paragraph**.
2. **Split** the doc wherever the zone changes (§9).
3. **Stamp** front-matter (§3) on each resulting piece.
4. On ambiguity, route to `90_research` and **emit an escalation note** — never guess a binding zone.
5. Reference upstream rules by `source_ref`; never copy or re-derive them.
