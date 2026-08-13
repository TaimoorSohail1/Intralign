import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { resolveInvitation } from "@/lib/server/oslo-api";

import ActivatePage from "./page";

vi.mock("@/lib/server/oslo-api", () => ({
  resolveInvitation: vi.fn(),
}));

vi.mock("./actions", () => ({
  activateAccount: vi.fn(),
}));

describe("ActivatePage", () => {
  afterEach(() => {
    cleanup();
    vi.clearAllMocks();
  });

  it("shows a recoverable unavailable state when invitation lookup fails", async () => {
    vi.mocked(resolveInvitation).mockRejectedValueOnce(new Error("API unavailable"));

    render(await ActivatePage({ searchParams: Promise.resolve({ token: "invite-token" }) }));

    expect(screen.getByRole("heading", { name: /This link can/i })).toBeInTheDocument();
    expect(screen.getByText(/Ask your workspace Owner for a new invitation/i))
      .toBeInTheDocument();
  });

  it("renders the activation form for a valid new-account invitation", async () => {
    vi.mocked(resolveInvitation).mockResolvedValueOnce({
      email: "member@example.com",
      workspace_name: "OSLO Product Grill",
      account_exists: false,
      expires_at: "2026-08-20T12:00:00Z",
      status: "pending",
    });

    render(await ActivatePage({ searchParams: Promise.resolve({ token: "invite-token" }) }));

    expect(screen.getByRole("heading", { name: "Activate your account" })).toBeInTheDocument();
    expect(screen.getByDisplayValue("member@example.com")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Create account/i })).toBeInTheDocument();
  });
});
