import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { ReviewerResponseForm } from "./reviewer-response-form";

describe("ReviewerResponseForm", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ status: "recorded" }), {
          status: 201,
          headers: { "content-type": "application/json" },
        }),
      ),
    );
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it("records an attested response without starting analysis", async () => {
    render(<ReviewerResponseForm token="review token" />);
    fireEvent.click(screen.getByLabelText("Suggest alternative"));
    fireEvent.change(screen.getByLabelText("Reviewer note"), {
      target: { value: "Sequence the pilot before the global rollout." },
    });
    fireEvent.click(screen.getByRole("button", { name: "Submit review" }));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "/api/public/review/review%20token",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({
            kind: "suggest_alternative",
            body: "Sequence the pilot before the global rollout.",
          }),
        }),
      );
    });
    expect(screen.getByRole("heading", { name: "Thank you for the review" })).toBeInTheDocument();
    expect(
      screen.getByText(/project team can decide whether to add it as project evidence/i),
    ).toBeInTheDocument();
    expect(screen.getByText(/No account or workspace seat was created/)).toBeInTheDocument();
  });

  it("surfaces a failed review submission without losing the form", async () => {
    vi.mocked(fetch).mockResolvedValueOnce(
      new Response(JSON.stringify({ message: "This review link has expired." }), {
        status: 410,
        headers: { "content-type": "application/json" },
      }),
    );
    render(<ReviewerResponseForm token="expired" />);
    fireEvent.change(screen.getByLabelText("Reviewer note"), {
      target: { value: "Looks good." },
    });
    fireEvent.click(screen.getByRole("button", { name: "Submit review" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("This review link has expired.");
    expect(screen.getByLabelText("Reviewer note")).toHaveValue("Looks good.");
  });
});
