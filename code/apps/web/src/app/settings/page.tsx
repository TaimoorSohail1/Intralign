import { redirect } from "next/navigation";

import { logout } from "@/app/logout-action";
import { WorkspaceSettings } from "@/components/workspace/workspace-settings";
import { getWorkspace, getWorkspacePreferences } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export default async function SettingsPage() {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) redirect("/login");
  const [workspace, preferences] = await Promise.all([
    getWorkspace({ accessToken: session.accessToken, workspaceId: session.workspaceId }),
    getWorkspacePreferences({ accessToken: session.accessToken, workspaceId: session.workspaceId }),
  ]);
  const activeProject = [...workspace.projects]
    .filter((project) => !project.archived)
    .sort((left, right) => right.updated_at.localeCompare(left.updated_at))[0];
  if (activeProject) {
    redirect(`/projects/${activeProject.id}/overview?settings=profile`);
  }
  return (
    <WorkspaceSettings
      displayName={session.displayName ?? "Member"}
      initial={preferences}
      logoutAction={logout}
      workspace={workspace}
      workspaceName={workspace.name}
    />
  );
}
