import {
  getProjectArtifact,
  OsloApiError,
  updateProjectArtifact,
} from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

function persistedArtifactType(artifactType: string) {
  return artifactType === "constraints" ? "context" : artifactType;
}

function presentArtifact(
  artifact: Awaited<ReturnType<typeof getProjectArtifact>>,
  artifactType: string,
) {
  if (artifactType !== "constraints") return artifact;
  return {
    ...artifact,
    artifact_type: "constraints",
    title: "Constraints",
    issues: artifact.issues.map((issue) => ({
      ...issue,
      artifact_type:
        issue.artifact_type === "context" ? "constraints" : issue.artifact_type,
    })),
  };
}

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
    const artifact = await getProjectArtifact(
      session.accessToken,
      projectId,
      persistedArtifactType(artifactType),
    );
    return Response.json(presentArtifact(artifact, artifactType));
  } catch (error) {
    if (error instanceof OsloApiError) {
      return Response.json({ message: error.message }, { status: error.status });
    }
    return Response.json({ message: "Artifact service unavailable" }, { status: 502 });
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
      artifactType: persistedArtifactType(artifactType),
      content: payload.content,
      expectedVersion: payload.expectedVersion,
      idempotencyKey: payload.idempotencyKey,
    });
    return Response.json(presentArtifact(artifact, artifactType), { status: 202 });
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
