"""Advise — advisory. Sole producer of Recommendation + ClarificationRequest (Derived).

OSLO never autonomously applies a SuggestedFix; the user applies it. Advise
PROPOSES candidate responses anchored to a Finding/Issue; it never evaluates/
scores (Evaluate's), generates Findings (Infer's), writes canonical / promotes
to Attested, governs/authorizes/executes, or ACCEPTS its own output (acceptance
is the user's — DL-055; Wave U).

Public surface (DTM-0014 / Wave C; IC-WC-ADVISE):

- ``AdviseEngine`` / ``AdviseResult`` — anchored Recommendation + Clarification
  Request derivation (recommendation text is AI-text via the LLM seam; the
  anchor/type/id are EXACT).
- ``run_advise_stage`` / ``build_advise_stage`` — the injected ``advise`` stage
  (CHR per emission via ``ctx.chr_repo``; events; recompute supersedes).

DTM-0015 (DL-047 Additions) — additive: a **SuggestedFix** (REC-04, a candidate
edit to a named artifact, anchored to a Finding) and a **Validation**
Recommendation (REC-05, seeks stakeholder confirmation). OSLO NEVER autonomously
applies a SuggestedFix — applying is a user-initiated artifact edit (Wave I).
"""

from backend.responsibilities.advise.engine import (
    ADVISE_VERSION,
    AdviseEngine,
    AdviseResult,
)
from backend.responsibilities.advise.stage import (
    OUTPUT_KIND_CLARIFICATION,
    OUTPUT_KIND_RECOMMENDATION,
    OUTPUT_KIND_SUGGESTED_FIX,
    SUGGESTED_FIX_PAYLOAD_TYPE,
    build_advise_stage,
    run_advise_stage,
)

__all__ = [
    "ADVISE_VERSION",
    "OUTPUT_KIND_CLARIFICATION",
    "OUTPUT_KIND_RECOMMENDATION",
    "OUTPUT_KIND_SUGGESTED_FIX",
    "SUGGESTED_FIX_PAYLOAD_TYPE",
    "AdviseEngine",
    "AdviseResult",
    "build_advise_stage",
    "run_advise_stage",
]
