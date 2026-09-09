import { osloApiUrl } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export const dynamic = "force-dynamic";

export async function GET(request: Request, context: RouteContext<"/api/analysis-runs/[runId]/events">) {
  const session = await readSession();
  if (!session.accessToken) return Response.json({ message: "Unauthorized" }, { status: 401 });
  const { runId } = await context.params;
  const requestedCursor = new URL(request.url).searchParams.get("lastEventId");
  const lastEventIdHeader = request.headers.get("last-event-id");
  const lastEventId = lastEventIdHeader && /^\d+$/.test(lastEventIdHeader)
    ? lastEventIdHeader
    : requestedCursor && /^\d+$/.test(requestedCursor)
      ? requestedCursor
      : "0";
  const upstream = await fetch(`${osloApiUrl}/v1/analysis-runs/${runId}/events`, {
    cache: "no-store",
    headers: {
      authorization: `Bearer ${session.accessToken}`,
      "Last-Event-ID": lastEventId,
    },
  });
  if (!upstream.ok || !upstream.body) {
    return Response.json({ message: "Event stream unavailable" }, { status: upstream.status });
  }
  return new Response(upstream.body, {
    headers: {
      "content-type": "text/event-stream",
      "cache-control": "no-cache, no-transform",
      "x-accel-buffering": "no",
    },
  });
}
