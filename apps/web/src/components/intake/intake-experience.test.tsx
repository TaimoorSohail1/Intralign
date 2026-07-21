import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { IntakeExperience } from "./intake-experience";

afterEach(cleanup);

describe("IntakeExperience", () => {
  it("keeps analysis blocked until the user adds meaningful input", () => {
    render(<IntakeExperience displayName="Alex" />);

    const start = screen.getByRole("button", { name: /See where I stand/ });
    expect(start).toBeDisabled();

    fireEvent.change(screen.getByLabelText("Describe your project"), {
      target: { value: "   " },
    });
    expect(start).toBeDisabled();

    fireEvent.change(screen.getByLabelText("Describe your project"), {
      target: { value: "Launch the new customer portal" },
    });
    expect(start).toBeEnabled();
  });

  it("seeds the composer from one of the five supported templates", () => {
    render(<IntakeExperience displayName="Alex" />);

    expect(screen.getAllByRole("button", { name: /Event|Marketing Campaign|Product \/ Software Launch|Strategic Initiative|Generic Project Plan/ })).toHaveLength(5);
    fireEvent.click(screen.getByRole("button", { name: "Event" }));

    expect((screen.getByLabelText("Describe your project") as HTMLTextAreaElement).value).toContain("event");
    expect(screen.getByRole("button", { name: /See where I stand/ })).toBeEnabled();
    expect(screen.queryByText(/guided q&a/i)).not.toBeInTheDocument();
  });

  it("accepts a supported document as sufficient intake", () => {
    render(<IntakeExperience displayName="Alex" />);

    const file = new File(["project notes"], "plan.md", { type: "text/markdown" });
    fireEvent.change(screen.getByLabelText("Attach documents"), {
      target: { files: [file] },
    });

    expect(screen.getByText("plan.md")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /See where I stand/ })).toBeEnabled();
  });

  it("loads the sample without starting analysis automatically", () => {
    render(<IntakeExperience displayName="Alex" />);

    fireEvent.click(screen.getByRole("button", { name: /sample project/i }));

    expect((screen.getByLabelText("Describe your project") as HTMLTextAreaElement).value).toContain("DevNorth");
    expect(screen.getByRole("button", { name: /See where I stand/ })).toBeEnabled();
    expect(screen.queryByRole("heading", { name: "Overview" })).not.toBeInTheDocument();
  });

  it("publishes Overview, shows orientation once and allows replay", async () => {
    vi.useFakeTimers();
    localStorage.clear();
    render(<IntakeExperience displayName="Alex" />);
    fireEvent.change(screen.getByLabelText("Describe your project"), {
      target: { value: "Launch the new customer portal" },
    });

    fireEvent.click(screen.getByRole("button", { name: /See where I stand/ }));
    expect(screen.getByRole("status")).toHaveTextContent(/Analyzing/i);
    await act(async () => vi.runAllTimersAsync());

    expect(screen.getByRole("heading", { name: "Overview" })).toBeInTheDocument();
    expect(screen.getByRole("dialog", { name: "How OSLO works" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Get started" }));
    expect(screen.queryByRole("dialog", { name: "How OSLO works" })).not.toBeInTheDocument();
    expect(localStorage.getItem("oslo_orientation_seen")).toBe("true");

    fireEvent.click(screen.getByRole("button", { name: /How OSLO works/ }));
    expect(screen.getByRole("dialog", { name: "How OSLO works" })).toBeInTheDocument();
    vi.useRealTimers();
  });

  it("does not repeat orientation after it has been recorded as seen", async () => {
    vi.useFakeTimers();
    localStorage.setItem("oslo_orientation_seen", "true");
    render(<IntakeExperience displayName="Alex" />);
    fireEvent.change(screen.getByLabelText("Describe your project"), {
      target: { value: "Launch another project" },
    });

    fireEvent.click(screen.getByRole("button", { name: /See where I stand/ }));
    await act(async () => vi.runAllTimersAsync());

    expect(screen.getByRole("heading", { name: "Overview" })).toBeInTheDocument();
    expect(screen.queryByRole("dialog", { name: "How OSLO works" })).not.toBeInTheDocument();
    vi.useRealTimers();
  });
});
