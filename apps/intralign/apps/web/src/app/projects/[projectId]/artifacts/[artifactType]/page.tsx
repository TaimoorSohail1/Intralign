import { notFound, redirect } from "next/navigation";

import { logout } from "@/app/logout-action";
import { ProjectOverview } from "@/components/overview/project-overview";
import { getOverview, getProjectIssueProposals } from "@/lib/server/oslo-api";
import type { IssueProposalSummary } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

const artifactTypes = new Set([
  "intent",
  "scope",
  "requirements",
  "constraints",
  "work_breakdown",
  "schedule",
  "resources",
]);

export default async function ArtifactPage({
  params,
  searchParams,
}: {
  params: Promise<{ projectId: string; artifactType: string }>;
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const session = await readSession();
  if (!session.accessToken) redirect("/login");
  const { projectId, artifactType } = await params;
  const query = await searchParams;
  const focus =
    query.new === "outcome"
      ? "new-outcome"
      : query.review === "held-outcomes"
        ? "held-outcomes"
        : typeof query.focus === "string" &&
            ["primary-outcome", "held-outcomes", "new-outcome"].includes(query.focus)
          ? (query.focus as "primary-outcome" | "held-outcomes" | "new-outcome")
          : undefined;
  if (artifactType === "context") {
    redirect(`/projects/${projectId}/artifacts/constraints`);
  }
  if (!artifactTypes.has(artifactType)) notFound();
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
  return (
    <ProjectOverview
      displayName={session.displayName ?? "Member"}
      initial={snapshot}
      initialProposals={proposals}
      initialArtifactFocus={artifactType === "intent" ? focus : undefined}
      returnToOutcome={artifactType === "intent" && query.return === "outcome"}
      initialView={artifactType as "intent"}
      logoutAction={logout}
    />
  );
}
