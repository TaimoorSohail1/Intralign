import { redirect } from "next/navigation";

import { logout } from "@/app/logout-action";
import { ProjectOverview } from "@/components/overview/project-overview";
import {
  getOverview,
  getProjectIssueProposals,
  listProjectOutcomes,
} from "@/lib/server/oslo-api";
import type { IssueProposalSummary, ProjectOutcomeSummary } from "@/lib/server/oslo-api";
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
  let outcomes: ProjectOutcomeSummary[] = [];
  try {
    [snapshot, proposals, outcomes] = await Promise.all([
      getOverview(session.accessToken, projectId),
      getProjectIssueProposals({ accessToken: session.accessToken, projectId }),
      session.workspaceId
        ? listProjectOutcomes({
            accessToken: session.accessToken,
            workspaceId: session.workspaceId,
            projectId,
          })
        : Promise.resolve([]),
    ]);
  } catch {
    redirect(`/intake?project=${projectId}`);
  }
  const activeOutcome =
    outcomes.find((outcome) => outcome.status === "active" && outcome.is_primary) ??
    outcomes.find((outcome) => outcome.status === "active") ??
    null;
  return <ProjectOverview initial={snapshot} initialOutcome={activeOutcome} initialProposals={proposals} displayName={session.displayName ?? "Member"} logoutAction={logout} />;
}
