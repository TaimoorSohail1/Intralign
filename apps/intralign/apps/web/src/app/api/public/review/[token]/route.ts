import { osloApiUrl } from "@/lib/server/oslo-api";

export async function POST(
  request: Request,
  context: { params: Promise<{ token: string }> },
) {
  const { token } = await context.params;
  const response = await fetch(
    `${osloApiUrl}/v1/public/review/${encodeURIComponent(token)}/responses`,
    {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: await request.text(),
      cache: "no-store",
    },
  );
  return new Response(await response.text(), {
    status: response.status,
    headers: { "content-type": "application/json" },
  });
}
