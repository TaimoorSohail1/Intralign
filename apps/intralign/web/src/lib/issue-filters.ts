export const issueArtifacts = [
  "intent",
  "context",
  "scope",
  "requirements",
  "work_breakdown",
  "schedule",
  "resources",
] as const;

export const issueDimensions = ["clarity", "alignment", "feasibility"] as const;
export const issueSeverities = ["Critical", "Moderate", "Warning"] as const;
export const issueStatuses = [
  "active",
  "open",
  "addressed",
  "resolved",
  "all",
] as const;

export interface IssueFilters {
  artifact: (typeof issueArtifacts)[number] | null;
  dimension: (typeof issueDimensions)[number] | null;
  severity: (typeof issueSeverities)[number] | null;
  status: (typeof issueStatuses)[number];
}

export const defaultIssueFilters: IssueFilters = {
  artifact: null,
  dimension: null,
  severity: null,
  status: "active",
};

type SearchInput = Record<string, string | string[] | undefined>;

function firstValue(value: string | string[] | undefined) {
  return Array.isArray(value) ? value[0] : value;
}

function includes<T extends string>(values: readonly T[], value?: string): value is T {
  return Boolean(value && values.includes(value as T));
}

export function parseIssueFilters(input: SearchInput): IssueFilters {
  const artifact = firstValue(input.artifact);
  const dimension = firstValue(input.dimension)?.toLowerCase();
  const severity = firstValue(input.severity);
  const status = firstValue(input.status)?.toLowerCase();

  return {
    artifact: includes(issueArtifacts, artifact) ? artifact : null,
    dimension: includes(issueDimensions, dimension) ? dimension : null,
    severity: includes(issueSeverities, severity) ? severity : null,
    status: includes(issueStatuses, status) ? status : "active",
  };
}

export function issueFiltersToSearchParams(filters: IssueFilters) {
  const params = new URLSearchParams();
  if (filters.artifact) params.set("artifact", filters.artifact);
  if (filters.dimension) params.set("dimension", filters.dimension);
  if (filters.severity) params.set("severity", filters.severity);
  if (filters.status !== "active") params.set("status", filters.status);
  return params;
}
