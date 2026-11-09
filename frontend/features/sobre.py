"""Transparência, limitações e impacto social em linguagem acessível."""
import streamlit as st
from frontend.ui.components import cabecalho, dica_privacidade


def renderizar() -> None:
    cabecalho("03 / Entenda a proposta", "Como o VivaBairro funciona", "Uma prova de conceito acadêmica para ajudar as pessoas a organizar relatos de problemas no espaço público.")
    with st.container(border=True):
        st.markdown("#### 1. Você conta o problema")
        st.write("Informe o bairro, selecione a categoria e descreva a situação sem incluir dados pessoais.")
    with st.container(border=True):
        st.markdown("#### 2. O serviço analisa")
        st.write("O front-end envia o texto a uma API. Quando o provedor real está configurado, a API usa um modelo de linguagem para propor prioridade, resumo e orientação.")
    with st.container(border=True):
        st.markdown("#### 3. Você decide")
        st.write("A classificação pode estar errada. Antes de registrar o relato nesta sessão, você pode corrigir categoria, prioridade e resumo, ou descartar tudo.")
    st.subheader("O que este projeto NÃO faz")
    st.warning("Não envia ocorrências à Prefeitura, não fornece protocolos oficiais, não substitui serviços de emergência, não garante precisão da análise e não armazena dados em banco.")
    dica_privacidade()
    st.subheader("Impacto social esperado")
    st.write("A proposta está relacionada à **ODS 11 — Cidades e comunidades sustentáveis**, ao facilitar a identificação de problemas nos espaços urbanos, e à **ODS 16 — Instituições eficazes**, ao explorar formas de organizar informações úteis ao atendimento público. Isso é benefício potencial, não impacto já comprovado.")
    st.markdown("Fontes: [ONU — ODS 11](https://brasil.un.org/pt-br/sdgs/11) · [ONU — ODS 16](https://brasil.un.org/pt-br/sdgs/16)")
