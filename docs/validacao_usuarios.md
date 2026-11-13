# Validação de usabilidade — protocolo e feedbacks reais

**Projeto:** VivaBairro — Global Solution 2026.2
**Atualização:** 13/11/2026
**Objetivo:** observar facilidade de uso, compreensão da sugestão, clareza das informações, segurança da revisão humana e localização dos dados no painel.

## Metodologia e transparência

Este documento mantém o protocolo para três participantes externos e registra **somente feedbacks efetivamente informados pelo aluno**. A avaliação por personas e Playwright está em [relatorio_usabilidade_simulada_20261113.md](relatorio_usabilidade_simulada_20261113.md) e **não conta como pesquisa com pessoas**.

- **Privacidade:** usar apenas identificadores P1, P2 e P3; não coletar CPF, telefone, endereço, fotos de rosto nem outros dados identificadores.
- **Contexto:** esclarecer que o VivaBairro é um projeto acadêmico e não envia demandas à Prefeitura. Os relatos dos testes devem ser fictícios.
- **Realização:** pedir que o participante descreva um problema, revise a análise e encontre o registro no painel; evitar orientá-lo sobre onde clicar, exceto quando necessário para destravar.
- **Coleta:** registrar tarefas concluídas, dificuldades observadas, comentários espontâneos, recomendações, eventual intervenção do mediador e data.

## Feedbacks recebidos

| Identificador | Origem da avaliação | Resultado comunicado | Dificuldade ou sugestão |
|---|---|---|---|
| **A0 — Autoavaliação** | Integrante do grupo, informada por ele na conversa | Experiência fácil, boa, intuitiva e adequada ao próprio uso; nenhuma dificuldade relatada | Nenhuma sugestão reportada. **Autoavaliação não contabilizada como participante externo.** |
| **P1 — Pessoa externa** | Feedback da participante transmitido pelo aluno em 13/11/2026 | Nenhuma dificuldade de utilização relatada; avaliou positivamente a ideia e o sistema funcionando; percebe potencial | **Excesso de informações na tela**, especialmente na etapa de revisão exibida nas capturas compartilhadas. Sugeriu simplificar a experiência. |
| **P2 - Pessoa externa** | Feedback do participante transmitido pelo aluno em 13/11/2026 | Considerou que o projeto faz sentido e conseguiu utilizá-lo normalmente, sem dificuldades relatadas. | Nenhuma sugestão específica foi informada. |
| **P3 - Pessoa externa** | Feedback do participante transmitido pelo aluno em 13/11/2026 | Utilizou o VivaBairro normalmente, sem dificuldades de uso, dúvidas sobre as funcionalidades ou necessidade de orientação técnica relatadas. | Não demonstrou interesse pelo projeto e considerou a solução **simples**. O integrante explicou que se trata de uma versão acadêmica inicial, que poderá evoluir futuramente. Nenhuma funcionalidade específica foi sugerida. |

**Limites dos dados:** não foram informados duração, idade, taxa de acerto, sequência completa de tarefas nem se P1 explorou todos os filtros do painel. Portanto, nenhuma dessas informações foi presumida. O relato sobre P1 é **indireto, fornecido pelo aluno**, e as capturas mostram a interface em revisão, não observações comportamentais de uma sessão gravada.

**Síntese qualitativa:** nos três relatos externos não foram comunicadas dificuldades operacionais. P1 trouxe uma sugestão concreta de redução da quantidade de informações, implementada e aprovada por ela na reavaliação. P2 considerou a proposta pertinente. P3 criticou a simplicidade e não demonstrou interesse, o que representa uma **percepção sobre escopo e atratividade**, e não um defeito de usabilidade demonstrado. Essa crítica pode orientar estudos de evolução do produto, mas não justifica criar funcionalidades não solicitadas na entrega atual.

## Melhoria implementada a partir do feedback de P1

**Problema apontado:** grande volume de textos, avisos e cartões no mesmo momento da revisão humana; isso aumenta a carga de leitura para quem está apenas tentando conferir o resultado e continuar.

**Solução implementada em `frontend/features/relatar.py`:**

1. A etapa de revisão apresenta prioritariamente **classificação, risco, orientação essencial e os controles para corrigir e confirmar**.
2. A justificativa, encaminhamento, resumo anterior e relato original passaram a ficar sob **“Ver justificativa e informações adicionais”**, acessíveis por expansão voluntária.
3. O aviso longo de modo de demonstração não é repetido na revisão, que já se identifica como demonstração; a mensagem de escopo oficial próxima da confirmação foi abreviada.
4. O aviso institucional redundante no rodapé da revisão foi retirado, mas a advertência de que o envio **não gera protocolo da Prefeitura** permanece ao lado da confirmação.
5. **Alertas de prioridade e de possível risco à integridade física permanecem visíveis**, independentemente da expansão dos detalhes. A decisão humana, correção de categoria/prioridade e resumo continuam disponíveis.

**Evidências de código e navegador:**

- Capturas anteriores: `docs/evidencias/feedback_usabilidade_20261113/antes/desktop_revisao.png` e `mobile_revisao.png`.
- Capturas após a alteração: `docs/evidencias/feedback_usabilidade_20261113/depois/desktop_revisao.png` e `mobile_revisao.png`.
- Expansão dos detalhes: `docs/evidencias/feedback_usabilidade_20261113/depois/desktop_detalhes_expandidos.png` e `mobile_detalhes_expandidos.png`.
- Verificação reexecutável: `python -m scripts.validar_densidade_revisao --fase depois` (requer front-end e API em modo demonstração).
- Resultados estruturados nos arquivos `resultados.json` de cada fase.

**Reavaliação humana da melhoria (relato recebido em 13/11/2026):** após visualizar a versão simplificada, a mesma participante P1 **gostou do que foi alterado**, considerou que a tela ficou **mais clara** e que informações não relevantes para os usuários deixaram de competir pela atenção. A avaliação foi transmitida pelo aluno; trata-se de **feedback qualitativo sobre a mudança visual**, não de um novo teste completo cronometrado de todas as tarefas. A validação técnica também confirmou preservação dos alertas, controles de revisão e responsividade em desktop/celular.

## Roteiro de referência para eventuais avaliações adicionais (10–15 minutos)

1. Apresente o sistema, explicando que não é canal oficial.
2. Peça que criem um relato fictício de problema urbano sem apontar os controles na tela.
3. Peça que interpretem a prioridade e editem algum campo se julgarem necessário.
4. Peça que confirmem e procurem o relato no painel.
5. Pergunte: “O que foi mais fácil?”, “O que foi confuso?” e “O que você melhoraria?”

**Situação:** **três avaliações externas reportadas (P1, P2 e P3)**, atingindo a quantidade prevista de participantes. A melhoria de interface solicitada por P1 foi implementada e avaliada positivamente pela própria participante após a alteração. A autoavaliação do integrante está registrada à parte. As avaliações são relatos qualitativos transmitidos pelo aluno; não foram presumidas tarefas específicas, duração ou perfil dos participantes.
