# OSLO architecture remediation — implementation report

Date: 30 July 2026

## Outcome

The approved remediation plan has been implemented as a production-safe first
release slice. It strengthens detection accuracy, issue stability, lifecycle
integrity, source coverage, benchmark governance, and the main UI consistency
problems found during the Wayfarer audit.

This work materially improves the system, but it does **not** justify claiming
that every future document will score 9/10 or that detection is now perfect.
Three governed benchmark packs are present; the approved long-term release gate
still needs the remaining unseen benchmark corpus and repeated live runs.

## Implemented

### 1. Governed quality gates

- Added governed manifests for Wayfarer, Greenway, and Thornfield.
- Set release thresholds to:
  - at least 90% expected-finding recall;
  - 100% critical-finding recall;
  - zero documented trap findings;
  - 100% evidence-locator validity;
  - no more than 5% duplicate findings;
  - stable ratings and at least 95% issue-ID stability across repeated runs.
- Added single-run and repeated-run evaluation models and tests.

### 2. Deterministic claim and contradiction detection

- Added an evidence claim graph with stable claim and relation identities.
- Added cross-source contradiction detection for:
  - controlled overbooking versus no-confirmation-without-inventory;
  - central rate control versus property-level discounts.
- The two contradictions are emitted once as canonical critical findings with
  traceable evidence.

### 3. Structurally missing control detection

Added explicit absence checks for:

- availability targets without disaster-recovery, RTO/RPO, backup, restore or
  failover controls;
- card-payment processing without PCI DSS or equivalent security controls;
- personal-profile processing without privacy/data-protection requirements;
- user-facing interfaces without an accessibility standard and verification
  route.

These checks suppress themselves when the required control is documented.

### 4. Evidence coverage

- Initial evidence selection now reserves a representative fragment from every
  uploaded source before high-signal fragments fill the remaining model
  context.
- This prevents one large or keyword-dense document from silently crowding out
  smaller sources.

### 5. Canonical issue identity and lifecycle

- Equivalent root causes are merged across artifact impacts when the evidence
  and semantic signature identify the same defect.
- Evidence references are combined on the canonical issue.
- Active state wins when duplicate issue records disagree; a stale resolved
  copy cannot hide an addressed or open copy.
- Saving an answer moves an issue to **Addressed** unless the supplied evidence
  explicitly completes the required confirmation.
- A re-analysis that splits or rephrases an issue no longer automatically marks
  the original issue resolved without sufficient confirmation.

### 6. UI consistency

- Issues: resolved findings no longer inflate Active filter counts or appear as
  falsely hidden findings.
- Artifacts: the selected issue callout appears once in the best evidence-linked
  section, with a first-section fallback.
- Inference Map:
  - repeated upstream assumption IDs no longer create React key collisions;
  - visual claim markers are bounded at 40 while exact totals remain visible and
    accessible.
- Reports:
  - duplicate assumptions, risks, questions and recommendations are removed;
  - the seven-section report structure and editable behavior remain intact.

## Verification

### Automated

- API: **223 passed**
- Web: **110 passed**
- Ruff: **passed**
- ESLint: **passed**
- Next.js production build: **passed**

### Live browser smoke test

- Issues Active view showed 26 active findings with matching artifact,
  dimension and severity totals and no false hidden-state message.
- Inference Map preserved exact claim totals while rendering no more than 40
  markers per artifact.
- Reports rendered 35 report paragraphs with no exact normalized duplicates.
- Requirements rendered 12 sections and only one active issue callout.
- The original project tab was returned to History after testing.

### Real Wayfarer source-document check

The deterministic audit was run read-only against
`Project_Wayfarer_Business_Requirements_Document_v1.2.pdf` and produced six
evidence-backed findings:

1. Controlled overbooking conflicts with the available-inventory rule
   (Critical).
2. Central rate control conflicts with a property-level discount (Critical).
3. Availability target has no disaster-recovery requirement (Moderate).
4. Card-payment processing has no payment-security requirement (Moderate).
5. Personal-data processing has no data-protection requirement (Moderate).
6. User-facing interfaces have no accessibility requirement (Low).

## Important operational note

Existing published project snapshots are immutable historical records. They
will continue to show the findings produced by their original analysis. The
new backend behavior appears on the next governed re-analysis or on a newly
uploaded project; historical snapshots must not be silently rewritten.

## Remaining work before a defensible 9/10 release claim

1. Add and govern the remaining unseen benchmark packs so the release corpus
   contains at least ten diverse projects.
2. Execute each governed pack at least three times in the deployed provider
   environment and enforce the repeatability gates in CI.
3. Expand the claim graph beyond the implemented contradiction and
   missing-control families.
4. Decompose the still-large semantic validation module into independently
   owned rule families with explicit versioning.
5. Re-run the complete Wayfarer, Greenway and Thornfield benchmark flow after
   deployment and publish recall, critical recall, trap rate, duplicate rate,
   locator validity, runtime, rating stability and issue-ID stability.

Until those steps pass, the correct status is: **materially improved and fully
regression-tested, but not yet proven universal or 9/10 across unseen
documents**.
