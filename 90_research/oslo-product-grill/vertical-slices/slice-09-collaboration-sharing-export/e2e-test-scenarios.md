# Slice 9 — Collaboration, Sharing & Export · E2E Test Scenarios (≤20)

Manual click-through (client-side prototype). "Restart" = phase-bar Restart (clears flags). No email actually leaves the prototype; no analysis runs in any scenario here. Covers collaboration/sharing/export **and** the Reports trio + depth.

1. **Open the sharing dialog.** Top bar → Share (`⤴`). **Expect:** a dialog to **invite by email** (role picker: Collaborator / Viewer — no Owner option) and a **share-link** section; a note "Roles are shown, not enforced"; footer "Sharing changes no assessment. Only an analysis update does."

2. **Roles + seats.** Read the roles band. **Expect:** Owner and Collaborator show **"takes a seat"**; **Viewer** shows **"no seat"**; a line that **asking for a read is free — no invite, no seat**.

3. **Two limits, never merged.** Read the top of the share dialog. **Expect:** a **phase** limit (invites/supply) and a **tier** limit (seats/depth) shown **separately** — never one blended "you've hit your limit — upgrade" sentence. Invite a Viewer at any seat count. **Expect:** never blocked (Viewers are unlimited).

4. **Create + copy a view-only link.** Click "Create a view-only link" → Copy. **Expect:** a snapshot link with **Copy / Preview what they see / Revoke**, lifetime "30 days · revocable · same on every plan"; copying toasts "opens a view-only read."

5. **The link shows a snapshot, relabelled if stale.** Preview what they see; then let the read move (run an analysis) and re-preview. **Expect:** it shows the read **as it stood**; after the read moves, it is labelled **"previous analysis"** with its date — never a stale read passed off as current. It never re-runs an analysis.

6. **Revoke a link.** Click Revoke. **Expect:** the link goes dead ("told it was revoked"), a History event is appended, and **nothing about the assessment changed**.

7. **Share link is not an export link.** Read the rule box. **Expect:** the dialog states a share link (revocable, live-project, view-only) is a **different object** from an export link (a frozen snapshot copy) — with a link across to Export (D107).

8. **Comment on a finding.** Open an issue → Comments → type and post (`⌘↵`). **Expect:** the comment appears in the thread; the label "Comments never change the assessment" sits at the box; a History `comment` event is appended; the read/assessment is unchanged.

9. **@mention + reply.** In the comment box type `@`, pick a teammate, post; then Reply on it. **Expect:** an `@Name` pill; the reply threads under its parent ("reply" chip); the mention menu's **"Invite someone new…"** opens the sharing dialog.

10. **Comments are append-only.** Look for any edit or delete control on a posted comment; open the row ⓘ. **Expect:** **none exists** (append-only by design); the ⓘ says "comments can't be edited or deleted once posted."

11. **Open Export — currency marker + disclaimer.** Top bar → Export. **Expect:** the **currency marker** (Outcome Confidence band + reliability + analysis run + when + open issues) and the **verbatim disclaimer** — "understanding maturity … **not** a measure of project health, readiness, or probability of success."

12. **Free = PDF only, but nothing is disabled.** On Free, click **Copy summary** / **Export link**. **Expect:** the buttons are **live** (labelled "Basic", not hidden); clicking surfaces the value-framed **UP-EXPORT** prompt naming the format and Basic — never a disabled control, never silence. Then export **PDF** → it succeeds (simulated).

13. **An export is a read.** After exporting, open History. **Expect:** an **append-only export record** saying it "generates no new assessment and never triggers an analysis." No band moved.

14. **Strategic Readout — tailor the ask, not the read.** In the export preview, switch the audience (Sponsor → Executive-board). **Expect:** only **§4 "What I need from you"** changes; §1 The read, §2 limiting, §3 unknowns, §5, §6 are identical across audiences; assembling it runs no analysis.

15. **Reports workspace — the tabs.** Sidebar → Reports. **Expect:** a slim **tab strip** with **Executive Briefing** (Authored) plus **Outcome Readiness · Assumptions & Evidence · Decision Record** (Generated), each with a kind chip.

16. **Outcome Readiness (generated, single-depth).** Open it. **Expect:** the band + a neutral maturity ramp (no fill, no RAG), the CAF drivers, a reliability trust-check ("✓ Sound basis" / "Read this with care"), grounding + issue counts + ladder rung, and "the one next move"; a note "A single depth — this snapshot is short by design"; no forecast/composite anywhere.

17. **Assumptions & Evidence + depth persists.** Open it, flip **Summary → Full**, leave and re-enter. **Expect:** Summary shows the load-bearing shortlist + open questions + per-dimension inference with "a level is not its trustworthiness"; **Full** adds "if it's wrong…" and the complete inferred register by dimension; the **Full choice is remembered** on re-entry (`repDepth`). Depth changes volume, never the claim.

18. **Decision Record honours D088.** Open it after making a decision (confirm/fix/answer) but before the next analysis update; then run the update. **Expect:** each decision shows **what it firmed** (a document → Confirmed by you) and a status **"Awaiting the next analysis update"** → **"Live in the read"** only after a newer run; the report never claims a decision moved the band by itself.

19. **One export modal for every report.** On any generated report, click **Export**. **Expect:** the **same** export modal (currency marker · disclaimer · tier gating · append-only record) — no separate machinery; "send" (a view-only share link) is kept distinct from the frozen export.

20. **Boundary, theme + a11y.** Confirm the **Asana execution-export** is not part of Reports/Export here (it is Slice 11's distinct object). Then toggle light theme; keyboard-tab into the share dialog, the comment mention menu, the export formats, and the report depth toggle. **Expect:** the Asana mapping is absent; light parity holds; focus rings visible; dialogs Esc-close; menus/toggles keyboard-operable; no analysis animation under reduced-motion.
