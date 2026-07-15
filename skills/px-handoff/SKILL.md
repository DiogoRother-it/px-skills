---
name: px-handoff
description: Skill de FECHAMENTO da cadeia PX. Monta o pacote de handoff pro dev a partir das histórias já ready — consolida o HTML do protótipo, o UI Kit do produto e as histórias de negócio (BDD + rastreabilidade componente→história). Não envia código-fonte, branches nem artefatos internos. Use ao fechar um lote de telas prontas pra levar pro dev — "fechar o handoff", "preparar a entrega pro dev", "empacotar pro desenvolvimento", "qual sprint essa entrega entra", "finalizar o fluxo".
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: handoff
---

# px-handoff — o fechamento da cadeia (entrega pro dev)

Esta skill **fecha** o ciclo de uma funcionalidade/fluxo: pega as histórias que já estão *ready* (saíram do `px-story`) e monta o **pacote de handoff** que o dev vai consumir — o que está sendo entregue (código funcional + histórias), como saber que ficou pronto (Definition of Done), como validar (flows/personas + Playwright) e **em qual sprint** isso entra.

**Contrato de entrega:** o dev recebe **código funcional rodando** (branch `ux/<funcionalidade>`) + **histórias de usuário** (critérios de aceite + BDD). Não é uma spec pra reinterpretar — é o trabalho implementado. O papel do dev é **nivelamento de stack**: adaptar a estrutura do sandbox ao projeto real. Não é reimplementação.

Ela **não desenha tela** (isso é `px-request`/`px-story`). Ela fecha o ciclo completo: monta o pacote **e** executa a mecânica de git (branch + push + Merge Request) — sem delegar pra outra skill.

**Público desta skill:** o líder UX/PX. Seja direto: monte o pacote a partir do que já existe, pergunte só o que muda a decisão, confirme e feche.

Contexto inicial via slash: `$ARGUMENTS` (nome da funcionalidade/fluxo, ou caminho de `planning/<funcionalidade>/`). Se vazio, pergunte qual funcionalidade será entregue.

## Prompting

Segue `Skill Prompting Conventions` do `CLAUDE.md`. Estruturada pra decisões enumeráveis (sprint-alvo, o que entra na leva, gerar flow agora?); livre pra nota de release. Toda decisão traz o porquê + default recomendado; eco antes de despachar.

## Pré-requisito (checar antes de montar)

- As telas da funcionalidade já passaram pelo **`px-story`** (têm história + aceite + usabilidade + BDD *ready*). Se alguma ainda está só em `px-request`, avise que o handoff nasce incompleto e ofereça fechar a `px-story` faltante antes.
- O **`px-preview` foi gerado** (HTML navegável das telas desta leva). Se não foi, **não avance** — ofereça rodar o `px-preview` agora antes de continuar. O navegável é o que elimina o "dev no escuro": sem ele, o MR chega com código mas sem referência visual e volta o problema da interpretação.
- Existe o checkpoint `planning/<funcionalidade>/PX-PROGRESS.md` (a cadeia veio criando). Se não existir, crie agora (ver "Checkpoint de progresso" no `px-protocol.md`) — o handoff é o último a atualizá-lo.

**Perguntas obrigatórias antes de montar o pacote (`AskUserQuestion`):**
> 1. "Esse projeto já aderiu de forma completa à biblioteca de componentes `@centralit`?"
>    **Sim** → DoD interno inclui a obrigatoriedade de usar os componentes da biblioteca.
>    **Não** → DoD interno registra que o dev adapta a referência visual conforme a stack do projeto.
> 2. "Qual o caminho local do repo do dev onde o pacote será entregue?" (ex: `C:/projetos/citpeople` ou URL do repositório git remoto)
>    — necessário para executar o push no BLOCO 6.

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

## BLOCO 3 — Definition of Done (checklist interna — não vai no pacote do dev)
**Por que importa:** o dev recebe o HTML já com breakpoints, estados e comportamentos resolvidos. O DoD é a régua que o PX usa pra confirmar que o HTML está completo *antes* de fechar a entrega — não uma lista de tarefas pro dev.
**Verificar antes de avançar pro BLOCO 4:**
- [ ] HTML cobre todos os estados de cada tela (default/loading/empty/error/disabled/read-only/hover/foco/responsivo).
- [ ] HTML cobre todos os breakpoints (Mobile/Tablet/Desktop/Widescreen).
- [ ] UI Kit do produto incluído no pacote (cores de marca, tipografia, identidade).
- [ ] Histórias de negócio com BDD completo (feliz + vazio + erro + permissão).
- [ ] Rastreabilidade componente → história preenchida em cada história.
- [ ] DoD específico da funcionalidade verificado: `<se houver>`

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

## BLOCO 5b — Perguntas em aberto (confirmar com o PX antes de enviar)
**Por que importa:** perguntas sem dono ou sem resposta não chegam pro dev como pendência solta — geram ruído e retorno desnecessário.
**Fazer (`AskUserQuestion` para cada item levantado):**
- Liste todas as pendências identificadas durante os blocos anteriores.
- Para cada uma, pergunte ao PX: **"Isso já tem resposta ou dono confirmado?"**
  - **Tem resposta** → resolve inline no documento antes de enviar.
  - **Tem dono mas sem resposta** → entra no pacote com `dono: <nome>` explícito.
  - **Sem dono e sem resposta** → **não envia**. Bloqueia a entrega até resolver ou descartar.
- Se não houver nenhuma pendência → omitir a seção do template (`nenhuma`).

## BLOCO 6 — Fechar: montar, confirmar e despachar

**Fazer, nesta ordem:**
1. Montar o `planning/<funcionalidade>/handoff.md` (template) com tudo preenchido.
2. Confirmar que o arquivo HTML do protótipo existe e cobre todas as telas desta leva.
3. **Plantar rastreabilidade no HTML:** para cada história, localizar o elemento acionador (botão, link, campo, etc.) e adicionar `data-story="<ID>"` no elemento correspondente.
4. Confirmar que o `ui-kit.md` desta funcionalidade está atualizado.
5. Passar pelo **GATE** (barreira de saída abaixo) — só avança se tudo verde.
6. Apresentar o eco final ao líder e aguardar aceite explícito.
7. **Com aceite confirmado — executar o push para o repo do dev** (a skill roda; o PX só confirma):
   - Montar a pasta de entrega com exatamente:
     - `<funcionalidade>.html` — protótipo visual
     - `ui-kit.md` — tokens e identidade do produto
     - `handoff.md` — histórias, rastreabilidade, fronteiras, perguntas em aberto
   - Mostrar a árvore dos 3 arquivos ao líder antes de commitar.
   - Commitar e empurrar no repo do dev: `git add <arquivos>` → `git commit -m "ux(<funcionalidade>): handoff <Sprint NN>"` → `git push`.
   - Confirmar o push com o hash do commit.

## GATE — Barreira de saída (verificar antes do eco final)

Rodar esta checklist completa antes de apresentar o eco ao líder. **Qualquer item com ✗ bloqueia a entrega** — resolver ou declarar como Pergunta em aberto com dono antes de prosseguir.

**Pacote**
- [ ] HTML do protótipo existe e cobre todas as telas desta leva
- [ ] `data-story="<ID>"` plantado em cada elemento acionador no HTML
- [ ] UI Kit do produto presente e atualizado
- [ ] `handoff.md` preenchido sem campos `<placeholder>` vazios

**Histórias**
- [ ] Todas as histórias desta leva têm BDD completo (feliz + vazio + erro + permissão)
- [ ] Toda história tem rastreabilidade: descrição em texto + anchor `data-story` no HTML
- [ ] Nenhuma story técnica interna do PX incluída — apenas histórias de negócio

**Perguntas em aberto**
- [ ] Toda pendência tem dono confirmado — nenhuma solta sem nome

**O que nunca deve sair**
- [ ] Nenhum arquivo de código-fonte (`.tsx`, `.ts`, `.jsx`, `.js` de componente)
- [ ] Nenhum arquivo de config (`vite.config`, `tsconfig`, `package.json`, `.env`)
- [ ] Nenhum artefato interno (`PX-PROGRESS.md`, stories técnicas, planejamento interno)
- [ ] Nenhuma branch ou referência a branch no documento

## Eco final

Antes de fechar, repita em 3–4 linhas: *"Handoff da funcionalidade **X**: **N** histórias com BDD, HTML do protótipo gerado, UI Kit incluído, **M** fronteiras de integração declaradas. Perguntas em aberto: `<N ou nenhuma>`. O dev recebe o `handoff.md` + HTML + UI Kit como referência visual — confirma o envio?"*. Só então feche.

## Onde salvar

`planning/<funcionalidade>/handoff.md` — o mesmo slug do planning.

## Regras

- **Não desenha tela.** Consolida o que `px-request`/`px-story` já produziram.
- **Não inventa boundary.** Puxa da spec/histórias; o que faltar vira Pergunta em aberto, não suposição.
- **Não envia perguntas em aberto sem dono.** Bloqueia até ter dono confirmado ou descartar.
- **Não inclui código-fonte, branches, config ou artefatos internos** (PX-PROGRESS, stories técnicas) no pacote do dev.
- **Nunca executa o push sem aceite explícito do PX.** O eco final é a porta — sem confirmação, não roda git.
- **O push vai direto pro repo do dev** — não pro boilerplate PX.

## Relação com o fluxo

```
px-request  →  px-story  →  px-handoff  →  dev (referência visual)
                            ^ você está aqui
                            (fecha a cadeia: HTML + UI Kit + histórias de negócio)
```

> `px-handoff` fecha o ciclo: consolida o pacote de referência visual (HTML + UI Kit) e as histórias de negócio (BDD + rastreabilidade) que o dev usa como especificação. O dev é responsável pela implementação na stack do projeto — o PX é referência, não código de produção.
