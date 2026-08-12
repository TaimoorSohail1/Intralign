import { redirect } from "next/navigation";

import { AnalysisProgress } from "@/components/analysis/analysis-progress";
import { getOrientationSeen } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export default async function AnalysisPage({
  params,
}: {
  params: Promise<{ projectId: string; runId: string }>;
}) {
  const session = await readSession();
  if (!session.accessToken) redirect("/login");
  const { projectId, runId } = await params;
  const orientationSeen = await getOrientationSeen(session.accessToken, projectId).catch(() => false);
  return (
    <AnalysisProgress
      mode={orientationSeen ? "watch" : "guided"}
      projectId={projectId}
      runId={runId}
    />
  );
}
