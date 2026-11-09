"""Estado explícito para preservar histórico durante reruns do Streamlit."""
from datetime import datetime
from uuid import uuid4
import streamlit as st


def inicializar() -> None:
    defaults = {"registros": [], "pendente": None, "pagina": "Fazer relato", "mensagem_sucesso": ""}
    for nome, inicial in defaults.items():
        if nome not in st.session_state:
            st.session_state[nome] = inicial.copy() if isinstance(inicial, list) else inicial


def registrar(entrada: dict, resultado: dict, corrigido: bool, modo: str) -> dict:
    registro = {
        "id": "LOCAL-" + uuid4().hex[:8].upper(),
        "quando": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "bairro": entrada["bairro"],
        "categoria": resultado["categoria"],
        "prioridade": resultado["prioridade"],
        "resumo": resultado["resumo"],
        "origem": "Exemplo fictício" if modo == "demonstracao" else "Análise de LLM revisada",
        "revisao": "Corrigido pelo cidadão" if corrigido else "Confirmado pelo cidadão",
    }
    st.session_state["registros"].insert(0, registro)
    return registro

