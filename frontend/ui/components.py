"""Componentes reutilizados entre telas com diferentes parâmetros e alta acessibilidade."""
import streamlit as st


def cabecalho(etapa: str, titulo: str, descricao: str) -> None:
    """Componente de cabeçalho padronizado reutilizado em todas as telas."""
    st.markdown(f'<div class="viva-kicker" role="doc-subtitle">{etapa}</div>', unsafe_allow_html=True)
    st.title(titulo)
    st.markdown(f'<p class="viva-lead">{descricao}</p>', unsafe_allow_html=True)


def faixa_prioridade(prioridade: str, detalhe: str | None = None) -> None:
    """Faixa semântica de criticidade combinando cor + ícone + texto explícito (WCAG AA)."""
    mapa = {
        "alta": (st.error, "🔴 Prioridade Alta — Requer atenção urgente ou risco potencial"),
        "media": (st.warning, "🟠 Prioridade Média — Acompanhar e planejar intervenção"),
        "baixa": (st.success, "🟢 Prioridade Baixa — Manutenção preventiva ou rotina"),
    }
    funcao, texto_base = mapa.get(prioridade, (st.info, "⚪ Classificação a ser revisada"))
    texto = f"{texto_base} · {detalhe}" if detalhe else texto_base
    funcao(texto, icon=None)


def card_metrica(rotulo: str, valor: str | int, subtitulo: str = "", icone: str = "📌", variante: str = "default") -> None:
    """Card reutilizável de métrica visual para painel e confirmação."""
    borda_cor = {
        "alta": "#b91c1c",
        "media": "#b45309",
        "baixa": "#15803d",
        "primario": "#0f766e",
        "default": "#cbd5e1",
    }.get(variante, "#cbd5e1")
    
    st.markdown(
        f"""
        <div style="background:#ffffff; border:1px solid {borda_cor}; border-left:5px solid {borda_cor}; border-radius:10px; padding:14px 18px; margin-bottom:10px; box-shadow:0 1px 3px rgba(0,0,0,0.06);">
            <div style="font-size:0.85rem; color:#475569; font-weight:600; text-transform:uppercase; letter-spacing:0.04em;">
                {icone} {rotulo}
            </div>
            <div style="font-size:1.85rem; font-weight:800; color:#0f172a; margin:4px 0 2px 0;">
                {valor}
            </div>
            {"<div style='font-size:0.82rem; color:#64748b;'>" + subtitulo + "</div>" if subtitulo else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )


def dica_privacidade() -> None:
    """Aviso padronizado de proteção de dados pessoais (LGPD)."""
    st.markdown(
        """
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:10px 14px; margin:10px 0; font-size:0.85rem; color:#334155;">
            🔒 <strong>Privacidade e LGPD:</strong> Não informe nome completo, CPF, telefone, endereço residencial exato ou dados sensíveis. Os relatos são processados como demonstração acadêmica e armazenados apenas na sua sessão atual.
        </div>
        """,
        unsafe_allow_html=True,
    )


def aviso_institucional() -> None:
    """Aviso de escopo acadêmico para evitar confusão com canal oficial."""
    st.markdown(
        """
        <div style="background:#fefce8; border:1px solid #fef08a; border-left:4px solid #ca8a04; border-radius:6px; padding:10px 14px; margin:12px 0; font-size:0.85rem; color:#854d0e;">
            🏛️ <strong>Aviso acadêmico:</strong> O VivaBairro é uma Prova de Conceito (POC) acadêmica FIAP. Ele <strong>NÃO</strong> envia solicitações à Prefeitura de São Paulo nem substitui o canal oficial <strong>SP156</strong>.
        </div>
        """,
        unsafe_allow_html=True,
    )
