import "server-only";

const apiUrl = process.env.OSLO_API_URL ?? "http://127.0.0.1:8000";

export interface InvitationDetails {
  email: string;
  workspace_name: string;
  role: "owner" | "collaborator" | "viewer";
  expires_at: string;
  account_exists: boolean;
}

export interface SessionPayload {
  user_id: string;
  email: string;
  workspace_id: string;
  access_token: string;
  refresh_token: string;
  expires_in: number;
  welcome_required: boolean;
}

export interface InvitationSummary {
  id: string;
  email: string;
  role: "owner" | "collaborator" | "viewer";
  status: "pending" | "accepted" | "revoked" | "expired";
  expires_at: string;
}

async function apiRequest<T>(path: string, init: RequestInit): Promise<T> {
  const response = await fetch(`${apiUrl}${path}`, {
    ...init,
    cache: "no-store",
    headers: { "content-type": "application/json", ...init.headers },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail?.message ?? body?.detail ?? "OSLO API request failed");
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export function resolveInvitation(token: string): Promise<InvitationDetails> {
  return apiRequest("/v1/invitations/resolve", {
    method: "POST",
    body: JSON.stringify({ token }),
  });
}

export function activateInvitation(input: {
  token: string;
  display_name: string;
  password: string;
}): Promise<SessionPayload> {
  return apiRequest("/v1/invitations/activate", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function acceptExistingInvitation(input: {
  token: string;
  email: string;
  password: string;
}): Promise<SessionPayload> {
  return apiRequest("/v1/invitations/accept-existing", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function sendInvitation(input: {
  accessToken: string;
  workspaceId: string;
  email: string;
  role: string;
}): Promise<{ id: string; email: string }> {
  return apiRequest(`/v1/workspaces/${input.workspaceId}/invitations`, {
    method: "POST",
    headers: { authorization: `Bearer ${input.accessToken}` },
    body: JSON.stringify({ email: input.email, role: input.role }),
  });
}

export function listInvitations(input: {
  accessToken: string;
  workspaceId: string;
}): Promise<InvitationSummary[]> {
  return apiRequest(`/v1/workspaces/${input.workspaceId}/invitations`, {
    method: "GET",
    headers: { authorization: `Bearer ${input.accessToken}` },
  });
}

export function resendInvitation(input: {
  accessToken: string;
  workspaceId: string;
  invitationId: string;
}): Promise<InvitationSummary> {
  return apiRequest(
    `/v1/workspaces/${input.workspaceId}/invitations/${input.invitationId}/resend`,
    { method: "POST", headers: { authorization: `Bearer ${input.accessToken}` } },
  );
}

export function revokeInvitation(input: {
  accessToken: string;
  workspaceId: string;
  invitationId: string;
}): Promise<void> {
  return apiRequest(
    `/v1/workspaces/${input.workspaceId}/invitations/${input.invitationId}`,
    { method: "DELETE", headers: { authorization: `Bearer ${input.accessToken}` } },
  );
}

export function startProject(input: {
  accessToken: string;
  workspaceId: string;
}): Promise<{ id: string; workspace_id: string; name: string; status: string }> {
  return apiRequest(`/v1/workspaces/${input.workspaceId}/projects`, {
    method: "POST",
    headers: { authorization: `Bearer ${input.accessToken}` },
  });
}
