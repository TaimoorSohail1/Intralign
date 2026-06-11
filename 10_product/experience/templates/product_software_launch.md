# Product / Software Launch — "Pulse" Team Check-in App (Sample)

> _Sample project (project_type: `product_launch`). A **fictitious worked example** so you can see OSLO analyze a realistic launch plan right away. Edit it to fit your launch, or start fresh._

## Outcome & Success Metrics
Launch **Pulse**, a lightweight async team check-in app, to general availability by **June 30**. Success = **300 activated teams** and **40% week-4 retention** within 60 days of GA, with a **<2%** crash-free-session shortfall.

## Target Users
People managers of distributed teams (5–30 people) who run weekly status rituals over chat and lose signal in long threads. They want a 2-minute structured check-in that rolls up into a digest. They'll adopt because it replaces a manual ritual they already dislike.

## Scope & Non-Goals
**In scope (this launch)**
- Async check-in templates, scheduled prompts, manager digest
- Slack + email delivery; web + iOS apps
- Free tier + Team tier billing

**Non-goals**
- Android app (fast-follow)
- Performance-review or HR integrations
- Analytics dashboards beyond the digest

## Requirements
- Check-in round-trip in **under 2 minutes** for a respondent
- Digest delivered reliably on schedule (>99%)
- SSO (Google/Microsoft) for Team tier
- WCAG 2.1 AA; data export; account deletion

## Release Milestones
- **Apr 30** — Feature complete
- **May 15** — Private beta (25 teams)
- **Jun 10** — Code freeze + launch readiness review
- **Jun 30** — GA + launch announcement
- **Jul 31** — Post-launch retro

## Dependencies & Risks
- *Dependency:* Slack app-directory review (lead time ~2 weeks) — submit by May 20.
- *Risk:* beta retention below target signals weak core loop — gate GA on a beta retention check.
- *Risk:* SSO edge cases delay Team tier — spike auth early in beta.

## Stakeholders
- **Decision-maker (launch go/no-go):** VP Product
- **Owners:** PM (scope), Eng Lead (delivery), Design Lead (UX), GTM Lead (announcement), Support Lead (readiness)
