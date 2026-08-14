import { redirect } from "next/navigation";

import { logout } from "@/app/logout-action";
import { IntakeExperience } from "@/components/intake/intake-experience";
import { getWorkspace } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export default async function IntakePage({
  searchParams,
}: {
  searchParams: Promise<{ project?: string; returning?: string }>;
}) {
  const session = await readSession();
  if (!session.accessToken) redirect("/login");
  const { project, returning } = await searchParams;
  if (!project) redirect("/welcome");
  const workspace = session.workspaceId
    ? await getWorkspace({
        accessToken: session.accessToken,
        workspaceId: session.workspaceId,
      }).catch(() => null)
    : null;
  const existingProject = workspace?.projects.find((candidate) => candidate.id === project);
  const analysisKind =
    existingProject && existingProject.analysis_status !== "not_analyzed"
      ? "extended"
      : "initial";
  return (
    <IntakeExperience
      analysisKind={analysisKind}
      displayName={session.displayName ?? "there"}
      logoutAction={logout}
      projectId={project}
      returningClient={returning === "1"}
    />
  );
}
