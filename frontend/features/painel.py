"""Painel com 2 filtros interativos, gráfico Plotly e dados da sessão."""
import pandas as pd
import streamlit as st
from frontend.demo_data import exemplos_ficticios
from frontend.ui.components import cabecalho
from frontend.visualization import aplicar_filtros, contagem_prioridade, grafico_prioridades


def renderizar() -> None:
    cabecalho("02 / Acompanhe as informações", "Painel de relatos", "Acompanhe os registros desta sessão e filtre os resultados para entender os tipos de problemas relatados.")
    registros = st.session_state["registros"]
    if not registros:
        st.info("Ainda não há relatos confirmados nesta sessão. Registre o primeiro relato ou use exemplos totalmente fictícios para explorar o painel.")
        if st.button("Carregar 6 exemplos fictícios", type="primary"):
            st.session_state["registros"] = exemplos_ficticios()
            st.rerun()
        return
    qtd_simulados = sum(r["origem"] == "Exemplo fictício" for r in registros)
    if qtd_simulados:
        st.warning(f"🧪 {qtd_simulados} registro(s) são exemplos fictícios. Não representam ocorrências reais nem testes com cidadãos.")
    st.subheader("Filtros")
    filtro1, filtro2 = st.columns(2)
    categorias = sorted(set(r["categoria"] for r in registros))
    with filtro1:
        categoria = st.selectbox("Categoria do problema", options=["Todas"] + categorias)
    with filtro2:
        prioridades = st.multiselect("Prioridade", options=["alta", "media", "baixa"], default=["alta", "media", "baixa"], format_func=lambda p: {"alta":"Alta", "media":"Média", "baixa":"Baixa"}[p])
    filtrados = aplicar_filtros(registros, categoria, prioridades)
    contagens = contagem_prioridade(filtrados)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Registros exibidos", len(filtrados))
    m2.metric("🔴 Alta", contagens["alta"])
    m3.metric("🟠 Média", contagens["media"])
    m4.metric("🟢 Baixa", contagens["baixa"])
    aba1, aba2 = st.tabs(["📊 Visão por prioridade", "📋 Registros detalhados"])
    with aba1:
        if filtrados:
            fig = grafico_prioridades(filtrados)
            st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False, "scrollZoom": True})
            st.caption("Gráfico interativo: passe o mouse para ver a quantidade, use zoom e altere os filtros acima.")
        else:
            st.info("Nenhum registro corresponde aos filtros selecionados. Ajuste os filtros para visualizar os dados.")
    with aba2:
        if filtrados:
            tabela = pd.DataFrame(filtrados)[["id", "bairro", "categoria", "prioridade", "resumo", "origem", "revisao"]]
            tabela.columns = ["Código local", "Bairro", "Categoria", "Prioridade", "Resumo", "Origem", "Revisão humana"]
            st.dataframe(tabela, use_container_width=True, hide_index=True)
        else:
            st.info("Não há registros para os filtros atuais.")
    if st.button("Limpar histórico da sessão"):
        st.session_state["registros"] = []
        st.rerun()
