"""Script automatizado de validação E2E e geração de evidências visuais com Playwright.
Executa FastAPI e Streamlit, valida fluxos e captura telas em Desktop, Tablet e Mobile.
"""
import os
import sys
import time
import subprocess
import httpx
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EVIDENCIAS_DIR = os.path.join(BASE_DIR, "docs", "evidencias")
os.makedirs(EVIDENCIAS_DIR, exist_ok=True)


def aguardar_servidor(url: str, timeout: float = 25.0) -> bool:
    inicio = time.time()
    while time.time() - inicio < timeout:
        try:
            r = httpx.get(url, timeout=2.0)
            if r.status_code in (200, 304):
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def main():
    env = os.environ.copy()
    env["PYTHONPATH"] = BASE_DIR
    env["LLM_PROVIDER"] = "demo"
    env["API_BASE_URL"] = "http://127.0.0.1:8000"

    print("1. Iniciando FastAPI Backend em http://127.0.0.1:8000 ...")
    proc_api = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=BASE_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    print("2. Iniciando Streamlit Frontend em http://127.0.0.1:8501 ...")
    proc_web = subprocess.Popen(
        [
            sys.executable, "-m", "streamlit", "run", "frontend/app.py",
            "--server.address", "127.0.0.1",
            "--server.port", "8501",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ],
        cwd=BASE_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        if not aguardar_servidor("http://127.0.0.1:8000/health", timeout=15):
            print("ERRO: Backend FastAPI não respondeu em /health")
            return 1
        print("Backend saudável!")

        if not aguardar_servidor("http://127.0.0.1:8501", timeout=20):
            print("ERRO: Frontend Streamlit não subiu a tempo")
            return 1
        print("Frontend acessível!")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            # -------------------------------------------------------------
            # CENÁRIO 1: DESKTOP (1440 x 900)
            # -------------------------------------------------------------
            print("\nCapturando telas Desktop (1440x900)...")
            context_desk = browser.new_context(viewport={"width": 1440, "height": 900})
            page = context_desk.new_page()

            page.goto("http://127.0.0.1:8501", wait_until="networkidle")
            time.sleep(3)

            # 01. Formulário Inicial
            page.evaluate("window.scrollTo(0, 0)")
            desk_inicial = os.path.join(EVIDENCIAS_DIR, "01_desktop_formulario_inicial.png")
            page.screenshot(path=desk_inicial, full_page=True)
            print(f"Salvo: {desk_inicial}")

            # Preenchendo relato
            print("Preenchendo relato...")
            bairro_input = page.locator('input[aria-label*="Bairro"]').first
            bairro_input.fill("Lapa")

            descricao_input = page.locator('textarea[aria-label*="O que aconteceu"]').first
            descricao_input.fill(
                "Uma calçada perto da praça tem degraus e blocos quebrados que bloqueiam totalmente a passagem de quem usa cadeira de rodas ou carrinho de bebê."
            )

            # Submeter análise
            print("Submetendo para análise de IA...")
            analisar_btn = page.locator('button:has-text("Analisar meu relato com IA")').first
            analisar_btn.click()

            # Aguarda a tela de revisão aparecer
            page.wait_for_selector('text=Sugestão da Inteligência Artificial', timeout=15000)
            time.sleep(2)

            # 02. Revisão Humana (Human-in-the-Loop)
            page.evaluate("window.scrollTo(0, 0)")
            desk_revisao = os.path.join(EVIDENCIAS_DIR, "02_desktop_revisao_human_in_the_loop.png")
            page.screenshot(path=desk_revisao, full_page=True)
            print(f"Salvo: {desk_revisao}")

            # Confirmar relato
            print("Confirmando relato...")
            confirmar_btn = page.locator('button:has-text("Confirmar e Registrar")').first
            confirmar_btn.scroll_into_view_if_needed()
            confirmar_btn.click()

            # Aguarda o recibo de confirmação
            page.wait_for_selector('text=Registro local concluído com sucesso', timeout=15000)
            time.sleep(2)

            # 03. Recibo pós-confirmação
            page.evaluate("window.scrollTo(0, 0)")
            desk_confirmado = os.path.join(EVIDENCIAS_DIR, "03_desktop_recibo_confirmacao.png")
            page.screenshot(path=desk_confirmado, full_page=True)
            print(f"Salvo: {desk_confirmado}")

            # 04. Painel de Relatos (Plotly)
            print("Navegando para o Painel de Relatos...")
            painel_nav = page.locator('button:has-text("Ver no Painel de Relatos")').first
            if painel_nav.count() > 0:
                painel_nav.click()
            else:
                page.locator('label:has-text("Painel de relatos")').first.click()

            time.sleep(4)
            page.evaluate("window.scrollTo(0, 0)")
            desk_painel = os.path.join(EVIDENCIAS_DIR, "04_desktop_painel_plotly.png")
            page.screenshot(path=desk_painel, full_page=True)
            print(f"Salvo: {desk_painel}")

            # 05. Como funciona (Ética e ODS)
            print("Navegando para 'Como funciona'...")
            sobre_nav = page.locator('label:has-text("Como funciona")').first
            sobre_nav.click()
            time.sleep(3)

            page.evaluate("window.scrollTo(0, 0)")
            desk_sobre = os.path.join(EVIDENCIAS_DIR, "05_desktop_como_funciona_ods_etica.png")
            page.screenshot(path=desk_sobre, full_page=True)
            print(f"Salvo: {desk_sobre}")

            context_desk.close()

            # -------------------------------------------------------------
            # CENÁRIO 2: TABLET (768 x 1024)
            # -------------------------------------------------------------
            print("\nCapturando tela Tablet (768x1024)...")
            context_tab = browser.new_context(viewport={"width": 768, "height": 1024})
            page_tab = context_tab.new_page()
            page_tab.goto("http://127.0.0.1:8501", wait_until="networkidle")
            time.sleep(3)
            page_tab.evaluate("window.scrollTo(0, 0)")

            tab_form = os.path.join(EVIDENCIAS_DIR, "06_tablet_formulario.png")
            page_tab.screenshot(path=tab_form, full_page=True)
            print(f"Salvo: {tab_form}")
            context_tab.close()

            # -------------------------------------------------------------
            # CENÁRIO 3: MOBILE (390 x 844 - Smartphone moderno)
            # -------------------------------------------------------------
            print("\nCapturando tela Mobile (390x844)...")
            context_mob = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
            page_mob = context_mob.new_page()
            page_mob.goto("http://127.0.0.1:8501", wait_until="networkidle")
            time.sleep(3)
            page_mob.evaluate("window.scrollTo(0, 0)")

            mob_form = os.path.join(EVIDENCIAS_DIR, "07_mobile_responsivo.png")
            page_mob.screenshot(path=mob_form, full_page=True)
            print(f"Salvo: {mob_form}")
            context_mob.close()

            browser.close()
            print("\nTodas as evidências visuais foram geradas com sucesso!")

    finally:
        print("Encerrando processos de teste...")
        proc_web.terminate()
        proc_api.terminate()
        try:
            proc_web.wait(timeout=3)
            proc_api.wait(timeout=3)
        except Exception:
            proc_web.kill()
            proc_api.kill()


if __name__ == "__main__":
    main()
