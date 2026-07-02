/**
 * DTM-0024 — Dashboard / Project List (IC-WE-DISCLOSE E1).
 *
 * The project discovery layer: the user's workspace projects, each presented with
 *
 *   - its **name** + a lifecycle/status indicator (a presented fact, never computed);
 *   - its **current Outcome Confidence** as a Derived `EpistemicLabel` (banded,
 *     conflict-aware) — a recomputable projection, never shown as settled; confidence
 *     = trust-in-understanding, NEVER project health / readiness / probability;
 *   - a **link to its workspace** (`/projects/$projectId`).
 *
 * A "calm index", not a metrics cockpit (Dashboard & Project List Experience Spec
 * §C, PL-6/PL-13): no computed score, no "health"/"readiness"/"on-track" indicator,
 * and the raw 0–100 confidence value / percentage is NEVER rendered — only the band.
 *
 * Read-only: there is no edit / score / accept / generate / recompute / archive /
 * pin control on this slice (decision #3 — Disclose presents, never generates; only
 * reanalysis changes an assessment, and reanalysis is not a Disclose affordance).
 * Search/filter/sort/archive/pin are deferred presentation affordances (Spec §H–§O)
 * — out of scope for this read slice; the gap is noted, not invented.
 *
 * THE PER-PROJECT-CONFIDENCE READ: the Project DTO carries no embedded confidence —
 * only `current_confidence_state_id`. The current Outcome Confidence is fetched per
 * row via the DTM-0018 `GET /projects/{pid}/confidence` read (UI_SCREEN_INVENTORY:
 * Dashboard → `GET /projects`, `GET /projects/{pid}/confidence`). A project with no
 * confidence yet (e.g. created, not analyzed) presents a clean "not yet available",
 * never a fabricated value (Spec §S, PL-12).
 *
 * It consumes the DTM-0018 Orval hooks read-only; the project list may be empty until
 * platform persistence lands → loading + empty states render cleanly and positively.
 */
import { useState } from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Chip from "@mui/material/Chip";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import CircularProgress from "@mui/material/CircularProgress";
import Alert from "@mui/material/Alert";
import { Link } from "@tanstack/react-router";
import { useQueryClient } from "@tanstack/react-query";

import {
  useListProjectsV1ProjectsGet,
  getListProjectsV1ProjectsGetQueryKey,
} from "../../api/generated/projects/projects";
import { useCreateProjectV1ProjectsPost } from "../../api/generated/project-commands/project-commands";
import { useGetConfidenceV1ProjectsProjectIdConfidenceGet } from "../../api/generated/confidence/confidence";
import { EpistemicLabel, fromDerivedEnvelope } from "../../components/EpistemicLabel";
import type {
  Project,
  ProjectLifecycle,
  ConfidenceState,
} from "../../api/generated/oSLORelease1API.schemas";

/** True for a plain object DTO (not an array, string, or null). */
function isRecord(v: unknown): v is Record<string, unknown> {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}

function asProjectArray(v: unknown): Project[] {
  return Array.isArray(v)
    ? (v.filter((x) => x && typeof x === "object") as Project[])
    : [];
}

/** Presented lifecycle/status label — a fact from the project, never computed. */
const LIFECYCLE_LABEL: Record<ProjectLifecycle, string> = {
  created: "Not yet analyzed",
  orienting: "Analyzing",
  oriented: "Oriented",
  deep_analyzing: "Analyzing (deep)",
  analyzed: "Analyzed",
  archived: "Archived",
};

/**
 * One project row — name + status + current confidence (Derived label) + a workspace
 * link. The current confidence is fetched per row (the Project DTO carries no
 * embedded confidence). A project without confidence yet shows a clean
 * "not yet available" instead of a fabricated value.
 */
function ProjectRow({ project }: { project: Project }) {
  const confidenceQ = useGetConfidenceV1ProjectsProjectIdConfidenceGet(
    project.project_id,
  );
  const confidence = isRecord(confidenceQ.data?.data)
    ? (confidenceQ.data?.data as ConfidenceState)
    : undefined;

  return (
    <Paper
      variant="outlined"
      sx={{ p: 2 }}
      data-testid="project-row"
      data-project-id={project.project_id}
    >
      <Box
        sx={{
          display: "flex",
          gap: 2,
          alignItems: "flex-start",
          justifyContent: "space-between",
          flexWrap: "wrap",
        }}
      >
        <Box sx={{ minWidth: 0 }}>
          <Typography variant="subtitle1" sx={{ fontWeight: 700 }}>
            {project.title ?? project.project_id}
          </Typography>
          {project.description ? (
            <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
              {project.description}
            </Typography>
          ) : null}
          <Box sx={{ display: "flex", gap: 1, alignItems: "center", flexWrap: "wrap" }}>
            {/* Status — a presented lifecycle fact, never a computed value. */}
            <Chip
              size="small"
              variant="outlined"
              label={LIFECYCLE_LABEL[project.lifecycle_state] ?? project.lifecycle_state}
              data-testid="project-status"
              data-lifecycle={project.lifecycle_state}
            />
            {/* Current Outcome Confidence — Derived, banded; never settled. */}
            {confidenceQ.isLoading ? (
              <Typography
                data-testid="confidence-loading"
                variant="caption"
                color="text.secondary"
              >
                Loading confidence…
              </Typography>
            ) : confidence ? (
              <EpistemicLabel epistemic={fromDerivedEnvelope(confidence.label)} />
            ) : (
              <Typography
                data-testid="confidence-unavailable"
                variant="caption"
                color="text.secondary"
              >
                Confidence not yet available
              </Typography>
            )}
          </Box>
        </Box>

        {/* Link to the project's workspace. */}
        <Link
          to="/projects/$projectId"
          params={{ projectId: project.project_id }}
          style={{ textDecoration: "none" }}
          data-testid="open-workspace"
        >
          <Button variant="outlined" component="span" size="small">
            Open workspace
          </Button>
        </Link>
      </Box>
    </Paper>
  );
}

/**
 * The create-project AFFORDANCE (DTM-0039 → §5 `POST /projects`). A user-initiated
 * command that creates a new project (lifecycle `created`) — it computes no cognition;
 * the new project starts un-analyzed. On success the project-list read is invalidated.
 */
function CreateProject() {
  const queryClient = useQueryClient();
  const createM = useCreateProjectV1ProjectsPost({
    mutation: {
      onSuccess: () =>
        queryClient.invalidateQueries({
          queryKey: getListProjectsV1ProjectsGetQueryKey(),
        }),
    },
  });
  const [title, setTitle] = useState("");

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    createM.mutate(
      { data: { title: title.trim() } },
      { onSuccess: () => setTitle("") },
    );
  };

  return (
    <Paper variant="outlined" sx={{ p: 2, mb: 2 }} data-testid="create-project">
      <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 700 }}>
        New project
      </Typography>
      <Box component="form" onSubmit={submit} sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
        <TextField
          size="small"
          label="Project name"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          inputProps={{ "data-testid": "create-project-title" }}
          sx={{ flexGrow: 1 }}
        />
        <Button
          type="submit"
          variant="contained"
          disabled={createM.isPending}
          data-testid="create-project-submit"
        >
          Create project
        </Button>
      </Box>
    </Paper>
  );
}

export function Dashboard() {
  const projectsQ = useListProjectsV1ProjectsGet();
  const projects = asProjectArray(projectsQ.data?.data);
  const loading = projectsQ.isLoading;

  return (
    <Box data-testid="dashboard" sx={{ py: 1 }}>
      <Typography variant="h5" component="h2" gutterBottom data-testid="surface-title">
        Projects
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Your projects and how much OSLO currently trusts its understanding of each.
        Open a project to go deeper. OSLO presents this; it computes nothing here —
        only reanalysis changes a project&apos;s understanding.
      </Typography>

      <CreateProject />

      {loading ? (
        <Box
          data-testid="dashboard-loading"
          sx={{ display: "flex", alignItems: "center", gap: 1, mb: 2 }}
        >
          <CircularProgress size={18} />
          <Typography variant="body2" color="text.secondary">
            Loading your projects…
          </Typography>
        </Box>
      ) : projectsQ.isError ? (
        <Alert severity="error" data-testid="dashboard-error">
          Projects could not be loaded. Refresh the page and try again.
        </Alert>
      ) : projects.length === 0 ? (
        <Paper variant="outlined" sx={{ p: 2 }}>
          <Typography
            data-testid="dashboard-empty"
            variant="body2"
            color="text.secondary"
          >
            No projects yet. Create your first project to start building understanding.
          </Typography>
        </Paper>
      ) : (
        <Stack spacing={2}>
          {projects.map((project) => (
            <ProjectRow key={project.project_id} project={project} />
          ))}
        </Stack>
      )}
    </Box>
  );
}

export default Dashboard;
