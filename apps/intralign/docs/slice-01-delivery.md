# Slice 1 delivery record

## Implemented tracer

1. Seeded Owner signs in through Supabase Auth.
2. Owner sends a seven-day, role-bearing invitation.
3. Mailpit receives a link containing a one-time raw token; PostgreSQL stores only its SHA-256 digest.
4. A new user activates, receives a membership, sees Welcome, and creates a draft project only when clicking **Start your first project**.
5. An existing user signs in with the invited email and accepts the membership without creating a duplicate account.
6. Owner can list, resend, and revoke invitations; every state change is audited.
7. Session cookies are HttpOnly/SameSite and rotate with the selected 24-hour or 30-day lifetime.

## Release gates

- Invite-only Auth and tenant RLS migration replay from an empty database.
- Python application, HTTP, identity, SMTP, PostgreSQL integration, and security tests.
- Vitest component contract, ESLint/React rules, and production Next.js build.
- Playwright full tracer and invitation-management scenarios at 1440×1000 and mobile emulation.

## Deliberately outside Slice 1

Document upload/parsing, deterministic or AI analysis, LangGraph, pgvector retrieval, Overview, anonymous access, social login, MFA, password reset, and billing.
