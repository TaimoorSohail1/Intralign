import { redirect } from "next/navigation";

import { AnalysisProgress } from "@/components/analysis/analysis-progress";
import { readSession } from "@/lib/server/session";

export default async function AnalysisPage({
  params,
}: {
  params: Promise<{ projectId: string; runId: string }>;
}) {
  const session = await readSession();
  if (!session.accessToken) redirect("/login");
  const { projectId, runId } = await params;
  return <AnalysisProgress projectId={projectId} runId={runId} />;
}
