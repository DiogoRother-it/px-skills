---
name: px-setup
description: Prepara o TERRENO técnico de um projeto (a parte de git/repositório) para o líder UX, sem ele decorar comando. Decide o cenário — projeto novo × continuação, e se os devs já criaram o repositório — e executa o setup certo: monta o sandbox a partir do boilerplate, ou clona o repo do dev e cria a branch ux/. Também executa a ENTREGA — migrar o trabalho do sandbox pro repo do dev (identidade + telas + planning) numa branch ux/ com Merge Request. Não idealiza nem desenha tela: prepara e entrega. Use ao começar o terreno de um projeto ou ao levar o sandbox pro repo do dev — "começar um projeto", "montar o ambiente", "os devs liberaram o repo", "levar meu trabalho pro repo do dev", "criar a branch ux".
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: setup
---

# px-setup — prepara o terreno e faz a entrega

Esta skill cuida da **parte mecânica de repositório** pra o líder UX não precisar decorar comando de `git`. Ela **pergunta o cenário**, **executa o setup certo** e, no fim do ciclo, **leva o trabalho pro repo do dev**. Ela não idealiza nem desenha tela — quem faz isso é a cadeia a partir de `px-start`.

**Público desta skill:** o líder UX/PX. Seja direto: pergunte só o que muda a decisão, execute o resto.

**Regra de ouro:** o UX descreve a intenção em português; a skill roda os comandos (`git`, `npm`, `npx`) por ele. Nunca peça pra ele digitar `git` na mão.

Contexto inicial via slash: `$ARGUMENTS` (nome/ideia do projeto ou "entrega"). Se vazio, pergunte o que a pessoa vem fazer.

## Prompting

Segue `Skill Prompting Conventions` do `CLAUDE.md`. Estruturada pra decisões enumeráveis (novo × continuação, repo existe?, é entrega?); livre pra nome do projeto e URL do repo. Toda pergunta traz o porquê + default recomendado; eco ao final antes de executar.

## Passo 0 — Qual é o cenário?

Pergunte (`AskUserQuestion`), porque o caminho muda tudo:

- **Projeto novo** → Passo 1.
- **Continuação de algo que já existe** (o repo do dev já está com você) → Passo 3 (entrar na branch e retomar).
- **Hora de entregar** (levar o sandbox pro repo do dev) → Passo 4.

## Passo 1 — Projeto novo: os devs já criaram o repositório?

Pergunte (`AskUserQuestion`), porque define de onde o terreno vem:

- **Ainda não há repo do dev** → **montar o sandbox** (Passo 2). O UX começa a idealizar já, sem esperar o dev.
- **O repo do dev já existe** → **clonar o repo do dev** e criar a branch `ux/<funcionalidade>` (Passo 3). O UX idealiza direto na arquitetura real.

> **Branch por funcionalidade/fluxo, não por projeto.** Um projeto tem várias funcionalidades → várias branches `ux/*`. O slug `<funcionalidade>` é o **mesmo** que a cadeia usa em `planning/<iniciativa>/` e no `PX-PROGRESS` — um slug só governa planning, checkpoint e branch. Se a funcionalidade ainda não tem nome (discovery não rodou), a branch nasce assim que o `px-intake` decide o slug; não invente nome provisório.

## Passo 2 — Montar o sandbox (projeto novo, sem repo do dev)

**O que é:** uma cópia local do boilerplate — já traz a biblioteca de componentes e os tokens. Rascunho padronizado, temporário e descartável.

**Executar (a skill roda; não peça pro UX digitar):**
1. Pedir um nome pra pasta (livre; ex: a ideia do projeto).
2. Clonar o boilerplate: `git clone https://github.com/DiogoRother-it/centralit-boilerplate.git <pasta>`
3. Entrar na pasta e **desconectar do git** pra não empurrar rascunho no boilerplate do time: `rm -rf .git`
4. Instalar: `npm install`
5. Adicionar as skills: `npx github:DiogoRother-it/px-skills`
6. Avisar pra **recarregar a sessão** (as skills aparecem no menu `/` só depois) e **começar por `/px-start`**.

**Pré-requisito:** a pessoa precisa ter acesso ao repo privado `centralit-boilerplate` (login normal do GitHub; sem token).

## Passo 3 — Trabalhar no repo do dev (novo com repo, ou continuação)

**O que é:** o repositório real do dev, com a arquitetura definitiva (monorepo).

**Executar:**
1. Se ainda não clonou: pedir a **URL do repo do dev** e clonar.
2. Criar/entrar na branch de UX: `git checkout -b ux/<funcionalidade>` (recém-clonado já parte da `main` atualizada; se o repo já estava na máquina, `git checkout main && git pull` antes).
3. **Nunca trabalhar na `main`.** Todo trabalho de UX vive numa branch `ux/<funcionalidade>`.
4. Encaminhar pra idealização (`/px-start`) se ainda não passou por ela.

> **Repo real = branch desde o início.** Diferente do sandbox (onde a branch só nasce na entrega, Passo 4), num repo real a branch `ux/<funcionalidade>` é criada **já aqui**, assim que a funcionalidade tem nome — todo o trabalho da cadeia já cai nela. Se o líder chegou com a funcionalidade clara, crie agora; se veio vago, o `px-intake` nomeia o slug e a branch é criada nesse ponto (esta skill é reinvocada pra isso).

## Passo 4 — Entrega: levar o sandbox pro repo do dev

Roda quando o dev libera o repo e o UX já tem trabalho no sandbox. Normalmente é **despachada pela `px-handoff`** (a skill de fechamento), que já traz o pacote pronto: a funcionalidade, o título do MR com `[Sprint NN]` e o `handoff.md` como corpo. Também pode ser chamada direto pra uma entrega simples.

**Pré-condição (confirme antes de migrar):** o repo do dev já precisa ter o `packages/components` **semeado com o padrão Central IT** (o time de dev faz isso ao criar o repo, via registry `@centralit/kit`). Se o repo chegou "cru", sem os componentes, as telas migradas vão referenciar componentes que não existem e quebram. Se for o caso, pare e sinalize o time de dev antes de seguir.

**Executar:**
1. Garantir o repo do dev clonado e a branch `ux/<funcionalidade>` criada (Passo 3).
2. **Migrar cada coisa pro lugar certo** (não copiar o sandbox inteiro):
   - **Identidade** (`src/index.css` do sandbox) → ajustar os valores dos tokens em `packages/components/src/styles.css` (o formato de token é diferente: `--primary` vira `@theme --color-primary`).
   - **Telas** → `apps/<front>/src/routes/`, adaptadas à estrutura de rotas do projeto.
   - **`planning/`** → `planning/` (vai quase direto).
   - **Não levar:** componentes (`src/components/ui`), `node_modules`, `.git` — já existem no repo do dev.
3. Commitar e empurrar a branch: `git add .` → `git commit -m "ux(<funcionalidade>): ..."` → `git push -u origin ux/<funcionalidade>`.
4. Gerar o **link do Merge Request** no GitLab (`ux/<funcionalidade>` → `main`) pra o UX abrir; o dev revisa e integra. **Título do MR com o sprint** quando vier da `px-handoff`: `[Sprint NN] ux(<funcionalidade>): <resumo>`; corpo = o `handoff.md`.

**Antes do commit, mostre ao UX o que vai entrar** (resumo dos arquivos migrados) pra ele conferir — a colocação envolve julgamento e pode variar por projeto.

## Eco final

Antes de executar, repita em 3–4 linhas: *"Então: cenário **X**, vou fazer **Y** em **Z** — confirma?"*. Só então rode os comandos.

## Regras

- **Não idealiza nem desenha.** Prepara terreno e entrega; a idealização é a partir de `px-start`.
- **Nunca `git` na mão pro UX.** A skill executa; o UX só confirma.
- **Nunca commit na `main`.** Sempre branch `ux/<funcionalidade>` + Merge Request.
- **Sandbox é descartável.** Depois de migrado e mergeado, pode ser apagado.
- **Sem token no fluxo de sandbox.** O acesso ao repo privado é o login normal do GitHub.

## Relação com o fluxo

```
px-setup (terreno / entrega)
   ├─ monta sandbox  ──►  /px-start  →  px-intake  →  px-kickoff  →  px-request  →  px-story  →  px-handoff
   └─ entrega (Passo 4)  ◄── px-handoff despacha → branch ux/<funcionalidade> + Merge Request [Sprint NN] → dev
```

> Integração: o Passo 1 do `px-start` delega o terreno técnico pra cá. Ele só confirma a raiz e o alvo de build e encaminha pra `px-setup` quando o terreno ainda não existe. Sem duplicação de comando de git entre as duas.
>
> Fechamento: a `px-handoff` monta o pacote de entrega (DoD + sprint + flows) e **despacha a mecânica de git pra cá** (Passo 4). O `px-handoff` não roda git; a `px-setup` não monta pacote — cada uma na sua metade.
