import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

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
    expect(screen.getByRole("checkbox", { name: "Stay signed in on this device" })).toBeChecked();
    expect(screen.getByRole("button", { name: "Create account & continue" })).toBeEnabled();
  });

  it("blocks weak and mismatched password confirmation", () => {
    const action = vi.fn();
    render(
      <ActivationForm
        action={action}
        email="new.member@example.com"
        token="activation-token"
        workspaceName="OSLO Product Grill"
      />,
    );

    const password = screen.getByLabelText("Choose a password");
    expect(password).toHaveAttribute("minlength", "12");
    fireEvent.change(password, { target: { value: "ActivationTest123!" } });
    fireEvent.change(screen.getByLabelText("Confirm password"), {
      target: { value: "DifferentPassword123!" },
    });
    fireEvent.submit(screen.getByRole("button", { name: /Create account/ }).closest("form")!);

    expect(screen.getByRole("alert")).toHaveTextContent("Passwords do not match");
    expect(action).not.toHaveBeenCalled();
  });
});
