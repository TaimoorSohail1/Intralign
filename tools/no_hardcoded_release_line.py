#!/usr/bin/env python3
"""no_hardcoded_release_line.py — no governance tool may name a release line it did not resolve.

WHY THIS IS A MECHANISM AND NOT A THIRD NOTE
--------------------------------------------
`RELEASE_LINE_CONVENTION.md` has said since 2026-08-12 that governance tooling resolves the active line
from `CURRENT_RELEASE` (delivery from `DELIVERY_RELEASE`) and NEVER hardcodes it. The rule has now been
broken three times, and each break was found by hand:

  1. `pointer_freshness_check.py` read `LINE = "release-2.1"`. Fixed — and its own docstring records that
     RB-086 was about to wire it into CI, "which would have made a hardcoded line permanent in a gate".
  2. `doc-integrity.yml` resolved the graduation generator from the wrong pointer, printed "skipping", and
     PASSED (RB-093, found by the dev lead). The convention was applied to the tool and not to the workflow.
  3. `state_matrix_check.py` still read `LINE = "release-2.1"` on 2026-08-18 — and RB-088 was about to wire
     THAT into CI. The same sentence, one file over.
  ...and 1's fix was partial: it resolved the LINE and still hardcoded `oslo-prototype-r2.1.html`, so a new
  line would resolve correctly and then look for the previous line's filename.

Three instances of one shape is not a note, it is a missing check (standing rule: on the SECOND instance,
build a mechanism). Written down and unenforced is how the first three happened — twice to the reader of
the rule.

WHAT IT CHECKS
--------------
Two axes, because instance 1 proves fixing one leaves the other:
  A. a hardcoded release-line DIRECTORY  (`"release-2"`, `"release-2.1"`, …)
  B. a hardcoded line-versioned FILENAME (`…-r2.1.html`, `R2_…`) — a resolved line plus a stale filename
     fails in exactly the same way as a stale line.

⚠️ Resolvers legitimately mention the pattern: they scan for `release-*` and derive prefixes. Those lines
are ALLOWED BY DECLARATION below, one entry per file with a reason — never by a blanket "skip the resolver"
rule, which would exempt the very files most able to get this wrong.

    python3 tools/no_hardcoded_release_line.py [--self-test]
    exit 0 = clean · exit 1 = a tool names a line it did not resolve
"""
import os, re, sys

# Files scanned: governance tooling only. Docs may name lines freely — they are records, not resolvers.
SCAN_DIRS = ["tools", "release-2/tools", "release-2.1/tools"]

# DECLARED ALLOWANCES — INLINE, on the line itself, never per file.
#
# ⚠️ v1 of this checker used a per-FILE allowlist, and its own docstring said not to: "never by a blanket
# 'skip the resolver' rule, which would exempt the very files most able to get this wrong." It then did
# exactly that — exempting `pointer_freshness_check.py` wholesale and hiding the hardcoded
# `oslo-prototype-r2.1.html` on line 83, a defect already known when the exemption was written. I wrote the
# warning and implemented the thing it warns about, in one file.
#
# So an allowance is a marker on the offending LINE, with a reason, in the file under review — the SKIP-OK
# shape RB-095 ratified: a skip must cite its rule where the skip happens, not in a list somewhere else.
#
#     LINE = _resolve_line(...)                      # no marker needed; it resolves
#     for d in os.listdir(root): d.startswith("release-")   # LINE-OK: resolver fallback scan
#
MARKER = re.compile(r'#\s*LINE-OK:\s*\S')

DIR_PAT  = re.compile(r'["\']release-\d[\w.]*["\']')
FILE_PAT = re.compile(r'["\'][\w./-]*-r\d[\w.]*\.html["\']|["\']R\d_[\w.]+["\']')


def scan(root):
    problems, allowed = [], 0
    for d in SCAN_DIRS:
        full = os.path.join(root, d)
        if not os.path.isdir(full):
            continue
        for name in sorted(os.listdir(full)):
            if not name.endswith((".py", ".sh")):
                continue
            rel = "%s/%s" % (d, name)
            in_doc = False
            for i, line in enumerate(open(os.path.join(full, name), encoding="utf-8"), 1):
                # Track the triple-quote STATE. v1 skipped only lines CONTAINING the quotes, so
                # docstring BODIES were scanned as code and this checker reported its own prose --
                # including the very instances its docstring describes. A checker that indicts its
                # own explanation is the RB-067 cry-wolf failure, self-inflicted.
                q = line.count('"""') + line.count("'''")
                if q:
                    in_doc = (q % 2 == 1) != in_doc
                    continue
                if in_doc or line.lstrip().startswith("#"):
                    continue
                hit = None
                for pat, axis in ((DIR_PAT, "release-line directory"), (FILE_PAT, "line-versioned filename")):
                    m = pat.search(line)
                    if m:
                        hit = (axis, m.group(0))
                        break
                if not hit:
                    continue
                if MARKER.search(line):
                    allowed += 1
                    continue
                problems.append("%s:%d names a %s literally: %s — resolve it from the pointer "
                                "(RELEASE_LINE_CONVENTION.md), or mark the line `# LINE-OK: <reason>`."
                                % (rel, i, hit[0], hit[1]))
    return problems, allowed


def self_test():
    """A check nobody has seen fail is a claim. Prove both axes fire and the allowlist is honoured."""
    import tempfile
    fails = []
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "tools"))
        w = lambda n, s: open(os.path.join(td, "tools", n), "w").write(s)

        w("clean.py", 'LINE = resolve("CURRENT_RELEASE")\n')
        if scan(td)[0]:
            fails.append("a resolving tool was reported")

        w("clean.py", 'LINE = "release-2.1"\n')   # LINE-OK: self-test fixture — the literal is the thing under test
        if not scan(td)[0]:
            fails.append("axis A (hardcoded directory) did NOT fire")

        w("clean.py", 'PROTOTYPE = "oslo-prototype-r2.1.html"\n')   # LINE-OK: self-test fixture — the literal is the thing under test
        if not scan(td)[0]:
            fails.append("axis B (line-versioned filename) did NOT fire")

        w("clean.py", 'MANIFEST = "R2_FREEZE_MANIFEST.md"\n')   # LINE-OK: self-test fixture — the literal is the thing under test
        if not scan(td)[0]:
            fails.append("axis B did not fire on a prefixed filename")

        w("clean.py", '# LINE = "release-2.1" is what this used to say\n')   # LINE-OK: self-test fixture — the literal is the thing under test
        if scan(td)[0]:
            fails.append("a comment was reported as code")

        # the marker allows, and ONLY on the line it is written on
        w("clean.py", 'X = "release-2.1"   # LINE-OK: fixture, a real name is the point\n')
        if scan(td)[0]:
            fails.append("an inline LINE-OK marker did not allow its own line")
        w("clean.py", 'A = "release-2.1"   # LINE-OK: reason\nB = "release-2.1"\n')
        if len(scan(td)[0]) != 1:
            fails.append("a marker on one line leaked to another line")

    if fails:
        print("SELF-TEST FAILED:")
        [print("   " + f) for f in fails]
        return False
    print("  self-test OK — both axes fire, comments are ignored, a resolving tool stays quiet")
    return True


def main():
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    if not self_test():
        sys.exit(1)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("▶ no-hardcoded-release-line — scanning %s" % ", ".join(SCAN_DIRS))
    print("    repo=%s" % root)
    problems, allowed = scan(root)
    print("    inline LINE-OK allowances honoured: %d" % allowed)
    if problems:
        print("\nFAIL — %d tool(s) name a release line they did not resolve:" % len(problems))
        for p in problems:
            print("   ✗ %s" % p)
        sys.exit(1)
    print("\nOK — every governance tool resolves its release line.")


if __name__ == "__main__":
    main()
