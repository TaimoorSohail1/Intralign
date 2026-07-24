import { redirect } from "next/navigation";

import { logout } from "@/app/logout-action";
import { IntakeExperience } from "@/components/intake/intake-experience";
import { readSession } from "@/lib/server/session";

export default async function IntakePage({
  searchParams,
}: {
  searchParams: Promise<{ project?: string }>;
}) {
  const session = await readSession();
  if (!session.accessToken) redirect("/login");
  const { project } = await searchParams;
  if (!project) redirect("/welcome");
  return (
    <IntakeExperience
      displayName={session.displayName ?? "there"}
      logoutAction={logout}
      projectId={project}
    />
  );
}
