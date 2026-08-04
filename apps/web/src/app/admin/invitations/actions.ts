"use server";

import { redirect } from "next/navigation";

import {
  OsloApiError,
  resendInvitation,
  revokeInvitation,
  sendInvitation,
} from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function inviteMember(formData: FormData) {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) redirect("/login");
  const email = String(formData.get("email") ?? "").trim();
  try {
    await sendInvitation({
      accessToken: session.accessToken,
      workspaceId: session.workspaceId,
      email,
    });
  } catch (caught) {
    const message =
      caught instanceof OsloApiError && caught.status === 422
        ? "Enter a valid email address."
        : caught instanceof OsloApiError && caught.status === 409
          ? "That person already has an active invitation or workspace access."
          : "The invitation could not be sent. Please try again.";
    redirect(
      `/admin/invitations?error=${encodeURIComponent(message)}&email=${encodeURIComponent(email)}`,
    );
  }
  redirect(`/admin/invitations?sent=${encodeURIComponent(email)}`);
}

export async function resendMemberInvitation(formData: FormData) {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) redirect("/login");
  await resendInvitation({
    accessToken: session.accessToken,
    workspaceId: session.workspaceId,
    invitationId: String(formData.get("invitation_id") ?? ""),
  });
  redirect("/admin/invitations?updated=resent");
}

export async function revokeMemberInvitation(formData: FormData) {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) redirect("/login");
  await revokeInvitation({
    accessToken: session.accessToken,
    workspaceId: session.workspaceId,
    invitationId: String(formData.get("invitation_id") ?? ""),
  });
  redirect("/admin/invitations?updated=revoked");
}
