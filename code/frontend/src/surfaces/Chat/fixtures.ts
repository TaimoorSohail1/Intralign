/**
 * OSLO Chat fixtures (DTM-0029, CHAT-01…04, IC-WE-DISCLOSE).
 *
 * CHAT-COMMAND ENDPOINT DATA FINDING (binding — see the worker report):
 * there is NO chat send/trigger endpoint and NO mutation endpoint of ANY kind in the
 * DTM-0018 generated client (`src/api/generated/**`): the surface exposes only GET reads
 * (confidence, caf, findings, recommendations, analysis-runs, notifications, projects,
 * acceptance) — no `ChatSession` / `ChatExchange` resource, no Advise/Deep-Pass trigger.
 * Per the ANTI_ASSUMPTION protocol we do NOT invent a canonical write: Chat renders the
 * conversation + an input, and a send appends an EPHEMERAL, NON-CANONICAL exchange marked
 * "pending" (it would route to the existing Advise/Deep-Pass trigger when exposed). The
 * dependency is FLAGGED, not filled.
 *
 * `ChatExchange` here is the NON-CANONICAL presentation shape the surface renders (canon
 * vocab: `ChatSession` / `ChatExchange`, non-canonical OBS-WE events) — it is NOT a DTO
 * and writes nothing.
 */
import type { ChatExchange, ChatContext } from "./Chat";

export const PROJECT_ID = "proj-001";

/** A seed transcript — OSLO explanation answers sourced from EXISTING understanding. */
export const seedExchangesFixture: ChatExchange[] = [
  {
    exchange_id: "ex-1",
    role: "user",
    text: "Why is alignment low for this project?",
    status: "delivered",
  },
  {
    exchange_id: "ex-2",
    role: "oslo",
    // Explanation from existing data; reliability-qualified; computes nothing.
    text:
      "Two stakeholders recorded conflicting go-live dates, so OSLO has lower trust in its understanding of alignment. This explains an existing finding — it is not a new assessment.",
    status: "delivered",
  },
];

/** Context inherited when Chat is launched from a Finding. */
export const findingContextFixture: ChatContext = {
  kind: "finding",
  id: "f-1",
  label: "Conflicting go-live dates",
};

/** Context inherited when Chat is launched from a Recommendation. */
export const recommendationContextFixture: ChatContext = {
  kind: "recommendation",
  id: "r-1",
  label: "Confirm the go-live date with both stakeholders",
};

/** Context inherited when Chat is launched from an Artifact. */
export const artifactContextFixture: ChatContext = {
  kind: "artifact",
  id: "artf-1",
  label: "Scope statement",
};
