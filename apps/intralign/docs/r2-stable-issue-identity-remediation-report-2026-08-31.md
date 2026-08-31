# R2 stable issue identity remediation report

Date: 2026-08-31  
Branch: `fix/r2-stable-issue-identity`  
Target PR: `idris-manley/oslo-knowledge-base#249`

## Result

The client-reported defect is confirmed and remediated in code. An issue is now
identified by the plan element and weakness it represents, rather than by
generated title/explanation wording. Rewording, reranking, severity changes, and
movement between artifacts therefore do not mint a new issue key.

## Defect and resolution

| Concern | Before | After | Result |
| --- | --- | --- | --- |
| Reworded finding | Identity hash changed with title/why text | Identity uses `graph_node_id + finding_type + structural_target` | Resolved |
| Finding moves artifact | Matching was restricted to the same artifact | Semantic identity is artifact-independent | Resolved |
| User confirmation disappears | Changed issue key no longer joined to the saved attestation | Stable semantic key remains the same, so the join remains valid | Resolved for new and immediate legacy reruns |
| Duplicate semantic keys | Two generated findings could collide | Assessment validation rejects duplicate semantic identities | Resolved, fail-closed |
| Unknown plan-element anchor | A finding could reference a missing graph node | Assessment validation rejects unknown graph nodes | Resolved, fail-closed |
| Existing saved snapshots | Semantic anchor was not persisted | `graph_node_id`, finding type, and target are stored and restored | Resolved |
| Legacy rollout | First V2 rerun could replace the current legacy key | Unique legacy match preserves the existing key | Resolved |
| Ambiguous legacy match | Heuristic could guess the wrong historical issue | Ambiguous matches are not guessed | Resolved, fail-closed |

Already-orphaned attestations from older staging runs are not deleted by this
change. If one was orphaned before deployment, it needs a one-time data repair
after the affected project and keys are identified. The fix prevents recurrence.

## Verification

| Gate | Result |
| --- | --- |
| Identity/OpenAI/persistence regression tests | 46 passed |
| Full API suite | Passed (445 tests collected) |
| Ruff | Passed |
| Web unit/component suite | 297 passed |
| Web lint | Passed |
| Production build | Passed |
| R2 guardrails | Passed: 43 API + 120 web active checks; 6/6 prototype corrections |
| Local browser sign-in/workspace | Passed |
| Local browser main R2 views | Passed: Issues, Outcome, Grounding Map, Reports, History |
| Local browser artifacts | Passed: all seven artifacts |
| Local browser Full Plan | Passed |
| Browser console errors on checked routes | 0 |

The browser verification used the production build locally against the local API
and seeded database. Staging is not changed by this branch until the PR is merged
and deployed.

## Files changed

- `services/api/src/oslo_api/analysis/models.py`
- `services/api/src/oslo_api/analysis/openai_harness.py`
- `services/api/src/oslo_api/analysis/issue_identity.py`
- `services/api/src/oslo_api/analysis/persistence.py`
- Regression tests for identity, provider schema, and snapshot persistence

