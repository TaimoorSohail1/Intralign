import {
  deliverProjectReport,
  getProjectReport,
  OsloApiError,
  saveProjectReport,
} from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

function reportError(error: unknown, fallback: string) {
  if (error instanceof OsloApiError) {
    return Response.json(
      { message: error.message, detail: error.detail },
      { status: error.status },
    );
  }
  return Response.json({ message: fallback }, { status: 502 });
}

export async function GET(
  _request: Request,
  context: { params: Promise<{ projectId: string }> },
) {
  const session = await readSession();
  if (!session.accessToken) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const { projectId } = await context.params;
  try {
    return Response.json(await getProjectReport(session.accessToken, projectId));
  } catch (error) {
    return reportError(error, "Report is unavailable.");
  }
}

export async function PUT(
  request: Request,
  context: { params: Promise<{ projectId: string }> },
) {
  const session = await readSession();
  if (!session.accessToken) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const { projectId } = await context.params;
  const body = await request.json();
  try {
    return Response.json(
      await saveProjectReport({
        accessToken: session.accessToken,
        projectId,
        snapshotId: body.snapshot_id,
        content: body.content,
      }),
    );
  } catch (error) {
    return reportError(error, "Report could not be saved.");
  }
}

export async function POST(
  request: Request,
  context: { params: Promise<{ projectId: string }> },
) {
  const session = await readSession();
  if (!session.accessToken) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const { projectId } = await context.params;
  const body = await request.json();
  try {
    const result = await deliverProjectReport({
      accessToken: session.accessToken,
      projectId,
      snapshotId: body.snapshot_id,
      recipientEmail: body.recipient_email,
      recipientLabel: body.recipient_label,
      subject: body.subject,
      content: body.content,
      scheduledFor: body.scheduled_for,
      confirmPreviousAnalysis: body.confirm_previous_analysis === true,
    });
    return Response.json(result, { status: 201 });
  } catch (error) {
    return reportError(error, "Report delivery failed.");
  }
}

export async function OPTIONS() {
  return new Response(null, { status: 204 });
}
