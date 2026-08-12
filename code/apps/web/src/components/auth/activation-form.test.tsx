import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import { ActivationForm } from "./activation-form";

afterEach(cleanup);

describe("ActivationForm", () => {
  it("locks the invited email and keeps the device signed in by default", () => {
    render(
      <ActivationForm
        email="new.member@example.com"
        token="activation-token"
        workspaceName="OSLO Product Grill"
      />,
    );

    expect(screen.getByLabelText("Email (from your invite)")).toHaveValue(
      "new.member@example.com",
    );
    expect(screen.getByLabelText("Email (from your invite)")).toHaveAttribute(
      "readonly",
    );
    expect(screen.getByLabelText("Display name")).toHaveValue("New Member");
    expect(screen.getAllByRole("radio")).toHaveLength(4);
    expect(screen.getByRole("radio", { name: /I run the plan/i })).toBeChecked();
    expect(screen.getByRole("checkbox", { name: "Stay signed in on this device" })).toBeChecked();
    expect(screen.getByRole("button", { name: "Create account & continue" })).toBeEnabled();
    expect(screen.getByRole("link", { name: /Back to the invitation/ })).toHaveAttribute(
      "href",
      "/activate?token=activation-token",
    );
  });

  it("matches the prototype role choice and single-password form", () => {
    render(
      <ActivationForm
        email="new.member@example.com"
        token="activation-token"
        workspaceName="OSLO Product Grill"
      />,
    );

    const password = screen.getByLabelText("Choose a password");
    expect(password).toHaveAttribute("minlength", "12");
    expect(screen.queryByLabelText("Confirm password")).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("radio", { name: /I own the outcome/i }));
    expect(screen.getByRole("radio", { name: /I own the outcome/i })).toBeChecked();
  });
});
