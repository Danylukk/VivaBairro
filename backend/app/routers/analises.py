"""Endpoints públicos com contratos Pydantic e erros legíveis."""
from fastapi import APIRouter, HTTPException, Request
from backend.app.schemas.relatos import RelatoEntrada, RespostaAnalise, SaudeResposta
from backend.app.pipelines.analise import processar
from backend.app.providers.llm import LLMIndisponivel

router = APIRouter()


@router.get("/health", response_model=SaudeResposta)
def health(request: Request) -> SaudeResposta:
    return SaudeResposta(modo="llm" if request.app.state.settings.llm_provider == "openai" else "demonstracao")


@router.post("/api/v1/analises", response_model=RespostaAnalise)
def analisar(entrada: RelatoEntrada, request: Request) -> RespostaAnalise:
    try:
        return processar(entrada, request.app.state.settings)
    except LLMIndisponivel as exc:
        raise HTTPException(status_code=503, detail="A análise não está disponível agora. Tente novamente mais tarde.") from exc
