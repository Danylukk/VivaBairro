"""Ponto de entrada Streamlit; orquestra features sem concentrar lógica."""
import streamlit as st
from frontend.features import relatar, painel, sobre
from frontend.providers.api import API_BASE_URL, obter_status
from frontend.state.store import inicializar
from frontend.ui.theme import aplicar_tema

st.set_page_config(page_title="VivaBairro | CitizenTech", page_icon="🏘️", layout="wide", initial_sidebar_state="expanded")
aplicar_tema()
inicializar()
with st.sidebar:
    st.markdown("# 🏘️ VivaBairro")
    st.caption("CitizenTech · GS FIAP 2026.2")
    st.divider()
    pagina = st.radio("Onde você quer ir?", ["Fazer relato", "Painel de relatos", "Como funciona"], key="pagina")
    st.divider()
    status = obter_status(API_BASE_URL)
    if status.get("status") != "ok":
        st.error("⚠️ Serviço indisponível")
    elif status["modo"] == "demonstracao":
        st.info("🧪 Demonstração simulada")
    else:
        st.success("✅ IA conectada via API")
    st.caption("Projeto acadêmico. Não é um canal oficial de atendimento.")

if pagina == "Fazer relato":
    relatar.renderizar()
elif pagina == "Painel de relatos":
    painel.renderizar()
else:
    sobre.renderizar()
st.markdown('<p class="viva-footnote">VivaBairro — protótipo acadêmico FIAP · Os dados são mantidos apenas na sessão atual.</p>', unsafe_allow_html=True)
