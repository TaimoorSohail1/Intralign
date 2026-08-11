import { beforeEach, describe, expect, it, vi } from "vitest";

const { getSessionContext, redirect, writeSessionCookies } = vi.hoisted(() => ({
  getSessionContext: vi.fn(),
  redirect: vi.fn((path: string) => {
    throw new Error(`REDIRECT:${path}`);
  }),
  writeSessionCookies: vi.fn(),
}));

vi.mock("next/navigation", () => ({ redirect }));
vi.mock("@/lib/server/oslo-api", () => ({
  acceptExistingInvitation: vi.fn(),
  getSessionContext,
}));
vi.mock("@/lib/server/session", () => ({ writeSessionCookies }));

describe("signIn", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false }));
  });

  it("returns invalid credentials to the login page instead of throwing a server error", async () => {
    const formData = new FormData();
    formData.set("email", "person@example.com");
    formData.set("password", "wrong-password");

    const { signIn } = await import("./actions");

    await expect(signIn(formData)).rejects.toThrow(
      "REDIRECT:/login?error=invalid_credentials",
    );
    expect(redirect).toHaveBeenCalledWith("/login?error=invalid_credentials");
  });

  it("returns a reusable Owner login to that Owner's workspace", async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        user: { id: "owner-user", email: "owner@example.com", user_metadata: {} },
        access_token: "owner-access",
        refresh_token: "owner-refresh",
        expires_in: 3600,
      }),
    } as Response);
    getSessionContext.mockResolvedValueOnce({
      user_id: "owner-user",
      email: "owner@example.com",
      workspace_id: "owner-workspace",
      display_name: "Workspace Owner",
      account_role: "owner",
      welcome_required: false,
    });
    const formData = new FormData();
    formData.set("email", "owner@example.com");
    formData.set("password", "OwnerPassword123!");

    const { signIn } = await import("./actions");

    await expect(signIn(formData)).rejects.toThrow("REDIRECT:/workspace");
    expect(getSessionContext).toHaveBeenCalledWith({ accessToken: "owner-access" });
    expect(writeSessionCookies).toHaveBeenCalledWith(
      expect.objectContaining({
        user_id: "owner-user",
        workspace_id: "owner-workspace",
        access_token: "owner-access",
      }),
      false,
      "Workspace Owner",
    );
  });

  it("routes only the platform Admin to invitation administration", async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        user: { id: "admin-user", email: "admin@oslo.local", user_metadata: {} },
        access_token: "admin-access",
        refresh_token: "admin-refresh",
        expires_in: 3600,
      }),
    } as Response);
    getSessionContext.mockResolvedValueOnce({
      user_id: "admin-user",
      email: "admin@oslo.local",
      workspace_id: "managed-workspace",
      display_name: "OSLO Admin",
      account_role: "admin",
      welcome_required: false,
    });
    const formData = new FormData();
    formData.set("email", "admin@oslo.local");
    formData.set("password", "AdminPassword123!");

    const { signIn } = await import("./actions");

    await expect(signIn(formData)).rejects.toThrow("REDIRECT:/admin/invitations");
    expect(writeSessionCookies).toHaveBeenCalledWith(
      expect.objectContaining({ workspace_id: "managed-workspace" }),
      false,
      "OSLO Admin",
    );
  });
});
