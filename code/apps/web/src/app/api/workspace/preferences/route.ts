import {
  getWorkspacePreferences,
  OsloApiError,
  updateWorkspacePreferences,
  type WorkspacePreferences,
} from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function GET() {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  try {
    return Response.json(
      await getWorkspacePreferences({
        accessToken: session.accessToken,
        workspaceId: session.workspaceId,
      }),
    );
  } catch (error) {
    if (error instanceof OsloApiError) {
      return Response.json(
        { message: error.status >= 500 ? "Settings are temporarily unavailable." : error.message },
        { status: error.status },
      );
    }
    return Response.json(
      { message: "Settings are temporarily unavailable." },
      { status: 502 },
    );
  }
}

export async function PUT(request: Request) {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const preferences = (await request.json()) as WorkspacePreferences;
  try {
    return Response.json(
      await updateWorkspacePreferences({
        accessToken: session.accessToken,
        workspaceId: session.workspaceId,
        preferences,
      }),
    );
  } catch (error) {
    return Response.json(
      { message: error instanceof Error ? error.message : "Settings could not be saved." },
      { status: 400 },
    );
  }
}
