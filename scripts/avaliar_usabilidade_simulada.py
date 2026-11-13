"""Avalia tres jornadas ficticias pelo navegador (nao sao usuarios reais).

Usar API em modo demo: python -m scripts.avaliar_usabilidade_simulada --fase antes|depois
Nao consome LLM e nao fabrica depoimentos de participantes.
"""
import argparse
import json
from pathlib import Path
import re
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parents[1]
EVIDENCIAS = RAIZ / "docs" / "evidencias" / "usabilidade_simulada"


def verificar_demo(api_url):
    with urlopen(api_url + "/health", timeout=4) as r:
        d = json.loads(r.read())
    if d.get("modo") != "demonstracao":
        raise RuntimeError("Abortando: provedor nao esta no modo demonstracao.")


def abrir(browser, url, largura, altura, mobile=False):
    ctx = browser.new_context(
        viewport={"width": largura, "height": altura},
        is_mobile=mobile, has_touch=mobile, color_scheme="light",
    )
    page = ctx.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    page.locator('input[aria-label*="Bairro"]').first.wait_for(timeout=30000)
    return ctx, page


def selecionar(page, indice, texto):
    page.locator('[data-baseweb="select"]').nth(indice).click()
    page.get_by_text(texto, exact=True).last.click()


def preencher(page, bairro, categoria, descricao):
    page.locator('input[aria-label*="Bairro"]').first.fill(bairro)
    selecionar(page, 0, categoria)
    page.locator('textarea[aria-label*="O que aconteceu"]').first.fill(descricao)


def submeter(page):
    page.get_by_role("button", name=re.compile("Analisar meu relato")).click()
    page.get_by_text("Sugestão do Assistente", exact=False).first.wait_for(timeout=25000)


def confirmar(page):
    page.get_by_role("button", name=re.compile("Confirmar e Registrar")).click()
    page.get_by_text("Registro local concluído com sucesso", exact=False).first.wait_for(timeout=25000)


def capturar(page, fase, nome):
    destino = EVIDENCIAS / fase
    destino.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(destino / (nome + ".png")), full_page=True)


def tela_painel(page):
    btn = page.get_by_role("button", name=re.compile("Ver no Painel de Relatos"))
    if btn.count():
        btn.click()
    else:
        # Em telas pequenas, expandir a barra lateral antes de trocar a pagina.
        pagina = page.get_by_text("Painel de relatos", exact=True)
        if not pagina.is_visible():
            for seletor in (
                '[data-testid="stSidebarCollapsedControl"] button',
                'button[aria-label="Open sidebar"]',
                'button[aria-label="Expand sidebar"]',
            ):
                botoes = page.locator(seletor)
                if botoes.count() and botoes.first.is_visible():
                    botoes.first.click()
                    break
        pagina.click()
    page.get_by_text("Painel Interativo de Relatos").first.wait_for(timeout=25000)


def fluxo(fase, url, api_url):
    verificar_demo(api_url)
    resultados = []
    with sync_playwright() as sp:
        browser = sp.chromium.launch(headless=True)

        # Cenario 1: perfil ficticio com pouca fluencia digital.
        ctx, page = abrir(browser, url, 1440, 900)
        capturar(page, fase, "01_inicio_desktop")
        desc = ("Na praça do bairro, a calcada esta com blocos quebrados e degraus "
                "que impedem a passagem segura de cadeirantes e pessoas com carrinho de bebe.")
        preencher(page, "Sé", "Calçadas e acessibilidade", desc)
        page.get_by_role("button", name=re.compile("Analisar meu relato")).click()
        page.wait_for_function("""() => document.body.innerText.includes("deve ter pelo menos 3 caracteres") || document.body.innerText.includes("Sugestão do Assistente")""", timeout=25000)
        aviso = page.get_by_text("deve ter pelo menos 3 caracteres", exact=False)
        recusado = aviso.count() > 0 and aviso.first.is_visible()
        resultados.append({"cenario": "01_acessibilidade", "bairro_se_recusado": recusado})
        capturar(page, fase, "01_bairro_se")
        if recusado:
            page.locator('input[aria-label*="Bairro"]').first.fill("Lapa")
            submeter(page)
        else:
            page.get_by_text("Sugestão do Assistente", exact=False).first.wait_for(timeout=25000)
        capturar(page, fase, "01_revisao")
        confirmar(page)
        capturar(page, fase, "01_recibo")
        recibo_texto = page.locator("body").inner_text()
        resultados[-1]["recibo_local"] = "LOCAL-" in recibo_texto
        resultados[-1]["aviso_nao_e_protocolo"] = "Não é protocolo oficial da Prefeitura" in recibo_texto
        if fase == "depois":
            assert not recusado, "Bairro Sé nao pode ser rejeitado"
            assert resultados[-1]["aviso_nao_e_protocolo"], "Recibo nao explica que nao e protocolo oficial"
        ctx.close()
        print("SCENARIO_01 OK; bairro_se_recusado=" + str(recusado), flush=True)

        # Cenario 2: uso em smartphone e consulta a dados da sessao.
        ctx, page = abrir(browser, url, 390, 844, mobile=True)
        preencher(
            page, "Centro", "Iluminação pública",
            "Diversas luminarias da praca estao apagadas ha dias e a rua fica muito escura no periodo noturno."
        )
        capturar(page, fase, "02_form_mobile")
        submeter(page)
        confirmar(page)
        capturar(page, fase, "02_recibo_mobile")
        tela_painel(page)
        page.locator('[data-testid="stPlotlyChart"]').first.wait_for(timeout=25000)
        capturar(page, fase, "02_painel_mobile")
        medida = page.evaluate("() => ({scroll:document.documentElement.scrollWidth, client:document.documentElement.clientWidth})")
        assert medida["scroll"] <= medida["client"]+2, medida
        resultados.append({"cenario": "02_mobile", "painel_plotly": True, "sem_overflow": True})
        ctx.close()
        print("SCENARIO_02 OK; mobile charts and layout", flush=True)

        # Cenario 3: revisao efetiva da classificacao antes do registro.
        ctx, page = abrir(browser, url, 1440, 900)
        preencher(
            page, "Mooca", "Vias e buracos",
            "Existe um buraco grande na via principal, proximo da faixa de pedestres, prejudicando o transito de veiculos."
        )
        submeter(page)
        capturar(page, fase, "03_revisao_antes")
        selecionar(page, 1, "🔴 Alta — Atenção urgente")
        novo_resumo = "Buraco grande na via principal da Mooca; solicitacao de revisao do local."
        campo = page.locator('textarea[aria-label*="Resumo final do relato"]').first
        campo.fill(novo_resumo)
        confirmar(page)
        capturar(page, fase, "03_recibo_alterado")
        texto = page.locator("body").inner_text()
        assert novo_resumo in texto
        tela_painel(page)
        page.locator('[data-testid="stPlotlyChart"]').first.wait_for(timeout=25000)
        capturar(page, fase, "03_painel")
        resultados.append({"cenario": "03_revisao", "resumo_editado_preservado": True, "painel_plotly": True})
        ctx.close()
        print("SCENARIO_03 OK; human review persisted in session", flush=True)
        browser.close()

    saida = EVIDENCIAS / fase / "resultados.json"
    saida.write_text(
        json.dumps({"metodo": "Testes automatizados usando personas ficticias, sem participantes reais",
                    "fase": fase, "cenarios": resultados}, ensure_ascii=False, indent=2)+"\n",
        encoding="utf-8",
    )
    print("EVIDENCE_FILE", str(saida),flush=True)


if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--fase",choices=("antes","depois"),required=True)
    ap.add_argument("--url",default="http://127.0.0.1:18501")
    ap.add_argument("--api",default="http://127.0.0.1:18000")
    args=ap.parse_args()
    fluxo(args.fase,args.url,args.api)
