/**
 * MRI Experience categories (Missing · Risky · Incomplete) — a PRESENTATION LENS
 * over the canonical 7-type Finding taxonomy (MRI Experience Spec §E / §F). This
 * adds NO new ontology and creates NO finding: it groups existing findings by the
 * kind of weakness they represent. A finding maps to exactly one category.
 *
 *   Missing    ← missing_information, coverage_gap
 *   Risky      ← assumption, inference, conflict, constraint
 *   Incomplete ← ambiguity
 */
import type { Finding, FindingType, Severity } from "../../api/generated/oSLORelease1API.schemas";

export type MriCategory = "missing" | "risky" | "incomplete";

export const MRI_CATEGORY_LABEL: Record<MriCategory, string> = {
  missing: "Missing",
  risky: "Risky",
  incomplete: "Incomplete",
};

export const MRI_CATEGORY_BLURB: Record<MriCategory, string> = {
  missing: "Understanding is absent — needed information or coverage isn't there.",
  risky: "Understanding is present but risky — unsupported or conflicting.",
  incomplete: "Understanding is present but unclear or partial.",
};

const TYPE_TO_CATEGORY: Record<FindingType, MriCategory> = {
  missing_information: "missing",
  coverage_gap: "missing",
  assumption: "risky",
  inference: "risky",
  conflict: "risky",
  constraint: "risky",
  ambiguity: "incomplete",
};

export const MRI_CATEGORY_ORDER: MriCategory[] = ["missing", "risky", "incomplete"];

export function categoryOf(finding: Finding): MriCategory {
  return TYPE_TO_CATEGORY[finding.finding_type] ?? "incomplete";
}

/** Qualitative severity ordering (critical → moderate → warning). NO numbers. */
const SEVERITY_ORDER: Record<Severity, number> = {
  critical: 0,
  moderate: 1,
  warning: 2,
};

export function severityRank(s: Severity | null | undefined): number {
  return s ? SEVERITY_ORDER[s] : 3;
}

/** Group findings by MRI category, each list severity-ordered (qualitative). */
export function groupByCategory(
  findings: Finding[],
): Record<MriCategory, Finding[]> {
  const out: Record<MriCategory, Finding[]> = {
    missing: [],
    risky: [],
    incomplete: [],
  };
  for (const f of findings) out[categoryOf(f)].push(f);
  for (const cat of MRI_CATEGORY_ORDER) {
    out[cat].sort((a, b) => severityRank(a.severity) - severityRank(b.severity));
  }
  return out;
}

/**
 * A finding is "open / awaiting review" (a blocking understanding dependency)
 * when it is not yet resolved — i.e. NOT closed or superseded. Presentation only;
 * MRI never changes a finding's lifecycle state.
 */
export function isAwaitingReview(finding: Finding): boolean {
  const s = finding.status;
  return s !== "closed" && s !== "superseded";
}
