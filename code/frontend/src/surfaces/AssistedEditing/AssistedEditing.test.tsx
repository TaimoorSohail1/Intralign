/**
 * DTM-0029 — Assisted Editing / Persistent Intelligence (AW-04/05, IC-WE-DISCLOSE).
 *
 * An always-visible panel that PRESENTS (read-only) the governed intelligence during
 * artifact editing: Outcome Confidence + CAF (Clarity/Alignment/Feasibility) +
 * Understanding-State — each via EpistemicLabel (Derived, banded, never settled). It
 * ROUTES assists to Chat (B1) and to a Suggested Fix (B3, reached via its Finding —
 * RP-C1); it performs NONE of them.
 *
 * The negative is the heart: the panel exposes NO generate / score / accept / apply
 * cognition control — it routes, it performs nothing.
 */
import { describe, it, expect, vi, beforeEach } from "vitest";
import { screen, within, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { renderAssistedEditing } from "./testHarness";
import {
  PROJECT_ID,
  ARTIFACT_ID,
  confidenceFixture,
  cafFixture,
  runsCurrentFixture,
  runsStaleFixture,
} from "./fixtures";

const confidenceState = { data: { data: confidenceFixture }, isLoading: false };
const cafState = { data: { data: cafFixture }, isLoading: false };
const runsState = { data: { data: runsCurrentFixture }, isLoading: false };

vi.mock("../../api/generated/confidence/confidence", () => ({
  useGetConfidenceV1ProjectsProjectIdConfidenceGet: () => confidenceState,
  useGetCafV1ProjectsProjectIdCafGet: () => cafState,
}));
vi.mock("../../api/generated/analysis-runs/analysis-runs", () => ({
  useListAnalysisRunsV1ProjectsProjectIdAnalysisRunsGet: () => runsState,
}));

import { AssistedEditing } from "./AssistedEditing";

function mount() {
  return renderAssistedEditing(
    <AssistedEditing projectId={PROJECT_ID} artifactId={ARTIFACT_ID} findingId="f-1" />,
    { artifactId: ARTIFACT_ID },
  );
}

beforeEach(() => {
  confidenceState.data = { data: confidenceFixture };
  confidenceState.isLoading = false;
  cafState.data = { data: cafFixture };
  cafState.isLoading = false;
  runsState.data = { data: runsCurrentFixture };
  runsState.isLoading = false;
});

describe("AssistedEditing — always-visible read-only intelligence", () => {
  it("renders the panel", async () => {
    await mount();
    expect(screen.getByTestId("assisted-editing")).toBeInTheDocument();
  });

  it("presents Outcome Confidence as a Derived banded label (never settled)", async () => {
    await mount();
    const conf = screen.getByTestId("ae-confidence");
    expect(within(conf).getByTestId("epistemic-label")).toHaveAttribute(
      "data-standing",
      "derived",
    );
    expect(within(conf).getByTestId("confidence-band")).toHaveAttribute(
      "data-band",
      confidenceFixture.label!.confidence_band,
    );
  });

  it("presents CAF — three co-equal dimensions, each a Derived banded label", async () => {
    await mount();
    const caf = screen.getByTestId("ae-caf");
    expect(within(caf).getByTestId("ae-caf-clarity")).toBeInTheDocument();
    expect(within(caf).getByTestId("ae-caf-alignment")).toBeInTheDocument();
    expect(within(caf).getByTestId("ae-caf-feasibility")).toBeInTheDocument();
    for (const dim of within(caf).getAllByTestId("ae-caf-dimension")) {
      expect(within(dim).getByTestId("epistemic-label")).toHaveAttribute(
        "data-standing",
        "derived",
      );
    }
  });

  it("presents Understanding-State (current)", async () => {
    await mount();
    const state = screen.getByTestId("ae-understanding-state");
    expect(state.textContent ?? "").toMatch(/current/i);
  });

  it("marks Understanding-State as previous analysis when the latest run is superseded", async () => {
    runsState.data = { data: runsStaleFixture };
    await mount();
    const state = screen.getByTestId("ae-understanding-state");
    expect(state.textContent ?? "").toMatch(/previous analysis/i);
  });
});

describe("AssistedEditing — ROUTES assists (B1 Chat / B3 Suggested Fix), performs none", () => {
  it("routes the assist-to-Chat affordance (B1) to the project Chat surface (carrying artifact context)", async () => {
    await mount();
    const link = screen.getByTestId("ae-route-chat");
    const href = link.getAttribute("href") ?? "";
    // Routes to the project Chat surface…
    expect(href.startsWith(`/projects/${PROJECT_ID}/chat`)).toBe(true);
    // …carrying the artifact as inherited context (read-only), never a mutation.
    expect(href).toMatch(/context_kind=artifact/);
    expect(href).toMatch(new RegExp(`context_id=${ARTIFACT_ID}`));
  });

  it("activating the Chat assist lands on the Chat surface", async () => {
    const { router } = await mount();
    fireEvent.click(screen.getByTestId("ae-route-chat"));
    await router.invalidate();
    expect(router.state.location.pathname).toBe(`/projects/${PROJECT_ID}/chat`);
    expect(screen.getByTestId("chat-target")).toBeInTheDocument();
  });

  it("routes the assist-to-Suggested-Fix affordance (B3) via its Finding (RP-C1)", async () => {
    await mount();
    const link = screen.getByTestId("ae-route-suggested-fix");
    // Reached via the Finding Panel — never a standalone recommendation route.
    expect(link).toHaveAttribute("href", `/projects/${PROJECT_ID}/findings/f-1`);
    expect(link.getAttribute("href")).not.toMatch(/\/recommendations(\/|$)/);
  });
});

describe("AssistedEditing — loading / empty states", () => {
  it("renders cleanly while loading", async () => {
    confidenceState.isLoading = true;
    confidenceState.data = undefined as never;
    await mount();
    expect(screen.getByTestId("assisted-editing")).toBeInTheDocument();
    expect(screen.getByTestId("ae-loading")).toBeInTheDocument();
  });

  it("renders clean empty states when confidence / CAF are not yet available", async () => {
    confidenceState.data = undefined as never;
    cafState.data = undefined as never;
    await mount();
    expect(screen.getByTestId("ae-confidence-empty")).toBeInTheDocument();
    expect(screen.getByTestId("ae-caf-empty")).toBeInTheDocument();
  });
});

// ── The Disclose / AW-04/05 NEGATIVES (the spine; fail review if absent) ──────────
describe("AssistedEditing — NEGATIVES: routes, performs NO cognition", () => {
  it("exposes NO generate / score / accept / apply / edit cognition control", async () => {
    const { container } = await mount();
    const controls = [
      ...container.querySelectorAll("button"),
      ...container.querySelectorAll('[role="button"]'),
      ...container.querySelectorAll("input"),
      ...container.querySelectorAll("textarea"),
      ...container.querySelectorAll("select"),
    ];
    const forbidden =
      /\bgenerate\b|\bscore\b|\baccept\b|\breject\b|\bdefer\b|\bapply\b|\bapprove\b|\bgovern\b|recompute|re-?analy[sz]e|run analysis|\bresolve\b|\bsave\b/i;
    for (const el of controls) {
      const text = `${el.textContent ?? ""} ${el.getAttribute("aria-label") ?? ""}`;
      expect(text).not.toMatch(forbidden);
    }
  });

  it("only affordances are routing links (no cognition-performing buttons)", async () => {
    const { container } = await mount();
    // The two assist affordances are links (routing), not action buttons.
    expect(screen.getByTestId("ae-route-chat").tagName.toLowerCase()).toBe("a");
    expect(screen.getByTestId("ae-route-suggested-fix").tagName.toLowerCase()).toBe("a");
    // No <button> performs cognition.
    expect(container.querySelectorAll("button").length).toBe(0);
  });

  it("no Derived value renders as settled / attested, and no bare score / % is shown", async () => {
    await mount();
    const surface = screen.getByTestId("assisted-editing");
    for (const label of within(surface).getAllByTestId("epistemic-label")) {
      expect(label).toHaveAttribute("data-standing", "derived");
    }
    const text = surface.textContent ?? "";
    expect(text).not.toMatch(/%/);
    expect(text).not.toMatch(/\bhealth\b/i);
    // raw 0–100 indices never rendered
    expect(text).not.toMatch(/\b64\b|\b78\b|\b35\b|\b60\b/);
  });
});
