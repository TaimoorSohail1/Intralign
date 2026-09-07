import { getAnalysisRun } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function GET(_request: Request, context: RouteContext<"/api/analysis-runs/[runId]">) {
  const session = await readSession();
  if (!session.accessToken) return Response.json({ message: "Unauthorized" }, { status: 401 });
  const { runId } = await context.params;
  try {
    return Response.json(await getAnalysisRun(session.accessToken, runId));
  } catch {
    return Response.json({ message: "Analysis not found" }, { status: 404 });
  }
}
