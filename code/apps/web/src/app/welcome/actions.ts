"use server";

import { redirect } from "next/navigation";

import { completeWelcome, OsloApiError, startProject } from "@/lib/server/oslo-api";
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
    const capacityCode =
      error instanceof OsloApiError &&
      typeof error.detail === "object" &&
      error.detail !== null &&
      "code" in error.detail
        ? error.detail.code
        : null;
    if (
      error instanceof OsloApiError &&
      ((error.status === 409 && capacityCode === "ACTIVE_PROJECT_LIMIT_REACHED") ||
        (error.status === 422 && capacityCode === "CAPACITY_COMMITMENT_REQUIRED"))
    ) {
      await completeWelcome({
        accessToken: session.accessToken,
        workspaceId: session.workspaceId,
      });
      redirect("/workspace");
    }
    throw error;
  }
  redirect(`/intake?project=${project.id}`);
}
