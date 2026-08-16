import { cleanup, render, screen, within } from "@testing-library/react";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { afterEach, describe, expect, it } from "vitest";

import { CollaborationGroundingMap, CollaborationRollUp } from "./collaboration-projections";

const node = {
  issue_id: "issue-1",
  title: "Confirm the accountable owner",
  artifact_type: "requirements",
  pillar: "Grounding",
  state: "routed" as const,
  exposure_rank: 9,
  href: "/projects/project-1/issues?issue=issue-1",
};

const collaborationStyles = readFileSync(
  resolve(process.cwd(), "src/app/globals.css"),
  "utf8",
);

afterEach(cleanup);

describe("Slice 6 read-only projections", () => {
  it("renders the owner roll-up with deep links and no write controls", () => {
    render(<CollaborationRollUp data={{
      project_id: "project-1",
      actor_role: "owner",
      integrity: {
        level: "Developing",
        limiting_pillar: "Grounding",
        decomposition: [],
        posture: "moment-in-time",
        tracking: "pending-execution",
      },
      trend: "unchanged",
      decision_queue: [node],
      reviewers: [],
      who_is_grounding_what: [{
        reviewer_name: "Amina",
        issue_id: "issue-1",
        state: "answered",
        href: node.href,
      }],
      rests_on: { grounded: 0, addressed: 0, routed: 1, inferred: 0 },
    }} />);

    expect(screen.getByRole("heading", { name: "What needs your judgment" })).toBeInTheDocument();
    expect(screen.getAllByRole("link", { name: /Confirm the accountable owner|Amina/ })).toHaveLength(2);
    expect(screen.getByText("1 answered")).toBeInTheDocument();
    expect(screen.queryByText("1 routed")).not.toBeInTheDocument();
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("renders Grounding map nodes as read-only issue deep links", () => {
    const denseNodes = Array.from({ length: 13 }, (_, index) => ({
      ...node,
      issue_id: `issue-${index + 1}`,
      title: `Load-bearing detail ${index + 1}`,
      href: `/projects/project-1/issues?issue=issue-${index + 1}`,
      state: index < 5 ? "grounded" as const : "inferred" as const,
    }));

    render(<CollaborationGroundingMap data={{
      project_id: "project-1",
      actor_role: "owner",
      counts: { grounded: 5, addressed: 0, routed: 0, inferred: 8 },
      nodes: denseNodes,
    }} />);

    expect(screen.getByRole("heading", { name: "Grounding map" })).toBeInTheDocument();
    expect(screen.getByText("what your plan rests on — grounded vs still OSLO-inferred")).toBeInTheDocument();
    const constellation = screen.getByLabelText("Grounding constellation");
    expect(constellation).toHaveAttribute("data-node-density", "overflow");
    expect(within(constellation).getAllByRole("link")).toHaveLength(6);
    expect(screen.getByText("5 of 13 load-bearing details grounded")).toBeInTheDocument();
    const additionalDetails = screen.getByLabelText("Additional grounding details");
    expect(within(additionalDetails).getAllByRole("link")).toHaveLength(7);
    expect(within(additionalDetails).getByRole("link", { name: /Load-bearing detail 13/ })).toHaveAttribute(
      "href",
      "/projects/project-1/issues?issue=issue-13",
    );
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("keeps the radial Grounding map through the prototype desktop shell width", () => {
    expect(collaborationStyles).toContain("@container (max-width: 560px)");
    expect(collaborationStyles).not.toContain("@container (max-width: 720px)");
    expect(collaborationStyles).toMatch(
      /\.grounding-constellation:not\(\.is-dense\)[^{]*\{[^}]*margin-top:\s*72px/s,
    );
  });

  it("keeps Grounding map copy readable when the saved site theme is light", () => {
    expect(collaborationStyles).toMatch(
      /:root\[data-theme="light"\] \.grounding-map-heading h1[^{]*\{[^}]*color:\s*var\(--text\)/s,
    );
    expect(collaborationStyles).toMatch(
      /:root\[data-theme="light"\] \.grounding-orbit-node strong[^{]*\{[^}]*color:\s*var\(--text\)/s,
    );
    expect(collaborationStyles).toMatch(
      /:root\[data-theme="light"\] \.grounding-orbit-node small[^{]*\{[^}]*color:\s*var\(--muted\)/s,
    );
  });

});
