/**
 * DTM-0023 — Issue Cards (IC-WE-DISCLOSE E1).
 *
 * Presents Issues as cards: each card carries its **severity** (a governed
 * qualifier) + the source Finding's **confidence band** as a Derived
 * `EpistemicLabel`, and links back to its **source Finding** (the Finding Panel
 * route). It PRESENTS, NEVER GENERATES — no edit/score/accept/defer/generate
 * control, the card never reads as settled/attested, and confidence never reads
 * as project health/readiness/probability.
 *
 * THE ISSUES-DATA FINDING: there is no dedicated Issue endpoint/DTO (see
 * fixtures.ts). The cards render from the DTM-0018 Finding read (the governed
 * carrier of severity + the Derived confidence label + source-finding lineage).
 * The DTM-0018 generated `useListFindings…` hook is mocked with fixture DTOs.
 */
import { describe, it, expect, vi, beforeEach } from "vitest";
import { screen, within, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { renderIssueCards } from "./testHarness";
import {
  issuesFixture,
  criticalIssueFixture,
  moderateIssueFixture,
  warningIssueFixture,
  PROJECT_ID,
} from "./fixtures";

// ── Mock the DTM-0018 findings list hook (the surface consumes, never re-implements) ──
const issuesState = {
  data: { data: issuesFixture },
  isLoading: false,
  isError: false,
  error: null as unknown,
};

vi.mock("../../api/generated/findings/findings", () => ({
  useListFindingsV1ProjectsProjectIdFindingsGet: () => issuesState,
}));

// Imported AFTER the mock is declared (vi.mock is hoisted).
import { IssueCards } from "./IssueCards";

function mount(projectId = PROJECT_ID) {
  return renderIssueCards(<IssueCards projectId={projectId} />, { projectId });
}

beforeEach(() => {
  issuesState.isLoading = false;
  issuesState.isError = false;
  issuesState.error = null;
  issuesState.data = { data: issuesFixture };
});

describe("IssueCards — presents each Issue as a card with severity + confidence + source link", () => {
  it("renders one card per issue", async () => {
    await mount();
    const surface = screen.getByTestId("issue-cards");
    const cards = within(surface).getAllByTestId("issue-card");
    expect(cards.length).toBe(issuesFixture.length);
  });

  it("each card shows its severity as a governed qualifier", async () => {
    await mount();
    const surface = screen.getByTestId("issue-cards");
    const cards = within(surface).getAllByTestId("issue-card");
    for (const card of cards) {
      const severity = within(card).getByTestId("issue-severity");
      // a non-empty governed severity label
      expect((severity.textContent ?? "").trim().length).toBeGreaterThan(0);
    }
    // and the distinct governed severities are surfaced
    expect(within(surface).getAllByText(/critical/i).length).toBeGreaterThan(0);
    expect(within(surface).getAllByText(/moderate/i).length).toBeGreaterThan(0);
    expect(within(surface).getAllByText(/warning/i).length).toBeGreaterThan(0);
  });

  it("each card renders its confidence as a Derived label (never Attested/settled)", async () => {
    await mount();
    const cards = screen.getAllByTestId("issue-card");
    for (const card of cards) {
      const label = within(card).getByTestId("epistemic-label");
      expect(label).toHaveAttribute("data-standing", "derived");
      // the banded confidence chip is present
      expect(within(card).getByTestId("confidence-band")).toBeInTheDocument();
    }
  });

  it("each card links back to its SOURCE FINDING (the Finding Panel route)", async () => {
    await mount();
    const cards = screen.getAllByTestId("issue-card");
    const link = within(cards[0]).getByTestId("view-source-finding");
    expect(link).toHaveAttribute(
      "href",
      `/projects/${PROJECT_ID}/findings/${criticalIssueFixture.finding_id}`,
    );
  });

  it("activating a card's source-finding link routes to the Finding Panel (and nowhere else)", async () => {
    const { router } = await mount();
    const cards = screen.getAllByTestId("issue-card");
    const link = within(cards[1]).getByTestId("view-source-finding");
    fireEvent.click(link);
    await router.invalidate();
    expect(
      router.state.location.pathname.endsWith(
        `/findings/${moderateIssueFixture.finding_id}`,
      ),
    ).toBe(true);
  });

  it("surfaces the conflict marker on a contested issue (presented, not resolved)", async () => {
    await mount();
    const cards = screen.getAllByTestId("issue-card");
    // the critical fixture is contested → its card carries a conflict marker
    expect(within(cards[0]).getByTestId("conflict-marker")).toBeInTheDocument();
    // the warning fixture is not contested → no conflict marker
    expect(within(cards[2]).queryByTestId("conflict-marker")).not.toBeInTheDocument();
  });
});

describe("IssueCards — loading / empty states", () => {
  it("renders a clean loading state without crashing", async () => {
    issuesState.isLoading = true;
    issuesState.data = undefined as never;
    await mount();
    expect(screen.getByTestId("issue-cards")).toBeInTheDocument();
    expect(screen.getByTestId("issue-cards-loading")).toBeInTheDocument();
  });

  it("renders a clean, positive empty state when there are no issues", async () => {
    issuesState.data = { data: [] };
    await mount();
    expect(screen.getByTestId("issue-cards")).toBeInTheDocument();
    expect(screen.getByTestId("issue-cards-empty")).toBeInTheDocument();
  });
});

// ── The epistemic-safety NEGATIVES (the spine of Disclose; fail review if absent) ──
describe("IssueCards — NEGATIVES: presents, never generates", () => {
  it("exposes NO edit / score / accept / defer / generate / govern control", async () => {
    const { container } = await mount();
    const controls = [
      ...container.querySelectorAll("button"),
      ...container.querySelectorAll('[role="button"]'),
      ...container.querySelectorAll("input"),
      ...container.querySelectorAll("textarea"),
      ...container.querySelectorAll("select"),
    ];
    const forbidden =
      /\bedit\b|\bscore\b|\baccept\b|\breject\b|\bdefer\b|\bresolve\b|\bprioriti[sz]e\b|\bapprove\b|\bgovern\b|\bgenerate\b|recompute|re-?analy[sz]e|run analysis|\bapply\b/i;
    for (const el of controls) {
      const text = `${el.textContent ?? ""} ${el.getAttribute("aria-label") ?? ""}`;
      expect(text).not.toMatch(forbidden);
    }
  });

  it("no issue card ever renders as settled / attested-truth (it stays Derived)", async () => {
    await mount();
    const surface = screen.getByTestId("issue-cards");
    expect(within(surface).queryByText(/\bsettled\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\bresolved\b/i)).not.toBeInTheDocument();
    for (const card of within(surface).getAllByTestId("issue-card")) {
      const label = within(card).getByTestId("epistemic-label");
      expect(label).toHaveAttribute("data-standing", "derived");
      expect(label).not.toHaveAttribute("data-standing", "attested");
    }
  });

  it("confidence never reads as project health / readiness / probability / a bare score", async () => {
    await mount();
    const surface = screen.getByTestId("issue-cards");
    expect(within(surface).queryByText(/\bhealth\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\breadiness\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\bprobability\b/i)).not.toBeInTheDocument();
    // severity must read as a governed qualifier, never a numeric score / %
    for (const card of within(surface).getAllByTestId("issue-card")) {
      const severity = (within(card).getByTestId("issue-severity").textContent ?? "").trim();
      expect(severity).not.toMatch(/%|\bscore\b|\bprobability\b/i);
    }
  });

  it("severity is a governed qualifier (critical/moderate/warning), not an invented value", async () => {
    await mount();
    const surface = screen.getByTestId("issue-cards");
    const allowed = /^(critical|moderate|warning)$/i;
    for (const card of within(surface).getAllByTestId("issue-card")) {
      const severity = (within(card).getByTestId("issue-severity").textContent ?? "").trim();
      expect(severity).toMatch(allowed);
    }
  });

  it("warning fixture renders a high band exactly as the governed value (no upgrade)", async () => {
    await mount();
    const cards = screen.getAllByTestId("issue-card");
    const band = within(cards[2]).getByTestId("confidence-band");
    expect(band).toHaveAttribute("data-band", warningIssueFixture.label!.confidence_band);
  });
});
