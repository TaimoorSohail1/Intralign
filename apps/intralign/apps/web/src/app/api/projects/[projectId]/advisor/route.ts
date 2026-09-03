import { askAdvisor } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function POST(
  request: Request,
  context: RouteContext<"/api/projects/[projectId]/advisor">,
) {
  const session = await readSession();
  if (!session.accessToken) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const { projectId } = await context.params;
  const payload = await request.json().catch(() => null);
  if (!payload || typeof payload.question !== "string" || !payload.question.trim()) {
    return Response.json({ message: "A question is required" }, { status: 422 });
  }
  try {
    return Response.json(
      await askAdvisor({
        accessToken: session.accessToken,
        projectId,
        question: payload.question.trim(),
        historyRunId:
          typeof payload.historyRunId === "string" ? payload.historyRunId : null,
      }),
    );
  } catch {
    return Response.json(
      { message: "Project Advisor is temporarily unavailable" },
      { status: 503 },
    );
  }
}
