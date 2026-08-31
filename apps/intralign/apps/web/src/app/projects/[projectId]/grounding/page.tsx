import { redirect } from "next/navigation";

import { logout } from "@/app/logout-action";
import { ProjectOverview } from "@/components/overview/project-overview";
import { getCollaborationGroundingMap, getOverview } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export default async function GroundingMapPage({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const session = await readSession();
  if (!session.accessToken) redirect("/login");
  const { projectId } = await params;
  let snapshot;
  let groundingMap;
  try {
    [snapshot, groundingMap] = await Promise.all([
      getOverview(session.accessToken, projectId),
      getCollaborationGroundingMap(session.accessToken, projectId),
    ]);
  } catch {
    redirect(`/projects/${projectId}/overview`);
  }
  return (
    <ProjectOverview
      displayName={session.displayName ?? "Member"}
      initial={snapshot}
      initialGroundingMap={groundingMap}
      initialView="grounding"
      logoutAction={logout}
    />
  );
}
