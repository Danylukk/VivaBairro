"""Configuração por variáveis de ambiente. Nunca armazenar chaves no código."""
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    llm_provider: str = "demo"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    app_env: str = "development"
    cors_origins: str = "http://localhost:8501,http://127.0.0.1:8501"
    llm_timeout_seconds: float = 25.0

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            llm_provider=os.getenv("LLM_PROVIDER", "demo").strip().lower(),
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            app_env=os.getenv("APP_ENV", "development").lower(),
            cors_origins=os.getenv("CORS_ORIGINS", "http://localhost:8501,http://127.0.0.1:8501"),
            llm_timeout_seconds=float(os.getenv("LLM_TIMEOUT_SECONDS", "25")),
        )

    def validate(self) -> None:
        if self.llm_provider not in ("demo", "openai"):
            raise ValueError("LLM_PROVIDER deve ser 'demo' ou 'openai'")
        if self.llm_provider == "openai" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY é obrigatória para LLM_PROVIDER=openai")
        if self.app_env == "production" and "*" in self.cors_origins:
            raise ValueError("CORS com origem * é proibido em produção")
        if self.llm_timeout_seconds <= 0:
            raise ValueError("Timeout inválido")
