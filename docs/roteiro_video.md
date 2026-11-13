# Roteiro final do vídeo — VivaBairro | GS 2026.2

**Duração-alvo:** 4min30s (270 segundos). **Limite do professor:** 5 minutos.
**Equipe:** trio, sem nomes definidos neste documento.
**Situação:** vídeo demonstrativo silencioso produzido em 13/11/2026, com duração de **4min35s**. O roteiro narrado abaixo permanece como alternativa caso a instituição exija apresentação oral. O vídeo sem áudio apresenta a explicação por títulos e legendas curtas e sinaliza explicitamente o modo de demonstração.

| Tempo | Integrante sugerido | Tela / demonstração | Fala-base objetiva |
|---|---|---|---|
| 0:00–0:25 | A | Tela inicial | "Apresentamos o VivaBairro, uma POC CitizenTech da FIAP 2026.2. Ela ajuda moradores a descrever problemas urbanos, como calçadas danificadas e iluminação pública, de maneira clara. Não é um serviço oficial da Prefeitura." |
| 0:25–0:45 | A | Como funciona / ODS | "A proposta se relaciona ao ODS 11, pelos espaços públicos acessíveis, e ao ODS 16, pela organização e clareza das informações cidadãs. O SP156 é uma referência de serviço oficial, sem integração com nossa POC." |
| 0:45–1:30 | A | Formulário e análise | "O cidadão informa bairro, categoria e descrição. A aplicação valida o preenchimento, mostra o carregamento e envia o relato por HTTP ao FastAPI. O back-end processa a análise e devolve os campos validados por Pydantic." **Se a inferência REAL estiver validada, demonstrar e dizer o modelo real; caso contrário, apresentar claramente o modo simulado e sua limitação.** |
| 1:30–2:05 | B | Revisão humana e recibo | "Antes de confirmar, o cidadão pode corrigir prioridade, categoria e resumo. Essa é a revisão humana: o sistema não decide sozinho. Após confirmar, gera um código apenas local, sem abrir solicitação na Prefeitura." |
| 2:05–2:40 | B | Painel de relatos | "O painel utiliza Plotly e mostra os relatos confirmados e os exemplos identificados. Os filtros de categoria, prioridade e origem atualizam gráficos, indicadores e tabela." Demonstrar filtros e hover. |
| 2:40–3:00 | B | Erro tratado | "Quando a API está indisponível, mostramos uma orientação clara, sem detalhes técnicos ou exposição de chaves. O cidadão pode tentar novamente." Preparar erro de forma segura antes de gravar. |
| 3:00–3:45 | C | VS Code / estrutura do projeto | "O front-end usa features, ui, state e providers; o back-end usa routers, schemas, pipelines e providers. A comunicação é via FastAPI, o estado do Streamlit mantém o histórico e o cache evita chamadas desnecessárias. As credenciais permanecem fora do Git." |
| 3:45–4:15 | C | Terminal / evidências | "Validamos a arquitetura com testes automatizados e executamos a aplicação em Docker. A documentação registra o resultado dos testes e os cenários de IA." **Somente se as sessões humanas ocorrerem:** apresentar observação real e ajuste implementado. **Somente se LLM real foi executado:** apresentar os 3 resultados reais. |
| 4:15–4:30 | C | Encerramento | "O VivaBairro demonstra o potencial da tecnologia acessível para apoiar o cidadão, sempre com revisão humana e transparência sobre suas limitações. Obrigado." |

## Preparação para a gravação

1. Confirmar qual integrante será A, B e C; ajustar a narração para falas naturais de cada um.
2. Testar a aplicação e preparar um relato **fictício**.
3. Configurar LLM real e registrar resultados, se disponível; nunca apresentar modo demo como IA real.
4. Completar os testes com três participantes e uma melhoria de código antes de afirmar essas evidências.
5. Abrir navegador, VS Code (sem `.env`) e terminal (sem tokens/credenciais); usar zoom legível.
6. Gravar e conferir duração **inferior a 5:00**, áudio, fluidez e informações corretas.
7. Publicar no YouTube como **não listado** ou disponibilizar arquivo na forma aceita pelo professor, e inserir link real no README.

**Arquivo pronto:** [VivaBairro_GS2026_2_Demo_SemAudio.mp4](video/VivaBairro_GS2026_2_Demo_SemAudio.mp4). Duração verificada: 04:35. Vídeo H.264 1600×900, sem trilha de áudio. O arquivo está no repositório; não foi publicado no YouTube. Verificar se a disciplina exige narração dos integrantes ou link de publicação externa.
