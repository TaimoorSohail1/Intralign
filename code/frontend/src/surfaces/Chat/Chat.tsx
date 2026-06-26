/**
 * DTM-0029 — OSLO Chat (CHAT-01…04, IC-WE-DISCLOSE E-Disclose / DL-047).
 *
 * A conversation surface that CONSUMES cognition (Explain / Clarify) and may TRIGGER it
 * (Improve → Advise + Deep Pass). The CRITICAL invariant (CHAT-1…3, decision #10): Chat
 * writes NO canonical, mutates NO artifact, and changes NO assessment. It renders the
 * transcript (non-canonical `ChatExchange`), an input, and the Explain/Clarify/Improve
 * affordances, and inherits context when launched from an issue/recommendation/artifact/
 * finding.
 *
 * CHAT ENDPOINT (DTM-0039 — replaces the flagged ephemeral stub): a send / Explain /
 * Clarify / Improve now calls `POST /projects/{id}/chat` (the generated
 * `useChat…` mutation). That endpoint is the NON-CANONICAL chat path: it appends a
 * `ChatExchange` and — for Improve — TRIGGERS the frozen Deep Pass. It writes NO
 * canonical, mutates NO artifact, changes NO assessment (the backend enforces this; the
 * surface performs no local canonical write either). The user turn renders immediately;
 * OSLO's phrased `response` is appended from the endpoint result.
 *
 * Honest behavior (spec §G/§O): clarification is information-capture that feeds the NEXT
 * reanalysis — Chat never implies an instant assessment change, never fabricates an
 * answer, never shows a score/percentage/health verdict.
 */
import { useMemo, useState } from "react";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Chip from "@mui/material/Chip";
import Alert from "@mui/material/Alert";
import { Link } from "@tanstack/react-router";

import { useChatV1ProjectsProjectIdChatPost } from "../../api/generated/chat/chat";
import type {
  ChatRequestIntent,
  ChatExchange as ChatExchangeDTO,
} from "../../api/generated/oSLORelease1API.schemas";

/** Who authored a turn in the transcript. */
export type ChatRole = "user" | "oslo";

/** Display lifecycle of a turn. `pending` = sent, awaiting the (unexposed) chat seam. */
export type ChatExchangeStatus = "delivered" | "pending";

/**
 * NON-CANONICAL conversation turn the surface renders (canon vocab: `ChatExchange`). NOT
 * a DTO; writes nothing. Ephemeral display state only.
 */
export interface ChatExchange {
  exchange_id: string;
  role: ChatRole;
  text: string;
  status: ChatExchangeStatus;
}

/** The kinds of source object Chat can inherit context from (read-only). */
export type ChatContextKind =
  | "project"
  | "finding"
  | "issue"
  | "recommendation"
  | "artifact";

/** Inherited context — used only to present and route relevantly; never to act/govern. */
export interface ChatContext {
  kind: ChatContextKind;
  id?: string;
  label?: string;
}

export interface ChatProps {
  projectId: string;
  /** The inherited context (read from the route search by ChatRoute). */
  context?: ChatContext;
  /** Seed transcript (presentation/history). Empty ⇒ neutral empty state. */
  initialExchanges?: ChatExchange[];
}

const CONTEXT_NOUN: Record<ChatContextKind, string> = {
  project: "this project",
  finding: "this finding",
  issue: "this issue",
  recommendation: "this recommendation",
  artifact: "this artifact",
};

/** One transcript turn. */
function ExchangeRow({ exchange }: { exchange: ChatExchange }) {
  const mine = exchange.role === "user";
  return (
    <Box
      data-testid="chat-exchange"
      data-role={exchange.role}
      data-status={exchange.status}
      sx={{ display: "flex", justifyContent: mine ? "flex-end" : "flex-start" }}
    >
      <Paper
        variant="outlined"
        sx={{
          p: 1.5,
          maxWidth: "80%",
          bgcolor: mine ? "action.hover" : "background.paper",
        }}
      >
        <Typography variant="caption" color="text.secondary" display="block">
          {mine ? "You" : "OSLO"}
        </Typography>
        <Typography variant="body2">{exchange.text}</Typography>
        {exchange.status === "pending" ? (
          <Chip size="small" variant="outlined" label="Pending" sx={{ mt: 0.5 }} />
        ) : null}
      </Paper>
    </Box>
  );
}

/** Map the surface's inherited context to the endpoint's optional `context` ref. */
function toRequestContext(ctx: ChatContext) {
  if (ctx.kind === "project" || !ctx.id) return undefined;
  return { object_type: ctx.kind, object_id: ctx.id };
}

export function Chat({ projectId, context, initialExchanges = [] }: ChatProps) {
  const ctx: ChatContext = context ?? { kind: "project" };
  const [exchanges, setExchanges] = useState<ChatExchange[]>(initialExchanges);
  const [draft, setDraft] = useState("");
  // The most recent honest disclosure (e.g. Improve triggered a Deep Pass).
  const [pendingNotice, setPendingNotice] = useState<string | null>(null);

  const nextId = useMemo(() => {
    let n = exchanges.length;
    return () => `ex-local-${++n}-${Date.now()}`;
  }, [exchanges.length]);

  // The chat ENDPOINT (DTM-0037): the non-canonical chat path. On success it returns a
  // `ChatExchange` whose `response` is OSLO's phrased reply — appended to the transcript.
  // It writes no canonical and changes no assessment (backend-enforced); the surface
  // performs no local canonical write either.
  const chatM = useChatV1ProjectsProjectIdChatPost();

  /**
   * Send a turn THROUGH the chat endpoint. The user turn renders immediately (marked
   * pending until the endpoint responds), then OSLO's phrased `response` is appended
   * from the result. Improve triggers a Deep Pass server-side (disclosed honestly).
   */
  function sendViaEndpoint(message: string, intent: ChatRequestIntent) {
    const trimmed = message.trim();
    if (!trimmed) return;
    const userTurnId = nextId();
    setExchanges((prev) => [
      ...prev,
      { exchange_id: userTurnId, role: "user", text: trimmed, status: "pending" },
    ]);
    setPendingNotice(null);
    chatM.mutate(
      {
        projectId,
        data: { message: trimmed, intent, context: toRequestContext(ctx) },
      },
      {
        onSuccess: (res) => {
          const exchange = res.data as ChatExchangeDTO;
          setExchanges((prev) => [
            // mark the user turn delivered…
            ...prev.map((e) =>
              e.exchange_id === userTurnId ? { ...e, status: "delivered" as const } : e,
            ),
            // …and append OSLO's phrased response (semantic; never a canonical output).
            {
              exchange_id: exchange.exchange_id,
              role: "oslo" as const,
              text: exchange.response,
              status: "delivered" as const,
            },
          ]);
          if (intent === "improve" && exchange.triggered_run) {
            setPendingNotice(
              "Improve triggered a Deep Pass reanalysis — Chat itself recorded nothing and " +
                "changed no assessment; the reanalysis will update OSLO's understanding when it " +
                "completes.",
            );
          }
        },
        onError: () => {
          setPendingNotice(
            "That message couldn't be delivered just now. Nothing was recorded and no " +
              "assessment changed — please try again.",
          );
        },
      },
    );
  }

  function handleSend() {
    if (!draft.trim()) return;
    // Default intent `explain` — the read-only intent (it triggers nothing).
    sendViaEndpoint(draft, "explain");
    setDraft("");
  }

  function handleExplain() {
    sendViaEndpoint(`Explain ${CONTEXT_NOUN[ctx.kind]}`, "explain");
  }

  function handleClarify() {
    sendViaEndpoint(`Clarify ${CONTEXT_NOUN[ctx.kind]}`, "clarify");
  }

  function handleImprove() {
    sendViaEndpoint(`Improve ${CONTEXT_NOUN[ctx.kind]}`, "improve");
  }

  const isEmpty = exchanges.length === 0;

  return (
    <Box data-testid="chat" sx={{ py: 1, display: "flex", flexDirection: "column", gap: 2 }}>
      <Box>
        <Typography variant="h5" component="h2" gutterBottom data-testid="surface-title">
          Ask OSLO
        </Typography>
        <Typography variant="body2" color="text.secondary">
          A conversation about your project&apos;s understanding. OSLO explains and clarifies
          from what it already understands; it records nothing here and changes no
          assessment — only reanalysis does that.
        </Typography>
      </Box>

      {/* Inherited context — presentation + routing only; never acts on it. */}
      <Box
        data-testid="chat-context"
        data-context-kind={ctx.kind}
        data-context-id={ctx.id}
        sx={{ display: "flex", alignItems: "center", gap: 1, flexWrap: "wrap" }}
      >
        <Typography variant="caption" color="text.secondary">
          Talking about:
        </Typography>
        <Chip
          size="small"
          variant="outlined"
          label={
            ctx.kind === "project"
              ? "the whole project"
              : `${ctx.kind}${ctx.label ? `: ${ctx.label}` : ""}`
          }
        />
        {/* Contextual handoff into the structured surface (Chat complements, never replaces). */}
        {ctx.kind === "finding" && ctx.id ? (
          <Link
            to="/projects/$projectId/findings/$findingId"
            params={{ projectId, findingId: ctx.id }}
            style={{ textDecoration: "none" }}
            data-testid="chat-open-finding"
          >
            <Typography variant="caption" color="primary">
              Open the Finding Panel
            </Typography>
          </Link>
        ) : null}
      </Box>

      {/* Transcript. */}
      <Paper variant="outlined" sx={{ p: 2, minHeight: 160 }} data-testid="chat-transcript">
        {isEmpty ? (
          <Typography variant="body2" color="text.secondary" data-testid="chat-empty">
            Ask me about your findings, recommendations, or confidence. I explain what OSLO
            already understands — I don&apos;t change the assessment here.
          </Typography>
        ) : (
          <Stack spacing={1.5}>
            {exchanges.map((ex) => (
              <ExchangeRow key={ex.exchange_id} exchange={ex} />
            ))}
          </Stack>
        )}
      </Paper>

      {/* The honest pending notice — the chat-command seam is flagged, never fabricated. */}
      {pendingNotice ? (
        <Alert severity="info" icon={false} data-testid="chat-pending-notice">
          {pendingNotice}
        </Alert>
      ) : null}

      {/* Explain / Clarify / Improve affordances — consume or trigger; never write canon. */}
      <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
        <Button
          size="small"
          variant="outlined"
          onClick={handleExplain}
          data-testid="chat-affordance-explain"
        >
          Explain
        </Button>
        <Button
          size="small"
          variant="outlined"
          onClick={handleClarify}
          data-testid="chat-affordance-clarify"
        >
          Clarify
        </Button>
        <Button
          size="small"
          variant="outlined"
          onClick={handleImprove}
          data-testid="chat-affordance-improve"
        >
          Improve
        </Button>
      </Stack>

      {/* Input — always enabled (free-tier cap stays enabled per spec §E). */}
      <Box
        data-testid="chat-input"
        component="form"
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        sx={{ display: "flex", gap: 1 }}
      >
        <TextField
          fullWidth
          size="small"
          multiline
          maxRows={4}
          placeholder="Ask about a finding, a recommendation, or confidence…"
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          inputProps={{ "aria-label": "Message OSLO" }}
        />
        <Button type="submit" variant="contained" data-testid="chat-send">
          Send
        </Button>
      </Box>
    </Box>
  );
}

export default Chat;
