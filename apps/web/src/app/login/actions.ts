"use server";

import { redirect } from "next/navigation";

import { acceptExistingInvitation } from "@/lib/server/oslo-api";
import { writeSessionCookies } from "@/lib/server/session";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL ?? "http://127.0.0.1:55321";
const publishableKey = process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ?? "";

export async function signIn(formData: FormData) {
  const email = String(formData.get("email") ?? "").trim().toLowerCase();
  const password = String(formData.get("password") ?? "");
  const invitationToken = String(formData.get("invitation_token") ?? "");
  const staySignedIn = formData.get("stay_signed_in") === "true";
  if (invitationToken) {
    const session = await acceptExistingInvitation({
      token: invitationToken,
      email,
      password,
    });
    await writeSessionCookies(session, staySignedIn, email.split("@")[0]);
    redirect(session.welcome_required ? "/welcome" : "/intake");
  }
  const response = await fetch(`${supabaseUrl}/auth/v1/token?grant_type=password`, {
    method: "POST",
    cache: "no-store",
    headers: { apikey: publishableKey, "content-type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) throw new Error("Email or password is incorrect");
  const payload = await response.json();
  await writeSessionCookies(
    {
      user_id: payload.user.id,
      email: payload.user.email,
      workspace_id: "018f9f7e-8de2-7000-8000-000000000010",
      access_token: payload.access_token,
      refresh_token: payload.refresh_token,
      expires_in: payload.expires_in,
      welcome_required: false,
    },
    staySignedIn,
    payload.user.user_metadata?.display_name ?? email.split("@")[0],
  );
  redirect("/admin/invitations");
}
