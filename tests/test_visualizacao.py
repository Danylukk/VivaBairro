"""Validação dos filtros e do gráfico sem iniciar o Streamlit."""
from frontend.visualization import aplicar_filtros, contagem_prioridade, grafico_prioridades
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


def test_sem_prioridade_nao_mostra_dados():
    assert aplicar_filtros(exemplos_ficticios(), "Todas", []) == []


def test_contagem_inclui_zeros():
    filtrados = aplicar_filtros(exemplos_ficticios(), "Todas", ["alta"])
    assert contagem_prioridade(filtrados) == {"alta": 3, "media": 0, "baixa": 0}


def test_plotly_interativo_com_hover():
    fig = grafico_prioridades(exemplos_ficticios())
    assert fig.data[0].type == "bar"
    assert "hovertemplate" in fig.data[0].to_plotly_json()
    assert sum(fig.data[0].y) == 6
