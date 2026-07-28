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
  active_project_limit: 1,
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
      active_project_limit: 3,
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
    expect(screen.getByText(/no payment method, invoice, or charge/i)).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Simulate upgrade" }));

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

  it("does not allow collaborators to change the workspace plan", () => {
    render(
      <PlanComparisonModal
        onClose={vi.fn()}
        onWorkspaceChange={vi.fn()}
        open
        workspace={{ ...workspace, role: "collaborator", can_manage_plan: false }}
      />,
    );

    expect(screen.getByText(/Only the workspace owner/)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Simulate upgrade" })).toBeDisabled();
  });
});
