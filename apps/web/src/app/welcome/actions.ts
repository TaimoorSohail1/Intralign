"use server";

import { redirect } from "next/navigation";

import { OsloApiError, startProject } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function startFirstProject() {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) redirect("/login");
  let project;
  try {
    project = await startProject({
      accessToken: session.accessToken,
      workspaceId: session.workspaceId,
    });
  } catch (error) {
    if (error instanceof OsloApiError && error.status === 409) {
      redirect("/workspace?new=1");
    }
    throw error;
  }
  redirect(`/intake?project=${project.id}`);
}
