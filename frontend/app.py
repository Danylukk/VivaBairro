"""Ponto de entrada Streamlit; orquestra features sem concentrar lógica."""
import streamlit as st
from frontend.features import relatar, painel, sobre
from frontend.providers.api import API_BASE_URL, obter_status
from frontend.state.store import inicializar
from frontend.ui.theme import aplicar_tema

st.set_page_config(
    page_title="VivaBairro | CitizenTech FIAP",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="auto"
)

aplicar_tema()
inicializar()

# Tratamento seguro de redirecionamento de tela antes de renderizar os widgets
opcoes_nav = ["Fazer relato", "Painel de relatos", "Como funciona"]
if st.session_state.get("redirecionar_pagina"):
    st.session_state["nav_radio"] = st.session_state.pop("redirecionar_pagina")

with st.sidebar:
    st.markdown("# 🏘️ VivaBairro")
    st.caption("CitizenTech · Global Solution FIAP 2026.2")
    st.divider()

    pagina_selecionada = st.radio(
        "Navegação Principal:",
        options=opcoes_nav,
        key="nav_radio"
    )
    st.session_state["pagina"] = pagina_selecionada

    st.divider()
    status = obter_status(API_BASE_URL)
    if status.get("status") != "ok":
        st.error("⚠️ **Serviço Indisponível**\n\nNão foi possível conectar ao servidor de processamento no momento.")
    elif status.get("modo") == "demonstracao":
        st.info("🧪 **Modo de Demonstração**\n\nSimulação local ativa para testes da interface. Nenhuma chamada externa é realizada.")
    else:
        st.success("✅ **Assistente Conectado**\n\nServiço de análise inteligente pronto para uso.")

    total_registros = len(st.session_state.get("registros", []))
    st.metric("Relatos nesta sessão", total_registros)

    st.divider()
    st.caption("🔒 **Projeto Acadêmico FIAP**\n\nNenhuma informação é transmitida à Prefeitura ou armazenada permanentemente.")

# Roteamento de telas
pagina_atual = st.session_state["pagina"]
if pagina_atual == "Fazer relato":
    relatar.renderizar()
elif pagina_atual == "Painel de relatos":
    painel.renderizar()
else:
    sobre.renderizar()

st.markdown('<p class="viva-footnote">VivaBairro CitizenTech — Protótipo acadêmico para a Global Solution FIAP 2026.2. Os dados residem unicamente na memória desta sessão.</p>', unsafe_allow_html=True)
