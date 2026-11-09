"""Jornada do cidadão: entrada -> API -> revisão com IA -> human-in-the-loop -> registro de sessão."""
import streamlit as st
from frontend.providers.api import API_BASE_URL, obter_status, enviar_relato, ErroAmigavel
from frontend.state.store import registrar
from frontend.ui.components import cabecalho, faixa_prioridade, dica_privacidade, aviso_institucional, card_metrica
from frontend.constants import CATEGORIAS, PRIORIDADES


def renderizar() -> None:
    cabecalho(
        "01 / Conte o que aconteceu",
        "VivaBairro — Sua Voz na Cidade",
        "Descreva um problema de zeladoria no espaço público. A inteligência artificial analisa a situação, "
        "propõe uma classificação e orientação, e <strong>você sempre confere e decide</strong> o que registrar."
    )

    status = obter_status(API_BASE_URL)
    if status.get("status") != "ok":
        st.error("⚠️ O serviço de análise automática está temporariamente indisponível. Nenhum dado foi enviado. "
                 "Verifique se o backend FastAPI está em execução.")
    elif status.get("modo") == "demonstracao":
        st.info("🧪 **Modo de demonstração simulada ativo:** As análises são geradas por regras ilustrativas locais, "
                "sem consumo de LLM externo. Para avaliação da IA real, configure `LLM_PROVIDER=openai` com sua chave no arquivo `.env`.")

    # Feedback de registro recém-confirmado
    if st.session_state.get("ultimo_registro"):
        rec = st.session_state["ultimo_registro"]
        st.success(f"✅ **Registro local concluído com sucesso!** Código local gerado: `{rec['id']}`")
        with st.container(border=True):
            col_a, col_b = st.columns([2, 1])
            with col_a:
                st.markdown(f"**Bairro:** {rec['bairro']} · **Categoria:** {rec['categoria']}")
                st.markdown(f"**Resumo confirmado:** {rec['resumo']}")
                st.caption(f"Status da revisão humana: *{rec['revisao']}* · Avaliação da IA: *{rec.get('avaliacao_ia', 'Útil')}*")
            with col_b:
                card_metrica("Código Local", rec["id"], "Apenas nesta sessão", "🏷️", "primario")
        
        aviso_institucional()
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("📊 Ver no Painel de Relatos", type="primary", use_container_width=True):
                st.session_state["redirecionar_pagina"] = "Painel de relatos"
                st.session_state["ultimo_registro"] = None
                st.rerun()
        with col_btn2:
            if st.button("➕ Fazer outro relato", use_container_width=True):
                st.session_state["ultimo_registro"] = None
                st.session_state["mensagem_sucesso"] = ""
                st.rerun()
        return

    pendente = st.session_state.get("pendente")

    # CASO 1: Há uma análise de IA pendente para Revisão Humana (Human-in-the-Loop)
    if pendente:
        st.markdown(
            '<div class="viva-step"><strong>Etapa atual:</strong> 1. Relatar (✓) &nbsp; → &nbsp; '
            '<strong>2. Revisão Humana da Sugestão da IA (Agora)</strong> &nbsp; → &nbsp; 3. Registro Local</div>',
            unsafe_allow_html=True
        )

        resultado = pendente["resposta"]["resultado"]
        entrada = pendente["entrada"]

        st.subheader("🔍 Sugestão da Inteligência Artificial")
        st.caption(f"🤖 {pendente['resposta']['aviso']}")

        # Exibição da prioridade com semântica e acessibilidade visual
        faixa_prioridade(resultado["prioridade"])

        if resultado.get("atencao_imediata"):
            st.error("⚠️ **Atenção Imediata Identificada:** O relato indica possível risco à integridade física. "
                     "Não se coloque em perigo e, se necessário, procure os canais oficiais de socorro e emergência.")

        with st.expander("📄 Ver relato original enviado pelo cidadão", expanded=False):
            st.markdown(f"**Bairro informado:** {entrada['bairro']}")
            st.markdown(f"**Categoria preliminar:** {entrada['categoria_informada']}")
            st.markdown(f"**Descrição original:** {entrada['descricao']}")

        col_ia1, col_ia2 = st.columns(2)
        with col_ia1:
            with st.container(border=True):
                st.markdown("##### 📌 Resumo e Justificativa da IA")
                st.write(f"**Resumo sugerido:** {resultado['resumo']}")
                st.write(f"**Por que esta prioridade?** {resultado['justificativa']}")
        with col_ia2:
            with st.container(border=True):
                st.markdown("##### 💡 Orientação e Encaminhamento Sugerido")
                st.write(f"**Orientação ao cidadão:** {resultado['orientacao']}")
                st.write(f"**Tipo genérico de serviço:** {resultado['encaminhamento']}")

        st.divider()
        st.subheader("✍️ Sua Decisão Humana (Human-in-the-Loop)")
        st.markdown("A inteligência artificial pode cometer erros ou alucinações. Você tem total controle para "
                    "corrigir as classificações antes de confirmar.")

        with st.form("form_revisao"):
            col_rev1, col_rev2 = st.columns(2)
            with col_rev1:
                categoria_final = st.selectbox(
                    "Categoria do problema (você pode alterar)",
                    options=CATEGORIAS,
                    index=CATEGORIAS.index(resultado["categoria"]) if resultado["categoria"] in CATEGORIAS else 0,
                    help="Corrija se a IA classificou a categoria de forma imprecisa."
                )
            with col_rev2:
                prioridade_final = st.selectbox(
                    "Nível de prioridade (você pode alterar)",
                    options=PRIORIDADES,
                    index=PRIORIDADES.index(resultado["prioridade"]) if resultado["prioridade"] in PRIORIDADES else 1,
                    format_func=lambda p: {"alta": "🔴 Alta — Atenção urgente", "media": "🟠 Média — Acompanhar", "baixa": "🟢 Baixa — Rotina"}[p],
                    help="Ajuste a prioridade com base na sua percepção real do local."
                )

            resumo_final = st.text_area(
                "Resumo final do relato (você pode editar o texto)",
                value=resultado["resumo"],
                height=90,
                max_chars=220,
                help="Ajuste o resumo para deixá-lo claro e fidedigno ao problema."
            )

            avaliacao_ia = st.radio(
                "Avaliação da sugestão gerada pela IA:",
                options=["Sim, adequada", "Parcialmente adequada", "Incorreta / Ajustei manualmente"],
                horizontal=True,
                help="Esse feedback ajuda a calibrar a eficácia do modelo."
            )

            st.caption("🔒 Ao confirmar, o relato será salvo exclusivamente na sessão deste navegador para consulta e gráficos.")
            confirmar = st.form_submit_button("✅ Confirmar e Registrar nesta Sessão", type="primary", use_container_width=True)

        if confirmar:
            if len(resumo_final.strip()) < 12:
                st.warning("O resumo precisa ter pelo menos 12 caracteres.")
            else:
                final = {
                    **resultado,
                    "categoria": categoria_final,
                    "prioridade": prioridade_final,
                    "resumo": resumo_final.strip()
                }
                modificado = any(final[k] != resultado[k] for k in ("categoria", "prioridade", "resumo"))
                registro = registrar(
                    entrada=pendente["entrada"],
                    resultado=final,
                    corrigido=modificado,
                    modo=pendente["resposta"]["modo"],
                    avaliacao_ia=avaliacao_ia
                )
                st.session_state["pendente"] = None
                st.rerun()

        if st.button("🗑️ Descartar esta sugestão e recomeçar", use_container_width=True):
            st.session_state["pendente"] = None
            st.rerun()

    # CASO 2: Formulário para novo relato
    else:
        st.markdown(
            '<div class="viva-step"><strong>Etapa 1:</strong> Preencha os dados do problema &nbsp; → &nbsp; '
            '<strong>Etapa 2:</strong> Receba a análise da IA &nbsp; → &nbsp; '
            '<strong>Etapa 3:</strong> Revise, corrija e confirme</div>',
            unsafe_allow_html=True
        )

        st.subheader("Descreva a situação do seu bairro")
        with st.form("form_relato", clear_on_submit=False):
            col1, col2 = st.columns([1, 1.2])
            with col1:
                bairro = st.text_input(
                    "Bairro ou região (obrigatório)",
                    max_chars=60,
                    placeholder="Ex.: Lapa, Pinheiros, Centro...",
                    help="Informe apenas o nome do bairro ou praça conhecida."
                )
            with col2:
                categoria = st.selectbox(
                    "Tipo de problema (categoria preliminar)",
                    options=CATEGORIAS,
                    help="Selecione o tipo de zeladoria mais condizente."
                )

            descricao = st.text_area(
                "O que aconteceu? (obrigatório — de 30 a 900 caracteres)",
                max_chars=900,
                height=150,
                placeholder="Exemplo: A calçada em frente à praça principal está com desníveis acentuados e buracos "
                            "que impedem a passagem segura de carrinhos e pessoas em cadeira de rodas.",
                help="Descreva objetivamente o obstáculo ou dano observado."
            )

            dica_privacidade()

            enviar = st.form_submit_button(
                "🔍 Analisar meu relato com IA",
                type="primary",
                use_container_width=True,
                disabled=status.get("status") != "ok"
            )

        if enviar:
            bairro_limpo = bairro.strip()
            desc_limpa = descricao.strip()
            if len(bairro_limpo) < 3:
                st.warning("⚠️ O campo 'Bairro' deve ter pelo menos 3 caracteres.")
            elif not (30 <= len(desc_limpa) <= 900):
                st.warning(f"⚠️ A descrição deve ter entre 30 e 900 caracteres. Seu texto tem {len(desc_limpa)} caracteres.")
            else:
                entrada = {
                    "bairro": bairro_limpo,
                    "categoria_informada": categoria,
                    "descricao": desc_limpa,
                }
                with st.spinner("⏳ Analisando seu relato com inteligência artificial... Aguarde alguns instantes."):
                    try:
                        resposta = enviar_relato(entrada)
                    except ErroAmigavel as exc:
                        st.error(f"❌ {str(exc)}")
                    else:
                        st.session_state["pendente"] = {"entrada": entrada, "resposta": resposta}
                        st.rerun()

    aviso_institucional()
