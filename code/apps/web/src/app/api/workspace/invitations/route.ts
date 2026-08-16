import {
  listInvitations,
  revokeInvitation,
  sendInvitation,
} from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

function unavailable(error: unknown) {
  return Response.json(
    { message: error instanceof Error ? error.message : "Workspace invitations are unavailable." },
    { status: 400 },
  );
}

export async function GET() {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }

  try {
    return Response.json(await listInvitations({
      accessToken: session.accessToken,
      workspaceId: session.workspaceId,
    }));
  } catch (error) {
    return unavailable(error);
  }
}

export async function POST(request: Request) {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) {
    return Response.json({ message: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json().catch(() => ({}));
  try {
    if (body.action === "invite") {
      const invitation = await sendInvitation({
        accessToken: session.accessToken,
        workspaceId: session.workspaceId,
        email: String(body.email ?? "").trim().toLowerCase(),
      });
      return Response.json(invitation, { status: 201 });
    }
    if (body.action === "revoke") {
      await revokeInvitation({
        accessToken: session.accessToken,
        workspaceId: session.workspaceId,
        invitationId: String(body.invitationId ?? ""),
      });
      return new Response(null, { status: 204 });
    }
    return Response.json({ message: "Unsupported invitation action." }, { status: 400 });
  } catch (error) {
    return unavailable(error);
  }
}
