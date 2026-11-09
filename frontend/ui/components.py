"""Componentes reutilizados entre telas com diferentes parâmetros."""
import streamlit as st


def cabecalho(etapa: str, titulo: str, descricao: str) -> None:
    """Reutilizado por todas as features do sistema."""
    st.markdown(f'<div class="viva-kicker">{etapa}</div>', unsafe_allow_html=True)
    st.title(titulo)
    st.markdown(descricao)


def faixa_prioridade(prioridade: str) -> None:
    mensagem = {
        "alta": (st.error, "🔴 Prioridade alta — precisa de atenção"),
        "media": (st.warning, "🟠 Prioridade média — acompanhar"),
        "baixa": (st.success, "🟢 Prioridade baixa — acompanhamento de rotina"),
    }
    funcao, texto = mensagem.get(prioridade, (st.info, "Classificação a revisar"))
    funcao(texto, icon=None)


def dica_privacidade() -> None:
    st.caption("🔒 Não informe nome completo, CPF, telefone, endereço exato ou dados de terceiros. Os registros ficam apenas nesta sessão do navegador, sem envio à Prefeitura.")
