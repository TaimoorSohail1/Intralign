import { getProjectHistory } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function GET(
  request: Request,
  context: RouteContext<"/api/projects/[projectId]/history">,
) {
  const session = await readSession();
  if (!session.accessToken) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const { projectId } = await context.params;
  const url = new URL(request.url);
  const category = url.searchParams.get("category") ?? "all";
  const allowed = [
    "all",
    "analysis",
    "issues",
    "versions",
    "decisions",
    "collaboration",
  ] as const;
  if (!allowed.includes(category as (typeof allowed)[number])) {
    return Response.json({ message: "Invalid history category" }, { status: 422 });
  }
  try {
    return Response.json(
      await getProjectHistory({
        accessToken: session.accessToken,
        projectId,
        category: category as (typeof allowed)[number],
        cursor: url.searchParams.get("cursor"),
        limit: 40,
      }),
    );
  } catch {
    return Response.json(
      { message: "Project history is temporarily unavailable" },
      { status: 503 },
    );
  }
}
