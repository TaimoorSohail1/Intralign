# Zone Grounding Rules

> **Status:** Working draft (proposed) — not ratified canonical governance.
> **Purpose:** Deterministically classify any document, section, or paragraph into exactly one
> ownership **zone**, so that an LLM (or a person) never files product content under engineering,
> or vice versa. This is a **filing + authoring rulebook**, not a spec of the product.
> **Operates alongside:** `ANTI_ASSUMPTION_BUILD_PROTOCOL.md` (escalation), `CANONICAL_GLOSSARY.md`
> (naming), `CLAUDE.md` (authority — owner ratifies).

---

## 1. The single axis everything resolves to

Every sentence is one of:

- **WHAT / WHY / RULE** → Product
- **HOW / MECHANISM** → Engineering
- **THE AGREED INTERFACE** between them → Handoff
- **A binding decision / unresolved owner choice** → Owner
- **Non-binding exploration** → Research

> If a sentence answers *"what must be true / why / for whom"* → **Product**.
> If it answers *"how is it built / with what structure"* → **Engineering**.
> If it is *the negotiated agreement that lets engineering start from product* → **Handoff**.

**Classify by what a sentence *does*, not what it is *about*.** A paragraph about "Confidence"
that contains a formula or a column name is Engineering, even though Confidence is a product concept.

---

## 2. The five zones

| Zone | Owner | Holds | Binds whom |
|---|---|---|---|
| `00_owner` | Owner only | ratified decisions, owner decision queue, open-TBD register, frameworks/manifest | both sides |
| `10_product` | Product / PM | problem, users, strategy, **domain meaning & invariants**, scope, experience intent, outcome acceptance + NFR **targets** | engineering |
| `20_handoff` | Shared (co-signed) | Impl/QA/Obs **contracts**, traceability matrix, agreed **interface** (API/event/state surface) | both sides |
| `30_engineering` | Engineering | architecture, schema, analysis-engine stages, rule-vs-LLM, stack, QA tests, delivery/CI, code | itself |
| `90_research` | Either | explorations, transcripts, legacy/raw, drafts | **no one (non-binding)** |

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

---

## 4. Deterministic router (top-to-bottom, FIRST match wins)

For any unit of content (doc, section, or paragraph):

1. **Ratified decision, owner-only ruling, or unresolved owner decision/TBD?** → `00_owner`
2. **Prescribes mechanism?** (schema, field, endpoint impl, data structure, algorithm, stage
   decomposition, tech/library, test code, build step, CI) → `30_engineering`
3. **Is it the agreed interface or capability↔build mapping?** (API surface, event/state contract,
   Impl/QA/Obs contract, traceability) → `20_handoff`
4. **Defines problem, user, scope, domain meaning, behavior, or an outcome target — with NO mechanism?** → `10_product`
5. **Exploratory, historical, transcript, or explicitly non-binding?** → `90_research`

> **Precedence:** *mechanism wins over topic; binding wins over convenient; decision wins over spec;
> interface wins over both sides; unsure wins nothing → `90_research` + escalate.*

---

## 5. Per-zone grounding cards

### `00_owner` — Decisions & Authority
- **Includes:** "DL-0XX ratifies…", "Owner must decide X", "TBD — owner decision required", precedence rules.
- **MUST NOT contain:** the *content* of a product spec or engineering design — only the **ruling about** it.
- **Litmus:** *"Is this a choice only the owner can make, or a record that one was made?"*
- **Signals:** ratify, supersede, adopt, decision, DL-, TBD, owner-approval-required.

### `10_product` — Product Ownership (WHAT / WHY / RULES)
- **Includes:** "A user needs to…", "Confidence *means* trust-in-understanding, never project health",
  "Derived must never be shown as settled", "First orientation must arrive in <60s", "In scope: … Out: …".
- **MUST NOT contain:** schemas, field names, endpoints, object models, stage lists, rule-vs-LLM splits,
  tech choices, test assertions, component markup. **No "how."**
- **Litmus:** *"If the entire tech stack changed, would this sentence still be true?"* Yes → Product.
- **Signals:** user, value, must/should (behavioral), means, scope, capability, journey, target, in/out of scope.

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
- **MUST NOT contain:** new product scope, new domain rules, or new user value not sourced from
  `10_product`/`00_owner`. Needed-but-missing rule → **escalate, don't author it here.**
- **Litmus:** *"Could a PM with no engineering background validate this?"* No → Engineering.
- **Signals:** schema, table, field, endpoint impl, object model, stage, pipeline, store, library, fixture, migration, CI.

### `90_research` — Non-canonical
- **Rule:** never binding; may inform either side; cited as **source**, never authority.
- **Litmus:** *"Is this an input/draft rather than a committed position?"* Yes → Research.

---

## 6. The five hard confusions (the boundary cuts THROUGH the topic)

| Topic | Product half (`10_product`) | Engineering half (`30_engineering`) |
|---|---|---|
| **Domain model** (Confidence/CAF/Reliability) | what it *means*, invariants, banding *semantics* | scoring realization, formulas, fields, computation |
| **API** | *nothing* — PM doesn't own APIs | interface → `20_handoff/interfaces`; impl → `30_engineering` |
| **Acceptance** | outcome-level ("user sees uncertainty labeled") | test assertions, fixtures, determinism tolerances |
| **UX** | behavior & intent ("user can trace a finding to its basis") | component markup, layout, framework, screen↔endpoint wiring |
| **NFR** | the *target* ("<60s") | the *mechanism* to hit it (stage budgets, parallelism, caching) |

**Cutting rule:** when a doc mixes both halves, **split it**; the meaning/target/behavior sentences go up,
the realization sentences go down, a one-line reference links them.

---

## 7. Tie-breakers (apply in order)

1. **Mechanism beats topic.** Any field name, endpoint, algorithm, or tech reference forces `30_engineering`.
2. **Binding beats convenient.** If it constrains what engineering must build → authority zone, never `30_engineering`.
3. **Decision beats spec.** "We chose X" → `00_owner`. "X works like this" → wherever the mechanism/rule lives.
4. **Interface beats both sides.** Anything two teams must agree on → `20_handoff`.
5. **Unsure → `90_research` + escalate.** Never guess a binding zone.

---

## 8. Global grounding invariants (every doc, every zone)

1. **One zone per document.** Spanning docs are split; cross-references replace copied content.
2. **No downward authoring.** Product may not write mechanism; Engineering may not write scope/domain rules.
   Cross-boundary opinions enter the *other* zone tagged `status: advisory`.
3. **Cite the source, don't restate it.** Lower-zone docs reference upper-zone rules by id; never re-derive
   them (the source wins on conflict).
4. **Stamp front-matter** (§3) so the zone is machine-checkable.
5. **Gap → escalate, never assume.** A missing upstream rule blocks the downstream doc; raise to `00_owner`.
6. **Forbidden-content guard (hard fails):**
   - `10_product` rejects any schema/endpoint/tech token.
   - `30_engineering` rejects any new capability/scope with no `source_ref`.
   - `20_handoff` rejects any pure-rationale or pure-implementation paragraph.

---

## 9. Worked example — splitting a mixed doc

**Input:** `05_execution/.../Phase_III_Wave_B_Understanding/IMPLEMENTATION_PLAN.md` — a single doc that
currently mixes four zones. Below, each original element is routed.

| Original element (paraphrased) | Zone | Why | Goes to |
|---|---|---|---|
| "Produce OSLO's *understanding* of the canonical record (Findings, Issues) — the user starts to learn something about a project." | `10_product` | Problem/value, no mechanism | `10_product/scope` (capability) |
| "Confidence = trust-in-understanding, **never** project health/readiness/score." | `10_product` (domain invariant) | Domain *meaning* + rule; tech-independent | `10_product/domain` |
| "Time-to-First-MRI **< 60s** (only owner-approved numeric target)." | `00_owner` (target ratified) → referenced by `10_product` | A ratified numeric target | `00_owner` decision; cited from `10_product/acceptance` |
| "Build order: `IC-WB-INFER` then `IC-WB-EVAL`; each is a contract." | `20_handoff` | Capability↔contract mapping | `20_handoff/contracts` |
| "Findings stored as **Derived**, carry `epistemic_state=derived`, band 0–49/50–74/75–100, ±3 edge-guard." | `30_engineering` | Field names + thresholds = mechanism | `30_engineering/data` |
| "Fast Pass = 8 stages; Stage 4 CAF Eval = hybrid; rule-derived values replay exactly, AI-numeric ±7 & same band." | `30_engineering` | Stage decomposition + determinism mechanism | `30_engineering/analysis_engine` + `/qa` |
| "Negative test: reject a Derived value written to canonical as Attested." | `30_engineering` (QA) | Test-level assertion | `30_engineering/qa` |
| "Acceptance: a recompute produces a new CHR; drift surfaced at ≥10 pts or band change." | **split** | *"drift is surfaced to the user"* = `10_product/acceptance`; *"new CHR / ≥10 pts"* = `30_engineering` | both, linked by ref |

**Result:** one mixed doc becomes (a) a product capability + domain rule + acceptance criteria in `10_product`,
(b) a contract mapping in `20_handoff`, (c) an engineering realization + QA spec in `30_engineering`,
(d) a `<60s` target recorded once in `00_owner`. Each new doc carries front-matter and `source_refs` linking back up.

---

## 10. Reviewer checklist (run against any incoming doc)

- [ ] Has valid front-matter (§3); `zone`, `owner`, `status`, `source_refs` all present.
- [ ] Content is **single-zone** — no paragraph belongs to a different zone (run §4 router on each).
- [ ] **No downward authoring**: product doc contains no mechanism; engineering doc invents no scope/rule.
- [ ] Every `20_handoff`/`30_engineering` doc has a real upstream `source_ref` (not invented).
- [ ] Domain rules are **cited, not restated** from their `10_product`/`00_owner` source.
- [ ] Any cross-boundary opinion is tagged `status: advisory`, not `binding`.
- [ ] Hard-fail tokens absent from the wrong zone (§8.6).
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
