import {
  getProjectArtifact,
  updateProjectArtifact,
} from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function GET(
  _request: Request,
  context: RouteContext<"/api/projects/[projectId]/artifacts/[artifactType]">,
) {
  const session = await readSession();
  if (!session.accessToken) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const { projectId, artifactType } = await context.params;
  try {
    return Response.json(
      await getProjectArtifact(session.accessToken, projectId, artifactType),
    );
  } catch {
    return Response.json({ message: "Artifact not found" }, { status: 404 });
  }
}

export async function PATCH(
  request: Request,
  context: RouteContext<"/api/projects/[projectId]/artifacts/[artifactType]">,
) {
  const session = await readSession();
  if (!session.accessToken) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const { projectId, artifactType } = await context.params;
  const payload = await request.json().catch(() => null);
  if (
    !payload ||
    typeof payload.expectedVersion !== "number" ||
    !payload.content ||
    typeof payload.idempotencyKey !== "string"
  ) {
    return Response.json({ message: "Invalid artifact update" }, { status: 422 });
  }
  try {
    const artifact = await updateProjectArtifact({
      accessToken: session.accessToken,
      projectId,
      artifactType,
      content: payload.content,
      expectedVersion: payload.expectedVersion,
      idempotencyKey: payload.idempotencyKey,
    });
    return Response.json(artifact, { status: 202 });
  } catch (error) {
    const conflict =
      error instanceof Error && error.message.includes("ARTIFACT_VERSION_CONFLICT");
    const analysisInProgress =
      error instanceof Error && error.message.includes("ARTIFACT_ANALYSIS_IN_PROGRESS");
    return Response.json(
      {
        message: conflict
          ? "This artifact changed elsewhere. Reload it."
          : analysisInProgress
            ? "OSLO is already re-analyzing this project. Apply this change when it finishes."
            : "Artifact save failed",
      },
      { status: conflict || analysisInProgress ? 409 : 400 },
    );
  }
}
