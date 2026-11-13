"""Jornada do cidadão: entrada -> API -> revisão assistida -> human-in-the-loop -> registro de sessão."""
import streamlit as st
from frontend.providers.api import API_BASE_URL, obter_status, enviar_relato, ErroAmigavel
from frontend.state.store import registrar
from frontend.ui.components import cabecalho, faixa_prioridade, dica_privacidade, aviso_institucional, card_metrica
from frontend.constants import CATEGORIAS, PRIORIDADES


def renderizar() -> None:
    cabecalho(
        "01 / Conte o que aconteceu",
        "VivaBairro — Sua Voz na Cidade",
        "Descreva um problema de zeladoria urbana. O assistente analisa a situação, "
        "propõe uma classificação e orientação preliminares, e <strong>você sempre confere e decide</strong> o que registrar."
    )

    status = obter_status(API_BASE_URL)
    if status.get("status") != "ok":
        st.warning("⚠️ **Aviso de Conexão:** O serviço de análise assistida está temporariamente indisponível. "
                   "Tente novamente em alguns instantes.")
    elif (status.get("modo") == "demonstracao"
          and not st.session_state.get("pendente")
          and not st.session_state.get("ultimo_registro")):
        st.info("ℹ️ **Modo de Demonstração Acadêmica:** Esta análise prévia é uma simulação para fins de teste da interface "
                "e não substitui o atendimento dos canais oficiais da Prefeitura.")

    # Feedback de registro recém-confirmado (Etapa 3 concluída)
    if st.session_state.get("ultimo_registro"):
        rec = st.session_state["ultimo_registro"]
        st.success(f"✅ **Registro local concluído com sucesso!** Código local gerado: `{rec['id']}`")
        st.info("ℹ️ **Este código é somente um comprovante temporário do VivaBairro.** "
                "**Não é protocolo oficial da Prefeitura.** Para solicitar atendimento real, utilize o SP156.")
        with st.container(border=True):
            col_a, col_b = st.columns([2, 1])
            with col_a:
                st.markdown(f"**Bairro:** {rec['bairro']} · **Categoria:** {rec['categoria']}")
                st.markdown(f"**Resumo confirmado:** {rec['resumo']}")
                st.caption(f"Revisão humana: *{rec['revisao']}* · Avaliação da sugestão: *{rec.get('avaliacao_ia', 'Sim, adequada')}*")
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

    # CASO 1: Há uma análise pendente para Revisão Humana (Human-in-the-Loop)
    if pendente:
        st.markdown(
            '<div class="viva-step"><strong>Etapa 1:</strong> Relatar (✓) &nbsp; → &nbsp; '
            '<strong>Etapa 2: Revisão Humana da Sugestão (Agora)</strong> &nbsp; → &nbsp; '
            '<strong>Etapa 3:</strong> Confirmação e Recibo</div>',
            unsafe_allow_html=True
        )

        resultado = pendente["resposta"]["resultado"]
        entrada = pendente["entrada"]
        eh_simulado = pendente["resposta"]["modo"] == "demonstracao"

        if eh_simulado:
            st.subheader("📋 Sugestão do Assistente (Modo Demonstração)")
            st.caption("🧪 Esta análise foi calculada por regras de teste da interface. Não é resposta de inteligência artificial.")
        else:
            st.subheader("🔍 Sugestão do Assistente Inteligente")
            st.caption("🤖 Análise processada por inteligência artificial para apoio ao cidadão. Confira e ajuste os dados abaixo.")

        # Exibição da prioridade com semântica e acessibilidade visual
        faixa_prioridade(resultado["prioridade"])

        if resultado.get("atencao_imediata"):
            st.error("⚠️ **Atenção Imediata Identificada:** O relato indica possível risco à integridade física. "
                     "Não se coloque em perigo e, se necessário, procure os canais oficiais de socorro e emergência.")

        # Exibir apenas a ação principal; detalhes técnicos ficam disponíveis sob demanda.
        # A prioridade e os avisos de risco permanecem visíveis mesmo com o expansor fechado.
        with st.container(border=True):
            st.markdown(f"**💡 Orientação preliminar:** {resultado['orientacao']}")

        with st.expander("Ver justificativa e informações adicionais", expanded=False):
            st.markdown(f"**Por que esta prioridade?** {resultado['justificativa']}")
            st.markdown(f"**Serviço sugerido:** {resultado['encaminhamento']}")
            st.markdown(f"**Resumo sugerido:** {resultado['resumo']}")
            st.divider()
            st.markdown("**Relato original**")
            st.markdown(f"**Bairro informado:** {entrada['bairro']}")
            st.markdown(f"**Categoria preliminar:** {entrada['categoria_informada']}")
            st.markdown(f"**Descrição original:** {entrada['descricao']}")

        st.subheader("✍️ Sua Decisão Humana")
        st.caption("Confira a sugestão. Se necessário, altere a categoria, a prioridade e o resumo antes de confirmar.")

        with st.form("form_revisao"):
            col_rev1, col_rev2 = st.columns(2)
            with col_rev1:
                categoria_final = st.selectbox(
                    "Categoria do problema (você pode alterar)",
                    options=CATEGORIAS,
                    index=CATEGORIAS.index(resultado["categoria"]) if resultado["categoria"] in CATEGORIAS else 0,
                    help="Corrija se a sugestão classificou a categoria de forma imprecisa."
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
                "A sugestão apresentada foi adequada para o seu caso?",
                options=["Sim, adequada", "Parcialmente adequada", "Não, precisei corrigir"],
                horizontal=True,
                help="Esse retorno ajuda a avaliar a clareza da proposta."
            )

            st.info("ℹ️ **Registro temporário:** salvo apenas nesta sessão; não é enviado à Prefeitura "
                    "nem gera protocolo oficial.")
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

        if st.button("↩️ Descartar sugestão e voltar", use_container_width=True):
            st.session_state["pendente"] = None
            st.rerun()

    # CASO 2: Formulário para novo relato (Etapa 1)
    else:
        st.markdown(
            '<div class="viva-step"><strong>Etapa 1:</strong> Preencha os dados do problema &nbsp; → &nbsp; '
            '<strong>Etapa 2:</strong> Revise a sugestão &nbsp; → &nbsp; '
            '<strong>Etapa 3:</strong> Confirme o registro</div>',
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
                    help="Informe o bairro ou região (pode ter apenas duas letras, como Sé). Não inclua endereço residencial."
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
                placeholder="Exemplo: A calçada em frente à praça principal está com desníveis acentuados e blocos "
                            "quebrados que impedem a passagem segura de carrinhos e pessoas em cadeira de rodas.",
                help="Descreva objetivamente o obstáculo ou dano observado."
            )

            dica_privacidade()

            enviar = st.form_submit_button(
                "🔍 Analisar meu relato",
                type="primary",
                use_container_width=True,
                disabled=status.get("status") != "ok"
            )

        if enviar:
            bairro_limpo = bairro.strip()
            desc_limpa = descricao.strip()
            if len(bairro_limpo) < 2:
                st.warning("⚠️ Informe o nome do bairro com pelo menos 2 caracteres (ex.: Sé).")
            elif not (30 <= len(desc_limpa) <= 900):
                st.warning(f"⚠️ A descrição deve ter entre 30 e 900 caracteres. Seu texto tem {len(desc_limpa)} caracteres.")
            else:
                entrada = {
                    "bairro": bairro_limpo,
                    "categoria_informada": categoria,
                    "descricao": desc_limpa,
                }
                with st.spinner("⏳ Analisando seu relato com o assistente... Aguarde alguns instantes."):
                    try:
                        resposta = enviar_relato(entrada)
                    except ErroAmigavel as exc:
                        st.error(f"❌ {str(exc)}")
                    else:
                        st.session_state["pendente"] = {"entrada": entrada, "resposta": resposta}
                        st.rerun()

    # Na revisão o aviso oficial já aparece próximo ao botão; evitar repetição visual.
    if not pendente:
        aviso_institucional()
