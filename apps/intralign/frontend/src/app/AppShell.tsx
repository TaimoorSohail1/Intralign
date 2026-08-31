/**
 * AppShell — the persistent frame every Wave E surface mounts into.
 *
 * IA from RELEASE_1_UI_SPECIFICATION_V1 §2 (reconciled in DTM-0042). The §2 rail is
 * a single flat list (Projects, Findings, Recommendations, Reports, Shared Artifacts,
 * Notifications; Settings in the user menu), with the project-resource entries stated
 * to "resolve within the active project". Wave E landed those as project-SCOPED
 * surfaces (`/projects/$projectId/…`), so the rail is split into two groups (see
 * `navModel.ts`):
 *   - GLOBAL_NAV — always (Projects/Dashboard, Notifications, Settings).
 *   - PROJECT_NAV — only when a project is active (route under `/projects/$projectId`),
 *     each link targeting the ACTIVE project.
 * RP-C1 is preserved (no standalone Recommendations entry) and the Category-E
 * commodity screens (Reports, Shared) are omitted rather than left as dead-ends.
 *
 * Brand is designer-pending (OPEN_TBD E4): the wordmark is plain text, not a logo.
 */
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import ListSubheader from "@mui/material/ListSubheader";
import Divider from "@mui/material/Divider";
import { Link, Outlet, useRouterState } from "@tanstack/react-router";
import {
  GLOBAL_NAV,
  buildProjectNav,
  activeProjectIdFromPath,
  type NavEntry,
} from "./navModel";

const NAV_WIDTH = 240;

/** One nav row. Deferred entries (no R1 surface) render disabled, never a link. */
function NavRow({ item }: { item: NavEntry }) {
  if (item.deferred) {
    return (
      <ListItem disablePadding>
        <ListItemButton disabled data-testid="nav-deferred">
          <ListItemText primary={item.label} secondary="Not in Release 1" />
        </ListItemButton>
      </ListItem>
    );
  }
  return (
    <ListItem disablePadding>
      <ListItemButton
        component={Link}
        to={item.to}
        activeProps={{ "aria-current": "page" }}
        activeOptions={{ exact: !!item.exact }}
        data-testid="nav-link"
      >
        <ListItemText primary={item.label} />
      </ListItemButton>
    </ListItem>
  );
}

export function AppShell() {
  // Derive the active project from the current route (DTM-0042 locked decision:
  // project-context links target the ACTIVE project; never a project-scoped link
  // with no id). useRouterState keeps this reactive to navigation.
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const activeProjectId = activeProjectIdFromPath(pathname);
  const projectNav = activeProjectId ? buildProjectNav(activeProjectId) : null;

  return (
    <Box sx={{ display: "flex", minHeight: "100vh" }} data-testid="app-shell">
      <AppBar
        position="fixed"
        color="secondary"
        sx={{ zIndex: (t) => t.zIndex.drawer + 1 }}
      >
        <Toolbar>
          <Typography variant="h6" component="h1" sx={{ fontWeight: 700 }}>
            OSLO
          </Typography>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: NAV_WIDTH,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: NAV_WIDTH, boxSizing: "border-box" },
        }}
      >
        <Toolbar />
        <Box component="nav" aria-label="Primary" sx={{ overflow: "auto" }}>
          <List
            aria-label="Global"
            data-testid="nav-global"
            subheader={
              <ListSubheader component="div" disableSticky>
                Workspace
              </ListSubheader>
            }
          >
            {GLOBAL_NAV.map((item) => (
              <NavRow key={item.to} item={item} />
            ))}
          </List>

          {projectNav ? (
            <>
              <Divider />
              <List
                aria-label="Project"
                data-testid="nav-project"
                subheader={
                  <ListSubheader component="div" disableSticky>
                    Project
                  </ListSubheader>
                }
              >
                {projectNav.map((item) => (
                  <NavRow key={item.to} item={item} />
                ))}
              </List>
            </>
          ) : (
            <>
              <Divider />
              <List aria-label="Project" data-testid="nav-project-hint">
                <ListItem>
                  <ListItemText
                    primary="Project"
                    secondary="Open a project to see its surfaces."
                    primaryTypographyProps={{ variant: "overline" }}
                  />
                </ListItem>
              </List>
            </>
          )}
        </Box>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, p: 3 }} data-testid="app-content">
        <Toolbar />
        {/* surfaces render here */}
        <Outlet />
      </Box>
    </Box>
  );
}

export default AppShell;
