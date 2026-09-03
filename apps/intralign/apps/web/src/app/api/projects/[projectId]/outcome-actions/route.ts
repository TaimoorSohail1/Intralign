import { actOnPrimaryOutcome } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function POST(
  request: Request,
  context: RouteContext<"/api/projects/[projectId]/outcome-actions">,
) {
  const session = await readSession();
  if (!session.accessToken) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const { projectId } = await context.params;
  const body = await request.json();
  try {
    const result = await actOnPrimaryOutcome({
      accessToken: session.accessToken,
      projectId,
      action: body.action,
      outcome: body.outcome,
      idempotencyKey: String(body.idempotencyKey ?? crypto.randomUUID()),
    });
    return Response.json(result);
  } catch (error) {
    return Response.json(
      { message: error instanceof Error ? error.message : "Outcome action failed" },
      { status: 400 },
    );
  }
}
