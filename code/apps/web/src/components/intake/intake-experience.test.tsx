import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { IntakeExperience } from "./intake-experience";

afterEach(cleanup);

describe("IntakeExperience", () => {
  it("keeps analysis blocked until the user adds meaningful input", () => {
    render(<IntakeExperience displayName="Alex" />);

    const start = screen.getByRole("button", { name: /Get my analysis/ });
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

    const templatePicker = screen.getByText(/start from a template/i).closest("details")!;
    expect(templatePicker).not.toHaveAttribute("open");
    fireEvent.click(screen.getByText(/start from a template/i));
    expect(templatePicker).toHaveAttribute("open");
    expect(screen.getAllByRole("button", { name: /Event|Marketing Campaign|Product \/ Software Launch|Strategic Initiative|Generic Project Plan/ })).toHaveLength(5);
    fireEvent.click(screen.getByRole("button", { name: "Event" }));

    expect((screen.getByLabelText("Describe your project") as HTMLTextAreaElement).value).toContain("event");
    expect(screen.getByRole("button", { name: /Get my analysis/ })).toBeEnabled();
    expect(screen.queryByText(/guided q&a/i)).not.toBeInTheDocument();
  });

  it("accepts a supported document as sufficient intake", () => {
    render(<IntakeExperience displayName="Alex" />);

    const file = new File(["project notes"], "plan.md", { type: "text/markdown" });
    fireEvent.change(screen.getByLabelText("Attach documents"), {
      target: { files: [file] },
    });

    expect(screen.getByText("plan.md")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Get my analysis/ })).toBeEnabled();
  });

  it("accepts PDF, DOCX, PPTX and XLSX together", () => {
    render(<IntakeExperience displayName="Alex" />);

    fireEvent.change(screen.getByLabelText("Attach documents"), {
      target: {
        files: [
          new File(["pdf"], "plan.pdf", { type: "application/pdf" }),
          new File(["docx"], "brief.docx"),
          new File(["pptx"], "review.pptx"),
          new File(["xlsx"], "budget.xlsx"),
        ],
      },
    });

    expect(screen.getByText("plan.pdf")).toBeInTheDocument();
    expect(screen.getByText("brief.docx")).toBeInTheDocument();
    expect(screen.getByText("review.pptx")).toBeInTheDocument();
    expect(screen.getByText("budget.xlsx")).toBeInTheDocument();
  });

  it("explains unsupported files and keeps them out of the analysis", () => {
    render(<IntakeExperience displayName="Alex" />);

    fireEvent.change(screen.getByLabelText("Attach documents"), {
      target: { files: [new File(["binary"], "installer.exe")] },
    });

    expect(screen.getByRole("alert")).toHaveTextContent(
      "installer.exe is not a supported document",
    );
    expect(screen.queryByText("installer.exe", { selector: "li" })).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Get my analysis/ })).toBeDisabled();
  });

  it("loads the sample without starting analysis automatically", () => {
    render(<IntakeExperience displayName="Alex" />);

    fireEvent.click(screen.getByRole("button", { name: /sample plan/i }));

    expect((screen.getByLabelText("Describe your project") as HTMLTextAreaElement).value).toContain("DevNorth");
    expect(screen.getByRole("button", { name: /Get my analysis/ })).toBeEnabled();
    expect(screen.queryByRole("heading", { name: "Overview" })).not.toBeInTheDocument();
  });

  it("publishes Overview, shows orientation once and allows replay", async () => {
    vi.useFakeTimers();
    localStorage.clear();
    render(<IntakeExperience displayName="Alex" />);
    fireEvent.change(screen.getByLabelText("Describe your project"), {
      target: { value: "Launch the new customer portal" },
    });

    fireEvent.click(screen.getByRole("button", { name: /Get my analysis/ }));
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

    fireEvent.click(screen.getByRole("button", { name: /Get my analysis/ }));
    await act(async () => vi.runAllTimersAsync());

    expect(screen.getByRole("heading", { name: "Overview" })).toBeInTheDocument();
    expect(screen.queryByRole("dialog", { name: "How OSLO works" })).not.toBeInTheDocument();
    vi.useRealTimers();
  });
});
