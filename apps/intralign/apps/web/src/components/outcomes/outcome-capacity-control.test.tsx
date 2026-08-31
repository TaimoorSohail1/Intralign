import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { OutcomeCapacityControl } from "./outcome-capacity-control";

const outcome = {
  id: "outcome-1",
  workspace_id: "workspace-1",
  project_id: "project-1",
  title: "Improve successful delivery",
  status: "active",
  is_primary: true,
  provenance: "inferred",
  created_at: "2026-08-13T10:00:00Z",
  archived_at: null,
};

describe("OutcomeCapacityControl", () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it("keeps an archived Outcome visible and allows reactivation", async () => {
    const onOutcomesChange = vi.fn();
    vi.stubGlobal(
      "fetch",
      vi.fn()
        .mockResolvedValueOnce(Response.json([outcome]))
        .mockResolvedValueOnce(
          Response.json({ ...outcome, status: "archived", archived_at: "2026-08-13T11:00:00Z" }),
        ),
    );

    render(
      <OutcomeCapacityControl
        onOutcomesChange={onOutcomesChange}
        projectId="project-1"
      />,
    );
    fireEvent.click(screen.getByRole("button", { name: "Manage Outcomes" }));

    expect(await screen.findByText("Improve successful delivery")).toBeInTheDocument();
    expect(onOutcomesChange).toHaveBeenCalledWith([outcome]);
    fireEvent.click(screen.getByRole("button", { name: "Archive Improve successful delivery" }));

    await waitFor(() =>
      expect(screen.getByRole("button", { name: "Reactivate Improve successful delivery" }))
        .toBeInTheDocument(),
    );
    expect(screen.getByText("Archived · record remains viewable")).toBeInTheDocument();
  });

  it("turns a second Outcome capacity response into a named Basic choice", async () => {
    const fetchMock = vi
      .fn()
        .mockResolvedValueOnce(Response.json([outcome]))
        .mockResolvedValueOnce(
          Response.json(
            {
              message: "Free includes one active Outcome. Archive one or choose Basic.",
              detail: {
                capability: "Optimize all your outcomes",
                tier_label: "Basic",
                price_usd_monthly: 29,
              },
            },
            { status: 422 },
          ),
        )
        .mockResolvedValueOnce(Response.json({ accepted: true }));
    vi.stubGlobal("fetch", fetchMock);

    render(<OutcomeCapacityControl projectId="project-1" />);
    fireEvent.click(screen.getByRole("button", { name: "Manage Outcomes" }));
    await screen.findByText("Improve successful delivery");
    fireEvent.change(screen.getByLabelText("New Outcome"), {
      target: { value: "Reduce avoidable rework" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Add Outcome" }));

    expect(await screen.findByText("Optimize all your outcomes")).toBeInTheDocument();
    expect(screen.getByText("Basic · $29/month")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Keep both with Basic" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Archive an Outcome instead" })).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Archive an Outcome instead" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(3));
    expect(fetchMock).toHaveBeenLastCalledWith(
      "/api/workspace/intent-signals",
      expect.objectContaining({
        body: JSON.stringify({
          wall_key: "multiOutcome",
          chosen_path: "free_path",
          full_option_set: ["archive_to_switch", "upgrade_basic", "not_now"],
          context: { project_id: "project-1" },
        }),
      }),
    );
  });
});
