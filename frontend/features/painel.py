"""Painel interativo com filtros dinâmicos, múltiplos gráficos Plotly e dados da sessão."""
import pandas as pd
import streamlit as st
from frontend.demo_data import exemplos_ficticios
from frontend.ui.components import cabecalho, card_metrica, aviso_institucional
from frontend.visualization import aplicar_filtros, contagem_prioridade, grafico_prioridades, grafico_categorias


def renderizar() -> None:
    cabecalho(
        "02 / Acompanhe as informações",
        "Painel Interativo de Relatos",
        "Visualize estatísticas agregadas dos relatos registrados nesta sessão do navegador. "
        "Use os filtros interativos para segmentar por categoria, prioridade ou tipo de dado."
    )

    registros = st.session_state.get("registros", [])

    if not registros:
        st.info("ℹ️ Ainda não há relatos confirmados nesta sessão. "
                "Você pode fazer o seu primeiro relato na aba **'Fazer relato'** ou carregar exemplos ilustrativos para testar os gráficos.",
                icon="💡")
        col_c1, _ = st.columns([1, 2])
        with col_c1:
            if st.button("📥 Carregar 6 exemplos fictícios para demonstração", type="primary", use_container_width=True):
                st.session_state["registros"] = exemplos_ficticios()
                st.rerun()
        aviso_institucional()
        return

    qtd_simulados = sum(r.get("origem") == "Exemplo fictício" for r in registros)
    qtd_reais = len(registros) - qtd_simulados
    if qtd_simulados > 0 and qtd_reais == 0:
        st.warning(
            f"🧪 **Atenção (Modo Demonstração):** O painel exibe {qtd_simulados} registro(s) gerado(s) por regras locais de teste ou exemplos ilustrativos. "
            "Esses dados servem para demonstrar o funcionamento dos gráficos e filtros.",
            icon="⚠️"
        )
    elif qtd_simulados > 0 and qtd_reais > 0:
        st.info(
            f"📊 O painel contém **{qtd_reais} relato(s) com análise de IA** e **{qtd_simulados} exemplo(s) ilustrativo(s)**. "
            "Use o filtro 'Tipo de Relato' para isolá-los.",
            icon="ℹ️"
        )

    # 3 FILTROS INTERATIVOS (requisito exige pelo menos 2)
    st.subheader("🔍 Filtros Interativos")
    f_col1, f_col2, f_col3 = st.columns([1.2, 1.2, 1])

    categorias_disponiveis = sorted(list(set(r.get("categoria", "") for r in registros if r.get("categoria"))))
    with f_col1:
        categoria_sel = st.selectbox(
            "Filtrar por Categoria",
            options=["Todas"] + categorias_disponiveis,
            help="Selecione uma categoria específica ou 'Todas'."
        )

    with f_col2:
        prioridades_sel = st.multiselect(
            "Filtrar por Prioridade",
            options=["alta", "media", "baixa"],
            default=["alta", "media", "baixa"],
            format_func=lambda p: {"alta": "🔴 Alta", "media": "🟠 Média", "baixa": "🟢 Baixa"}[p],
            help="Marque ou desmarque níveis de criticidade."
        )

    with f_col3:
        origens_disponiveis = ["Todas", "Apenas análises de IA", "Apenas exemplos fictícios"]
        origem_opcao = st.selectbox(
            "Tipo de Relato",
            options=origens_disponiveis,
            help="Separe relatos desta sessão dos dados de exemplo."
        )
        origem_filtro = {
            "Todas": "Todas",
            "Apenas análises de IA": "Análise de LLM revisada",
            "Apenas exemplos fictícios": "Exemplo fictício",
        }.get(origem_opcao, "Todas")

    filtrados = aplicar_filtros(
        registros,
        categoria=categoria_sel,
        prioridades=prioridades_sel,
        origem=origem_filtro
    )
    contagens = contagem_prioridade(filtrados)

    # CARDS DE MÉTRICAS REUTILIZANDO O COMPONENTE card_metrica
    st.markdown("#### Indicadores Selecionados")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        card_metrica("Total Selecionado", len(filtrados), f"de {len(registros)} na sessão", "📊", "primario")
    with m2:
        card_metrica("Prioridade Alta", contagens["alta"], "Atenção prioritária", "🔴", "alta")
    with m3:
        card_metrica("Prioridade Média", contagens["media"], "Acompanhar", "🟠", "media")
    with m4:
        card_metrica("Prioridade Baixa", contagens["baixa"], "Rotina preventiva", "🟢", "baixa")

    # ABAS DE VISUALIZAÇÃO COM PLOTLY E TABELA
    aba_graf1, aba_graf2, aba_tabela = st.tabs([
        "📊 Distribuição por Prioridade (Plotly)",
        "📈 Relatos por Categoria (Plotly)",
        "📋 Tabela Completa de Registros"
    ])

    with aba_graf1:
        if filtrados:
            fig_prio = grafico_prioridades(filtrados)
            st.plotly_chart(fig_prio, use_container_width=True, config={"displaylogo": False, "scrollZoom": True})
            st.caption("🔍 **Interatividade:** Passe o mouse para detalhes (hover), clique duas vezes para resetar o zoom ou use a barra de ferramentas do gráfico.")
        else:
            st.info("Nenhum registro corresponde aos filtros selecionados. Tente ajustar os filtros acima.")

    with aba_graf2:
        if filtrados:
            fig_cat = grafico_categorias(filtrados)
            st.plotly_chart(fig_cat, use_container_width=True, config={"displaylogo": False, "scrollZoom": True})
            st.caption("🔍 **Interatividade:** Gráfico horizontal por tipo de problema urbano com suporte a zoom e hover.")
        else:
            st.info("Nenhum registro corresponde aos filtros selecionados. Tente ajustar os filtros acima.")

    with aba_tabela:
        if filtrados:
            df = pd.DataFrame(filtrados)[["id", "quando", "bairro", "categoria", "prioridade", "resumo", "revisao", "origem"]]
            df.columns = ["Código Local", "Data/Hora", "Bairro", "Categoria", "Prioridade", "Resumo", "Revisão Humana", "Origem"]
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption("🔒 Dados armazenados temporariamente na memória da sessão atual.")
        else:
            st.info("Nenhum registro a exibir com os filtros atuais.")

    aviso_institucional()
