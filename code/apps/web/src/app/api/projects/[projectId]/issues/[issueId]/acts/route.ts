import { actOnProjectIssueLifecycle, OsloApiError } from "@/lib/server/oslo-api";
import type { IssueBasis, IssueLifecycleAct } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

const acts = new Set(["confirm", "flag", "fix", "ground", "route", "withdraw"]);
const bases = new Set([
  "documented",
  "vendor-or-owner-verified",
  "verified-directly",
  "answered",
]);

export async function POST(
  request: Request,
  context: { params: Promise<{ projectId: string; issueId: string }> },
) {
  const session = await readSession();
  if (!session.accessToken) return Response.json({ message: "Unauthorized" }, { status: 401 });
  const { projectId, issueId } = await context.params;
  const payload = await request.json().catch(() => null);
  if (
    !payload ||
    typeof payload.act !== "string" ||
    !acts.has(payload.act) ||
    (payload.basis != null && (typeof payload.basis !== "string" || !bases.has(payload.basis))) ||
    typeof payload.idempotencyKey !== "string" ||
    payload.idempotencyKey.length < 8
  ) {
    return Response.json({ message: "A valid issue lifecycle act is required" }, { status: 422 });
  }
  try {
    return Response.json(
      await actOnProjectIssueLifecycle({
        accessToken: session.accessToken,
        projectId,
        issueId,
        act: payload.act as IssueLifecycleAct,
        basis: (payload.basis as IssueBasis | null) ?? null,
        evidenceRef: payload.evidenceRef ?? null,
        resolution: payload.resolution ?? null,
        reviewer: payload.reviewer ?? null,
        idempotencyKey: payload.idempotencyKey,
      }),
      { status: 202 },
    );
  } catch (error) {
    if (error instanceof OsloApiError) {
      return Response.json({ message: error.message, detail: error.detail }, { status: error.status });
    }
    return Response.json({ message: "The lifecycle act could not be saved" }, { status: 502 });
  }
}
