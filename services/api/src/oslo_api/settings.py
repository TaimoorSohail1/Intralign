from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "postgresql+psycopg://postgres:postgres@127.0.0.1:55322/postgres"
    supabase_url: str = "http://127.0.0.1:55321"
    supabase_secret_key: str = Field(min_length=20)
    web_url: str = "http://localhost:3000"
    smtp_host: str = "127.0.0.1"
    smtp_port: int = 55325
    email_sender: str = "OSLO <no-reply@oslo.local>"
    analysis_worker_threads: int = Field(default=4, ge=1, le=32)
    analysis_artifact_worker_threads: int = Field(default=4, ge=1, le=16)
    analysis_phase_delay_ms: int = Field(default=120, ge=0, le=10_000)
    extended_analysis_delay_ms: int = Field(default=750, ge=0, le=60_000)
    analysis_harness: Literal["auto", "deterministic", "openai"] = "auto"
    openai_api_key: str | None = None
    openai_model: str | None = None
    openai_fast_model: str = "gpt-5.6-luna"
    openai_extended_model: str = "gpt-5.6-terra"
    openai_fallback_model: str | None = None
    # Dense structured responses routinely exceed 30 seconds even when the input is
    # correctly bounded. Keep this below the worker's external timeout while allowing
    # each artifact shard enough time to finish once instead of being retried mid-call.
    openai_timeout_seconds: float = Field(default=90, ge=5, le=120)
    # Workflow-level artifact recovery already retries one isolated artifact and
    # can publish a visibly provisional fallback. Avoid multiplying the SDK retry
    # loop inside that recovery path, which previously allowed one artifact to
    # consume four full provider timeouts.
    openai_max_retries: int = Field(default=0, ge=0, le=3)
    object_storage_path: Path = Path(__file__).resolve().parents[2] / ".data" / "uploads"
