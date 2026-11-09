# Roteiro de Gravação do Vídeo de Apresentação (Até 5 Minutos)

**Meta de Duração:** 4 minutos e 30 segundos (margem de segurança abaixo do teto de 5 minutos).  
**Formato de Entrega:** Vídeo no YouTube (configurado como **Não Listado**) ou arquivo de vídeo no repositório.  
**Dica de Gravação:** Use OBS Studio, Loom ou gravação nativa do Windows (`Win + G` / Ferramenta de Captura). Mantenha a fonte do navegador ampliada (110% de zoom) e áudio limpo.

---

## ⏱️ Cronograma e Roteiro Passo a Passo

| Tempo Estimado | Tela / Ação Visual | Narrativa do Apresentador (O Que Falar) |
|---|---|---|
| **0:00 – 0:40** | **Capa do VivaBairro + Tela Inicial** (`http://localhost:8501`) | *"Olá, professor e avaliadores. Apresentamos o **VivaBairro**, uma solução CitizenTech desenvolvida para a Global Solution 2026.2 da FIAP. Nosso objetivo é enfrentar uma dor real dos moradores das cidades: a dificuldade de relatar problemas urbanos de zeladoria — como calçadas inacessíveis, buracos e falhas de iluminação — e entender como esses relatos podem ser priorizados e orientados sem jargões técnicos. Tomamos como evidência da dor as cartas de serviços do serviço municipal oficial SP156."* |
| **0:40 – 1:10** | **Aba 'Como Funciona' (ODS 11 e 16)** | *"A solução alinha-se diretamente a dois Objetivos de Desenvolvimento Sustentável da ONU: o **ODS 11 (Cidades e Comunidades Sustentáveis)**, ao apoiar a remoção de barreiras urbanas e espaços seguros, e o **ODS 16 (Paz, Justiça e Instituições Eficazes)**, ao estudar a transparência e a organização de informações cidadãs. Ressaltamos que o VivaBairro é uma Prova de Conceito acadêmica e não substitui os canais oficiais da Prefeitura."* |
| **1:10 – 2:05** | **Tela 'Fazer Relato' (Entrada + Latência + Resposta IA)** | *"Demonstrando o fluxo de ponta a ponta: o cidadão informa o bairro 'Lapa', seleciona a categoria preliminar e descreve o obstáculo na calçada. O front-end valida o tamanho e não permite dados vazios. Ao clicar em 'Analisar', visualizamos o spinner de latência. O front-end envia um JSON via HTTP para nossa API FastAPI, que orquestra a chamada ao modelo de IA e devolve um schema Pydantic estruturado. A interface exibe a prioridade com cor semântica e ícone (🔴 Alta), justificativa, resumo e orientação segura ao munícipe."* |
| **2:05 – 2:45** | **Human-in-the-Loop + Confirmação** | *"Aqui está o diferencial do **Human-in-the-Loop**: a IA não toma decisões finais sozinha. O morador confere a sugestão, pode editar a categoria, ajustar a prioridade, refinar o resumo e avaliar a qualidade da IA. Ao clicar em confirmar, geramos o código local `LOCAL-XXXXXXXX`, com aviso explícito de que não é protocolo oficial municipal, armazenando o dado exclusivamente na sessão atual."* |
| **2:45 – 3:30** | **Painel de Relatos (Plotly + 3 Filtros)** | *"Avançando para o Painel de Relatos: os dados confirmados alimentam nossos gráficos interativos em **Plotly**. Podemos interagir com hover para ver proporções e utilizar zoom dinâmico. Temos 3 filtros ativos: Categoria, Prioridade e Tipo de Relato, que atualizam em tempo real tanto os cards de métricas reutilizáveis quanto a tabela detalhada de registros."* |
| **3:30 – 4:05** | **Cenário de Erro Tratado + Robustez** | *"Para comprovar a resiliência e tratamento de falhas, simulamos a API offline ou um erro de rede: a interface exibe um alerta claro e amigável ao cidadão, sem expor mensagens técnicas indecifráveis nem stack traces. Os segredos e chaves de API nunca são expostos no front-end nem no navegador."* |
| **4:05 – 4:35** | **Arquitetura no VS Code + Autoria do Código** | *(Alternar rapidamente para o VS Code)*<br>*"Comprovando a autoria do projeto e a arquitetura exigida: no front-end temos `features/`, `ui/` com componentes reutilizáveis, `state/` com store e `providers/` com o cliente HTTP, sem nenhuma chamada direta ao LLM. No back-end FastAPI temos `routers/`, `schemas/` Pydantic, `pipelines/` de orquestração e `providers/` com a chamada isolada ao modelo de linguagem. O cache com `@st.cache_data` é usado estritamente no health check, preservando a privacidade dos relatos."* |
| **4:35 – 4:55** | **Evidências de Validação e Encerramento** | *"Apresentamos em nossa documentação a suíte com 45 testes automatizados aprovados no Pytest, os testes no navegador com Playwright em Desktop, Tablet e Mobile, e as evidências de validação. O VivaBairro demonstra como a inteligência artificial combinada à revisão humana e ao bom design de software pode empoderar o cidadão nas cidades. Muito obrigado!"* |

---

## 📌 Checklist de Gravação

1. O navegador está com as abas preparadas: `Fazer relato`, `Painel de relatos` e `Como funciona`.
2. O Uvicorn e o Streamlit estão rodando.
3. Não há arquivos `.env` ou senhas abertas no editor durante a gravação.
4. O tempo total está rigorosamente abaixo de 5 minutos.
5. O link gerado no YouTube está com visibilidade **Não Listado** (*Unlisted*).
