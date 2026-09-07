import { beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  getOverview: vi.fn(),
  getProjectArtifact: vi.fn(),
  getProjectIssueProposals: vi.fn(),
  projectOverview: vi.fn(),
  readSession: vi.fn(),
  redirect: vi.fn((location: string) => {
    throw new Error(`redirect:${location}`);
  }),
  withCurrentFullPlanArtifacts: vi.fn(),
}));

vi.mock("next/navigation", () => ({ redirect: mocks.redirect }));
vi.mock("@/app/logout-action", () => ({ logout: vi.fn() }));
vi.mock("@/components/execution/full-plan-projection", () => ({
  withCurrentFullPlanArtifacts: mocks.withCurrentFullPlanArtifacts,
}));
vi.mock("@/components/overview/project-overview", () => ({
  ProjectOverview: mocks.projectOverview,
}));
vi.mock("@/lib/server/oslo-api", () => ({
  getOverview: mocks.getOverview,
  getProjectArtifact: mocks.getProjectArtifact,
  getProjectIssueProposals: mocks.getProjectIssueProposals,
}));
vi.mock("@/lib/server/session", () => ({ readSession: mocks.readSession }));

import FullPlanPage from "./page";

describe("FullPlanPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocks.readSession.mockResolvedValue({
      accessToken: "access-token",
      displayName: "Member",
    });
    mocks.getOverview.mockResolvedValue({ project_id: "project-full-plan" });
    mocks.getProjectIssueProposals.mockResolvedValue([]);
    mocks.getProjectArtifact.mockImplementation(
      async (_accessToken: string, _projectId: string, artifactType: string) => {
        if (artifactType === "resources") throw new Error("Resources unavailable");
        return { artifact_type: artifactType };
      },
    );
    mocks.withCurrentFullPlanArtifacts.mockImplementation(
      (overview, artifacts) => ({ ...overview, current_artifacts: artifacts }),
    );
  });

  it("keeps an established project on Full Plan when one artifact refresh is unavailable", async () => {
    const result = await FullPlanPage({
      params: Promise.resolve({ projectId: "project-full-plan" }),
    });

    expect(mocks.redirect).not.toHaveBeenCalled();
    expect(mocks.withCurrentFullPlanArtifacts).toHaveBeenCalledWith(
      { project_id: "project-full-plan" },
      [{ artifact_type: "work_breakdown" }, { artifact_type: "schedule" }],
    );
    expect(result.props.initialView).toBe("full_plan");
  });
});
