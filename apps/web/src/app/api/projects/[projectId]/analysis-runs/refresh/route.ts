import { apiRequest } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function POST(
  _request: Request,
  context: RouteContext<"/api/projects/[projectId]/analysis-runs/refresh">,
) {
  const session = await readSession();
  if (!session.accessToken) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const { projectId } = await context.params;
  try {
    const run = await apiRequest<{ run_id: string }>(
      `/v1/projects/${projectId}/analysis-runs/refresh`,
      {
        method: "POST",
        headers: {
          authorization: `Bearer ${session.accessToken}`,
          "Idempotency-Key": `manual-refresh:${projectId}:${crypto.randomUUID()}`,
        },
      },
    );
    return Response.json(run, { status: 202 });
  } catch (error) {
    return Response.json(
      { message: error instanceof Error ? error.message : "Analysis could not refresh" },
      { status: 400 },
    );
  }
}
