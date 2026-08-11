import { getOverview } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function GET(_request: Request, context: RouteContext<"/api/projects/[projectId]/overview">) {
  const session = await readSession();
  if (!session.accessToken) return Response.json({ message: "Unauthorized" }, { status: 401 });
  const { projectId } = await context.params;
  try {
    return Response.json(await getOverview(session.accessToken, projectId));
  } catch {
    return Response.json({ message: "Overview not found" }, { status: 404 });
  }
}
