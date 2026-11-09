# Matriz de rastreabilidade — GS Front-end 2026.2

Legenda: **Implementado** = possui código; **Testado** = teste automatizado local; **Pendente** = precisa de comprovação externa/manual.

| Exigência do professor | Evidência prevista no projeto | Estado verificado |
|---|---|---|
| Problema real, público e fonte | `README.md` §1, Prefeitura SP156 | Implementado/documentado |
| Entrada com validação | `features/relatar.py` e `schemas/relatos.py` | Implementado, testado backend |
| Streamlit → FastAPI HTTP | `frontend/providers/api.py` → `routers/analises.py` | Implementado, API testada |
| LLM no back-end, não no front | `backend/app/providers/llm.py` | Implementado, **conexão real pendente** |
| Saída Pydantic estruturada | `schemas/relatos.py` `ResultadoIA` | Implementado, testado com mock |
| Resposta útil, não dump | `features/relatar.py` | Implementado, UI não inspecionada no navegador |
| Front: `features`, `ui`, `state`, `providers` | pastas `frontend/` | Implementado |
| Back: `routers`, `schemas`, `pipelines`, `providers` | pastas `backend/app/` | Implementado |
| Estado e histórico | `state/store.py` (`st.session_state`) | Implementado, UI pendente de teste manual |
| Cache | `providers/api.py`: `@st.cache_data(ttl=20)` | Implementado, UI pendente de teste manual |
| Falha de API, timeout, LLM e JSON inválido | `providers/api.py`, `providers/llm.py`, testes | Implementado; testes da API e provider passam |
| Chave fora do Git | `.env.example`, `.gitignore`, backend config | Implementado |
| CORS restrito | `backend/app/main.py`, teste CORS | Testado |
| Tabs, colunas e sidebar | `app.py`, `features/painel.py` | Implementado, inspeção visual pendente |
| Latência, estado vazio/erro | `st.spinner`, `st.info`, `st.error` | Implementado, inspeção visual pendente |
| Cores + texto/ícones | `ui/components.py` e painel | Implementado, contraste manual pendente |
| Human-in-the-loop | revisão/correção/descarte antes da sessão | Implementado, teste UI manual pendente |
| Plotly com hover e zoom | `visualization.py` | Testado (objeto Plotly) |
| Ao menos 2 filtros | `features/painel.py` | Lógica testada, UI manual pendente |
| UI componente reutilizado | `ui/components.py`: `cabecalho` em 3 features | Implementado |
| Deploy público OU Docker | Dockerfiles e `docker-compose.yml` | Arquivos criados; **Docker não executado aqui** |
| ODS, ética, limites e decisões técnicas | `README.md` §§1, 3, 6–8 | Documentado |
| Teste com 3 pessoas + ajuste | `docs/validacao_usuarios.md` | **Pendente de teste real** |
| 3 casos IA entrada/esperada/obtida/ajuste | `docs/casos_teste_ia.md` | **Pendente de inferência real** |
| Vídeo de até 5 min | `docs/roteiro_video.md` | Roteiro preparado; **gravação pendente** |
| Repositório público GitHub | Arquivos e comandos no README | **Publicação pendente** |

**Não atribuir nota estimada ou informar nota máxima garantida:** o professor exige evidências reais e validação manual.
