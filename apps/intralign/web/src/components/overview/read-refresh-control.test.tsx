import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { ReadRefreshControl } from "./read-refresh-control";

const exhaustedCapacity = {
  monthly_analysis_limit: 3,
  monthly_analyses_used: 3,
  monthly_analysis_resets_at: "2026-10-01",
};

describe("ReadRefreshControl", () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it("keeps the exhausted action focusable and explains when capacity resets", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);

    render(
      <ReadRefreshControl
        capacity={exhaustedCapacity}
        projectId="project-1"
      />,
    );

    const action = screen.getByRole("button", { name: "Update now" });
    const explanation = screen.getByText(/0 analyses remaining this month/);

    expect(action).not.toBeDisabled();
    expect(action).toHaveAttribute("aria-disabled", "true");
    expect(action).toHaveAttribute("aria-describedby", explanation.id);
    expect(explanation).toHaveTextContent(
      "0 analyses remaining this month. Your current read remains available. Resets 1 October 2026.",
    );

    action.focus();
    expect(action).toHaveFocus();
    fireEvent.click(action);
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("starts one unchanged Deep Pass and prevents duplicate requests", () => {
    const fetchMock = vi.fn().mockReturnValue(new Promise<Response>(() => undefined));
    vi.stubGlobal("fetch", fetchMock);

    render(
      <ReadRefreshControl
        capacity={{
          monthly_analysis_limit: null,
          monthly_analyses_used: 7,
          monthly_analysis_resets_at: "2026-10-01",
        }}
        projectId="project-1"
      />,
    );

    expect(screen.getByText(/counts as 1 analysis · no monthly cap/)).toBeVisible();
    const action = screen.getByRole("button", { name: "Update now" });
    fireEvent.click(action);
    fireEvent.click(action);

    expect(fetchMock).toHaveBeenCalledOnce();
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/projects/project-1/analysis-runs/refresh",
      { method: "POST" },
    );
    expect(screen.getByRole("button", { name: "Starting…" })).toHaveAttribute(
      "aria-disabled",
      "true",
    );
  });

  it("derives the remaining allowance from returned capacity data", () => {
    render(
      <ReadRefreshControl
        capacity={{
          monthly_analysis_limit: 5,
          monthly_analyses_used: 3,
          monthly_analysis_resets_at: "2026-10-01",
        }}
        projectId="project-1"
      />,
    );

    expect(
      screen.getByText("Runs a new Deep Pass · uses 1 of 2 analyses remaining this month."),
    ).toBeVisible();
  });

  it("loads capacity from the authenticated workspace response", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      Response.json({
        monthly_analysis_limit: 5,
        monthly_analyses_used: 4,
        monthly_analysis_resets_at: "2026-10-01",
      }),
    );
    vi.stubGlobal("fetch", fetchMock);

    render(<ReadRefreshControl projectId="project-1" />);

    expect(screen.getByRole("button", { name: "Update now" })).toHaveAttribute(
      "aria-disabled",
      "true",
    );
    await waitFor(() => expect(fetchMock).toHaveBeenCalledWith("/api/workspace", {
      cache: "no-store",
    }));
    expect(
      await screen.findByText("Runs a new Deep Pass · uses 1 of 1 analyses remaining this month."),
    ).toBeVisible();
  });

  it("keeps project data unchanged and offers retry when refresh cannot start", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(
        Response.json({ message: "raw upstream transport detail" }, { status: 502 }),
      )
      .mockReturnValueOnce(new Promise<Response>(() => undefined));
    vi.stubGlobal("fetch", fetchMock);

    render(
      <ReadRefreshControl
        capacity={{
          monthly_analysis_limit: null,
          monthly_analyses_used: 7,
          monthly_analysis_resets_at: "2026-10-01",
        }}
        projectId="project-1"
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "Update now" }));

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Analysis could not refresh. Your project data is unchanged; try again.",
    );
    expect(screen.queryByText("raw upstream transport detail")).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Try again" }));
    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(screen.getByRole("button", { name: "Starting…" })).toHaveAttribute(
      "aria-disabled",
      "true",
    );
  });
});
