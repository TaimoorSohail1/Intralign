import { redirect } from "next/navigation";

import { logout } from "@/app/logout-action";
import { HistoryOnlyPage } from "@/components/history/history-only-page";
import { ProjectOverview } from "@/components/overview/project-overview";
import { getOverview, getProjectHistory } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export default async function HistoryPage({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const session = await readSession();
  if (!session.accessToken) redirect("/login");
  const { projectId } = await params;
  const history = await getProjectHistory({
    accessToken: session.accessToken,
    projectId,
  }).catch(() => null);
  if (!history) redirect(`/intake?project=${projectId}`);
  let snapshot;
  try {
    snapshot = await getOverview(session.accessToken, projectId);
  } catch {
    return <HistoryOnlyPage history={history} projectId={projectId} />;
  }
  return (
    <ProjectOverview
      displayName={session.displayName ?? "Member"}
      initial={snapshot}
      initialHistory={history}
      initialView="history"
      logoutAction={logout}
    />
  );
}
