import { OsloApiError, setProjectArchived } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function POST(
  _request: Request,
  { params }: { params: Promise<{ projectId: string }> },
) {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const { projectId } = await params;
  try {
    await setProjectArchived({
      accessToken: session.accessToken,
      workspaceId: session.workspaceId,
      projectId,
      archived: false,
    });
    return new Response(null, { status: 204 });
  } catch (error) {
    if (error instanceof OsloApiError) {
      const code = error.status === 409 ? "PROJECT_LIMIT_REACHED" : "PROJECT_RESTORE_DENIED";
      return Response.json({ code, message: "Project cannot be restored" }, { status: error.status });
    }
    return Response.json({ message: "Project cannot be restored" }, { status: 502 });
  }
}
