# Avaliação técnica de usabilidade por cenários simulados — VivaBairro

**Data:** 13/11/2026
**Projeto:** VivaBairro — Global Solution FIAP 2026.2
**Escopo:** interface Streamlit, API FastAPI em modo de demonstração, navegação móvel e revisão humana.
**Metodologia:** três personas fictícias e execução dos fluxos pelo navegador com Playwright. **Não houve entrevistas, depoimentos ou testes com participantes humanos reais.**

## Objetivo e condições

Verificar se três jornadas representativas de usuários são realizáveis, identificar problemas observáveis e aplicar correções justificadas por evidências. Nenhuma chamada à API OpenAI foi feita nesta avaliação. A API foi iniciada com `LLM_PROVIDER=demo` e o script verifica `GET /health` antes de submeter qualquer relato. O Docker Desktop não estava disponível neste notebook; FastAPI e Streamlit foram executados localmente para estes testes.

## Cenários executados

| Cenário e persona fictícia | Tarefa | Observação da execução inicial | Resultado após correção |
|---|---|---|---|
| **01 — Pessoa com pouca familiaridade digital** | Relatar calçada inacessível no bairro **Sé**, revisar e confirmar | O formulário **rejeitou indevidamente** o nome "Sé" por exigir 3 caracteres. Para completar o restante do fluxo inicial, o teste utilizou "Lapa". | **Aprovado.** "Sé" passou a ser aceito pela interface e API; revisão e recibo foram exibidos. |
| **02 — Usuário de smartphone** | Relatar iluminação pública no Centro, confirmar e abrir o painel | Fluxo concluído; gráfico Plotly carregou e não houve overflow horizontal a 390px. | **Aprovado novamente**, com gráfico e navegação preservados. |
| **03 — Pessoa com fluência digital intermediária** | Relatar buraco em via da Mooca, alterar prioridade e resumo antes de confirmar, consultar painel | Alteração de resumo e prioridade permitida; resumo editado e gráficos exibidos após confirmação. | **Aprovado novamente**, sem regressões identificadas no cenário. |

As personas são **hipóteses de uso**, não participantes recrutados. Nenhuma dificuldade subjetiva ou opinião foi atribuída a pessoas inexistentes.

## Problemas e melhorias

### A. Bairro válido de duas letras era rejeitado

- **Evidência inicial:** `evidencias/usabilidade_simulada/antes/01_bairro_se.png` e `antes/resultados.json` (`bairro_se_recusado=true`).
- **Causa:** `RelatoEntrada.bairro` exigia comprimento mínimo de 3 caracteres e a interface repetia essa regra. A restrição desconsiderava bairros reais como **Sé**.
- **Correção:** `backend/app/schemas/relatos.py` ajustado para `min_length=2`; `frontend/features/relatar.py` alinhado ao contrato e com orientação mais clara ao usuário.
- **Verificação:** cenário 01 executado novamente com "Sé" sem troca de bairro; `depois/resultados.json` registra `bairro_se_recusado=false`. Novo teste unitário `test_aceita_bairro_de_dois_caracteres`, preservando rejeição de entrada com apenas um caractere.

### B. Esclarecimento do recibo temporário

- **Problema de comunicação inspecionado no código:** o fluxo inicial mostrava um identificador `LOCAL-...` e um aviso institucional, mas não explicitava junto ao comprovante que aquele código **não é um protocolo oficial**.
- **Correção:** no momento anterior à confirmação e imediatamente após o recibo, a interface explica que o registro só vale para a sessão acadêmica, sem envio automático à Prefeitura, e remete ao canal SP156.
- **Verificação:** `depois/resultados.json` registra `aviso_nao_e_protocolo=true` e a captura `depois/01_recibo.png` mostra o aviso associado ao recibo.
- **Limite da evidência:** isto verifica a presença da mensagem na tela, não garante que um cidadão real a compreenderá.

## Evidências e reprodução

Os arquivos de evidência estão em `docs/evidencias/usabilidade_simulada/`:

- `antes/resultados.json` e `depois/resultados.json` apresentam os resultados executados por cenário.
- `antes/01_bairro_se.png` e `depois/01_bairro_se.png` mostram a correção da validação.
- `antes/01_recibo.png` e `depois/01_recibo.png` mostram a comunicação no comprovante.
- `antes/02_painel_mobile.png` e `depois/02_painel_mobile.png` mostram o painel móvel.
- `antes/03_recibo_alterado.png` e `depois/03_recibo_alterado.png` mostram a confirmação de resumo revisado.
- As demais capturas registram formulário, revisão e painel em cada cenário.

Com FastAPI e Streamlit ligados em modo demo, execute:

```bash
python -m scripts.avaliar_usabilidade_simulada --fase depois --url http://127.0.0.1:18501 --api http://127.0.0.1:18000
python -m pytest -q
```

**Resultados obtidos em 13/11/2026:** três cenários executados após as correções; **48 testes pytest aprovados**; teste de contraste de tema `scripts.validar_tema_e2e` aprovado em desktop claro, desktop com SO escuro e celular com SO escuro.

## Limitação acadêmica

Esta avaliação técnica **não substitui** o requisito do professor de testar com **três pessoas reais** e implementar uma melhoria baseada no **feedback humano de fato coletado**. A melhoria documentada aqui foi motivada por defeito técnico reproduzido e revisão da comunicação da interface, não por depoimentos ou observações de participantes humanos.
