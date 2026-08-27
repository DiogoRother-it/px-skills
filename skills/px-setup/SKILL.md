---
name: px-setup
description: Prepara o TERRENO técnico de um projeto (a parte de git/repositório) para o líder UX, sem ele decorar comando. PX SEMPRE trabalha no boilerplate — nunca no repo do dev. Monta o sandbox a partir do boilerplate para o PX idealizar. Não idealiza nem desenha tela e não faz a entrega — a entrega git (branch ux/ + push + MR) é responsabilidade do px-handoff, que tem todo o contexto do pacote. Use ao começar o terreno de um projeto — "começar um projeto", "montar o ambiente", "montar o sandbox", "setup inicial".
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: setup
---

# px-setup — prepara o terreno (sandbox)

Esta skill cuida da **parte mecânica de repositório** pra o líder UX não precisar decorar comando de `git`. Ela **pergunta o cenário** e **monta o sandbox**. Ela não idealiza nem desenha tela — quem faz isso é a cadeia a partir de `px-start`. A entrega git (branch + push + MR) é responsabilidade do `px-handoff`.

**Regra fundamental:** o PX **sempre** trabalha no boilerplate. O repo do dev é destino de entrega, nunca ambiente de trabalho.

**Público desta skill:** o líder UX/PX. Seja direto: pergunte só o que muda a decisão, execute o resto.

**Regra de ouro:** o UX descreve a intenção em português; a skill roda os comandos (`git`, `npm`, `npx`) por ele. Nunca peça pra ele digitar `git` na mão.

Contexto inicial via slash: `$ARGUMENTS` (nome/ideia do projeto ou "entrega"). Se vazio, pergunte o que a pessoa vem fazer.

## Prompting

Segue `Skill Prompting Conventions` do `CLAUDE.md`. Estruturada pra decisões enumeráveis (novo × continuação, é entrega?); livre pra nome do projeto e URL do repo. Toda pergunta traz o porquê + default recomendado; eco ao final antes de executar.

## Passo 0 — Qual é o cenário?

Pergunte (`AskUserQuestion`), porque o caminho muda:

- **Projeto novo** → Passo 1 (montar o sandbox).
- **Continuação** (sandbox já existe, retomando o trabalho) → confirme a pasta do sandbox e encaminhe de volta pra cadeia PX.

> A entrega (branch `ux/<funcionalidade>` + push + MR) é responsabilidade do `px-handoff` — não despache pra cá pra isso.

## Passo 1 — Projeto novo: montar o sandbox

O PX sempre começa no boilerplate — independentemente de o repo do dev existir ou não. O sandbox é o **único ambiente de trabalho do PX**.

> **Branch por funcionalidade/fluxo, não por projeto.** Um projeto tem várias funcionalidades → várias branches `ux/*`. O slug `<funcionalidade>` é o **mesmo** que a cadeia usa em `planning/<iniciativa>/` e no `PX-PROGRESS` — um slug só governa planning, checkpoint e branch. Se a funcionalidade ainda não tem nome (discovery não rodou), ela nasce assim que o `px-intake` decide o slug; não invente nome provisório.

## Passo 2 — Montar o sandbox

**O que é:** uma cópia local do boilerplate — já traz a biblioteca de componentes e os tokens. É o ateliê do PX: padronizado, isolado e independente do repo do dev.

**Executar (a skill roda; não peça pro UX digitar):**
1. Pedir um nome pra pasta (livre; ex: a ideia do projeto).
2. Clonar o boilerplate: `git clone https://github.com/DiogoRother-it/centralit-boilerplate.git <pasta>`
3. Entrar na pasta e **preservar a procedência, desabilitando o push** (⛔ **nunca** `rm -rf .git` — ver abaixo):
   - `git remote rename origin boilerplate-upstream`
   - `git remote set-url --push boilerplate-upstream no-push`
4. Instalar: `npm install`
5. **Configurar o token do registry** (Passo 2b) — sem ele o sandbox não puxa componente novo.
6. Adicionar as skills: `npx github:DiogoRother-it/px-skills`
7. Avisar pra **recarregar a sessão** (as skills aparecem no menu `/` só depois) e **começar por `/px-start`**.

> ⛔ **Por que não `rm -rf .git`.** Cortar o git deixa o sandbox **inauditável**: sem commit de origem, sem `git fetch`, sem idade. Um sandbox que envelhece meses passa a divergir do boilerplate **sem sinal nenhum** — e a cadeia inteira produz entrega plausível sobre base errada. O remote renomeado com push desabilitado resolve as duas coisas: protege o boilerplate do time (era a intenção original) **e** mantém a procedência medível pelo `px-proto`.

## Passo 2b — Token do registry `@centralit` (uma vez por máquina)

**Por que importa:** a biblioteca de componentes **não** vem só do clone. Ela é distribuída como registry shadcn privado (`@centralit`, 52 itens), declarado no `components.json` do boilerplate e autenticado por `Authorization: Bearer ${CENTRALIT_TOKEN}`. Clone e registry são **dois acessos distintos**: dá pra ter o clone e não ter o registry. Nesse estado, `npx shadcn add` cai no shadcn **público** — que responde com sucesso e entrega o default `new-york`, não o componente da Central IT. Silencioso, plausível e errado.

**Verificar (a skill executa):**
1. `CENTRALIT_TOKEN` está no ambiente? (`echo $CENTRALIT_TOKEN` / `$env:CENTRALIT_TOKEN`)
2. O `components.json` da pasta tem o bloco `registries` com `@centralit`?
3. Teste de alcance real: puxar um item conhecido do registry e confirmar que a resposta veio de `api.github.com`, não de `ui.shadcn.com`.

**Se qualquer um falhar — ⛔ pare e resolva antes de seguir.** Não contorne com shadcn público, não hand-rolle componente, não siga "por enquanto".

**Como resolver:** pedir ao dono do repositório um **Personal Access Token** do GitHub com leitura em `DiogoRother-it/centralit-boilerplate`, e persistir:

```bash
export CENTRALIT_TOKEN=<token>
```

No Windows (PowerShell): `$env:CENTRALIT_TOKEN = "<token>"`. Para persistir, adicionar ao perfil (`~/.bashrc`, `~/.zshrc` ou `$PROFILE`).

Se o `components.json` não tiver o bloco `registries`, o procedimento completo está em `docs/registry.md` no boilerplate.

**Pré-requisitos, os dois:** acesso de leitura ao repo privado `centralit-boilerplate` (login normal do GitHub, para o `git clone`) **e** o `CENTRALIT_TOKEN` no ambiente (para o registry). Confirme os dois; um sem o outro não sustenta a cadeia.

## Eco final

Antes de executar, repita em 2–3 linhas: *"Então: projeto **X**, vou montar o sandbox em **Z** — confirma?"*. Só então rode os comandos.

## Regras

- **Não idealiza nem desenha.** Prepara o terreno; a idealização começa no `px-start`.
- **Não faz a entrega.** Branch, push e MR são responsabilidade do `px-handoff`.
- **Nunca `git` na mão pro UX.** A skill executa; o UX só confirma.
- **Sandbox é o ateliê, não o produto.** Depois de entregue e mergeado, pode ser apagado.
- **Dois acessos, não um.** O `git clone` usa o login normal do GitHub; o registry `@centralit` exige `CENTRALIT_TOKEN`. Confirmar os dois no Passo 2b — ter um só é o estado que produz entrega errada em silêncio.
- **Procedência preservada.** ⛔ Nunca `rm -rf .git` no sandbox. Remote renomeado com push desabilitado; é o que permite ao `px-proto` medir a idade da base.
- **Falhar fechado.** Acesso ausente **bloqueia** o setup. Nunca cair no shadcn público como alternativa.

## Relação com o fluxo

```
px-setup (terreno)
   └─ monta sandbox (boilerplate)  ──►  px-start  →  px-intake  →  px-kickoff  →  px-request  →  px-proto  →  px-story  →  px-handoff
                                                                                                                            (fecha cadeia + git + MR)
```

> O `px-start` delega o terreno técnico pra cá. Sem duplicação de comando de git entre as duas.
>
> A entrega (branch + push + MR) é responsabilidade exclusiva do `px-handoff` — ele tem todo o contexto do pacote e fecha o ciclo completo.
