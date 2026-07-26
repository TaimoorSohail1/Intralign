import { markWorkspaceNotificationsRead } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function POST(request: Request) {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const payload = (await request.json()) as { keys?: string[] };
  await markWorkspaceNotificationsRead({
    accessToken: session.accessToken,
    workspaceId: session.workspaceId,
    keys: payload.keys ?? [],
  });
  return new Response(null, { status: 204 });
}
