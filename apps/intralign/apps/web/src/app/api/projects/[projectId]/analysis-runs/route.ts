import { startAnalysis } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function POST(request: Request, context: RouteContext<"/api/projects/[projectId]/analysis-runs">) {
  const session = await readSession();
  if (!session.accessToken) return Response.json({ message: "Unauthorized" }, { status: 401 });
  const { projectId } = await context.params;
  const body = await request.json();
  const kind = body.kind === "extended" ? "extended" : "initial";
  try {
    const run = await startAnalysis({
      accessToken: session.accessToken,
      projectId,
      kind,
      provisional: kind === "initial",
      description: String(body.description ?? ""),
      sourceNames: Array.isArray(body.sourceNames) ? body.sourceNames.slice(0, 10) : [],
      sourceDocumentIds: Array.isArray(body.sourceDocumentIds)
        ? body.sourceDocumentIds.slice(0, 10)
        : [],
      idempotencyKey: String(body.idempotencyKey ?? crypto.randomUUID()),
    });
    return Response.json(run, { status: 202 });
  } catch (error) {
    return Response.json(
      { message: error instanceof Error ? error.message : "Analysis could not start" },
      { status: 400 },
    );
  }
}
