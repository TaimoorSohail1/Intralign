/**
 * DTM-0027 — History / Timeline (IC-WE-DISCLOSE E1).
 *
 * Reconstructs THE TRAIL — what OSLO said when (CHR, via the analysis runs that
 * appended them) + what the user confirmed (UAR + plan facts) — RECORD-EXACT, the
 * "why did it change" narrative. Presentation is APPEND-ONLY (never destructively
 * edited/reordered; superseded entries STAY visible). Plan facts display as
 * USER-ATTESTED. Read-only.
 *
 * THE CRITICAL NEGATIVES (the spine of this slice — fail review if absent):
 *   - PRESENTS, NEVER GENERATES: no edit/accept/generate/delete/rollback control.
 *   - HISTORY NOT EDITABLE/MUTABLE: no mutation affordance anywhere.
 *   - APPEND-EXACT ordering: the per-source record order is preserved (no
 *     destructive reorder); supersession is ADDITIVE (the superseded entry remains).
 *   - PLAN-FACT user-attested: rendered as "You confirmed" (not world-truth, not
 *     evidence-attested, not OSLO-attested).
 *   - CHR Derived: every CHR/run entry reads as Derived, NEVER settled.
 *
 * The three reads are mocked with fixture DTOs:
 *   - `useListHistory…`       (the first-class CHR trail, DTM-0038 — Derived)
 *   - `useListAcceptances…`   (UARs — user-attested, version-pinned)
 *   - `useListPlanFacts…`     (plan facts — user-attested, NOT world-truth)
 */
import { describe, it, expect, vi, beforeEach } from "vitest";
import { screen, within } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { renderTimeline } from "./testHarness";
import {
  analysisRunsFixture,
  acceptancesFixture,
  planFactsFixture,
  supersededRun,
  failedRun,
  currentRun,
  acceptUar,
  planFactOne,
  PROJECT_ID,
} from "./fixtures";

// ── Mock the three DTM-0018 reads (the surface consumes, never re-implements) ─────
const runsState = {
  data: { data: analysisRunsFixture },
  isLoading: false,
  isError: false,
  error: null as unknown,
};
const acceptancesState = {
  data: { data: acceptancesFixture },
  isLoading: false,
  isError: false,
  error: null as unknown,
};
const planFactsState = {
  data: { data: planFactsFixture },
  isLoading: false,
  isError: false,
  error: null as unknown,
};

vi.mock("../../api/generated/history/history", () => ({
  useListHistoryV1ProjectsProjectIdHistoryGet: () => runsState,
}));
vi.mock("../../api/generated/acceptance/acceptance", () => ({
  useListAcceptancesV1ProjectsProjectIdAcceptanceGet: () => acceptancesState,
  useListPlanFactsV1ProjectsProjectIdPlanFactsGet: () => planFactsState,
}));

// Imported AFTER the mocks are declared (vi.mock is hoisted).
import { Timeline } from "./Timeline";

function mount(projectId: string = PROJECT_ID) {
  return renderTimeline(<Timeline projectId={projectId} />, projectId);
}

beforeEach(() => {
  runsState.isLoading = false;
  runsState.data = { data: analysisRunsFixture };
  acceptancesState.isLoading = false;
  acceptancesState.data = { data: acceptancesFixture };
  planFactsState.isLoading = false;
  planFactsState.data = { data: planFactsFixture };
});

// ── POSITIVE: reconstructs the CHR + UAR + plan-fact trail ───────────────────────
describe("Timeline — reconstructs the trail (CHR + UAR + plan facts)", () => {
  it("renders the surface with a title", async () => {
    await mount();
    expect(screen.getByTestId("timeline")).toBeInTheDocument();
    expect(screen.getByTestId("surface-title")).toBeInTheDocument();
  });

  it("renders one CHR trail entry per analysis run (current + past)", async () => {
    await mount();
    const surface = screen.getByTestId("timeline");
    const chr = within(surface).getAllByTestId("chr-entry");
    expect(chr.length).toBe(analysisRunsFixture.length);
    // current + past are BOTH present
    expect(
      chr.some((e) => e.getAttribute("data-chr-id") === currentRun.chr_id),
    ).toBe(true);
    expect(
      chr.some((e) => e.getAttribute("data-chr-id") === supersededRun.chr_id),
    ).toBe(true);
  });

  it("labels every CHR entry Derived (a projection — never settled)", async () => {
    await mount();
    for (const entry of screen.getAllByTestId("chr-entry")) {
      const label = within(entry).getByTestId("epistemic-label");
      expect(label).toHaveAttribute("data-standing", "derived");
    }
  });

  it("marks the current understanding distinctly from prior entries", async () => {
    await mount();
    const current = screen
      .getAllByTestId("chr-entry")
      .find((e) => e.getAttribute("data-chr-id") === currentRun.chr_id)!;
    expect(current).toHaveAttribute("data-current", "true");
  });

  it("renders one UAR entry per acceptance record, user-attested", async () => {
    await mount();
    const uars = screen.getAllByTestId("uar-entry");
    expect(uars.length).toBe(acceptancesFixture.length);
    const one = uars.find((u) => u.getAttribute("data-uar-id") === acceptUar.uar_id)!;
    const label = within(one).getByTestId("epistemic-label");
    expect(label).toHaveAttribute("data-standing", "attested");
    expect(label).toHaveAttribute("data-source", "user");
  });

  it("shows the UAR version-pin (the exact CHR accepted)", async () => {
    await mount();
    const one = screen
      .getAllByTestId("uar-entry")
      .find((u) => u.getAttribute("data-uar-id") === acceptUar.uar_id)!;
    expect(within(one).getByText(new RegExp(acceptUar.version_pin))).toBeInTheDocument();
  });

  it("renders one plan-fact entry per plan fact, user-attested ('You confirmed')", async () => {
    await mount();
    const facts = screen.getAllByTestId("plan-fact-entry");
    expect(facts.length).toBe(planFactsFixture.length);
    const one = facts.find(
      (f) => f.getAttribute("data-plan-fact-id") === planFactOne.plan_fact_id,
    )!;
    const label = within(one).getByTestId("epistemic-label");
    expect(label).toHaveAttribute("data-standing", "attested");
    expect(label).toHaveAttribute("data-source", "user");
    // the user-attested copy, not world-truth
    expect(within(one).getByText(/you confirmed/i)).toBeInTheDocument();
    // the verbatim proposition is rendered (record-exact)
    expect(within(one).getByText(planFactOne.proposition)).toBeInTheDocument();
  });
});

// ── SUPERSESSION is additive (the prior entry STAYS visible) ──────────────────────
describe("Timeline — supersession is visible, not erased (append-only)", () => {
  it("renders the superseded run AND marks it superseded (prior retained)", async () => {
    await mount();
    const superseded = screen
      .getAllByTestId("chr-entry")
      .find((e) => e.getAttribute("data-chr-id") === supersededRun.chr_id)!;
    expect(superseded).toBeInTheDocument();
    expect(superseded).toHaveAttribute("data-superseded", "true");
    // and it is NOT shown as the current understanding
    expect(superseded).not.toHaveAttribute("data-current", "true");
  });

  it("retains a prior (un-superseded) CHR in the trail, not marked current (append-only)", async () => {
    await mount();
    const prior = screen
      .getAllByTestId("chr-entry")
      .find((e) => e.getAttribute("data-chr-id") === failedRun.chr_id)!;
    expect(prior).toBeInTheDocument();
    // it is a prior CHR — not the current understanding
    expect(prior).not.toHaveAttribute("data-current", "true");
  });
});

// ── Loading / empty states ───────────────────────────────────────────────────────
describe("Timeline — loading / empty states", () => {
  it("renders a clean loading state without crashing", async () => {
    runsState.isLoading = true;
    runsState.data = undefined as never;
    acceptancesState.isLoading = true;
    acceptancesState.data = undefined as never;
    planFactsState.isLoading = true;
    planFactsState.data = undefined as never;
    await mount();
    expect(screen.getByTestId("timeline")).toBeInTheDocument();
    expect(screen.getByTestId("timeline-loading")).toBeInTheDocument();
  });

  it("renders a clean 'no history yet' empty state when the trail is empty", async () => {
    runsState.data = { data: [] };
    acceptancesState.data = { data: [] };
    planFactsState.data = { data: [] };
    await mount();
    expect(screen.getByTestId("timeline")).toBeInTheDocument();
    expect(screen.getByTestId("timeline-empty")).toBeInTheDocument();
  });
});

// ── THE CRITICAL NEGATIVES (fail review if absent) ───────────────────────────────
describe("Timeline — NEGATIVES: presents, never generates; append-only; record-exact", () => {
  it("exposes NO edit / accept / generate / delete / rollback / govern control", async () => {
    const { container } = await mount();
    const controls = [
      ...container.querySelectorAll("button"),
      ...container.querySelectorAll('[role="button"]'),
      ...container.querySelectorAll("input"),
      ...container.querySelectorAll("textarea"),
      ...container.querySelectorAll("select"),
      ...container.querySelectorAll('[contenteditable="true"]'),
    ];
    const forbidden =
      /\bedit\b|\baccept\b|\breject\b|\bdefer\b|\bgenerate\b|\bdelete\b|\brestore\b|\brollback\b|roll back|\bapprove\b|\bgovern\b|recompute|re-?analy[sz]e|reanalyze|reanalyse|\bapply\b|\bscore\b|\bresolve\b/i;
    for (const el of controls) {
      const text = `${el.textContent ?? ""} ${el.getAttribute("aria-label") ?? ""}`;
      expect(text).not.toMatch(forbidden);
    }
  });

  it("never frames itself as audit / approval / compliance / decision-record", async () => {
    await mount();
    const surface = screen.getByTestId("timeline");
    expect(within(surface).queryByText(/\baudit\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\bapproved\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\bapproval\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\bcompliance\b/i)).not.toBeInTheDocument();
  });

  it("CHR entries NEVER render as settled / world-truth (always Derived projections)", async () => {
    await mount();
    const surface = screen.getByTestId("timeline");
    expect(within(surface).queryByText(/\bsettled\b/i)).not.toBeInTheDocument();
    for (const entry of within(surface).getAllByTestId("chr-entry")) {
      const label = within(entry).getByTestId("epistemic-label");
      expect(label).toHaveAttribute("data-standing", "derived");
      expect(label).not.toHaveAttribute("data-standing", "attested");
    }
  });

  it("plan facts NEVER render as world-truth or evidence-attested (only user-attested)", async () => {
    await mount();
    for (const fact of screen.getAllByTestId("plan-fact-entry")) {
      const label = within(fact).getByTestId("epistemic-label");
      expect(label).toHaveAttribute("data-source", "user");
      // not evidence-attested, not OSLO-attested
      expect(label).not.toHaveAttribute("data-source", "evidence");
      expect(label).not.toHaveAttribute("data-source", "oslo");
      // never the Derived projection wording
      expect(label).not.toHaveAttribute("data-standing", "derived");
    }
    // and the surface never claims plan facts are world-truth / verified
    const surface = screen.getByTestId("timeline");
    expect(within(surface).queryByText(/world.?truth/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\bverified\b/i)).not.toBeInTheDocument();
  });

  it("CRITICAL: ordering is APPEND-EXACT — the per-source record order is preserved (no destructive reorder)", async () => {
    await mount();
    // The CHR trail renders the analysis runs in the EXACT order the read returned
    // them (the fixture's append order) — not re-sorted, not reversed.
    const renderedRunIds = screen
      .getAllByTestId("chr-entry")
      .map((e) => e.getAttribute("data-chr-id"));
    const sourceRunIds = analysisRunsFixture.map((r) => r.chr_id);
    expect(renderedRunIds).toEqual(sourceRunIds);

    // Same for UARs and plan facts — record order preserved per source.
    const renderedUarIds = screen
      .getAllByTestId("uar-entry")
      .map((e) => e.getAttribute("data-uar-id"));
    expect(renderedUarIds).toEqual(acceptancesFixture.map((u) => u.uar_id));

    const renderedFactIds = screen
      .getAllByTestId("plan-fact-entry")
      .map((e) => e.getAttribute("data-plan-fact-id"));
    expect(renderedFactIds).toEqual(planFactsFixture.map((f) => f.plan_fact_id));
  });

  it("CRITICAL: rendering does NOT mutate the governed DTOs (record-exact, read-only)", async () => {
    const runsBefore = JSON.parse(JSON.stringify(analysisRunsFixture));
    const uarsBefore = JSON.parse(JSON.stringify(acceptancesFixture));
    const factsBefore = JSON.parse(JSON.stringify(planFactsFixture));
    await mount();
    // the surface presents the records byte-for-byte; it writes nothing back
    expect(analysisRunsFixture).toEqual(runsBefore);
    expect(acceptancesFixture).toEqual(uarsBefore);
    expect(planFactsFixture).toEqual(factsBefore);
  });
});
