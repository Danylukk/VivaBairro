"""Transformações e construção Plotly independentes do Streamlit.
Gráficos interativos com hover, zoom e alta acessibilidade visual.
"""
from collections import Counter
import plotly.graph_objects as go

# Cores semânticas com contraste aprovado WCAG 2.2 AA (> 4.5:1 contra fundos claros)
COR = {
    "alta": "#b91c1c",    # Vermelho escuro acessível
    "media": "#b45309",   # Âmbar quente acessível
    "baixa": "#15803d",   # Verde escuro acessível
    "primario": "#0f766e" # Verde-azulado VivaBairro
}


def aplicar_filtros(
    registros: list[dict],
    categoria: str = "Todas",
    prioridades: list[str] | None = None,
    origem: str = "Todas",
    bairro: str = "Todos",
) -> list[dict]:
    """Filtra registros por múltiplos critérios independentes."""
    if prioridades is None:
        prioridades = ["alta", "media", "baixa"]

    filtrados = []
    for r in registros:
        if categoria != "Todas" and r.get("categoria") != categoria:
            continue
        if r.get("prioridade") not in prioridades:
            continue
        if origem != "Todas" and r.get("origem") != origem:
            continue
        if bairro != "Todos" and r.get("bairro") != bairro:
            continue
        filtrados.append(r)
    return filtrados


def contagem_prioridade(registros: list[dict]) -> dict[str, int]:
    """Contagem determinística de prioridades preservando todas as chaves."""
    conteudo = Counter(registro.get("prioridade") for registro in registros)
    return {nivel: conteudo.get(nivel, 0) for nivel in ("alta", "media", "baixa")}


def contagem_categoria(registros: list[dict]) -> dict[str, int]:
    """Contagem ordenada de registros por categoria."""
    conteudo = Counter(registro.get("categoria", "Não classificado") for registro in registros)
    return dict(sorted(conteudo.items(), key=lambda item: item[1], reverse=True))


def grafico_prioridades(registros: list[dict]) -> go.Figure:
    """Gráfico de barras interativo Plotly por prioridade com suporte a hover e zoom."""
    contagens = contagem_prioridade(registros)
    total = sum(contagens.values())
    percentuais = [f"{(v/total*100):.1f}%" if total > 0 else "0%" for v in contagens.values()]

    fig = go.Figure(go.Bar(
        x=["🔴 Alta", "🟠 Média", "🟢 Baixa"],
        y=list(contagens.values()),
        marker_color=[COR["alta"], COR["media"], COR["baixa"]],
        text=[f"{v} ({p})" if v > 0 else "0" for v, p in zip(contagens.values(), percentuais)],
        textposition="outside",
        hovertemplate="<b>Prioridade:</b> %{x}<br><b>Quantidade:</b> %{y}<br><b>Proporção:</b> %{text}<extra></extra>",
    ))
    fig.update_layout(
        title="<b>Distribuição de Relatos por Prioridade</b>",
        template="plotly_white",
        height=360,
        yaxis_title="Quantidade de registros",
        xaxis_title="Nível de Prioridade Sugerido / Confirmado",
        hovermode="x",
        margin=dict(l=35, r=25, t=60, b=45),
        yaxis=dict(rangemode="tozero", dtick=1),
        showlegend=False,
    )
    return fig


def grafico_categorias(registros: list[dict]) -> go.Figure:
    """Gráfico de barras horizontal interativo Plotly por categoria de problema."""
    contagens = contagem_categoria(registros)
    if not contagens:
        categorias = ["Nenhum registro"]
        valores = [0]
    else:
        categorias = list(contagens.keys())
        valores = list(contagens.values())

    fig = go.Figure(go.Bar(
        y=categorias,
        x=valores,
        orientation="h",
        marker_color=COR["primario"],
        text=valores,
        textposition="outside",
        hovertemplate="<b>Categoria:</b> %{y}<br><b>Relatos:</b> %{x}<extra></extra>",
    ))
    fig.update_layout(
        title="<b>Relatos por Categoria de Zeladoria Urbana</b>",
        template="plotly_white",
        height=360,
        xaxis_title="Quantidade de registros",
        yaxis_title="Categoria",
        margin=dict(l=40, r=30, t=60, b=45),
        xaxis=dict(rangemode="tozero", dtick=1),
        showlegend=False,
    )
    return fig
