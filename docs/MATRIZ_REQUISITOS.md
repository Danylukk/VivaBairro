# Matriz Final de Conformidade — GS Front-End em Sistemas de IA 2026.2

**Projeto:** VivaBairro — CitizenTech  
**Data da Auditoria:** 09/11/2026  
**Status Geral:** Código auditado e testado (48 testes pytest, fluxo Docker E2E e evidências visuais de contraste em desktop e mobile).
**Legenda de Status:**
- ✅ **Aprovado:** Implementado em código, coberto por testes automatizados e comprovado por evidências reais.
- 🟡 **Pendente Externo:** Arquitetura pronta e testada em simulação/mock; depende de chave privada do usuário (LLM real) ou participação de pessoas reais (testes com cidadãos).
- ⚠️ **Bloqueado no Ambiente:** Requer privilégios administrativos no host (ex.: inicialização do daemon do Docker Desktop no Windows).

---

## 1. Fluxo CitizenTech e Integração com IA (Valor Máximo: 2,0 pontos)

| Requisito do Enunciado | Status | Arquivo / Função Responsável | Teste Executado | Evidência | Correção Aplicada | Pendência Restante |
|---|---|---|---|---|---|---|
| Entrada com validação (bairro, categoria, descrição) | ✅ Aprovado | `frontend/features/relatar.py`<br>`backend/app/schemas/relatos.py` (`RelatoEntrada`) | `test_exige_descricao_minima`<br>`test_exige_bairro`<br>`test_rejeita_categoria_desconhecida`<br>`test_rejeita_campos_extras`<br>`test_strip_automatico_espacos` | `01_desktop_formulario_inicial.png`<br>`06_tablet_formulario.png` | Inclusão de validação de comprimento (30-900 chars), sanitização de espaços e caracteres não-imprimíveis. | Nenhuma |
| Chamada ao LLM no back-end (FastAPI) sem chamada direta no front-end | ✅ Aprovado | `frontend/providers/api.py` (`enviar_relato`)<br>`backend/app/routers/analises.py`<br>`backend/app/pipelines/analise.py` | `test_fluxo_ponta_a_ponta_simulado`<br>`test_resposta_llm_estruturada_mockada`<br>`test_app_inicializacao` | `backend/app/providers/llm.py`<br>Front-end consome apenas endpoint HTTP `/api/v1/analises`. | Auditoria completa de imports no front-end: nenhuma dependência ou chave de LLM no front-end. | Nenhuma |
| Saída estruturada com schema Pydantic (não apenas texto livre) | ✅ Aprovado | `backend/app/schemas/relatos.py` (`ResultadoIA`)<br>`backend/app/providers/llm.py` | `test_provedor_retorna_pydantic_valido`<br>`test_saida_ia_invalida_e_rejeitada`<br>`test_provedor_aceita_saida_com_markdown_fences` | `schemas/relatos.py:ResultadoIA`<br>JSON Schema injetado no prompt do sistema. | Adicionada função `limpar_json_resposta` para tratar saídas do LLM envolvidas em blocos markdown (` ```json `). | Nenhuma |
| Resposta útil ao cidadão (orientação, prioridade, encaminhamento) | ✅ Aprovado | `frontend/features/relatar.py`<br>`backend/app/pipelines/analise.py` | Execução E2E com Playwright em fluxo completo de análise. | `02_desktop_revisao_human_in_the_loop.png` | Reestruturação dos blocos visuais: resumo, justificativa da criticidade, orientação de segurança e tipo de serviço municipal. | Nenhuma |
| Conexão com LLM real com credenciais seguras | ✅ Validado em 09/11/2026 | `backend/app/providers/llm.py` (`analisar_openai`)<br>`backend/app/config.py` | 3 chamadas externas reais com modelo configurado `gpt-4o-mini`, respostas Pydantic válidas; testes mock existentes continuam complementares | `docs/relatorio_validacao_llm_real_20261109.md`<br>`docs/evidencias/llm_real_20261109_173040.json` | A terceira entrada foi corrigida de `Sé` para `Bairro da Sé` para atender ao schema; executada apenas uma chamada adicional após 2 anteriores bem-sucedidas. | Não extrapolar o resultado a outros relatos; validação de usabilidade com pessoas continua pendente. |

---

## 2. Arquitetura e Estrutura de Código (Valor Máximo: 2,0 pontos)

| Requisito do Enunciado | Status | Arquivo / Função Responsável | Teste Executado | Evidência | Correção Aplicada | Pendência Restante |
|---|---|---|---|---|---|---|
| Front-end dividido em `features/`, `ui/`, `state/`, `providers/` | ✅ Aprovado | `frontend/features/`<br>`frontend/ui/`<br>`frontend/state/`<br>`frontend/providers/` | `test_frontend_state.py`<br>`test_frontend_apptest.py` | Estrutura de diretórios em `frontend/` com responsabilidades isoladas. | Eliminação de acoplamento entre telas; centralização do store em `frontend/state/store.py`. | Nenhuma |
| Back-end dividido em `routers/`, `schemas/`, `pipelines/`, `providers/` | ✅ Aprovado | `backend/app/routers/`<br>`backend/app/schemas/`<br>`backend/app/pipelines/`<br>`backend/app/providers/` | `test_api.py`<br>`test_provider.py` | Estrutura de diretórios em `backend/app/`. | Pipelines desacoplados de transporte HTTP; providers isolados de regras de negócio. | Nenhuma |
| Proibição de arquivos monolíticos | ✅ Aprovado | Todo o repositório | Inspeção estrutural de código e contagem de linhas por módulo. | Nenhum arquivo ultrapassa responsabilidade única. | Separação de temas, componentes reutilizáveis, contratos Pydantic e lógicas de visualização. | Nenhuma |

---

## 3. Estado, Performance e Robustez (Valor Máximo: 1,5 pontos)

| Requisito do Enunciado | Status | Arquivo / Função Responsável | Teste Executado | Evidência | Correção Aplicada | Pendência Restante |
|---|---|---|---|---|---|---|
| Uso correto de `st.session_state` sem perda de histórico em reruns | ✅ Aprovado | `frontend/state/store.py`<br>`frontend/app.py` | `test_inicializar_cria_chaves`<br>`test_registrar_gera_id_local_e_insere_no_historico`<br>`test_app_navegacao_painel` | `03_desktop_recibo_confirmacao.png`<br>`04_desktop_painel_plotly.png` | Corrigido bug de colisão de chave do `st.radio` usando `redirecionar_pagina` antes da renderização do widget. | Nenhuma |
| Uso de `@st.cache_data` sem expor dados privados de cidadãos | ✅ Aprovado | `frontend/providers/api.py` (`obter_status`) | Testes de cache e ausência de cache em `enviar_relato`. | `api.py:obter_status` possui `@st.cache_data(ttl=20)`; `enviar_relato` não possui cache. | Garantido que apenas checagem de saúde da API é cacheada. | Nenhuma |
| Tratamento de falhas (API fora do ar, timeout, resposta inválida) | ✅ Aprovado | `frontend/providers/api.py`<br>`backend/app/routers/analises.py` | `test_erro_llm_nao_vaza_detalhe`<br>`test_timeout_e_convertido_em_erro_seguro`<br>`test_rejeita_resposta_invalida` | Exibição de mensagens com `st.error` amigável sem stack trace ao usuário. | Mapeamento de `ConnectError`, `TimeoutException` e `HTTPStatusError` para `ErroAmigavel`. | Nenhuma |
| Proteção de segredos (chaves de API) | ✅ Aprovado | `.env.example`<br>`.gitignore`<br>`backend/app/config.py` | `test_requer_segredo_para_ia`<br>Inspeção do repositório Git. | Nenhuma chave nos arquivos versionados; `.env` presente no `.gitignore`. | Remoção de qualquer valor hardcoded; validação estrita no boot da aplicação. | Nenhuma |
| CORS restritivo e seguro | ✅ Aprovado | `backend/app/main.py`<br>`backend/app/config.py` | `test_cors_permitido`<br>`test_cors_estranho_sem_cabecalho_liberacao`<br>`test_proibe_cors_global_em_producao` | Headers CORS inspecionados em requisições OPTIONS. | Bloqueio de `*` em ambiente de produção; liberação estrita para porta do Streamlit. | Nenhuma |
| Resiliência a Prompt Injection e XSS | ✅ Aprovado | `backend/app/schemas/relatos.py`<br>`backend/app/providers/llm.py` | `test_resiliencia_tentativa_prompt_injection`<br>`test_resiliencia_caracteres_xss_e_html`<br>`test_rejeita_caracteres_controle_invalidos` | Relatos maliciosos tratados puramente como texto, sem execução ou desvio de regras. | Prompt de sistema reforçado contra injeção e descarte de instruções dentro do relato. | Nenhuma |

---

## 4. UX/UI Centrada no Cidadão, Acessibilidade e Visualização (Valor Máximo: 2,0 pontos)

| Requisito do Enunciado | Status | Arquivo / Função Responsável | Teste Executado | Evidência | Correção Aplicada | Pendência Restante |
|---|---|---|---|---|---|---|
| Layout organizado com tabs, colunas e sidebar | ✅ Aprovado | `frontend/app.py`<br>`frontend/features/painel.py`<br>`frontend/features/sobre.py` | Testes de navegação `AppTest` e Playwright em 3 viewports. | `01_desktop_formulario_inicial.png`<br>`04_desktop_painel_plotly.png`<br>`05_desktop_como_funciona_ods_etica.png` | Reorganização das telas em seções de fácil leitura, com linguagem direta e sem jargões. | Nenhuma |
| Design para latência e estados vazios/erros | ✅ Aprovado | `frontend/features/relatar.py`<br>`frontend/features/painel.py` | E2E Playwright verificando spinners e mensagens de estado vazio. | `st.spinner` durante chamada HTTP; cards de estado vazio informativos com botão de demonstração. | Ajuste visual dos alertas e spinners para cidadãos comuns. | Nenhuma |
| Cores semânticas com apoio de texto/ícone (WCAG 2.2 AA) | ✅ Aprovado | `frontend/ui/components.py`<br>`frontend/ui/theme.py`<br>`frontend/visualization.py` | Verificação de contraste de cores (todas as cores possuem taxa > 4.5:1). | `faixa_prioridade` combina cor semântica + ícone (🔴, 🟠, 🟢) + texto explícito. | Substituição de cores de baixo contraste por tons aprovados WCAG AA (`#b91c1c`, `#b45309`, `#15803d`). | Nenhuma |
| Foco visível e responsividade (Desktop, Tablet e Mobile) | ✅ Aprovado | `frontend/ui/theme.py`<br>`frontend/app.py` | Captura Playwright em 1440x900 (Desktop), 768x1024 (Tablet) e 390x844 (Mobile). | `01_desktop_formulario_inicial.png`<br>`06_tablet_formulario.png`<br>`07_mobile_responsivo.png` | Adicionado `:focus-visible` com anel de 3px e `initial_sidebar_state="auto"` para colapso automático em smartphones. | Nenhuma |
| Human-in-the-Loop funcional (conferência, edição e descarte) | ✅ Aprovado | `frontend/features/relatar.py`<br>`frontend/state/store.py` | `test_registrar_com_correcao_humana`<br>E2E Playwright de revisão e confirmação. | `02_desktop_revisao_human_in_the_loop.png`<br>`03_desktop_recibo_confirmacao.png` | Inclusão de campos editáveis (categoria, prioridade, resumo), opção de descarte e avaliação da IA ("Sim, adequada", "Incorreta"). | Nenhuma |
| Pelo menos 1 gráfico Plotly interativo (hover e zoom) | ✅ Aprovado | `frontend/visualization.py`<br>`frontend/features/painel.py` | `test_plotly_prioridades_interativo_com_hover_e_zoom`<br>`test_plotly_categorias_interativo_com_hover` | `04_desktop_painel_plotly.png`<br>Gráfico por prioridade e gráfico horizontal por categoria. | Implementação de dois gráficos Plotly interativos com `hovertemplate` detalhado e controle de zoom. | Nenhuma |
| Pelo menos 2 filtros que alteram efetivamente a exibição | ✅ Aprovado | `frontend/features/painel.py`<br>`frontend/visualization.py` | `test_filtro_categoria`<br>`test_filtro_prioridade`<br>`test_dois_filtros_combinados`<br>`test_filtro_por_origem` | 3 filtros implementados: Categoria (Selectbox), Prioridade (Multiselect) e Tipo de Relato (Selectbox). | Implementado 3 filtros combináveis que reagem em tempo real sobre os gráficos e tabela. | Nenhuma |
| Componentização real de UI reutilizada em múltiplos contextos | ✅ Aprovado | `frontend/ui/components.py` | Usado em `relatar.py`, `painel.py` e `sobre.py`. | `cabecalho` reutilizado em 3 telas; `card_metrica` reutilizado no recibo e no painel de indicadores com diferentes parâmetros. | Implementação e parametrização de componentes modulares reutilizáveis. | Nenhuma |

---

## 5. Deploy e Repositório (Valor Máximo: 1,0 ponto)

| Requisito do Enunciado | Status | Arquivo / Função Responsável | Teste Executado | Evidência | Correção Aplicada | Pendência Restante |
|---|---|---|---|---|---|---|
| Repositório Git configurado | ✅ Aprovado | `.git/`<br>Branch `feature/auditoria-e-finalizacao-gs2026-2` | Comandos `git status` e `git log`. | Histórico de commits estruturado e isolamento de arquivos. | Repositório local inicializado com commit de baseline e branch de trabalho. | Envio ao GitHub público pelo aluno antes do prazo. |
| Dockerfiles e docker-compose.yml funcionais | ✅ Aprovado | `backend/Dockerfile`<br>`frontend/Dockerfile`<br>`docker-compose.yml`<br>`scripts/test_docker_e2e.py` | `docker compose config`, `docker compose build`, `docker compose up -d`, `scripts/test_docker_e2e.py` | Containers `api` e `web` executados com status `healthy`; validação E2E via Playwright realizada com sucesso diretamente contra os containers ativos. | Configuração rigorosa de variáveis de ambiente, portas (8000 e 8501), healthcheck HTTP e comunicação inter-serviços. | Nenhuma (comprovado por execução real). |
| Arquivos de dependências e configuração | ✅ Aprovado | `backend/requirements.txt`<br>`frontend/requirements.txt`<br>`.env.example` | `pip install` e execução de testes. | Arquivos revisados sem dependências conflitantes. | Alinhamento de dependências com versões compatíveis. | Nenhuma |

---

## 6. Justificativa, Validação e Impacto Social (Valor Máximo: 1,5 pontos)

| Requisito do Enunciado | Status | Arquivo / Função Responsável | Teste Executado | Evidência | Correção Aplicada | Pendência Restante |
|---|---|---|---|---|---|---|
| Fundamentação do problema e público-alvo com fontes reais | ✅ Aprovado | `README.md` §1<br>`frontend/features/sobre.py` | Verificação das fontes da Prefeitura de SP (SP156) e Cartas de Serviços. | Links oficiais documentados no README e na interface. | Inclusão de referências verificáveis do SP156 sem falsa afirmação de integração direta. | Nenhuma |
| Relação com ODS 11 e ODS 16 fundamentada | ✅ Aprovado | `README.md` §1<br>`frontend/features/sobre.py` | Verificação dos textos e metas da ONU Brasil (Meta 11.7 e Meta 16.6). | Aba temática "🎯 ODS e Impacto Social" no sistema. | Justificativa detalhada de como organizar relatos urbanos apoia cidades sustentáveis e transparência institucional. | Nenhuma |
| Decisões técnicas e limites éticos documentados | ✅ Aprovado | `README.md` §§3, 6-8<br>`frontend/features/sobre.py` | Revisão dos critérios de viés, alucinação, vazamento de dados e Human-in-the-Loop. | Aba temática "⚖️ Ética e Limites da IA" e documentação técnica. | Descrição detalhada de mitigação para cada risco e explicitação do que o protótipo não faz. | Nenhuma |
| Validação com 3 participantes reais (P1, P2, P3) | 🟡 3 avaliações externas reportadas | `docs/validacao_usuarios.md` | O aluno transmitiu feedbacks de três participantes externos: P1 observou excesso de informação na revisão; P2 utilizou sem dificuldades e achou a proposta pertinente; P3 utilizou sem dúvidas, mas achou o protótipo simples e não demonstrou interesse. A autoavaliação do integrante está separada. | Relato anonimizado e capturas técnicas antes/depois em `docs/evidencias/feedback_usabilidade_20261113/`. | Simplificação da revisão com detalhes expansíveis, preservando alertas de risco e decisão humana; Playwright desktop/mobile aprovado. | Três feedbacks externos relatados; reavaliação qualitativa positiva de P1 após a simplificação registrada. Vídeo MP4 silencioso de 4min35s produzido; confirmar formato de envio e realizar submissão. |
| 3 Casos de teste de IA com entrada, saída e ajuste | ✅ Executado em 09/11/2026 | `docs/casos_teste_ia.md`, `docs/relatorio_validacao_llm_real_20261109.md` | Três chamadas reais ao LLM registradas e revisadas (incluindo correção de fixture inválida). | `docs/evidencias/llm_real_20261109_173040.json` e relatório correspondente. | Critérios de validação Pydantic e análise qualitativa documentados. | Nenhuma chamada adicional autorizada; não executar novamente sem autorização. |
| Vídeo demonstrativo de até 5 minutos | ✅ MP4 produzido (04:35) | `docs/roteiro_video.md`, `docs/video/VivaBairro_GS2026_2_Demo_SemAudio.mp4` | Captura da aplicação em modo demonstração; cenas de registro, revisão humana, recibo, painel, ODS, arquitetura, evidências e melhoria baseada em feedback. | Vídeo H.264 1600×900 sem áudio, duração 4min35s. | Edição com títulos/legendas curtas, identificação clara de inferência local e integração real validada separadamente. | Confirmar aceitação de vídeo sem narração; disponibilizar link no canal exigido e enviar. |

---

## Correção de contraste do tema visual — 09/11/2026

**Defeito identificado pela captura do aluno:** a preferência escura do navegador/sistema ativava elementos nativos do Streamlit em modo escuro, enquanto o CSS personalizado mantinha algumas cores do modo claro. Resultado: fundo escuro com texto escuro na área principal e fundo claro com texto quase branco na barra lateral.

**Correções:** o arquivo `.streamlit/config.toml` fixa uma paleta clara coerente para o Streamlit; `frontend/Dockerfile` copia essa configuração para o contêiner; `frontend/ui/theme.py` alinha o fundo principal e preserva o contraste.

**Teste no navegador:** `python -m scripts.validar_tema_e2e`. Foram verificados desktop em sistema claro (1440×900), desktop em sistema escuro (1440×900) e celular em sistema escuro (390×844). Resultado: contraste do título principal de **17,9:1**, título da barra lateral de **17,1:1** e ausência de transbordamento horizontal nos três cenários.

**Capturas após a correção:** `docs/evidencias/09_tema_contraste_desktop_claro.png`, `docs/evidencias/09_tema_contraste_desktop_sistema_escuro.png` e `docs/evidencias/09_tema_contraste_mobile_sistema_escuro.png`.

**Regressão:** 47 testes pytest passaram; o fluxo Playwright Docker passou (formulário, API, revisão humana, recibo, painel Plotly, mobile). Os contêineres continuaram em modo de demonstração, sem chamadas novas à OpenAI.

**Integridade acadêmica:** esta correção foi motivada pela captura enviada pelo aluno. Não representa a melhoria obrigatória a ser realizada com base no feedback dos três participantes reais, que permanece pendente.

---

## Reavaliação de usabilidade técnica — 13/11/2026

Relatório completo: [`relatorio_usabilidade_simulada_20261113.md`](relatorio_usabilidade_simulada_20261113.md).

Foram executadas três jornadas automatizadas com personas fictícias em navegador (nenhum participante humano). A primeira detectou rejeição indevida do bairro **Sé**; o schema Pydantic e a validação da interface foram corrigidos para aceitar nomes com dois caracteres. A interface também ganhou aviso explícito de que o recibo local não é protocolo oficial, próximo da confirmação e do próprio recibo.

**Evidências:** `docs/evidencias/usabilidade_simulada/antes` e `depois` (capturas e arquivos JSON). O bairro Sé foi rejeitado antes e aceito depois; os cenários mobile e revisão humana passaram nas duas fases. Nova regressão local: **48 testes pytest aprovados**; os três testes visuais de contraste passaram. O Docker não foi reexecutado nesta data porque o daemon estava indisponível; os testes E2E ocorreram com FastAPI/Streamlit locais em modo demo.

**Limitação:** a execução por cenários não substitui os três participantes reais exigidos pelo professor. Não atribuir dificuldades, feedback ou entrevistas a pessoas inexistentes.
