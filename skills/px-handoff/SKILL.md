---
name: px-handoff
description: Skill de FECHAMENTO da cadeia PX. Monta o pacote de handoff pro dev a partir das histórias já ready — consolida o HTML unificado do protótipo, o UI Kit do produto e as histórias de negócio (BDD + rastreabilidade componente→história), organizadas por fluxo. Não envia código-fonte nem artefatos internos. Use ao fechar um lote de telas prontas pra levar pro dev — "fechar o handoff", "preparar a entrega pro dev", "empacotar pro desenvolvimento", "qual sprint essa entrega entra", "finalizar o fluxo".
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: handoff
---

# px-handoff — o fechamento da cadeia (entrega pro dev)

Esta skill **fecha** o ciclo de uma semana/sprint: pega as histórias que já estão *ready* (saíram do `px-story`) e monta o **pacote de handoff** que o dev vai consumir — HTML unificado do protótipo, UI Kit e histórias de negócio organizadas por fluxo.

**Contrato de entrega:** o dev recebe **HTML unificado** (protótipo navegável com âncoras `#view-*` por fluxo) + **UI Kit** + **histórias de negócio** (BDD + rastreabilidade). O PX é referência visual — o dev implementa na stack do projeto.

Ela **não desenha tela** (isso é `px-request`/`px-story`). Ela fecha o ciclo: monta o pacote e executa o push para o repo do dev.

**Público desta skill:** o líder UX/PX. Seja direto: monte o pacote a partir do que já existe, pergunte só o que muda a decisão, confirme e feche.

Contexto inicial via slash: `$ARGUMENTS` (semana/sprint ou lista de fluxos prontos). Se vazio, pergunte qual é a semana/sprint sendo fechada.

## Prompting

Segue `Skill Prompting Conventions` do `CLAUDE.md`. Estruturada pra decisões enumeráveis; livre pra nota de release. Toda decisão traz o porquê + default recomendado; eco antes de despachar.

## Pré-requisito (checar antes de montar)

- As histórias desta leva já passaram pelo **`px-story`** (BDD *ready*). Se alguma ainda está em `px-request`, avise que o handoff nasce incompleto e ofereça fechar a `px-story` faltante antes.
- O **HTML unificado do protótipo existe** e cobre todas as telas desta leva. Se não foi gerado, **não avance** — ofereça rodar o `px-preview` antes de continuar.
- As histórias *ready* ainda não entregues são identificadas automaticamente — a skill varre os arquivos `.md` de histórias e compara com as entregas anteriores (`handoff-ux/`) para montar o delta desta leva. O PX confirma o que entra.

**Perguntas obrigatórias antes de montar o pacote (`AskUserQuestion`):**
> 1. "Esse projeto já aderiu de forma completa à biblioteca de componentes `@centralit`?"
>    **Sim** → DoD interno inclui a obrigatoriedade de usar os componentes da biblioteca.
>    **Não** → DoD interno registra que o dev adapta a referência visual conforme a stack do projeto.
> 2. "Qual o caminho local do repo do dev onde o pacote será entregue?" (ex: `C:/projetos/citpeople`)
>    — necessário para executar o push no BLOCO 6.

---

# Os blocos do handoff

> Não é entrevista de descoberta (isso já foi feito). É **consolidação**: puxe do que existe, confirme, carimbe. Avance na ordem. Registre no template `templates/px-handoff.md`.

## BLOCO 1 — Escopo da entrega (o que entra nesta leva)
**Decidir:** quais histórias prontas vão neste handoff.
**Por que importa:** uma semana pode ter mais histórias do que o dev consegue integrar num sprint. O que fica de fora é tão importante quanto o que entra.
**Fazer:**
- Varrer as histórias com status *ready* que ainda não foram entregues (não aparecem em nenhuma `handoff-ux/semana-*/`). Apresentar a lista ao PX e confirmar quais entram nesta leva.
- Marque o que **fica pra depois** (e por quê) — vira a próxima leva.
- **Recorte dev-facing vs. interno:** aplicar o `templates/handoff-manifest.md`. Além de HTML + UI Kit + stories, entram também as **decisões de produto canônicas** (`decisoes/*.md`) e o **mapa de permissões/triggers** (`rbac-*.md`) quando existirem. Ficam de fora checkpoints (`PX-PROGRESS`), prompts de continuidade/contexto de chat, discovery/auditoria, épicos/requests e scratchpad. Se a iniciativa tiver muitos `.md` internos, gravar/atualizar `planning/<iniciativa>/HANDOFF-MANIFEST.md` a partir do template e confirmar o recorte com o PX.

## BLOCO 2 — Semana da entrega (o carimbo do "quando")
**Decidir:** a qual semana ISO esta entrega se refere.
**Fazer (`AskUserQuestion` para o número da semana):**
- Registre **`semana-<NN>`** + a **semana ISO** correspondente (ex: `semana-29 · 2026-W29`).
- Este carimbo define o nome da pasta de entrega: `handoff-ux/semana-<NN>/`.

## BLOCO 3 — Definition of Done (checklist interna — não vai no pacote do dev)
**Por que importa:** o dev recebe o HTML já com breakpoints, estados e comportamentos resolvidos. O DoD é a régua que o PX usa pra confirmar que o HTML está completo *antes* de fechar a entrega.
**Verificar antes de avançar pro BLOCO 4:**
- [ ] HTML unificado cobre todos os estados de cada tela (default/loading/empty/error/disabled/read-only/hover/foco/responsivo).
- [ ] HTML cobre todos os breakpoints (Mobile/Tablet/Desktop/Widescreen).
- [ ] UI Kit do produto presente e atualizado (cores de marca, tipografia, identidade).
- [ ] Histórias de negócio com BDD completo (feliz + vazio + erro + permissão).
- [ ] Rastreabilidade preenchida em cada história (texto + `data-story` no HTML).
- [ ] Nomes de arquivo das histórias sem prefixos numéricos (`historia-nome.md`, não `01-historia-nome.md`).

## BLOCO 4 — Fronteiras de integração (onde acaba o mock, começa o real)
**Decidir:** o que hoje é mock/fixture e precisa virar integração real no dev.
**Fazer:**
- Consolide as `⚑ Boundary` das histórias: cada dependência de API/low-code/storage/terceiro, com o que precisa ser substituído.
- Sem dependência → "Nenhuma — opera sobre dados já mockados/carregados."

## BLOCO 5 — Perguntas em aberto (confirmar com o PX antes de enviar)
**Por que importa:** perguntas sem dono não chegam pro dev como pendência solta.
**Fazer (`AskUserQuestion` para cada item levantado):**
- Para cada pendência: **"Isso já tem resposta ou dono confirmado?"**
  - **Tem resposta** → resolve inline antes de enviar.
  - **Tem dono mas sem resposta** → entra no pacote com `dono: <nome>` explícito.
  - **Sem dono e sem resposta** → **não envia**. Bloqueia até resolver ou descartar.
- Sem pendências → omitir a seção do template.

## BLOCO 6 — Fechar: montar, confirmar e despachar

**Fazer, nesta ordem:**
1. **Plantar rastreabilidade no HTML:**
   - Para elementos estáticos: adicionar `data-story="<ID>"` diretamente no elemento HTML acionador (botão, link, campo, etc.).
   - Para elementos gerados por JavaScript: localizar a função geradora (ex: `renderRow()`, `buildActionBtn()`) e adicionar `data-story="<ID>"` no HTML que ela constrói — não no HTML estático.
2. Montar o `handoff.md` (template) com tudo preenchido.
3. Passar pelo **GATE** (barreira de saída abaixo) — só avança se tudo verde.
4. Apresentar o eco final ao líder e aguardar aceite explícito.
5. **Com aceite confirmado — montar a estrutura e executar o push** (a skill roda; o PX só confirma):
   - Montar a pasta de entrega **na raiz do repo do dev** com a estrutura:
     ```
     handoff-ux/
     └── semana-<NN>/
         ├── <Produto>-Prototipo.html
         ├── ui-kit.md
         ├── <fluxo-a>/
         │   └── stories/
         │       ├── <historia-1>.md
         │       └── <historia-2>.md
         └── <fluxo-b>/
             └── stories/
                 └── <historia-3>.md
     ```
   - `handoff-ux/` sempre na raiz — nunca dentro de pasta existente do repo do dev.
   - Uma pasta por fluxo. Histórias em `stories/`. HTML e UI Kit na raiz da semana.
   - Mostrar a árvore completa ao líder antes de commitar.
   - **Usar branch órfã para push limpo** (sem herdar histórico do boilerplate):
     ```
     git checkout --orphan ux/semana-<NN>
     git rm -rf .
     git add handoff-ux/semana-<NN>/
     git commit -m "ux(semana-<NN>): handoff <resumo>"
     git push origin ux/semana-<NN>
     ```
   - Confirmar o push com o hash do commit.

## GATE — Barreira de saída (verificar antes do eco final)

Rodar esta checklist completa antes de apresentar o eco ao líder. **Qualquer item com ✗ bloqueia a entrega** — resolver ou declarar como Pergunta em aberto com dono antes de prosseguir.

**Pacote**
- [ ] HTML unificado existe e cobre todas as telas desta leva
- [ ] `data-story="<ID>"` plantado em cada elemento acionador (estático ou gerado por JS)
- [ ] UI Kit presente e atualizado
- [ ] `handoff.md` preenchido sem campos `<placeholder>` vazios

**Histórias**
- [ ] Todas as histórias desta leva têm BDD completo (feliz + vazio + erro + permissão)
- [ ] Toda história tem rastreabilidade: descrição em texto + anchor `data-story` no HTML
- [ ] Nomes de arquivo sem prefixos numéricos
- [ ] Nenhuma story técnica interna do PX incluída — apenas histórias de negócio

**Perguntas em aberto**
- [ ] Toda pendência tem dono confirmado — nenhuma solta sem nome

**O que nunca deve sair** (ver `templates/handoff-manifest.md`)
- [ ] Nenhum arquivo de código-fonte (`.tsx`, `.ts`, `.jsx`, `.js` de componente)
- [ ] Nenhum arquivo de config (`vite.config`, `tsconfig`, `package.json`, `.env`)
- [ ] Nenhum artefato interno: checkpoint (`PX-PROGRESS`), prompt de continuidade/contexto de chat, discovery/auditoria, épicos, scratchpad, memória
- [ ] Nenhuma referência a `planning/` no documento

**O que deve entrar** (além do HTML unificado + UI Kit + stories)
- [ ] Decisões de produto canônicas (`decisoes/*.md`) — regras que o dev implementa
- [ ] Mapa de permissões/triggers (`rbac-*.md`) — quando o produto tem RBAC

## Eco final

Antes de fechar, repita em 3–4 linhas: *"Handoff semana-**NN**: **N** histórias em **M** fluxos, HTML unificado com `data-story` plantados, UI Kit incluído, **X** fronteiras de integração. Perguntas em aberto: `<N ou nenhuma>`. Push via branch órfã `ux/semana-<NN>` no repo do dev — confirma?"*. Só então feche.

## Onde salvar

`handoff-ux/semana-<NN>/handoff.md` — o mesmo slug da semana.

## Regras

- **Não desenha tela.** Consolida o que `px-request`/`px-story` já produziram.
- **Não inventa boundary.** Puxa das histórias; o que faltar vira Pergunta em aberto, não suposição.
- **Não envia perguntas em aberto sem dono.** Bloqueia até ter dono confirmado ou descartar.
- **Não inclui código-fonte, config ou artefatos internos** no pacote do dev.
- **Nunca executa o push sem aceite explícito do PX.**
- **Push sempre via branch órfã** — nunca branch criada a partir do histórico do boilerplate.
- **`handoff-ux/` sempre na raiz do repo do dev** — nunca dentro de pasta existente.
- **HTML é sempre unificado** — nunca separar por funcionalidade.

## Relação com o fluxo

```
px-request  →  px-story  →  px-handoff  →  dev (referência visual)
                            ^ você está aqui
                            (fecha a cadeia: HTML unificado + UI Kit + histórias por fluxo)
```

> `px-handoff` fecha o ciclo: consolida o pacote de referência visual e o entrega via branch órfã limpa no repo do dev. O dev implementa na stack do projeto — o PX é referência, não código de produção.
