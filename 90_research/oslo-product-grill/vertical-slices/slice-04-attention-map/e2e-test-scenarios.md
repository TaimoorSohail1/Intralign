# Slice 4 — Attention Map (MRI) · E2E Test Scenarios

Manual/E2E scenarios for the cumulative Slice 1–4 prototype. Reach the app via Restart → activate → intake (Sample) → analyze → land on Overview. (≤20 scenarios.)

| # | Scenario | Steps | Expected |
|---|---|---|---|
| 1 | Reach Attention (co-primary) | On Overview, click **Attention** in the top-center switch | Heatmap renders: 7 artifact rows × Clarity/Alignment/Feasibility columns |
| 2 | Reach Attention (Overview pointer) | On Overview Confidence card, click **"Attention map →"** | Lands on the Attention heatmap (D062) |
| 3 | Legend copy | Read the map bar + legend | Both state **"Brighter = more attention — not a health score."** (D057) |
| 4 | Cell shading | Inspect cells | Resources × Feasibility is brightest (l3, critical); others l1/l2; empty cells neutral l0 (D057/D060) |
| 5 | Count + severity label | Inspect a non-empty cell | Shows the open-issue count + a mini severity label; multi cell shows a "multiple" pip |
| 6 | Single-issue cell → issue | Click **Requirements × Clarity** (1 open) | The light issue panel opens **that issue** directly (D058) |
| 7 | Multi-issue cell → scoped list | Click **Resources × Feasibility** (2 open) | Scoped Issues list opens with **both filters lit**: *Plan artifact · Resources* + *Dimension · Feasibility* (D058) |
| 8 | Scoped list → open issue | In the scoped list, click a row | The issue opens; closing it returns to the scoped list underneath |
| 9 | Scoped list seam note | View the scoped panel | A dashed note says the full Issues surface arrives in Slice 6 |
| 10 | Clear a scope filter | In the scoped list, remove the Dimension chip | List re-scopes to the artifact only; removing both closes the panel |
| 11 | Row header route | Click the **Resources** row header | Opens the Resources issues (scoped, since >1) |
| 12 | Empty cell inert | Try clicking/tabbing an empty l0 cell (e.g. Intent × Feasibility) | Nothing happens; it is not focusable and does not scale on hover (D060/D061) |
| 13 | Field view toggle | Click **Field** | Heatmap hides; three dimension cards show (Clarity/Alignment/Feasibility) with open counts (D059) |
| 14 | Field card route | In Field view, click **Feasibility** | Opens the Feasibility issues (scoped, since >1) |
| 15 | Field neutral color | Inspect field cards | Levels use the neutral maturity ramp — no red/amber (D060) |
| 16 | Resolve → cell dims | Open the critical Resources issue → answer the clarification → wait | Reanalysis resolves it; the cell count drops, Feasibility shifts; heatmap + field update live (D042) |
| 17 | All-clear state | Phase bar → **Sim all-clear** | Grid replaced by the all-clear state ("Nothing needs your attention right now"), framed as attention not success (D061) |
| 18 | All-clear restore | Click **Sim all-clear** again | The full heatmap returns with prior issues restored |
| 19 | Context preserved | Scroll the Overview down → open Attention → return to Overview | Overview restores its prior scroll position (D062) |
| 20 | No regression | Exercise confidence pill popover, false-confidence trigger, tour, chat, clarification loop | All Slice 1–3 behavior works; "Plan artifacts" term intact; `node --check` passes |
