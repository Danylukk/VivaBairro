# Relatório técnico de verificação — preparação da POC

Data da execução: **09/11/2026** (ambiente de preparação automatizado).

## Executado de fato

- `pytest -q`: **27 testes aprovados**, cobrindo API FastAPI em simulação, contratos Pydantic, integração com provedor LLM usando mocks, saída inválida, timeouts, proteção de erros, CORS, integração de filtros e objetos Plotly.
- `python -m compileall -q backend frontend tests`: **concluído sem erros de sintaxe**.
- Teste HTTP real da API com Uvicorn: `GET /health` retornou `status=ok, modo=demonstracao`; `POST /api/v1/analises` com entrada fictícia válida retornou JSON Pydantic e prioridade alta em modo demonstração.
- Verificações não exigem chamada paga ao provedor LLM.

## Limitações verificadas no ambiente

- **Streamlit não estava instalado** neste ambiente e não havia acesso externo a pacotes; portanto **não foi executado teste visual real em navegador** nem `st.form`/fluxo de UI automatizado.
- **Docker não estava instalado**; `docker compose up --build` **não foi executado aqui**. Os artefatos Docker foram criados e precisam de validação em máquina com Docker.
- **Nenhuma chave real foi fornecida**; não foi feita inferência com OpenAI, logo 3 casos reais de IA continuam pendentes.
- **Três testes com pessoas não foram realizados**, pois exigem participação real.
- Nenhuma publicação no GitHub, URL de deploy externo ou gravação de vídeo foi realizada.

## Checklist manual (para executar antes da entrega)

- [ ] Executar `docker compose up --build` e verificar ambos os serviços.
- [ ] Validar layout desktop e mobile, navegação teclado, contraste, estados vazios.
- [ ] Executar entrada válida/inválida no front e confirmar resposta do backend.
- [ ] Ativar LLM real, executar 3 casos e salvar resultados no arquivo correspondente.
- [ ] Corrigir categoria/prioridade/resumo, confirmar e verificar gráfico e filtros.
- [ ] Simular API fora do ar: mensagem amigável, sem traceback ao usuário.
- [ ] Executar três sessões com participantes e implementar pelo menos um ajuste real.
- [ ] Inspecionar repositório antes de publicar: nenhuma chave, arquivo `.env` ou dados pessoais.
- [ ] Gravar vídeo de no máximo 5 minutos e enviar links oficiais.
