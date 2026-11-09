# Validação de Usabilidade — Teste com 3 Participantes Reais

**Objetivo:** Avaliar a experiência real do cidadão comum na interação com a interface do VivaBairro, verificando clareza das instruções, facilidade no preenchimento, compreensão da sugestão de IA e eficácia do mecanismo de revisão humana (*Human-in-the-Loop*).

> **Aviso de Integridade Acadêmica:** Este protocolo está completamente preparado e estruturado para execução. Os testes devem ser realizados com 3 pessoas reais pelo aluno antes do envio final. Não devem ser inventados dados de entrevistados.

---

## 1. Regras e Cuidados Éticos na Condução (LGPD)

- **Participantes:** 3 pessoas adultas (P1, P2, P3) com diferentes graus de familiaridade com tecnologia (ex.: jovem conectado, usuário intermediário e pessoa idosa ou com menor fluência digital).
- **Anonimização:** Jamais colete ou registre nome completo, CPF, telefone, e-mail, fotos de rosto ou endereço pessoal.
- **Esclarecimento Prévio:** Explique ao participante que se trata de uma **Prova de Conceito (POC) acadêmica**, que o sistema **não tem conexão com a Prefeitura de São Paulo** e que os relatos informados devem ser **fictícios**.

---

## 2. Roteiro de Aplicação Padronizado (10 a 15 minutos por pessoa)

Apresente a tela inicial (`http://localhost:8501`) sem instruções detalhadas e peça para o participante realizar as seguintes tarefas enquanto expressa seus pensamentos em voz alta (*Think-Aloud Protocol*):

1. **Reconhecimento Inicial (1 min):** Olhe para a tela inicial. Para que você acha que serve este sistema? O objetivo fica claro logo de início?
2. **Registro de Relato (3 min):** Imagine que você encontrou um buraco perigoso ou uma calçada quebrada perto da praça do seu bairro. Preencha o formulário e solicite a análise de inteligência artificial.
3. **Avaliação da Resposta da IA (3 min):** Veja a resposta que a IA gerou. A prioridade sugerida faz sentido para você? As cores e os ícones ajudam a entender a gravidade?
4. **Revisão Humana e Confirmação (3 min):** Você concorda com o resumo ou quer ajustar a categoria/prioridade? Corrija algum campo se desejar, avalie se a sugestão foi adequada e confirme o relato. O aviso de que **não é um protocolo oficial da Prefeitura** ficou perceptível?
5. **Exploração do Painel de Relatos (3 min):** Acesse o painel. Tente filtrar os relatos por categoria e por nível de prioridade. Você consegue ver o gráfico e entender a quantidade de relatos?
6. **Pergunta de Fechamento (2 min):** O que você achou mais confuso ou difícil? Se pudesse mudar algo nesta tela para torná-la mais simples para qualquer morador, o que mudaria?

---

## 3. Matriz de Registro das Observações

*(Preencher após a condução das 3 sessões)*

| ID | Perfil do Participante (idade aproximada e fluência digital) | Tarefa Concluída com Sucesso? | Principal Dificuldade Observada | Feedback ou Sugestão Espontânea | Evidência (Anotação / Registro) |
|---|---|---|---|---|---|
| **P1** | *Ex.: 24 anos, estudante universitário, alta familiaridade digital* | *(Sim / Parcial / Não)* | *(Registrar se houve hesitação ao enviar ou entender os botões)* | *(Sugestão de melhoria dada pelo participante)* | *Sessão realizada em DD/MM/AAAA* |
| **P2** | *Ex.: 48 anos, comerciante de bairro, uso habitual apenas de WhatsApp* | *(Sim / Parcial / Não)* | *(Registrar se a linguagem técnica ou termos do formulário causaram dúvida)* | *(Sugestão de melhoria dada pelo participante)* | *Sessão realizada em DD/MM/AAAA* |
| **P3** | *Ex.: 67 anos, aposentada, baixa familiaridade com computadores/desktop* | *(Sim / Parcial / Não)* | *(Registrar se a navegação por sidebar ou leitura dos gráficos gerou dificuldade)* | *(Sugestão de melhoria dada pelo participante)* | *Sessão realizada em DD/MM/AAAA* |

---

## 4. Ajuste Decorrente do Feedback (Exigência Obrigatória)

O enunciado exige que pelo menos um ajuste real seja aplicado no código/interface com base nas dificuldades apontadas pelos participantes:

- **Problema Observado:** *(Descrever a dificuldade real relatada pelos participantes durante o teste. Ex.: Usuário ficava em dúvida se o relato tinha sido salvo após clicar em confirmar, ou tinha dificuldade de voltar ao painel).*
- **Alteração Aplicada no Código:** *(Citar o arquivo alterado e a modificação realizada. Ex.: Criação de tela dedicada de recibo em `frontend/features/relatar.py` com o código local destacado e botão direto 'Ver no Painel de Relatos').*
- **Evidência do Antes e Depois:** *(Referenciar captura de tela demonstrando a tela antes e após o aprimoramento).*
- **Como Foi Verificado que Melhorou:** *(Nova execução do fluxo comprovando menor atrito e maior clareza para o cidadão).*
