"""Tema visual da prova de conceito. Contraste e estados semânticos legíveis."""
import streamlit as st


def aplicar_tema() -> None:
    st.markdown("""
    <style>
    :root { --viva-ink:#10283f; --viva-muted:#4c6070; --viva-primary:#086a69; }
    .block-container { max-width: 1100px; padding-top: 1.8rem; padding-bottom: 3rem; }
    html, body, [class*="st-"] { font-family: system-ui,-apple-system,Segoe UI,sans-serif; }
    h1, h2, h3 { color: #10283f; letter-spacing: -.015em; }
    h1 { font-size: 2.15rem; }
    .viva-kicker { color:#086a69; text-transform: uppercase; letter-spacing:.12em; font-size:.73rem; font-weight:750; }
    .viva-title { font-size:2rem; font-weight:790; line-height:1.14; letter-spacing:-.025em; color:#10283f; }
    .viva-lead { color:#415568; font-size:1.05rem; line-height:1.6; max-width:700px; }
    .viva-step { background:#f0f7f6; border-left:4px solid #086a69; padding:13px 16px; border-radius:6px; color:#153e3e; margin: 14px 0 22px; }
    [data-testid="stSidebar"] { background:#f3f8f8; }
    [data-testid="stMetric"] { background:#f4f7f8; border:1px solid #e0e9ed; border-radius:12px; padding:16px; }
    .viva-footnote { color:#4c6070; font-size:.83rem; margin-top:24px; }
    div.stButton>button[kind="primary"], div.stFormSubmitButton>button[kind="primary"] { background:#086a69; color:white; border-color:#086a69; }
    div.stButton>button[kind="primary"]:hover, div.stFormSubmitButton>button[kind="primary"]:hover { background:#075656; border-color:#075656; }
    </style>
    """, unsafe_allow_html=True)
