import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

const { useFormStatus } = vi.hoisted(() => ({
  useFormStatus: vi.fn(() => ({
    action: null,
    data: null,
    method: "get",
    pending: false,
  })),
}));

vi.mock("react-dom", async (importOriginal) => ({
  ...(await importOriginal<typeof import("react-dom")>()),
  useFormStatus,
}));

import { WelcomeSubmitButton } from "./welcome-submit";

afterEach(() => {
  useFormStatus.mockReset();
  useFormStatus.mockReturnValue({ action: null, data: null, method: "get", pending: false });
});

describe("WelcomeSubmitButton", () => {
  it("prevents duplicate project creation while the welcome action is pending", () => {
    useFormStatus.mockReturnValue({ action: null, data: null, method: "post", pending: true });

    render(<WelcomeSubmitButton />);

    expect(screen.getByRole("button", { name: "Starting your outcome" })).toBeDisabled();
  });
});
