import { getProjectIssueProposals, OsloApiError } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function GET(
  _request: Request,
  context: { params: Promise<{ projectId: string }> },
) {
  const session = await readSession();
  if (!session.accessToken) return Response.json({ message: "Unauthorized" }, { status: 401 });
  const { projectId } = await context.params;
  try {
    return Response.json(await getProjectIssueProposals({
      accessToken: session.accessToken,
      projectId,
    }));
  } catch (error) {
    if (error instanceof OsloApiError) {
      return Response.json({ message: error.message, detail: error.detail }, { status: error.status });
    }
    return Response.json({ message: "Proposals are unavailable" }, { status: 502 });
  }
}
