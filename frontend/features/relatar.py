"""Jornada do cidadão: entrada -> API -> revisão -> registro de sessão."""
import streamlit as st
from frontend.providers.api import API_BASE_URL, obter_status, enviar_relato, ErroAmigavel
from frontend.state.store import registrar
from frontend.ui.components import cabecalho, faixa_prioridade, dica_privacidade
from frontend.constants import CATEGORIAS, PRIORIDADES


def renderizar() -> None:
    cabecalho("01 / Conte o que aconteceu", "Um bairro melhor começa com a sua voz", "Descreva um problema no espaço público. O sistema sugere uma orientação; **você confere e decide** o que registrar.")
    st.markdown('<div class="viva-step"><strong>Como funciona:</strong> 1. Conte o problema &nbsp; → &nbsp; 2. Receba uma sugestão &nbsp; → &nbsp; 3. Revise e confirme</div>', unsafe_allow_html=True)
    if st.session_state["mensagem_sucesso"]:
        st.success(st.session_state["mensagem_sucesso"])
        st.session_state["mensagem_sucesso"] = ""
    status = obter_status(API_BASE_URL)
    if status.get("status") != "ok":
        st.error("A análise automática está indisponível. Seus dados não foram enviados. Consulte as instruções para iniciar a API.")
    elif status.get("modo") == "demonstracao":
        st.info("🧪 Modo de demonstração: as respostas são simuladas por regras, não por um modelo de IA. Ative o provedor real para a avaliação da integração com LLM.")
    st.subheader("Descreva a situação")
    with st.form("form_relato", clear_on_submit=False):
        col1, col2 = st.columns([1, 1.15])
        with col1:
            bairro = st.text_input("Bairro ou região (obrigatório)", max_chars=60, placeholder="Ex.: Lapa", help="Informe apenas o bairro, sem o endereço exato")
        with col2:
            categoria = st.selectbox("Tipo de problema", options=CATEGORIAS, help="Escolha a opção mais próxima")
        descricao = st.text_area("O que aconteceu? (obrigatório)", max_chars=900, height=145, placeholder="Ex.: A calçada está com desnível e dificulta a passagem de pessoas com carrinho ou cadeira de rodas. O problema fica perto da praça do bairro.")
        st.caption("Use de 30 a 900 caracteres. Evite dados pessoais.")
        dica_privacidade()
        enviar = st.form_submit_button("Analisar meu relato", type="primary", use_container_width=True, disabled=status.get("status") != "ok")
    if enviar:
        if len(bairro.strip()) < 3 or not 30 <= len(descricao.strip()) <= 900:
            st.warning("Revise os campos: bairro com pelo menos 3 caracteres e relato de 30 a 900 caracteres.")
        else:
            entrada = {"bairro": bairro.strip(), "categoria_informada": categoria, "descricao": descricao.strip()}
            with st.spinner("Analisando seu relato. Isso pode levar alguns segundos..."):
                try:
                    resposta = enviar_relato(entrada)
                except ErroAmigavel as exc:
                    st.error(str(exc))
                else:
                    st.session_state["pendente"] = {"entrada": entrada, "resposta": resposta}
                    st.rerun()
    pendente = st.session_state.get("pendente")
    if pendente:
        resultado = pendente["resposta"]["resultado"]
        st.divider()
        st.subheader("Revise a sugestão antes de registrar")
        st.caption(pendente["resposta"]["aviso"])
        faixa_prioridade(resultado["prioridade"])
        st.write(f"**Resumo sugerido:** {resultado['resumo']}")
        st.write(f"**Por que esta prioridade?** {resultado['justificativa']}")
        st.write(f"**Orientação inicial:** {resultado['orientacao']}")
        st.write(f"**Tipo de serviço indicado:** {resultado['encaminhamento']}")
        if resultado["atencao_imediata"]:
            st.error("⚠️ Pode haver risco. Não se coloque em perigo; procure os canais oficiais de emergência se necessário.")
        with st.form("form_revisao"):
            categoria_final = st.selectbox("Categoria final (você pode corrigir)", options=CATEGORIAS, index=CATEGORIAS.index(resultado["categoria"]))
            prioridade_final = st.selectbox("Prioridade final (você pode corrigir)", options=PRIORIDADES, index=PRIORIDADES.index(resultado["prioridade"]), format_func=lambda p: {"alta":"Alta", "media":"Média", "baixa":"Baixa"}[p])
            resumo_final = st.text_area("Resumo final (você pode corrigir)", value=resultado["resumo"], height=90, max_chars=220)
            st.caption("Ao confirmar, o registro será guardado apenas na sessão atual. Não será enviado a serviços públicos.")
            confirmar = st.form_submit_button("Confirmar e registrar nesta sessão", type="primary", use_container_width=True)
        if confirmar:
            if len(resumo_final.strip()) < 12:
                st.warning("O resumo precisa ter pelo menos 12 caracteres.")
            else:
                final = {**resultado, "categoria": categoria_final, "prioridade": prioridade_final, "resumo": resumo_final.strip()}
                modificado = any(final[k] != resultado[k] for k in ("categoria", "prioridade", "resumo"))
                registro = registrar(pendente["entrada"], final, modificado, pendente["resposta"]["modo"])
                st.session_state["pendente"] = None
                st.session_state["mensagem_sucesso"] = f"Registro local {registro['id']} confirmado. Este código NÃO é protocolo oficial da Prefeitura."
                st.rerun()
        if st.button("Descartar esta sugestão", use_container_width=True):
            st.session_state["pendente"] = None
            st.rerun()
