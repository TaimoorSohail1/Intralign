/**
 * DTM-0029 — Honest-limit disclosure (DL-048 UP-4, IC-WE-DISCLOSE).
 *
 * When a Fast/Deep run is scope- or budget-limited (Tier-1 envelope exceeded →
 * partial orientation), Disclose MUST present a TRUTHFUL partial-analysis disclosure:
 * the reduced coverage shown WITH the reason ("partial because the project exceeds the
 * tier size"). This is an epistemic-safety obligation FIRST — never imply a full/final
 * analysis. Any Upgrade-Prompt affordance (MON-04 UP-4) is rendered on the SAME surface,
 * ALONGSIDE the honest disclosure, never INSTEAD OF it.
 *
 * The negatives are the heart:
 *   - partial-as-complete is rejected (a limited result must never read as complete/final);
 *   - upgrade-instead-of-disclosure is rejected (the upgrade prompt never appears in place
 *     of the honest disclosure; the disclosure is always present when limited).
 */
import { describe, it, expect } from "vitest";
import { render, screen, within } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { ThemeProvider } from "@mui/material/styles";
import { theme } from "../theme";
import { HonestLimitDisclosure } from "./HonestLimitDisclosure";
import {
  partialLimitFixture,
  partialLimitNoUpgradeFixture,
  completeRunFixture,
} from "./honestLimit.fixtures";

function mount(ui: React.ReactElement) {
  return render(<ThemeProvider theme={theme}>{ui}</ThemeProvider>);
}

describe("HonestLimitDisclosure — truthful partial-analysis disclosure", () => {
  it("renders the disclosure when a run is scope/budget-limited", () => {
    mount(<HonestLimitDisclosure limit={partialLimitFixture} />);
    expect(screen.getByTestId("honest-limit")).toBeInTheDocument();
  });

  it("states the result is PARTIAL (never complete/final)", () => {
    mount(<HonestLimitDisclosure limit={partialLimitFixture} />);
    const disclosure = screen.getByTestId("honest-limit-disclosure");
    expect(disclosure.textContent ?? "").toMatch(/partial/i);
  });

  it("shows the REASON for the reduced coverage", () => {
    mount(<HonestLimitDisclosure limit={partialLimitFixture} />);
    const reason = screen.getByTestId("honest-limit-reason");
    expect(reason.textContent ?? "").toMatch(/exceeds the/i);
  });

  it("shows the reduced-coverage detail", () => {
    mount(<HonestLimitDisclosure limit={partialLimitFixture} />);
    expect(screen.getByTestId("honest-limit-coverage")).toBeInTheDocument();
  });

  it("renders nothing when the run is NOT limited (complete)", () => {
    const { container } = mount(<HonestLimitDisclosure limit={completeRunFixture} />);
    expect(screen.queryByTestId("honest-limit")).not.toBeInTheDocument();
    expect(container.textContent ?? "").not.toMatch(/partial/i);
  });
});

describe("HonestLimitDisclosure — upgrade ALONGSIDE, never INSTEAD OF (UP-4)", () => {
  it("renders the upgrade prompt ALONGSIDE the disclosure when one is supplied", () => {
    mount(<HonestLimitDisclosure limit={partialLimitFixture} />);
    // BOTH present, on the same surface.
    const root = screen.getByTestId("honest-limit");
    expect(within(root).getByTestId("honest-limit-disclosure")).toBeInTheDocument();
    expect(within(root).getByTestId("honest-limit-upgrade")).toBeInTheDocument();
  });

  it("the disclosure precedes the upgrade prompt in the DOM (disclosure-first)", () => {
    mount(<HonestLimitDisclosure limit={partialLimitFixture} />);
    const disclosure = screen.getByTestId("honest-limit-disclosure");
    const upgrade = screen.getByTestId("honest-limit-upgrade");
    // disclosure comes before upgrade => disclosure leads, upgrade is alongside/after.
    expect(
      disclosure.compareDocumentPosition(upgrade) &
        Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
  });

  it("NEGATIVE: still renders the honest disclosure even when NO upgrade prompt is given", () => {
    mount(<HonestLimitDisclosure limit={partialLimitNoUpgradeFixture} />);
    // The disclosure is mandatory; the upgrade is optional/commodity.
    expect(screen.getByTestId("honest-limit-disclosure")).toBeInTheDocument();
    expect(screen.queryByTestId("honest-limit-upgrade")).not.toBeInTheDocument();
  });

  it("NEGATIVE: never presents the limited result as complete/final/full", () => {
    mount(<HonestLimitDisclosure limit={partialLimitFixture} />);
    const root = screen.getByTestId("honest-limit");
    const text = (root.textContent ?? "").toLowerCase();
    expect(text).not.toMatch(/\bcomplete analysis\b/);
    expect(text).not.toMatch(/\bfull analysis\b/);
    expect(text).not.toMatch(/\bfinal analysis\b/);
    expect(text).not.toMatch(/analysis complete/);
  });
});
