/**
 * The OSLO MUI theme — Intralign palette (CHG-068) + WCAG 2.1 AA + CssBaseline.
 *
 * This is the clean theme seam (DTM-0019, decision #7). It encodes ONLY the
 * owner-ratified visual facts and a sensible MUI default type scale; it invents
 * no fonts/logo/redlines. The designer refines `tokens.ts` + this file later.
 */
import { createTheme } from "@mui/material/styles";
import { intralign, surfaces } from "./tokens";

export { intralign, surfaces, epistemicTones } from "./tokens";

export const theme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: intralign.orange,
      // charcoal text on the orange fill clears AA (≈5.4:1); white on orange does not.
      contrastText: intralign.charcoal,
    },
    secondary: {
      main: intralign.charcoal,
      contrastText: intralign.warmWhite,
    },
    background: {
      default: intralign.warmWhite,
      paper: surfaces.paper,
    },
    text: {
      primary: intralign.charcoal,
      secondary: surfaces.textSecondary,
    },
    divider: surfaces.divider,
  },
  shape: {
    borderRadius: 8,
  },
  // Sensible MUI default type scale only (OPEN_TBD E4 — no invented fonts/redlines).
  // System font stack so nothing brand-specific is assumed before the designer lands.
  typography: {
    fontFamily: [
      "system-ui",
      "-apple-system",
      "Segoe UI",
      "Roboto",
      "Helvetica",
      "Arial",
      "sans-serif",
    ].join(","),
  },
  components: {
    MuiButton: {
      defaultProps: { disableElevation: true },
      styleOverrides: {
        // brand affordance: orange fill carries charcoal text (AA-safe)
        root: { textTransform: "none" },
      },
    },
  },
});

export type AppTheme = typeof theme;
