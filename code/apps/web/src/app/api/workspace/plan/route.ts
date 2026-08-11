import { OsloApiError, setWorkspacePlan } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function PUT(request: Request) {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json().catch(() => null);
  if (body?.plan !== "free" && body?.plan !== "basic") {
    return Response.json({ message: "Choose a supported plan." }, { status: 422 });
  }

  try {
    return Response.json(
      await setWorkspacePlan({
        accessToken: session.accessToken,
        workspaceId: session.workspaceId,
        plan: body.plan,
      }),
    );
  } catch (error) {
    if (error instanceof OsloApiError) {
      return Response.json(
        { message: error.status === 403 ? "Only a workspace owner can change the plan." : "The plan could not be updated." },
        { status: error.status },
      );
    }
    return Response.json({ message: "The plan could not be updated." }, { status: 502 });
  }
}
