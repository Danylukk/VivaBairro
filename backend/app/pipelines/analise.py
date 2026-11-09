"""Orquestração separada do transporte HTTP e da interface."""
from backend.app.config import Settings
from backend.app.providers.llm import analisar_openai
from backend.app.schemas.relatos import RelatoEntrada, ResultadoIA, RespostaAnalise

ORIENTACOES = {
    "Vias e buracos": ("Sinalizar o risco com segurança e registrar detalhes da condição da via.", "Manutenção de vias"),
    "Calçadas e acessibilidade": ("Descrever a barreira de passagem e buscar orientação no serviço municipal de acessibilidade.", "Manutenção de calçadas"),
    "Iluminação pública": ("Evitar pontos escuros com risco e consultar o canal municipal de iluminação pública.", "Iluminação pública"),
    "Lixo e limpeza": ("Evitar contato com resíduos potencialmente perigosos e consultar o canal municipal de limpeza.", "Limpeza urbana"),
    "Drenagem e alagamentos": ("Evitar a área alagada e acompanhar orientações oficiais de segurança e defesa civil.", "Drenagem urbana"),
    "Outros": ("Registrar mais detalhes e consultar o serviço municipal adequado ao problema.", "Atendimento municipal"),
}


def analisar_demo(entrada: RelatoEntrada) -> ResultadoIA:
    """DEMONSTRAÇÃO DETERMINÍSTICA: não é LLM e não deve ser apresentada como IA real."""
    texto = entrada.descricao.casefold()
    sinais = ("ferid", "acident", "cadeirante", "não consegue passar", "impede a passagem", "cadeira de rodas", "queda", "risco", "perigo", "alagad", "fio exposto")
    alta = any(palavra in texto for palavra in sinais)
    orientacao, encaminhamento = ORIENTACOES[entrada.categoria_informada]
    return ResultadoIA(
        categoria=entrada.categoria_informada,
        prioridade="alta" if alta else "media",
        resumo=f"Relato sobre {entrada.categoria_informada.lower()} no bairro {entrada.bairro}.",
        justificativa="O texto menciona possível risco e precisa de revisão humana." if alta else "A prioridade sugerida é preliminar e exige revisão humana.",
        orientacao=orientacao,
        encaminhamento=encaminhamento,
        atencao_imediata=alta,
    )


def processar(entrada: RelatoEntrada, settings: Settings) -> RespostaAnalise:
    if settings.llm_provider == "demo":
        return RespostaAnalise(
            resultado=analisar_demo(entrada), modo="demonstracao",
            aviso="Resultado fictício gerado por regras para demonstrar a interface. NÃO é resposta de um LLM.",
        )
    return RespostaAnalise(
        resultado=analisar_openai(entrada, settings), modo="llm",
        aviso="Sugestão gerada por IA. Confira e corrija antes de registrar.",
    )
