import {
  fileFeedbackTicket,
  listFeedbackTickets,
  OsloApiError,
  type FeedbackTicketInput,
} from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";


export async function GET(request: Request) {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const sessionId = new URL(request.url).searchParams.get("session_id") ?? "";
  if (!/^[A-Za-z0-9_-]{8,128}$/.test(sessionId)) {
    return Response.json({ message: "Feedback session is invalid." }, { status: 422 });
  }
  try {
    return Response.json(
      await listFeedbackTickets({
        accessToken: session.accessToken,
        workspaceId: session.workspaceId,
        sessionId,
      }),
    );
  } catch (error) {
    const status = error instanceof OsloApiError ? error.status : 502;
    return Response.json({ message: "Filed feedback could not be loaded." }, { status });
  }
}


export async function POST(request: Request) {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const body = (await request.json().catch(() => null)) as FeedbackTicketInput | null;
  if (!body?.body?.trim()) {
    return Response.json({ message: "Tell us what happened first." }, { status: 422 });
  }
  try {
    return Response.json(
      await fileFeedbackTicket({
        accessToken: session.accessToken,
        workspaceId: session.workspaceId,
        ticket: body,
      }),
      { status: 201 },
    );
  } catch (error) {
    const status = error instanceof OsloApiError ? error.status : 502;
    return Response.json(
      { message: "Feedback could not be filed. Your text is still here; try again." },
      { status },
    );
  }
}
