# Roteiro para vídeo de até 5 minutos (meta: 4min35s)

**Preparação:** API e front funcionando em Docker ou deploy; LLM **real** configurado; três testes IA e três usuários documentados; chave mascarada; deixar 1 registro em histórico e poder reproduzir erro; gravar tela com fonte legível.

| Tempo | Tela / ação | Narrativa sugerida |
|---|---|---|
| 0:00–0:35 | Capa VivaBairro + problema | "Problemas nas calçadas, iluminação e manutenção fazem parte do cotidiano. Criamos uma POC para organizar relatos usando IA, com foco no cidadão." Cite SP156 como evidência, sem afirmar integração. |
| 0:35–1:00 | Público e ODS | Público-alvo, ODS 11 e 16, por que uma interface simples importa. |
| 1:00–2:12 | Entrada → FastAPI → LLM | Preencher relato fictício, destacar validação e spinner; mostrar resposta estruturada e aviso claro sobre IA. |
| 2:12–2:50 | Human-in-the-loop | Corrigir prioridade/resumo, confirmar e mostrar código `LOCAL` (não oficial). |
| 2:50–3:26 | Painel e filtros | Navegar para painel; mostrar Plotly hover, zoom e filtros de categoria/prioridade; identificar dados fictícios se houver. |
| 3:26–3:53 | Cenário de erro | Demonstrar API fora do ar ou uma resposta de erro tratada, sem exibir segredos. Reiniciar serviço. |
| 3:53–4:18 | Código e arquitetura | Mostrar rapidamente `features`, `ui`, `state`, `providers`, `routers`, `schemas`, `pipelines`, onde está a chamada LLM e `@st.cache_data`. |
| 4:18–4:35 | Evidências e limites | Mostrar tabela dos três casos reais e feedback dos três usuários, citar o ajuste feito; reforçar que não substitui canal oficial. |

**Importante:** não apresente testes em modo demo como inferência real. Não grave variáveis secretas, custos nem identificadores pessoais. Vídeo hospedado no YouTube como **não listado** ou como arquivo no repositório conforme o enunciado.
