import { getWorkspace, OsloApiError } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function GET() {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  try {
    return Response.json(
      await getWorkspace({
        accessToken: session.accessToken,
        workspaceId: session.workspaceId,
      }),
    );
  } catch (error) {
    if (error instanceof OsloApiError) {
      return Response.json({ message: "Workspace unavailable" }, { status: error.status });
    }
    return Response.json({ message: "Workspace unavailable" }, { status: 502 });
  }
}
