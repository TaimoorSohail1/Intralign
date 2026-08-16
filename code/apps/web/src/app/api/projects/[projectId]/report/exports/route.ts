import { OsloApiError, recordProjectReportExport } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function POST(
  request: Request,
  context: { params: Promise<{ projectId: string }> },
) {
  const session = await readSession();
  if (!session.accessToken) return Response.json({ message: "Unauthorized" }, { status: 401 });
  const { projectId } = await context.params;
  const body = await request.json();
  try {
    return Response.json(
      await recordProjectReportExport({
        accessToken: session.accessToken,
        projectId,
        format: body.format,
        contentChecksum: body.content_checksum,
      }),
      { status: 201 },
    );
  } catch (error) {
    if (error instanceof OsloApiError) {
      return Response.json(
        { message: error.message, detail: error.detail },
        { status: error.status },
      );
    }
    return Response.json({ message: "Export record failed." }, { status: 502 });
  }
}
