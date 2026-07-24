import { answerProjectIssue } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

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
    typeof payload.answer !== "string" ||
    !payload.answer.trim() ||
    typeof payload.idempotencyKey !== "string" ||
    payload.idempotencyKey.length < 8
  ) {
    return Response.json({ message: "A valid answer is required" }, { status: 422 });
  }
  try {
    const run = await answerProjectIssue({
      accessToken: session.accessToken,
      projectId,
      issueId,
      answer: payload.answer.trim(),
      idempotencyKey: payload.idempotencyKey,
    });
    return Response.json(run, { status: 202 });
  } catch {
    return Response.json({ message: "The answer could not be saved" }, { status: 400 });
  }
}
