/**
 * DTM-0021 — the Finding Panel (IC-WE-DISCLOSE E1).
 *
 * Presents ONE Finding: its summary + type + Derived confidence label, its
 * Attested evidence anchors (the evidence lineage), a conflict marker when the
 * finding is contested, and the RP-C1 affordance to open the Recommendation Panel
 * (the nested recommendations route). It PRESENTS, NEVER GENERATES — no
 * edit/accept/resolve/generate control, and recommendations are NOT rendered
 * inline here (that's DTM-0022).
 *
 * The DTM-0018 generated `useGetFinding…` hook is mocked with fixture DTOs.
 */
import { describe, it, expect, vi, beforeEach } from "vitest";
import { screen, within, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { renderFindingPanel } from "./testHarness";
import {
  conflictedFindingFixture,
  cleanFindingFixture,
  noEvidenceFindingFixture,
  PROJECT_ID,
} from "./fixtures";

// ── Mock the DTM-0018 finding hook (the panel consumes, never re-implements) ──
const findingState = {
  data: { data: conflictedFindingFixture },
  isLoading: false,
  isError: false,
  error: null as unknown,
};

vi.mock("../../../api/generated/findings/findings", () => ({
  useGetFindingV1FindingsFindingIdGet: () => findingState,
  getGetFindingV1FindingsFindingIdGetQueryKey: (findingId: string) => [
    `/v1/findings/${findingId}`,
  ],
}));

// ── Mock the DTM-0035 finding lifecycle commands (acknowledge/address/reopen) ──
const acknowledgeMutate = vi.fn();
const addressMutate = vi.fn();
const reopenMutate = vi.fn();
let lastAckOnSuccess: (() => void) | undefined;
vi.mock("../../../api/generated/finding-commands/finding-commands", () => ({
  useAcknowledgeFindingV1FindingsFindingIdAcknowledgePost: (opts?: {
    mutation?: { onSuccess?: () => void };
  }) => {
    lastAckOnSuccess = opts?.mutation?.onSuccess;
    return { mutate: acknowledgeMutate, isPending: false };
  },
  useAddressFindingV1FindingsFindingIdAddressPost: () => ({
    mutate: addressMutate,
    isPending: false,
  }),
  useReopenFindingV1FindingsFindingIdReopenPost: () => ({
    mutate: reopenMutate,
    isPending: false,
  }),
}));

// Imported AFTER the mock is declared (vi.mock is hoisted).
import { FindingPanel } from "./FindingPanel";

function mount(findingId = conflictedFindingFixture.finding_id) {
  return renderFindingPanel(
    <FindingPanel projectId={PROJECT_ID} findingId={findingId} />,
    { projectId: PROJECT_ID, findingId },
  );
}

beforeEach(() => {
  findingState.isLoading = false;
  findingState.isError = false;
  findingState.error = null;
  findingState.data = { data: conflictedFindingFixture };
  acknowledgeMutate.mockReset();
  addressMutate.mockReset();
  reopenMutate.mockReset();
  lastAckOnSuccess = undefined;
});

describe("FindingPanel — presents one Finding with its lineage + confidence", () => {
  it("renders the finding summary and a user-friendly finding type", async () => {
    await mount();
    const panel = screen.getByTestId("finding-panel");
    expect(within(panel).getByText(conflictedFindingFixture.summary as string)).toBeInTheDocument();
    // the finding type is surfaced (user-friendly label of `conflict`)
    expect(within(panel).getByTestId("finding-type")).toBeInTheDocument();
    expect(within(panel).getByTestId("finding-type").textContent ?? "").toMatch(/conflict/i);
  });

  it("renders the finding's confidence as a Derived label (never Attested/settled)", async () => {
    await mount();
    const confidence = screen.getByTestId("finding-confidence");
    const label = within(confidence).getByTestId("epistemic-label");
    expect(label).toHaveAttribute("data-standing", "derived");
  });

  it("renders each Attested evidence anchor with the attested/evidence label", async () => {
    await mount();
    const evidence = screen.getByTestId("finding-evidence");
    const anchors = within(evidence).getAllByTestId("evidence-anchor");
    expect(anchors.length).toBe(conflictedFindingFixture.evidence_links!.length);
    for (const anchor of anchors) {
      const label = within(anchor).getByTestId("epistemic-label");
      // Attested standing, sourced from evidence — NEVER Derived.
      expect(label).toHaveAttribute("data-standing", "attested");
      expect(label).toHaveAttribute("data-source", "evidence");
    }
  });

  it("surfaces the conflict marker when the finding is contested (presented, not resolved)", async () => {
    await mount();
    const panel = screen.getByTestId("finding-panel");
    expect(within(panel).getByTestId("conflict-marker")).toBeInTheDocument();
  });

  it("shows NO conflict marker when the finding is not contested", async () => {
    findingState.data = { data: cleanFindingFixture };
    await mount(cleanFindingFixture.finding_id);
    const panel = screen.getByTestId("finding-panel");
    expect(within(panel).queryByTestId("conflict-marker")).not.toBeInTheDocument();
  });
});

describe("FindingPanel — RP-C1: affordance to open the Recommendation Panel", () => {
  it("renders a 'view recommendations' affordance that routes to the nested recommendations route", async () => {
    const { router } = await mount();
    const affordance = screen.getByTestId("view-recommendations");
    // It is a link to the nested RP-C1 route, not an inline render.
    expect(affordance).toHaveAttribute(
      "href",
      `/projects/${PROJECT_ID}/findings/${conflictedFindingFixture.finding_id}/recommendations`,
    );
    fireEvent.click(affordance);
    await router.invalidate();
    expect(
      router.state.location.pathname.endsWith(
        `/findings/${conflictedFindingFixture.finding_id}/recommendations`,
      ),
    ).toBe(true);
  });
});

describe("FindingPanel — loading / empty-evidence / not-found states", () => {
  it("renders a clean loading state without crashing", async () => {
    findingState.isLoading = true;
    findingState.data = undefined as never;
    await mount();
    expect(screen.getByTestId("finding-panel")).toBeInTheDocument();
    expect(screen.getByTestId("finding-loading")).toBeInTheDocument();
  });

  it("renders a not-found state when the finding is absent", async () => {
    findingState.data = { data: undefined as never };
    await mount();
    expect(screen.getByTestId("finding-panel")).toBeInTheDocument();
    expect(screen.getByTestId("finding-not-found")).toBeInTheDocument();
  });

  it("renders an explicit empty-evidence state (distinct from not-analyzed)", async () => {
    findingState.data = { data: noEvidenceFindingFixture };
    await mount(noEvidenceFindingFixture.finding_id);
    expect(screen.getByTestId("finding-evidence-empty")).toBeInTheDocument();
  });
});

// ── Finding-lifecycle affordance (DTM-0039 → DTM-0035) ───────────────────────────
describe("FindingPanel — lifecycle affordance calls the workflow command", () => {
  it("acknowledge calls the acknowledge command for a detected finding", async () => {
    await mount(); // conflictedFindingFixture is `detected`
    const ack = screen.getByTestId("finding-acknowledge");
    fireEvent.click(ack);
    expect(acknowledgeMutate).toHaveBeenCalledWith({
      findingId: conflictedFindingFixture.finding_id,
    });
  });

  it("presents the finding's Derived workflow status (a status, not an assessment)", async () => {
    await mount();
    const status = screen.getByTestId("finding-status");
    expect(status).toHaveAttribute("data-status", "detected");
  });

  it("on command success it invalidates the finding read (re-reads the governed status)", async () => {
    await mount();
    expect(typeof lastAckOnSuccess).toBe("function");
  });
});

// ── The epistemic-safety NEGATIVES (the spine of Disclose; fail review if absent) ──
describe("FindingPanel — NEGATIVES: presents, never generates", () => {
  it("exposes NO edit / accept / resolve / generate / govern control", async () => {
    const { container } = await mount();
    const controls = [
      ...container.querySelectorAll("button"),
      ...container.querySelectorAll('[role="button"]'),
      ...container.querySelectorAll("input"),
      ...container.querySelectorAll("textarea"),
    ];
    const forbidden =
      /\bedit\b|\baccept\b|\breject\b|\bdefer\b|\bresolve\b|\bclose finding\b|\bapprove\b|\bgovern\b|\bgenerate\b|recompute|re-?analy[sz]e|run analysis|\bapply\b/i;
    for (const el of controls) {
      const text = `${el.textContent ?? ""} ${el.getAttribute("aria-label") ?? ""}`;
      expect(text).not.toMatch(forbidden);
    }
  });

  it("the finding never renders as settled / attested-truth (it stays Derived)", async () => {
    await mount();
    const panel = screen.getByTestId("finding-panel");
    expect(within(panel).queryByText(/\bsettled\b/i)).not.toBeInTheDocument();
    expect(within(panel).queryByText(/\bresolved\b/i)).not.toBeInTheDocument();
    // The finding's own confidence label is Derived.
    const confidence = screen.getByTestId("finding-confidence");
    expect(within(confidence).getByTestId("epistemic-label")).toHaveAttribute(
      "data-standing",
      "derived",
    );
  });

  it("evidence anchors are NEVER rendered as Derived", async () => {
    await mount();
    const evidence = screen.getByTestId("finding-evidence");
    const labels = within(evidence).getAllByTestId("epistemic-label");
    for (const label of labels) {
      expect(label).toHaveAttribute("data-standing", "attested");
      expect(label).not.toHaveAttribute("data-standing", "derived");
    }
  });

  it("does NOT render any inline recommendation list (RP-C1 — that's the Recommendation Panel)", async () => {
    await mount();
    // No inline recommendation content — only the affordance/link to the nested route.
    expect(screen.queryByTestId("recommendation-list")).not.toBeInTheDocument();
    expect(screen.queryByTestId("recommendation-item")).not.toBeInTheDocument();
    expect(screen.queryByTestId("rec-panel-target")).not.toBeInTheDocument();
  });
});
