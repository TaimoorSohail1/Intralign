import { notFound, redirect } from "next/navigation";

import { logout } from "@/app/logout-action";
import { ProjectOverview } from "@/components/overview/project-overview";
import { getOverview } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

const artifactTypes = new Set([
  "intent",
  "context",
  "scope",
  "requirements",
  "work_breakdown",
  "schedule",
  "resources",
]);

export default async function ArtifactPage({
  params,
}: {
  params: Promise<{ projectId: string; artifactType: string }>;
}) {
  const session = await readSession();
  if (!session.accessToken) redirect("/login");
  const { projectId, artifactType } = await params;
  if (!artifactTypes.has(artifactType)) notFound();
  let snapshot;
  try {
    snapshot = await getOverview(session.accessToken, projectId);
  } catch {
    redirect(`/intake?project=${projectId}`);
  }
  return (
    <ProjectOverview
      displayName={session.displayName ?? "Member"}
      initial={snapshot}
      initialView={artifactType as "intent"}
      logoutAction={logout}
    />
  );
}
