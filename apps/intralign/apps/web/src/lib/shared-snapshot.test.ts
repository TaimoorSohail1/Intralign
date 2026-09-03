import { describe, expect, it } from "vitest";

import { openSharedIssues } from "./shared-snapshot";

describe("openSharedIssues", () => {
  it("never labels retained resolved issues as open", () => {
    expect(
      openSharedIssues([
        { id: "open", title: "Open", severity: "Critical", dimension: "Clarity", status: "open" },
        {
          id: "resolved",
          title: "Resolved",
          severity: "Moderate",
          dimension: "Alignment",
          status: "resolved",
        },
      ]).map((issue) => issue.id),
    ).toEqual(["open"]);
  });
});
