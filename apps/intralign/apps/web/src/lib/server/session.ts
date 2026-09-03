import "server-only";

import { cookies } from "next/headers";

import type { SessionPayload } from "./oslo-api";

const secure = process.env.NODE_ENV === "production";

export async function writeSessionCookies(
  session: SessionPayload,
  staySignedIn: boolean,
  displayName: string,
) {
  const cookieStore = await cookies();
  const refreshLifetime = staySignedIn ? 60 * 60 * 24 * 30 : 60 * 60 * 24;
  const common = { httpOnly: true, sameSite: "lax" as const, secure, path: "/" };
  cookieStore.set("oslo_access_token", session.access_token, { ...common, maxAge: session.expires_in });
  cookieStore.set("oslo_refresh_token", session.refresh_token, { ...common, maxAge: refreshLifetime });
  cookieStore.set("oslo_workspace_id", session.workspace_id, { ...common, maxAge: refreshLifetime });
  cookieStore.set("oslo_display_name", displayName, { ...common, maxAge: refreshLifetime });
  cookieStore.set("oslo_account_role", session.account_role ?? "owner", {
    ...common,
    maxAge: refreshLifetime,
  });
  cookieStore.set("oslo_session_lifetime", String(refreshLifetime), {
    ...common,
    maxAge: refreshLifetime,
  });
}

export async function readSession() {
  const cookieStore = await cookies();
  return {
    accessToken: cookieStore.get("oslo_access_token")?.value,
    workspaceId: cookieStore.get("oslo_workspace_id")?.value,
    displayName: cookieStore.get("oslo_display_name")?.value,
    accountRole: cookieStore.get("oslo_account_role")?.value,
  };
}

export async function clearSessionCookies() {
  const cookieStore = await cookies();
  for (const name of [
    "oslo_access_token",
    "oslo_refresh_token",
    "oslo_workspace_id",
    "oslo_display_name",
    "oslo_account_role",
    "oslo_session_lifetime",
  ]) {
    cookieStore.delete(name);
  }
}
