import { redirect } from "next/navigation";

import { logout } from "@/app/logout-action";
import { withCurrentFullPlanArtifacts } from "@/components/execution/full-plan-projection";
import { ProjectOverview } from "@/components/overview/project-overview";
import {
  getOverview,
  getProjectArtifact,
  getProjectIssueProposals,
} from "@/lib/server/oslo-api";
import type { IssueProposalSummary } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export default async function FullPlanPage({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const session = await readSession();
  if (!session.accessToken) redirect("/login");
  const accessToken = session.accessToken;
  const { projectId } = await params;
  let snapshot;
  let proposals: IssueProposalSummary[] = [];
  try {
    const [overview, currentArtifacts, currentProposals] = await Promise.all([
      getOverview(accessToken, projectId),
      Promise.all(
        ["work_breakdown", "schedule", "resources"].map((artifactType) =>
          getProjectArtifact(accessToken, projectId, artifactType),
        ),
      ),
      getProjectIssueProposals({ accessToken, projectId }),
    ]);
    snapshot = withCurrentFullPlanArtifacts(overview, currentArtifacts);
    proposals = currentProposals;
  } catch {
    redirect(`/intake?project=${projectId}`);
  }
  return (
    <ProjectOverview
      displayName={session.displayName ?? "Member"}
      initial={snapshot}
      initialProposals={proposals}
      initialView="full_plan"
      logoutAction={logout}
    />
  );
}
