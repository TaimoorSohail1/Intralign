import { retryAnalysis } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function POST(_request: Request, context: RouteContext<"/api/analysis-runs/[runId]/retry">) {
  const session = await readSession();
  if (!session.accessToken) return Response.json({ message: "Unauthorized" }, { status: 401 });
  const { runId } = await context.params;
  try {
    return Response.json(await retryAnalysis(session.accessToken, runId), { status: 202 });
  } catch {
    return Response.json({ message: "Retry failed" }, { status: 400 });
  }
}
