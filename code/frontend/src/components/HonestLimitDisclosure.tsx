/**
 * HonestLimitDisclosure — DL-048 UP-4 honest-limit disclosure (IC-WE-DISCLOSE).
 *
 * When a Fast/Deep run is scope- or budget-limited (Tier-1 envelope exceeded → partial
 * orientation; DL-048 degradation), Disclose MUST present a TRUTHFUL partial-analysis
 * disclosure: reduced coverage shown WITH the reason. This is an epistemic-safety
 * obligation FIRST (CONTEXT.md "honest-limit disclosure") — it must never imply a
 * full/final analysis.
 *
 * Alongside-not-instead (the contracted negative): the commodity Upgrade-Prompt
 * affordance (MON-04 UP-4) renders on this SAME surface, AFTER and beside the honest
 * disclosure — never in place of it. The disclosure is mandatory whenever `limited`;
 * the upgrade is optional commodity. By construction the disclosure always renders
 * first and the upgrade can never replace it.
 *
 * DATA DEPENDENCY (flagged): there is no scope/budget-limit DTO in the DTM-0018 REST
 * surface — the DL-048 constraint-detection signals (cap-hit, envelope-exceeded, budget
 * gate) are not yet exposed over REST. This component consumes a non-canonical
 * presentation `HonestLimit` shape and invents no DTO. See honestLimit.fixtures.ts.
 */
import Alert from "@mui/material/Alert";
import AlertTitle from "@mui/material/AlertTitle";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";

/** The commodity Upgrade-Prompt (UP-4) — presentation only; copy is commodity. */
export interface HonestLimitUpgrade {
  message: string;
  cta_label: string;
  /** Optional handler; absent in read-only presentation contexts. */
  onUpgrade?: () => void;
}

/**
 * Non-canonical presentation shape for a scope/budget-limited run. NOT a DTO — the
 * DL-048 limit signals are not yet exposed over REST (flagged dependency). When
 * `limited` is false the component renders nothing.
 */
export interface HonestLimit {
  limited: boolean;
  /** Why coverage is reduced — shown verbatim (the epistemic-safety obligation). */
  reason?: string;
  /** The reduced-coverage detail. */
  coverage_note?: string;
  /** The commodity upgrade prompt; alongside, never instead-of. Optional. */
  upgrade?: HonestLimitUpgrade;
}

export interface HonestLimitDisclosureProps {
  limit: HonestLimit;
}

export function HonestLimitDisclosure({ limit }: HonestLimitDisclosureProps) {
  // Not limited → present NOTHING (never fabricate a partial state).
  if (!limit.limited) return null;

  return (
    <Alert
      severity="warning"
      icon={false}
      data-testid="honest-limit"
      sx={{ my: 2 }}
    >
      {/* ── The honest disclosure — ALWAYS first, always present when limited. ── */}
      <Box data-testid="honest-limit-disclosure">
        <AlertTitle sx={{ fontWeight: 700 }}>Partial analysis</AlertTitle>
        <Typography variant="body2" data-testid="honest-limit-reason" sx={{ mb: 1 }}>
          {limit.reason ??
            "This is a partial analysis — the run was limited and did not cover the full project."}
        </Typography>
        {limit.coverage_note ? (
          <Typography
            variant="body2"
            color="text.secondary"
            data-testid="honest-limit-coverage"
          >
            {limit.coverage_note}
          </Typography>
        ) : (
          <Typography
            variant="body2"
            color="text.secondary"
            data-testid="honest-limit-coverage"
          >
            Coverage was reduced for this run — what is shown reflects only the analyzed
            portion, not the whole project.
          </Typography>
        )}
      </Box>

      {/* ── The commodity Upgrade-Prompt — ALONGSIDE the disclosure, never instead. ── */}
      {limit.upgrade ? (
        <Box
          data-testid="honest-limit-upgrade"
          sx={{
            mt: 2,
            pt: 1.5,
            borderTop: "1px solid",
            borderColor: "divider",
            display: "flex",
            flexDirection: { xs: "column", sm: "row" },
            alignItems: { xs: "flex-start", sm: "center" },
            gap: 1,
          }}
        >
          <Typography variant="body2" sx={{ flex: 1 }}>
            {limit.upgrade.message}
          </Typography>
          <Button
            size="small"
            variant="outlined"
            color="inherit"
            onClick={limit.upgrade.onUpgrade}
            data-testid="honest-limit-upgrade-cta"
          >
            {limit.upgrade.cta_label}
          </Button>
        </Box>
      ) : null}
    </Alert>
  );
}

export default HonestLimitDisclosure;
