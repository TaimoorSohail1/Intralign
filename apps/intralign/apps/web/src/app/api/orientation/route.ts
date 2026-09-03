import { apiRequest } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function POST() {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  try {
    await apiRequest(`/v1/workspaces/${session.workspaceId}/orientation-seen`, {
      method: "POST",
      headers: { authorization: `Bearer ${session.accessToken}` },
    });
    return new Response(null, { status: 204 });
  } catch {
    return Response.json({ message: "Could not save orientation" }, { status: 400 });
  }
}
