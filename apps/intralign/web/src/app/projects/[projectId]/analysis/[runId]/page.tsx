import { redirect } from "next/navigation";

import { AnalysisProgress } from "@/components/analysis/analysis-progress";
import { getOrientationSeen } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export default async function AnalysisPage({
  params,
  searchParams,
}: {
  params: Promise<{ projectId: string; runId: string }>;
  searchParams: Promise<{ returning?: string }>;
}) {
  const session = await readSession();
  if (!session.accessToken) redirect("/login");
  const { projectId, runId } = await params;
  const { returning } = await searchParams;
  const orientationSeen = await getOrientationSeen(session.accessToken, projectId).catch(() => false);
  return (
    <AnalysisProgress
      mode={returning === "1" || orientationSeen ? "watch" : "guided"}
      projectId={projectId}
      runId={runId}
    />
  );
}
