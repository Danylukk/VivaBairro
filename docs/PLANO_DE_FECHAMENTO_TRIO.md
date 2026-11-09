# Plano de fechamento — trio — GS Front-end 2026.2

**Estado observado em 09/11/2026:** o projeto local existe na branch `feature/auditoria-e-finalizacao-gs2026-2`; não havia `.env`, variável de chave disponível no processo nem `git remote` configurado. A disponibilidade da chave pessoal foi informada pelo aluno, mas **não significa que já esteja instalada no projeto**.

**Prazo geral:** 19/11/2026 às 23h55, pelo Portal do Aluno. **Não afirmar nota prevista como garantida.**

## Divisão sugerida (nomes dos integrantes ainda não informados)

| Responsável | Entrega | Evidência de conclusão |
|---|---|---|
| Integrante A — integração e testes | Configurar secretamente `.env`, validar três inferências reais, revisar respostas, executar `pytest` e Docker | `docs/evidencias/llm_real_*.json`, testes e logs sem segredos |
| Integrante B — usabilidade | Convidar participantes P1, P2 e P3; conduzir sessões de 10–15 min; registrar dificuldades **reais** | Registros preenchidos neste documento ou `docs/validacao_usuarios.md` |
| Integrante C — entrega | Consolidar README, revisar vídeo (até 5 min), conferir repositório GitHub e links | Link público correto, vídeo gravado e enviado, README final |

Os três integrantes devem conhecer o funcionamento do sistema e contribuir com a apresentação. Esta divisão é uma sugestão, não um relato de trabalho já realizado.

## 1. Integrar LLM real

1. Na raiz do projeto, copie `.env.example` para `.env`.
2. Em `.env`, configure `LLM_PROVIDER=openai` e `OPENAI_API_KEY` com a chave **no seu computador**. Não envie a chave por mensagens, GitHub ou captura de tela.
3. Antes de consumir a API, confira limite e disponibilidade de créditos na conta.
4. Verifique a preparação sem custo: `python -m scripts.validar_llm_real`.
5. Com autorização de uso e chave correta, execute: `python -m scripts.validar_llm_real --executar`.
6. O script realiza **no máximo três chamadas**, grava apenas entradas fictícias e respostas em `docs/evidencias/llm_real_*.json`. Não grava a chave.
7. Leia as respostas, compare esperado/obtido e registre eventuais ajustes reais em `docs/casos_teste_ia.md`. Pydantic válido não garante resposta correta.
8. Antes de qualquer publicação, revise o JSON de evidências.

**Situação atual:** execução real não realizada por ausência da chave no ambiente do projeto.

## 2. Realizar testes com três participantes reais

- Convidar **três adultos distintos** com diferentes níveis de familiaridade digital. O usuário informou dispor inicialmente de uma ou duas pessoas; **a terceira ainda precisa ser encontrada**.
- Pedir consentimento para participação, explicar que é POC e usar apenas relatos fictícios. Não registrar nome, CPF, telefone, foto do rosto ou endereço residencial.
- Cada participante deve completar o roteiro em `docs/validacao_usuarios.md` sem instruções detalhadas do facilitador.
- Registrar: data, código P1/P2/P3, faixa etária aproximada (opcional), familiaridade digital, tarefas concluídas, dificuldades concretas, sugestão espontânea e necessidade de ajuda.
- Depois dos três testes: **escolher uma dificuldade real**, implementar melhoria no código, capturar antes/depois e retestar. Não atribuir melhorias anteriores a feedback inexistente.

### Registro rápido por participante (deixe em branco até testar)

| ID | Data | Familiaridade digital | Conclusão das tarefas | Dificuldade observada | Sugestão real | Precisou de ajuda? |
|---|---|---|---|---|---|---|
| P1 | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE |
| P2 | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE |
| P3 | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE |

### Melhoria derivada de feedback (não preencher antecipadamente)

- Dificuldade real:
- Participante(s) que a observaram:
- Arquivo e alteração aplicada:
- Evidência antes/depois:
- Teste pós-melhoria e resultado:

## 3. GitHub e entrega

- Git está configurado localmente; em 09/11/2026 **não havia remoto**.
- Conta no GitHub foi informada como existente, porém o repositório `VivaBairro` não foi encontrado entre os repositórios acessíveis na conexão consultada.
- Escolher **um** repositório público do trio com os arquivos finais na branch padrão; nunca publicar `.env`.
- Publicação pública deve ser autorizada pelo proprietário; verificar GitHub e README após o push.
- No Portal FIAP, enviar link real do repositório e vídeo de até cinco minutos (YouTube não listado ou arquivo permitido no repositório).

## 4. Vídeo do trio

- Usar roteiro em `docs/roteiro_video.md`, ajustando para aproximadamente 4min30s.
- Mostrar: contexto/ODS, entrada, análise real (se validada), latência, revisão humana, confirmação, Plotly/filtros, erro tratado, arquitetura e testes.
- Só declarar testes humanos, chamadas LLM e links publicados depois de concluídos.
- Evitar qualquer `.env`, token ou dados privados na gravação.

## 5. Integração com outras disciplinas

**Decisão em aberto informada pelo grupo.** Antes de gravar a introdução, alinhar se VivaBairro será apenas a POC da disciplina de Front-end ou parte de solução integrada da GS. Não criar integrações novas sem decisão do trio.

## 6. Critérios para fechamento

- [ ] Três casos de LLM real executados e avaliados
- [ ] Três participantes reais testaram o sistema
- [ ] Uma melhoria comprovada após feedback humano
- [ ] Testes automatizados executados após a melhoria
- [ ] GitHub público publicado e verificado
- [ ] Vídeo real gravado e link verificado
- [ ] Integração com outras disciplinas decidida pelo trio
- [ ] Links submetidos no Portal FIAP
