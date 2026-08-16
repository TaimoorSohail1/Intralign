import type {
  CollaborationRollUpProjection,
  GroundingNodeState,
  OverviewSnapshot,
  ProjectOutcomeSummary,
} from "@/lib/server/oslo-api";

export interface YourOutcomeProjection {
  project_id: string;
  project_title: string;
  primary_outcome: ProjectOutcomeSummary | null;
  visible_secondary_outcomes: ProjectOutcomeSummary[];
  held_outcome_count: number;
  disclosure_eligible: boolean;
  intent_counts: {
    goals: number;
    success_criteria: number;
    kpis: number;
  };
  integrity: OverviewSnapshot["assessment"]["integrity"];
  trend: "strengthened" | "weakened" | "unchanged";
  grounding: {
    grounded: number;
    total: number;
  };
  freshness: OverviewSnapshot["freshness"] | null;
  unseen_changes: Array<{
    id: string;
    summary: string;
    created_at: string;
    href: string;
  }>;
  needs_you: Array<{
    issue_id: string;
    title: string;
    detail: string;
    severity: string | null;
    pillar: string;
    state: GroundingNodeState;
    exposure_rank: number;
    href: string;
  }>;
  in_motion: Array<{
    reviewer_name: string;
    issue_id: string;
    issue_title: string;
    detail: string;
    state: string;
    href: string;
  }>;
  actor_role: string;
}

function isIdentifier(value: string) {
  return /^(?:[A-Z]{1,5}-?\d+|\d+(?:\.\d+){1,4})$/i.test(value.trim());
}

function bestTextCell(section: { columns: string[] }, row: string[]) {
  const preferred = section.columns.findIndex((column) =>
    /statement|description|requirement|constraint|deliverable|task|milestone|resource|name|title|outcome|goal/i.test(
      column,
    ),
  );
  if (preferred >= 0 && row[preferred]?.trim()) return preferred;

  const candidates = row
    .map((value, index) => ({ value: value.trim(), index }))
    .filter(({ value }) => value && !isIdentifier(value) && !/^\d{4}-\d{2}-\d{2}$/.test(value));
  if (!candidates.length) return Math.max(0, row.findIndex(Boolean));
  return candidates.sort((left, right) => right.value.length - left.value.length)[0].index;
}

function normalizedClaimKey(value: string) {
  return value
    .normalize("NFKC")
    .toLocaleLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, " ")
    .trim();
}

function sectionClaims(section: {
  body: string;
  bullets: string[];
  columns: string[];
  rows: string[][];
}) {
  const populatedRows = section.rows.filter((row) => row.some((cell) => cell.trim()));
  if (populatedRows.length) {
    return populatedRows
      .map((row) => row[bestTextCell(section, row)]?.trim() ?? "")
      .filter(Boolean);
  }
  return [section.body.trim(), ...section.bullets.map((item) => item.trim())].filter(Boolean);
}

type IntentGroup = "purpose" | "outcomes" | "goals" | "success_criteria" | "kpis";
type IntentSection = NonNullable<
  OverviewSnapshot["artifacts"][number]["content"]
>["sections"][number];

const intentFallbackGroups: IntentGroup[] = [
  "purpose",
  "outcomes",
  "goals",
  "success_criteria",
  "kpis",
];

function intentGroup(
  section: IntentSection,
  index: number,
): IntentGroup {
  const source = `${section.heading} ${section.body}`.toLowerCase();
  if (/kpi|metric|tracked|measure/.test(source)) return "kpis";
  if (/success|criterion|criteria|target|acceptance/.test(source)) return "success_criteria";
  if (/goal|aim|objective/.test(source)) return "goals";
  if (/outcome|end.state|result|business case|benefit|value|impact/.test(source)) return "outcomes";
  if (/purpose|intent|why|summary/.test(source)) return "purpose";
  return intentFallbackGroups[Math.min(index, intentFallbackGroups.length - 1)];
}

function countIntentClaims(snapshot: OverviewSnapshot, group: IntentGroup) {
  const intent = snapshot.artifacts.find((artifact) => artifact.artifact_type === "intent");
  const claims = (intent?.content?.sections ?? [])
    // IC-WE-DISCLOSE: keep the read-only dashboard totals aligned with the
    // governed Intent grouping used by the editable artifact surface.
    .filter((section, index) => intentGroup(section, index) === group)
    .flatMap(sectionClaims);
  return new Set(claims.map(normalizedClaimKey).filter(Boolean)).size;
}

function unseenChangeSummary(
  notification: NonNullable<OverviewSnapshot["read_moved_notifications"]>[number],
) {
  if (notification.settled_causes[0]) return notification.settled_causes[0];
  if (notification.previous_band && notification.current_band) {
    if (notification.previous_band === notification.current_band) {
      return `Outcome Integrity remains ${notification.current_band}`;
    }
    return `Outcome Integrity moved from ${notification.previous_band} to ${notification.current_band}`;
  }
  return "The current read changed after new grounded evidence";
}

export function buildYourOutcomeProjection({
  snapshot,
  outcomes,
  rollUp,
}: {
  snapshot: OverviewSnapshot;
  outcomes: ProjectOutcomeSummary[];
  rollUp: CollaborationRollUpProjection;
}): YourOutcomeProjection {
  const activeOutcomes = outcomes.filter((outcome) => outcome.status === "active");
  const primaryOutcome =
    activeOutcomes.find((outcome) => outcome.is_primary) ?? activeOutcomes[0] ?? null;
  const disclosureEligible = Boolean(
    snapshot.first_run?.ever_unlocked &&
      snapshot.first_run.grounding_act_count >= snapshot.first_run.unlock_threshold,
  );
  const secondaryOutcomes = activeOutcomes.filter(
    (outcome) => outcome.id !== primaryOutcome?.id,
  );
  const visibleSecondaryOutcomes = disclosureEligible ? secondaryOutcomes : [];
  const detectedOutcomeCount = countIntentClaims(snapshot, "outcomes");
  const heldOutcomeCount = disclosureEligible
    ? Math.max(0, detectedOutcomeCount - Number(Boolean(primaryOutcome)) - visibleSecondaryOutcomes.length)
    : 0;
  const totalGrounding = Object.values(rollUp.rests_on).reduce(
    (total, count) => total + count,
    0,
  );
  const issuesById = new Map(
    snapshot.assessment.issues.map((issue) => [issue.id, issue]),
  );

  return {
    project_id: snapshot.project_id,
    project_title: snapshot.project_title || "Project",
    primary_outcome: primaryOutcome,
    visible_secondary_outcomes: visibleSecondaryOutcomes,
    held_outcome_count: heldOutcomeCount,
    disclosure_eligible: disclosureEligible,
    intent_counts: {
      goals: countIntentClaims(snapshot, "goals"),
      success_criteria: countIntentClaims(snapshot, "success_criteria"),
      kpis: countIntentClaims(snapshot, "kpis"),
    },
    integrity: snapshot.assessment.integrity,
    trend: rollUp.trend,
    grounding: {
      grounded: rollUp.rests_on.grounded,
      total: totalGrounding,
    },
    freshness: snapshot.freshness ?? null,
    unseen_changes: (snapshot.read_moved_notifications ?? [])
      .filter((notification) => !notification.seen_at)
      .map((notification) => ({
        id: notification.id,
        summary: unseenChangeSummary(notification),
        created_at: notification.created_at,
        href: `/projects/${snapshot.project_id}/history?focus=since-last-looked`,
      })),
    needs_you: [...rollUp.decision_queue]
      .sort((left, right) => right.exposure_rank - left.exposure_rank)
      .map((item) => {
        const issue = issuesById.get(item.issue_id);
        return {
          issue_id: item.issue_id,
          title: item.title,
          detail:
            item.detail || issue?.why || `${item.pillar} · ${item.artifact_type.replaceAll("_", " ")}`,
          // IC-WB-EVAL / IC-WE-DISCLOSE: severity is projected, never re-scored here.
          severity: issue?.severity ?? null,
          pillar: item.pillar,
          state: item.state,
          exposure_rank: item.exposure_rank,
          href: item.href,
        };
      }),
    in_motion: rollUp.who_is_grounding_what.map((item) => {
      const issue = issuesById.get(item.issue_id);
      return {
        reviewer_name: item.reviewer_name,
        issue_id: item.issue_id,
        issue_title: issue?.title ?? item.issue_id,
        detail: issue?.why ?? "",
        state: item.state,
        href: item.href,
      };
    }),
    actor_role: rollUp.actor_role,
  };
}
