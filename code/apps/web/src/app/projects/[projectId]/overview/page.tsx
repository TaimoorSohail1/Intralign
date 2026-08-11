import { redirect } from "next/navigation";

import { logout } from "@/app/logout-action";
import { ProjectOverview } from "@/components/overview/project-overview";
import { getOverview } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export default async function OverviewPage({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const session = await readSession();
  if (!session.accessToken) redirect("/login");
  const { projectId } = await params;
  let snapshot;
  try {
    snapshot = await getOverview(session.accessToken, projectId);
  } catch {
    redirect(`/intake?project=${projectId}`);
  }
  return <ProjectOverview initial={snapshot} displayName={session.displayName ?? "Member"} logoutAction={logout} />;
}
