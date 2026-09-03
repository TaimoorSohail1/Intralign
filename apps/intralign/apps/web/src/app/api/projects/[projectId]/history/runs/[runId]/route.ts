import { getProjectHistorySnapshot } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function GET(
  _request: Request,
  context: RouteContext<"/api/projects/[projectId]/history/runs/[runId]">,
) {
  const session = await readSession();
  if (!session.accessToken) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const { projectId, runId } = await context.params;
  try {
    return Response.json(
      await getProjectHistorySnapshot({
        accessToken: session.accessToken,
        projectId,
        runId,
      }),
    );
  } catch {
    return Response.json(
      { message: "Historical snapshot is unavailable" },
      { status: 404 },
    );
  }
}
