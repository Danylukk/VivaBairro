"""Validação dos filtros e das visualizações Plotly sem iniciar o Streamlit."""
from frontend.visualization import (
    aplicar_filtros,
    contagem_prioridade,
    contagem_categoria,
    grafico_prioridades,
    grafico_categorias,
)
from frontend.demo_data import exemplos_ficticios


def test_exemplos_sao_rotulados_ficticios():
    registros = exemplos_ficticios()
    assert len(registros) == 6
    assert all(r["origem"] == "Exemplo fictício" for r in registros)


def test_filtro_categoria():
    filtrados = aplicar_filtros(exemplos_ficticios(), "Vias e buracos", ["alta", "media", "baixa"])
    assert len(filtrados) == 2


def test_filtro_prioridade():
    filtrados = aplicar_filtros(exemplos_ficticios(), "Todas", ["alta"])
    assert len(filtrados) == 3


def test_dois_filtros_combinados():
    filtrados = aplicar_filtros(exemplos_ficticios(), "Vias e buracos", ["alta"])
    assert filtrados == []


def test_filtro_por_origem():
    exemplos = exemplos_ficticios()
    registros_mistos = exemplos + [
        {
            "id": "LOCAL-12345678", "quando": "09/11/2026 14:00", "bairro": "Pinheiros",
            "categoria": "Vias e buracos", "prioridade": "alta",
            "resumo": "Buraco crítico na via.", "origem": "Análise de LLM revisada",
            "revisao": "Confirmado sem alterações", "avaliacao_ia": "Sim, adequada"
        }
    ]
    apenas_llm = aplicar_filtros(registros_mistos, origem="Análise de LLM revisada")
    assert len(apenas_llm) == 1
    assert apenas_llm[0]["id"] == "LOCAL-12345678"

    apenas_ficticios = aplicar_filtros(registros_mistos, origem="Exemplo fictício")
    assert len(apenas_ficticios) == 6


def test_filtro_por_bairro():
    filtrados = aplicar_filtros(exemplos_ficticios(), bairro="Centro")
    assert len(filtrados) == 1
    assert filtrados[0]["bairro"] == "Centro"


def test_sem_prioridade_nao_mostra_dados():
    assert aplicar_filtros(exemplos_ficticios(), "Todas", []) == []


def test_contagem_inclui_zeros():
    filtrados = aplicar_filtros(exemplos_ficticios(), "Todas", ["alta"])
    assert contagem_prioridade(filtrados) == {"alta": 3, "media": 0, "baixa": 0}


def test_contagem_categoria():
    contagens = contagem_categoria(exemplos_ficticios())
    assert contagens["Vias e buracos"] == 2
    assert contagens["Iluminação pública"] == 1
    assert sum(contagens.values()) == 6


def test_plotly_prioridades_interativo_com_hover_e_zoom():
    fig = grafico_prioridades(exemplos_ficticios())
    assert fig.data[0].type == "bar"
    assert "hovertemplate" in fig.data[0].to_plotly_json()
    assert sum(fig.data[0].y) == 6
    assert fig.layout.hovermode == "x"


def test_plotly_categorias_interativo_com_hover():
    fig = grafico_categorias(exemplos_ficticios())
    assert fig.data[0].type == "bar"
    assert fig.data[0].orientation == "h"
    assert "hovertemplate" in fig.data[0].to_plotly_json()
    assert sum(fig.data[0].x) == 6


def test_plotly_vazio_nao_quebra():
    fig_vazia = grafico_categorias([])
    assert fig_vazia.data[0].type == "bar"
    assert sum(fig_vazia.data[0].x) == 0
