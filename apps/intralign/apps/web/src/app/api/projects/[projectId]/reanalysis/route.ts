import { runProjectReanalysis } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function POST(
  request: Request,
  context: RouteContext<"/api/projects/[projectId]/reanalysis">,
) {
  const session = await readSession();
  if (!session.accessToken) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const { projectId } = await context.params;
  const body = await request.json().catch(() => ({}));
  try {
    const run = await runProjectReanalysis({
      accessToken: session.accessToken,
      projectId,
      deep: body.deep === true,
      idempotencyKey: String(body.idempotencyKey ?? crypto.randomUUID()),
    });
    return Response.json(run, { status: 202 });
  } catch (error) {
    return Response.json(
      { message: error instanceof Error ? error.message : "Reanalysis could not start" },
      { status: 400 },
    );
  }
}
