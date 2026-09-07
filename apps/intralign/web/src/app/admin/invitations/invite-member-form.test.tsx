import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { InviteMemberForm } from "./invite-member-form";

const { refresh } = vi.hoisted(() => ({ refresh: vi.fn() }));

vi.mock("next/navigation", () => ({
  useRouter: () => ({ refresh }),
}));

describe("InviteMemberForm", () => {
  const writeText = vi.fn();

  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(Response.json({
      id: "invite-1",
      email: "new.member@example.com",
      activation_url: "https://app.example.com/activate?token=one-time-token",
    }, { status: 201 })));
    Object.defineProperty(navigator, "clipboard", {
      configurable: true,
      value: { writeText },
    });
  });

  afterEach(() => {
    cleanup();
    vi.clearAllMocks();
    vi.unstubAllGlobals();
  });

  it("refreshes the invitation list and presents the one-time URL in a copy dialog", async () => {
    render(<InviteMemberForm />);
    fireEvent.change(screen.getByRole("textbox", { name: "Email address" }), {
      target: { value: "new.member@example.com" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Send invitation →" }));

    expect(await screen.findByRole("dialog", { name: "Invitation link" })).toHaveTextContent(
      "Recommended only if the invitation email has not arrived.",
    );
    expect(refresh).toHaveBeenCalledTimes(1);

    const copyButton = screen.getByRole("button", { name: "Copy link" });
    fireEvent.click(copyButton);

    await waitFor(() => expect(writeText).toHaveBeenCalledWith(
      "https://app.example.com/activate?token=one-time-token",
    ));
    expect(screen.getByRole("button", { name: "Copied" })).toBeInTheDocument();
    expect(screen.getByText("Invitation link copied to the clipboard.")).toBeInTheDocument();
  });

  it("removes the one-time link when the dialog is closed", async () => {
    render(<InviteMemberForm />);
    fireEvent.change(screen.getByRole("textbox", { name: "Email address" }), {
      target: { value: "new.member@example.com" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Send invitation →" }));

    await screen.findByRole("dialog", { name: "Invitation link" });
    fireEvent.click(screen.getByRole("button", { name: "Close dialog" }));

    expect(screen.queryByRole("dialog", { name: "Invitation link" })).not.toBeInTheDocument();
  });
});
