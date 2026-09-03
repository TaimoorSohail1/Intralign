import {
  createProjectReportSchedule,
  getProjectReportSchedules,
  OsloApiError,
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

export async function GET(
  _request: Request,
  context: { params: Promise<{ projectId: string }> },
) {
  const session = await readSession();
  if (!session.accessToken) return Response.json({ message: "Unauthorized" }, { status: 401 });
  const { projectId } = await context.params;
  try {
    return Response.json(
      await getProjectReportSchedules({ accessToken: session.accessToken, projectId }),
    );
  } catch (error) {
    return scheduleError(error);
  }
}

export async function POST(
  request: Request,
  context: { params: Promise<{ projectId: string }> },
) {
  const session = await readSession();
  if (!session.accessToken) return Response.json({ message: "Unauthorized" }, { status: 401 });
  const { projectId } = await context.params;
  const body = await request.json();
  try {
    const schedule = await createProjectReportSchedule({
      accessToken: session.accessToken,
      projectId,
      recipientEmail: body.recipient_email,
      recipientClass: body.recipient_class,
      weekday: body.weekday,
      localTime: body.local_time,
      timezone: body.timezone,
    });
    return Response.json(schedule, { status: 201 });
  } catch (error) {
    return scheduleError(error);
  }
}
