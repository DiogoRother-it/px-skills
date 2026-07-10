---
name: px-start
description: Porta de entrada de PROJETO NOVO neste design system. É o "comece aqui" da cadeia PX — orienta o líder UX em 3 linhas, faz o scaffold do projeto a partir do boilerplate, e roteia pro próximo passo (px-intake se o problema ainda é vago, px-kickoff se já é hora de definir identidade). Não produz spec nem código de tela: ele prepara o terreno e despacha. Use ao iniciar um projeto do zero — "vou começar um projeto novo", "comecei um repo novo do boilerplate", "por onde começo esse projeto", "setup inicial".
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: start
---

# px-start — a porta de entrada de projeto novo

Todo projeto novo sobre este design system **começa aqui**. Esta skill não desenha tela nem escreve código: ela **orienta**, **prepara o terreno** e **despacha** pro próximo passo certo da cadeia PX. É o "comece aqui" — o que impede um projeto de nascer sem público-alvo, sem UI KIT, ou pulando direto pra implementação.

**Público desta skill:** o líder UX/PX (por ora não é o onboarding do não-UX — isso fica pra depois). Então seja direto: sem trilha pedagógica longa, só o essencial pra destravar o começo.

Contexto inicial via slash: `$ARGUMENTS` (nome/ideia do projeto). Se vazio, pergunte o que a pessoa vem começar.

## Prompting

Segue `Skill Prompting Conventions` do `CLAUDE.md`. Estruturada pra decisões enumeráveis (é projeto novo?, onde vive, próximo passo); livre pra nome do projeto. Toda pergunta traz o porquê + default recomendado; eco ao final.

## Passo 0 — Isto é mesmo um projeto novo?

Antes de tudo, confirme o cenário — porque o começo muda tudo:

- **Projeto novo do zero** (sem repo/identidade ainda) → segue nesta skill.
- **Projeto já existe, quero uma tela nova** → não é aqui: vá pro `px-request` (ou `px-epic` se for várias telas).
- **Tenho só uma ideia/problema vago, nem sei o tamanho** → o próprio `px-start` te leva pro `px-intake` no Passo 3.

Se não é projeto novo, encaminhe e encerre — não force o fluxo de setup.

## Passo 1 — Terreno pronto? (delega pra `px-setup`)

**Decidir:** o terreno técnico (repo/branch/scaffold) já existe? Onde a cadeia PX vai gravar?
**Por que importa:** a cadeia PX escreve artefatos em `planning/<iniciativa>/` e a identidade em `src/index.css`. Sem o esqueleto, os próximos passos não têm onde gravar. Mas a **mecânica de git/scaffold é da `px-setup`** — o `px-start` não repete comando de repositório.
**Fazer:**
- Confirme a raiz do projeto (o repo). Se ambíguo, pergunte antes de escrever qualquer coisa.
- **Se o terreno ainda não está preparado** (sem sandbox nem repo do dev clonado) → encaminhe pra **`px-setup`**, que monta o sandbox a partir do boilerplate ou clona o repo do dev e cria a branch `ux/<projeto>`. Volte pra cá depois.
- **Alvo de build** (`AskUserQuestion`): *App React do produto a partir do boilerplate (Recomendado)* × *Protótipo HTML descartável (via `agile-proto`, stack própria)*. Muda onde a identidade é aplicada e o que "pronto" significa. Essa decisão é de idealização e fica aqui.
- Se for protótipo, aponte pro `agile-proto` como manual técnico — a decisão já vem registrada.

## Passo 2 — Orientar (a cadeia PX em 3 linhas)

Mostre o caminho pra quem está começando, sem enrolação:

```
px-start (aqui)  →  px-intake (clareia o problema, se vago)
                 →  px-kickoff (público-alvo + UI KIT — a identidade do projeto)
                 →  px-epic (só se for iniciativa com várias telas)
                 →  px-request (spec por tela)  →  px-story (história + BDD)  →  handoff → dev
```

Uma frase por etapa é suficiente. O objetivo é a pessoa saber onde está e o que vem — não decorar o fluxo inteiro.

## Passo 3 — Rotear (o despacho)

**Decidir:** qual é o próximo passo real deste projeto.
**Por que importa:** é a função central do `px-start`. Rotear errado faz a pessoa pular a identidade ou detalhar tela cedo demais.
**Perguntar (`AskUserQuestion`, recomendada marcada):**
- **O problema ainda está vago / não sei o tamanho** → **`px-intake`** (clareia e decide o caminho). *Recomendado quando há dúvida.*
- **Já sei que é um projeto novo e quero definir a identidade agora** → **`px-kickoff`** (público-alvo + UI KIT).
- **Já tenho a identidade e é um sistema (várias telas)** → **`px-epic`** (decompor em backlog de telas).

Registre a recomendação e confirme antes de disparar a próxima skill.

## Eco final

Antes de encerrar, repita em 3–4 linhas: *"Então: projeto **X**, alvo **Y**, terreno preparado em **Z**, próximo passo **`px-…`** — confirma?"*. Só então dispare a skill escolhida.

## Regras

- **Não produz spec nem código.** O `px-start` prepara e despacha; quem gera artefato é a skill de destino.
- **Nunca pula a identidade.** Um projeto novo não vai pra `px-request` sem ter passado por `px-kickoff` (público-alvo + UI KIT). Se a pessoa quiser pular, avise o risco e registre.
- **Não é o onboarding do não-UX** (ainda). Se aparecer alguém sem repertório de UX, oriente que a trilha guiada pra não-UX é trabalho futuro; por ora, conduza você.

## Relação com o fluxo

```
px-setup (terreno)  →  px-start  →  px-intake  →  px-kickoff  →  px-epic  →  px-request  →  px-story  →  handoff → dev
                       ^ você está aqui (a porta de entrada de todo projeto novo)
```

> A `px-setup` prepara o terreno técnico (sandbox/clone/branch) e faz a entrega pro repo do dev; o `px-start` orienta e despacha a idealização. Se o terreno ainda não existe, passe pela `px-setup` antes.
