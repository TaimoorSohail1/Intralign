import { redirect } from "next/navigation";

import { logout } from "@/app/logout-action";
import { IntakeExperience } from "@/components/intake/intake-experience";
import { readSession } from "@/lib/server/session";

export default async function IntakePage({
  searchParams,
}: {
  searchParams: Promise<{ project?: string; returning?: string }>;
}) {
  const session = await readSession();
  if (!session.accessToken) redirect("/login");
  const { project, returning } = await searchParams;
  if (!project) redirect("/welcome");
  return (
    <IntakeExperience
      displayName={session.displayName ?? "there"}
      logoutAction={logout}
      projectId={project}
      returningClient={returning === "1"}
    />
  );
}
