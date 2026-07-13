---
name: px-story
description: Entrevista à prova de balas que transforma um px-request numa história de usuário pronta pro backlog, com critérios de aceite, critérios de usabilidade (rubrica ux-persona) e cenários BDD em Gherkin (pt-BR). Formula cada critério UM de cada vez, explicando o porquê, com exemplo e default, e confirma cobertura de todos os estados. Feita para que até quem não é UX gere uma história sem furos. Use quando o líder disser "gera a história", "cria a user story", "escreve os critérios de aceite", "quero o BDD disso", ou ao formalizar um px-request para handoff.
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: story
---

# px-story — entrevista da história (aceite + usabilidade + BDD)

Transforma o resultado de um `px-request` numa **história de usuário** com três camadas de critério que o dev e o `ux-persona`/Playwright vão verificar. A `px-request` já mastigou a descoberta; aqui a gente **formula os critérios** com o mesmo cuidado — um por vez, sem deixar comportamento nem estado sem cobertura.

Você continua **chato de propósito.** Um critério vago ("deve ser fácil de usar") não passa: tem que virar algo observável e testável.

Contexto inicial via slash: `$ARGUMENTS` (caminho do `px-request`, descrição, ou referência).

## As 7 regras da entrevista (inegociáveis)

1. **Uma coisa de cada vez** — formule/confirme um critério (ou micro-lote) por rodada.
2. **Sempre explique o porquê** — por que aquele critério importa e o que ele previne.
3. **Sempre dê exemplo + default recomendado** — proponha o critério pronto; o líder só ajusta.
4. **Enumerou? Pergunta estruturada** (`AskUserQuestion`).
5. **"Não sei / tanto faz" não trava** — proponha o default e registre como Premissa.
6. **Eco ao fim de cada bloco** — releia os critérios formulados e confirme.
7. **Nunca pule um estado em silêncio** — todo estado do `px-request` (empty/error/loading/read-only) precisa virar critério e cenário. Definition of Ready no fim não tem lacuna.

## Idioma

História e cenários em pt-BR. Gherkin em português: `Funcionalidade / Cenário / Dado / Quando / Então / E`.

---

# Os blocos da entrevista

## S0 — Ingerir o px-request (base de tudo)
**Por que importa:** a história herda propósito, público, variação, dados, ações e estados já levantados — não reinventar.
**Fazer:** ler o `px-request` de origem. Se não existir, **avisar que o ideal é rodar `px-request` antes** (senão a história nasce sem base) e oferecer coletar o mínimo aqui. Ecoar o que foi herdado: "Vou partir disto: propósito X, público Y, variação Z, estados A/B/C — certo?"

## S1 — Narrativa
**Decidir:** a frase "Como / quero / para", ancorada num público REAL do kickoff (não "usuário" genérico).
**Por que importa:** amarra a história a uma pessoa e a um valor; genérico não orienta decisão.
**Fazer:** propor a narrativa pronta a partir do request e confirmar. *ex: "Como gestor de acessos, quero desativar quem saiu da empresa, para manter as permissões corretas."*

## S2 — Granularidade
**Decidir:** isto cabe em uma história ou precisa quebrar?
**Por que importa:** história grande demais não fecha num ciclo e vira handoff impreciso.
**Perguntar (estruturada):** "Isto é uma entrega única ou são várias?" — *Uma história (Recomendado se cabe num ciclo)* · *Quebrar em várias → chamar `agile-epic`.*

## S3 — Critérios de aceite (funcional)
**Decidir:** o que precisa ser verdade pra dizer "funciona".
**Por que importa:** é o contrato objetivo do que a feature faz. Cada item tem que ser **verificável** (dá pra apontar e dizer passou/não passou).
**Fazer, um de cada vez:**
- Derive um critério por **comportamento** do request (B5 ações) e um por **estado** (B7): default, empty, error, loading, read-only.
- Escreva cada um como afirmação testável — *ex: "Ao desativar um usuário, a linha passa a 'Inativo' e aparece um toast de confirmação."* Evite "deve funcionar bem".
- Confirme cada critério com o líder (ou registre Premissa se ele deixar no default).

## S4 — Critérios de usabilidade (rubrica ux-persona, dimensão por dimensão)
**Decidir:** o critério concreto de CADA dimensão que o `ux-persona` avalia. Vá **uma dimensão por vez** — é aqui que "fácil de usar" vira algo checável.
**Por que importa:** é o que separa "o código roda" de "a pessoa consegue". O dev valida isto no Playwright; o `ux-persona`, no walkthrough.
Para cada dimensão, pergunte/proponha o critério desta tela:
- **Descoberta** — "o público acha a ação sem adivinhar?" *ex: ação visível na linha, não escondida.*
- **Clareza** — "os textos são claros pro nível de familiaridade do público?" *ex: Status com rótulo + cor, não só cor.*
- **Feedback** — "toda ação responde (sucesso/erro/loading)?" *ex: botão mostra loading; sucesso vira toast.*
- **Fricção** — "mínimo de passos? nada redundante?" *ex: lote em 1 confirmação, não N.*
- **Sem beco sem saída** — "erro e vazio oferecem próximo passo?" *ex: vazio tem CTA 'Convidar'.*
- **Fidelidade** — "bate com o UI KIT/design (tokens, layout, copy)?" *ex: disabled = cinza real.*
- **Autenticidade de dados** — "mostra dado real do usuário, nunca mock/lorem em produção?" *ex: após editar, a linha reflete o valor salvo.*
Marque N/A com motivo qualquer dimensão que não se aplique — nunca some em silêncio.

## S5 — BDD (cenários Gherkin, pt-BR)
**Decidir:** os cenários executáveis que amarram aceite + usabilidade em comportamento observável.
**Por que importa:** vira o roteiro do dev e do teste; é a prova viva de que a história foi cumprida.
**Regras (aplicar em todo cenário):**
- Escrever **pela interface** (clicar/preencher), nunca por URL/rota interna — espelha a regra de ouro do `ux-persona`.
- `Então` sempre **observável** (estado de UI, mensagem, dado na tela) — nunca "funciona".
- Um `Cenário` por comportamento.
**Cobertura obrigatória (confirme que existe um cenário para cada):**
- [ ] Caminho feliz (a ação principal)
- [ ] Estado vazio
- [ ] Estado de erro (com recuperação)
- [ ] Permissão/read-only (se houver mais de um público)
- [ ] Pelo menos uma regra de negócio do request (B9)
Escreva os cenários, mostre, e confirme a cobertura acima antes de fechar.

## S6 — Rastreabilidade
**Fazer:** amarrar a história às fontes, para o dev navegar:
- Request de origem · Variação de componente (`ds-components_v4.md`) · Público-alvo (`publico-alvo.md`) · UI KIT · Flow sugerido do `ux-flows` (com o persona de cada público).

## S7 — Definition of Ready (trava + eco final)
- [ ] Narrativa ancorada num público real (S1)
- [ ] Critérios de aceite verificáveis, um por comportamento e por estado (S3)
- [ ] Critérios de usabilidade por dimensão (S4), N/A justificado onde não se aplica
- [ ] BDD com cobertura: feliz + vazio + erro + permissão + regra de negócio (S5)
- [ ] Rastreabilidade completa (S6)
- [ ] Premissas registradas
Eco final: resumo de 5–8 linhas da história. O líder confirma. Só então está *ready* pro handoff.

## Onde salvar
- Com iniciativa: `planning/<iniciativa>/stories/<slug>.md`
- Standalone: `planning/<projeto>/stories/<slug>.md`

## Encadeamento

> Ao fechar, **atualize o checkpoint** `planning/<iniciativa>/PX-PROGRESS.md` (ver "Checkpoint de progresso" no `px-protocol.md`): marque a história desta tela como feita (com o caminho do artefato), aponte a próxima tela ou o handoff em *Próximo passo*, e sincronize Premissas → *Decisões travadas* e pendências → *Perguntas em aberto*.

Com a Definition of Ready completa, oferecer:
- "Quero gerar o flow do `ux-flows` pro dev validar como usuário?"
- "Fechar o handoff → dev com a `px-handoff` (Definition of Done + sprint + flows)?" — quando o lote de telas da funcionalidade estiver pronto. A `px-handoff` consolida as histórias, carimba o sprint e despacha a entrega pra `px-setup` Passo 4.

## Relação com o fluxo
```
px-kickoff  →  px-request  →  px-story  →  px-handoff  →  px-setup P4 → dev (ux-flows/ux-persona + Playwright)
                              ^ você está aqui
```
