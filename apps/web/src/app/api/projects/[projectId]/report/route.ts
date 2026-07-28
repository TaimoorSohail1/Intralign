import {
  deliverProjectReport,
  getProjectReport,
  saveProjectReport,
} from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

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
    return Response.json(
      { message: error instanceof Error ? error.message : "Report is unavailable." },
      { status: 400 },
    );
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
    return Response.json(
      { message: error instanceof Error ? error.message : "Report could not be saved." },
      { status: 400 },
    );
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
    });
    return Response.json(result, { status: 201 });
  } catch (error) {
    return Response.json(
      { message: error instanceof Error ? error.message : "Report delivery failed." },
      { status: 400 },
    );
  }
}

export async function OPTIONS() {
  return new Response(null, { status: 204 });
}
