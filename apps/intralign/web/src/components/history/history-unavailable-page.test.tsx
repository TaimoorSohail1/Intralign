import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { HistoryUnavailablePage } from "./history-unavailable-page";

describe("HistoryUnavailablePage", () => {
  it("keeps a History outage on the History surface instead of sending the user to Intake", () => {
    render(<HistoryUnavailablePage projectId="project-123" />);

    expect(screen.getByRole("status")).toHaveTextContent("Project History is temporarily unavailable.");
    expect(screen.getByRole("status")).toHaveTextContent("Your project data is unchanged.");
    expect(screen.getByRole("link", { name: "Try History again" })).toHaveAttribute(
      "href",
      "/projects/project-123/history",
    );
    expect(screen.queryByRole("link", { name: "Analysis" })).not.toBeInTheDocument();
  });
});
