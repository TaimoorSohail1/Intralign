# Release 1 — Visual Design & Branding Specification v1

**Document Type:** Visual/brand spec — the **designer↔code seam** (commodity presentation/Render layer) · **Status:** Interim baseline; brand values **owner/designer-TBD** · **Date:** 2026-06-05
**Purpose:** the corpus specs UI **behavior/structure** richly (the UX surface specs + their conformance "fail conditions") but **deliberately defers visual styling** ("introduces no styling," "exact copy/visual form deferred"). This document fills that seam **without inventing your brand**: it defines a **design-token contract** so R1 builds to a clean default now and your designer's brand applies later as a **token swap, not a rebuild.**

> **Decision (owner, 2026-06-05):** R1 is the owner's **validation vehicle** → **a clean, tokenized default is sufficient**; brand is a **fast-follow token swap**. A **designer will deliver** the brand source of truth; until then, brand tokens carry **clearly-marked placeholder values** and are **owner/designer-TBD** (Anti-Assumption Protocol — *escalate, don't invent a brand identity*).

---

## 0. The two kinds of "UI correctness"

| Fidelity | Source of truth | Status | Verified by |
|---|---|---|---|
| **Behavioral / structural** (surfaces, actions, states, epistemic-safety, limit-reached interactions) | the UX surface specs + their **fail conditions** | **Specified** (rich) | per-surface conformance checklist (§6) |
| **Visual / brand** (color, type, spacing, components, logo, microcopy) | **this token contract** → filled by the designer | **Token contract now; values TBD** | token-adherence lint + visual review (§6) |

The build can proceed on **clean default tokens**; behavior is verifiable today, brand is verifiable when the designer delivers.

## 1. The design-token contract (the seam — non-negotiable rule)

**All color, type, spacing, radius, shadow, and motion are expressed as tokens. No hardcoded hex/px brand values anywhere in components.** This is what makes the brand a swappable layer: when the designer delivers, you replace token *values* in one file and the whole app re-themes, guaranteed total by the lint (§6.3).

**Implementation:** **Tailwind + shadcn/ui** (already the React stack) with tokens as **CSS variables** mapped into the Tailwind theme. Components consume **semantic** token names (`bg-surface`, `text-muted`, `border-default`), never raw palette values.

### 1.1 Token categories
```css
:root {
  /* COLOR — semantic. INTERIM values; SEED FROM intralign.ai (owner direction 2026-06-05),
     then designer supersedes. The exact intralign.ai hexes are TBD — see note below; the
     values here are a neutral professional stand-in, NOT asserted to be intralign's brand. */
  --color-bg:           #0b0c0f;   /* app background — TBD intralign */
  --color-surface:      #16181d;   /* cards/panels */
  --color-surface-2:    #1e2127;
  --color-text:         #e7e9ee;
  --color-text-muted:   #9aa1ad;
  --color-border:       #2a2e37;
  --color-primary:      #5b8cff;   /* brand accent — TBD, seed from intralign.ai */
  --color-primary-fg:   #0b0c0f;
  --color-focus:        #5b8cff;

  /* SYSTEM state (success/warn/danger — UI feedback ONLY, never project "health") */
  --color-success:      #3fb27f;
  --color-warning:      #d6a13c;
  --color-danger:       #e5645e;

  /* TYPE */
  --font-sans: "Inter", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;   /* IDs, evidence refs */
  --text-xs:12px; --text-sm:14px; --text-base:16px; --text-lg:18px;
  --text-xl:20px; --text-2xl:24px; --text-3xl:30px; --text-4xl:36px;
  --weight-regular:400; --weight-medium:500; --weight-semibold:600;
  --leading-tight:1.25; --leading-normal:1.5;

  /* SPACING (4px base) */ --s1:4px; --s2:8px; --s3:12px; --s4:16px; --s6:24px; --s8:32px; --s12:48px;
  /* RADIUS */ --radius-sm:6px; --radius-md:10px; --radius-lg:16px; --radius-full:9999px;
  /* SHADOW */ --shadow-sm:0 1px 2px rgba(0,0,0,.3); --shadow-md:0 4px 16px rgba(0,0,0,.4);
  /* MOTION */ --dur-fast:120ms; --dur-base:200ms; --ease:cubic-bezier(.2,.6,.2,1);
  /* LAYOUT */ --container-max:1200px; --bp-md:768px; --bp-lg:1024px;
}
```
*(Interim = a neutral professional dark theme. Light theme = the same token names under `:root[data-theme="light"]`. The designer overwrites values; **component code never changes**.)*

> **Interim palette source — `intralign.ai` (owner direction, 2026-06-05).** Seed the interim color tokens from the **intralign.ai** brand palette so R1 feels on-direction before the designer delivers. **Exact hexes are TBD** — `intralign.ai` is client-rendered, so they need to be captured from the live site (designer, browser inspector, or a connected extraction) rather than guessed; the values above are a stand-in **not asserted to be intralign's**. Map intralign's primary/accent → `--color-primary`, its background/surface neutrals → `--color-bg`/`--color-surface`, its text neutrals → `--color-text(-muted)`. The designer's eventual brand delivery supersedes this seed entirely (single token-swap, §5).

### 1.2 OSLO-specific epistemic color constraints *(this is where the product's rules shape the visuals — brief the designer on these)*

These are **not stylistic preferences** — they protect OSLO's epistemic invariants and the UX specs' fail-conditions:

- **Confidence & CAF are NOT health/traffic-light colored.** Confidence (0–100) is **understanding maturity, not a probability or a good/bad health score** (Seam Audit 001 S6; UX fail-conditions forbid fabricated "health"). Use a **neutral maturity ramp** (e.g. low-saturation cool→warm or a single-hue intensity scale), **never red=bad / green=good**. A red low-confidence reads as "failing project" — which OSLO must never imply.
  ```css
  --conf-low: #6b7280; --conf-medium: #8b93a7; --conf-high: #b9c2d8;  /* maturity ramp, not health */
  ```
- **Severity (Issues) may use an alert ramp** (critical/moderate/warning) — these *are* problem signals, so warning/danger hues are correct **for issues**, distinct from confidence.
- **Analysis state** (analyzing / analyzed / **stale**) needs a clear, non-alarming **stale** treatment (muted + a "may be out of date" affordance) — stale is honest, not an error.
- **Epistemic labels** (Attested vs Derived, provisional banners, reliability) must be **visually legible and consistent** — they are a safety feature, not decoration.

### 1.3 Microcopy / voice tone
OSLO's voice: **honest, precise, never overstating.** "OSLO advises; you decide." Never imply certainty, health, or that OSLO acted on the world. Warm but professional. Examples:
- Empty: *"No projects yet — add a few documents and OSLO will map your understanding."* (not "Get started now!")
- Limit (UP-3): *"Free includes 1 active project. Upgrade to Basic for 3, or archive this one to start another."* (honest, two paths — never a dark pattern, per Seam Audit 001)
- Partial analysis: *"This is a partial orientation — your project exceeds the Free size. Upgrade to analyze it in full."* (honest disclosure = the upgrade moment)
- Error: *"Analysis didn't complete. Your work is safe; try again."* (no fabricated state)

## 2. Component baseline (build to this now)
- **shadcn/ui + Tailwind**, themed entirely via §1 tokens. Gives instant visual coherence on a clean default.
- Build the OSLO surfaces (MRI, Finding/Recommendation Panels, Chat, Overview, Dashboard, Nav shell) **as composed shadcn primitives** so re-theming is global.
- **Desktop-first** (the UX specs are desktop-canonical); responsive is secondary for R1.
- Put every reusable component in **Storybook** from day one (the visual review surface, §6).

## 3. Accessibility target (R1)
- **WCAG 2.1 AA** as the working baseline (the corpus flags accessibility as TBD — adopt AA): contrast ≥4.5:1 body / 3:1 large; visible focus (`--color-focus`); full keyboard nav; semantic HTML/ARIA; respects `prefers-reduced-motion` (and **never** animates during an active Fast/Deep pass — the no-interrupt rule). Final tier is an owner confirm (Open-TBD).

## 4. What we need from the designer *(input checklist — maps 1:1 to the tokens)*
Delivering these = filling the token contract; no code change required.
- **Brand assets:** logo (SVG, light/dark), favicon, app icon, OG/social image.
- **Color:** primary + accent hexes; background/surface/text/border for **light AND dark**; the **confidence maturity ramp** (briefed per §1.2 — *not* a health palette); severity ramp; success/warn/danger.
- **Type:** font family(ies) + license/host (Google/Adobe/self), the type scale & weights, mono for IDs/evidence.
- **Spacing/shape:** base unit, radius, shadow/elevation, any density preference.
- **Components:** any redlines that differ from shadcn defaults (buttons, inputs, cards, panels, the MRI/CAF visualizations — the CAF Triangle/Heatmap especially, since those are signature surfaces).
- **Motion & iconography:** icon set (or "use Lucide"), motion durations/feel.
- **The OSLO constraints brief:** §1.2 (confidence ≠ health color) + §1.3 (honest, no-dark-pattern voice) — share these *before* they design, so the brand respects the epistemics.

## 5. Brand application = a token swap
When the designer delivers: one PR replaces token **values** (and adds the font + assets). The §6.3 lint proves no component hardcoded a brand value, so the swap is **total and low-risk**. Visual-regression snapshots (§6.2) catch any unintended drift. This is the entire "apply the brand" step — by design.

## 6. Verification — how to ensure it's implemented as expected

### 6.1 Behavioral / structural conformance *(run now)*
- For each surface, a **conformance checklist built from that UX spec's own "fail conditions."** Example (Project Dashboard): *computes no score/health · doesn't fabricate indicators · Create Project stays enabled at the limit (CHG-065) · archiving is non-destructive · honest empty/failure states.*
- **PR gate:** Claude Code cites the surface spec; the PR includes **screenshots** of each state (empty/loading/error/limit-reached/stale); owner reviews against the checklist. **Fail the PR** if any fail-condition is violated.

### 6.2 Visual conformance *(activates when brand lands; baseline now)*
- **Storybook** review of components in isolation (now, on default tokens).
- **Visual-regression** (Playwright or Chromatic screenshots) as a CI gate — catches unintended visual drift on every PR; becomes the brand-fidelity gate once Figma exists (screenshot ↔ Figma diff).
- Once the designer delivers Figma: **per-surface visual diff** against the designs.

### 6.3 The token-adherence lint *(the keystone — run now)*
- **stylelint / ESLint rule (or Tailwind config lockdown): reject any hardcoded color hex or non-token spacing in component code** — all styling must reference tokens / Tailwind theme classes. This is what *guarantees* the brand is fully swappable and that "implemented as expected" is enforceable mechanically, not by eyeballing.

### 6.4 The loop
Claude Code builds to the surface spec + default tokens → PR with screenshots + Storybook → owner reviews behavioral conformance now, visual conformance when brand lands → designer delivers → token-swap PR → visual-regression confirms. Behavior is right from day one; brand is right the day the tokens land.

---
*This specification fills the deliberate visual/brand gap in OSLO's Release-1 UX corpus by defining a design-token contract as the designer↔code seam: all color, type, spacing, radius, shadow, and motion are tokens (Tailwind + shadcn/ui), so R1 builds to a clean, accessible default now and the designer's brand applies later as a single-PR token swap rather than a rebuild, with a token-adherence lint guaranteeing nothing brand-related is hardcoded. It encodes OSLO-specific epistemic constraints on the visuals (Confidence/CAF rendered as a neutral maturity ramp, never a red/green health palette; honest, no-dark-pattern microcopy), sets a WCAG-AA accessibility baseline, provides a designer-input checklist that maps one-to-one onto the tokens, and defines a two-track verification process — behavioral/structural conformance (checklists from each UX spec's fail-conditions, screenshot PR review) runnable now, and visual conformance (Storybook, visual-regression, Figma diff) that activates when the brand source of truth arrives. Brand values remain owner/designer-TBD per the Anti-Assumption Protocol: the build escalates rather than invents a brand identity.*

**Release 1 Visual Design & Branding Specification v1 complete.**
