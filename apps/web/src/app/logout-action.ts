"use server";

import { redirect } from "next/navigation";

import { clearSessionCookies, readSession } from "@/lib/server/session";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL ?? "http://127.0.0.1:55321";
const publishableKey = process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ?? "";

export async function logout() {
  const session = await readSession();
  if (session.accessToken) {
    try {
      await fetch(`${supabaseUrl}/auth/v1/logout`, {
        method: "POST",
        cache: "no-store",
        headers: {
          apikey: publishableKey,
          authorization: `Bearer ${session.accessToken}`,
        },
        signal: AbortSignal.timeout(3_000),
      });
    } catch {
      // Remote revocation is best-effort. Never leave a user signed in locally
      // because the identity provider is temporarily slow or unavailable.
    }
  }
  await clearSessionCookies();
  redirect("/login");
}
