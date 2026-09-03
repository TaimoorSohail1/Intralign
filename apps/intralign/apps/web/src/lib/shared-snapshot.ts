export interface SharedIssue {
  id: string;
  title: string;
  severity: string;
  dimension: string;
  status?: string;
}

export function openSharedIssues(issues: SharedIssue[] | undefined) {
  return (issues ?? []).filter((issue) => issue.status !== "resolved");
}
