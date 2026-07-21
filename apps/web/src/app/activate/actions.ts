"use server";

import { redirect } from "next/navigation";

import { activateInvitation } from "@/lib/server/oslo-api";
import { writeSessionCookies } from "@/lib/server/session";

export async function activateAccount(formData: FormData) {
  const token = String(formData.get("token") ?? "");
  const displayName = String(formData.get("display_name") ?? "").trim();
  const password = String(formData.get("password") ?? "");
  const confirmPassword = String(formData.get("confirm_password") ?? "");
  if (password !== confirmPassword) throw new Error("Passwords do not match");
  const staySignedIn = formData.get("stay_signed_in") === "true";
  const session = await activateInvitation({ token, display_name: displayName, password });
  await writeSessionCookies(session, staySignedIn, displayName);
  redirect("/welcome");
}
