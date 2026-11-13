"""Grava trajetos reais do browser para o vídeo silencioso da GS.

Requer API + frontend em modo demonstracao. Não chama LLM pago.
Cria apenas arquivos temporarios; video final montado por editar_video_gs.py.
"""
from __future__ import annotations
import json
import re
import shutil
import tempfile
import time
from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import sync_playwright

BASE = Path(tempfile.gettempdir()) / "VivaBairro_Video_GS_20261113"
BASE.mkdir(parents=True, exist_ok=True)
URL = "http://127.0.0.1:18501"
API = "http://127.0.0.1:18000"
VIDEO_W, VIDEO_H = 1600, 900


def demo_ok():
    with urlopen(API + "/health", timeout=6) as res:
        payload = json.loads(res.read())
    assert payload.get("modo") == "demonstracao", "Recusado: LLM pago ativo"
    print("API_DEMO_VALIDATED", flush=True)


def loc_select(page, index, text):
    page.locator('[data-baseweb="select"]').nth(index).click()
    page.get_by_text(text, exact=True).last.click()


def wait(seconds):
    time.sleep(seconds)


def new_page(browser, name):
    ctx = browser.new_context(
        viewport={"width": VIDEO_W, "height": VIDEO_H},
        record_video_dir=str(BASE), record_video_size={"width": VIDEO_W, "height": VIDEO_H},
        color_scheme="light", device_scale_factor=1,
    )
    page = ctx.new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=30000)
    page.locator('input[aria-label*="Bairro"]').first.wait_for(timeout=30000)
    return ctx, page


def capture_chapter(page, bookmarks, name, expected_seconds, action):
    start = time.monotonic()
    action()
    elapsed = time.monotonic() - start
    if elapsed < expected_seconds:
        page.wait_for_timeout(int((expected_seconds - elapsed) * 1000))
    end = time.monotonic()
    bookmarks.append({"name": name, "start": start, "end": end, "duration": end-start})
    print(f"CAPTURED {name}: {end-start:.1f} seconds", flush=True)


def save(ctx, page, name, bookmarks, start_time):
    # Normalize timestamps to the beginning of this recording.
    timeline = []
    for mark in bookmarks:
        timeline.append({
            "name": mark["name"], "ss": round(mark["start"] - start_time, 3),
            "duration": round(mark["duration"], 3)
        })
    ctx.close()
    source = Path(page.video.path())
    target = BASE / f"{name}.webm"
    shutil.copy2(source, target)
    print("VIDEO", target, target.stat().st_size, flush=True)
    return {"file": str(target), "bookmarks": timeline}


def main():
    demo_ok()
    manifest = {}
    with sync_playwright() as play:
        browser = play.chromium.launch(headless=True)

        # REAL SCREEN RECORDING 01: registro -> classificacao -> revisao -> recibo
        ctx, page = new_page(browser, "relato")
        start_time = time.monotonic()
        marks = []

        def intro():
            page.mouse.move(910, 326, steps=12)
            wait(4)
            page.mouse.wheel(0, 460)
            wait(3)
            page.mouse.move(355, 640, steps=18)
            wait(2)
        capture_chapter(page, marks, "ui_inicio", 16, intro)

        def formulario():
            page.locator('input[aria-label*="Bairro"]').first.fill("Vila Leopoldina")
            page.mouse.move(750, 360, steps=20)
            loc_select(page, 0, "Calçadas e acessibilidade")
            desc=("Uma calçada com blocos quebrados e desníveis perto de uma praça "
                  "dificulta a passagem segura de pedestres e cadeirantes.")
            page.locator('textarea[aria-label*="O que aconteceu"]').first.press_sequentially(
                desc, delay=28
            )
            page.mouse.wheel(0, 370)
            page.get_by_role("button",name=re.compile("Analisar meu relato")).first.hover()
            wait(2)
            page.get_by_role("button",name=re.compile("Analisar meu relato")).first.click()
            page.get_by_text("Sugestão do Assistente", exact=False).first.wait_for(timeout=30000)
        capture_chapter(page,marks,"ui_formulario",27,formulario)

        def analise():
            page.mouse.wheel(0, 280)
            wait(4)
            page.get_by_text("Ver justificativa e informações adicionais", exact=False).first.click()
            wait(5)
            page.mouse.wheel(0, 220)
            wait(4)
            page.get_by_text("Ver justificativa e informações adicionais", exact=False).first.click()
            wait(2)
        capture_chapter(page,marks,"ui_analise",22,analise)

        def revisao():
            page.get_by_text("Sua Decisão Humana", exact=False).first.scroll_into_view_if_needed()
            page.mouse.wheel(0, 300)
            wait(3)
            # Verifica opções, mantém prioridade alta caso o cenário tenha risco.
            page.locator('textarea[aria-label*="Resumo final do relato"]').first.fill(
                "Calçada danificada na Vila Leopoldina: risco à passagem de pedestres e cadeirantes."
            )
            page.get_by_text("Parcialmente adequada",exact=True).first.click()
            wait(3)
            page.mouse.wheel(0, 280)
            btn=page.get_by_role("button",name=re.compile("Confirmar e Registrar"))
            btn.hover()
            wait(4)
            btn.click()
            page.get_by_text("Registro local concluído com sucesso", exact=False).first.wait_for(timeout=30000)
        capture_chapter(page,marks,"ui_revisao",25,revisao)

        def recibo():
            page.mouse.wheel(0, -900)
            wait(3)
            page.get_by_text("Este código é somente um comprovante",exact=False).first.wait_for()
            page.mouse.move(1054, 560, steps=20)
            wait(3)
        capture_chapter(page,marks,"ui_recibo",13,recibo)
        manifest["relato"] = save(ctx,page,"relato",marks,start_time)

        # REAL SCREEN RECORDING 02: painel e filtros com exemplos claramente ficticios
        ctx, page = new_page(browser,"painel")
        page.get_by_text("Painel de relatos",exact=True).first.click()
        page.get_by_role("button",name=re.compile("Carregar 6 exemplos fictícios")).wait_for(timeout=15000)
        page.get_by_role("button",name=re.compile("Carregar 6 exemplos fictícios")).click()
        page.locator('[data-testid="stPlotlyChart"]').first.wait_for(timeout=30000)
        start_time=time.monotonic()
        marks=[]
        def dashboard():
            page.mouse.move(1020, 340,steps=14)
            wait(3)
            page.mouse.wheel(0, 440)
            wait(4)
            # Interaja nos graficos com mouse para acionar hover/tooltip.
            chart=page.locator('[data-testid="stPlotlyChart"]:visible').first
            if chart.count():
                chart.hover(timeout=3000)
            wait(5)
            page.get_by_role("tab",name=re.compile("Relatos por Categoria")).first.click()
            wait(5)
            chart=page.locator('[data-testid="stPlotlyChart"]:visible').first
            if chart.count():
                chart.hover(timeout=3000)
            wait(4)
            page.mouse.wheel(0,-450)
            wait(3)
        capture_chapter(page,marks,"ui_painel",34,dashboard)
        manifest["painel"]=save(ctx,page,"painel",marks,start_time)

        # REAL SCREEN RECORDING 03: ODS e limites do prototipo.
        ctx,page=new_page(browser,"ods")
        page.get_by_text("Como funciona",exact=True).first.click()
        page.get_by_text("Arquitetura, Ética e Impacto Social").first.wait_for(timeout=20000)
        start_time=time.monotonic()
        marks=[]
        def ods():
            page.get_by_role("tab",name=re.compile("ODS e Impacto Social")).first.click()
            wait(4)
            page.mouse.wheel(0, 390)
            wait(3)
            page.mouse.wheel(0,-340)
            wait(1)
            page.get_by_role("tab",name=re.compile("Ética e Limites da IA")).first.click()
            wait(2)
        capture_chapter(page,marks,"ui_ods",14,ods)
        manifest["ods"]=save(ctx,page,"ods",marks,start_time)
        browser.close()
    out=BASE / "manifest.json"
    out.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    print("MANIFEST",out,flush=True)


if __name__=="__main__":
    main()
