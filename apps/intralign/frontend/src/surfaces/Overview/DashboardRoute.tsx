/**
 * DashboardRoute — the thin route element for the Dashboard / Project List. It mounts
 * at the top-level `/` route, replacing the DTM-0019 placeholder. The Dashboard takes
 * no params (it lists the caller's workspace projects), so the adapter is a trivial
 * pass-through that keeps the surface itself decoupled from the router.
 */
import { Dashboard } from "./Dashboard";

export function DashboardRoute() {
  return <Dashboard />;
}

export default DashboardRoute;
