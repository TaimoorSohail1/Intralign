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
  collaborator_seat_limit: null,
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

  it("explains equal judgment and starts real hosted Basic checkout", async () => {
    const onCheckoutRedirect = vi.fn();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            id: "cs_test_123",
            url: "https://checkout.stripe.com/c/pay/cs_test_123",
          }),
          {
            status: 201,
            headers: { "content-type": "application/json" },
          },
        ),
      ),
    );

    render(
      <PlanComparisonModal
        onClose={vi.fn()}
        onCheckoutRedirect={onCheckoutRedirect}
        open
        workspace={workspace}
      />,
    );

    expect(screen.getByText("Every plan gets the same read.")).toBeInTheDocument();
    expect(screen.getByText("1 active project")).toBeInTheDocument();
    expect(screen.getByText("3 active projects")).toBeInTheDocument();
    expect(screen.getByText("1 active outcome")).toBeInTheDocument();
    expect(screen.getByText("Multiple active outcomes")).toBeInTheDocument();
    expect(screen.queryByText(/preview-only/i)).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Upgrade to Basic — $29/mo" }));

    await waitFor(() =>
      expect(onCheckoutRedirect).toHaveBeenCalledWith(
        "https://checkout.stripe.com/c/pay/cs_test_123",
      ),
    );
    expect(fetch).toHaveBeenCalledWith(
      "/api/workspace/billing/checkout",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ interval: "monthly", wall_key: "multiPlan" }),
      }),
    );
  });

});
