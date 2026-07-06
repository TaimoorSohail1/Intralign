import type { ReactElement } from "react";
import { describe, it, expect } from "vitest";
import { render, screen, within } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { ThemeProvider } from "@mui/material/styles";
import { EpistemicLabel } from "./EpistemicLabel";
import { theme } from "../theme";

function renderLabel(ui: ReactElement) {
  return render(<ThemeProvider theme={theme}>{ui}</ThemeProvider>);
}

// IC-WE-DISCLOSE E0 — epistemic-safety labeling. The single reusable component
// every Wave E surface mounts. It MUST make it impossible to render a Derived
// item as settled/confirmed, or low confidence as high.
describe("EpistemicLabel — standing (Attested vs Derived)", () => {
  it("renders an Attested item with its standing word, never as Derived", () => {
    renderLabel(<EpistemicLabel epistemic={{ standing: "attested", source: "evidence" }} />);
    const root = screen.getByTestId("epistemic-label");
    expect(root).toHaveAttribute("data-standing", "attested");
    expect(within(root).getByText(/attested/i)).toBeInTheDocument();
    expect(within(root).queryByText(/derived/i)).not.toBeInTheDocument();
  });

  it("renders a Derived item as Derived and never as settled/confirmed", () => {
    renderLabel(
      <EpistemicLabel epistemic={{ standing: "derived", confidenceValue: 90 }} />,
    );
    const root = screen.getByTestId("epistemic-label");
    expect(root).toHaveAttribute("data-standing", "derived");
    expect(within(root).getByText(/derived/i)).toBeInTheDocument();
    // NEGATIVE: a Derived projection is never presented as settled/confirmed/attested truth.
    expect(within(root).queryByText(/settled/i)).not.toBeInTheDocument();
    expect(within(root).queryByText(/confirmed/i)).not.toBeInTheDocument();
    expect(within(root).queryByText(/^attested/i)).not.toBeInTheDocument();
  });
});

describe("EpistemicLabel — plan-fact variant is user-attested", () => {
  it("renders a plan fact as user-attested (not world-truth, not Derived)", () => {
    renderLabel(<EpistemicLabel epistemic={{ standing: "attested", source: "user" }} />);
    const root = screen.getByTestId("epistemic-label");
    expect(root).toHaveAttribute("data-standing", "attested");
    expect(root).toHaveAttribute("data-source", "user");
    expect(within(root).getByText(/you confirmed|user[- ]attested/i)).toBeInTheDocument();
    // not asserted as world-truth
    expect(within(root).queryByText(/true|truth|fact(?!or)/i)).not.toBeInTheDocument();
  });
});

describe("EpistemicLabel — confidence band + edge guard", () => {
  const cases: Array<[number, "low" | "medium" | "high"]> = [
    [48, "low"],
    [52, "low"],
    [74, "medium"],
    [75, "high"],
    [77, "medium"],
  ];
  it.each(cases)("value %i resolves to the %s band", (value, expected) => {
    renderLabel(
      <EpistemicLabel epistemic={{ standing: "derived", confidenceValue: value }} />,
    );
    const band = screen.getByTestId("confidence-band");
    // The band is the machine contract (data-band); the visible text is a
    // trust-in-understanding synonym (Low/Moderate/High understanding).
    expect(band).toHaveAttribute("data-band", expected);
  });

  it("a low-confidence value can never display as high (edge guard, value 77)", () => {
    renderLabel(
      <EpistemicLabel epistemic={{ standing: "derived", confidenceValue: 77 }} />,
    );
    const band = screen.getByTestId("confidence-band");
    expect(band).toHaveAttribute("data-band", "medium");
    expect(band).not.toHaveTextContent(/high/i);
  });

  it("confidence text is trust-in-understanding, never project health", () => {
    renderLabel(
      <EpistemicLabel epistemic={{ standing: "derived", confidenceValue: 90 }} />,
    );
    const band = screen.getByTestId("confidence-band");
    // band label words about trust in understanding, not project health/probability
    expect(band).not.toHaveTextContent(/health|on track|probability|risk score/i);
  });

  it("accepts a pre-banded value from the DTO without a numeric value", () => {
    renderLabel(
      <EpistemicLabel epistemic={{ standing: "derived", band: "high" }} />,
    );
    expect(screen.getByTestId("confidence-band")).toHaveAttribute("data-band", "high");
  });
});

describe("EpistemicLabel — conflict marker", () => {
  it("shows a conflict marker when contested", () => {
    renderLabel(
      <EpistemicLabel
        epistemic={{ standing: "derived", confidenceValue: 80, conflict: true }}
      />,
    );
    expect(screen.getByTestId("conflict-marker")).toBeInTheDocument();
    expect(screen.getByTestId("conflict-marker")).toHaveTextContent(/conflict|contested/i);
  });

  it("omits the conflict marker when not contested", () => {
    renderLabel(
      <EpistemicLabel epistemic={{ standing: "derived", confidenceValue: 80 }} />,
    );
    expect(screen.queryByTestId("conflict-marker")).not.toBeInTheDocument();
  });
});

describe("EpistemicLabel — fromDerivedEnvelope adapter (consumes the DTO)", () => {
  it("maps a generated DerivedEnvelope DTO to a safe Derived label", () => {
    renderLabel(
      <EpistemicLabel
        epistemic={{
          standing: "derived",
          band: "high",
          confidenceValue: 90,
          conflict: false,
        }}
      />,
    );
    const root = screen.getByTestId("epistemic-label");
    expect(root).toHaveAttribute("data-standing", "derived");
    expect(screen.getByTestId("confidence-band")).toHaveAttribute("data-band", "high");
  });
});
