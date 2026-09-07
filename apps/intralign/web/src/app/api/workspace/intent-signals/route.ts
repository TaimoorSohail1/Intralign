import { OsloApiError, recordCapacityIntent } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

const wallKeys = new Set(["multiOutcome", "multiPlan", "envelope", "schedule"]);
const choices = new Set(["committed", "free_path", "declined", "keep_both"]);

export async function POST(request: Request) {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const body = await request.json().catch(() => null);
  if (
    !wallKeys.has(body?.wall_key) ||
    !choices.has(body?.chosen_path) ||
    !Array.isArray(body?.full_option_set) ||
    typeof body?.context !== "object" ||
    body.context === null
  ) {
    return Response.json({ message: "Invalid capacity choice." }, { status: 422 });
  }
  try {
    await recordCapacityIntent({
      accessToken: session.accessToken,
      workspaceId: session.workspaceId,
      wallKey: body.wall_key,
      chosenPath: body.chosen_path,
      fullOptionSet: body.full_option_set,
      context: body.context,
    });
    return new Response(null, { status: 204 });
  } catch (error) {
    const status = error instanceof OsloApiError ? error.status : 502;
    return Response.json({ message: "The capacity choice could not be recorded." }, { status });
  }
}
