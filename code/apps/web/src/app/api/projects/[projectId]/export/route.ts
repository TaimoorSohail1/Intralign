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
  if (!response.ok) {
    const failure = await response.json().catch(() => null);
    const message =
      failure?.detail?.message ??
      failure?.message ??
      "The snapshot could not be exported.";
    return Response.json({ message }, { status: response.status });
  }
  const pdf = await response.arrayBuffer();
  const signature = new TextDecoder("latin1").decode(pdf.slice(0, 5));
  if (signature !== "%PDF-") {
    return Response.json(
      { message: "The report service returned an invalid PDF." },
      { status: 502 },
    );
  }
  return new Response(pdf, {
    status: response.status,
    headers: {
      "content-type": "application/pdf",
      "content-disposition": response.headers.get("content-disposition") ?? "attachment",
      "content-length": String(pdf.byteLength),
    },
  });
}
