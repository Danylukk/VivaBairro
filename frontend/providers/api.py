"""Cliente HTTP dedicado; nenhuma chamada ao LLM acontece aqui."""
import os
import httpx
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")


class ErroAmigavel(Exception):
    """Erro sem detalhes internos para o cidadão."""


@st.cache_data(ttl=20, show_spinner=False)
def obter_status(url: str) -> dict:
    try:
        with httpx.Client(timeout=3) as client:
            resposta = client.get(f"{url}/health")
            resposta.raise_for_status()
            return resposta.json()
    except (httpx.HTTPError, ValueError):
        return {"status": "indisponivel", "modo": "desconhecido"}


def enviar_relato(payload: dict) -> dict:
    """Não usar cache para conteúdos submetidos pelos cidadãos."""
    try:
        with httpx.Client(timeout=32) as client:
            response = client.post(f"{API_BASE_URL}/api/v1/analises", json=payload)
        if response.status_code == 422:
            raise ErroAmigavel("Confira o bairro e o relato: o texto deve ter entre 30 e 900 caracteres.")
        if response.status_code in (502, 503, 504):
            raise ErroAmigavel("O serviço de análise está temporariamente indisponível. Tente novamente.")
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict) or not isinstance(data.get("resultado"), dict):
            raise ErroAmigavel("Recebemos uma resposta inesperada. Tente novamente.")
        return data
    except httpx.TimeoutException as exc:
        raise ErroAmigavel("A análise demorou mais que o esperado. Tente de novo.") from exc
    except httpx.ConnectError as exc:
        raise ErroAmigavel("Não foi possível conectar ao serviço. Verifique a conexão e tente novamente.") from exc
    except (httpx.HTTPError, ValueError) as exc:
        raise ErroAmigavel("Não foi possível concluir a análise. Tente novamente.") from exc
