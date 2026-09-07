import { createBasicCheckout, OsloApiError } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

const wallKeys = new Set(["multiOutcome", "multiPlan", "envelope", "schedule"]);

export async function POST(request: Request) {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  const body = await request.json().catch(() => null);
  if (
    (body?.interval !== "monthly" && body?.interval !== "annual") ||
    !wallKeys.has(body?.wall_key)
  ) {
    return Response.json({ message: "Choose a supported billing option." }, { status: 422 });
  }
  try {
    return Response.json(
      await createBasicCheckout({
        accessToken: session.accessToken,
        workspaceId: session.workspaceId,
        interval: body.interval,
        wallKey: body.wall_key,
      }),
      { status: 201 },
    );
  } catch (error) {
    if (error instanceof OsloApiError) {
      const message =
        error.status === 403
          ? "Only the workspace owner can manage billing."
          : error.status === 503
            ? "Billing is not configured in this environment."
            : "Secure checkout could not be started.";
      return Response.json({ message }, { status: error.status });
    }
    return Response.json({ message: "Secure checkout could not be started." }, { status: 502 });
  }
}
