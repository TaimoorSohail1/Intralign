/**
 * DTM-0028 — Export / Share-out (IC-WE-DISCLOSE E1).
 *
 * A lightweight Companion-Surface-class ACTION (spec §D) that PACKAGES the existing
 * governed outputs (project / confidence / CAF / findings / recommendations / runs /
 * UARs / plan facts) into an exportable artifact — an in-app PREVIEW plus a
 * browser-native download (Blob/anchor) and a copyable plain-text summary. It honors
 * the epistemic labels (Derived/Attested + band, plan-fact attribution), preserves
 * provenance (the CHR version/source travels into the package), and introduces NO new
 * claim. It PRESENTS, NEVER GENERATES.
 *
 * THE NO-NEW-CLAIM GUARANTEE is structural: the surface renders ONLY what
 * `buildExportPackage` produced, and the packager lifts every claim verbatim off a
 * governed DTO field (see buildExportPackage.ts + its negative tests). The preview
 * shows each claim's value + its epistemic label + its provenance (sourceObject.field
 * @ CHR ref). No computation, no scoring, no verdict, no summary that invents.
 *
 * THE NO-EXPORT-ENDPOINT DATA FINDING (flagged — see the worker report): there is NO
 * server export/report/share endpoint in the generated client. The package is assembled
 * CLIENT-SIDE from the already-fetched governed reads; we invent no server "Export
 * produced" claim (the OBS-WE event is conceptual here).
 *
 * Read-only: no generate / score / accept / reject / defer / edit / govern / reanalyze
 * control anywhere on the surface.
 */
import { useMemo } from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import Alert from "@mui/material/Alert";
import CircularProgress from "@mui/material/CircularProgress";

import { useGetProjectV1ProjectsProjectIdGet } from "../../api/generated/projects/projects";
import {
  useGetConfidenceV1ProjectsProjectIdConfidenceGet,
  useGetCafV1ProjectsProjectIdCafGet,
} from "../../api/generated/confidence/confidence";
import { useListFindingsV1ProjectsProjectIdFindingsGet } from "../../api/generated/findings/findings";
import { useListRecommendationsV1ProjectsProjectIdRecommendationsGet } from "../../api/generated/recommendations/recommendations";
import { useListAnalysisRunsV1ProjectsProjectIdAnalysisRunsGet } from "../../api/generated/analysis-runs/analysis-runs";
import {
  useListAcceptancesV1ProjectsProjectIdAcceptanceGet,
  useListPlanFactsV1ProjectsProjectIdPlanFactsGet,
} from "../../api/generated/acceptance/acceptance";

import { EpistemicLabel } from "../../components/EpistemicLabel";
import {
  buildExportPackage,
  toPlainText,
  toJson,
  type ExportClaim,
  type ExportPackage,
} from "./buildExportPackage";
import type {
  Project,
  ConfidenceState,
  CAFState,
  Finding,
  Recommendation,
  AnalysisRun,
  UserAcceptanceRecord,
  PlanFact,
} from "../../api/generated/oSLORelease1API.schemas";

export interface ExportProps {
  projectId: string;
}

/** True for a plain object DTO (not an array, string, or null). */
function asRecord<T>(v: unknown): T | null {
  return typeof v === "object" && v !== null && !Array.isArray(v) ? (v as T) : null;
}
function asArray<T>(v: unknown): T[] {
  return Array.isArray(v) ? (v.filter((x) => x && typeof x === "object") as T[]) : [];
}

/** Browser-native download — a Blob + a transient anchor; NO export/PDF library. */
function downloadBlob(filename: string, contents: string, type: string) {
  const blob = new Blob([contents], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

/** One claim row — the value lifted off a governed field + its label + provenance. */
function ClaimRow({ claim }: { claim: ExportClaim }) {
  const prov = claim.provenance;
  return (
    <Box sx={{ display: "flex", gap: 1, alignItems: "baseline", flexWrap: "wrap", mb: 0.5 }}>
      <Typography variant="body2" component="span" sx={{ fontWeight: 600 }}>
        {claim.label}:
      </Typography>
      <Typography variant="body2" component="span">
        {claim.value}
      </Typography>
      <Typography
        data-testid="export-provenance"
        variant="caption"
        color="text.secondary"
        component="span"
      >
        source: {prov.sourceObject}.{prov.sourceField}
        {prov.chrRef ? ` @ ${prov.chrRef}` : ""}
      </Typography>
    </Box>
  );
}

/** One claim group — a single source record's claims, sharing one epistemic label. */
function ClaimGroup({ group }: { group: ExportClaim[] }) {
  if (group.length === 0) return null;
  const sourceId = group[0].provenance.sourceId;
  const epistemic = group[0].epistemic;
  return (
    <Paper
      variant="outlined"
      sx={{ p: 1.5 }}
      data-testid={sourceId ? `export-item-${sourceId}` : "export-item"}
    >
      <Box sx={{ mb: 0.5 }}>
        <EpistemicLabel epistemic={epistemic} />
      </Box>
      {group.map((claim, i) => (
        <ClaimRow key={`${claim.provenance.sourceField}-${i}`} claim={claim} />
      ))}
    </Paper>
  );
}

export function Export({ projectId }: ExportProps) {
  const projectQ = useGetProjectV1ProjectsProjectIdGet(projectId);
  const confidenceQ = useGetConfidenceV1ProjectsProjectIdConfidenceGet(projectId);
  const cafQ = useGetCafV1ProjectsProjectIdCafGet(projectId);
  const findingsQ = useListFindingsV1ProjectsProjectIdFindingsGet(projectId);
  const recommendationsQ =
    useListRecommendationsV1ProjectsProjectIdRecommendationsGet(projectId);
  const runsQ = useListAnalysisRunsV1ProjectsProjectIdAnalysisRunsGet(projectId);
  const acceptancesQ = useListAcceptancesV1ProjectsProjectIdAcceptanceGet(projectId);
  const planFactsQ = useListPlanFactsV1ProjectsProjectIdPlanFactsGet(projectId);

  const loading =
    projectQ.isLoading ||
    confidenceQ.isLoading ||
    cafQ.isLoading ||
    findingsQ.isLoading ||
    recommendationsQ.isLoading ||
    runsQ.isLoading ||
    acceptancesQ.isLoading ||
    planFactsQ.isLoading;

  // Package the already-fetched governed reads — pure, no fetch, no mutation. The
  // exportedAt is the export action's own timestamp (NOT a governed claim).
  const pkg: ExportPackage | null = useMemo(() => {
    if (loading) return null;
    return buildExportPackage(
      {
        project: asRecord<Project>(projectQ.data?.data),
        confidence: asRecord<ConfidenceState>(confidenceQ.data?.data),
        caf: asRecord<CAFState>(cafQ.data?.data),
        findings: asArray<Finding>(findingsQ.data?.data),
        recommendations: asArray<Recommendation>(recommendationsQ.data?.data),
        analysisRuns: asArray<AnalysisRun>(runsQ.data?.data),
        acceptances: asArray<UserAcceptanceRecord>(acceptancesQ.data?.data),
        planFacts: asArray<PlanFact>(planFactsQ.data?.data),
      },
      {
        exportedAt: new Date().toISOString(),
        sourceContext: "Project understanding",
      },
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    loading,
    projectQ.data,
    confidenceQ.data,
    cafQ.data,
    findingsQ.data,
    recommendationsQ.data,
    runsQ.data,
    acceptancesQ.data,
    planFactsQ.data,
  ]);

  const isEmpty = !loading && pkg !== null && pkg.sections.length === 0;
  const isStale = pkg?.currency === "previous";

  const onDownloadJson = () => {
    if (!pkg) return;
    downloadBlob(
      `oslo-understanding-${pkg.projectId || "export"}.json`,
      toJson(pkg),
      "application/json",
    );
  };
  const onDownloadText = () => {
    if (!pkg) return;
    downloadBlob(
      `oslo-understanding-${pkg.projectId || "export"}.txt`,
      toPlainText(pkg),
      "text/plain",
    );
  };
  const onCopy = async () => {
    if (!pkg) return;
    const text = toPlainText(pkg);
    try {
      await navigator.clipboard?.writeText(text);
    } catch {
      // copy is best-effort; the preview already shows the same content.
    }
  };

  return (
    <Box data-testid="export-surface" sx={{ py: 1 }}>
      <Typography variant="h5" component="h2" gutterBottom data-testid="surface-title">
        Export &amp; Share
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Package a faithful, honestly-labeled snapshot of what OSLO currently understands —
        to share for outside review. It packages existing understanding only: it computes
        nothing, generates nothing, and changes nothing. Every item carries its epistemic
        label and its provenance, exactly as the surfaces show it.
      </Typography>

      {loading ? (
        <Box
          data-testid="export-loading"
          sx={{ display: "flex", alignItems: "center", gap: 1 }}
        >
          <CircularProgress size={18} />
          <Typography variant="body2" color="text.secondary">
            Assembling the snapshot…
          </Typography>
        </Box>
      ) : isEmpty || !pkg ? (
        <Paper variant="outlined" sx={{ p: 2 }}>
          <Typography data-testid="export-empty" variant="body2" color="text.secondary">
            Nothing to export here yet. Once OSLO has analysed this project and you have
            confirmed planning items, a snapshot of that understanding will be packageable
            here.
          </Typography>
        </Paper>
      ) : (
        <Stack spacing={2}>
          {isStale ? (
            <Alert
              severity="warning"
              variant="outlined"
              data-testid="export-stale-warning"
            >
              This snapshot reflects a <strong>previous analysis</strong> — it is not
              OSLO&apos;s current understanding. It is packaged as-is and labeled previous
              analysis; exporting it refreshes nothing and triggers no reanalysis.
            </Alert>
          ) : null}

          {/* The packaging affordances — browser-native, no library. */}
          <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
            <Button
              data-testid="export-download"
              variant="contained"
              onClick={onDownloadJson}
            >
              Download snapshot (JSON)
            </Button>
            <Button data-testid="export-download-text" variant="outlined" onClick={onDownloadText}>
              Download summary (text)
            </Button>
            <Button data-testid="export-copy" variant="text" onClick={onCopy}>
              Copy summary
            </Button>
          </Box>

          {/* The in-app preview — a faithful render of the packaged understanding. */}
          <Paper variant="outlined" sx={{ p: 2 }} data-testid="export-preview">
            <Typography variant="subtitle1" sx={{ fontWeight: 700 }}>
              {pkg.projectName}
            </Typography>
            <Typography variant="caption" color="text.secondary" display="block">
              Snapshot taken {pkg.exportedAt} · {pkg.sourceContext}
            </Typography>
            <Typography variant="caption" color="text.secondary" display="block">
              Analysis currency:{" "}
              {pkg.currency === "previous"
                ? "previous analysis (not current)"
                : pkg.currency === "current"
                  ? "current"
                  : "not yet analysed"}
            </Typography>
            {pkg.chrRefs.length > 0 ? (
              <Typography
                variant="caption"
                color="text.secondary"
                display="block"
                data-testid="export-provenance-summary"
              >
                Provenance (CHR versions presented): {pkg.chrRefs.join(", ")}
              </Typography>
            ) : null}

            <Stack spacing={3} sx={{ mt: 2 }}>
              {pkg.sections.map((section) => (
                <Box key={section.key} data-testid={`export-section-${section.key}`}>
                  <Typography variant="subtitle2" sx={{ mb: 1 }}>
                    {section.title}
                  </Typography>
                  <Stack spacing={1.5}>
                    {section.items.map((group, i) => (
                      <ClaimGroup key={group[0]?.provenance.sourceId ?? i} group={group} />
                    ))}
                  </Stack>
                </Box>
              ))}
            </Stack>
          </Paper>

          {/* The mandatory disclaimer (spec §I / EX-6) — always present. */}
          <Alert severity="info" variant="outlined" data-testid="export-disclaimer">
            {pkg.disclaimer}
          </Alert>
        </Stack>
      )}
    </Box>
  );
}

export default Export;
