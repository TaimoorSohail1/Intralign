import { describe, expect, it } from "vitest";

import {
  defaultIssueFilters,
  issueFiltersToSearchParams,
  parseIssueFilters,
} from "./issue-filters";

describe("issue filters", () => {
  it("accepts canonical shareable filters", () => {
    expect(
      parseIssueFilters({
        artifact: "schedule",
        dimension: "feasibility",
        severity: "Critical",
        status: "addressed",
      }),
    ).toEqual({
      artifact: "schedule",
      dimension: "feasibility",
      severity: "Critical",
      status: "addressed",
    });
  });

  it("ignores invalid query values", () => {
    expect(
      parseIssueFilters({
        artifact: "unknown",
        dimension: "health",
        severity: "urgent",
        status: "deleted",
      }),
    ).toEqual(defaultIssueFilters);
  });

  it("omits default filters from the URL", () => {
    expect(issueFiltersToSearchParams(defaultIssueFilters).toString()).toBe("");
    expect(
      issueFiltersToSearchParams({
        ...defaultIssueFilters,
        artifact: "resources",
        dimension: "feasibility",
      }).toString(),
    ).toBe("artifact=resources&dimension=feasibility");
  });
});
