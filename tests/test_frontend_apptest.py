"""Testes automatizados da UI Streamlit utilizando o framework nativo AppTest."""
from unittest.mock import patch
from streamlit.testing.v1 import AppTest


def test_app_inicializacao():
    at = AppTest.from_file("frontend/app.py", default_timeout=15)
    with patch("frontend.providers.api.obter_status", return_value={"status": "ok", "modo": "demonstracao"}):
        at.run()
    assert not at.exception
    assert at.title[0].value == "VivaBairro — Sua Voz na Cidade"
    assert len(at.radio) >= 1
    assert at.radio[0].value == "Fazer relato"


def test_app_navegacao_painel():
    at = AppTest.from_file("frontend/app.py", default_timeout=15)
    with patch("frontend.providers.api.obter_status", return_value={"status": "ok", "modo": "demonstracao"}):
        at.run()
        at.radio[0].set_value("Painel de relatos").run()
    assert not at.exception
    assert at.title[0].value == "Painel Interativo de Relatos"


def test_app_navegacao_sobre():
    at = AppTest.from_file("frontend/app.py", default_timeout=15)
    with patch("frontend.providers.api.obter_status", return_value={"status": "ok", "modo": "demonstracao"}):
        at.run()
        at.radio[0].set_value("Como funciona").run()
    assert not at.exception
    assert at.title[0].value == "Arquitetura, Ética e Impacto Social"
