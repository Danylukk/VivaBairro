"""Tema visual da prova de conceito VivaBairro.
Projetado segundo diretrizes WCAG 2.2 AA (contraste >= 4.5:1, foco visível e responsividade).
"""
import streamlit as st


def aplicar_tema() -> None:
    st.markdown("""<style>
    :root {
        --viva-ink: #0f172a;
        --viva-muted: #475569;
        --viva-primary: #0f766e;
        --viva-primary-hover: #115e59;
        --viva-bg-card: #ffffff;
        --viva-border: #e2e8f0;
    }
    
    .block-container {
        max-width: 1160px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }
    
    html, body, [class*="st-"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #0f172a;
    }
    
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 750;
        letter-spacing: -0.02em;
    }
    
    h1 {
        font-size: 2.15rem;
        line-height: 1.2;
    }
    
    /* Indicador de Foco Visível para Navegação por Teclado (WCAG 2.2 AA) */
    *:focus-visible {
        outline: 3px solid #0f766e !important;
        outline-offset: 2px !important;
    }
    
    .viva-kicker {
        color: #0f766e;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.78rem;
        font-weight: 800;
        margin-bottom: 4px;
    }
    
    .viva-lead {
        color: #334155;
        font-size: 1.05rem;
        line-height: 1.6;
        margin-bottom: 1.25rem;
    }
    
    .viva-step {
        background: #f0fdfa;
        border: 1px solid #ccfbf1;
        border-left: 4px solid #0f766e;
        padding: 12px 16px;
        border-radius: 8px;
        color: #134e4a;
        margin: 12px 0 20px 0;
        font-size: 0.93rem;
    }
    
    [data-testid="stSidebar"] {
        background: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Botões primários com alto contraste e semântica de acessibilidade */
    div.stButton>button[kind="primary"], div.stFormSubmitButton>button[kind="primary"] {
        background-color: #0f766e !important;
        color: #ffffff !important;
        border-color: #0f766e !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        min-height: 44px !important;
    }
    
    div.stButton>button[kind="primary"]:hover, div.stFormSubmitButton>button[kind="primary"]:hover {
        background-color: #115e59 !important;
        border-color: #115e59 !important;
        color: #ffffff !important;
    }
    
    /* Ajustes para telas menores (mobile / tablet) */
    @media (max-width: 640px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
        }
        h1 {
            font-size: 1.7rem;
        }
        .viva-lead {
            font-size: 0.95rem;
        }
    }
    
    .viva-footnote {
        color: #64748b;
        font-size: 0.82rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
    }
    </style>""", unsafe_allow_html=True)
