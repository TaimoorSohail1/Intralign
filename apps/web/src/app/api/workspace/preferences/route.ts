import {
  getWorkspacePreferences,
  updateWorkspacePreferences,
  type WorkspacePreferences,
} from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function GET() {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  return Response.json(
    await getWorkspacePreferences({
      accessToken: session.accessToken,
      workspaceId: session.workspaceId,
    }),
  );
}

export async function PUT(request: Request) {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const preferences = (await request.json()) as WorkspacePreferences;
  return Response.json(
    await updateWorkspacePreferences({
      accessToken: session.accessToken,
      workspaceId: session.workspaceId,
      preferences,
    }),
  );
}
