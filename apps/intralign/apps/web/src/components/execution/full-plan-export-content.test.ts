import { describe, expect, it } from "vitest";

import type { OverviewSnapshot } from "@/lib/server/oslo-api";

import { buildFullPlanExport } from "./full-plan-export-content";
import type { FullPlanProjection } from "./full-plan-projection";

const snapshot = {
  project_id: "project-export",
  project_title: "Atlas B2B Launch",
  analysis_run_id: "run-export",
  snapshot_id: "snapshot-export",
  published_at: "2026-08-17T08:30:00Z",
  assessment: {
    integrity: { level: "Fragile", limiting_pillar: "Grounding" },
  },
} as unknown as OverviewSnapshot;

const projection: FullPlanProjection = {
  confirmedCount: 1,
  inferredCount: 1,
  proposedCount: 0,
  missingWorkBreakdown: false,
  rows: [
    {
      id: "task-1",
      task: '=IMPORTXML("unsafe")',
      workPackage: "Checkout",
      deliverable: "Commerce platform",
      owner: "Dana",
      start: "2026-09-01",
      due: "2026-09-12",
      schedule: "2026-09-01 – 2026-09-12",
      state: "yours",
      provenance: ["document:plan:page:3"],
      note: "PCI boundary",
    },
    {
      id: "task-2",
      task: "Test recovery",
      workPackage: "Checkout",
      deliverable: "Commerce platform",
      owner: null,
      start: null,
      due: null,
      schedule: null,
      state: "inferred",
      provenance: [],
      note: "",
    },
  ],
};

describe("buildFullPlanExport", () => {
  it("creates stable CSV, Excel and text payloads from the same combined plan", () => {
    const exportPayload = buildFullPlanExport(snapshot, projection);

    expect(exportPayload.baseName).toBe("atlas-b2b-launch-full-plan");
    expect(exportPayload.csv.content).toContain(
      "Deliverable,Workstream,Task,Owner,Start,Due,Provenance,Note",
    );
    expect(exportPayload.csv.content).toContain("'=IMPORTXML");
    expect(exportPayload.excel.mime).toBe("application/vnd.ms-excel");
    expect(exportPayload.excel.content).toContain("Atlas B2B Launch — Full plan");
    expect(exportPayload.text.content).toContain("OSLO advisory disclaimer");
    expect(exportPayload.text.content).toContain("Warning: 1 task is unowned; 1 task is unscheduled.");
  });

  it("never leaks internal assessment fields into the PM-facing export", () => {
    const exportPayload = buildFullPlanExport(snapshot, projection);

    expect(exportPayload.csv.content).not.toContain("limiting_pillar");
    expect(exportPayload.text.content).not.toContain("confidence_explanation");
  });
});
