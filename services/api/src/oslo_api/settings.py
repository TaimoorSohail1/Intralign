from pathlib import Path

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
