#!/usr/bin/env python3
"""DL records helper (DL-065 — Decision-Recording Discipline).

Subcommands:
  next   - print the next free DL number (scans EVERY DL id in use repo-wide, not one directory)
  self-test - prove the numbering rule fails when it should (run it before trusting a green)
  index  - regenerate the records index block in decision_log.md (between markers)
  check  - validate the records/ regime (also run by doc_integrity_check.py)

Records live at 00_owner/decisions/records/DL-XXXX-slug.md (DL-065+).
DL-029..DL-064 remain in the frozen decision_log.md and are NOT validated here.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DECISIONS = ROOT / "00_owner/decisions"
LEGACY_LOG = DECISIONS / "decision_log.md"
RECORDS = DECISIONS / "records"
FROZEN_THROUGH = 64  # decision_log.md is the historical ledger through DL-064

REC_NAME_RE = re.compile(r"^DL-(\d{3,})-[a-z0-9][a-z0-9-]*\.md$")
HEAD_DL_RE = re.compile(r"^#\s*DL-(\d{3,})\b")
REQUIRED_FIELDS = ("Decision", "Status")


def legacy_max(root=ROOT):
    log = Path(root) / "00_owner/decisions/decision_log.md"
    if not log.exists():
        return 0
    nums = [int(n) for n in re.findall(r"^###\s*DL-(\d{3,})\b",
            log.read_text(encoding="utf-8", errors="ignore"), re.M)]
    return max(nums) if nums else 0


def record_files(root=ROOT):
    recs = Path(root) / "00_owner/decisions/records"
    return sorted(recs.glob("DL-*.md")) if recs.exists() else []


def record_nums(root=ROOT):
    nums = []
    for rf in record_files(root):
        m = REC_NAME_RE.match(rf.name)
        if m:
            nums.append(int(m.group(1)))
    return nums


# ── DL ids IN USE, repo-wide (added 2026-08-19) ───────────────────────────────────────────────────
# ⚠️ next_number() used to read ONE directory (00_owner/decisions/records) plus the frozen legacy log,
# and the dl-land workflow's header claimed that numbering off current `main` made mis-numbering
# impossible. MEASURED on 2026-08-19 against origin/main at 65cbf59, that claim was false, and false
# for a reason that has nothing to do with stale clones: THIS REPOSITORY HAS FOUR DECISION HOMES.
#
#   00_owner/decisions/records      99 files
#   release-2/canon/decisions        6 files, spanning ids 158 through 228
#   release-2.1/canon/decisions      4 files
#   90_research/oslo-product-grill   7 files
#
# Reading one of four, next_number() returned id 157 — a number already cited throughout the working
# tree. A counter that can re-issue a number in use is not a counter; it is a collision waiting for
# whoever dispatches next. The fix is not to migrate the corpus (that is Framework 002 section 9 and it is a
# different piece of work) but to stop the counter from asserting more than it has looked at.
#
# ⚠️ FILENAMES ARE SCANNED AS WELL AS CONTENTS, deliberately. release-2/canon/decisions holds files
# named with an underscore and upper case rather than a slug — which REC_NAME_RE (lowercase
# slug, hyphens) cannot match. Those six files are exactly the ones the old rule could not see, so a
# content-only scan would reproduce the defect for any record whose body omits its own id.
# ⚠️ NO TRAILING \\b, AND THE SELF-TEST IS WHY. The first cut used \\bDL-(\\d{3,})\\b and the
# filename-only clause went red: `_` is a word character, so there is no boundary in a
# name like DL-nnn_CORRECTIVE_VS_EVOLUTIONARY.md — the regex missed the exact six files this scan exists to
# see. A leading lookbehind handles FOO_DL-nnn too, which \\b would also have refused.
# Over-matching is the safe direction here: it can only raise the ceiling, and a GAP is harmless
# where a COLLISION is not.
CITE_RE = re.compile(r"(?<![A-Za-z0-9])DL-(\d{3,})")
SCAN_SUFFIXES = (".md", ".py", ".yml", ".yaml", ".sh", ".json", ".html", ".txt")
SCAN_SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", "site-packages"}


def ids_in_use(root=ROOT):
    """Every DL id in use ANYWHERE in the repo -> the first path it was seen at.

    'In use' is deliberately broader than 'recorded'. An id cited in canon but never written to a
    record file is still spoken for: re-issuing it would make two different decisions answer to one
    name, which is worse than a gap in the sequence.
    """
    seen = {}
    root = Path(root)
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SCAN_SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        hay = path.name
        try:
            hay += "\n" + path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            pass
        for m in CITE_RE.finditer(hay):
            n = int(m.group(1))
            seen.setdefault(n, str(path.relative_to(root)))
    return seen


# ── The corpus is not all on one branch, and that is the half that actually bites ─────────────────
# ⚠️ Widening the working-tree scan is necessary and NOT sufficient, and this was measured rather than
# assumed. The dl-land workflow checks out the integration branch, and the integration branch does NOT
# carry release-2/canon/decisions or release-2.1/canon/decisions at all. So a working-tree scan run
# there sees one home no matter how wide the glob is, and still returns 157.
#
# Measured cost of looking properly: a content scan across every ref takes ~5.6s here; a filename-only
# scan takes 0.4s and misses ids that are cited but never named a file. The slow one is bought.
#
# ⚠️ refs/remotes/origin/* IS the right thing to read HERE and only here: in CI, `origin` is GitHub. In
# a clone-of-a-clone, origin/* maps the intermediate clone's LOCAL branches and is actively misleading.
# Do not copy this line into a sandbox script.
def ids_across_refs(root=ROOT):
    """{id: 'ref:path'} for every DL id in any ref, or None when the refs cannot be seen.

    None is not zero. A counter that has looked at one branch cannot assert repo-wide freedom, so the
    caller must fail closed rather than treat an unseen corpus as an empty one.
    """
    import subprocess
    try:
        refs = subprocess.run(["git", "for-each-ref", "--format=%(refname)",
                               "refs/remotes/origin/", "refs/heads/"],
                              cwd=str(root), capture_output=True, text=True, timeout=60)
        names = [r for r in refs.stdout.split() if r]
        # ⚠️ NOT `len(names) < 2`, AND THE REASON IS MEASURED, NOT ARGUED. A clone made with
        # `--depth 1 --single-branch` yields EXACTLY TWO refnames — refs/heads/main and
        # refs/remotes/origin/main — so the old test passed while the scan had seen ONE BRANCH,
        # which is the precise state this sentinel exists to catch. Measured 2026-08-22 on such a
        # clone: ids_across_refs() returned a dict instead of None, and assert_mintable() then
        # accepted a number it had no basis to call free. The docstring below was already correct
        # ("None is not zero"); the test under it was counting the wrong thing.
        # Count DISTINCT BRANCHES, not refnames: a branch and its origin mirror are one branch.
        branches = {r.replace("refs/remotes/origin/", "", 1).replace("refs/heads/", "", 1)
                    for r in names}
        if len(branches) < 2:
            return None
        out = subprocess.run(["git", "grep", "-o", "-E", r"DL-[0-9]{3,}"] + names,
                             cwd=str(root), capture_output=True, text=True, timeout=600)
        seen = {}
        for line in out.stdout.splitlines():
            loc, _, tail = line.rpartition(":")
            m = CITE_RE.search(tail)
            if m:
                seen.setdefault(int(m.group(1)), loc or "a ref")
        return seen or None
    except Exception:
        return None


def next_number(root=ROOT, explain=False):
    """The next number no decision anywhere in this repository already answers to."""
    used = dict(ids_in_use(root))
    across = ids_across_refs(root) if root == ROOT else None
    if across:
        for n, where in across.items():
            used.setdefault(n, where)
    floors = {"the frozen legacy range (FROZEN_THROUGH)": FROZEN_THROUGH,
              "the legacy decision_log": legacy_max(root)}
    recs = record_nums(root)
    if recs:
        floors["00_owner/decisions/records"] = max(recs)
    if used:
        top = max(used)
        floors["an id in use at %s" % used[top]] = top
    ceiling_from, ceiling = max(floors.items(), key=lambda kv: kv[1])
    n = ceiling + 1
    if explain:
        print("ceiling %d set by %s -> next DL-%03d" % (ceiling, ceiling_from, n), file=sys.stderr)
        if ceiling_from.startswith("an id in use") and ceiling not in recs:
            print("::warning::the ceiling comes from a CITATION rather than a record (%s). "
                  "If that citation is a typo it has permanently advanced the counter — check it."
                  % used[max(used)], file=sys.stderr)
    return n


def assert_mintable(n, root=ROOT):
    """Fail closed if the number about to be minted is already spoken for.

    ⚠️ This must never be quietly repaired by advancing n. A collision here means next_number() has
    stopped seeing part of the corpus, and silently stepping over it would hide the regression that
    this whole function exists to surface — the same shape as a gate that passes by skipping.
    """
    used = dict(ids_in_use(root))
    if root == ROOT:
        across = ids_across_refs()
        if across is None:
            raise SystemExit(
                "::error::refusing to mint DL-%03d — the other refs could not be read, so this counter "
                "has seen ONE branch.\n"
                "::error::The decision corpus is split across branches; a number free here can be taken "
                "there. Fetch every ref before landing (the workflow does this explicitly), or land by "
                "hand with the number chosen deliberately." % n)
        for k, v in across.items():
            used.setdefault(k, v)
    if n in used:
        raise SystemExit(
            "::error::refusing to mint DL-%03d — that id is already in use at %s.\n"
            "::error::next_number() has stopped seeing part of the decision corpus. Fix the scan; "
            "do not step over the collision." % (n, used[n]))
    if n <= FROZEN_THROUGH:
        raise SystemExit("::error::refusing to mint DL-%03d — it is inside the frozen legacy range "
                         "(<= DL-%03d)." % (n, FROZEN_THROUGH))
    return n


def check_records(root=ROOT):
    """Return a list of error strings for the records/ regime (empty == clean)."""
    errs = []
    recs = sorted((root / "00_owner/decisions/records").glob("DL-*.md")) \
        if (root / "00_owner/decisions/records").exists() else []
    seen = {}
    for rf in recs:
        rel = str(rf.relative_to(root))
        if rf.name.startswith("DL-PENDING"):
            errs.append(f"[record-pending] {rel} still DL-PENDING — assign a number before merge (tools/dl_records.py next)")
            continue
        m = REC_NAME_RE.match(rf.name)
        if not m:
            errs.append(f"[record-name] {rel} must be named DL-XXXX-slug.md (zero-padded, kebab-case)")
            continue
        num = int(m.group(1))
        head = rf.read_text(encoding="utf-8", errors="ignore")
        # header DL number must match the filename
        hm = HEAD_DL_RE.search(head[:400])
        if not hm or int(hm.group(1)) != num:
            errs.append(f"[record-header] {rel} '# DL-{num:03d} — …' header missing or mismatched")
        # required fields present (accept bold field, inline "Field:", or "## Field" heading)
        for fld in REQUIRED_FIELDS:
            if not (f"**{fld}" in head or f"{fld}:" in head
                    or re.search(rf"(?mi)^#{{1,6}}\s*{fld}\b", head)):
                errs.append(f"[record-fields] {rel} missing required field '{fld}'")
        # uniqueness
        if num in seen:
            errs.append(f"[record-dup] DL-{num:03d} in both {seen[num]} and {rel}")
        seen[num] = rel
        # records must be DL-065+ (legacy stays in the frozen log)
        if num <= FROZEN_THROUGH:
            errs.append(f"[record-range] {rel} number DL-{num:03d} is in the frozen legacy range (≤ DL-{FROZEN_THROUGH}); records are DL-{FROZEN_THROUGH+1}+")
    return errs


# ── A citation that resolves to nothing (added 2026-08-23) ────────────────────────────────────────
# ⚠️ THIS FILE ALREADY KNEW HOW TO ASK "is this id spoken for?" and was never asked the complementary
# question: "does this id RESOLVE?" The difference is not academic. ids_in_use() deliberately treats a
# bare citation as claiming an id, which is right for a counter and useless as a gate — under that
# rule a framework cited by section number for nine days, and never written, is in perfect health.
#
# Measured on main the day this was written: 172 ids cited, 161 resolve, ELEVEN do not, across 50
# citations. doc_integrity passed on all 1120 documents throughout. Two of the eleven were caught by
# hand hours apart on the same day — one framework cited by section number since 2026-08-14 and never
# written, and one glossary row about to be landed citing four sections of a spec the project's own
# decision index records as "spec unfinished". SECOND INSTANCE OF ONE SHAPE ⇒ MECHANISM, not a note.
#
# ⚠️ RESOLVE is deliberately NARROWER than "in use", in three ways, each of which was a real bug in a
# draft of this function:
#   1. 90_research is NON-CANONICAL (zone rules). It holds files literally named DL-nnn-*-dl-land-body.md
#      — dispatch DRAFTS. Counting them would let a research scratch file satisfy a canon citation.
#      Excluded as a RECORD home AND as a citing surface: a dangling citation in a non-canonical zone
#      is not a canon defect.
#   2. The debt register is excluded as a citing surface. It names every id it exempts, so counting it
#      would make the "this row is dead" clause below permanently unable to fire — a dead trigger
#      created by the change that needs it, the shape that has now appeared here three times.
#   3. The legacy log resolves ids only INSIDE the frozen range. Outside it, the log's generated
#      records-index is derivative of the record files and asserts nothing on its own; treating a
#      prose mention as a record is how a missing decision looks recorded.
REC_HOMES = ("00_owner/decisions/records",
             "release-2/canon/decisions",
             "release-2.1/canon/decisions")
REGISTER_REL = "00_owner/decisions/UNRECORDED_DECISIONS.md"
CITE_SKIP_DIRS = {"90_research"}
REGISTER_ROW_RE = re.compile(r"^\|\s*\*\*DL-(\d{3,})\*\*\s*\|")

# ── Decision INDEXES ────────────────────────────────────────────────────────────────────────────
# ⚠️ The R2 series was maintained as an INDEX, not as one file per decision. Only some entries were ever
# promoted to records/, so a citation to an adjudicated-but-unpromoted decision read as "resolves to no
# record" — 12 of them, every one carrying a ratified disposition in the index below. The corpus was not
# incomplete; the resolver could not see where the series actually lived.
#
# DECLARED, NEVER GLOBBED. A glob would let any new file silently become an authority for resolving
# citations. Each index is named, and a declared index that is ABSENT is an ERROR — so adopting this
# mechanism forces the index itself to graduate rather than letting the gate go quiet.
DECISION_INDEX_RELS = ("00_owner/decisions/indexes/R2_DECISION_INDEX_PHASE_A.md",)

# ⚠️ DEFAULT-DENY, ON AN EXPLICIT MARKER. A first draft resolved any structured table row, and the very
# first row of the real index is
#     | DL-157, 159, 160, 161, 163 | **Occur nowhere** — no record, no reference, on any branch |
# — a row whose PURPOSE is to record that those decisions do not exist. Inferring resolution from row
# SHAPE would have made an absence record into an authority. So the index must SAY which rows resolve:
# the marker is `[R]`, placed in the readiness column, and a row without it resolves nothing.
INDEX_ROW_RE = re.compile(r"^\|\s*\*{0,2}DL-\d{3,}")
INDEX_MARK = "[R]"
# Ranges and comma lists are real in this index (`DL-200–205`, `DL-157, 159, 160`). Capturing only the
# first id of a row would resolve DL-200 and silently refuse DL-205 — arbitrary, and arbitrary is not a
# rule. Every id a marked row catalogues resolves; no id an unmarked row mentions does.
INDEX_RANGE_RE = re.compile(r"DL-(\d{3,})\s*[\u2013\u2014\u2026-]\s*(\d{3,})")
INDEX_ID_RE = re.compile(r"DL-(\d{3,})")
INDEX_BARE_ID_RE = re.compile(r"(?<![\w-])(\d{3})(?![\d])")


# ⚠️ THE SUBJECT IS THE TRACKED CORPUS, NOT THE FILESYSTEM. A draft of this gate walked rglob and was
# handed to the owner; on his clone it failed instantly on EIGHT ids cited only in
# release-2/oslo-prototype-r2.backup-*.html — UNTRACKED backup files left in the working tree by a
# previous checkout, present on no ref at all. Checking out main does not remove untracked files, so
# the gate graded local litter as canon and the "fix" it invited was to enter stray backups into the
# decision register: the precise failure the register's own header warns against.
#
# ⚠️ Over-scanning is the UNSAFE direction for a gate, the opposite of the trade-off in next_number()
# above. There, over-matching can only raise a ceiling and a gap is harmless. Here a false red trains
# people to reach for the exemption list, and a gate that reds on one machine and greens on another
# asserts nothing. This is the fourth appearance of checker-and-subject-in-different-scopes on this
# repository, so it is fixed at the enumeration rather than patched at the call site.
#
# Inside a git work tree the answer is `git ls-files`. Outside one (the self-test fixtures) the
# filesystem IS the corpus. ⚠️ Inside a work tree where ls-files FAILS we return None and the caller
# errors: a scan that cannot see the corpus must not report on it.
def scan_paths(root=ROOT):
    """(relative paths, scope) where scope is 'tracked' | 'filesystem', or (None, 'broken')."""
    import subprocess
    root = Path(root)
    # ⚠️ Asked BEFORE git runs, and it is the clause C8 caught. Judging "is this a repository?" purely
    # from `rev-parse` exit status silently reclassifies a BROKEN work tree as "not a repo", and the
    # filesystem fallback then reports a clean pass on a corpus it never enumerated — a gate passing by
    # not running. The presence of .git is the claim; failing to read it is a broken gate, not a hint
    # to go and glob instead.
    looks_git = (root / ".git").exists()
    try:
        inside = subprocess.run(["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"],
                                capture_output=True, text=True, timeout=30)
        if inside.returncode == 0 and inside.stdout.strip() == "true":
            out = subprocess.run(["git", "-C", str(root), "ls-files", "-z"],
                                 capture_output=True, text=True, timeout=300)
            if out.returncode != 0:
                return None, "broken"
            return [p for p in out.stdout.split("\0") if p], "tracked"
    except Exception:
        return None, "broken"
    if looks_git:
        return None, "broken"
    return [str(f.relative_to(root)) for f in sorted(root.rglob("*")) if f.is_file()], "filesystem"


def recorded_ids(root=ROOT):
    """{id: path} for every id that RESOLVES to a record on this ref.

    Filenames, not bodies: one of the four homes names its files in UPPER_SNAKE, which the canonical
    slug pattern cannot match, and those are precisely the records a slug-only scan cannot see.
    """
    root = Path(root)
    out = {}
    paths, _scope = scan_paths(root)
    for rel in (paths or []):
        if not rel.lower().endswith(".md"):
            continue
        if not any(rel.startswith(home + "/") for home in REC_HOMES):
            continue
        m = CITE_RE.search(Path(rel).name)
        if m:
            out.setdefault(int(m.group(1)), rel)
    log = root / "00_owner/decisions/decision_log.md"
    if log.exists():
        text = log.read_text(encoding="utf-8", errors="ignore")
        for n in (int(x) for x in CITE_RE.findall(text)):
            if n <= FROZEN_THROUGH:
                out.setdefault(n, "00_owner/decisions/decision_log.md (frozen legacy range)")
    return out


def cited_ids_canonical(root=ROOT):
    """{id: [up to 3 paths]} for ids cited on tracked CANONICAL surfaces, or None if unscannable."""
    root = Path(root)
    out = {}
    paths, _scope = scan_paths(root)
    if paths is None:
        return None
    for rel in paths:
        parts = set(Path(rel).parts)
        if parts & SCAN_SKIP_DIRS or parts & CITE_SKIP_DIRS:
            continue
        if Path(rel).suffix.lower() not in SCAN_SUFFIXES:
            continue
        if rel == REGISTER_REL:
            continue
        # ⚠️ A DECLARED INDEX MAY NOT CITE ITSELF — the same treatment REGISTER_REL gets directly above,
        # and for the same reason. An index CATALOGUES ids; reading its own rows as CITATIONS makes the
        # document the author of its own demand, so it resolves what nothing outside it ever asked for.
        # MEASURED 2026-09-02 on the merged graduation chain: without this, 45 of 51 resolutions were
        # the index citing itself; with it, 13 remain and every one has a citer outside the index.
        if rel in DECISION_INDEX_RELS:
            continue
        f = root / rel
        if not f.is_file():
            continue
        try:
            hay = f.name + "\n" + f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for m in CITE_RE.finditer(hay):
            locs = out.setdefault(int(m.group(1)), [])
            if rel not in locs and len(locs) < 3:
                locs.append(rel)
    return out


def register_ids(root=ROOT):
    """{id: True} for every row of the debt register, or {} when the register is absent."""
    reg = Path(root) / REGISTER_REL
    if not reg.exists():
        return {}
    out = {}
    for line in reg.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = REGISTER_ROW_RE.match(line.strip())
        if m:
            out[int(m.group(1))] = True
    return out


def indexed_ids(root=ROOT):
    """({id: rel}, errors) — ids catalogued as a structured row of a DECLARED decision index.

    An index entry is a resolvable record: it carries the id, the substance and the ratified
    disposition. What it is not is a promotion — an id resolved here still has no record file, and the
    notice in check_citations_resolve says so on every run rather than letting it pass silently.
    """
    out, errs = {}, []
    for rel in DECISION_INDEX_RELS:
        f = Path(root) / rel
        if not f.exists():
            # ⚠️ FAIL-CLOSED, BUT ONLY FOR THE REAL CORPUS. A first draft raised this in every tree and
            # broke six existing fixtures — synthetic trees carry no index and should not be required to.
            # Resolution is tree-local; "a declared index must EXIST" is a corpus-level invariant.
            if Path(root) == ROOT:
                errs.append(f"[index-missing] {rel} is declared in DECISION_INDEX_RELS but is not "
                            f"present. A declared index that cannot be read must FAIL — an unreadable "
                            f"authority is not an absent constraint (DL-243 6b). Graduate the index, "
                            f"or undeclare it.")
            continue
        for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
            l = line.strip()
            if not INDEX_ROW_RE.match(l) or INDEX_MARK not in l:
                continue
            cell = l.split("|")[1] if "|" in l else l
            ids = set()
            for a, b in INDEX_RANGE_RE.findall(cell):
                ids.update(range(int(a), int(b) + 1))
            ids.update(int(x) for x in INDEX_ID_RE.findall(cell))
            ids.update(int(x) for x in INDEX_BARE_ID_RE.findall(cell))
            for n in ids:
                out.setdefault(n, rel)
    return out, errs


def check_citations_resolve(root=ROOT):
    """(errors, notices). A cited id must resolve to a record or be an owner-ratified debt row.

    ⚠️ ASYMMETRIC ON PURPOSE, and the asymmetry is the interesting part.
    * "cited but neither recorded nor registered" is an ERROR on every ref. That is the property.
    * "registered but it now resolves" is a NOTICE, not an error. A release line legitimately carries
      records main has not graduated yet, so a row that is redundant THERE is still load-bearing on
      main; failing would punish the correct ref. Shrinking the register is bookkeeping, and it is
      owned by the Freeze audit, not by this gate.
    * "registered but cited nowhere" IS an error, because that row can only rot. This is the clause a
      draft of this function could not fire at all, until the register stopped counting itself.
    """
    root = Path(root)
    recorded = recorded_ids(root)
    cited = cited_ids_canonical(root)
    reg = register_ids(root)
    idx, idx_errs = indexed_ids(root)
    errs, notes = list(idx_errs), []
    if cited is None:
        return ([f"[citation-guard] the tracked corpus could not be enumerated (git ls-files failed), "
                 f"so this gate has seen nothing. A scan that cannot see the corpus must not report on "
                 f"it — fix the checkout, do not treat an unseen corpus as a clean one."], notes)
    for n in sorted(cited):
        if n in recorded or n in reg:
            continue
        if n in idx:
            # Resolved, and deliberately NOISY: an index entry is a record for citation purposes and
            # is still not a promoted record file. Silence here would hide the shape of the corpus.
            notes.append(f"[citation-indexed] DL-{n:03d} resolves at {idx[n]} (index entry, not a "
                         f"record file) — cited by {cited[n][0]}")
            continue
        where = ", ".join(cited[n][:2])
        errs.append(
            f"[citation-unresolved] DL-{n:03d} is cited ({where}) but resolves to no record.\n"
            f"                      Write the record, or — with an owner ratification — enter it in "
            f"{REGISTER_REL} with its reason.\n"
            f"                      ⚠️ Adding a row to turn this gate green is the failure the "
            f"register exists to prevent.")
    for n in sorted(reg):
        if n in recorded:
            notes.append(f"[citation-debt-paid] DL-{n:03d} now resolves at {recorded[n]} — the "
                         f"{REGISTER_REL} row is redundant on this ref and should be dropped when it "
                         f"is redundant on every ref.")
        elif n not in cited:
            errs.append(
                f"[citation-debt-dead] DL-{n:03d} is listed in {REGISTER_REL} but is cited nowhere on "
                f"this ref.\n"
                f"                     A debt row for a citation that no longer exists can only rot — "
                f"delete the row.")
    return errs, notes


def title_of(rf):
    for line in rf.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = re.match(r"^#\s*(DL-\d{3,}\s*—\s*.+)$", line.strip())
        if m:
            return m.group(1).strip()
    return rf.stem


START = "<!-- RECORDS-INDEX:START (generated by tools/dl_records.py index — do not hand-edit) -->"
END = "<!-- RECORDS-INDEX:END -->"


def build_index_block():
    lines = [START, "", "## Individual Decision Records (DL-065+)", "",
             "_One file per decision per DL-065. Generated — do not hand-edit._", ""]
    for rf in sorted(record_files(), key=lambda p: p.name):
        if rf.name.startswith("DL-PENDING"):
            continue
        lines.append(f"- {title_of(rf)} → `00_owner/decisions/records/{rf.name}`")
    lines += ["", END]
    return "\n".join(lines)


def regenerate_index():
    text = LEGACY_LOG.read_text(encoding="utf-8", errors="ignore")
    block = build_index_block()
    if START in text and END in text:
        new = re.sub(re.escape(START) + r".*?" + re.escape(END), block, text, flags=re.S)
    else:
        new = text.rstrip() + "\n\n---\n\n" + block + "\n"
    LEGACY_LOG.write_text(new, encoding="utf-8")
    try:
        where = LEGACY_LOG.relative_to(ROOT)
    except ValueError:
        where = LEGACY_LOG
    n = len([r for r in record_files() if not r.name.startswith("DL-PENDING")])
    print(f"index: wrote {n} record(s) into {where}")


CHANGELOG = ROOT / "00_owner/changelog/changelog.md"


def next_chg():
    if not CHANGELOG.exists():
        return 1
    nums = [int(n) for n in re.findall(r"^###\s*CHG-(\d{3,})\b",
            CHANGELOG.read_text(encoding="utf-8", errors="ignore"), re.M)]
    return (max(nums) + 1) if nums else 1


def _slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "decision"


def land(slug, title, body, decided_by, klass, date=None):
    """Create a numbered record from inputs, regenerate the index, append a CHG.
    Returns (dl_number, chg_number). Used by the dl-land workflow (DL-067)."""
    import datetime
    date = date or datetime.date.today().isoformat()
    slug = _slugify(slug)
    dl = assert_mintable(next_number(explain=True))
    chg = next_chg()
    RECORDS.mkdir(parents=True, exist_ok=True)
    rec = RECORDS / f"DL-{dl:03d}-{slug}.md"
    header = (f"# DL-{dl:03d} — {title}\n\n"
              f"- **Date:** {date} · **Status:** Ratified · **Decided by:** {decided_by}\n"
              f"- **Class:** {klass}\n\n")
    rec.write_text(header + body.strip() + "\n", encoding="utf-8")
    regenerate_index()
    chg_block = (f"### CHG-{chg:03d} — DL-{dl:03d}: {title}\n\n"
                 f"- **Date:** {date} · **Authorizing Decision:** DL-{dl:03d}.\n"
                 f"- **Affected Artifacts:** `00_owner/decisions/records/{rec.name}` (new); "
                 f"`00_owner/decisions/decision_log.md` (records index regenerated).\n"
                 f"- **Change Summary:** {title}. Landed via the dl-land workflow (DL-067).\n"
                 f"- **Supersession Reference:** None.\n")
    ctext = CHANGELOG.read_text(encoding="utf-8", errors="ignore")
    marker = "\n---\n\n## Governance Notes"
    if marker in ctext:
        ctext = ctext.replace(marker, "\n" + chg_block + marker, 1)
    else:
        ctext = ctext.rstrip() + "\n\n" + chg_block
    CHANGELOG.write_text(ctext, encoding="utf-8")
    return dl, chg, slug


# ── Self-test (RED first) ─────────────────────────────────────────────────────────────────────────
# ⚠️ Every clause below was watched to FAIL before it was trusted to pass. The numbering rule this file
# replaces was green for months and wrong the whole time, because nothing ever asked it to fail. Two of
# these clauses found real defects in this very change: the filename clause caught a regex that could
# not see an underscore, and the last clause caught THIS FILE inflating the counter it computes.
#
# ⚠️⚠️ FIXTURE IDS ARE BUILT FROM INTEGERS, NEVER WRITTEN AS LITERALS. A literal here is indexed by the
# scan above and permanently raises the real ceiling — which is exactly what happened on the first cut.
# A test fixture that changes the value under test is not a fixture.
def self_test():
    import tempfile
    fails = []
    tag = lambda n: "DL-%03d" % n

    def tree(spec):
        d = Path(tempfile.mkdtemp())
        for rel, text in spec.items():
            f = d / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(text, encoding="utf-8")
        return d

    frozen = "### %s — frozen\n" % tag(FROZEN_THROUGH)

    # 1. THE DEFECT ITSELF: an id living in a second decision home must raise the ceiling.
    t = tree({"00_owner/decisions/decision_log.md": frozen,
              "00_owner/decisions/records/%s-a-thing.md" % tag(100): "# %s\n" % tag(100),
              "release-2/canon/decisions/%s_CORRECTIVE.md" % tag(228): "# %s\n" % tag(228)})
    got = next_number(root=t)
    if got != 229:
        fails.append("an id in a second decision home did not raise the ceiling (got %s want %s)"
                     % (tag(got), tag(229)))
    old_rule = max([legacy_max(t)] + record_nums(t) + [FROZEN_THROUGH]) + 1
    if old_rule == got:
        fails.append("the widened scan agrees with the one-directory rule — the fixture cannot detect "
                     "the defect it was written for")

    # 2. An id CITED but never written to a record file is still spoken for.
    t = tree({"00_owner/decisions/decision_log.md": frozen,
              "20_handoff/contracts/SOMETHING.md": "as ruled in %s the seam is closed\n" % tag(300)})
    if next_number(root=t) != 301:
        fails.append("an id cited in prose but never recorded was re-issued")

    # 3. FILENAME-ONLY: the release-line homes name files with underscores and upper case, which
    #    REC_NAME_RE cannot match, so a content-only scan reproduces the original blindness.
    t = tree({"00_owner/decisions/decision_log.md": frozen,
              "release-2/canon/decisions/%s_NO_ID_IN_BODY.md" % tag(240):
                  "this body never names its own id\n"})
    if next_number(root=t) != 241:
        fails.append("an id present only in a FILENAME was invisible — the underscore blind spot is back")

    # 4. A collision must FAIL CLOSED, never be stepped over.
    t = tree({"00_owner/decisions/decision_log.md": frozen,
              "00_owner/decisions/records/%s-taken.md" % tag(120): "# %s\n" % tag(120)})
    try:
        assert_mintable(120, root=t)
        fails.append("assert_mintable minted an id that was already in use")
    except SystemExit:
        pass

    # 5. The frozen legacy range is refused.
    try:
        assert_mintable(50, root=t)
        fails.append("assert_mintable minted inside the frozen legacy range")
    except SystemExit:
        pass

    # 6. ⚠️ AN UNSEEN CORPUS IS NOT AN EMPTY ONE. When the other refs cannot be read, this counter has
    #    looked at one branch and must refuse rather than guess.
    global ids_across_refs
    keep = ids_across_refs
    try:
        ids_across_refs = lambda: None
        try:
            assert_mintable(9999)
            fails.append("assert_mintable minted while the other refs were unreadable — a counter that "
                         "has seen one branch asserted repo-wide freedom")
        except SystemExit:
            pass
    finally:
        ids_across_refs = keep

    # 8. ⚠️ THE SENTINEL IN CLAUSE 6 MUST ACTUALLY FIRE ON A ONE-BRANCH CHECKOUT.
    #    Clause 6 proves that assert_mintable refuses WHEN ids_across_refs returns None — it stubs the
    #    function out, so it never tests whether the real one returns None when it should. It did not:
    #    measured 2026-08-22 on a `clone --depth 1 --single-branch`, the old `len(names) < 2` test saw
    #    refs/heads/main AND refs/remotes/origin/main, counted two, and reported a corpus it had not
    #    read. A sentinel that passes in the exact state it guards against is not a sentinel.
    #    This clause builds a REAL one-branch repository rather than mocking one, because the defect
    #    lived in what git actually prints, and a mock would have agreed with the bug.
    import subprocess as _sp
    _d = Path(tempfile.mkdtemp())
    try:
        _q = dict(cwd=str(_d), capture_output=True, text=True)
        _sp.run(["git", "init", "-q", "-b", "main", "."], **_q)
        _sp.run(["git", "config", "user.email", "t@t"], **_q)
        _sp.run(["git", "config", "user.name", "t"], **_q)
        (_d / "a.md").write_text("# %s\n" % tag(100), encoding="utf-8")
        _sp.run(["git", "add", "-A"], **_q)
        _sp.run(["git", "commit", "-qm", "one"], **_q)
        # the shape a shallow single-branch checkout has: one branch, mirrored under origin/
        _sp.run(["git", "update-ref", "refs/remotes/origin/main", "refs/heads/main"], **_q)
        if ids_across_refs(root=_d) is not None:
            fails.append("ids_across_refs() reported a corpus from a ONE-BRANCH checkout — the "
                         "fail-closed sentinel counts refnames, and a branch plus its origin mirror "
                         "is two refnames but one branch")
        # and with a genuine second branch it must once again see something
        _sp.run(["git", "branch", "other"], **_q)
        _sp.run(["git", "update-ref", "refs/remotes/origin/other", "refs/heads/other"], **_q)
        if ids_across_refs(root=_d) is None:
            fails.append("ids_across_refs() refused a checkout that really does carry two branches — "
                         "the sentinel is now too strict and would block every landing")
    finally:
        import shutil as _sh
        _sh.rmtree(_d, ignore_errors=True)

    # 7. ⚠️ THIS FILE MUST NOT INVENT AN ID. It found itself doing exactly that on the first cut: the
    #    fixtures were written as literals, the scan indexed them, and the counter jumped by 64.
    #    ⚠️ The first version of THIS clause compared against the working tree only and asked whether
    #    this file held the highest id. That was too strict, and merging with the release line proved
    #    it: the ripple/in-flight comment cites two earlier decisions as history, and on a `main` tree
    #    those records do not exist, so a legitimate citation looked like inflation. CITING HISTORY IS
    #    FINE; INVENTING A NUMBER IS NOT. The clause now asks the question it meant to ask — does this
    #    id exist anywhere else at all?
    me = Path(__file__).resolve()
    mine = {int(m.group(1)) for m in CITE_RE.finditer(
        me.name + "\n" + me.read_text(encoding="utf-8", errors="ignore"))}
    mine = {n for n in mine if n > FROZEN_THROUGH}
    elsewhere = {n for n, where in ids_in_use().items() if Path(where).name != me.name}
    across = ids_across_refs()
    if across:
        elsewhere |= set(across)
    invented = sorted(n for n in mine if n not in elsewhere)
    if invented:
        fails.append("this file cites %s, which exist(s) nowhere else in the repository or its refs — "
                     "the scanner is inventing ids and inflating the counter it computes"
                     % ", ".join(tag(n) for n in invented))

    # ── The citation gate, RED-proved in BOTH directions (added 2026-08-23) ───────────────────────
    # ⚠️ Each clause below was watched to fail before it was trusted. The pair C1/C3 differ by ONE
    # file, so a green C3 cannot be a fixture that simply cannot detect anything.
    reg = lambda ids: "".join("| **%s** | 1x | fixture | fixture |\n" % tag(i) for i in ids)
    cited_only = lambda n: {"00_owner/decisions/decision_log.md": frozen,
                            "20_handoff/contracts/SEAM.md": "as ruled in %s\n" % tag(n)}

    # C1 RED — cited, no record, no register row: must ERROR.
    t = tree(cited_only(301))
    e, _ = check_citations_resolve(root=t)
    if not any("citation-unresolved" in x and tag(301) in x for x in e):
        fails.append("a cited id with no record and no register row did not fail the citation gate")

    # ── INDEX resolution, RED-proved in BOTH directions (added 2026-09-02) ───────────────────────
    # ⚠️ The dangerous failure is not "an index entry does not resolve" — it is an index that resolves
    # EVERYTHING. I1 and I2 differ by one ROW, so a green I1 cannot be a fixture that always passes.
    idxrel = DECISION_INDEX_RELS[0]
    idxrow = lambda ids: ("| id | what | disposition | R2 |\n|---|---|---|---|\n"
                          + "".join("| DL-%03d | fixture | CARRY-MODS | ok [R] |\n" % i for i in ids))
    idxrow_unmarked = lambda ids: ("| id | what | disposition | R2 |\n|---|---|---|---|\n"
                          + "".join("| DL-%03d | fixture | CARRY-MODS | ok |\n" % i for i in ids))

    # I1 GREEN — cited, no record, no register row, but CATALOGUED in a declared index: must pass.
    s1 = cited_only(311); s1[idxrel] = idxrow([311])
    e, n1 = check_citations_resolve(root=tree(s1))
    if e:
        fails.append("an indexed decision did not resolve: %s" % e[0].splitlines()[0])
    if not any("citation-indexed" in x and tag(311) in x for x in n1):
        fails.append("an index resolution was silent — it must announce that no record file exists")

    # I2 RED — the SAME tree, index present but WITHOUT that row: must still ERROR.
    # This is the clause that proves the index is being read as a catalogue, not as a blanket exemption.
    s2 = cited_only(312); s2[idxrel] = idxrow([999])
    e, _ = check_citations_resolve(root=tree(s2))
    if not any("citation-unresolved" in x and tag(312) in x for x in e):
        fails.append("an id ABSENT from the declared index still resolved — the index is exempting "
                     "everything, which is the failure this mechanism must not introduce")

    # I3 RED — a MENTION is not a row. The id appears in prose only: must still ERROR.
    s3 = cited_only(313); s3[idxrel] = idxrow([999]) + ("\nSee also %s, which has no record.\n" % tag(313))
    e, _ = check_citations_resolve(root=tree(s3))
    if not any("citation-unresolved" in x and tag(313) in x for x in e):
        fails.append("a bare MENTION in the index resolved a citation — INDEX_ROW_RE is too loose")

    # I5 RED — the row is present and catalogues the id, but carries NO [R] marker: must still ERROR.
    # This is the absence-row case, generalised: the index decides what resolves, not the row's shape.
    s5 = cited_only(315); s5[idxrel] = idxrow_unmarked([315])
    e, _ = check_citations_resolve(root=tree(s5))
    if not any("citation-unresolved" in x and tag(315) in x for x in e):
        fails.append("an UNMARKED index row resolved a citation — the marker is not load-bearing, so a "
                     "row recording a decision's ABSENCE would resolve it")

    # I6 GREEN — a marked RANGE row resolves every id it spans, not just the first.
    s6 = cited_only(317)
    s6[idxrel] = ("| id | what | d | R2 |\n|---|---|---|---|\n| %s\u2013318 | fixture | CARRY | ok [R] |\n"
                  % tag(316))
    e, _ = check_citations_resolve(root=tree(s6))
    if e:
        fails.append("a marked RANGE row did not resolve an id inside it: %s" % e[0].splitlines()[0])

    # I7 GREEN — an index's OWN rows are not citations. A tree whose only mention of an id is the
    # index row that catalogues it must pass, and must NOT announce a resolution, because nothing
    # cited it. Without the DECISION_INDEX_RELS exclusion this tree resolves — self-authored demand.
    s7 = {"00_owner/decisions/decision_log.md": frozen, idxrel: idxrow([321])}
    e, n7 = check_citations_resolve(root=tree(s7))
    if e:
        fails.append("an index row citing only itself raised an error: %s" % e[0].splitlines()[0])
    if any(tag(321) in x for x in n7):
        fails.append("the index resolved an id NOTHING outside it cited — a document became the "
                     "author of its own demand")

    # I8 RED — the exclusion must not blind the gate. The SAME id, cited by a real canonical file and
    # absent from the index, must still ERROR. I7 and I8 differ only in who does the citing.
    s8 = cited_only(322); s8[idxrel] = idxrow([999])
    e, _ = check_citations_resolve(root=tree(s8))
    if not any("citation-unresolved" in x and tag(322) in x for x in e):
        fails.append("excluding the index as a citer also hid a citation from a real file — the "
                     "exclusion is too wide")

    # I4 RED — a DECLARED index that is absent must fail closed at the REAL corpus, not pass quietly.
    # Proved directly against indexed_ids: every declared index is checked, and absence is an error.
    _saved = globals()["DECISION_INDEX_RELS"]
    try:
        globals()["DECISION_INDEX_RELS"] = ("00_owner/decisions/indexes/DOES-NOT-EXIST.md",)
        _, ie = indexed_ids(root=ROOT)
        if not any("index-missing" in x for x in ie):
            fails.append("a declared-but-absent decision index did not fail at the real root — "
                         "skip-as-pass in the mechanism that exists to prevent it")
    finally:
        globals()["DECISION_INDEX_RELS"] = _saved

    # C2 GREEN — the same tree plus an owner-ratified debt row: must pass.
    s = cited_only(302); s[REGISTER_REL] = reg([302])
    e, _ = check_citations_resolve(root=tree(s))
    if e:
        fails.append("a registered debt row did not exempt its citation: %s" % e[0].splitlines()[0])

    # C3 GREEN — the same tree plus the RECORD: must pass. Differs from C1 by one file only.
    s = cited_only(303); s["00_owner/decisions/records/%s-a-thing.md" % tag(303)] = "# %s\n" % tag(303)
    e, _ = check_citations_resolve(root=tree(s))
    if e:
        fails.append("a cited id WITH a record still failed the citation gate: %s" % e[0].splitlines()[0])

    # C4 RED — a debt row for an id cited nowhere is a rotting row: must ERROR.
    # ⚠️ THIS CLAUSE COULD NOT FIRE AT ALL until the citing scan stopped reading the register, which
    # names every id it exempts. A draft shipped with it permanently green — a dead trigger created by
    # the change that needs it.
    e, _ = check_citations_resolve(root=tree({"00_owner/decisions/decision_log.md": frozen,
                                             REGISTER_REL: reg([304])}))
    if not any("citation-debt-dead" in x and tag(304) in x for x in e):
        fails.append("a debt row for an id cited nowhere did not fail — the register can rot, and the "
                     "citing scan is probably counting the register itself")

    # C5 — a debt row whose id now resolves is a NOTICE, never an error. A release line legitimately
    # carries records main has not graduated, so failing here would punish the correct ref.
    s = cited_only(305); s[REGISTER_REL] = reg([305])
    s["00_owner/decisions/records/%s-a-thing.md" % tag(305)] = "# %s\n" % tag(305)
    e, n = check_citations_resolve(root=tree(s))
    if e:
        fails.append("a debt row whose id now resolves was treated as an error, not a notice")
    if not any("citation-debt-paid" in x and tag(305) in x for x in n):
        fails.append("a debt row whose id now resolves produced no notice — nothing will ever ask for "
                     "the row to be dropped")

    # C6 BOTH DIRECTIONS — a non-canonical zone must not fail the gate, and the SAME citation in a
    # canonical zone must. One assertion each way; the pair is the proof.
    e, _ = check_citations_resolve(root=tree({
        "00_owner/decisions/decision_log.md": frozen,
        "90_research/notes/SCRATCH.md": "as ruled in %s\n" % tag(306)}))
    if e:
        fails.append("a dangling citation in the non-canonical research zone failed the gate")
    e, _ = check_citations_resolve(root=tree(cited_only(306)))
    if not e:
        fails.append("the research-zone exemption is swallowing canonical citations too — the C6 pair "
                     "cannot tell the zones apart")


    # C7 BOTH DIRECTIONS — the subject is the TRACKED corpus. This is the clause the owner's clone
    # taught us: a draft walked the filesystem and failed on eight ids cited only in untracked
    # release-2/*.backup-*.html files left behind by a checkout. Same file, same citation, tracked vs
    # not; the pair is the proof, and a single-direction version of this clause would have passed on
    # the broken draft.
    import subprocess as _sp

    def _gittree(spec, track):
        d = tree(spec)
        _sp.run(["git", "init", "-q", str(d)], check=True)
        for rel in track:
            _sp.run(["git", "-C", str(d), "add", rel], check=True)
        return d

    _spec = lambda n: {"00_owner/decisions/decision_log.md": frozen,
                       "release-2/proto.backup.html": "as ruled in %s\n" % tag(n)}
    e, _ = check_citations_resolve(root=_gittree(_spec(307), ["release-2/proto.backup.html"]))
    if not any("citation-unresolved" in x and tag(307) in x for x in e):
        fails.append("a dangling citation in a TRACKED file did not fail — the C7 pair cannot tell "
                     "tracked from untracked")
    e, _ = check_citations_resolve(root=_gittree(_spec(308), []))
    if e:
        fails.append("a dangling citation in an UNTRACKED file failed the gate: the scan is walking the "
                     "filesystem, so local litter grades as canon (%s)" % e[0].splitlines()[0])

    # C8 — a git work tree whose corpus cannot be enumerated must ERROR, never pass quietly.
    _d = tree({"00_owner/decisions/decision_log.md": frozen})
    (_d / ".git").mkdir(exist_ok=True)
    (_d / ".git" / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    e, _ = check_citations_resolve(root=_d)
    if not any("citation-guard" in x for x in e):
        fails.append("an unenumerable git work tree passed the citation gate — an unseen corpus is "
                     "being treated as a clean one")


    for f in fails:
        print("  FAIL " + f)
    if not fails:
        print("  self-test OK — a second decision home raises the ceiling, a cited-but-unrecorded id is "
              "not re-issued, a filename-only id is seen, a collision fails closed, the frozen range is "
              "refused, an unreadable corpus refuses rather than guesses, a ONE-BRANCH checkout is "
              "detected as one branch rather than two refnames, this file invents no id, and a\n"
              "          citation that resolves to nothing fails while a ratified debt row does not")
    return 1 if fails else 0


def main(argv):
    cmd = argv[1] if len(argv) > 1 else ""
    if cmd == "next":
        print(f"DL-{assert_mintable(next_number(explain=True)):03d}")
    elif cmd == "next-chg":
        print(f"CHG-{next_chg():03d}")
    elif cmd == "index":
        regenerate_index()
    elif cmd == "self-test":
        return self_test()
    elif cmd == "citations":
        errs, notes = check_citations_resolve()
        for n in notes:
            print("NOTICE " + n)
        for e in errs:
            print("ERROR " + e)
        print("PASS" if not errs else f"FAIL ({len(errs)} citation error(s))")
        return 1 if errs else 0
    elif cmd == "check":
        errs = check_records()
        for e in errs:
            print("ERROR " + e)
        print("PASS" if not errs else f"FAIL ({len(errs)} record error(s))")
        return 1 if errs else 0
    elif cmd == "land":
        import argparse
        p = argparse.ArgumentParser(prog="dl_records.py land")
        p.add_argument("--slug", required=True)
        p.add_argument("--title", required=True)
        p.add_argument("--body-file", required=True)
        p.add_argument("--decided-by", default="Idris (Founder Console)")
        p.add_argument("--class", dest="klass", default="A")
        p.add_argument("--date", default=None)
        a = p.parse_args(argv[2:])
        body = Path(a.body_file).read_text(encoding="utf-8")
        dl, chg, slug = land(a.slug, a.title, body, a.decided_by, a.klass, a.date)
        print(f"landed DL-{dl:03d} (CHG-{chg:03d}) — records/DL-{dl:03d}-{slug}.md")
        import os
        gho = os.environ.get("GITHUB_OUTPUT")
        if gho:
            with open(gho, "a", encoding="utf-8") as f:
                f.write(f"dl={dl:03d}\nchg={chg:03d}\nslug={slug}\nbranch=decision/dl-{dl:03d}-{slug}\n")
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
