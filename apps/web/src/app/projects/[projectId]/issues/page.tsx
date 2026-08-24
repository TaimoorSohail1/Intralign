import { redirect } from "next/navigation";

import { logout } from "@/app/logout-action";
import { ProjectOverview } from "@/components/overview/project-overview";
import { parseIssueFilters } from "@/lib/issue-filters";
import { getOverview } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export default async function IssuesPage({
  params,
  searchParams,
}: {
  params: Promise<{ projectId: string }>;
  searchParams: Promise<Record<string, string | string[] | undefined>>;
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
  return (
    <ProjectOverview
      displayName={session.displayName ?? "Member"}
      initial={snapshot}
      initialIssueFilters={parseIssueFilters(await searchParams)}
      initialView="issues"
      logoutAction={logout}
    />
  );
}
