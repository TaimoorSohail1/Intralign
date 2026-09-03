"""Event seam for the Wave A contracts — dispatcher protocol only.

The backbone (IC-WA-00R A6) and artifact intake (IC-WA-001 A6) emit their
contract events through this seam; transport is deliberately NOT decided here
(open NFR). Full observability wiring — OTel spans, LangSmith linkage, governed
output event transport — is DTM-0006's ``ObservedEventEmitter`` decorator; this
module stays a thin internal dispatcher so the emitter can be swapped without
touching the responsibilities.

The vocabulary is pinned PER CONTRACT (deep-task decision #1, DTM-0007):

- ``EVENT_NAMES_WA00R`` — EXACTLY the seven IC-WA-00R A6 names, in contract order.
- ``EVENT_NAMES_WA001`` — EXACTLY the eight IC-WA-001 A6 names, in contract
  order. ``stale_detected`` belongs to the WA00R set and is referenced, never
  duplicated (IC-WA-001 A6 "Artifact Modified / Stale Detected").
- ``EVENT_NAMES_WA002`` — EXACTLY the five IC-WA-002 A6 names, in contract
  order (DTM-0008; OBS-WA-002 C2 == A6).
- ``EVENT_NAMES_WS`` — EXACTLY the four IC/OBS-WS-SYNTH A6 names (DTM-0009;
  decision #9), in contract order.
- ``EVENT_NAMES_WB_INFER`` — EXACTLY the two IC/OBS-WB-INFER A6 names (DTM-0010;
  decision #9), in contract order.
- ``EVENT_NAMES_WB_EVAL`` — EXACTLY the five IC/OBS-WB-EVAL A6 names (DTM-0011;
  decision #9), in contract order — the three OBS-WB-EVAL §2.3 events
  (Issue Generated / CAF Assessed / Outcome Confidence Computed) plus the two
  DL-047 trust signals (Understanding State Changed / false-confidence flag).
- ``EVENT_NAMES_WC_ADVISE`` — EXACTLY the two IC/OBS-WC-ADVISE A6 names
  (DTM-0014; decision #11), in contract order — "Recommendation Generated" /
  "Clarification Requested". The per-emission ``cognition_history_record_appended``
  is reused from the WA00R set (never duplicated).
- ``EVENT_NAMES_WC_FIX`` — EXACTLY the one DL-047 SuggestedFix OBS name
  (DTM-0015) — "Suggested Fix Offered". A SuggestedFix rides the existing
  ``recommendation`` CHR output_kind; its CHR-append pairs with the reused
  ``cognition_history_record_appended``. Application is observed as a USER edit +
  recompute (commodity / Wave I) — NOT an Advise event.
- ``EVENT_NAMES_WU_ACCEPT`` — EXACTLY the three IC/OBS-WU-ACCEPT C3 events
  (DTM-0016 + DTM-0017), in contract order — "User Acceptance Record appended" /
  "Plan-Fact recorded" / "Acceptance-Impact Assessment emitted". The capture
  event ``user_acceptance_captured`` is reused from the WA001 set (Perceive's);
  the per-emission ``cognition_history_record_appended`` is reused from the WA00R
  set (the Acceptance-Impact Assessment rides the existing ``acceptance_impact``
  CHR output_kind).
- ``EVENT_NAMES_COST`` — the single shared DL-048 spend event
  (``ai_spend_recorded``), introduced in DTM-0009 and reused by Wave B/C.
- ``EVENT_NAMES_ANALYSIS`` — EXACTLY the three Event Model §8.8 analysis-COMMAND
  events (DTM-0032), in §8.8 order — "Fast/Deep Analysis Requested" /
  "Analysis Cancelled". The run lifecycle (``*_analysis_started/completed``) is
  engine-produced through the recompute backbone (WA00R), never a command event.
- ``EVENT_NAMES`` — the union (concatenation) the emitters accept; kept as the
  back-compat alias for existing consumers.

An unknown name is a programming error and is rejected loudly — events are
contract surface, not free-form logging.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol, runtime_checkable

# IC-WA-00R A6 — the seven backbone events, exactly.
EVENT_NAMES_WA00R: tuple[str, ...] = (
    "stale_detected",
    "reanalysis_triggered",
    "recompute_started",
    "cognition_history_record_appended",
    "recompute_completed",
    "recompute_failed",
    "state_transition_occurred",
)

# IC-WA-001 A6 — the eight intake events, exactly (OBS-WA-001 C2).
# stale_detected is NOT repeated here — it is already pinned in the WA00R set.
EVENT_NAMES_WA001: tuple[str, ...] = (
    "artifact_received",
    "artifact_normalizing",
    "artifact_normalized",
    "promotion_candidate_ready",
    "promotion_readiness_failed",
    "user_acceptance_captured",
    "context_signal_received",
    "artifact_modified",
)

# IC-WA-002 A6 — the retention events (OBS-WA-002 C2).
# NOTE (RB-025 / DL-058): ``knowledge_unarchived`` is the append-only archive-reversal
# event added with unarchive-in-R1; this expands the contract's original "five retention
# events, exactly" to six. The OBS-WA-002 contract (20_handoff) + the traceability matrix
# must be updated to match — co-governed change, owner/EM review (see escalation).
EVENT_NAMES_WA002: tuple[str, ...] = (
    "knowledge_promoted",
    "knowledge_versioned",
    "knowledge_superseded",
    "knowledge_archived",
    "knowledge_unarchived",
    "knowledge_mutation_recorded",
)

# IC/OBS-WS-SYNTH A6 — the four synthesis-engine events, exactly (decision #9).
# Pinned verbatim against OBS-WS-SYNTH §3 / A6 ("Claim Extracted", "Planning
# Artifact Generated/Regenerated", "Synthesized Model Updated"). The
# per-emission ``cognition_history_record_appended`` is reused from the WA00R
# set (never duplicated). DTM-0009 / Wave S.
EVENT_NAMES_WS: tuple[str, ...] = (
    "claim_extracted",
    "planning_artifact_generated",
    "planning_artifact_regenerated",
    "synthesized_model_updated",
)

# IC/OBS-WB-INFER A6 — the two Finding events, exactly (decision #9; DTM-0010).
# Pinned verbatim against OBS-WB-INFER §1.3 / A6 ("Finding Detected/Superseded";
# C2 == A6). The per-emission ``cognition_history_record_appended`` is reused
# from the WA00R set (never duplicated). Wave B / Infer.
EVENT_NAMES_WB_INFER: tuple[str, ...] = (
    "finding_detected",
    "finding_superseded",
)

# IC/OBS-WB-EVAL A6 — the five Evaluate events, exactly (decision #9; DTM-0011).
# Pinned verbatim against OBS-WB-EVAL §2.3 / A6 ("Issue Generated"; "CAF
# Assessed"; "Outcome Confidence Computed") plus the DL-047 additions
# ("Understanding State Changed"; the false-confidence flag event, CONF-06). The
# per-emission ``cognition_history_record_appended`` is reused from the WA00R
# set (never duplicated). Wave B / Evaluate.
EVENT_NAMES_WB_EVAL: tuple[str, ...] = (
    "issue_generated",
    "caf_assessed",
    "outcome_confidence_computed",
    "understanding_state_changed",
    "false_confidence_flagged",
)

# IC/OBS-WC-ADVISE A6 — the two Advise events, exactly (decision #11; DTM-0014).
# Pinned verbatim against OBS-WC-ADVISE C3 / A6 ("Recommendation Generated";
# "Clarification Requested"). The per-emission ``cognition_history_record_appended``
# is reused from the WA00R set (never duplicated). Wave C / Advise.
EVENT_NAMES_WC_ADVISE: tuple[str, ...] = (
    "recommendation_generated",
    "clarification_requested",
)

# DL-047 SuggestedFix OBS — the single "Suggested Fix Offered" event (DTM-0015).
# A SuggestedFix is OFFERED, never applied by OSLO; application is observed as a
# user edit + recompute (Wave I / commodity), not as an Advise event. The
# per-emission ``cognition_history_record_appended`` is reused from the WA00R set
# (a fix rides the existing ``recommendation`` output_kind).
EVENT_NAMES_WC_FIX: tuple[str, ...] = (
    "suggested_fix_offered",
)

# IC/OBS-WU-ACCEPT C3 — the three acceptance events, exactly (DTM-0016 + 0017).
# Pinned verbatim against OBS-WU-ACCEPT C3 / U3 ("User Acceptance Record
# appended"; "Plan-Fact recorded"; "Acceptance-Impact Assessment emitted"). The
# capture event ``user_acceptance_captured`` is REUSED from the WA001 set
# (Perceive's, never duplicated); the per-emission ``cognition_history_record_appended``
# is REUSED from the WA00R set (the Acceptance-Impact Assessment rides the
# existing ``acceptance_impact`` CHR output_kind). Wave U / Retain + Evaluate.
EVENT_NAMES_WU_ACCEPT: tuple[str, ...] = (
    "user_acceptance_record_appended",
    "plan_fact_recorded",
    "acceptance_impact_assessed",
)

# DL-048 cost-governance — the single shared spend event (decision #9),
# introduced in DTM-0009 and reused by Wave B/C. "AI Spend Recorded" (OBS §3).
EVENT_NAMES_COST: tuple[str, ...] = ("ai_spend_recorded",)

# Event Model §8.8 "Analysis" — the three analysis-COMMAND events emitted by the
# DTM-0032 REST command router (:fast / :deep / :cancel), exactly, in §8.8 order.
# The run lifecycle (``*_analysis_started`` / ``*_analysis_completed``) is
# engine-produced through the existing recompute backbone (WA00R), not a command
# event — those names are NOT pinned here. Pinned verbatim against EM §8.8.
EVENT_NAMES_ANALYSIS: tuple[str, ...] = (
    "fast_analysis_requested",
    "deep_analysis_requested",
    "analysis_cancelled",
)

# Event Model §8.11 "Recommendations" — the four recommendation-COMMAND events
# emitted by the DTM-0033 REST command router (:accept / :reject / :defer /
# :implement), exactly, in §8.11 order. Each is a USER action recorded by Wave U
# (DL-055 rec lifecycle); ``recommendation_generated`` (the engine emission) lives
# in the WC_ADVISE set and is NOT repeated here. Pinned verbatim against EM §8.11.
EVENT_NAMES_RECOMMENDATION: tuple[str, ...] = (
    "recommendation_accepted",
    "recommendation_rejected",
    "recommendation_deferred",
    "recommendation_implemented",
)

# Event Model §5 "Project Events" — the three project-COMMAND events emitted by
# the DTM-0034 REST command router (create / patch / archive), exactly, in §5
# order. Pinned verbatim against EM §5.
EVENT_NAMES_PROJECT: tuple[str, ...] = (
    "project_created",
    "project_updated",
    "project_archived",
)

# Event Model §6 "Artifact Events" — the two artifact-intake-COMMAND events
# emitted by the DTM-0034 router (create artifact / append version), exactly, in
# §6 order. ``artifact_updated`` (§6) is a later state-command slice and is NOT
# pinned here. Pinned verbatim against EM §6.
EVENT_NAMES_ARTIFACT: tuple[str, ...] = (
    "artifact_created",
    "artifact_version_created",
)

# Event Model §7 "Context Events" — the single evidence-intake-COMMAND event
# emitted by the DTM-0034 router (add evidence), exactly. The ``context_item_*``
# events (§7) are extraction-engine emissions, not this command, and are NOT
# pinned here. Pinned verbatim against EM §7.
EVENT_NAMES_EVIDENCE: tuple[str, ...] = ("evidence_added",)

# Event Model §10 "Finding Events" — the two finding-LIFECYCLE-COMMAND events
# emitted by the DTM-0035 REST command router (:acknowledge / :address / :reopen),
# exactly, in EM §10 order. Per API Contract §5 + the endpoint catalog,
# ``:acknowledge`` and ``:address`` both carry ``finding_updated`` (the resulting
# status — acknowledged / addressed — rides the payload; the granular
# ``finding_acknowledged``/``finding_addressed`` are documented status FACETS of
# this canonical event, NOT new event types), and ``:reopen`` carries
# ``finding_reopened``. ``finding_detected``/``finding_superseded`` (engine emissions)
# live in the WB_INFER set; ``finding_created``/``finding_closed`` are engine/`:close`
# emissions NOT in this command vocabulary. Pinned verbatim against EM §10.
EVENT_NAMES_FINDING: tuple[str, ...] = (
    "finding_updated",
    "finding_reopened",
)

# Event Model §12 "Notification Events" — the two notification-STATE-COMMAND events
# emitted by the DTM-0035 REST command router (:view / :dismiss), exactly, in EM §12
# order. PLATFORM awareness state (non-canonical): a notification event has ZERO
# recompute consumers and never alters a Finding or Recommendation (§12 clarification).
# ``notification_created`` (source-object change) / ``notification_expired`` (scheduler)
# are NOT client commands and are NOT pinned here. Pinned verbatim against EM §12.
EVENT_NAMES_NOTIFICATION: tuple[str, ...] = (
    "notification_viewed",
    "notification_dismissed",
)

# OBS-WI-INTERACT — the single OSLO Chat event emitted by the DTM-0037 chat
# router (POST /projects/{pid}/chat), exactly. NON-CANONICAL: a ``chat_exchange``
# is an interaction record (like a notification) — zero recompute consumers, it
# alters no Finding/Recommendation/assessment. Chat's Improve TRIGGERS a Deep
# Pass whose run lifecycle (``*_analysis_*``) rides the recompute backbone
# (WA00R) and its CHR append rides ``cognition_history_record_appended`` (WA00R)
# — those are NOT this event. Pinned verbatim against OBS-WI-INTERACT §3
# ("Chat Exchange", non-canonical).
EVENT_NAMES_CHAT: tuple[str, ...] = ("chat_exchange",)

# Union vocabulary accepted by emitters (back-compat alias for consumers).
EVENT_NAMES: tuple[str, ...] = (
    EVENT_NAMES_WA00R
    + EVENT_NAMES_WA001
    + EVENT_NAMES_WA002
    + EVENT_NAMES_WS
    + EVENT_NAMES_WB_INFER
    + EVENT_NAMES_WB_EVAL
    + EVENT_NAMES_WC_ADVISE
    + EVENT_NAMES_WC_FIX
    + EVENT_NAMES_WU_ACCEPT
    + EVENT_NAMES_COST
    + EVENT_NAMES_ANALYSIS
    + EVENT_NAMES_RECOMMENDATION
    + EVENT_NAMES_PROJECT
    + EVENT_NAMES_ARTIFACT
    + EVENT_NAMES_EVIDENCE
    + EVENT_NAMES_FINDING
    + EVENT_NAMES_NOTIFICATION
    + EVENT_NAMES_CHAT
)

_EVENT_NAME_SET: frozenset[str] = frozenset(EVENT_NAMES)


class UnknownEventError(ValueError):
    """Raised when an event name outside the contract vocabularies is emitted."""


@runtime_checkable
class EventEmitter(Protocol):
    """The seam responsibilities emit through (callback protocol, not a transport)."""

    def emit(self, event_name: str, payload: Mapping[str, Any]) -> None:
        """Dispatch one contract event with its payload."""
        ...  # pragma: no cover - protocol


class CollectingEventEmitter:
    """Default emitter: validates names and collects events in order.

    Serves tests and local runs until a real external transport is bound.
    """

    def __init__(self) -> None:
        self.events: list[tuple[str, dict[str, Any]]] = []

    def emit(self, event_name: str, payload: Mapping[str, Any]) -> None:
        if event_name not in _EVENT_NAME_SET:
            raise UnknownEventError(
                f"unknown contract event {event_name!r} — the vocabulary is "
                "exactly IC-WA-00R A6 + IC-WA-001 A6 + IC-WA-002 A6 + "
                "IC-WS-SYNTH A6 + IC-WB-INFER A6 + IC-WB-EVAL A6 + "
                "IC-WC-ADVISE A6 + DL-047 SuggestedFix + IC-WU-ACCEPT C3 + "
                "DL-048 cost: "
                f"{', '.join(EVENT_NAMES)}"
            )
        self.events.append((event_name, dict(payload)))

    @property
    def names(self) -> list[str]:
        """Event names in emission order (assertion convenience)."""
        return [name for name, _ in self.events]
