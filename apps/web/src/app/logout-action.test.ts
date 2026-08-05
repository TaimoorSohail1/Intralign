import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const { clearSessionCookies, readSession, redirect } = vi.hoisted(() => ({
  clearSessionCookies: vi.fn(),
  readSession: vi.fn(),
  redirect: vi.fn((path: string) => {
    throw new Error(`REDIRECT:${path}`);
  }),
}));

vi.mock("next/navigation", () => ({ redirect }));
vi.mock("@/lib/server/session", () => ({ clearSessionCookies, readSession }));

describe("logout", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    readSession.mockResolvedValue({ accessToken: "access-token" });
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("clears the local session when remote revocation fails", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("provider unavailable")));
    const { logout } = await import("./logout-action");

    await expect(logout()).rejects.toThrow("REDIRECT:/login");

    expect(clearSessionCookies).toHaveBeenCalledOnce();
    expect(redirect).toHaveBeenCalledWith("/login");
  });
});
