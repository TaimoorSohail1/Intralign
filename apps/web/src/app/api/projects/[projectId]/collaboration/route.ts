import {
  createReviewGrant,
  createShareLink,
  getCollaboration,
  listInvitations,
  promoteReviewResponse,
  revokeInvitation,
  revokeReviewGrant,
  revokeShareLink,
  sendInvitation,
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
    const collaboration = await getCollaboration(session.accessToken, projectId);
    if (collaboration.actor_role !== "owner" || !session.workspaceId) {
      return Response.json(collaboration);
    }

    const invitations = await listInvitations({
      accessToken: session.accessToken,
      workspaceId: session.workspaceId,
    });
    return Response.json({
      ...collaboration,
      invitations,
    });
  } catch (error) {
    return Response.json(
      { message: error instanceof Error ? error.message : "Collaboration is unavailable." },
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
  const body = await request.json().catch(() => ({}));

  try {
    if (body.action === "share") {
      const result = await createShareLink(session.accessToken, projectId);
      return Response.json(result, { status: 201 });
    }
    if (body.action === "review") {
      const result = await createReviewGrant({
        accessToken: session.accessToken,
        projectId,
        issueId: body.issueId ?? null,
        reviewerName: body.reviewerName,
        reviewerEmail: body.reviewerEmail ?? null,
      });
      return Response.json(result, { status: 201 });
    }
    if (body.action === "invite") {
      if (!session.workspaceId) {
        return Response.json({ message: "Workspace session is missing." }, { status: 400 });
      }
      const result = await sendInvitation({
        accessToken: session.accessToken,
        workspaceId: session.workspaceId,
        email: body.email,
        role: body.role,
      });
      return Response.json(result, { status: 201 });
    }
    if (body.action === "revoke_share") {
      await revokeShareLink({
        accessToken: session.accessToken,
        projectId,
        linkId: body.linkId,
      });
      return new Response(null, { status: 204 });
    }
    if (body.action === "revoke_review") {
      await revokeReviewGrant({
        accessToken: session.accessToken,
        projectId,
        grantId: body.grantId,
      });
      return new Response(null, { status: 204 });
    }
    if (body.action === "use_review_evidence") {
      const result = await promoteReviewResponse({
        accessToken: session.accessToken,
        projectId,
        responseId: body.responseId,
      });
      return Response.json(result, { status: 202 });
    }
    if (body.action === "revoke_invitation") {
      if (!session.workspaceId) {
        return Response.json({ message: "Workspace session is missing." }, { status: 400 });
      }
      await revokeInvitation({
        accessToken: session.accessToken,
        workspaceId: session.workspaceId,
        invitationId: body.invitationId,
      });
      return new Response(null, { status: 204 });
    }

    return Response.json({ message: "Unsupported collaboration action." }, { status: 400 });
  } catch (error) {
    return Response.json(
      { message: error instanceof Error ? error.message : "Collaboration action failed." },
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
  const body = await request.json().catch(() => ({}));
  const { addProjectComment } = await import("@/lib/server/oslo-api");

  try {
    const result = await addProjectComment({
      accessToken: session.accessToken,
      projectId,
      issueId: body.issueId,
      body: body.body,
      mentions: body.mentions ?? [],
    });
    return Response.json(result, { status: 201 });
  } catch (error) {
    return Response.json(
      { message: error instanceof Error ? error.message : "Comment could not be added." },
      { status: 400 },
    );
  }
}
