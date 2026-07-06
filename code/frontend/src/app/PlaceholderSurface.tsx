/**
 * Placeholder route element. DTM-0019 ships only the SHELL — the real surfaces
 * (MRI, Finding Panel, Recommendation Panel, …) are authored in DTM-0020+ and
 * mount under `src/surfaces/`. This element holds a route's slot until then.
 *
 * It deliberately renders NO governed cognition (Disclose presents existing
 * canonical data — there is none to present yet, and the shell never generates).
 */
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

export interface PlaceholderSurfaceProps {
  title: string;
  /** The screen's one-line purpose from UI_SCREEN_INVENTORY (placeholder copy). */
  purpose?: string;
}

export function PlaceholderSurface({ title, purpose }: PlaceholderSurfaceProps) {
  return (
    <Box sx={{ py: 2 }}>
      <Typography variant="h5" component="h2" gutterBottom data-testid="surface-title">
        {title}
      </Typography>
      {purpose ? (
        <Typography variant="body1" color="text.secondary">
          {purpose}
        </Typography>
      ) : null}
      <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: "block" }}>
        Surface pending (DTM-0020+). This route is part of the app shell only.
      </Typography>
    </Box>
  );
}

export default PlaceholderSurface;
