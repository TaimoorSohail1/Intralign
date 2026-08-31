/**
 * DTM-0029 — OSLO Chat (CHAT-01…04, IC-WE-DISCLOSE).
 *
 * A conversation surface that CONSUMES cognition (Explain / Clarify) and may TRIGGER it
 * (Improve → Advise + Deep Pass) — but writes NO canonical, mutates NO artifact, changes
 * NO assessment (Critical). It renders exchanges (non-canonical `ChatExchange`), an input,
 * the Explain/Clarify/Improve affordances, and inherits context when launched from an
 * issue/recommendation/artifact/finding.
 *
 * THE CRITICAL NEGATIVES (the heart of this slice — fail review if absent):
 *   - Chat writes NO canonical and mutates NO governed object: there is no write/mutation
 *     call in the generated client, so sending appends a NON-CANONICAL, ephemeral
 *     exchange marked "pending" — it never calls a write, never mutates a finding/
 *     recommendation/assessment, never self-accepts.
 *   - Chat changes NO assessment: nothing the user does here alters confidence/CAF.
 */
import { describe, it, expect, vi, beforeEach } from "vitest";
import { screen, within, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { renderChat } from "./testHarness";
import {
  PROJECT_ID,
  seedExchangesFixture,
  findingContextFixture,
} from "./fixtures";

// Import the READ API modules so a test can assert — structurally — that they remain
// read-only: Chat reaches NO canonical-write hook (accept/finding-mutation/etc.). The
// ONLY write Chat performs is the chat ENDPOINT (the non-canonical chat path).
import * as findingsApi from "../../api/generated/findings/findings";
import * as recommendationsApi from "../../api/generated/recommendations/recommendations";
import * as acceptanceApi from "../../api/generated/acceptance/acceptance";
import * as confidenceApi from "../../api/generated/confidence/confidence";
import * as analysisRunsApi from "../../api/generated/analysis-runs/analysis-runs";
import * as projectsApi from "../../api/generated/projects/projects";
import * as notificationsApi from "../../api/generated/notifications/notifications";

// ── Mock the chat ENDPOINT (DTM-0037). Chat now sends THROUGH this — the non-canonical
//    chat path. The mock captures the variables and lets a test drive onSuccess. ──────
const chatMutate = vi.fn();
vi.mock("../../api/generated/chat/chat", () => ({
  useChatV1ProjectsProjectIdChatPost: () => ({
    mutate: (
      vars: { projectId: string; data: { message: string; intent?: string } },
      opts?: {
        onSuccess?: (res: { data: unknown }) => void;
        onError?: (e: unknown) => void;
      },
    ) => {
      chatMutate(vars);
      // Simulate the endpoint's NON-CANONICAL ChatExchange response (OSLO's phrasing).
      opts?.onSuccess?.({
        data: {
          exchange_id: `srv-${chatMutate.mock.calls.length}`,
          project_id: vars.projectId,
          user_message: vars.data.message,
          response: "OSLO explains from existing understanding; nothing changed.",
          intent: vars.data.intent ?? "explain",
          epistemic_state: "non-canonical",
          model_or_rule_version: "test",
          triggered_run: vars.data.intent === "improve" ? "run-deep-1" : null,
        },
      });
    },
    isPending: false,
  }),
}));

import { Chat } from "./Chat";
import { ChatRoute } from "./ChatRoute";

function mount(opts?: { search?: string }) {
  return renderChat(
    <Chat projectId={PROJECT_ID} initialExchanges={seedExchangesFixture} />,
    { projectId: PROJECT_ID, search: opts?.search },
  );
}

/**
 * Mount the real ChatRoute so context inheritance flows through the route search
 * (`context_kind`/`context_id`/`context_label`) → the surface, exactly as in the app.
 */
function mountRoute(search: string) {
  return renderChat(<ChatRoute />, { projectId: PROJECT_ID, search });
}

beforeEach(() => {
  chatMutate.mockReset();
});

describe("Chat — renders the conversation + input + affordances", () => {
  it("renders the chat surface", async () => {
    await mount();
    expect(screen.getByTestId("chat")).toBeInTheDocument();
  });

  it("renders the seed exchanges (non-canonical ChatExchange)", async () => {
    await mount();
    const transcript = screen.getByTestId("chat-transcript");
    const items = within(transcript).getAllByTestId("chat-exchange");
    expect(items.length).toBe(seedExchangesFixture.length);
  });

  it("renders an input affordance", async () => {
    await mount();
    expect(screen.getByTestId("chat-input")).toBeInTheDocument();
  });

  it("renders Explain / Clarify / Improve affordances", async () => {
    await mount();
    expect(screen.getByTestId("chat-affordance-explain")).toBeInTheDocument();
    expect(screen.getByTestId("chat-affordance-clarify")).toBeInTheDocument();
    expect(screen.getByTestId("chat-affordance-improve")).toBeInTheDocument();
  });
});

describe("Chat — context inheritance (launched from a source object)", () => {
  it("inherits a Finding context from the URL search params", async () => {
    await mountRoute(
      `?context_kind=finding&context_id=${findingContextFixture.id}&context_label=${encodeURIComponent(
        findingContextFixture.label!,
      )}`,
    );
    const ctx = screen.getByTestId("chat-context");
    expect(ctx.textContent ?? "").toMatch(/finding/i);
    expect(ctx).toHaveAttribute("data-context-kind", "finding");
    expect(ctx).toHaveAttribute("data-context-id", findingContextFixture.id);
  });

  it("shows a neutral 'whole project' context when launched without a source", async () => {
    await mountRoute("");
    const ctx = screen.getByTestId("chat-context");
    expect(ctx).toHaveAttribute("data-context-kind", "project");
  });
});

describe("Chat — empty state", () => {
  it("renders a neutral empty state when there is no conversation yet", async () => {
    const { container } = await renderChat(
      <Chat projectId={PROJECT_ID} initialExchanges={[]} />,
      { projectId: PROJECT_ID },
    );
    expect(within(container).getByTestId("chat-empty")).toBeInTheDocument();
  });
});

describe("Chat — sending (via the chat ENDPOINT, DTM-0037)", () => {
  it("sends the message THROUGH the chat endpoint (the non-canonical chat path)", async () => {
    await mount();
    const input = within(screen.getByTestId("chat-input")).getByRole("textbox");
    fireEvent.change(input, { target: { value: "What drives feasibility here?" } });
    fireEvent.click(screen.getByTestId("chat-send"));
    // the endpoint mutation is the path — called with the project + message + intent
    expect(chatMutate).toHaveBeenCalledTimes(1);
    expect(chatMutate).toHaveBeenCalledWith(
      expect.objectContaining({
        projectId: PROJECT_ID,
        data: expect.objectContaining({
          message: "What drives feasibility here?",
          intent: "explain",
        }),
      }),
    );
    // the user message appears in the transcript
    const transcript = screen.getByTestId("chat-transcript");
    expect(within(transcript).getByText(/what drives feasibility here\?/i)).toBeInTheDocument();
  });

  it("appends OSLO's phrased response from the endpoint result (never fabricated locally)", async () => {
    await mount();
    const input = within(screen.getByTestId("chat-input")).getByRole("textbox");
    fireEvent.change(input, { target: { value: "Explain alignment" } });
    fireEvent.click(screen.getByTestId("chat-send"));
    const transcript = screen.getByTestId("chat-transcript");
    // OSLO's response (from the mocked endpoint) is rendered
    expect(
      within(transcript).getByText(/oslo explains from existing understanding/i),
    ).toBeInTheDocument();
  });

  it("Improve sends with intent=improve and discloses the triggered Deep Pass honestly", async () => {
    await mount();
    fireEvent.click(screen.getByTestId("chat-affordance-improve"));
    expect(chatMutate).toHaveBeenCalledWith(
      expect.objectContaining({ data: expect.objectContaining({ intent: "improve" }) }),
    );
    const notice = screen.getByTestId("chat-pending-notice");
    expect(notice.textContent ?? "").toMatch(/deep pass|reanalysis/i);
  });
});

// ── THE CRITICAL NEGATIVES — Chat writes no canonical / mutates nothing / changes no
//    assessment. These are the spine of the slice. ────────────────────────────────────
describe("Chat — CRITICAL negatives: no canonical write / no mutation / no assessment change", () => {
  it("the READ modules stay read-only — Chat reaches NO canonical-write hook", () => {
    // The findings/recommendations/acceptance/confidence/analysis-runs/projects/
    // notifications READ modules are GET-only (Orval names a GET op "…Get"). Chat
    // imports NONE of the command modules (accept/finding-mutation/etc.); the ONLY
    // write it performs is the chat ENDPOINT — the non-canonical chat path. So Chat
    // structurally CANNOT write canonical or mutate a governed object.
    const readModuleExports = [
      ...Object.keys(findingsApi),
      ...Object.keys(recommendationsApi),
      ...Object.keys(acceptanceApi),
      ...Object.keys(confidenceApi),
      ...Object.keys(analysisRunsApi),
      ...Object.keys(projectsApi),
      ...Object.keys(notificationsApi),
    ];
    const hookExports = readModuleExports.filter((name) => name.startsWith("use"));
    expect(hookExports.length).toBeGreaterThan(0);
    for (const name of hookExports) {
      // Every hook in these READ modules is a GET read — none is a canonical-write
      // hook Chat could reach.
      expect(name).toMatch(/Get$/);
    }
  });

  it("sending mutates NO governed object — only ephemeral conversation display state changes", async () => {
    await mount();
    // Snapshot the governed objects' rendered identity is irrelevant here; assert the
    // surface mutates nothing beyond the transcript: after send, the only DOM growth is a
    // new exchange + a pending notice — no governed-object state ('accepted'/'resolved'/
    // 'applied'/'saved') appears anywhere.
    const input = within(screen.getByTestId("chat-input")).getByRole("textbox");
    fireEvent.change(input, { target: { value: "Accept this recommendation" } });
    fireEvent.click(screen.getByTestId("chat-send"));
    const surface = screen.getByTestId("chat");
    expect(surface.textContent ?? "").not.toMatch(
      /\baccepted\b|\bresolved\b|\bapplied\b|\bsaved\b|\bapproved\b/i,
    );
  });

  it("exposes NO accept / approve / govern / write / save control (it consumes/triggers, never records canon)", async () => {
    const { container } = await mount();
    const controls = [
      ...container.querySelectorAll("button"),
      ...container.querySelectorAll('[role="button"]'),
    ];
    const forbidden =
      /\baccept\b|\bapprove\b|\bgovern\b|\bsign[- ]?off\b|\bratif/i;
    for (const el of controls) {
      const text = `${el.textContent ?? ""} ${el.getAttribute("aria-label") ?? ""}`;
      expect(text).not.toMatch(forbidden);
    }
  });

  it("the Improve affordance does NOT mutate — it routes to the existing Advise/Deep-Pass trigger (flagged pending)", async () => {
    await mount();
    fireEvent.click(screen.getByTestId("chat-affordance-improve"));
    // It surfaces a pending/route notice; it does NOT claim an applied change or mutate.
    const notice = screen.getByTestId("chat-pending-notice");
    expect(notice.textContent ?? "").toMatch(/pending|advise|deep pass|when available/i);
    // It never claims to have changed/applied/resolved anything.
    const surface = screen.getByTestId("chat");
    expect(surface.textContent ?? "").not.toMatch(/\bapplied\b|\bresolved\b|\baccepted\b|\bsaved\b/i);
  });

  it("clarify is information-capture only — never claims an instant assessment change", async () => {
    await mount();
    fireEvent.click(screen.getByTestId("chat-affordance-clarify"));
    const surface = screen.getByTestId("chat");
    const text = (surface.textContent ?? "").toLowerCase();
    // honest: routes through information → reanalysis; no instant change.
    expect(text).not.toMatch(/\bupdated the assessment\b|\bchanged confidence\b|\bresolved the finding\b/);
  });

  it("never shows a score / percentage / project-health verdict", async () => {
    await mount();
    const surface = screen.getByTestId("chat");
    const text = surface.textContent ?? "";
    expect(text).not.toMatch(/%/);
    expect(text).not.toMatch(/\bhealth\b/i);
    expect(text).not.toMatch(/\bon[- ]?track\b/i);
  });
});

// ── Contextual handoff into the structured surfaces (Chat complements, never replaces) ──
describe("Chat — contextual handoff to the Finding Panel", () => {
  it("offers an 'Open the Finding Panel' handoff when in a Finding context", async () => {
    await mountRoute(
      `?context_kind=finding&context_id=${findingContextFixture.id}&context_label=${encodeURIComponent(
        findingContextFixture.label!,
      )}`,
    );
    const link = screen.getByTestId("chat-open-finding");
    expect(link).toHaveAttribute(
      "href",
      `/projects/${PROJECT_ID}/findings/${findingContextFixture.id}`,
    );
  });
});
