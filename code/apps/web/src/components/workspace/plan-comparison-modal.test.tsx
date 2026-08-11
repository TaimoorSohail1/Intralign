import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { WorkspaceSummary } from "@/lib/server/oslo-api";

import { PlanComparisonModal } from "./plan-comparison-modal";

const workspace: WorkspaceSummary = {
  id: "workspace-1",
  name: "OSLO Alpha",
  role: "owner",
  plan: "free",
  plan_label: "Free",
  price_usd_monthly: 0,
  document_limit: 20,
  word_limit: 50_000,
  collaborator_seat_limit: 3,
  monthly_analysis_limit: null,
  monthly_analyses_used: 2,
  can_manage_plan: true,
  projects: [],
  notifications: [],
};

describe("PlanComparisonModal", () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it("explains equal judgment and activates Basic without a charge", async () => {
    const updated = {
      ...workspace,
      plan: "basic" as const,
      plan_label: "Basic",
      price_usd_monthly: 12,
      document_limit: 40,
      word_limit: 100_000,
      collaborator_seat_limit: 10,
    };
    const onWorkspaceChange = vi.fn();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify(updated), {
          status: 200,
          headers: { "content-type": "application/json" },
        }),
      ),
    );

    render(
      <PlanComparisonModal
        onClose={vi.fn()}
        onWorkspaceChange={onWorkspaceChange}
        open
        workspace={workspace}
      />,
    );

    expect(screen.getByText("Every plan gets the same read.")).toBeInTheDocument();
    expect(screen.getByText("1 active project")).toBeInTheDocument();
    expect(screen.getByText("3 active projects")).toBeInTheDocument();
    expect(screen.getAllByText(/no card, no charge/i)).toHaveLength(2);

    fireEvent.click(screen.getByRole("button", { name: "Upgrade to Basic — $12/mo." }));

    await waitFor(() => expect(onWorkspaceChange).toHaveBeenCalledWith(updated));
    expect(fetch).toHaveBeenCalledWith(
      "/api/workspace/plan",
      expect.objectContaining({
        method: "PUT",
        body: JSON.stringify({ plan: "basic" }),
      }),
    );
    expect(await screen.findByText(/No card was charged/)).toBeInTheDocument();
  });

});
