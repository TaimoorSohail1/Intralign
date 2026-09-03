import { redirect } from "next/navigation";

import { logout } from "@/app/logout-action";
import { ProjectOverview } from "@/components/overview/project-overview";
import { buildYourOutcomeProjection } from "@/components/outcomes/your-outcome-projection";
import {
  getCollaborationRollUp,
  getOverview,
  listProjectOutcomes,
} from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export default async function OutcomePage({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const session = await readSession();
  if (!session.accessToken) redirect("/login");
  const { projectId } = await params;
  if (!session.workspaceId) redirect(`/projects/${projectId}/overview`);

  let loaded;
  try {
    loaded = await Promise.all([
      getOverview(session.accessToken, projectId),
      listProjectOutcomes({
        accessToken: session.accessToken,
        workspaceId: session.workspaceId,
        projectId,
      }),
      getCollaborationRollUp(session.accessToken, projectId),
    ]);
  } catch {
    redirect(`/projects/${projectId}/overview`);
  }
  const [snapshot, outcomes, rollUp] = loaded;
  const outcomeDashboard = buildYourOutcomeProjection({ snapshot, outcomes, rollUp });

  return (
    <ProjectOverview
      displayName={session.displayName ?? "Member"}
      initial={snapshot}
      initialOutcome={outcomeDashboard.primary_outcome}
      initialOutcomeDashboard={outcomeDashboard}
      initialView="outcome"
      logoutAction={logout}
    />
  );
}
