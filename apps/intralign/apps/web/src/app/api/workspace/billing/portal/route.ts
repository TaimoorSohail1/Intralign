import { createBillingPortal, OsloApiError } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function POST() {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }
  try {
    return Response.json(
      await createBillingPortal({
        accessToken: session.accessToken,
        workspaceId: session.workspaceId,
      }),
      { status: 201 },
    );
  } catch (error) {
    if (error instanceof OsloApiError) {
      const message =
        error.status === 403
          ? "Only the workspace owner can manage billing."
          : error.status === 409
            ? "No billing account is available for this workspace."
            : "Billing could not be opened.";
      return Response.json({ message }, { status: error.status });
    }
    return Response.json({ message: "Billing could not be opened." }, { status: 502 });
  }
}
