import { redirect } from "next/navigation";

import { logout } from "@/app/logout-action";
import { IntakeExperience } from "@/components/intake/intake-experience";
import { readSession } from "@/lib/server/session";

export default async function IntakePage() {
  const session = await readSession();
  if (!session.accessToken) redirect("/login");
  return <IntakeExperience displayName={session.displayName ?? "there"} logoutAction={logout} />;
}
