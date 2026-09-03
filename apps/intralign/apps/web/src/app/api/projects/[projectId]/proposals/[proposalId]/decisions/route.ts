import { decideProjectIssueProposal, OsloApiError } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

const surfaces = new Set(["issue_card", "artifact", "folded_read"]);

export async function POST(
  request: Request,
  context: { params: Promise<{ projectId: string; proposalId: string }> },
) {
  const session = await readSession();
  if (!session.accessToken) return Response.json({ message: "Unauthorized" }, { status: 401 });
  const { projectId, proposalId } = await context.params;
  const payload = await request.json().catch(() => null);
  if (
    !payload ||
    typeof payload.accepted !== "boolean" ||
    typeof payload.surface !== "string" ||
    !surfaces.has(payload.surface) ||
    typeof payload.idempotencyKey !== "string" ||
    payload.idempotencyKey.length < 8
  ) {
    return Response.json({ message: "A valid proposal decision is required" }, { status: 422 });
  }
  try {
    return Response.json(await decideProjectIssueProposal({
      accessToken: session.accessToken,
      projectId,
      proposalId,
      accepted: payload.accepted,
      surface: payload.surface as "issue_card" | "artifact" | "folded_read",
      idempotencyKey: payload.idempotencyKey,
    }), { status: 202 });
  } catch (error) {
    if (error instanceof OsloApiError) {
      return Response.json({ message: error.message, detail: error.detail }, { status: error.status });
    }
    return Response.json({ message: "The proposal decision could not be saved" }, { status: 502 });
  }
}
