"use server";

import { redirect } from "next/navigation";

import { startProject } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function startFirstProject() {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) redirect("/login");
  const project = await startProject({
    accessToken: session.accessToken,
    workspaceId: session.workspaceId,
  });
  redirect(`/intake?project=${project.id}`);
}
