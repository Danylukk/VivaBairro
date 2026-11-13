"""Regressao visual da etapa de revisao em desktop/mobile (modo demo)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright
from scripts.avaliar_usabilidade_simulada import (
    preencher, submeter, verificar_demo,
)

BASE = Path(__file__).resolve().parents[1] / "docs" / "evidencias" / "feedback_usabilidade_20261113"


def rodar(fase: str, url: str, api_url: str) -> None:
    verificar_demo(api_url)  # Bloqueia execucao em provedor pago.
    pasta = BASE / fase
    pasta.mkdir(parents=True, exist_ok=True)
    saidas = []
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        for nome, largura, altura, mobile in [
            ("desktop", 1440, 900, False),
            ("mobile", 390, 844, True),
        ]:
            ctx = navegador.new_context(
                viewport={"width": largura, "height": altura},
                color_scheme="light", is_mobile=mobile, has_touch=mobile,
            )
            pagina = ctx.new_page()
            pagina.goto(url, wait_until="domcontentloaded")
            pagina.locator('input[aria-label*="Bairro"]').first.wait_for(timeout=30000)
            preencher(
                pagina, "Vila Leopoldina", "Calçadas e acessibilidade",
                "A calcada proxima da praca esta quebrada e impede a passagem "
                "segura de cadeirantes, pedestres e familias com carrinhos de bebe.",
            )
            submeter(pagina)
            pagina.get_by_text("Sua Decisão Humana", exact=False).first.wait_for(timeout=30000)
            pagina.screenshot(path=str(pasta / (nome + "_revisao.png")), full_page=True)
            conteudo = pagina.locator("body").inner_text()
            resumo_visivel = "Por que esta prioridade?" in conteudo
            tem_details = pagina.get_by_text(
                "Ver justificativa e informações adicionais", exact=False
            ).count() > 0
            verificacao = {
                "cenario": nome,
                "antes": fase == "antes",
                "justificativa_visivel_por_padrao": resumo_visivel,
                "controle_detalhes": tem_details,
                "aviso_risco_visivel": "Atenção Imediata Identificada" in conteudo,
                "revisao_visivel": "Sua Decisão Humana" in conteudo,
            }
            if fase == "depois":
                assert tem_details, "Expansor de justificativa ausente"
                assert not resumo_visivel, "Justificativa deveria estar recolhida"
                assert verificacao["aviso_risco_visivel"], "Risco importante foi escondido"
                exp = pagina.get_by_text(
                    "Ver justificativa e informações adicionais", exact=False
                )
                exp.click()
                pagina.get_by_text("Por que esta prioridade?", exact=False).first.wait_for()
                assert "Por que esta prioridade?" in pagina.locator("body").inner_text()
                assert pagina.get_by_role(
                    "button", name="Confirmar e Registrar nesta Sessão"
                ).count() > 0
                pagina.screenshot(
                    path=str(pasta / (nome + "_detalhes_expandidos.png")),
                    full_page=True,
                )
                largura_real = pagina.evaluate(
                    "() => ({largura: document.documentElement.scrollWidth,"
                    " tela: document.documentElement.clientWidth})"
                )
                assert largura_real["largura"] <= largura_real["tela"] + 2
                verificacao["detalhes_abriram"] = True
                verificacao["sem_rolagem_horizontal"] = True
            saidas.append(verificacao)
            ctx.close()
            print("OK " + fase + " " + nome, flush=True)
        navegador.close()
    arquivo = pasta / "resultados.json"
    arquivo.write_text(
        json.dumps({"metodo": "Navegador automatizado; nao sao respostas de participantes.",
                    "cenarios": saidas}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Evidencias:", arquivo, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fase", required=True, choices=("antes", "depois"))
    parser.add_argument("--url", default="http://127.0.0.1:18501")
    parser.add_argument("--api", default="http://127.0.0.1:18000")
    args = parser.parse_args()
    rodar(args.fase, args.url, args.api)
