alter table public.project_report_deliveries
  add column currency_state text not null default 'current'
    check (currency_state in ('current', 'previous_analysis')),
  add column previous_analysis_confirmed boolean not null default false;

comment on column public.project_report_deliveries.currency_state is
  'Whether the delivered report used the current snapshot or a retained previous analysis.';
comment on column public.project_report_deliveries.previous_analysis_confirmed is
  'Records explicit sender confirmation when a previous-analysis report is delivered.';
