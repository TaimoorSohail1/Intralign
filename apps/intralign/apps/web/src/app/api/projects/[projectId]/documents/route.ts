import { OsloApiError, uploadDocument } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function POST(
  request: Request,
  context: RouteContext<"/api/projects/[projectId]/documents">,
) {
  const session = await readSession();
  if (!session.accessToken) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const { projectId } = await context.params;
  const form = await request.formData();
  const file = form.get("file");
  if (!(file instanceof File)) {
    return Response.json({ message: "A document is required" }, { status: 400 });
  }
  try {
    const document = await uploadDocument({
      accessToken: session.accessToken,
      projectId,
      file,
    });
    return Response.json(document, { status: 201 });
  } catch (error) {
    const apiError = error instanceof OsloApiError || (
      error instanceof Error &&
      "status" in error &&
      typeof error.status === "number"
    ) ? error as OsloApiError : null;
    if (apiError) {
      return Response.json(
        {
          code: apiError.status === 404 ? "PROJECT_NOT_FOUND" : undefined,
          message: apiError.message,
        },
        { status: apiError.status },
      );
    }
    return Response.json(
      { message: error instanceof Error ? error.message : "Document could not be processed" },
      { status: 422 },
    );
  }
}
