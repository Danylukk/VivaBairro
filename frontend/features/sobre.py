"""Transparência, limitações, ética em IA e impacto social (ODS) em linguagem acessível."""
import streamlit as st
from frontend.ui.components import cabecalho, dica_privacidade, aviso_institucional


def renderizar() -> None:
    cabecalho(
        "03 / Entenda a proposta",
        "Arquitetura, Ética e Impacto Social",
        "Conheça o funcionamento da Prova de Conceito VivaBairro, os fundamentos técnicos, "
        "as diretrizes éticas no uso de IA e o alinhamento com os Objetivos de Desenvolvimento Sustentável da ONU."
    )

    aba_func, aba_ods, aba_etica, aba_tecnica = st.tabs([
        "🏙️ Jornada do Cidadão",
        "🎯 ODS e Impacto Social",
        "⚖️ Ética e Limites da IA",
        "🛠️ Decisões Arquiteturais"
    ])

    with aba_func:
        st.subheader("Como o VivaBairro Funciona de Ponta a Ponta")
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True):
                st.markdown("#### 1. Entrada Cidadã")
                st.write("O cidadão informa bairro, categoria e relato livre com validações locais de tamanho e conteúdo.")
        with col2:
            with st.container(border=True):
                st.markdown("#### 2. Processamento por IA")
                st.write("O backend FastAPI orquestra a chamada ao modelo de linguagem com saída estruturada validada por Pydantic.")
        with col3:
            with st.container(border=True):
                st.markdown("#### 3. Revisão Humana")
                st.write("O cidadão confere, corrige a classificação e decide conscientemente se confirma o registro.")

        aviso_institucional()

    with aba_ods:
        st.subheader("Alinhamento aos Objetivos de Desenvolvimento Sustentável (ODS)")
        col_ods1, col_ods2 = st.columns(2)
        with col_ods1:
            with st.container(border=True):
                st.markdown("### 🏙️ ODS 11 — Cidades e Comunidades Sustentáveis")
                st.markdown("**Meta 11.7:** Proporcionar o acesso universal a espaços públicos seguros, inclusivos, acessíveis e verdes.")
                st.write("O VivaBairro contribui conceitualmente ao capacitar qualquer munícipe a relatar barreiras de acessibilidade em calçadas, "
                         "falhas em iluminação que geram insegurança e riscos de alagamento, promovendo espaços urbanos mais seguros e inclusivos.")
                st.caption("Referência: [ONU Brasil — ODS 11](https://brasil.un.org/pt-br/sdgs/11)")
        with col_ods2:
            with st.container(border=True):
                st.markdown("### 🏛️ ODS 16 — Paz, Justiça e Instituições Eficazes")
                st.markdown("**Meta 16.6:** Desenvolver instituições eficazes, responsáveis e transparentes em todos os níveis.")
                st.write("Ao estruturar relatos em categorias claras e orientar o cidadão com transparência, a solução estuda como a IA "
                         "pode aproximar o morador da governança urbana, sem intermediários opacos e com dados auditáveis.")
                st.caption("Referência: [ONU Brasil — ODS 16](https://brasil.un.org/pt-br/sdgs/16)")

    with aba_etica:
        st.subheader("Ética, Limites da IA e Mitigação de Riscos")
        with st.container(border=True):
            st.markdown("#### Principais Riscos Mapeados")
            st.markdown("""
            1. **Alucinação e invenção de protocolos:** O modelo pode gerar números falsos de protocolo ou telefones errados.
               - *Mitigação:* Prompt restritivo proibindo invenção de dados, validação de schema Pydantic e avisos claros de escopo.
            2. **Viés e má classificação de prioridade:** Rótulos automáticos podem subestimar ou superestimar a gravidade.
               - *Mitigação:* Arquitetura **Human-in-the-Loop** obrigatória: nenhuma decisão final é tomada sem confirmação do cidadão.
            3. **Tentativas de injeção de prompt:** Cidadãos podem colar textos maliciosos tentando burlar as regras.
               - *Mitigação:* Tratamento do relato como dado não-confiável e prompt de sistema blindado.
            4. **Vazamento de dados pessoais (LGPD):** Moradores podem incluir CPF, nome completo ou telefones no texto livre.
               - *Mitigação:* Orientações explícitas antes do envio, não persistência em banco compartilhado e escopo estrito à sessão local.
            """)
        dica_privacidade()

    with aba_tecnica:
        st.subheader("Por que Estas Tecnologias?")
        st.markdown("""
        - **Streamlit (Front-end):** Proporciona desenvolvimento ágil da interface interativa centrada no usuário, gerenciamento robusto de `st.session_state` e visualizações reativas com Plotly, respeitando o dimensionamento da POC.
        - **FastAPI (Back-end):** Separa responsabilidades, assegura tipagem com Pydantic em entrada e saída, protege credenciais e isola o acesso a provedores externos de IA.
        - **Saída Estruturada (Pydantic):** Elimina saídas em texto livre desordenado, garantindo que o front-end receba sempre campos previsíveis (`categoria`, `prioridade`, `orientacao`, `resumo`).
        - **Docker / Docker Compose:** Garante reprodutibilidade do ambiente tanto no front-end quanto na API com isolamento de dependências.
        """)

    st.divider()
    st.markdown("#### Canais Oficiais de Zeladoria em São Paulo")
    st.write("Para atendimento real e abertura de solicitações oficiais de zeladoria na cidade de São Paulo, utilize exclusivamente os canais municipais:")
    st.markdown("- **Portal SP156:** [sp156.prefeitura.sp.gov.br](https://sp156.prefeitura.sp.gov.br)")
    st.markdown("- **Telefone SP156:** Disque 156")
    st.markdown("- **Praças de Atendimento das Subprefeituras:** Presencialmente em cada região da cidade")
