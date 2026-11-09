"""Tema visual da prova de conceito VivaBairro.
Projetado segundo diretrizes WCAG 2.2 AA (contraste >= 4.5:1, foco visível,
ícones Material Symbols preservados e responsividade para 390px, 768px e 1440px).
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
    
    html, body, .stApp {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #0f172a;
        overflow-x: hidden !important;
    }
    
    .block-container {
        max-width: 1160px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        overflow-x: hidden !important;
        box-sizing: border-box;
    }
    
    /* Preservação estrita dos ícones do Streamlit (Material Symbols) */
    [data-testid="stIconMaterial"],
    [data-testid*="stIcon"],
    .material-symbols-rounded,
    [class*="material-symbols"] {
        font-family: "Material Symbols Rounded", "Material Icons", sans-serif !important;
        font-weight: normal !important;
        font-style: normal !important;
        font-size: 1.35rem !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-block !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-smoothing: antialiased !important;
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
    
    /* Botões primários com alto contraste (Verde Petróleo WCAG AA, ratio > 4.5:1) */
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
    
    /* Botões secundários e de descarte: neutros, nunca vermelhos alarmantes */
    div.stButton>button[kind="secondary"], div.stButton>button:not([kind="primary"]) {
        background-color: #f8fafc !important;
        color: #334155 !important;
        border: 1px solid #cbd5e1 !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        min-height: 44px !important;
    }
    
    div.stButton>button[kind="secondary"]:hover, div.stButton>button:not([kind="primary"]):hover {
        background-color: #f1f5f9 !important;
        border-color: #94a3b8 !important;
        color: #0f172a !important;
    }
    
    /* Expander sem sobreposição de texto ou caracteres indevidos */
    [data-testid="stExpander"] {
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        background-color: #ffffff !important;
        margin-top: 0.75rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
        overflow: hidden !important;
    }
    
    [data-testid="stExpander"] summary {
        padding: 0.75rem 1rem !important;
        font-weight: 600 !important;
        color: #1e293b !important;
        cursor: pointer !important;
    }

    [data-testid="stExpander"] summary:hover {
        background-color: #f8fafc !important;
        color: #0f766e !important;
    }
    
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        padding: 0.75rem 1rem 1rem 1rem !important;
        border-top: 1px solid #f1f5f9 !important;
        background-color: #f8fafc !important;
    }
    
    /* Ajustes de responsividade para tablet e mobile */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            padding-top: 1rem !important;
        }
        h1 {
            font-size: 1.65rem !important;
        }
        .viva-lead {
            font-size: 0.95rem !important;
        }
        .viva-step {
            font-size: 0.82rem !important;
            padding: 10px 12px !important;
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
