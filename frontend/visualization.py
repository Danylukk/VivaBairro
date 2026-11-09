"""Transformações e construção Plotly independentes do Streamlit."""
from collections import Counter
import plotly.graph_objects as go

COR = {"alta": "#b42318", "media": "#a15c00", "baixa": "#137547"}


def aplicar_filtros(registros: list[dict], categoria: str, prioridades: list[str]) -> list[dict]:
    return [
        r for r in registros
        if (categoria == "Todas" or r["categoria"] == categoria)
        and r["prioridade"] in prioridades
    ]


def contagem_prioridade(registros: list[dict]) -> dict[str, int]:
    conteudo = Counter(registro["prioridade"] for registro in registros)
    return {nivel: conteudo.get(nivel, 0) for nivel in ("alta", "media", "baixa")}


def grafico_prioridades(registros: list[dict]) -> go.Figure:
    contagens = contagem_prioridade(registros)
    fig = go.Figure(go.Bar(
        x=["Alta", "Média", "Baixa"],
        y=list(contagens.values()),
        marker_color=[COR["alta"], COR["media"], COR["baixa"]],
        text=list(contagens.values()),
        textposition="outside",
        hovertemplate="Prioridade: %{x}<br>Registros: %{y}<extra></extra>",
    ))
    fig.update_layout(
        title="Registros por prioridade", template="plotly_white", height=350,
        yaxis_title="Quantidade de registros", xaxis_title="Prioridade",
        hovermode="x", margin=dict(l=30, r=20, t=58, b=35),
        yaxis=dict(rangemode="tozero", dtick=1), showlegend=False,
    )
    return fig
