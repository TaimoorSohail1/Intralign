import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { ProjectCollaborationControls } from "./project-collaboration-controls";

const collaboration = {
  actor_role: "owner",
  plan: {
    name: "Free",
    collaborator_seats: 3,
    collaborator_seats_used: 1,
    monthly_invites: 2,
    monthly_invites_used: 0,
    viewers_unlimited: true,
    reviewers_unmetered: true,
  },
  participants: [{ id: "owner", display_name: "Taimoor", role: "owner" }],
  invitations: [],
  share_links: [],
  reviews: [],
};

function jsonResponse(payload: unknown, status = 200) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { "content-type": "application/json" },
  });
}

describe("ProjectCollaborationControls", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse(collaboration)));
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it("loads governed sharing state and creates a distinct snapshot link", async () => {
    render(<ProjectCollaborationControls projectId="project-1" />);
    fireEvent.click(screen.getByRole("button", { name: "Share" }));

    expect(await screen.findByText("People with workspace access")).toBeInTheDocument();
    expect(screen.getByText("1/3 seats")).toBeInTheDocument();

    vi.mocked(fetch)
      .mockResolvedValueOnce(
        jsonResponse(
          {
            url: "http://localhost:3000/share/snapshot-token",
            expires_at: "2026-08-26T00:00:00Z",
          },
          201,
        ),
      )
      .mockResolvedValueOnce(jsonResponse(collaboration));
    fireEvent.click(screen.getByRole("button", { name: "Create snapshot link" }));

    expect(
      await screen.findByText("A read-only snapshot is ready to share."),
    ).toBeInTheDocument();
    expect(fetch).toHaveBeenNthCalledWith(
      2,
      "/api/projects/project-1/collaboration",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({
          action: "share",
          reviewerName: "",
          reviewerEmail: null,
        }),
      }),
    );
  });

  it("creates an unmetered external review link with reviewer identity", async () => {
    render(<ProjectCollaborationControls projectId="project-1" />);
    fireEvent.click(screen.getByRole("button", { name: "Share" }));
    await screen.findByText("External review");

    vi.mocked(fetch)
      .mockResolvedValueOnce(
        jsonResponse(
          {
            url: "http://localhost:3000/review/review-token",
            expires_at: "2026-08-10T00:00:00Z",
          },
          201,
        ),
      )
      .mockResolvedValueOnce(jsonResponse(collaboration));
    fireEvent.change(screen.getByLabelText("Reviewer name"), {
      target: { value: "Amina Khan" },
    });
    fireEvent.change(screen.getByLabelText(/Reviewer email/), {
      target: { value: "amina@example.com" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Create review link" }));

    await waitFor(() => {
      expect(fetch).toHaveBeenNthCalledWith(
        2,
        "/api/projects/project-1/collaboration",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({
            action: "review",
            reviewerName: "Amina Khan",
            reviewerEmail: "amina@example.com",
          }),
        }),
      );
    });
  });

  it("offers a read-only PDF export without starting analysis", async () => {
    render(<ProjectCollaborationControls projectId="project-1" />);
    const headerActions = screen.getByRole("group", {
      name: "Project sharing and export",
    });
    expect(headerActions).toContainElement(screen.getByRole("button", { name: "Share" }));
    expect(headerActions).toContainElement(screen.getByRole("button", { name: "Export" }));
    fireEvent.click(screen.getByRole("button", { name: "Export" }));

    expect(
      await screen.findByRole("heading", { name: "Project snapshot · PDF" }),
    ).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Download PDF" })).toHaveAttribute(
      "href",
      "/api/projects/project-1/export",
    );
    expect(fetch).toHaveBeenCalledTimes(0);
  });

  it("lets an owner invite a collaborator and refreshes governed plan usage", async () => {
    render(<ProjectCollaborationControls projectId="project-1" />);
    fireEvent.click(screen.getByRole("button", { name: "Share" }));

    expect(await screen.findByText("0/2 this month")).toBeInTheDocument();
    vi.mocked(fetch)
      .mockResolvedValueOnce(
        jsonResponse(
          {
            id: "invitation-1",
            email: "amina@example.com",
            role: "collaborator",
            status: "pending",
            expires_at: "2026-08-10T00:00:00Z",
          },
          201,
        ),
      )
      .mockResolvedValueOnce(
        jsonResponse({
          ...collaboration,
          plan: { ...collaboration.plan, monthly_invites_used: 1 },
          invitations: [
            {
              id: "invitation-1",
              email: "amina@example.com",
              role: "collaborator",
              status: "pending",
              expires_at: "2026-08-10T00:00:00Z",
            },
          ],
        }),
      );

    fireEvent.change(screen.getByLabelText("Email address"), {
      target: { value: "amina@example.com" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Send invitation" }));

    expect(await screen.findByText("Invitation sent to amina@example.com.")).toBeInTheDocument();
    expect(await screen.findByText("1/2 this month")).toBeInTheDocument();
    expect(fetch).toHaveBeenNthCalledWith(
      2,
      "/api/projects/project-1/collaboration",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({
          action: "invite",
          email: "amina@example.com",
          role: "collaborator",
        }),
      }),
    );
  });

  it("shows a retry path when governed access cannot be loaded", async () => {
    vi.mocked(fetch)
      .mockResolvedValueOnce(jsonResponse({ message: "Service unavailable" }, 503))
      .mockResolvedValueOnce(jsonResponse(collaboration));

    render(<ProjectCollaborationControls projectId="project-1" />);
    fireEvent.click(screen.getByRole("button", { name: "Share" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("Service unavailable");
    fireEvent.click(screen.getByRole("button", { name: "Retry" }));
    expect(await screen.findByText("People with workspace access")).toBeInTheDocument();
  });

  it("revokes an active snapshot without affecting project analysis", async () => {
    vi.mocked(fetch).mockResolvedValueOnce(
      jsonResponse({
        ...collaboration,
        share_links: [
          {
            id: "share-1",
            expires_at: "2026-08-26T00:00:00Z",
            revoked_at: null,
          },
        ],
      }),
    );
    render(<ProjectCollaborationControls projectId="project-1" />);
    fireEvent.click(screen.getByRole("button", { name: "Share" }));
    await screen.findByText("Active access");

    vi.mocked(fetch)
      .mockResolvedValueOnce(new Response(null, { status: 204 }))
      .mockResolvedValueOnce(jsonResponse(collaboration));
    fireEvent.click(screen.getByRole("button", { name: "Revoke" }));

    expect(await screen.findByText("The snapshot link was revoked.")).toBeInTheDocument();
    expect(fetch).toHaveBeenNthCalledWith(
      2,
      "/api/projects/project-1/collaboration",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ action: "revoke_share", linkId: "share-1" }),
      }),
    );
  });
});
