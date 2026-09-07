import { undoPendingAct } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function DELETE(
  _request: Request,
  context: RouteContext<"/api/projects/[projectId]/acts/[eventId]">,
) {
  const session = await readSession();
  if (!session.accessToken) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const { projectId, eventId } = await context.params;
  try {
    return Response.json(
      await undoPendingAct({
        accessToken: session.accessToken,
        projectId,
        eventId,
      }),
    );
  } catch (error) {
    return Response.json(
      { message: error instanceof Error ? error.message : "Unable to undo change" },
      { status: 409 },
    );
  }
}
