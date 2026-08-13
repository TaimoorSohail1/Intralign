# R2 Slices 1–3 — live browser and real-document QA rerun

**Date:** 2026-08-13  
**Branch:** `codex/release-2-build`  
**Verdict:** **NOT COMPLETE.** The three flows run, but exact prototype parity and evidence-grounded document analysis still have major open gaps.

## Audit summary

| Area | Result | Evidence |
|---|---|---|
| First-time invitation → activation → role/password → welcome → intake | **PASS** | Invitation email was delivered locally; all role choices, form controls, welcome CTA, sample plan, templates, and analysis start worked. |
| Guided first-time animation | **PASS** | The guided graph/outcome sequence rendered and Skip intro handed off to Overview. See [guided animation](screenshots/06-app-guided-animation.png). |
| Returning-client intake and analysis | **PASS** | Existing client reached the same intake surface, did not replay the first-time story, and used the returning watch-it-work analysis path. See [returning intake](screenshots/03-app-returning-intake.png). |
| Slice 1 shell, queue, advisor rail, navigation | **PARTIAL** | Core shell and controls work, but issue focus/expansion does not match the prototype and the live advisor did not answer a source-specific question. |
| Slice 2 lifecycle | **PASS functionally / FAIL visually** | Confirm → reanalysis → Resolved and Withdraw → ranked queue worked; proposal Accept/Reject and advisor Widen/Hide/Reopen worked. Expanded issue layout is not prototype-identical. |
| Slice 3 reanalysis | **PASS mechanically / FAIL semantically** | Reanalysis queued, animated, completed, refreshed counts, and returned to Overview. Extracted artifacts/issues did not faithfully represent the supplied ground truth. |
| Automated gates rerun | **PASS** | 78 focused web tests, 13 focused API tests, 4 guardrail infrastructure tests, and 17 active R2 guard tests passed. These tests do not cover the live gaps below. |

## Open gaps

| Severity | Screen / component | Prototype | Current app | Likely files |
|---|---|---|---|---|
| **Major** | Expanded issue | Opens as a stable focus layer; surrounding shell stays fixed. | Inserts a large card into the queue, moves the work column by about 192 px, and grows the page by more than 1,000 px. | `apps/web/src/components/overview/project-overview.tsx`, `apps/web/src/app/globals.css` |
| **Major** | Real-document artifacts | Each of the seven artifacts should contain its own structured, source-grounded content. | Artifact views repeat a largely generic/flattened read instead of distinct structured extraction. | `services/api/src/oslo_api/analysis/harness.py`, `services/api/src/oslo_api/analysis/workflow.py` |
| **Major** | Issue generation from evidence | Planted Atlas gaps/conflicts should become traceable issue cards. | Only four mostly generic issues appeared; several planted gaps and date/cost conflicts were absent. | `services/api/src/oslo_api/analysis/harness.py`, `services/api/src/oslo_api/analysis/completeness.py`, `services/api/src/oslo_api/analysis/integrity.py` |
| **Major** | OSLO evidence question | Should cite the £45,000 conflict source and state what to verify. | Returned the generic highest-priority delivery-capacity recommendation. The runtime followed the deterministic fallback branch, which does not interpret this evidence-specific question. | `services/api/src/oslo_api/analysis/advisor.py` |

## Real-document test

- Uploaded **9 mixed documents** to an existing client: PDF, DOCX, and XLSX.
- Ran a second clean check with the **6-document Atlas PDF pack** and its `ground_truth.json`.
- Upload/analysis/reanalysis completed without a crash; the existing project showed **84/84 grounded** and four issues.
- Field checks found some expected terms (REQ-007, PCI DSS, £1.8m/£1.845m) but missed or failed to map key facts such as the 0.5 FTE shortage, 08/22 February milestone conflict, ParcelLink confirmation gap, native-offline exclusion, and the £45,000 approval variance.
- The temporary clean QA project was archived after testing and the original workspace project was restored.

## Control coverage

Passed: invitation activation, four role choices, stay-signed-in toggle, welcome CTA, sample plan, five templates, document-analysis handoff, Skip intro, issue open/close, Evidence and alternative expanders, Confirm, Withdraw, proposal Accept/Reject, advisor Widen/Narrow/Hide/Reopen, and reanalysis completion.

The in-app browser file chooser could not be driven by the browser-control bridge, so the same authenticated local upload API was used for the files while the resulting analysis/reanalysis was observed and tested in the browser. This is a test-tool limitation, not evidence that the app file picker is broken.

## Visual evidence

- [App vs prototype expanded issue comparison](screenshots/12-expanded-issue-app-vs-prototype.png)
- [First-time Overview](screenshots/07-app-first-time-overview.png)
- [Real-document Overview](screenshots/10-app-real-document-overview.png)
- [Prototype main shell](screenshots/01-prototype-main.png)

## Final slice status

| Slice | Status | Reason |
|---|---|---|
| Slice 1 | **IN PROGRESS** | Shell works; issue layout and grounded advisor response remain open. |
| Slice 2 | **IN PROGRESS** | Lifecycle works; expanded issue is not prototype-identical. |
| Slice 3 | **IN PROGRESS** | Flow/reanalysis work; live extraction and issue fidelity fail ground-truth review. |

No production code was changed in this QA rerun.
