"""Validação E2E no ambiente de containers Docker ativos (FastAPI e Streamlit).
Executa o fluxo completo do munícipe no Chromium headless apontando para http://127.0.0.1:8501.
"""
import time
from playwright.sync_api import sync_playwright


def test_fluxo_docker():
    print("Iniciando validação E2E nos containers Docker ativos...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # 1. Acesso à aplicação no container Streamlit
        page.goto("http://127.0.0.1:8501", wait_until="networkidle")
        time.sleep(3)
        assert "VivaBairro" in page.title() or page.locator("text=VivaBairro").count() > 0
        print("  [OK] Container Streamlit acessível no navegador.")

        # 2. Preenchimento de relato no formulário
        bairro_input = page.locator('input[aria-label*="Bairro"]').first
        bairro_input.fill("Perdizes")

        desc_input = page.locator('textarea[aria-label*="O que aconteceu"]').first
        desc_input.fill("Degraus irregulares e piso esburacado na calçada impedem o trânsito de cadeirantes e pedestres com mobilidade reduzida.")

        # 3. Submissão (Front-end no Docker comunica com API no Docker via http://api:8000)
        analisar_btn = page.locator('button:has-text("Analisar meu relato")').first
        analisar_btn.click()

        # 4. Aguarda análise preliminar
        page.wait_for_selector('text=Sugestão do Assistente', timeout=15000)
        print("  [OK] Comunicação inter-container (Web -> API) concluída com sucesso.")

        # 5. Validação do Human-in-the-Loop no Docker
        expander = page.locator('[data-testid="stExpander"] summary').first
        assert expander.count() > 0
        expander.click()
        time.sleep(1)
        expander.click()

        # 6. Confirmação do relato
        confirmar_btn = page.locator('button:has-text("Confirmar e Registrar")').first
        confirmar_btn.scroll_into_view_if_needed()
        confirmar_btn.click()

        # 7. Recibo gerado no container
        page.wait_for_selector('text=Registro local concluído com sucesso', timeout=15000)
        print("  [OK] Registro local gerado na sessão do Streamlit no Docker.")

        # 8. Navegação para o Painel de Relatos (Plotly)
        painel_btn = page.locator('button:has-text("Ver no Painel de Relatos")').first
        if painel_btn.count() > 0:
            painel_btn.click()
        else:
            page.locator('label:has-text("Painel de relatos")').first.click()

        time.sleep(3)
        assert page.locator('div[data-testid="stPlotlyChart"]').count() > 0
        print("  [OK] Gráficos Plotly renderizados com sucesso no container.")

        # 9. Teste de responsividade mobile no Docker (390x844)
        context_mob = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
        page_mob = context_mob.new_page()
        page_mob.goto("http://127.0.0.1:8501", wait_until="networkidle")
        time.sleep(2)
        scroll_w = page_mob.evaluate("() => document.documentElement.scrollWidth")
        client_w = page_mob.evaluate("() => document.documentElement.clientWidth")
        assert scroll_w <= client_w + 2, f"Overflow no Docker: {scroll_w} > {client_w}"
        print(f"  [OK] Responsividade mobile no Docker validada: {scroll_w}px == {client_w}px (zero overflow).")

        browser.close()
        print("\nTodos os fluxos E2E no ambiente Docker foram 100% aprovados!")


if __name__ == "__main__":
    test_fluxo_docker()
