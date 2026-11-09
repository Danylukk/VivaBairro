"""Estado explícito para preservar histórico e fluxo durante reruns do Streamlit."""
from datetime import datetime
from uuid import uuid4
import streamlit as st


def inicializar() -> None:
    """Garante a existência de todas as chaves do estado da sessão."""
    defaults = {
        "registros": [],
        "pendente": None,
        "pagina": "Fazer relato",
        "mensagem_sucesso": "",
        "ultimo_registro": None,
    }
    for nome, inicial in defaults.items():
        if nome not in st.session_state:
            st.session_state[nome] = inicial.copy() if isinstance(inicial, list) else inicial


def registrar(entrada: dict, resultado: dict, corrigido: bool, modo: str, avaliacao_ia: str = "Útil") -> dict:
    """Registra uma análise confirmada pelo cidadão apenas no histórico local da sessão."""
    registro = {
        "id": "LOCAL-" + uuid4().hex[:8].upper(),
        "quando": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "bairro": entrada["bairro"],
        "categoria": resultado["categoria"],
        "prioridade": resultado["prioridade"],
        "resumo": resultado["resumo"],
        "orientacao": resultado.get("orientacao", ""),
        "encaminhamento": resultado.get("encaminhamento", ""),
        "origem": "Exemplo fictício" if modo == "demonstracao" else "Análise de LLM revisada",
        "revisao": "Corrigido pelo cidadão" if corrigido else "Confirmado sem alterações",
        "avaliacao_ia": avaliacao_ia,
    }
    st.session_state["registros"].insert(0, registro)
    st.session_state["ultimo_registro"] = registro
    return registro
