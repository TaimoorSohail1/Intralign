import { redirect } from "next/navigation";

import { readSession } from "@/lib/server/session";

export default async function RollUpPage({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const session = await readSession();
  if (!session.accessToken) redirect("/login");
  const { projectId } = await params;
  redirect(`/projects/${projectId}/outcome`);
}
