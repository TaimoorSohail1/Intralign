import { getProjectAsanaHandoff, importProjectToAsana, OsloApiError } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

function failure(error: unknown) {
  if (error instanceof OsloApiError) {
    return Response.json(
      { message: error.message, detail: error.detail },
      { status: error.status },
    );
  }
  return Response.json({ message: "Asana hand-off is unavailable." }, { status: 502 });
}

export async function GET(
  _request: Request,
  context: { params: Promise<{ projectId: string }> },
) {
  const session = await readSession();
  if (!session.accessToken) return Response.json({ message: "Unauthorized" }, { status: 401 });
  const { projectId } = await context.params;
  try {
    return Response.json(
      await getProjectAsanaHandoff({ accessToken: session.accessToken, projectId }),
    );
  } catch (error) {
    return failure(error);
  }
}

export async function POST(
  _request: Request,
  context: { params: Promise<{ projectId: string }> },
) {
  const session = await readSession();
  if (!session.accessToken) return Response.json({ message: "Unauthorized" }, { status: 401 });
  const { projectId } = await context.params;
  try {
    return Response.json(
      await importProjectToAsana({ accessToken: session.accessToken, projectId }),
      { status: 201 },
    );
  } catch (error) {
    return failure(error);
  }
}
