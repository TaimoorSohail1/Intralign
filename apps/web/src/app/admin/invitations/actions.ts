"use server";

import { redirect } from "next/navigation";

import { resendInvitation, revokeInvitation, sendInvitation } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function inviteMember(formData: FormData) {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) redirect("/login");
  const email = String(formData.get("email") ?? "");
  const role = String(formData.get("role") ?? "collaborator");
  await sendInvitation({ accessToken: session.accessToken, workspaceId: session.workspaceId, email, role });
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
