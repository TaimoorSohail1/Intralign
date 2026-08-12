# R2 Slice 01 UI/UX and accessibility audit

**Mode:** combined UX/accessibility audit

**Target:** executable Outcome Integrity Overview, masthead, and breakdown

**Reference:** `release-2/oslo-prototype-r2.html` and Slice 1 AC-1…AC-10

**Verdict:** **PARTIAL PASS — same-state visual/responsive parity passes; remaining manual accessibility and failure-state checks block the full gate.**

**Current-run evidence limit (2026-08-12 00:09 PKT):** the required in-app browser could not attach a fresh page after three attempts. The automated same-state captures were regenerated and inspected, but they are not substituted for the missing current-run manual keyboard, assistive-technology, zoom, reduced-motion, or failure-state audit.

**Resumption evidence limit (2026-08-12 01:05 PKT):** the in-app browser connected, but two fresh-page requests failed before a webview attached even after the documented recovery procedure and visibility attempt. Controlled and user-visible tab lists remained empty. The healthy local application could not be manually inspected, so no open accessibility or failure-state check changed status.

**Second resumption evidence limit (2026-08-12 02:05 PKT):** the in-app browser connected, but two fresh-page requests again failed before a webview attached. After the supported recovery path, visibility remained false and controlled/user-visible tab lists remained empty. The healthy seeded application therefore produced no current-run screenshot or interaction evidence; keyboard, assistive-technology, reduced-motion, 200% zoom, responsive, and failure-state checks remain open.

**Third resumption evidence limit (2026-08-12 03:10 PKT):** the in-app browser connected, but two fresh-page requests failed before a webview attached. Supported recovery retained the browser binding, confirmed empty controlled/user-visible tab lists, exposed visibility, and requested a fresh page. The web (`307`) and API health (`200`) endpoints were reachable, but no page existed to inspect. Local Supabase was also unavailable because Docker Desktop's service could not be started by the scheduler account; this would block the seeded owner journey after attachment but did not cause the earlier webview attachment failure. No current-run screenshot or interaction evidence was accepted, so keyboard, assistive-technology, reduced-motion, 200% zoom, responsive, and failure-state checks remain open.

**Fourth resumption evidence limit (2026-08-12 04:06 PKT):** the in-app browser connected, but the initial fresh-page request timed out before a webview attached. The documented recovery retained the browser binding, checked the controlled and user-visible tab lists, requested visibility, and requested one fresh page; the retry also failed before attachment. Both tab lists were empty and visibility remained false after recovery. Docker Engine was separately unresponsive and its Windows service could not be started by the scheduler account, but the page failed before navigation, so no source state was available to capture or inspect. Per the audit evidence rules, no prior or automated screenshot was substituted for current-run manual evidence. Keyboard, assistive-technology, reduced-motion, 200% zoom, responsive, and failure-state checks remain open.

**Fifth resumption evidence limit (2026-08-12 05:10 PKT):** Supabase Auth, PostgreSQL, FastAPI, and the Next.js listener were reachable, but the in-app browser's initial and one supported-recovery fresh-page requests both timed out before a webview attached. The same binding was retained; controlled and user-visible tab lists were empty, and a visibility request remained false. No page existed to capture or inspect. Per the audit evidence rules, no prior or automated screenshot was substituted for current-run evidence. Keyboard, assistive-technology, reduced-motion, 200% zoom, responsive, and failure-state checks remain open.

**Sixth resumption evidence limit (2026-08-12 06:08 PKT):** the in-app browser's initial and one supported-recovery fresh-page requests both timed out before a webview attached. The same binding was retained; controlled and user-visible tab lists stayed empty, and a visibility request remained false. Docker Engine was separately unresponsive and its stopped Windows service could not be opened by the scheduler account, but the page failed before navigation. No source state existed to capture or inspect. Per the audit evidence rules, no prior or automated screenshot was substituted for current-run evidence. Keyboard, assistive-technology, reduced-motion, 200% zoom, responsive, and failure-state checks remain open.

**Seventh resumption evidence limit (2026-08-12 07:09 PKT):** Supabase Auth, PostgreSQL, FastAPI, and Next.js were reachable, but the in-app browser's initial and one supported-recovery fresh-page requests both timed out before a webview attached. The same binding was retained; controlled and user-visible tab lists stayed empty, and visibility remained false. The seed refresh separately stalled on the Docker control channel, but the page failed before navigation and the existing seeded platform endpoints were healthy. No source state existed to capture or inspect. Per the audit evidence rules, no prior or automated screenshot was substituted for current-run evidence. Keyboard, assistive-technology, reduced-motion, 200% zoom, responsive, and failure-state checks remain open.

**Eighth resumption evidence limit (2026-08-12 08:10 PKT):** Supabase Auth, REST, PostgreSQL, FastAPI, and Next.js were reachable, but the in-app browser's initial and one supported-recovery fresh-page requests both timed out before a webview attached. The same binding was retained; controlled and user-visible tab lists stayed empty, requesting visibility remained false, and no page existed to capture or inspect. The idempotent seed refresh separately stalled for 49 seconds and was stopped, but the page failed before navigation and the existing platform endpoints were healthy. Per the audit evidence rules, no prior or automated screenshot was substituted for current-run evidence. Keyboard, assistive-technology, reduced-motion, 200% zoom, responsive, and failure-state checks remain open.

## Passed findings

1. **Hierarchy and copy.** The five-step Fragile→Sound ramp leads, the single limiting pillar follows, and all three pillar controls expose a band and count basis. Moment-in-time and live-tracking language is explicit; no probability or 0–100 integrity score appears.
2. **Compact masthead parity.** Viability, Grounding, and Adaptability chips with mini range bars now accompany the integrity headline at the applicable desktop width. They collapse at narrower widths to prevent crowding while the full card remains available.
3. **Breakdown behavior.** The named dialog receives initial focus, Escape closes it, and focus returns to the trigger. The dialog repeats the anti-forecast explanation and all three pillar details.
4. **Tablet.** At 768×1024 the header and content fit with no horizontal overflow; the three pillar controls remain side by side and readable.
5. **Mobile.** At 390×844 the page has no horizontal overflow; navigation becomes a bottom bar, content order is preserved, and pillar controls stack into full-width targets.
6. **Same-state comparison.** Desktop, tablet, and mobile combined captures show the same Fragile/Adaptability-gated state, Sound Viability/Grounding, five-band ramp, decomposition, and next-action hierarchy.

## Accessibility notes

- Pillar controls and masthead trigger have accessible button names containing pillar/band context.
- Focus-visible styling and dialog focus containment/restoration are present.
- Targets exceed the WCAG 2.1 AA minimum guidance used by the existing design system.
- Responsive reflow preserves reading order and avoids horizontal scrolling.

## Open checks

- A complete manual keyboard traversal, screen-reader announcement pass, reduced-motion observation, and 200% zoom inspection remain open.
- The manual timeout/stale/retry/last-good flow remains open because the chosen in-app browser's action channel timed out.
- Full WCAG compliance is not claimed.

The visual parity artifact passes; the overall UI/UX gate remains partial until the remaining manual accessibility and failure-state checks are exercised.
