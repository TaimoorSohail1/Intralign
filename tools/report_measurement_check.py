#!/usr/bin/env python3
"""report_measurement_check.py — a COUNT that reaches a governed report must name the command that produced it.

OWNER RULED 2026-08-29, after four measurement errors in one audit session, all one shape:

    1. an oracle count from a grep pattern instead of the tool's own count  (withdrawn twice — 08-24, 08-29)
    2. unrecorded-decision ids counted from TABLE ROWS, not the ids the file carries  (27 -> 21 -> 35)
    3. a state-matrix walk reporting "NEVER RECORDED" against a structure it had GUESSED
    4. a guard called never-evaluated, read from where its name APPEARED in an n/a column,
       never from the states where it was ABSENT  (it is measured and passing in 5 states)

Each measured a convenient PROXY instead of the SUBJECT. Three were caught by continuing to measure.
⚠️ The fourth of that shape — a branch assumed rather than checked — was NOT caught, and put 235 files
on `main` past the PR rule and doc-integrity. The difference was luck, not method.

⚠️⚠️ THE RULE: a section of a governed report that asserts a COUNT must carry

    MEASURED-BY: `<command>` @ <where>        or        NOT-MEASURABLE: <why>

so the proxy is visible IN THE ARTIFACT rather than only in the author's head. A reader who can re-run
the command can catch the error; a reader who cannot is being asked to trust it.

── EXTENDS, DOES NOT MINT (standing rule ①) ────────────────────────────────────────────────────────
`MEASURED-BY:` already exists and is enforced by `queued_work_check.py` on backlog ROWS (added
2026-08-19). `claim_verifier_check.py` enforces `VERIFIED-BY:` on Ledger rows asserting an OUTCOME.
⚠️ NEITHER looks at audit reports — which is precisely where all four errors above landed. This applies
the SAME field to the SAME kind of claim in the one document class that was uncovered. No new vocabulary.

── SCOPE, MEASURED BEFORE IT WAS CHOSEN (RB-067 — precision over recall) ────────────────────────────
MEASURED-BY: `python3 -c "<count integers in BUILD_READINESS_AUDIT_*.md by pattern>"` @ _repo_staging
    bare integer anywhere ............ 316 hits  -> NOISE. Every version number and date qualifies.
    integer + noun ("26 SIM tags") ... 118 hits  -> still noise; table cells and prose dominate.
    count-verb phrasing ................ 4 hits  -> too narrow to catch anything real.

⚠️ So the unit is NOT the token. It is the SECTION — the same unit as a backlog row, which is the
granularity the existing discipline already works at. A section is in scope when it presents a count as
EVIDENCE: inside a fenced block, or in a bolded/table claim. A dozen sections, not 316 tokens.

    python3 tools/report_measurement_check.py [--self-test]
    exit 0 = every count-bearing section names its command · exit 1 = one does not
⚠️ Read the exit code WITHOUT a pipe; `... | tail; echo $?` reports tail's status.

RB-113 — this checker states where it stood: it prints the file set and the section count it examined,
so an empty run is distinguishable from a run that found nothing to examine.
"""
import os, re, sys, glob, fnmatch

MARK_OK   = re.compile(r'^\s*(?:⚠️\s*)?\**(MEASURED-BY|NOT-MEASURABLE)\**\s*:', re.M)
# a verifier that names NOTHING is worse than no field (claim_verifier_check's lesson, restated):
# MEASURED-BY must carry a command in backticks, a path, or a tool invocation.
NAMES_A_COMMAND = re.compile(r'`[^`]*(?:python3|bash|git|gh|md5|grep|node|\.py|\.sh)[^`]*`|`[^`]{6,}`')

# A section presents a count as EVIDENCE if a number appears in a fenced block or a bold/table claim.
FENCE = re.compile(r'```.*?```', re.S)
COUNT_IN_FENCE = re.compile(r'\b\d+\b')
BOLD_COUNT  = re.compile(r'\*\*[^*]*\b\d+\b[^*]*\*\*')
TABLE_COUNT = re.compile(r'^\|.*\b\d+\b.*\|', re.M)

# Dates, version ids and DL/GT/RB/PR references are NOT counts — they are names that contain digits.
# ⚠️ `#245` and `§8c` must NOT carry a leading \b: `#` and `§` are not word characters, so \b before
# them can never match after a space. The self-test caught exactly this on its first run — the detector
# fired on a section whose only digits were ids, which is the noise condition it exists to avoid.
NOT_A_COUNT = re.compile(
    r'\b(?:20\d\d-\d\d-\d\d|R\d(?:\.\d)?|DL-\d+|GT-\d+|RB-\d+|CHG-\d+|v\d+)\b'
    r'|[#§]\d+[a-z\-]*'
    r'|\bmd5\s*`?\w+`?')

SECTION = re.compile(r'^(#{2,4})\s+(.+?)\s*$', re.M)


def sections(text):
    """(heading, body) for every ##/###/#### section, in order."""
    marks = list(SECTION.finditer(text))
    out = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out.append((m.group(2).strip(), text[m.end():end]))
    return out


def presents_a_count(body):
    """True when the section offers a NUMBER AS EVIDENCE, not merely a name containing digits."""
    stripped = NOT_A_COUNT.sub(' ', body)
    for f in FENCE.findall(stripped):
        if COUNT_IN_FENCE.search(f):
            return True
    return bool(BOLD_COUNT.search(stripped) or TABLE_COUNT.search(stripped))


def check_text(text):
    """(failures, examined) — failures are (heading, reason)."""
    fails, examined = [], 0
    doc_level = MARK_OK.search(text.split('\n## ', 1)[0]) if '\n## ' in text else None
    for heading, body in sections(text):
        if not presents_a_count(body):
            continue
        examined += 1
        m = MARK_OK.search(body)
        if not m and not doc_level:
            fails.append((heading, 'presents a count and names no MEASURED-BY / NOT-MEASURABLE'))
            continue
        src = body if m else text
        if 'NOT-MEASURABLE' in (m.group(1) if m else ''):
            continue
        line = src[src.index('MEASURED-BY'):][:400] if 'MEASURED-BY' in src else ''
        if line and not NAMES_A_COMMAND.search(line):
            fails.append((heading, 'MEASURED-BY names no command — a marker that names nothing is a rubber stamp'))
    return fails, examined


# ── GRANDFATHER BOUNDARY — a DATE, not a list ───────────────────────────────────────────────────────
# The rule was ruled on 2026-08-29. Reports authored BEFORE it cannot retroactively name commands their
# authors did not record. ⚠️ The boundary is the RULING DATE parsed from the filename, so it CANNOT
# GROW — an allowlist that only grows is the rubber stamp in a third costume (RB-095's lesson). A
# report dated on or after the ruling is in scope, always, with no exceptions field to add to.
RULED_ON = '2026-08-29'
DATE_IN_NAME = re.compile(r'(20\d\d-\d\d-\d\d)')


def in_scope(path):
    """(bool, reason) — dated on/after the ruling, or undated (new reports must comply)."""
    m = DATE_IN_NAME.search(os.path.basename(path))
    if not m:
        return True, 'undated'
    return (m.group(1) >= RULED_ON), ('dated %s' % m.group(1))


# ── SCOPE EXTENSION — RELEASE VALIDATION EVIDENCE (owner ruling G6, 2026-08-30) ─────────────────
# The rule was built for audits. A release VALIDATION report makes the same kind of claim and was
# outside it: PR #248 asserted "8 sections passed, 2 partial, 0 failed" (2026-08-28) while an audit
# of the same staging app found 3 blocking defects the next day. Neither verdict named what produced
# it, so neither could be re-run. Same failure, one document class over.
#
# SCOPE MEASURED BEFORE IT WAS CHOSEN (RB-067 — precision over recall).
# MEASURED-BY: `git ls-tree -r --name-only origin/codex/r2-uat-remediation -- code/docs | grep -i report`
#   8 markdown reports total
#     3 assert a release VERDICT ....... validation-report · release-readiness-report ·
#                                        release-blockers-report            -> IN scope
#     5 are PROGRESS records ........... slice-*-final · *-implementation-report ·
#                                        DEVELOPMENT_COMPLETION_REPORT      -> OUT of scope
# ⚠️ Sweeping progress records in would make this gate noisy, and a noisy gate stops being read —
# which is how the three rules this checker's docstring lists came to be broken by hand.
REPORT_PATTERNS = [
    '**/BUILD_READINESS_AUDIT_*.md', '**/*_PROBE_*.md', '**/*STAGING_PROBE*.md',
    # both spellings: the knowledge base screams, the application tree hyphenates.
    '**/*validation-report*.md',        '**/*VALIDATION_REPORT*.md',
    '**/*release-readiness-report*.md', '**/*RELEASE_READINESS_REPORT*.md',
    '**/*release-blockers-report*.md',  '**/*RELEASE_BLOCKERS_REPORT*.md',
]


def governed_reports(root='.'):
    seen = []
    for p in REPORT_PATTERNS:
        seen += glob.glob(os.path.join(root, p), recursive=True)
    return sorted(set(seen))


def matches_scope(name):
    """True when a BASENAME is a governed-report class.

    Exposed so self_test can RED-prove the SCOPE, not only the parser. A scope that was never
    tested against a document it must EXCLUDE is the same rubber stamp as a MEASURED-BY that
    names nothing.
    """
    return any(fnmatch.fnmatch(name, p[3:] if p.startswith('**/') else p)
               for p in REPORT_PATTERNS)


def self_test():
    """RED-prove BOTH directions. A check that cannot fail is not a check."""
    fails = []

    bad = "## Findings\n\n### B1 the thing\n\n```\n26 SIM tags · 29 capabilities\n```\n"
    f, ex = check_text(bad)
    if not f:
        fails.append('a count with no MEASURED-BY did not FAIL')
    if ex != 1:
        fails.append('scope wrong: expected 1 examined section, got %d' % ex)

    good = ("## Findings\n\n### B1 the thing\n\n```\n26 SIM tags · 29 capabilities\n```\n\n"
            "MEASURED-BY: `python3 tools/sim_coverage.py` @ refresh/r21-from-main\n")
    f, _ = check_text(good)
    if f:
        fails.append('a count WITH a command-naming MEASURED-BY wrongly failed: %s' % f)

    stamp = ("## Findings\n\n### B1 the thing\n\n```\n26 SIM tags\n```\n\n"
             "MEASURED-BY: I checked it\n")
    f, _ = check_text(stamp)
    if not f:
        fails.append('a MEASURED-BY naming NO command did not FAIL (rubber stamp accepted)')

    # Fixture identifiers come from a deliberately non-resolving range and are assembled at
    # runtime. A literal live DL id in this source must remain visible to the citation gate.
    fixture_dl = 'DL-' + str(900001)
    names = ("## Findings\n\n### B2 refs only\n\n"
             "**See %s, GT-900001, RB-900001 and #900001 on 2026-08-29.**\n" % fixture_dl)
    f, ex = check_text(names)
    if ex != 0:
        fails.append('ids/dates were treated as counts — detector is noise')

    nm = ("## Findings\n\n### B3 the thing\n\n```\n17 findings\n```\n\n"
          "NOT-MEASURABLE: staging returned 503 for the whole window\n")
    f, _ = check_text(nm)
    if f:
        fails.append('NOT-MEASURABLE was not accepted as the declared alternative')

    if in_scope('BUILD_READINESS_AUDIT_2026-08-24_R2.1_FREEZE.md')[0]:
        fails.append('a report predating the ruling was NOT grandfathered')
    if not in_scope('BUILD_READINESS_AUDIT_2026-08-29_R2.1_FREEZE.md')[0]:
        fails.append('a report ON the ruling date was wrongly grandfathered')
    if not in_scope('BUILD_READINESS_AUDIT_2026-12-01_R3.md')[0]:
        fails.append('a FUTURE report was grandfathered — the boundary is growing')
    if not in_scope('SOME_NEW_PROBE.md')[0]:
        fails.append('an undated report was grandfathered — new reports must comply')

    # ── SCOPE, RED-PROVED IN BOTH DIRECTIONS (G6 extension, 2026-08-30) ─────────────────────────
    # A scope only ever tested on documents it must INCLUDE cannot fail, and so is not a check.
    for name in ('BUILD_READINESS_AUDIT_2026-08-29_R2.0_STAGING.md',
                 'r2-live-staging-validation-report-2026-08-28.md',
                 'release-readiness-report-2026-08-05.md',
                 'staging-release-blockers-report-2026-08-05.md',
                 'R2_LIVE_STAGING_VALIDATION_REPORT.md'):  # LINE-OK: self-test FIXTURE name, never resolved to a path — the scope predicate is being RED-proved against an uppercase variant, per owner ruling 9 (fixtures must not masquerade as real subjects)
        if not matches_scope(name):
            fails.append('a release-verdict document is OUT of scope: %s' % name)

    for name in ('slice-10-implementation-report.md',
                 'slice-02-final-report.md',
                 'structured-artifact-reliability-implementation-report.md',
                 'DEVELOPMENT_COMPLETION_REPORT.md',
                 'design-qa.md',
                 'README.md'):
        if matches_scope(name):
            fails.append('a progress/unrelated document was swept IN — scope is noisy: %s' % name)

    if fails:
        print('SELF-TEST FAILED:')
        for x in fails:
            print('  ✗', x)
        return 1
    print('self-test OK — fails on a bare count, on a rubber stamp; passes a named command, a')
    print('NOT-MEASURABLE, and a section whose only digits are ids and dates.')
    print('boundary OK — pre-ruling grandfathered; on-date, future and undated all IN scope.')
    print('scope OK — audits and release-verdict reports IN; slice/implementation/progress reports OUT.')
    return 0


def main():
    if '--self-test' in sys.argv:
        sys.exit(self_test())
    root = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else '.'
    docs = governed_reports(root)
    # RB-113 — state where this stood, so an empty run is not mistaken for a clean one.
    print('report_measurement_check: %d governed report(s) under %s' % (len(docs), os.path.abspath(root)))
    if not docs:
        print('⚠️  NO governed reports found — this is NOT a pass. Check the path.')
        sys.exit(1)
    bad = total = skipped = 0
    for d in docs:
        ok, why = in_scope(d)
        if not ok:
            skipped += 1
            print('  grandfathered (%s, predates the %s ruling): %s'
                  % (why, RULED_ON, os.path.relpath(d, root)))
            continue
        f, ex = check_text(open(d, encoding='utf-8').read())
        total += ex
        for heading, why in f:
            bad += 1
            print('::error::%s → "%s": %s' % (os.path.relpath(d, root), heading[:70], why))
    print('%d count-bearing section(s) examined · %d unnamed · %d report(s) grandfathered'
          % (total, bad, skipped))
    if bad:
        print('⚠️  A count whose command is not stated asks the reader to trust it rather than re-run it.')
        sys.exit(1)
    print('PASS — every count that reaches a governed report names how it was produced.')
    sys.exit(0)


if __name__ == '__main__':
    main()
