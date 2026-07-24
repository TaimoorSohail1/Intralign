import { startProject } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function POST() {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  try {
    return Response.json(
      await startProject({
        accessToken: session.accessToken,
        workspaceId: session.workspaceId,
      }),
      { status: 201 },
    );
  } catch {
    return Response.json({ message: "Could not create a new project" }, { status: 400 });
  }
}
