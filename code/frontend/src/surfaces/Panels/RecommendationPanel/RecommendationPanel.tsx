/**
 * DTM-0022 — the Recommendation Panel (IC-WE-DISCLOSE E1; RP-C1).
 *
 * The contextual, advisory-first, finding-anchored surface (Recommendation Panel
 * Spec v1). It PRESENTS the Recommendations anchored to ONE Finding and NEVER
 * GENERATES — and, critically, NEVER ACCEPTS:
 *
 *   - The finding's Recommendations, read via the DTM-0018
 *     `useListRecommendationsForFinding…` hook (read-only). Each is a Derived
 *     projection labelled via `fromDerivedEnvelope` → `EpistemicLabel` (never
 *     shown settled), and carries its DL-055 `status` read from the governed
 *     source as-is (Generated/Accepted/Rejected/Deferred/…) — the panel presents
 *     the status, it does not set it.
 *   - **OSLO Recommended** — the primary recommendation, shown distinctly (§J).
 *   - **Resolution Paths** — the *other* Recommendations for the SAME finding,
 *     grouped as a PRESENTATION SUBSTRUCTURE (§J / RP-6). This is markup over the
 *     same `recommendation_id`s; it constructs/emits NO Resolution-Path object,
 *     field, lifecycle, or event. Alternatives stay visible after acceptance (RP-5).
 *   - The **accept / reject / defer affordance** (§K). This is an AFFORDANCE, not
 *     a write: Disclose renders it but NEVER performs acceptance (decision #3,
 *     Critical). It hands off to the EXISTING Wave U capture seam — it does NOT
 *     flip a recommendation to "Accepted" client-side, mark it accepted, or write
 *     any canonical/version-pin (Wave U owns acceptance + the mandatory
 *     version-pin). version-pin is mandatory on any acceptance; the panel performs
 *     none.
 *
 * RP-C1 — Recommendation-only-in-Finding-context: this surface is meaningful ONLY
 * within a Finding context. The route tree mounts it solely under a Finding
 * (`…/findings/$findingId/recommendations`); as a defence in depth, when no
 * `findingId` is present the panel renders an explicit no-context guard and NO
 * recommendation content (a standalone Recommendation Panel is a rejected negative).
 *
 * Read-only / presents-never-generates: there is no generate / score / recompute /
 * reanalyze / resolve-finding / govern / approve / execute / apply affordance
 * (Recommendation Panel Spec §K prohibitions; RP-7/RP-8/RP-10/RP-11). Only
 * reanalysis changes assessment, and reanalysis is not a Disclose affordance.
 *
 * Acceptance-write wiring (DTM-0039 — replaces the DTM-0022 hand-off): the affordance
 * now calls the user-initiated acceptance COMMAND (the generated
 * `acceptance-commands` hooks — `:accept`/`:reject`/`:defer`/`:implement`). The
 * BACKEND records the UAR (+ version-pin) and writes the plan fact on accept; the
 * SURFACE performs NO local acceptance — it does NOT flip the recommendation to
 * "Accepted" client-side and writes no canonical. On success it invalidates the
 * finding-recs read so the governed status is re-read from the source. Disclose still
 * presents the affordance; it never accepts itself.
 */
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Chip from "@mui/material/Chip";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";
import Divider from "@mui/material/Divider";
import { useQueryClient } from "@tanstack/react-query";

import {
  useListRecommendationsForFindingV1FindingsFindingIdRecommendationsGet,
  getListRecommendationsForFindingV1FindingsFindingIdRecommendationsGetQueryKey,
} from "../../../api/generated/recommendations/recommendations";
import {
  useAcceptRecommendationV1RecommendationsRecommendationIdAcceptPost,
  useRejectRecommendationV1RecommendationsRecommendationIdRejectPost,
  useDeferRecommendationV1RecommendationsRecommendationIdDeferPost,
  useImplementRecommendationV1RecommendationsRecommendationIdImplementPost,
} from "../../../api/generated/acceptance-commands/acceptance-commands";
import { EpistemicLabel, fromDerivedEnvelope } from "../../../components/EpistemicLabel";
import { epistemicTones } from "../../../theme/tokens";
import type {
  Recommendation,
  RecommendationStatus,
  RecommendationType,
  EffortLevel,
  Dimension,
} from "../../../api/generated/oSLORelease1API.schemas";

export interface RecommendationPanelProps {
  projectId: string;
  /**
   * The Finding this panel is anchored to. RP-C1: when absent there is no Finding
   * context, so the panel renders the no-context guard and NO recommendation
   * content. The optional shape lets the route adapter pass through whatever the
   * (Finding-nested) route resolves.
   */
  findingId?: string;
}

/** User-facing label for the DL-055 lifecycle status (presentation, §N). */
const STATUS_LABEL: Record<RecommendationStatus, string> = {
  generated: "New",
  accepted: "Accepted",
  rejected: "Rejected",
  deferred: "Set aside",
  implemented: "Acted on",
  superseded: "Superseded",
};

/** User-friendly recommendation type (descriptive, never a directive). */
const TYPE_LABEL: Record<RecommendationType, string> = {
  improvement: "Improvement",
  validation: "Validation",
  suggested_fix: "Suggested fix",
};

const EFFORT_LABEL: Record<EffortLevel, string> = {
  low: "Low effort",
  medium: "Medium effort",
  high: "High effort",
};

const DIMENSION_LABEL: Record<Dimension, string> = {
  clarity: "Clarity",
  alignment: "Alignment",
  feasibility: "Feasibility",
};

/** True for a plain object DTO (not an array, string, or null). */
function isRecord(v: unknown): v is Record<string, unknown> {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}

/** A titled section card — pure presentation scaffolding. */
function Section({
  title,
  testId,
  subtitle,
  children,
}: {
  title: string;
  testId?: string;
  subtitle?: string;
  children: React.ReactNode;
}) {
  return (
    <Paper variant="outlined" sx={{ p: 2 }} data-testid={testId}>
      <Typography variant="subtitle1" sx={{ fontWeight: 700 }} gutterBottom>
        {title}
      </Typography>
      {subtitle ? (
        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
          {subtitle}
        </Typography>
      ) : null}
      {children}
    </Paper>
  );
}

/**
 * The accept / reject / defer / implement AFFORDANCE for a recommendation (§K).
 *
 * DTM-0039: each button calls the user-initiated acceptance COMMAND (the generated
 * `acceptance-commands` mutation hooks). The BACKEND records the UAR (+ the mandatory
 * version-pin) and writes the plan fact on accept — the SURFACE performs NO local
 * acceptance: it never flips the recommendation to "Accepted" client-side and writes
 * no canonical. On success it invalidates the finding-recs read so the governed
 * status is re-read from the source (the only place the status changes). Disclose
 * still presents the affordance; it never accepts itself.
 */
function AcceptanceAffordance({
  findingId,
  projectId,
  recommendationId,
}: {
  findingId: string;
  projectId: string;
  recommendationId: string;
}) {
  const queryClient = useQueryClient();

  // On any acceptance command succeeding, re-read the governed recommendation list for
  // this finding — the surface never mutates the status locally, it re-reads it.
  const invalidate = () =>
    queryClient.invalidateQueries({
      queryKey: getListRecommendationsForFindingV1FindingsFindingIdRecommendationsGetQueryKey(
        findingId,
        { project_id: projectId },
      ),
    });

  const acceptM = useAcceptRecommendationV1RecommendationsRecommendationIdAcceptPost({
    mutation: { onSuccess: invalidate },
  });
  const rejectM = useRejectRecommendationV1RecommendationsRecommendationIdRejectPost({
    mutation: { onSuccess: invalidate },
  });
  const deferM = useDeferRecommendationV1RecommendationsRecommendationIdDeferPost({
    mutation: { onSuccess: invalidate },
  });
  const implementM = useImplementRecommendationV1RecommendationsRecommendationIdImplementPost({
    mutation: { onSuccess: invalidate },
  });

  const pending =
    acceptM.isPending || rejectM.isPending || deferM.isPending || implementM.isPending;

  return (
    <Box
      data-testid="acceptance-affordance"
      sx={{ display: "flex", gap: 1, flexWrap: "wrap", mt: 1 }}
    >
      <Typography variant="body2" color="text.secondary" sx={{ width: "100%", mb: 0.5 }}>
        Your decision is recorded by OSLO&apos;s acceptance capture — this panel presents the
        options; it does not accept on your behalf, and accepting changes no assessment.
      </Typography>
      <Button
        variant="contained"
        disabled={pending}
        data-testid="affordance-accept"
        onClick={() => acceptM.mutate({ recommendationId })}
      >
        Accept this recommendation
      </Button>
      <Button
        variant="outlined"
        disabled={pending}
        data-testid="affordance-reject"
        onClick={() => rejectM.mutate({ recommendationId })}
      >
        Reject this recommendation
      </Button>
      <Button
        variant="outlined"
        disabled={pending}
        data-testid="affordance-defer"
        onClick={() => deferM.mutate({ recommendationId })}
      >
        Defer this recommendation
      </Button>
      <Button
        variant="outlined"
        disabled={pending}
        data-testid="affordance-implement"
        onClick={() => implementM.mutate({ recommendationId })}
      >
        Mark as acted on
      </Button>
    </Box>
  );
}

/** One recommendation card — its header, label, status, rationale, affordance. */
function RecommendationCard({
  findingId,
  projectId,
  rec,
  primary,
}: {
  findingId: string;
  projectId: string;
  rec: Recommendation;
  primary: boolean;
}) {
  const status = (rec.status ?? "generated") as RecommendationStatus;
  return (
    <Paper
      variant="outlined"
      sx={{ p: 2, borderColor: primary ? epistemicTones.derived : "divider" }}
      data-testid="recommendation-item"
      data-recommendation-id={rec.recommendation_id}
      data-status={status}
    >
      {/* the same node, also addressable by id, so a test can target one card */}
      <Box data-testid={`recommendation-item-${rec.recommendation_id}`} data-status={status}>
        <Box sx={{ display: "flex", gap: 1, alignItems: "center", flexWrap: "wrap", mb: 1 }}>
          {primary ? (
            <Chip
              size="small"
              label="OSLO recommended"
              data-testid="oslo-recommended"
              sx={{ color: "#fff", backgroundColor: epistemicTones.derived, fontWeight: 600 }}
            />
          ) : null}
          {rec.recommendation_type ? (
            <Chip
              size="small"
              variant="outlined"
              label={TYPE_LABEL[rec.recommendation_type as RecommendationType] ?? rec.recommendation_type}
              data-testid="recommendation-type"
            />
          ) : null}
          {/* DL-055 status, read as-is from the governed source — presented, not set */}
          <Chip
            size="small"
            variant="outlined"
            label={STATUS_LABEL[status] ?? status}
            data-testid="recommendation-status"
            data-status={status}
          />
          {rec.effort ? (
            <Chip
              size="small"
              variant="outlined"
              label={EFFORT_LABEL[rec.effort as EffortLevel] ?? rec.effort}
              data-testid="recommendation-effort"
            />
          ) : null}
          {rec.expected_dimension ? (
            <Chip
              size="small"
              variant="outlined"
              label={DIMENSION_LABEL[rec.expected_dimension as Dimension] ?? rec.expected_dimension}
              data-testid="recommendation-dimension"
            />
          ) : null}
        </Box>

        <Typography variant="body1" sx={{ fontWeight: 600 }}>
          {rec.title ?? rec.recommendation_id}
        </Typography>
        {rec.description ? (
          <Typography variant="body2" sx={{ mt: 0.5 }}>
            {rec.description}
          </Typography>
        ) : null}
        {rec.rationale ? (
          <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
            Why OSLO suggests this: {rec.rationale}
          </Typography>
        ) : null}

        {/* Derived label — a projection, banded, never shown settled */}
        <Box sx={{ mt: 1 }}>
          <EpistemicLabel epistemic={fromDerivedEnvelope(rec.label)} />
        </Box>

        {/* The accept/reject/defer/implement affordance — calls the command; the
            backend records the UAR. The surface performs no local acceptance. */}
        <AcceptanceAffordance
          findingId={findingId}
          projectId={projectId}
          recommendationId={rec.recommendation_id}
        />
      </Box>
    </Paper>
  );
}

export function RecommendationPanel({ projectId, findingId }: RecommendationPanelProps) {
  // RP-C1 — defence in depth: no Finding context ⇒ no recommendation content. The
  // route tree already mounts this only under a Finding; this guard makes a
  // standalone render a no-op presentation (a rejected negative).
  if (!findingId) {
    return (
      <Box data-testid="recommendation-panel" sx={{ py: 1 }}>
        <Typography variant="h5" component="h2" gutterBottom data-testid="surface-title">
          Recommendations
        </Typography>
        <Paper variant="outlined" sx={{ p: 2 }}>
          <Typography data-testid="recommendation-panel-no-context" variant="body2" color="text.secondary">
            Recommendations open only within a finding's context — there's nothing to show on
            their own. Open a finding to see the recommendations that address it.
          </Typography>
        </Paper>
      </Box>
    );
  }

  return <RecommendationPanelInner projectId={projectId} findingId={findingId} />;
}

function RecommendationPanelInner({
  projectId,
  findingId,
}: {
  projectId: string;
  findingId: string;
}) {
  const recsQ = useListRecommendationsForFindingV1FindingsFindingIdRecommendationsGet(
    findingId,
    { project_id: projectId },
  );

  // Defensive coercion: the projection may be absent until upstream populates it.
  const recommendations: Recommendation[] = Array.isArray(recsQ.data?.data)
    ? (recsQ.data?.data as Recommendation[]).filter(isRecord)
    : [];

  const loading = recsQ.isLoading;

  // OSLO Recommended = the primary (first); the rest are the alternatives shown as
  // Resolution Paths. This is presentation ordering only — no object is created.
  const [primary, ...alternatives] = recommendations;

  return (
    <Box data-testid="recommendation-panel" sx={{ py: 1 }}>
      <Typography variant="h5" component="h2" gutterBottom data-testid="surface-title">
        Recommendations
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Advisory recommendations that address this finding. OSLO suggests; you decide. Choosing
        one records your decision through OSLO's acceptance capture — it changes no assessment by
        itself; only reanalysis does.
      </Typography>

      {loading ? (
        <Box
          data-testid="recommendation-loading"
          sx={{ display: "flex", alignItems: "center", gap: 1, mb: 2 }}
        >
          <CircularProgress size={18} />
          <Typography variant="body2" color="text.secondary">
            Loading recommendations…
          </Typography>
        </Box>
      ) : recommendations.length === 0 ? (
        <Paper variant="outlined" sx={{ p: 2 }}>
          <Typography data-testid="recommendation-empty" variant="body2" color="text.secondary">
            No recommendations address this finding yet. (Distinct from “still being generated” —
            this finding currently has none on record.)
          </Typography>
        </Paper>
      ) : (
        <Stack spacing={2}>
          {/* ── OSLO Recommended — the primary, shown distinctly (§J) ── */}
          <Section
            title="OSLO recommended"
            testId="oslo-recommended-section"
            subtitle="What OSLO currently suggests as the primary way to address this finding — advisory, no score."
          >
            <RecommendationCard findingId={findingId} projectId={projectId} rec={primary} primary />
          </Section>

          {/* ── Resolution Paths — the OTHER recommendations, grouped (§J / RP-6) ──
               A PRESENTATION grouping of multiple Recommendations: no object, field,
               lifecycle, or event. Alternatives stay visible after acceptance (RP-5). */}
          {alternatives.length > 0 ? (
            <Section
              title="Resolution Paths"
              testId="resolution-paths"
              subtitle="Other recommendations that address the same finding — shown together so you can compare. This is a way of presenting multiple recommendations, not a separate thing OSLO created."
            >
              <Stack spacing={2}>
                {alternatives.map((rec) => (
                  <Box
                    key={rec.recommendation_id}
                    data-testid="resolution-path"
                    data-recommendation-id={rec.recommendation_id}
                  >
                    <RecommendationCard findingId={findingId} projectId={projectId} rec={rec} primary={false} />
                  </Box>
                ))}
              </Stack>
            </Section>
          ) : (
            <Paper variant="outlined" sx={{ p: 2 }}>
              <Typography data-testid="no-alternatives" variant="body2" color="text.secondary">
                No alternative recommendations for this finding — OSLO Recommended above is the
                only one on record.
              </Typography>
            </Paper>
          )}

          <Divider />
          <Typography variant="caption" color="text.secondary">
            Accepting, rejecting, or deferring records your decision and changes no assessment on
            its own. Only reanalysis can weaken or close the finding.
          </Typography>
        </Stack>
      )}
    </Box>
  );
}

export default RecommendationPanel;
