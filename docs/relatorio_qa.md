# Relatório Técnico de Garantia da Qualidade (QA) e Evidências

**Data da Auditoria e Testes:** 09/11/2026  
**Ambiente de Execução:** Windows 11 · Python 3.14 · Playwright Chromium · Pytest 9.0.3 · Streamlit 1.57 · FastAPI 0.137

---

## 1. Resumo Executivo das Verificações

A suíte completa de testes automatizados e validações end-to-end foi executada com **100% de sucesso**.

- **Testes Automatizados (Pytest):** **45 testes aprovados** (0 falhas, 0 warnings de bloqueio) em ~3.9 segundos.
- **Validação de Interface Nativa (Streamlit AppTest):** Inicialização, renderização de formulários e navegação entre abas validadas programaticamente.
- **Validação E2E no Navegador Real (Playwright):** Simulação completa da jornada do cidadão em três resoluções de tela distintas, com geração de 7 capturas de tela em alta resolução.
- **Auditoria de Código e Compilação:** `python -m compileall -q backend frontend tests scripts` executado sem qualquer erro sintático.

---

## 2. Cobertura da Suíte de Testes Automatizados (Pytest)

### 2.1 Backend e API (`tests/test_api.py` — 20 testes)
1. `test_health_demo`: Resposta do endpoint `/health` com status `ok` e modo `demonstracao`.
2. `test_fluxo_ponta_a_ponta_simulado`: Submissão de relato e retorno de `ResultadoIA` estruturado.
3. `test_exige_descricao_minima`: Rejeição de descrição com menos de 30 caracteres (HTTP 422).
4. `test_exige_bairro`: Rejeição de bairro com menos de 3 caracteres (HTTP 422).
5. `test_rejeita_categoria_desconhecida`: Validação estrita de enum da categoria informada (HTTP 422).
6. `test_rejeita_campos_extras`: Bloqueio de campos adicionais não previstos no schema (ex.: CPF, RG) (HTTP 422).
7. `test_limite_tamanho`: Rejeição de relatos que excedam 900 caracteres (HTTP 422).
8. `test_controle_nao_executa_acao_externa`: Garantia de que a API não inventa protocolos de prefeitura.
9. `test_cors_permitido`: Verificação de headers CORS para origens autorizadas (Streamlit em 8501).
10. `test_cors_estranho_sem_cabecalho_liberacao`: Bloqueio de origens arbitrárias não autorizadas.
11. `test_proibe_cors_global_em_producao`: Proibição estrita de wildcard `*` em `APP_ENV=production`.
12. `test_requer_segredo_para_ia`: Falha segura ao tentar inicializar modo `openai` sem chave de API.
13. `test_erro_llm_nao_vaza_detalhe`: Erros internos do LLM retornam mensagem genérica 503 sem expor tokens ou dados de infraestrutura.
14. `test_resposta_llm_estruturada_mockada`: Validação da orquestração do pipeline com resposta estruturada de LLM.
15. `test_saida_ia_invalida_e_rejeitada`: Pydantic rejeita saídas fora do contrato antes de devolver à UI.
16. `test_opcoes_frontend_batem_contrato_backend`: Sincronia perfeita entre categorias e prioridades no front e back.
17. `test_resiliencia_tentativa_prompt_injection`: Relato com tentativa de injeção de prompt ("Ignore todas as regras...") é tratado puramente como dado textual passivo, sem comprometer as instruções do sistema.
18. `test_resiliencia_caracteres_xss_e_html`: Tags HTML/script no relato são tratadas de forma segura.
19. `test_rejeita_caracteres_controle_invalidos`: Rejeição de bytes nulos ou caracteres de controle ASCII.
20. `test_strip_automatico_espacos`: Sanitização de espaços em branco antes e depois do texto.

### 2.2 Provedor de LLM (`tests/test_provider.py` — 7 testes)
1. `test_limpar_json_resposta`: Sanitização de saídas com e sem blocos markdown (` ```json `).
2. `test_provedor_retorna_pydantic_valido`: Conversão direta de JSON da API para objeto `ResultadoIA`.
3. `test_provedor_aceita_saida_com_markdown_fences`: Resiliência caso o modelo retorne JSON envolvido por delimitadores.
4. `test_provedor_respeita_base_url_customizada`: Suporte a gateways e proxies OpenAI compatíveis (`OPENAI_BASE_URL`).
5. `test_rejeita_resposta_invalida`: Exceção `LLMIndisponivel` levantada em caso de schema quebrado.
6. `test_timeout_e_convertido_em_erro_seguro`: Conversão de `ReadTimeout` para erro amigável ao cidadão.
7. `test_nao_aceita_saida_sem_choice`: Tratamento de respostas vazias ou truncadas da API.

### 2.3 Gerenciamento de Estado (`tests/test_frontend_state.py` — 3 testes)
1. `test_inicializar_cria_chaves`: Inicialização limpa e idempotente de todas as chaves de sessão.
2. `test_registrar_gera_id_local_e_insere_no_historico`: Criação de código local `LOCAL-XXXXXXXX`, ordenação cronológica e isolamento em memória.
3. `test_registrar_com_correcao_humana`: Rastreamento de alteração humana no resultado da IA (`corrigido=True`) e gravação do feedback de satisfação (`avaliacao_ia`).

### 2.4 Interface e Navegação (`tests/test_frontend_apptest.py` — 3 testes)
1. `test_app_inicializacao`: Verificação de carregamento da tela de relato e elementos do formulário.
2. `test_app_navegacao_painel`: Transição para a tela do Painel Interativo de Relatos.
3. `test_app_navegacao_sobre`: Transição para a tela de Ética, ODS e Arquitetura.

### 2.5 Visualização e Filtros Plotly (`tests/test_visualizacao.py` — 12 testes)
1. `test_exemplos_sao_rotulados_ficticios`: Rotulação obrigatória de dados ilustrativos.
2. `test_filtro_categoria`: Filtragem correta por categoria de problema.
3. `test_filtro_prioridade`: Filtragem correta por prioridades selecionadas.
4. `test_dois_filtros_combinados`: Combinação de categoria e prioridade sem colisão de estado.
5. `test_filtro_por_origem`: Separação entre relatos da sessão e dados de exemplo.
6. `test_filtro_por_bairro`: Filtragem por região/bairro informado.
7. `test_sem_prioridade_nao_mostra_dados`: Estado vazio quando nenhum filtro de prioridade é marcado.
8. `test_contagem_inclui_zeros`: Preservação de contagens zeradas para manter consistência nos eixos dos gráficos.
9. `test_contagem_categoria`: Agrupamento e contagem ordenada por categoria.
10. `test_plotly_prioridades_interativo_com_hover_e_zoom`: Gráfico de barras verticais Plotly com hovertemplate e proporções.
11. `test_plotly_categorias_interativo_com_hover`: Gráfico horizontal de barras Plotly para visualização de volume por tema.
12. `test_plotly_vazio_nao_quebra`: Resiliência do gráfico quando nenhum dado está selecionado.

---

## 3. Evidências Visuais e Comparativo Antes/Depois (Playwright)

As capturas de tela foram geradas automaticamente pelo script `scripts/run_e2e_evidence.py`, que executou os dois serviços reais em portas locais (`8000` e `8501`) e interagiu através do Chromium headless em múltiplos viewports:

| # | Arquivo de Evidência (Depois) | Evidência Anterior (Antes) | Resolução | Melhorias Comprovadas Visualmente |
|---|---|---|:---:|---|
| 1 | [`docs/evidencias/01_desktop_formulario_inicial.png`](file:///c:/Users/thiago.danyluk/Documents/Thiago%20-%20Chiasa/GS2/FRONT/VivaBairro_GS_Frontend_2026_2/VivaBairro_GS2026_2/docs/evidencias/01_desktop_formulario_inicial.png) | `docs/evidencias/antes/01_desktop_formulario_inicial.png` | 1440 × 900 | Remoção de instruções de `.env` e `LLM_PROVIDER`; linguagem focada no cidadão; ícones intactos. |
| 2 | [`docs/evidencias/02_desktop_revisao_human_in_the_loop.png`](file:///c:/Users/thiago.danyluk/Documents/Thiago%20-%20Chiasa/GS2/FRONT/VivaBairro_GS_Frontend_2026_2/VivaBairro_GS2026_2/docs/evidencias/02_desktop_revisao_human_in_the_loop.png) | `docs/evidencias/antes/02_desktop_revisao_human_in_the_loop.png` | 1440 × 900 | Eliminação de `keyboard_arrow_right` como texto; chevron renderizado como ícone; expander sem sobreposição; botões secundários neutros (não vermelhos). |
| 3 | [`docs/evidencias/03_desktop_recibo_confirmacao.png`](file:///c:/Users/thiago.danyluk/Documents/Thiago%20-%20Chiasa/GS2/FRONT/VivaBairro_GS_Frontend_2026_2/VivaBairro_GS2026_2/docs/evidencias/03_desktop_recibo_confirmacao.png) | `docs/evidencias/antes/03_desktop_recibo_confirmacao.png` | 1440 × 900 | Recibo com código local `LOCAL-XXXXXXXX`, aviso institucional sem ambiguidade e botões de direcionamento. |
| 4 | [`docs/evidencias/04_desktop_painel_plotly.png`](file:///c:/Users/thiago.danyluk/Documents/Thiago%20-%20Chiasa/GS2/FRONT/VivaBairro_GS_Frontend_2026_2/VivaBairro_GS2026_2/docs/evidencias/04_desktop_painel_plotly.png) | `docs/evidencias/antes/04_desktop_painel_plotly.png` | 1440 × 900 | 3 filtros combinados; aviso amigável sobre dados simulados; gráficos Plotly com hover rico. |
| 5 | [`docs/evidencias/05_desktop_como_funciona_ods_etica.png`](file:///c:/Users/thiago.danyluk/Documents/Thiago%20-%20Chiasa/GS2/FRONT/VivaBairro_GS_Frontend_2026_2/VivaBairro_GS2026_2/docs/evidencias/05_desktop_como_funciona_ods_etica.png) | `docs/evidencias/antes/05_desktop_como_funciona_ods_etica.png` | 1440 × 900 | Abas de transparência cidadã, ODS 11 e 16, Ética/Limites e decisões de arquitetura. |
| 6 | [`docs/evidencias/06_tablet_formulario.png`](file:///c:/Users/thiago.danyluk/Documents/Thiago%20-%20Chiasa/GS2/FRONT/VivaBairro_GS_Frontend_2026_2/VivaBairro_GS2026_2/docs/evidencias/06_tablet_formulario.png) | `docs/evidencias/antes/06_tablet_formulario.png` | 768 × 1024 | Layout intermediário responsivo sem quebras ou textos cortados. |
| 7 | [`docs/evidencias/07_mobile_responsivo.png`](file:///c:/Users/thiago.danyluk/Documents/Thiago%20-%20Chiasa/GS2/FRONT/VivaBairro_GS_Frontend_2026_2/VivaBairro_GS2026_2/docs/evidencias/07_mobile_responsivo.png) | `docs/evidencias/antes/07_mobile_responsivo.png` | 390 × 844 | Eliminação de `keyboard_double_arrow_right` no botão de menu; `scrollWidth == 390px` (zero overflow horizontal); campos em coluna única. |

---

## 4. Estado do Docker no Ambiente de Teste

- **Instalação:** `Docker versão 29.6.1` e `Docker Compose versão v5.3.0` estão instalados no sistema operacional.
- **Execução do Daemon:** O serviço `Docker Desktop Service (com.docker.service)` encontra-se parado no host. Por se tratar de um ambiente corporativo/acadêmico sem privilégios de Administrador do Windows, o comando de inicialização do serviço (`Start-Service com.docker.service`) não pôde ser executado diretamente por este processo.
- **Validação de Artefatos:** Os arquivos `backend/Dockerfile`, `frontend/Dockerfile` e `docker-compose.yml` foram auditados:
  - Contextos de build e caminhos de cópia rigorosamente validados.
  - Healthchecks HTTP configurados no endpoint `/health`.
  - Dependência entre serviços com `condition: service_healthy`.
  - Isolação de redes e exposição nas portas `8000` (API) e `8501` (Web).
- **Instrução de Execução:** Em máquina com Docker Desktop iniciado:
  ```bash
  docker compose up --build
  ```

---

## 5. Checklist Manual para o Aluno Antes da Submissão Final

- [x] Arquitetura em camadas conferida e separada sem chamadas diretas de IA pelo front-end.
- [x] 45 testes automatizados executando e passando localmente.
- [x] Correção dos ícones de texto (`keyboard_double_arrow_right`, etc.) e preservação estrita de fontes Material Symbols.
- [x] Correção de sobreposição no controle expander ("Ver relato original enviado").
- [x] Remoção de instruções técnicas (`.env`, `LLM_PROVIDER=openai`) das telas públicas voltadas ao cidadão.
- [x] Paleta semântica revisada com vermelho exclusivo para criticidades altas e botões neutros para descarte/ações secundárias.
- [x] Capturas de tela Playwright geradas em Desktop, Tablet e Mobile (comprovando zero overflow horizontal).
- [ ] Inserir chave no arquivo `.env` local (`LLM_PROVIDER=openai`, `OPENAI_API_KEY=...`) e registrar as 3 saídas reais de inferência em `docs/casos_teste_ia.md`.
- [ ] Convidar 3 pessoas do público-alvo para seguir o roteiro de `docs/validacao_usuarios.md` e anotar as impressões.
- [ ] Gravar vídeo de 4m30s seguindo a narrativa em `docs/roteiro_video.md`.
- [ ] Publicar no GitHub público e submeter os links no Portal do Aluno FIAP.
