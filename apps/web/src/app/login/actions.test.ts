import { beforeEach, describe, expect, it, vi } from "vitest";

const { redirect } = vi.hoisted(() => ({
  redirect: vi.fn((path: string) => {
    throw new Error(`REDIRECT:${path}`);
  }),
}));

vi.mock("next/navigation", () => ({ redirect }));
vi.mock("@/lib/server/oslo-api", () => ({ acceptExistingInvitation: vi.fn() }));
vi.mock("@/lib/server/session", () => ({ writeSessionCookies: vi.fn() }));

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
});
