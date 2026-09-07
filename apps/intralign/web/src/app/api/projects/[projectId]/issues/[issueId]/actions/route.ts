import { actOnProjectIssue, OsloApiError } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

const actions = new Set(["select", "apply", "custom"]);

export async function POST(
  request: Request,
  context: { params: Promise<{ projectId: string; issueId: string }> },
) {
  const session = await readSession();
  if (!session.accessToken) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const { projectId, issueId } = await context.params;
  const payload = await request.json().catch(() => null);
  if (
    !payload ||
    typeof payload.action !== "string" ||
    !actions.has(payload.action) ||
    typeof payload.resolution !== "string" ||
    !payload.resolution.trim() ||
    typeof payload.idempotencyKey !== "string" ||
    payload.idempotencyKey.length < 8
  ) {
    return Response.json({ message: "A valid issue action is required" }, { status: 422 });
  }
  try {
    const result = await actOnProjectIssue({
      accessToken: session.accessToken,
      projectId,
      issueId,
      action: payload.action,
      resolution: payload.resolution.trim(),
      idempotencyKey: payload.idempotencyKey,
    });
    return Response.json(result, { status: 202 });
  } catch (error) {
    if (error instanceof OsloApiError) {
      return Response.json(
        { message: error.message, detail: error.detail },
        { status: error.status },
      );
    }
    return Response.json(
      { message: "The issue action could not be saved" },
      { status: 502 },
    );
  }
}
