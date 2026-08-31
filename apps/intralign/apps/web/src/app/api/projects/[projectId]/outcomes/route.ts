import {
  createProjectOutcome,
  listProjectOutcomes,
  OsloApiError,
} from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

type RouteContext = { params: Promise<{ projectId: string }> };

export async function GET(_request: Request, context: RouteContext) {
  const session = await readSession();
  const { projectId } = await context.params;
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  try {
    return Response.json(
      await listProjectOutcomes({
        accessToken: session.accessToken,
        workspaceId: session.workspaceId,
        projectId,
      }),
    );
  } catch (error) {
    const status = error instanceof OsloApiError ? error.status : 502;
    return Response.json({ message: "Outcomes could not be loaded." }, { status });
  }
}

export async function POST(request: Request, context: RouteContext) {
  const session = await readSession();
  const { projectId } = await context.params;
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const body = await request.json().catch(() => null);
  if (typeof body?.title !== "string" || !body.title.trim()) {
    return Response.json({ message: "Name the Outcome." }, { status: 422 });
  }
  try {
    return Response.json(
      await createProjectOutcome({
        accessToken: session.accessToken,
        workspaceId: session.workspaceId,
        projectId,
        title: body.title.trim(),
      }),
      { status: 201 },
    );
  } catch (error) {
    if (error instanceof OsloApiError) {
      return Response.json(
        {
          message: error.status === 422
            ? "Free includes one active Outcome. Archive one or choose Basic."
            : "The Outcome could not be created.",
          detail: error.detail,
        },
        { status: error.status },
      );
    }
    return Response.json({ message: "The Outcome could not be created." }, { status: 502 });
  }
}
