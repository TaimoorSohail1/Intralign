import { OsloApiError, setOutcomeArchived } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

type RouteContext = { params: Promise<{ outcomeId: string; action: string }> };

export async function POST(_request: Request, context: RouteContext) {
  const session = await readSession();
  const { outcomeId, action } = await context.params;
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  if (action !== "archive" && action !== "reactivate") {
    return Response.json({ message: "Unsupported Outcome action." }, { status: 404 });
  }
  try {
    return Response.json(
      await setOutcomeArchived({
        accessToken: session.accessToken,
        workspaceId: session.workspaceId,
        outcomeId,
        archived: action === "archive",
      }),
    );
  } catch (error) {
    if (error instanceof OsloApiError) {
      return Response.json(
        {
          message: error.status === 422
            ? "Free already has an active Outcome. Archive it before reactivating this one."
            : "The Outcome could not be updated.",
          detail: error.detail,
        },
        { status: error.status },
      );
    }
    return Response.json({ message: "The Outcome could not be updated." }, { status: 502 });
  }
}
