#!/usr/bin/env python3
"""
OSLO Doc-Integrity Check (KIA2-1) — read-only knowledge-integrity gate.

Runs in CI on push/PR (and locally). It DETECTS drift; it never edits, fixes,
merges, or deploys. ERRORs fail the build; WARNs are reported but do not fail
(tune the policy in main()).

Checks:
  1. ERROR — broken internal doc links (markdown links + `backtick.md` refs),
     resolving the repo's bare-filename convention (basename match anywhere).
  2. WARN  — active-tree docs that reference a SUPERSEDED/legacy/historical doc
     (allowlisted: audits, changelog, decision log, indexes, READMEs, the
     glossary, deprecation banners — they legitimately cite history).
  3. WARN  — high-signal banned terminology (deprecated layer names, retired
     concepts) used in the active tree.
  4. WARN  — stale operative-DL range claims vs the actual max DL in the ledger.

Usage:  python3 tools/doc_integrity_check.py [--strict]
        --strict  → WARNs also fail the build.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD = [p for p in ROOT.rglob("*.md") if ".git" not in p.parts]
ALL_BASENAMES = {p.name for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts}

errors, warns = [], []

def rel(p): return str(p.relative_to(ROOT))

# ---- allowlists -------------------------------------------------------------
# files that may legitimately reference history / deprecated terms:
# files that are the reasoning/governance trail — they legitimately cite history,
# moved paths, sibling/old docs; exempt from broken-link ERRORs + history WARNs.
HIST_REF_ALLOW = ("audit", "changelog", "decision_log", "REPOSITORY_INDEX",
                  "OWNER_DECISION_QUEUE", "readme", "ANTI_ASSUMPTION", "glossary",
                  "legacy_layer_engineering", "historical_artifacts",
                  "REORGANIZATION", "SIMPLIFICATION", "KNOWLEDGE_INTEGRITY",
                  "OPEN_TBD", "PROPOSAL_", "DISPOSITION", "/decisions/", "/backlog/",
                  "/architecture_decisions/", "/product_decisions/", "/audits_reviews/",
                  "/constitution/", "/doctrine/", "/models/", "/domain/", "RECONCILIATION",
                  "CONSOLIDATION", "/transcripts/", "REVIEW", "REPOSITORY_ARCHITECTURE")
def allow_hist(path_str): return any(a.lower() in path_str.lower() for a in HIST_REF_ALLOW)

# active tree = build-relevant; exclude history + research + the reasoning trail
def is_active(p):
    s = rel(p)
    return not any(x in s for x in ("90_research/", "legacy_layer_engineering/",
                   "historical_artifacts/", "00_owner/audits/", "00_raw",
                   "raw/", "node_modules/"))  # 90_research/ + raw/ = raw source export; node_modules/ = vendored deps (e.g. the visual_regression harness) — never canon

# high-signal RETIRED terms only (unambiguous; common words like "Governance Layer"
# are excluded — they appear legitimately in governance/constitution prose).
BANNED = [r"Judge?ment Layer", r"Context Plane", r"Outcome Management"]
BANNED_RE = re.compile("|".join(BANNED))

LINK_RE = re.compile(r"\]\(([^)]+)\)")
CODE_MD_RE = re.compile(r"`([^`]+\.md)`")
SKIP_LINK = ("http://", "https://", "#", "mailto:", "{", "<")
# a CLEAN reference = a real relative path or bare filename, no prose/glob/ellipsis
CLEAN_REF = re.compile(r"^[A-Za-z0-9._\-/]+\.md$")

def superseded(p):
    try: head = p.read_text(encoding="utf-8", errors="ignore")[:600]
    except Exception: return False
    return ("SUPERSEDED" in head or "Historical — superseded" in head
            or "DEPRECATED" in head.upper() or "DO NOT BUILD" in head)

# ---- 1 + 2: links ----------------------------------------------------------
for f in MD:
    text = f.read_text(encoding="utf-8", errors="ignore")
    targets = [m.group(1).strip() for m in LINK_RE.finditer(text)]
    targets += [m.group(1).strip() for m in CODE_MD_RE.finditer(text)]
    for t in targets:
        if t.startswith(SKIP_LINK): continue
        t = t.split("#")[0].strip().strip("`")
        # only evaluate CLEAN references; prose/glob/ellipsis/example/shorthand patterns skipped
        if not CLEAN_REF.match(t): continue
        if t.startswith("_") or re.search(r"\d/\d", t): continue   # "_002.md", "001/002.md" shorthand
        if "/" in t:
            ok = (f.parent / t).exists() or (ROOT / t).exists() or Path(t).name in ALL_BASENAMES
        else:
            ok = t in ALL_BASENAMES
        if not ok:
            # historical/ledger files legitimately preserve old paths → not an active-tree error
            if is_active(f) and not allow_hist(rel(f)):
                errors.append(f"[broken-link] {rel(f)} → {t}")
            continue
        # resolve the referenced file (best effort) for supersede check
        refp = None
        cands = [ (f.parent / t), (ROOT / t) ]
        for c in cands:
            if c.exists(): refp = c; break
        if refp is None:
            for p in MD:
                if p.name == Path(t).name: refp = p; break
        if refp and is_active(f) and not allow_hist(rel(f)) and superseded(refp):
            warns.append(f"[active→superseded] {rel(f)} → {t}")

# ---- 3: banned terminology in active tree ----------------------------------
for f in MD:
    if not is_active(f) or allow_hist(rel(f)): continue
    for i, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
        if BANNED_RE.search(line):
            warns.append(f"[banned-term] {rel(f)}:{i} → {BANNED_RE.search(line).group(0)}")

# ---- 4: stale DL-range -----------------------------------------------------
dl_log = ROOT / "00_owner/decisions/decision_log.md"
if dl_log.exists():
    log_text = dl_log.read_text(encoding="utf-8", errors="ignore")
    dls = [int(m.group(1)) for m in re.finditer(r"DL-0?(\d{2,3})", log_text)]
    max_dl = max(dls) if dls else 0
    for f in MD:
        # the ledger + dispositions record historical ranges by design; not stale claims
        if any(x in rel(f).lower() for x in ("audit","decision_log","changelog","proposal_","disposition")): continue
        for m in re.finditer(r"DL-029 through DL-0?(\d{2,3})", f.read_text(encoding='utf-8', errors='ignore')):
            claimed = int(m.group(1))
            if claimed < max_dl:
                warns.append(f"[stale-DL-range] {rel(f)} claims …DL-{claimed:03d} but ledger max is DL-{max_dl:03d}")

# ---- 5: DL-053 disambiguation regression guard -----------------------------
# Bare-word qualification (Governance/Gate/Drift/Model → qualified form) is an AUTHORING
# NORM in CANONICAL_GLOSSARY § Disambiguation Register — it is NOT regex-enforced here,
# because the bare words have hundreds of legitimate uses ("authority resides with the
# owner", "scope drift") and flagging them all is noise, not signal.
# What IS enforced (precise, low-false-positive): the DL-053 RENAMES must not regress —
# the retired identifiers may not reappear in active build-relevant specs.
RENAMED = [("canonical_key", "dedup_key"),
           ("GOVERNANCE_MODEL_V1", "AUTHORITY_PLANE_MODEL_V1")]
# the glossary, the DL-053 proposal, and the ledger legitimately name the old identifiers
GUARD_SKIP = ("canonical_glossary", "proposal_terminology_disambiguation", "decision_log")
for f in MD:
    if not is_active(f) or allow_hist(rel(f)): continue
    if any(s in rel(f).lower() for s in GUARD_SKIP): continue
    text = f.read_text(encoding="utf-8", errors="ignore")
    for old, new in RENAMED:
        if old in text:
            warns.append(f"[renamed-term] {rel(f)} uses retired '{old}' → use '{new}' (DL-053)")

# ---- 6: decision-record discipline guard (DL-065) --------------------------
# Validates the records/ regime ONLY (DL-065+): naming, header↔filename match,
# required fields, uniqueness, and no DL-PENDING on main. The frozen legacy
# decision_log (DL-029..DL-064) is grandfathered and not re-validated here.
try:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from dl_records import check_records
    for e in check_records(ROOT):
        errors.append(e)
except Exception as ex:
    warns.append(f"[records-guard] could not run records check: {ex}")

# ---- report ----------------------------------------------------------------
print(f"OSLO doc-integrity: {len(MD)} docs · {len(errors)} errors · {len(warns)} warnings\n")
for e in errors: print("ERROR  " + e)
for w in warns: print("warn   " + w)
strict = "--strict" in sys.argv
fail = errors or (strict and warns)
print(f"\n{'FAIL' if fail else 'PASS'} (errors fail the build{'; --strict: warns too' if strict else ''}).")
sys.exit(1 if fail else 0)
