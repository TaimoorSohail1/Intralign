import type { OverviewSnapshot } from "@/lib/server/oslo-api";

export const projectArtifactOrder = [
  "intent",
  "context",
  "scope",
  "requirements",
  "work_breakdown",
  "schedule",
  "resources",
] as const;

export type ProjectArtifactType = (typeof projectArtifactOrder)[number];

export interface ArtifactProvenance {
  artifactType: ProjectArtifactType;
  grounded: number;
  inferred: number;
  total: number;
  verifyFirst: boolean;
}

export interface InferenceAssumption {
  id: string;
  artifactType: ProjectArtifactType;
  text: string;
  issueId: string | null;
  issueTitle: string | null;
  createdAt: string;
  loadBearing: boolean;
  state: "confirmed" | "inferred" | "conflicting";
}

export interface ProjectProvenance {
  artifacts: ArtifactProvenance[];
  assumptions: InferenceAssumption[];
  groundedClaims: number;
  inferredClaims: number;
  totalClaims: number;
  loadBearingInferences: number;
  structure: {
    unconfirmedDependencies: number;
    unownedParties: number;
    untraceableNumbers: number;
  };
  thisWeek: {
    userGrounded: number;
    osloInferred: number;
  };
}

const ownerPattern = /\b(owner|ownership|accountable|responsib(?:le|ility)|approver)\b/i;
const dependencyPattern =
  /\b(dependenc(?:y|ies)|depends?|confirm(?:ed|ation)?|unresolved|undefined|missing)\b/i;
const numberPattern = /\b\d+(?:[.,]\d+)?\b/;

function isArtifactType(value: string): value is ProjectArtifactType {
  return projectArtifactOrder.includes(value as ProjectArtifactType);
}

function isUserConfirmed(basis: string) {
  return /\b(attested|confirmed(?:_by_user)?|user confirmed)\b/i.test(basis);
}

function artifactClaimCounts(
  artifact: OverviewSnapshot["artifacts"][number] | undefined,
) {
  if (!artifact?.content?.sections?.length) {
    if (!artifact) return { grounded: 0, inferred: 0 };
    const grounded =
      artifact.evidence_refs.length > 0 || isUserConfirmed(artifact.basis) ? 1 : 0;
    return { grounded, inferred: grounded ? 0 : 1 };
  }

  let grounded = 0;
  let inferred = 0;
  for (const section of artifact.content.sections) {
    if (section.rows.length) {
      section.rows.forEach((_row, index) => {
        const state = section.row_states?.[index];
        const evidence = section.row_evidence_refs?.[index] ?? [];
        if (
          (state === "confirmed" || state === "conflicting") &&
          evidence.length
        ) {
          grounded += 1;
        }
        else inferred += 1;
      });
      continue;
    }
    const claimCount = section.bullets.length + (section.body.trim() ? 1 : 0);
    if ((section.evidence_refs?.length ?? 0) > 0) grounded += claimCount;
    else inferred += claimCount;
  }
  return { grounded, inferred };
}

export function buildProjectProvenance(snapshot: OverviewSnapshot): ProjectProvenance {
  if (snapshot.provenance?.schema_version === 1) {
    const canonical = snapshot.provenance;
    const artifacts = projectArtifactOrder.map((artifactType) => {
      const item = canonical.artifacts.find(
        (candidate) => candidate.artifact_type === artifactType,
      );
      return {
        artifactType,
        grounded: item?.grounded ?? 0,
        inferred: item?.inferred ?? 0,
        total: item?.total ?? 0,
        verifyFirst: item?.verify_first ?? false,
      };
    });
    const assumptions = canonical.assumptions
      .filter((item) => isArtifactType(item.artifact_type))
      .map((item) => ({
        id: item.id,
        artifactType: item.artifact_type as ProjectArtifactType,
        text: item.text,
        issueId: item.issue_id,
        issueTitle: item.issue_title,
        createdAt: snapshot.published_at,
        loadBearing: item.load_bearing,
        state: item.state,
      }));
    return {
      artifacts,
      assumptions,
      groundedClaims: canonical.grounded_claims,
      inferredClaims: canonical.inferred_claims,
      totalClaims: canonical.total_claims,
      loadBearingInferences: canonical.load_bearing_inferences,
      structure: {
        unconfirmedDependencies: canonical.structure.unconfirmed_dependencies,
        unownedParties: canonical.structure.unowned_parties,
        untraceableNumbers: canonical.structure.untraceable_numbers,
      },
      thisWeek: {
        userGrounded: canonical.this_week.user_grounded,
        osloInferred: canonical.this_week.oslo_inferred,
      },
    };
  }

  const openIssues = snapshot.assessment.issues.filter(
    (issue) => issue.status !== "resolved" && isArtifactType(issue.artifact_type),
  );

  const artifacts = projectArtifactOrder.map((artifactType) => {
    const artifact = snapshot.artifacts.find(
      (candidate) => candidate.artifact_type === artifactType,
    );
    const { grounded, inferred } = artifactClaimCounts(artifact);
    const total = grounded + inferred;
    return {
      artifactType,
      grounded,
      inferred,
      total,
      verifyFirst:
        total > 0 &&
        inferred > grounded &&
        artifact?.reliability.toLowerCase() !== "low",
    };
  });

  const assumptions = snapshot.artifacts
    .filter((artifact) => isArtifactType(artifact.artifact_type))
    .flatMap((artifact) =>
      (artifact.assumptions ?? []).map((assumption) => {
        const relatedIssue = openIssues.find(
          (issue) =>
            issue.artifact_type === artifact.artifact_type &&
            `${issue.title} ${issue.why}`.toLowerCase().includes(
              assumption.statement.toLowerCase().slice(0, 32),
            ),
        );
        return {
          id: assumption.id,
          artifactType: artifact.artifact_type as ProjectArtifactType,
          text: assumption.statement,
          issueId: relatedIssue?.id ?? null,
          issueTitle: relatedIssue?.title ?? null,
          createdAt: snapshot.published_at,
          loadBearing: assumption.load_bearing,
          state: assumption.state,
        };
      }),
    )
    .sort((left, right) => {
      if (left.loadBearing !== right.loadBearing) return left.loadBearing ? -1 : 1;
      return left.text.localeCompare(right.text);
    });

  const groundedClaims = artifacts.reduce((total, artifact) => total + artifact.grounded, 0);
  const inferredClaims = artifacts.reduce((total, artifact) => total + artifact.inferred, 0);
  const loadBearingInferences = assumptions.filter(
    (assumption) => assumption.loadBearing && assumption.state !== "confirmed",
  ).length;

  const issueText = (issue: (typeof openIssues)[number]) =>
    `${issue.title} ${issue.why} ${issue.clarification ?? ""}`;

  return {
    artifacts,
    assumptions,
    groundedClaims,
    inferredClaims,
    totalClaims: groundedClaims + inferredClaims,
    loadBearingInferences,
    structure: {
      unconfirmedDependencies: openIssues.filter((issue) =>
        dependencyPattern.test(issueText(issue)),
      ).length,
      unownedParties: openIssues.filter((issue) => ownerPattern.test(issueText(issue)))
        .length,
      untraceableNumbers: openIssues.filter(
        (issue) =>
          numberPattern.test(issueText(issue)) && issue.evidence_refs.length === 0,
      ).length,
    },
    thisWeek: {
      userGrounded: snapshot.artifacts.filter((artifact) =>
        isUserConfirmed(artifact.basis),
      ).length,
      osloInferred: inferredClaims,
    },
  };
}
