/**
 * DTM-0028 — Export / Share-out: the packaging core (IC-WE-DISCLOSE E1).
 *
 * This is the no-new-claim guarantee made structural. `buildExportPackage` takes the
 * ALREADY-FETCHED governed DTOs (the DTM-0018 reads — project / confidence / CAF /
 * findings / recommendations / analysis-runs / acceptances / plan-facts) and packages
 * them into an `ExportPackage` whose every claim line is a `{ sourceObject,
 * sourceField, value }` provenance triple lifted VERBATIM off an input DTO field.
 *
 * Safety by construction (the negatives are the point):
 *   - Every `ExportClaim` carries `sourceObject` + `sourceField` — the exact DTO field
 *     it came from. The packager NEVER synthesises a value: it reads a field and copies
 *     it. A negative test asserts every claim's value === the value at
 *     `input[sourceObject][...sourceField]`, so an invented/summarised conclusion (one
 *     with no backing field) cannot exist.
 *   - Epistemic standing travels with each claim: Derived items carry a Derived
 *     `EpistemicStanding` (band off `DerivedEnvelope`, never upgraded, never settled);
 *     plan facts carry `attested/user` ("You confirmed", not world-truth); UARs carry
 *     `attested/user`. The packager maps, it never re-labels.
 *   - Provenance preserved: each Derived claim carries the `current_chr_ref` (the CHR
 *     version presented) as `provenance.chrRef`; the package carries the source CHR set
 *     so what-was-shown is reconstructable (OBS-WE-DISCLOSE).
 *   - NO computation: no scoring, no CAF/Confidence math, no verdict, no count that is
 *     not `array.length` of a governed read. The analysis-currency marker is read off
 *     the governed `AnalysisRun.run_status` (`superseded` ⇒ previous analysis), NOT a
 *     fabricated `is_stale` flag (none exists — see the worker report).
 *
 * It produces NO finding, NO recommendation, NO assessment, NO new understanding. It
 * packages presented understanding and nothing else (spec §C, §G, EX-1/EX-2).
 */
import type {
  Project,
  ConfidenceState,
  CAFState,
  CAFDimensionView,
  Finding,
  Recommendation,
  AnalysisRun,
  UserAcceptanceRecord,
  PlanFact,
  DerivedEnvelope,
} from "../../api/generated/oSLORelease1API.schemas";
import {
  fromDerivedEnvelope,
  type EpistemicStanding,
} from "../../components/EpistemicLabel";

/** The governed reads the export packages — all ALREADY fetched (read-only). */
export interface ExportSourceInputs {
  project?: Project | null;
  confidence?: ConfidenceState | null;
  caf?: CAFState | null;
  findings?: Finding[] | null;
  recommendations?: Recommendation[] | null;
  analysisRuns?: AnalysisRun[] | null;
  acceptances?: UserAcceptanceRecord[] | null;
  planFacts?: PlanFact[] | null;
}

/** Which governed object a claim was lifted from (for the provenance trace). */
export type ExportSourceObject =
  | "project"
  | "confidence"
  | "caf"
  | "finding"
  | "recommendation"
  | "analysisRun"
  | "acceptance"
  | "planFact";

/**
 * The provenance a claim carries into the export — the governed object + field it was
 * lifted from, plus the CHR version (lineage) when the source is Derived.
 */
export interface ExportProvenance {
  /** The governed object the value came from. */
  sourceObject: ExportSourceObject;
  /** The exact DTO field path the value was lifted from (e.g. "summary"). */
  sourceField: string;
  /** The id of the specific source record (e.g. a finding_id), when applicable. */
  sourceId?: string;
  /** The Cognition History Record version presented (Derived lineage). */
  chrRef?: string;
}

/**
 * One exported claim — a label + the value lifted VERBATIM off a governed field, its
 * epistemic standing, and its provenance. There is no claim without a `provenance`
 * pointing at a real input field — that is the no-new-claim invariant.
 */
export interface ExportClaim {
  /** A presentation label for the field (NOT a new assertion — names the field). */
  label: string;
  /** The value, copied byte-for-byte from the governed source field. */
  value: string;
  /** The item's epistemic standing (Derived band / attested-user / …). */
  epistemic: EpistemicStanding;
  /** Where this claim came from — object + field + CHR lineage. */
  provenance: ExportProvenance;
}

/** A grouped section of claims in the package (Findings, Recommendations, …). */
export interface ExportSection {
  key: string;
  title: string;
  /** A group of claims that share a source record (e.g. one finding's claims). */
  items: ExportClaim[][];
}

export type AnalysisCurrency = "current" | "previous" | "none";

export interface ExportPackage {
  /** Header metadata — all read off governed fields or the export action itself. */
  projectName: string;
  projectId: string;
  /** When the package was assembled (the export action's own timestamp — not a claim). */
  exportedAt: string;
  /** The source context the export was scoped from. */
  sourceContext: string;
  /** current / previous (stale) / none — read off the governed AnalysisRun status. */
  currency: AnalysisCurrency;
  /** The grouped claim sections. */
  sections: ExportSection[];
  /** The set of CHR refs the package reflects (reconstructability / provenance). */
  chrRefs: string[];
  /** The mandatory disclaimer (spec §I) — understanding, not project health/approval. */
  disclaimer: string;
}

/** The required disclaimer — verbatim from the spec §I / EX-6. */
export const EXPORT_DISCLAIMER =
  "This package presents OSLO's understanding — what OSLO understands and where it is " +
  "weak, reliability-qualified — and not project health, readiness, outcome probability, " +
  "approval, or certification. Viewing or sharing it changes no assessment; only " +
  "reanalysis changes an assessment.";

function asArray<T>(v: T[] | null | undefined): T[] {
  return Array.isArray(v) ? v.filter((x) => x && typeof x === "object") : [];
}

/** A Derived standing straight off the envelope — band never upgraded, never settled. */
function derivedFrom(label: DerivedEnvelope | undefined | null): EpistemicStanding {
  return fromDerivedEnvelope(label);
}

function chrRefOf(label: DerivedEnvelope | undefined | null): string | undefined {
  const ref = label?.current_chr_ref;
  return typeof ref === "string" ? ref : undefined;
}

/**
 * The analysis-currency marker — read off the GOVERNED run status (spec §J). A latest
 * run carrying `run_status: "superseded"` is, by the governed object's own status,
 * previous (stale) analysis. We invent no `is_stale` flag.
 */
export function resolveCurrency(runs: AnalysisRun[]): AnalysisCurrency {
  if (runs.length === 0) return "none";
  // The latest run is the last in append order (the reads return append-exact).
  const latest = runs[runs.length - 1];
  if (latest.run_status === "superseded") return "previous";
  if (latest.run_status === "completed") return "current";
  return "none";
}

/**
 * Package the governed reads into an export. Pure: no fetch, no mutation, no
 * computation beyond reading governed fields and `array.length`.
 */
export function buildExportPackage(
  inputs: ExportSourceInputs,
  opts: { exportedAt: string; sourceContext?: string },
): ExportPackage {
  const project = inputs.project ?? null;
  const confidence = inputs.confidence ?? null;
  const caf = inputs.caf ?? null;
  const findings = asArray(inputs.findings);
  const recommendations = asArray(inputs.recommendations);
  const analysisRuns = asArray(inputs.analysisRuns);
  const acceptances = asArray(inputs.acceptances);
  const planFacts = asArray(inputs.planFacts);

  const chrRefs = new Set<string>();
  const sections: ExportSection[] = [];

  // ── Confidence summary (Derived; banded, reliability-qualified — never bare) ──────
  if (confidence) {
    const claims: ExportClaim[] = [];
    const epi = derivedFrom(confidence.label);
    const chr = chrRefOf(confidence.label);
    if (chr) chrRefs.add(chr);
    if (typeof confidence.confidence_band === "string") {
      claims.push({
        label: "Confidence band",
        value: confidence.confidence_band,
        epistemic: epi,
        provenance: {
          sourceObject: "confidence",
          sourceField: "confidence_band",
          sourceId: confidence.confidence_state_id ?? undefined,
          chrRef: chr,
        },
      });
    }
    if (typeof confidence.reliability_qualifier === "string") {
      claims.push({
        label: "Reliability",
        value: confidence.reliability_qualifier,
        epistemic: epi,
        provenance: {
          sourceObject: "confidence",
          sourceField: "reliability_qualifier",
          sourceId: confidence.confidence_state_id ?? undefined,
          chrRef: chr,
        },
      });
    }
    for (const [i, b] of asArray(confidence.basis).entries()) {
      if (typeof b === "string")
        claims.push({
          label: "Basis",
          value: b,
          epistemic: epi,
          provenance: {
            sourceObject: "confidence",
            sourceField: `basis[${i}]`,
            sourceId: confidence.confidence_state_id ?? undefined,
            chrRef: chr,
          },
        });
    }
    if (claims.length > 0)
      sections.push({
        key: "confidence",
        title: "Outcome confidence (trust in understanding)",
        items: [claims],
      });
  }

  // ── CAF summary (qualitative — the band per dimension, never the numeric index) ───
  if (caf) {
    const chr = chrRefOf(caf.label);
    if (chr) chrRefs.add(chr);
    const dims: Array<[string, CAFDimensionView | undefined]> = [
      ["clarity", caf.clarity],
      ["alignment", caf.alignment],
      ["feasibility", caf.feasibility],
    ];
    const items: ExportClaim[][] = [];
    for (const [name, dim] of dims) {
      if (!dim) continue;
      const epi: EpistemicStanding = { standing: "derived", band: dim.band };
      const group: ExportClaim[] = [
        {
          label: `${name} band`,
          value: dim.band,
          epistemic: epi,
          provenance: { sourceObject: "caf", sourceField: `${name}.band`, chrRef: chr },
        },
        {
          label: `${name} reliability`,
          value: dim.reliability,
          epistemic: epi,
          provenance: {
            sourceObject: "caf",
            sourceField: `${name}.reliability`,
            chrRef: chr,
          },
        },
      ];
      items.push(group);
    }
    if (items.length > 0)
      sections.push({ key: "caf", title: "CAF summary (qualitative)", items });
  }

  // ── Findings (descriptive — summary + type + severity, each Derived/banded) ───────
  if (findings.length > 0) {
    const items: ExportClaim[][] = findings.map((f) => {
      const epi = derivedFrom(f.label);
      const chr = chrRefOf(f.label);
      if (chr) chrRefs.add(chr);
      const group: ExportClaim[] = [];
      if (typeof f.summary === "string")
        group.push({
          label: "Finding",
          value: f.summary,
          epistemic: epi,
          provenance: {
            sourceObject: "finding",
            sourceField: "summary",
            sourceId: f.finding_id,
            chrRef: chr,
          },
        });
      group.push({
        label: "Type",
        value: f.finding_type,
        epistemic: epi,
        provenance: {
          sourceObject: "finding",
          sourceField: "finding_type",
          sourceId: f.finding_id,
          chrRef: chr,
        },
      });
      if (typeof f.severity === "string")
        group.push({
          label: "Severity",
          value: f.severity,
          epistemic: epi,
          provenance: {
            sourceObject: "finding",
            sourceField: "severity",
            sourceId: f.finding_id,
            chrRef: chr,
          },
        });
      return group;
    });
    sections.push({ key: "findings", title: "Findings (descriptive)", items });
  }

  // ── Recommendations (advisory — title + type, each anchored to its finding) ───────
  if (recommendations.length > 0) {
    const items: ExportClaim[][] = recommendations.map((r) => {
      const epi = derivedFrom(r.label);
      const chr = chrRefOf(r.label);
      if (chr) chrRefs.add(chr);
      const group: ExportClaim[] = [];
      if (typeof r.title === "string")
        group.push({
          label: "Recommendation",
          value: r.title,
          epistemic: epi,
          provenance: {
            sourceObject: "recommendation",
            sourceField: "title",
            sourceId: r.recommendation_id,
            chrRef: chr,
          },
        });
      if (typeof r.recommendation_type === "string")
        group.push({
          label: "Type",
          value: r.recommendation_type,
          epistemic: epi,
          provenance: {
            sourceObject: "recommendation",
            sourceField: "recommendation_type",
            sourceId: r.recommendation_id,
            chrRef: chr,
          },
        });
      // The associated finding context (RP-C1 / EX-5) — the anchor, not a new claim.
      group.push({
        label: "Associated finding",
        value: r.finding_id,
        epistemic: epi,
        provenance: {
          sourceObject: "recommendation",
          sourceField: "finding_id",
          sourceId: r.recommendation_id,
          chrRef: chr,
        },
      });
      return group;
    });
    sections.push({ key: "recommendations", title: "Recommendations (advisory)", items });
  }

  // ── What you confirmed — UARs (user-attested, version-pinned) ─────────────────────
  if (acceptances.length > 0) {
    const items: ExportClaim[][] = acceptances.map((u) => {
      const epi: EpistemicStanding = { standing: "attested", source: "user" };
      const group: ExportClaim[] = [
        {
          label: "You confirmed",
          value: u.action,
          epistemic: epi,
          provenance: {
            sourceObject: "acceptance",
            sourceField: "action",
            sourceId: u.uar_id,
          },
        },
      ];
      if (typeof u.version_pin === "string")
        group.push({
          label: "Pinned to",
          value: u.version_pin,
          epistemic: epi,
          provenance: {
            sourceObject: "acceptance",
            sourceField: "version_pin",
            sourceId: u.uar_id,
          },
        });
      return group;
    });
    sections.push({ key: "acceptances", title: "What you confirmed", items });
  }

  // ── Plan facts — user-attested confirmed planning items (NOT world-truth) ─────────
  if (planFacts.length > 0) {
    const items: ExportClaim[][] = planFacts.map((p) => {
      const epi: EpistemicStanding = { standing: "attested", source: "user" };
      const group: ExportClaim[] = [
        {
          label: "You confirmed",
          value: p.proposition,
          epistemic: epi,
          provenance: {
            sourceObject: "planFact",
            sourceField: "proposition",
            sourceId: p.plan_fact_id,
          },
        },
      ];
      if (typeof p.version_pin === "string")
        group.push({
          label: "Pinned to",
          value: p.version_pin,
          epistemic: epi,
          provenance: {
            sourceObject: "planFact",
            sourceField: "version_pin",
            sourceId: p.plan_fact_id,
          },
        });
      return group;
    });
    sections.push({ key: "planFacts", title: "Planning items you attested", items });
  }

  const projectName =
    (typeof project?.title === "string" && project.title) || project?.project_id || "—";

  return {
    projectName,
    projectId: project?.project_id ?? "",
    exportedAt: opts.exportedAt,
    sourceContext: opts.sourceContext ?? "Project understanding",
    currency: resolveCurrency(analysisRuns),
    sections,
    chrRefs: Array.from(chrRefs),
    disclaimer: EXPORT_DISCLAIMER,
  };
}

/** A flat list of every claim in the package (for serialisation + tests). */
export function allClaims(pkg: ExportPackage): ExportClaim[] {
  return pkg.sections.flatMap((s) => s.items.flatMap((g) => g));
}

/**
 * Serialise the package to a copyable plain-text summary (browser-native; no library).
 * Every line is a claim value lifted off a governed field + its standing + provenance —
 * the text introduces no sentence the package didn't already carry.
 */
export function toPlainText(pkg: ExportPackage): string {
  const standingText = (e: EpistemicStanding): string =>
    e.standing === "attested"
      ? e.source === "user"
        ? "[you confirmed]"
        : `[attested: ${e.source}]`
      : `[derived${e.band ? `, ${e.band} confidence` : ""}]`;

  const lines: string[] = [];
  lines.push(`OSLO understanding export — ${pkg.projectName}`);
  lines.push(`Project: ${pkg.projectId}`);
  lines.push(`Exported: ${pkg.exportedAt}`);
  lines.push(`Source context: ${pkg.sourceContext}`);
  lines.push(
    `Analysis currency: ${
      pkg.currency === "previous"
        ? "PREVIOUS ANALYSIS (not current)"
        : pkg.currency === "current"
          ? "current"
          : "not yet analysed"
    }`,
  );
  if (pkg.chrRefs.length > 0)
    lines.push(`Provenance (CHR versions): ${pkg.chrRefs.join(", ")}`);
  lines.push("");
  for (const section of pkg.sections) {
    lines.push(`## ${section.title}`);
    for (const group of section.items) {
      for (const claim of group) {
        const prov = claim.provenance.chrRef
          ? ` (source: ${claim.provenance.sourceObject}.${claim.provenance.sourceField} @ ${claim.provenance.chrRef})`
          : ` (source: ${claim.provenance.sourceObject}.${claim.provenance.sourceField})`;
        lines.push(`- ${claim.label}: ${claim.value} ${standingText(claim.epistemic)}${prov}`);
      }
      lines.push("");
    }
  }
  lines.push("—");
  lines.push(pkg.disclaimer);
  return lines.join("\n");
}

/** Serialise to a self-describing JSON artifact (the full provenance-carrying package). */
export function toJson(pkg: ExportPackage): string {
  return JSON.stringify(pkg, null, 2);
}
