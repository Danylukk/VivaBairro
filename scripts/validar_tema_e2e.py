"""Valida o contraste do VivaBairro no browser real, inclusive em sistemas com tema escuro.

Pré-requisito: docker compose up -d --build
Executar: python -m scripts.validar_tema_e2e

Não envia relatos nem realiza chamadas ao LLM.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parents[1]
PASTA = RAIZ / "docs" / "evidencias"


def rgb(valor: str) -> tuple[float, float, float]:
    # getComputedStyle retorna rgb(r, g, b) nos navegadores Chromium suportados.
    numeros = valor.replace("rgb(", "").replace("rgba(", "").replace(")", "").split(",")
    return tuple(float(x.strip()) / 255 for x in numeros[:3])


def contraste(cor_a: str, cor_b: str) -> float:
    def lum(c: str) -> float:
        cores = rgb(c)
        linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in cores]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]
    a, b = sorted((lum(cor_a), lum(cor_b)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def info(page: object, seletor: str) -> dict[str, str]:
    return page.locator(seletor).first.evaluate("""el => {
        const css = getComputedStyle(el);
        return {cor: css.color, fundo: css.backgroundColor};
    }""")


def testar(base_url: str) -> None:
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        cenarios = [
            ("desktop_claro", "light", 1440, 900, False),
            ("desktop_sistema_escuro", "dark", 1440, 900, False),
            ("mobile_sistema_escuro", "dark", 390, 844, True),
        ]
        PASTA.mkdir(parents=True, exist_ok=True)
        for nome, esquema, largura, altura, mobile in cenarios:
            contexto = navegador.new_context(
                viewport={"width": largura, "height": altura},
                color_scheme=esquema,
                is_mobile=mobile,
                has_touch=mobile,
            )
            pagina = contexto.new_page()
            pagina.goto(base_url, wait_until="networkidle", timeout=25000)
            pagina.get_by_text("VivaBairro — Sua Voz na Cidade").first.wait_for(timeout=20000)

            app = info(pagina, ".stApp")
            lateral = info(pagina, '[data-testid="stSidebar"]')
            lateral_titulo = info(pagina, '[data-testid="stSidebar"] h1')
            corpo_titulo = info(pagina, '[data-testid="stMain"] h1')
            campo_rotulo = info(pagina, '[data-testid="stWidgetLabel"]')
            fundo_principal = app["fundo"]
            fundo_lateral = lateral["fundo"]

            resultados = {
                "titulo_principal": contraste(corpo_titulo["cor"], fundo_principal),
                "titulo_sidebar": contraste(lateral_titulo["cor"], fundo_lateral),
                "rotulo_formulario": contraste(campo_rotulo["cor"], fundo_principal),
            }
            for item, taxa in resultados.items():
                if taxa < 4.5:
                    raise AssertionError(f"{nome} — {item}: contraste {taxa:.2f}:1 abaixo de WCAG AA")
            if fundo_principal != "rgb(255, 255, 255)":
                raise AssertionError(f"{nome} — fundo principal inesperado: {fundo_principal}")
            if fundo_lateral != "rgb(248, 250, 252)":
                raise AssertionError(f"{nome} — fundo sidebar inesperado: {fundo_lateral}")
            medidas = pagina.evaluate("""() => ({
              larguraDocumento: document.documentElement.scrollWidth,
              larguraJanela: document.documentElement.clientWidth
            })""")
            if medidas["larguraDocumento"] > medidas["larguraJanela"] + 1:
                raise AssertionError(f"{nome} — transbordamento horizontal: {medidas}")
            captura = PASTA / f"09_tema_contraste_{nome}.png"
            pagina.screenshot(path=str(captura), full_page=True)
            print(f"OK {nome}: contraste título={resultados['titulo_principal']:.1f}:1, "
                  f"sidebar={resultados['titulo_sidebar']:.1f}:1, "
                  f"rótulo={resultados['rotulo_formulario']:.1f}:1; captura={captura.name}")
            contexto.close()
        navegador.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8501")
    args = parser.parse_args()
    testar(args.url)
