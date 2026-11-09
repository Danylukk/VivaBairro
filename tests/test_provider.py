"""Contratos com o provedor real sem enviar requisição externa ou gastar tokens."""
from unittest.mock import patch, MagicMock
import httpx
import pytest
from backend.app.config import Settings
from backend.app.providers.llm import analisar_openai, LLMIndisponivel
from backend.app.schemas.relatos import RelatoEntrada

ENTRADA = RelatoEntrada(
    bairro="Centro", categoria_informada="Iluminação pública",
    descricao="A iluminação da praça está danificada há vários dias e o local fica muito escuro.",
)
SETTINGS = Settings(llm_provider="openai", openai_api_key="FAKE_TOKEN")
RESULTADO = {
    "categoria": "Iluminação pública", "prioridade": "media",
    "resumo": "Praça do Centro está com iluminação danificada.",
    "justificativa": "A falta de luz pode prejudicar a circulação de pessoas.",
    "orientacao": "Consulte o serviço municipal de iluminação e evite áreas com pouca visibilidade.",
    "encaminhamento": "Iluminação pública", "atencao_imediata": False,
}


def resposta_fake(body):
    response = MagicMock()
    response.raise_for_status.return_value = None
    response.json.return_value = body
    return response


def test_provedor_retorna_pydantic_valido():
    with patch("backend.app.providers.llm.httpx.Client") as client:
        client.return_value.__enter__.return_value.post.return_value = resposta_fake({"choices": [{"message": {"content": __import__("json").dumps(RESULTADO)}}]})
        resultado = analisar_openai(ENTRADA, SETTINGS)
    assert resultado.categoria == "Iluminação pública"
    args, kwargs = client.return_value.__enter__.return_value.post.call_args
    assert args[0].endswith("/chat/completions")
    assert kwargs["json"]["response_format"] == {"type": "json_object"}
    assert kwargs["headers"]["Authorization"] == "Bearer FAKE_TOKEN"


def test_rejeita_resposta_invalida():
    with patch("backend.app.providers.llm.httpx.Client") as client:
        client.return_value.__enter__.return_value.post.return_value = resposta_fake({"choices": [{"message": {"content": '{"prioridade":"alta"}'}}]})
        with pytest.raises(LLMIndisponivel):
            analisar_openai(ENTRADA, SETTINGS)


def test_timeout_e_convertido_em_erro_seguro():
    with patch("backend.app.providers.llm.httpx.Client") as client:
        client.return_value.__enter__.return_value.post.side_effect = httpx.ReadTimeout("timeout")
        with pytest.raises(LLMIndisponivel):
            analisar_openai(ENTRADA, SETTINGS)


def test_nao_aceita_saida_sem_choice():
    with patch("backend.app.providers.llm.httpx.Client") as client:
        client.return_value.__enter__.return_value.post.return_value = resposta_fake({"choices": []})
        with pytest.raises(LLMIndisponivel):
            analisar_openai(ENTRADA, SETTINGS)
