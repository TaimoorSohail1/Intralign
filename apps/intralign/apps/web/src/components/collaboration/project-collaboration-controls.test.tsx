import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { ProjectCollaborationControls } from "./project-collaboration-controls";

const collaboration = {
  actor_role: "owner",
  plan: {
    name: "Free",
    collaborators_unmetered: true,
    invitations_unmetered: true,
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

    expect(await screen.findByText("People on this project")).toBeInTheDocument();
    expect(screen.getByText("Collaboration and invitations are never metered.")).toBeInTheDocument();
    expect(screen.queryByText(/in this slice/i)).not.toBeInTheDocument();

    vi.mocked(fetch)
      .mockResolvedValueOnce(
        jsonResponse(
          {
            id: "share-created",
            url: "http://localhost:3000/share/snapshot-token",
            expires_at: "2026-08-26T00:00:00Z",
          },
          201,
        ),
      )
      .mockResolvedValueOnce(jsonResponse({
        ...collaboration,
        share_links: [{
          id: "share-created",
          expires_at: "2026-08-26T00:00:00Z",
          revoked_at: null,
          recipient_name: "Amina Khan",
        }],
      }));
    fireEvent.change(screen.getByLabelText("Snapshot recipient name"), {
      target: { value: "Amina Khan" },
    });
    fireEvent.change(screen.getByLabelText("Snapshot recipient email"), {
      target: { value: "amina@example.com" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Create a view-only link" }));

    expect(
      await screen.findByText("A view-only snapshot is ready to share."),
    ).toBeInTheDocument();
    expect(fetch).toHaveBeenNthCalledWith(
      2,
      "/api/projects/project-1/collaboration",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({
          action: "share",
          recipientName: "Amina Khan",
          recipientEmail: "amina@example.com",
        }),
      }),
    );

    vi.mocked(fetch)
      .mockResolvedValueOnce(new Response(null, { status: 204 }))
      .mockResolvedValueOnce(jsonResponse(collaboration));
    fireEvent.click(screen.getByRole("button", { name: "Revoke" }));
    expect(await screen.findByText("The snapshot link was revoked.")).toBeInTheDocument();
    expect(screen.queryByText("View-only snapshot link")).not.toBeInTheDocument();
  });

  it("routes external review creation through an issue-scoped composer", async () => {
    render(<ProjectCollaborationControls projectId="project-1" />);
    fireEvent.click(screen.getByRole("button", { name: "Share" }));
    await screen.findByText("External review request");

    expect(screen.getByText("Start from an issue.")).toBeInTheDocument();
    expect(screen.getByText(/exactly one question and one cited source/i)).toBeInTheDocument();
    expect(screen.queryByLabelText("Reviewer name")).not.toBeInTheDocument();
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  it("offers the five-section snapshot composer without starting analysis", async () => {
    vi.mocked(fetch)
      .mockResolvedValueOnce(jsonResponse(collaboration))
      .mockResolvedValueOnce(jsonResponse({
        state: "current",
        summary: "The current project read.",
        assessment: {
          confidence_band: "Moderate",
          reliability: "Moderate",
          limiting_dimension: "feasibility",
          integrity: {
            level: "Developing",
            limiting_pillar: "Grounding",
            decomposition: [],
            posture: "moment-in-time",
            tracking: "pending-execution",
          },
          issues: [],
        },
      }));
    render(<ProjectCollaborationControls projectId="project-1" />);
    const headerActions = screen.getByRole("group", {
      name: "Project sharing and export",
    });
    expect(headerActions).toContainElement(screen.getByRole("button", { name: "Share" }));
    expect(headerActions).toContainElement(screen.getByRole("button", { name: "Export" }));
    fireEvent.click(screen.getByRole("button", { name: "Export" }));

    expect(
      await screen.findByRole("heading", { name: "Export a snapshot" }),
    ).toBeInTheDocument();
    expect(screen.getByText("Strategic readout — the five-section read")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "§1The read" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /PDF/ })).toHaveAttribute(
      "href",
      "/api/projects/project-1/export",
    );
    expect(fetch).toHaveBeenCalledTimes(2);
  });

  it("invites a project-scoped Delegate-PM without exposing arbitrary roles", async () => {
    render(<ProjectCollaborationControls projectId="project-1" />);
    fireEvent.click(screen.getByRole("button", { name: "Share" }));

    expect(await screen.findByText("Collaboration and invitations are never metered.")).toBeInTheDocument();
    vi.mocked(fetch)
      .mockResolvedValueOnce(
        jsonResponse(
          {
            id: "invitation-1",
            email: "amina@example.com",
            role: "delegate_pm",
            project_id: "project-1",
            status: "pending",
            expires_at: "2026-08-10T00:00:00Z",
          },
          201,
        ),
      )
      .mockResolvedValueOnce(
        jsonResponse({
          ...collaboration,
          invitations: [
            {
              id: "invitation-1",
              email: "amina@example.com",
              role: "delegate_pm",
              project_id: "project-1",
              status: "pending",
              expires_at: "2026-08-10T00:00:00Z",
            },
          ],
        }),
      );

    fireEvent.change(screen.getByLabelText("Email address"), {
      target: { value: "amina@example.com" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Invite" }));

    expect(await screen.findByText("Invitation sent to amina@example.com.")).toBeInTheDocument();
    expect(screen.getByText("Collaboration and invitations are never metered.")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Collaborator" })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Viewer" })).not.toBeInTheDocument();
    expect(fetch).toHaveBeenNthCalledWith(
      2,
      "/api/projects/project-1/collaboration",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({
          action: "invite",
          email: "amina@example.com",
        }),
      }),
    );
  });

  it("keeps owner-only sharing actions unavailable to a Delegate-PM", async () => {
    vi.mocked(fetch).mockResolvedValueOnce(jsonResponse({
      ...collaboration,
      actor_role: "delegate_pm",
      participants: [
        collaboration.participants[0],
        { id: "delegate", display_name: "Amina", role: "delegate_pm" },
      ],
    }));

    render(<ProjectCollaborationControls projectId="project-1" />);
    fireEvent.click(screen.getByRole("button", { name: "Share" }));

    expect(await screen.findByText("People on this project")).toBeInTheDocument();
    expect(screen.getByText("Amina")).toBeInTheDocument();
    expect(screen.queryByLabelText("Email address")).not.toBeInTheDocument();
    expect(screen.queryByText("Share link — a view-only snapshot of this project"))
      .not.toBeInTheDocument();
    expect(screen.queryByText("External review request")).not.toBeInTheDocument();
    expect(screen.queryByText("Active access")).not.toBeInTheDocument();
  });

  it("shows a retry path when governed access cannot be loaded", async () => {
    vi.mocked(fetch)
      .mockResolvedValueOnce(jsonResponse({ message: "Service unavailable" }, 503))
      .mockResolvedValueOnce(jsonResponse(collaboration));

    render(<ProjectCollaborationControls projectId="project-1" />);
    fireEvent.click(screen.getByRole("button", { name: "Share" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("Service unavailable");
    fireEvent.click(screen.getByRole("button", { name: "Retry" }));
    expect(await screen.findByText("People on this project")).toBeInTheDocument();
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
    await screen.findByText(/1 active snapshot link/);

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

  it("shows that a reviewer verdict has already entered the governed flow", async () => {
    const responded = {
      ...collaboration,
      reviews: [
        {
          id: "review-1",
          reviewer_name: "Amina Khan",
          expires_at: "2026-08-26T00:00:00Z",
          responded_at: "2026-07-28T00:00:00Z",
          response_id: "response-1",
          response_kind: "approve",
          response_body: "The steering committee approved the pilot.",
          analysis_run_id: null,
        },
      ],
    };
    vi.mocked(fetch).mockResolvedValueOnce(jsonResponse(responded));
    render(<ProjectCollaborationControls projectId="project-1" />);
    fireEvent.click(screen.getByRole("button", { name: "Share" }));

    expect(await screen.findByText("Reviewer responses")).toBeInTheDocument();
    expect(screen.getByText("The steering committee approved the pilot.")).toBeInTheDocument();

    expect(screen.getByText("Recorded")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Use as project evidence" })).not.toBeInTheDocument();
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  it("keeps the post-review collaborator invitation as a user-controlled draft", async () => {
    const responded = {
      ...collaboration,
      reviews: [
        {
          id: "review-1",
          reviewer_name: "Amina Khan",
          reviewer_email: "amina@example.com",
          expires_at: "2026-08-26T00:00:00Z",
          responded_at: "2026-07-28T00:00:00Z",
          response_id: "response-1",
          response_kind: "approve",
          response_body: "The steering committee approved the pilot.",
          analysis_run_id: "run-1",
        },
      ],
    };
    vi.mocked(fetch).mockResolvedValueOnce(jsonResponse(responded));
    render(<ProjectCollaborationControls projectId="project-1" />);
    fireEvent.click(screen.getByRole("button", { name: "Share" }));

    expect(await screen.findByText("Invitation draft — not sent")).toBeInTheDocument();
    expect(fetch).toHaveBeenCalledTimes(1);

    vi.mocked(fetch)
      .mockResolvedValueOnce(jsonResponse({ id: "invitation-1" }, 201))
      .mockResolvedValueOnce(jsonResponse(collaboration));
    fireEvent.click(screen.getByRole("button", { name: "Send invitation to Amina Khan" }));

    expect(await screen.findByText("Invitation sent to amina@example.com.")).toBeInTheDocument();
    expect(fetch).toHaveBeenNthCalledWith(
      2,
      "/api/projects/project-1/collaboration",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ action: "invite", email: "amina@example.com" }),
      }),
    );

  });
});
