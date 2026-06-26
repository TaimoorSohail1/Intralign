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
 * CHAT-COMMAND ENDPOINT (ANTI_ASSUMPTION — FLAGGED): there is no chat send/trigger
 * endpoint, and no mutation endpoint of any kind, in the DTM-0018 generated client (GET
 * reads only). Per the protocol we do NOT invent a canonical write: a send appends an
 * EPHEMERAL, NON-CANONICAL exchange marked "pending" — "Improve" would route to the
 * existing Advise/Deep-Pass trigger when that seam is exposed. Nothing canonical is
 * recorded; no governed object is mutated; no assessment changes. Only ephemeral
 * conversation display state changes.
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

export function Chat({ projectId, context, initialExchanges = [] }: ChatProps) {
  const ctx: ChatContext = context ?? { kind: "project" };
  const [exchanges, setExchanges] = useState<ChatExchange[]>(initialExchanges);
  const [draft, setDraft] = useState("");
  // The most recent reason a turn is pending / a trigger is flagged (honest disclosure).
  const [pendingNotice, setPendingNotice] = useState<string | null>(null);

  const nextId = useMemo(() => {
    let n = exchanges.length;
    return () => `ex-local-${++n}-${Date.now()}`;
  }, [exchanges.length]);

  /**
   * Append an EPHEMERAL, NON-CANONICAL user turn marked pending. This writes nothing
   * canonical and mutates no governed object — the chat-command seam is not exposed, so
   * the turn is held pending (never fabricates an OSLO answer).
   */
  function appendPending(text: string, notice: string) {
    const trimmed = text.trim();
    if (!trimmed) return;
    setExchanges((prev) => [
      ...prev,
      { exchange_id: nextId(), role: "user", text: trimmed, status: "pending" },
    ]);
    setPendingNotice(notice);
  }

  function handleSend() {
    if (!draft.trim()) return;
    appendPending(
      draft,
      "Sent — OSLO Chat's conversation seam is not yet wired, so this is held pending. " +
        "Nothing was recorded and no assessment changed.",
    );
    setDraft("");
  }

  function handleExplain() {
    appendPending(
      `Explain ${CONTEXT_NOUN[ctx.kind]}`,
      "Explain reads from OSLO's existing understanding — it computes nothing and changes " +
        "no assessment. The conversation seam is not yet wired, so this is held pending.",
    );
  }

  function handleClarify() {
    appendPending(
      `Clarify ${CONTEXT_NOUN[ctx.kind]}`,
      "Clarifications capture information that feeds the NEXT reanalysis — answering one " +
        "changes no confidence/CAF and resolves no finding by itself. Held pending until " +
        "the conversation seam is available.",
    );
  }

  function handleImprove() {
    appendPending(
      `Improve ${CONTEXT_NOUN[ctx.kind]}`,
      "Improve would route to the existing Advise + Deep Pass trigger — Chat itself records " +
        "nothing and mutates nothing. The trigger seam is not yet exposed, so this is held " +
        "pending.",
    );
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
