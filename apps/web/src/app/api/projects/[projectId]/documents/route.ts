import { uploadDocument } from "@/lib/server/oslo-api";
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
    return Response.json(
      { message: error instanceof Error ? error.message : "Document could not be processed" },
      { status: 422 },
    );
  }
}
