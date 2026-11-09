"""Exemplos explicitamente fictícios para demonstrar os gráficos."""
def exemplos_ficticios() -> list[dict]:
    dados = [
        ("Centro", "Iluminação pública", "alta"),
        ("Lapa", "Calçadas e acessibilidade", "alta"),
        ("Pinheiros", "Vias e buracos", "media"),
        ("Sé", "Lixo e limpeza", "baixa"),
        ("Butantã", "Drenagem e alagamentos", "alta"),
        ("Mooca", "Vias e buracos", "media"),
    ]
    return [
        {
            "id": f"EXEMPLO-{idx:03}", "quando": "Exemplo ilustrativo", "bairro": bairro,
            "categoria": categoria, "prioridade": prioridade,
            "resumo": f"Exemplo fictício de {categoria.lower()} em {bairro}.",
            "origem": "Exemplo fictício", "revisao": "Simulado",
        }
        for idx, (bairro, categoria, prioridade) in enumerate(dados, 1)
    ]
