import { osloApiUrl } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export async function GET(
  _request: Request,
  context: { params: Promise<{ projectId: string }> },
) {
  const session = await readSession();
  if (!session.accessToken) return Response.json({ message: "Unauthorized" }, { status: 401 });
  const { projectId } = await context.params;
  const response = await fetch(`${osloApiUrl}/v1/projects/${projectId}/exports/pdf`, {
    headers: { authorization: `Bearer ${session.accessToken}` },
    cache: "no-store",
  });
  return new Response(response.body, {
    status: response.status,
    headers: {
      "content-type": response.headers.get("content-type") ?? "application/pdf",
      "content-disposition": response.headers.get("content-disposition") ?? "attachment",
    },
  });
}
