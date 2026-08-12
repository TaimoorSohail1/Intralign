import { redirect } from "next/navigation";

import { logout } from "@/app/logout-action";
import { ProjectOverview } from "@/components/overview/project-overview";
import { getOverview, getProjectIssueProposals } from "@/lib/server/oslo-api";
import type { IssueProposalSummary } from "@/lib/server/oslo-api";
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
  let proposals: IssueProposalSummary[] = [];
  try {
    [snapshot, proposals] = await Promise.all([
      getOverview(session.accessToken, projectId),
      getProjectIssueProposals({ accessToken: session.accessToken, projectId }),
    ]);
  } catch {
    redirect(`/intake?project=${projectId}`);
  }
  return <ProjectOverview initial={snapshot} initialProposals={proposals} displayName={session.displayName ?? "Member"} logoutAction={logout} />;
}
