import {
  deleteProjectReportSchedule,
  OsloApiError,
  updateProjectReportSchedule,
} from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

function scheduleError(error: unknown) {
  if (error instanceof OsloApiError) {
    return Response.json(
      { message: error.message, detail: error.detail },
      { status: error.status },
    );
  }
  return Response.json({ message: "Report schedule is unavailable." }, { status: 502 });
}

export async function PATCH(
  request: Request,
  context: { params: Promise<{ projectId: string; scheduleId: string }> },
) {
  const session = await readSession();
  if (!session.accessToken) return Response.json({ message: "Unauthorized" }, { status: 401 });
  const { projectId, scheduleId } = await context.params;
  const body = await request.json();
  try {
    return Response.json(
      await updateProjectReportSchedule({
        accessToken: session.accessToken,
        projectId,
        scheduleId,
        state: body.state,
      }),
    );
  } catch (error) {
    return scheduleError(error);
  }
}

export async function DELETE(
  _request: Request,
  context: { params: Promise<{ projectId: string; scheduleId: string }> },
) {
  const session = await readSession();
  if (!session.accessToken) return Response.json({ message: "Unauthorized" }, { status: 401 });
  const { projectId, scheduleId } = await context.params;
  try {
    await deleteProjectReportSchedule({ accessToken: session.accessToken, projectId, scheduleId });
    return new Response(null, { status: 204 });
  } catch (error) {
    return scheduleError(error);
  }
}
