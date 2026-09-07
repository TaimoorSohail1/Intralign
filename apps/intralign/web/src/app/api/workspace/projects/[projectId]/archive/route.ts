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
      archived: true,
    });
    return new Response(null, { status: 204 });
  } catch (error) {
    if (error instanceof OsloApiError) {
      return Response.json({ message: "Project cannot be archived" }, { status: error.status });
    }
    return Response.json({ message: "Project cannot be archived" }, { status: 502 });
  }
}
