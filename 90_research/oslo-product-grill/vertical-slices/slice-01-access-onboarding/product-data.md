# Slice 1 — Access & Onboarding · Product Data

Product entities and their visible fields for the access & onboarding funnel, plus prototype-local storage rules. **No database technology is specified or implied** — the prototype persists only client-side (D016). Internal canonical object names are noted; user-facing labels follow the plain-language map (D012).

## Entities & visible fields

### Invite
The simulated invitation that gates Alpha access (D022).
- `email` — the invited address (visible: "To idris@intralign.ai").
- `token` — unique activation token (visible in the simulated email; opaque string).
- `phase` — release phase the invite belongs to (Alpha).
- `expiresIn` — illustrative expiry ("expires in 7 days"; not enforced).
- Note: real issuance/validation is owner-TBD; the prototype renders a fixed sample invite.

### Account
The authenticated user created at activation (D022).
- `email` — pre-filled from the invite, read-only at activation.
- `name` — display name (user-entered; shown in Welcome and account menu).
- `active` — boolean; true after activation.
- Excluded from the prototype by design: password value is never stored (simulated field only), no roles/permissions (visibility-first).

### Session
The simulated sign-in state (D028).
- `staySignedIn` — boolean; whether the session persists on the device.
- Derived state: "signed in" = an active `Account` exists and (on reload) `staySignedIn` is true.
- Real session length / idle-timeout is owner-TBD; not modelled.

### Project (draft)
The project created from intake, pre- and post-analysis.
- `title` — "New project" until named/saved (e.g. "DevNorth 2026" after claim-through).
- `startMethod` — one of: describe · attach · template · sample (D023).
- `template` — the chosen template label, if the template method was used (Event · Marketing Campaign · Product / Software Launch · Strategic Initiative · Generic Project Plan).
- `phaseOrigin` — whether it began as an Alpha authenticated project or a GA anonymous first-run.
- Later slices own the plan artifacts; Slice 1 only carries the draft to the hand-off.

### Intake evidence
The raw inputs the user supplies to start analysis.
- `description` — free-text brief from the composer (may be a template-seeded string).
- `documents[]` — attached files; each has a display name (e.g. `document_1.pdf`) and a `type` from {pdf, docx, txt, md, pptx, xlsx, csv} (accepted attachment types, D033). Fake/simulated — no upload occurs.
  - Illustrative caps (D033): ~10 MB per file, up to ~10 files. Tier size rules are owner-TBD (GA).
  - Table-bearing types (`xlsx`, `csv`) also carry extracted **structured rows** alongside their text; those rows inform Resources/Schedule during ingestion (D034).
- Constraint: at least one of {non-empty description, ≥1 document, selected template} is required to start (minimum-to-value gate).

### AnalysisRun
A single analysis pass over the intake evidence (D005).
- `type` — Initial Analysis (Fast Pass) | Extended Analysis (Deep Pass). User-facing labels only.
- `state` — analyzing → complete (Extended supersedes Initial when complete).
- `confidenceBand` — illustrative maturity band on completion (e.g. Moderate), on the neutral ramp — never health-colored (D002/D003).
- `reliability` — qualifier shown with the band (e.g. Moderate reliability).
- Slice 1 shows Initial Analysis end-to-end and kicks off Extended Analysis; the full run detail belongs to later slices.

## Prototype-local storage rules (client-side only — D016)
- All state lives in `localStorage` under the namespace `oslo-s1-*` (JSON-encoded). No cookies, no server, no DB.
- Persisted keys:
  - `oslo-s1-phase` — release-phase preview (`alpha` | `ga`).
  - `oslo-s1-account` — the simulated `Account` (`{email, name, active}`).
  - `oslo-s1-staySignedIn` — boolean session persistence.
  - `oslo-s1-orientSeen` — proficiency flag; once true, the one-time orientation does not reappear (D027 sunset).
- Ephemeral (in-memory only, not persisted): attached file chips, composer text, current AnalysisRun timers, `ANON_RUN` (whether the current run is a GA anonymous first-run).
- **Restart/Reset** clears `orientSeen`, `account`, and `staySignedIn` and reloads, returning to the Alpha invitation entry.
- **Claim-through (GA):** replaces the anonymous state with an `Account`, carrying the draft project through unchanged (D026).
