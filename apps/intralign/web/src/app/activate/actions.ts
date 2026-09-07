"use server";

import { redirect } from "next/navigation";

import { activateInvitation } from "@/lib/server/oslo-api";
import { writeSessionCookies } from "@/lib/server/session";

export interface ActivationActionState {
  error: string | null;
}

export async function activateAccount(
  _previousState: ActivationActionState,
  formData: FormData,
): Promise<ActivationActionState> {
  const token = String(formData.get("token") ?? "");
  const displayName = String(formData.get("display_name") ?? "").trim();
  const password = String(formData.get("password") ?? "");
  const staySignedIn = formData.get("stay_signed_in") === "true";
  try {
    const session = await activateInvitation({ token, display_name: displayName, password });
    await writeSessionCookies(session, staySignedIn, displayName);
  } catch {
    return {
      error: "OSLO could not finish activation just now. Your invitation is safe—please try again.",
    };
  }
  redirect("/welcome");
}
