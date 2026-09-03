import { beforeEach, describe, expect, it, vi } from "vitest";

const { activateInvitation, redirect, writeSessionCookies } = vi.hoisted(() => ({
  activateInvitation: vi.fn(),
  redirect: vi.fn((path: string) => {
    throw new Error(`REDIRECT:${path}`);
  }),
  writeSessionCookies: vi.fn(),
}));

vi.mock("next/navigation", () => ({ redirect }));
vi.mock("@/lib/server/oslo-api", () => ({ activateInvitation }));
vi.mock("@/lib/server/session", () => ({ writeSessionCookies }));

describe("activateAccount", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns a recoverable error instead of crashing the activation page", async () => {
    activateInvitation.mockRejectedValueOnce(new Error("API unavailable"));
    const formData = new FormData();
    formData.set("token", "invite-token");
    formData.set("display_name", "New member");
    formData.set("password", "Password123!");

    const { activateAccount } = await import("./actions");
    const result = await activateAccount({ error: null }, formData);

    expect(result).toEqual({
      error: "OSLO could not finish activation just now. Your invitation is safe—please try again.",
    });
    expect(writeSessionCookies).not.toHaveBeenCalled();
    expect(redirect).not.toHaveBeenCalled();
  });

  it("writes the session and continues to welcome after activation", async () => {
    const session = {
      user_id: "new-user",
      email: "member@example.com",
      workspace_id: "workspace-id",
      access_token: "access-token",
      refresh_token: "refresh-token",
      expires_in: 3600,
      welcome_required: true,
    };
    activateInvitation.mockResolvedValueOnce(session);
    const formData = new FormData();
    formData.set("token", "invite-token");
    formData.set("display_name", "New member");
    formData.set("password", "Password123!");
    formData.set("stay_signed_in", "true");

    const { activateAccount } = await import("./actions");

    await expect(activateAccount({ error: null }, formData)).rejects.toThrow(
      "REDIRECT:/welcome",
    );
    expect(writeSessionCookies).toHaveBeenCalledWith(session, true, "New member");
  });
});
