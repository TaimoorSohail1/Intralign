import { redirect } from "next/navigation";

import { logout } from "@/app/logout-action";
import { ProjectOverview } from "@/components/overview/project-overview";
import { getOverview, getProjectHistory } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export default async function InferencePage({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const session = await readSession();
  if (!session.accessToken) redirect("/login");
  const { projectId } = await params;
  let snapshot;
  let history;
  try {
    [snapshot, history] = await Promise.all([
      getOverview(session.accessToken, projectId),
      getProjectHistory({ accessToken: session.accessToken, projectId }),
    ]);
  } catch {
    redirect(`/intake?project=${projectId}`);
  }
  return (
    <ProjectOverview
      displayName={session.displayName ?? "Member"}
      initial={snapshot}
      initialHistory={history}
      initialView="inference"
      logoutAction={logout}
    />
  );
}
