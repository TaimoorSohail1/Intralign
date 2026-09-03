alter table public.billing_checkout_sessions
  add column wall_key text not null default 'multiPlan'
  check (wall_key in ('multiOutcome', 'multiPlan', 'envelope', 'schedule'));

comment on column public.billing_checkout_sessions.wall_key is
  'Capacity wall that led to this hosted Checkout attempt.';
