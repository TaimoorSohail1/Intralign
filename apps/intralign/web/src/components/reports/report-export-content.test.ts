import { describe, expect, it } from "vitest";

import type { OverviewSnapshot } from "@/lib/server/oslo-api";

import { buildPlanExport } from "./report-export-content";

const snapshot = {
  project_id: "project-export",
  project_title: "Atlas launch",
  analysis_run_id: "run-export",
  snapshot_id: "snapshot-export",
  published_at: "2026-08-15T08:30:00Z",
  artifacts: [
    {
      artifact_type: "schedule",
      title: "Schedule",
      summary: "Delivery plan",
      reliability: "Moderate",
      basis: "Documented",
      evidence_refs: ["description:1", "document:plan:page:2"],
      content: {
        sections: [
          {
            heading: "Milestones",
            body: "",
            bullets: [],
            columns: ["Task", "Owner", "Due"],
            rows: [["=IMPORTXML(\"bad\")", "Avery", "2026-09-01"]],
            row_evidence_refs: [["description:1", "document:plan:page:2"]],
          },
        ],
      },
    },
  ],
} as unknown as OverviewSnapshot;

describe("buildPlanExport", () => {
  it("creates consistent real CSV, Excel and text payloads without formula execution", () => {
    const result = buildPlanExport(snapshot);

    expect(result.csv.mime).toBe("text/csv");
    expect(result.csv.content).toContain("Analysis completed,2026-08-15T08:30:00Z");
    expect(result.csv.content).toContain("'=IMPORTXML");
    expect(result.excel.mime).toBe("application/vnd.ms-excel");
    expect(result.excel.content).toContain("Atlas launch");
    expect(result.text.content).toContain("Task: =IMPORTXML");
    expect(result.text.content).toContain("Provenance: Project description | plan, page 2");
    expect(result.text.content).not.toContain("description:1");
    expect(result.csv.content).not.toContain("confidence_explanation");
  });
});
