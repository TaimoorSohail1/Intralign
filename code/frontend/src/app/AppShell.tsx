/**
 * AppShell — the persistent frame every Wave E surface mounts into.
 *
 * IA from RELEASE_1_UI_SPECIFICATION_V1 §2: a persistent left rail (Projects,
 * Findings, Recommendations, Reports, Shared Artifacts, Notifications) + a content
 * outlet. No surface content lives here — surfaces render in the <Outlet/>.
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
import { Link, Outlet } from "@tanstack/react-router";

const NAV_WIDTH = 240;

/** Top-level nav entries — mirror the API resource scoping (UI spec §2). */
const NAV: Array<{ to: string; label: string }> = [
  { to: "/", label: "Projects" },
  { to: "/findings", label: "Findings" },
  { to: "/recommendations", label: "Recommendations" },
  { to: "/reports", label: "Reports" },
  { to: "/shared", label: "Shared Artifacts" },
  { to: "/notifications", label: "Notifications" },
  { to: "/settings", label: "Settings" },
];

export function AppShell() {
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
          <List>
            {NAV.map((item) => (
              <ListItem key={item.to} disablePadding>
                <ListItemButton
                  component={Link}
                  to={item.to}
                  activeProps={{ "aria-current": "page" }}
                  activeOptions={{ exact: item.to === "/" }}
                >
                  <ListItemText primary={item.label} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>

      <Box
        component="main"
        sx={{ flexGrow: 1, p: 3 }}
        data-testid="app-content"
      >
        <Toolbar />
        <Outlet />
      </Box>
    </Box>
  );
}

export default AppShell;
