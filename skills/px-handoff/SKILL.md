---
name: px-handoff
description: Skill de FECHAMENTO da cadeia PX. Monta o pacote de handoff pro dev a partir das histórias já ready — consolida o que está sendo entregue, fecha a Definition of Done (Playwright + 99% de fidelidade), amarra os flows/personas do ux-flows/ux-persona, carimba a qual sprint/semana a entrega se refere e atualiza o PX-PROGRESS. Não desenha tela e NÃO roda git: delega a entrega mecânica (branch ux/<funcionalidade> + Merge Request) pra px-setup Passo 4. Use ao fechar um lote de telas prontas pra levar pro dev — "fechar o handoff", "preparar a entrega pro dev", "empacotar pro desenvolvimento", "gerar a definition of done", "qual sprint essa entrega entra", "finalizar o fluxo".
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: handoff
---

# px-handoff — o fechamento da cadeia (entrega pro dev)

Esta skill **fecha** o ciclo de uma funcionalidade/fluxo: pega as histórias que já estão *ready* (saíram do `px-story`) e monta o **pacote de handoff** que o dev vai consumir — o que está sendo entregue (código funcional + histórias), como saber que ficou pronto (Definition of Done), como validar (flows/personas + Playwright) e **em qual sprint** isso entra.

**Contrato de entrega:** o dev recebe **código funcional rodando** (branch `ux/<funcionalidade>`) + **histórias de usuário** (critérios de aceite + BDD). Não é uma spec pra reinterpretar — é o trabalho implementado. O papel do dev é **nivelamento de stack**: adaptar a estrutura do sandbox ao projeto real. Não é reimplementação.

Ela **não desenha tela** (isso é `px-request`/`px-story`) e **não roda git** — a mecânica de branch/Merge Request é da **`px-setup` Passo 3** (o protocolo proíbe duplicar comando de git entre skills). O `px-handoff` monta o documento e **despacha a entrega pra `px-setup`**.

**Público desta skill:** o líder UX/PX. Seja direto: monte o pacote a partir do que já existe, pergunte só o que muda a decisão, confirme e feche.

Contexto inicial via slash: `$ARGUMENTS` (nome da funcionalidade/fluxo, ou caminho de `planning/<funcionalidade>/`). Se vazio, pergunte qual funcionalidade será entregue.

## Prompting

Segue `Skill Prompting Conventions` do `CLAUDE.md`. Estruturada pra decisões enumeráveis (sprint-alvo, o que entra na leva, gerar flow agora?); livre pra nota de release. Toda decisão traz o porquê + default recomendado; eco antes de despachar.

## Pré-requisito (checar antes de montar)

- As telas da funcionalidade já passaram pelo **`px-story`** (têm história + aceite + usabilidade + BDD *ready*). Se alguma ainda está só em `px-request`, avise que o handoff nasce incompleto e ofereça fechar a `px-story` faltante antes.
- O **`px-preview` foi gerado** (HTML navegável das telas desta leva). Se não foi, **não avance** — ofereça rodar o `px-preview` agora antes de continuar. O navegável é o que elimina o "dev no escuro": sem ele, o MR chega com código mas sem referência visual e volta o problema da interpretação.
- Existe o checkpoint `planning/<funcionalidade>/PX-PROGRESS.md` (a cadeia veio criando). Se não existir, crie agora (ver "Checkpoint de progresso" no `px-protocol.md`) — o handoff é o último a atualizá-lo.

> **Nota de slug:** `<funcionalidade>` é o mesmo slug que a cadeia usa em `planning/<iniciativa>/` e na branch `ux/<funcionalidade>`. Um slug só governa planning, checkpoint e branch — não invente um nome novo aqui.

---

# Os blocos do handoff

> Não é entrevista de descoberta (isso já foi feito). É **consolidação**: puxe do que existe, confirme, carimbe. Avance na ordem. Registre no template `templates/px-handoff.md`.

## BLOCO 1 — Escopo da entrega (o que entra nesta leva)
**Decidir:** quais histórias/telas prontas vão neste handoff.
**Por que importa:** uma funcionalidade pode ter mais telas do que cabe num sprint. O que fica de fora é tão importante quanto o que entra.
**Fazer:**
- Liste as histórias *ready* de `planning/<funcionalidade>/stories/` com status. Confirme com o líder quais entram nesta leva.
- Marque o que **fica pra depois** (e por quê) — vira a próxima leva.

## BLOCO 2 — Sprint / semana da entrega (o carimbo do "quando")
**Decidir:** a qual sprint (e semana ISO) esta entrega se refere.
**Por que importa:** o dev se organiza por sprint. Este é o momento em que o "quando" vira real — antes disso era só a ordem relativa do roadmap do `px-epic`.
**Fazer (`AskUserQuestion` pro número do sprint):**
- Se o `px-epic` já sugeriu um **sprint-alvo** pra estas telas, apresente-o como default e confirme/ajuste — a decisão final de calendário é aqui.
- Registre **`Sprint NN`** + a **semana ISO** correspondente (ex: `Sprint 12 · 2026-W29`). A semana ISO desambigua; o número do sprint é o que o time lê.
- Este carimbo vai pro campo `Sprint` do `PX-PROGRESS` e pro **título do Merge Request** (`[Sprint 12] ux(<funcionalidade>): ...`).

> A branch **não** carrega o sprint: `ux/<funcionalidade>` atravessa sprints. O sprint é carimbo de entrega (MR + PX-PROGRESS), não de branch.

## BLOCO 3 — Definition of Done (como o dev sabe que ficou pronto)
**Decidir:** o critério objetivo de "entregue" pra esta leva.
**Por que importa:** sem DoD explícito, "pronto" é opinião. O protocolo fixa a régua; aqui você a instancia.
**Fazer — montar a DoD (padrão da casa, ver `px-protocol.md` › Handoff → dev):**
- [ ] Nivelamento de stack concluído: telas do sandbox integradas na estrutura do projeto real, sem perda de comportamento ou estado.
- [ ] Todas as telas implementadas seguindo o UI KIT (tokens, sem hex/radius solto, grid de 8px).
- [ ] Todos os estados de cada tela (default/loading/empty/error/disabled/read-only/hover/foco/responsivo).
- [ ] Todos os breakpoints (Mobile/Tablet/Desktop/Widescreen).
- [ ] Validação visual via **Playwright**, **meta de 99% de fidelidade**, evidências anexadas ao MR.
- [ ] Os cenários **BDD** de cada história passam (feliz + vazio + erro + permissão + 1 regra de negócio).
- [ ] Histórias de usuário (`px-story`) referenciadas no MR — são o contrato de aceite.
- Adicione DoD específico da funcionalidade se houver (ex: integração X mockada e marcada).

## BLOCO 4 — Validação pelo usuário (flows + personas)
**Decidir:** como o dev valida a usabilidade percorrendo como usuário, não só rodando o código.
**Por que importa:** "o código roda" ≠ "a pessoa consegue". Amarra o handoff ao `ux-flows`/`ux-persona`.
**Fazer:**
- Para cada história, aponte o **flow do `ux-flows`** correspondente e o **persona** de cada público (do `publico-alvo.md`). Se o flow ainda não existe, ofereça gerá-lo agora (`ux-flows`) — o dev valida por ele.
- Regra herdada: validação **pela interface** (clicar/preencher), nunca por rota interna.

## BLOCO 5 — Fronteiras de integração (onde acaba o mock, começa o real)
**Decidir:** o que hoje é mock/fixture e precisa virar integração real no dev.
**Por que importa:** é a ponte com o back-end. Sem isso, o dev não sabe o que plugar.
**Fazer:**
- Consolide as `⚑ Boundary` das histórias/spec (ver `px-epic` › consolidação): cada dependência de API/low-code/storage/terceiro, com o que precisa ser substituído.
- Sem dependência → "Nenhuma — opera sobre dados já mockados/carregados."

## BLOCO 6 — Fechar: atualizar checkpoint e despachar a entrega
**Fazer, nesta ordem:**
1. Montar o `planning/<funcionalidade>/handoff.md` (template) e apresentar o resumo ao líder.
2. **Atualizar o `PX-PROGRESS.md`**: marcar as histórias entregues como feitas, preencher o campo `Sprint`, e apontar a próxima leva (ou "cadeia concluída") em *Próximo passo*.
3. **Confirmar que o `px-preview` existe** — o arquivo HTML navegável gerado anteriormente vai **anexado ao MR** como referência visual obrigatória. Sem ele, não despacha.
4. **Despachar a entrega git pra `px-setup` Passo 3** — não rode git aqui. Passe pra ela: a funcionalidade (`ux/<funcionalidade>`), o título do MR com `[Sprint NN]`, o `handoff.md` como corpo do MR, e o caminho do HTML do `px-preview` para anexar.

## Eco final

Antes de despachar, repita em 4–6 linhas: *"Handoff da funcionalidade **X**: **N** histórias (código funcional + BDD), **Sprint NN · semana ISO**, DoD fechada, flows amarrados, **M** fronteiras de integração, navegável `px-preview` gerado. O dev recebe a branch `ux/<funcionalidade>` + o HTML de referência e faz o nivelamento de stack. Vou atualizar o checkpoint e mandar a entrega pra `px-setup` — confirma?"*. Só então feche.

## Onde salvar

`planning/<funcionalidade>/handoff.md` — o mesmo slug da branch e do planning.

## Regras

- **Não desenha tela.** Consolida o que `px-request`/`px-story` já produziram.
- **Não roda git.** Branch e Merge Request são da `px-setup` Passo 3; o `px-handoff` despacha pra ela.
- **Não inventa DoD nem boundary.** Puxa da spec/histórias; o que faltar vira Pergunta em aberto, não suposição.
- **Sprint é carimbo de entrega**, não de branch. Vai no MR e no `PX-PROGRESS`, nunca no nome da branch.

## Relação com o fluxo

```
px-request  →  px-story  →  px-handoff  →  px-setup (Passo 3: branch ux/<funcionalidade> + MR)  →  dev (nivela stack)
                            ^ você está aqui (fecha a cadeia: código + histórias + DoD + sprint + flows)
```

> `px-handoff` é a entrega **pro dev** no nível de pacote (o que/como/quando + histórias); a `px-setup` Passo 3 é a mecânica de git dessa entrega; a `px-preview` gera o navegável que vai **obrigatoriamente anexado ao MR** — referência visual que elimina o "dev no escuro". As três são complementares e obrigatórias no fechamento.
>
> O dev **não reimplementa** — ele nivela. O código funcional do sandbox é o entregável; a adaptação à estrutura do projeto real é o nivelamento de stack, responsabilidade exclusiva do dev.
