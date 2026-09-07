"use server";

import { redirect } from "next/navigation";

import { acceptExistingInvitation, getSessionContext } from "@/lib/server/oslo-api";
import { writeSessionCookies } from "@/lib/server/session";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL ?? "http://127.0.0.1:55321";
const publishableKey = process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ?? "";

export async function signIn(formData: FormData) {
  const email = String(formData.get("email") ?? "").trim().toLowerCase();
  const password = String(formData.get("password") ?? "");
  const invitationToken = String(formData.get("invitation_token") ?? "");
  const staySignedIn = formData.get("stay_signed_in") === "true";
  if (invitationToken) {
    let session;
    try {
      session = await acceptExistingInvitation({
        token: invitationToken,
        email,
        password,
      });
    } catch {
      redirect(
        `/login?invite=${encodeURIComponent(invitationToken)}&error=service_unavailable`,
      );
    }
    await writeSessionCookies(session, staySignedIn, email.split("@")[0]);
    redirect(session.welcome_required ? "/welcome" : "/intake");
  }
  const response = await fetch(`${supabaseUrl}/auth/v1/token?grant_type=password`, {
    method: "POST",
    cache: "no-store",
    headers: { apikey: publishableKey, "content-type": "application/json" },
    body: JSON.stringify({ email, password }),
  }).catch(() => null);
  if (!response) redirect("/login?error=service_unavailable");
  if (!response.ok) redirect("/login?error=invalid_credentials");
  const payload = await response.json();
  const context = await getSessionContext({ accessToken: payload.access_token }).catch(() => null);
  if (!context) redirect("/login?error=access_unavailable");
  await writeSessionCookies(
    {
      user_id: payload.user.id,
      email: payload.user.email,
      workspace_id: context.workspace_id,
      access_token: payload.access_token,
      refresh_token: payload.refresh_token,
      expires_in: payload.expires_in,
      welcome_required: context.welcome_required,
      account_role: context.account_role,
    },
    staySignedIn,
    context.display_name,
  );
  if (context.account_role === "admin") redirect("/admin/invitations");
  redirect(context.welcome_required ? "/welcome" : "/workspace");
}
