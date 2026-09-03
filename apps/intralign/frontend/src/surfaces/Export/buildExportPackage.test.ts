/**
 * DTM-0028 — Export / Share-out packaging core (IC-WE-DISCLOSE E1 + E2 negative).
 *
 * THE CRITICAL NEGATIVE (the spine — fail review if absent): the export PACKAGES
 * EXISTING UNDERSTANDING ONLY. Every exported claim must trace to a governed source
 * object/field — the package emits NO claim absent from the governed source (no
 * invented summary, no synthesized conclusion, no computed verdict). This suite
 * negative-tests that EVERY exported claim's value maps byte-for-byte to the value at
 * its `provenance.{sourceObject, sourceField}` on the INPUT DTOs.
 *
 * Plus: Derived stays Derived (banded, never settled, band never upgraded); plan facts
 * + UARs stay user-attested ("you confirmed", not world-truth); provenance (the CHR
 * version/source) travels into the package; the analysis-currency marker is read off
 * the governed run status (no fabricated `is_stale`).
 */
import { describe, it, expect } from "vitest";
import {
  buildExportPackage,
  allClaims,
  resolveCurrency,
  toPlainText,
  toJson,
  EXPORT_DISCLAIMER,
  type ExportSourceInputs,
  type ExportClaim,
} from "./buildExportPackage";
import {
  exportProjectFixture,
  exportConfidenceFixture,
  exportCafFixture,
  exportFindingsFixture,
  exportRecommendationsFixture,
  exportRunsCurrentFixture,
  exportRunsStaleFixture,
  exportAcceptancesFixture,
  exportPlanFactsFixture,
} from "./fixtures";

const FULL_INPUTS: ExportSourceInputs = {
  project: exportProjectFixture,
  confidence: exportConfidenceFixture,
  caf: exportCafFixture,
  findings: exportFindingsFixture,
  recommendations: exportRecommendationsFixture,
  analysisRuns: exportRunsCurrentFixture,
  acceptances: exportAcceptancesFixture,
  planFacts: exportPlanFactsFixture,
};

const OPTS = { exportedAt: "2026-06-26T12:00:00Z" };

/**
 * Read the value at `provenance.sourceObject[sourceId].sourceField` on the RAW inputs.
 * This is the independent oracle the no-new-claim negative checks every claim against —
 * if a claim has no backing input field, this returns `undefined` and the test fails.
 */
function resolveSourceValue(
  inputs: ExportSourceInputs,
  claim: ExportClaim,
): unknown {
  const { sourceObject, sourceField, sourceId } = claim.provenance;
  // Walk a possibly-nested field path: "basis[0]", "clarity.band", "summary".
  const readPath = (obj: unknown, path: string): unknown => {
    let cur: unknown = obj;
    for (const seg of path.split(".")) {
      const m = seg.match(/^([^[]+)(\[(\d+)\])?$/);
      if (!m || cur == null || typeof cur !== "object") return undefined;
      cur = (cur as Record<string, unknown>)[m[1]];
      if (m[3] !== undefined) {
        if (!Array.isArray(cur)) return undefined;
        cur = cur[Number(m[3])];
      }
    }
    return cur;
  };
  switch (sourceObject) {
    case "project":
      return readPath(inputs.project, sourceField);
    case "confidence":
      return readPath(inputs.confidence, sourceField);
    case "caf":
      return readPath(inputs.caf, sourceField);
    case "finding":
      return readPath(
        (inputs.findings ?? []).find((f) => f.finding_id === sourceId),
        sourceField,
      );
    case "recommendation":
      return readPath(
        (inputs.recommendations ?? []).find((r) => r.recommendation_id === sourceId),
        sourceField,
      );
    case "analysisRun":
      return readPath(
        (inputs.analysisRuns ?? []).find((a) => a.analysis_run_id === sourceId),
        sourceField,
      );
    case "acceptance":
      return readPath(
        (inputs.acceptances ?? []).find((u) => u.uar_id === sourceId),
        sourceField,
      );
    case "planFact":
      return readPath(
        (inputs.planFacts ?? []).find((p) => p.plan_fact_id === sourceId),
        sourceField,
      );
  }
}

describe("buildExportPackage — packages governed outputs with labels + provenance", () => {
  it("packages confidence, CAF, findings, recommendations, UARs, plan facts", () => {
    const pkg = buildExportPackage(FULL_INPUTS, OPTS);
    const keys = pkg.sections.map((s) => s.key);
    expect(keys).toContain("confidence");
    expect(keys).toContain("caf");
    expect(keys).toContain("findings");
    expect(keys).toContain("recommendations");
    expect(keys).toContain("acceptances");
    expect(keys).toContain("planFacts");
  });

  it("carries the project name + a timestamp + the source context (header)", () => {
    const pkg = buildExportPackage(FULL_INPUTS, OPTS);
    expect(pkg.projectName).toBe(exportProjectFixture.title);
    expect(pkg.exportedAt).toBe(OPTS.exportedAt);
    expect(pkg.sourceContext.length).toBeGreaterThan(0);
  });

  it("always carries the mandatory disclaimer (understanding, not project health/approval)", () => {
    const pkg = buildExportPackage(FULL_INPUTS, OPTS);
    expect(pkg.disclaimer).toBe(EXPORT_DISCLAIMER);
    expect(pkg.disclaimer).toMatch(/not project health/i);
    expect(pkg.disclaimer).toMatch(/only reanalysis changes an assessment/i);
  });

  it("preserves provenance — every Derived claim carries its CHR ref; the package lists the CHR set", () => {
    const pkg = buildExportPackage(FULL_INPUTS, OPTS);
    expect(pkg.chrRefs).toContain("chr-cs-001");
    expect(pkg.chrRefs).toContain("chr-f-1");
    expect(pkg.chrRefs).toContain("chr-r-1");
    for (const claim of allClaims(pkg)) {
      if (claim.epistemic.standing === "derived") {
        // a Derived claim carries the CHR lineage of the version presented
        expect(typeof claim.provenance.chrRef === "string").toBe(true);
      }
    }
  });
});

// ── THE CRITICAL NEGATIVE: no claim absent from a governed source ─────────────────
describe("buildExportPackage — NEGATIVE: packages existing understanding ONLY (no new claim)", () => {
  it("CRITICAL: every exported claim's value maps to an INPUT DTO field (no invented/summarized conclusion)", () => {
    const pkg = buildExportPackage(FULL_INPUTS, OPTS);
    const claims = allClaims(pkg);
    expect(claims.length).toBeGreaterThan(0);
    for (const claim of claims) {
      const sourceValue = resolveSourceValue(FULL_INPUTS, claim);
      // the claim's value is the governed field's value, byte-for-byte
      expect(String(sourceValue)).toBe(claim.value);
      // and the field actually exists on the source (no orphan claim)
      expect(sourceValue).not.toBeUndefined();
    }
  });

  it("emits NO claim with a non-existent source field (no synthesized verdict/summary)", () => {
    const pkg = buildExportPackage(FULL_INPUTS, OPTS);
    for (const claim of allClaims(pkg)) {
      expect(resolveSourceValue(FULL_INPUTS, claim)).not.toBeUndefined();
    }
  });

  it("computes no numeric score/verdict — the package carries no bare confidence/CAF number", () => {
    const pkg = buildExportPackage(FULL_INPUTS, OPTS);
    const text = toPlainText(pkg);
    // the numeric 0–100 confidence index is never surfaced (only the band)
    expect(text).not.toMatch(/\b66\b/);
    expect(text).not.toMatch(/\b72\b/); // a CAF dimension index
    // no percentage / project-health framing
    expect(text).not.toMatch(/%/);
    // the disclaimer legitimately DENIES "project health/readiness/probability" — that
    // denial is required (EX-6); assert the framing never appears in a CLAIM value,
    // only (if at all) in the mandatory disclaimer.
    for (const claim of allClaims(pkg)) {
      expect(claim.value).not.toMatch(/project health|readiness|probability/i);
    }
  });
});

// ── Derived stays Derived; band never upgraded; never settled ──────────────────────
describe("buildExportPackage — NEGATIVE: Derived stays Derived (not flattened to fact)", () => {
  it("every finding/recommendation/confidence/CAF claim is Derived (never attested/settled)", () => {
    const pkg = buildExportPackage(FULL_INPUTS, OPTS);
    for (const section of pkg.sections) {
      if (["confidence", "caf", "findings", "recommendations"].includes(section.key)) {
        for (const claim of section.items.flat()) {
          expect(claim.epistemic.standing).toBe("derived");
        }
      }
    }
    expect(toPlainText(pkg)).not.toMatch(/\bsettled\b/i);
  });

  it("carries the band VERBATIM — a low-band finding is NEVER upgraded to high", () => {
    const pkg = buildExportPackage(FULL_INPUTS, OPTS);
    const findings = pkg.sections.find((s) => s.key === "findings")!;
    // f-2 is band-low in the fixture; its claims must read low, not high
    const lowGroup = findings.items.find((g) =>
      g.some((c) => c.provenance.sourceId === "f-2"),
    )!;
    for (const claim of lowGroup) {
      if (claim.epistemic.standing === "derived") {
        expect(claim.epistemic.band).not.toBe("high");
        expect(claim.epistemic.band).toBe("low");
      }
    }
  });
});

// ── Plan facts + UARs stay user-attested ("you confirmed", NOT world-truth) ────────
describe("buildExportPackage — NEGATIVE: plan facts / UARs stay user-attested", () => {
  it("every plan-fact + UAR claim is attested/user (not evidence, not oslo, not derived)", () => {
    const pkg = buildExportPackage(FULL_INPUTS, OPTS);
    for (const key of ["planFacts", "acceptances"]) {
      const section = pkg.sections.find((s) => s.key === key)!;
      for (const claim of section.items.flat()) {
        expect(claim.epistemic.standing).toBe("attested");
        if (claim.epistemic.standing === "attested") {
          expect(claim.epistemic.source).toBe("user");
        }
      }
    }
    const text = toPlainText(pkg);
    expect(text).not.toMatch(/world.?truth/i);
    expect(text).toMatch(/you confirmed/i);
  });
});

// ── The analysis-currency marker is read off the governed run status ───────────────
describe("buildExportPackage — analysis currency (read off governed status, not fabricated)", () => {
  it("marks 'current' when the latest run is completed", () => {
    const pkg = buildExportPackage(FULL_INPUTS, OPTS);
    expect(pkg.currency).toBe("current");
  });

  it("marks 'previous' (stale) when the latest run is governed-superseded", () => {
    const pkg = buildExportPackage(
      { ...FULL_INPUTS, analysisRuns: exportRunsStaleFixture },
      OPTS,
    );
    expect(pkg.currency).toBe("previous");
    expect(toPlainText(pkg)).toMatch(/previous analysis/i);
  });

  it("resolveCurrency reads the latest run's governed status", () => {
    expect(resolveCurrency(exportRunsCurrentFixture)).toBe("current");
    expect(resolveCurrency(exportRunsStaleFixture)).toBe("previous");
    expect(resolveCurrency([])).toBe("none");
  });
});

// ── Serialisation (browser-native; no library) is faithful and read-only ───────────
describe("buildExportPackage — serialisation is faithful (no new content, read-only)", () => {
  it("JSON round-trips the full provenance-carrying package", () => {
    const pkg = buildExportPackage(FULL_INPUTS, OPTS);
    const parsed = JSON.parse(toJson(pkg));
    expect(parsed.disclaimer).toBe(EXPORT_DISCLAIMER);
    expect(parsed.sections.length).toBe(pkg.sections.length);
  });

  it("does NOT mutate the governed input DTOs (record-exact, read-only)", () => {
    const before = JSON.parse(JSON.stringify(FULL_INPUTS));
    buildExportPackage(FULL_INPUTS, OPTS);
    expect(FULL_INPUTS).toEqual(before);
  });

  it("empty inputs produce a package with no sections (but still a disclaimer)", () => {
    const pkg = buildExportPackage({}, OPTS);
    expect(pkg.sections.length).toBe(0);
    expect(pkg.disclaimer).toBe(EXPORT_DISCLAIMER);
    expect(pkg.currency).toBe("none");
  });
});
