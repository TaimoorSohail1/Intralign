export function currentReadSummary(
  summary: string,
  openIssueCount: number,
  projectTitle?: string | null,
) {
  const openLabel = `${openIssueCount} open ${openIssueCount === 1 ? "finding" : "findings"}`;
  let visibleSummary = summary.replace(
    /\b\d+\s+open\s+(?:findings?|issues?|points?)\b/gi,
    openLabel,
  );

  const title = projectTitle?.trim();
  const governedDetail = visibleSummary.match(
    /\bAt the (?:orientation|expanded|validated) stage,[\s\S]*$/i,
  );
  if (title && governedDetail) {
    visibleSummary = `${title}. ${governedDetail[0]}`;
  }

  return visibleSummary;
}
