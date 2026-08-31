/**
 * ChatRoute — the thin route element that adapts the TanStack route params + search into
 * the presentational `Chat`. It mounts at `/projects/$projectId/chat`, replacing the
 * DTM-0025 placeholder.
 *
 * CONTEXT INHERITANCE: Chat inherits context when launched from an issue / recommendation
 * / artifact / finding. The launching surface passes the source as search params
 * (`context_kind`, `context_id`, `context_label`); the route reads them (read-only) and
 * pre-scopes the conversation. Absent params ⇒ a neutral whole-project context.
 *
 * The surface takes plain props so it stays trivially testable and decoupled from the
 * router. Live conversation history would arrive via the (unexposed) chat seam — flagged;
 * the route seeds no fabricated transcript.
 */
import { getRouteApi } from "@tanstack/react-router";
import { Chat, type ChatContext, type ChatContextKind } from "./Chat";

const routeApi = getRouteApi("/projects/$projectId/chat");

const CONTEXT_KINDS: ChatContextKind[] = [
  "project",
  "finding",
  "issue",
  "recommendation",
  "artifact",
];

export function ChatRoute() {
  const { projectId } = routeApi.useParams();
  const search = routeApi.useSearch();

  const kind: ChatContextKind = CONTEXT_KINDS.includes(
    search.context_kind as ChatContextKind,
  )
    ? (search.context_kind as ChatContextKind)
    : "project";

  const context: ChatContext = {
    kind,
    id: search.context_id,
    label: search.context_label,
  };

  return <Chat projectId={projectId} context={context} initialExchanges={[]} />;
}

export default ChatRoute;
