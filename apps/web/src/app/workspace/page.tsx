import { redirect } from "next/navigation";

import { WorkspaceHome } from "@/components/workspace/workspace-home";
import { getWorkspace } from "@/lib/server/oslo-api";
import { readSession } from "@/lib/server/session";

export default async function WorkspacePage({
  searchParams,
}: {
  searchParams: Promise<{ new?: string }>;
}) {
  const session = await readSession();
  if (!session.accessToken || !session.workspaceId) redirect("/login");
  const workspace = await getWorkspace({
    accessToken: session.accessToken,
    workspaceId: session.workspaceId,
  });
  return (
    <WorkspaceHome
      displayName={session.displayName ?? "Member"}
      initial={workspace}
      openNewProject={(await searchParams).new === "1"}
    />
  );
}
