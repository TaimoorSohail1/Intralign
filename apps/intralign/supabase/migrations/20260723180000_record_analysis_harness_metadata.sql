alter table public.analysis_node_attempts
  add column provider text,
  add column model_id text,
  add column prompt_version text,
  add column provider_response_id text,
  add column input_tokens integer check (input_tokens >= 0),
  add column output_tokens integer check (output_tokens >= 0),
  add column duration_ms integer check (duration_ms >= 0),
  add column execution_mode text
    check (execution_mode in ('primary', 'fallback')),
  add column fallback_reason text;

comment on column public.analysis_node_attempts.provider_response_id is
  'Safe provider trace identifier. Raw prompts, outputs and credentials are never stored here.';
