"""Testes automatizados do gerenciamento de estado do frontend (store.py)."""
from unittest.mock import patch
from frontend.state.store import inicializar, registrar


def test_inicializar_cria_chaves():
    fake_state = {}
    with patch("frontend.state.store.st.session_state", fake_state):
        inicializar()
        assert "registros" in fake_state
        assert isinstance(fake_state["registros"], list)
        assert fake_state["pendente"] is None
        assert fake_state["pagina"] == "Fazer relato"
        assert fake_state["ultimo_registro"] is None


def test_registrar_gera_id_local_e_insere_no_historico():
    fake_state = {"registros": []}
    with patch("frontend.state.store.st.session_state", fake_state):
        entrada = {
            "bairro": "Perdizes",
            "categoria_informada": "Calçadas e acessibilidade",
            "descricao": "Calçada irregular com buracos profundos e degraus."
        }
        resultado = {
            "categoria": "Calçadas e acessibilidade",
            "prioridade": "alta",
            "resumo": "Calçada irregular em Perdizes com buracos.",
            "orientacao": "Caminhar com atenção e buscar reparo.",
            "encaminhamento": "Manutenção de calçadas"
        }

        registro = registrar(entrada, resultado, corrigido=False, modo="demonstracao")

        assert registro["id"].startswith("LOCAL-")
        assert registro["bairro"] == "Perdizes"
        assert registro["revisao"] == "Confirmado sem alterações"
        assert registro["origem"] == "Exemplo fictício"
        assert len(fake_state["registros"]) == 1
        assert fake_state["ultimo_registro"]["id"] == registro["id"]


def test_registrar_com_correcao_humana():
    fake_state = {"registros": []}
    with patch("frontend.state.store.st.session_state", fake_state):
        entrada = {
            "bairro": "Pinheiros",
            "categoria_informada": "Outros",
            "descricao": "Luminária queimada deixando a esquina completamente escura."
        }
        resultado_corrigido = {
            "categoria": "Iluminação pública",
            "prioridade": "alta",
            "resumo": "Poste de iluminação sem lâmpada na esquina.",
            "orientacao": "Evitar o local à noite.",
            "encaminhamento": "Iluminação pública"
        }

        registro = registrar(
            entrada,
            resultado_corrigido,
            corrigido=True,
            modo="llm",
            avaliacao_ia="Incorreta / Ajustei manualmente"
        )

        assert registro["revisao"] == "Corrigido pelo cidadão"
        assert registro["origem"] == "Análise de LLM revisada"
        assert registro["avaliacao_ia"] == "Incorreta / Ajustei manualmente"
        assert fake_state["registros"][0]["categoria"] == "Iluminação pública"
