/**
 * ArtifactEditorRoute — the Artifact Editor route element that mounts the Assisted-
 * Editing / Persistent-Intelligence panel (AW-04/05), replacing the DTM-0019 placeholder.
 *
 * The panel is always-visible, read-only, and routes assists (to Chat / Suggested Fix) —
 * it performs no cognition. It needs the project context (Outcome Confidence / CAF /
 * Understanding-State are project-scoped reads); the editor reads `project_id` (and an
 * optional `finding_id` for the B3 Suggested-Fix route) from the route search. When no
 * project context is present the panel is held with a clean empty state rather than
 * fabricating a project.
 *
 * NOTE: the artifact CONTENT editor (the editable text + save/reanalysis state machine,
 * ARTIFACT_AUTHORING spec) is a separate, out-of-scope build — this slice owns only the
 * Persistent-Intelligence panel (AW-04/05). The content area is left as a clean seam.
 */
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import { getRouteApi } from "@tanstack/react-router";
import { AssistedEditing } from "./AssistedEditing";
import { HonestLimitDisclosure } from "../../components/HonestLimitDisclosure";

const routeApi = getRouteApi("/artifacts/$artifactId");

export function ArtifactEditorRoute() {
  const { artifactId } = routeApi.useParams();
  const { project_id, finding_id, limited } = routeApi.useSearch();

  return (
    <Box
      data-testid="artifact-editor"
      sx={{
        display: "grid",
        gridTemplateColumns: { xs: "1fr", md: "minmax(0, 1fr) 320px" },
        gap: 2,
        py: 1,
      }}
    >
      {/* The artifact content area — a clean seam (the content editor is out of scope). */}
      <Paper variant="outlined" sx={{ p: 2 }} data-testid="artifact-content">
        <Typography variant="h5" component="h2" gutterBottom>
          Artifact
        </Typography>
        <Typography variant="body2" color="text.secondary">
          The artifact content view. Editing changes content only; only reanalysis changes
          the assessment.
        </Typography>

        {/* DL-048 honest-limit disclosure — rendered on this same (partial-orientation)
            surface when the run is scope/budget-limited, truthfully and with the reason,
            and the upgrade prompt ALONGSIDE (never instead of). The limit SIGNAL is not
            yet exposed over REST (flagged) — `limited` is the presentation seam. */}
        {limited ? (
          <HonestLimitDisclosure
            limit={{
              limited: true,
              reason:
                "This project exceeds the Free tier size, so the analysis covered only part of it.",
              coverage_note:
                "Roughly the first portion of the project content was analyzed.",
              upgrade: {
                message: "Basic analyzes projects up to ~100k words.",
                cta_label: "See Basic",
              },
            }}
          />
        ) : null}
      </Paper>

      {/* The always-visible Persistent-Intelligence panel (AW-04/05). */}
      {project_id ? (
        <AssistedEditing
          projectId={project_id}
          artifactId={artifactId}
          findingId={finding_id}
        />
      ) : (
        <Paper variant="outlined" sx={{ p: 2 }} data-testid="assisted-editing-no-context">
          <Typography variant="subtitle1" sx={{ fontWeight: 700 }} gutterBottom>
            Persistent intelligence
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Open this artifact from its project to see OSLO&apos;s current understanding
            (Outcome Confidence, CAF, and Understanding-State) alongside it.
          </Typography>
        </Paper>
      )}
    </Box>
  );
}

export default ArtifactEditorRoute;
