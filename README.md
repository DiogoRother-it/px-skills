# @centralit/px-skills

Instalador da **cadeia de skills PX/UX** da Central IT + os **docs de design system** que elas
referenciam. Feito para o **PX instalar as skills no repo do produto** (a base que o dev entrega
traz só a stack de componentes; as skills não vêm com ela).

## O que instala

- **12 skills de entrevista** (`px-*`) em `.claude/skills/`: `px-setup`, `px-start`, `px-audit`, `px-intake`, `px-kickoff`, `px-epic`, `px-proto`, `px-request`, `px-story`, `px-handoff`, `px-preview`, `px-sync`
- **2 skills de execução** (`ux-*`): `ux-flows` (registra uma jornada real como flow executável) e `ux-persona` (percorre o flow simulando uma persona — sente e depois diagnostica pela rubrica de usabilidade). Diferente das `px-*`, não são entrevista: rodam sobre o produto ao vivo (repo local ou URL), dentro do `px-audit` ou depois do handoff, junto do Playwright do dev.
- **Docs de design system** em `docs/design-system/` (foundations, components, patterns, engineering)
- **Protocolo** em `docs/px-protocol.md` (Protocolo de Interação UX + Skill Prompting Conventions)
- Um ponteiro pro protocolo no `CLAUDE.md` do repo (cria se não existir)

O pacote é **autossuficiente**: leva as skills e suas dependências de documentação juntas, então
não quebra se rodado num repo que ainda não tem o design system.

Toda atualização de skill é descrita no terminal ao instalar (seção "O que mudou") **e** fica
registrada no [`CHANGELOG.md`](CHANGELOG.md) — o terminal mostra só a versão mais recente, o
changelog guarda o histórico completo.

## Como instalar

Rode **dentro do repositório do produto** (o diretório atual vira o destino):

```bash
# direto do GitHub (sem publicar no npm)
npx github:DiogoRother-it/px-skills

# ou, após publicar no npm
npx @centralit/px-skills
```

Depois, abra o Claude Code nesse repo — as skills aparecem no menu `/`:
`/px-setup · /px-start · /px-audit · /px-intake · /px-kickoff · /px-epic · /px-proto · /px-request · /px-story · /px-handoff · /px-preview · /px-sync`
`/ux-flows · /ux-persona`

## Pré-requisito

A **biblioteca de componentes** (`src/components/ui/` + tokens em `src/index.css`) precisa estar
no repo para o trabalho de UI. Ela vem no **bundle do design system** entregue ao dev, não neste
pacote — este aqui é só a camada de skills + protocolo, para o PX.

## Duas portas de entrada

- **Projeto novo do zero** → comece por `/px-start`
- **Redesign de produto existente** → comece por `/px-audit` (analisa repo/URL ao vivo ou prints/PDF)

O **alvo de build** (decidido no `px-start`/`px-intake`/`px-kickoff`) escolhe o caminho de idealização: **app React do produto** (a partir do boilerplate) ou **protótipo HTML descartável** via `/px-proto` (stack própria só-CDN, valida o fluxo sem tocar no produto).

## Manutenção — canonicidade dividida (não inverter a direção)

Este pacote e o `centralit-boilerplate` são **acoplados**, mas cada um é canônico pra uma coisa:

| Conteúdo | Fonte da verdade | Cópia |
|---|---|---|
| **Skills** (`skills/`) | **px-skills** (aqui) | — nenhuma. O `px-setup` sempre instala fresco via `npx github:DiogoRother-it/px-skills`; não existe cópia local pra manter em dia. |
| **Protocolo** (`assets/px-protocol.md`) | **px-skills** (aqui) | boilerplate `docs/px-protocol.md` |
| **Docs de design-system** (`assets/design-system/`) | **centralit-boilerplate** (regras de uso de componente) | aqui, em `assets/design-system/` |

O boilerplate é a **biblioteca de componentes + regras de uso**; o px-skills é a **biblioteca de habilidades do UX**. Algumas skills (ex: `px-request`) **absorvem** as regras de uso que vivem no boilerplate — por isso uma regra de componente nova nasce **no boilerplate** e a skill reflete.

O sandbox do PX (`px-setup`) é o próprio boilerplate clonado — por isso `docs/design-system/` e `docs/px-protocol.md` precisam estar em dia **lá**: o instalador não sobrescreve o que já existe no destino. Skills não têm esse risco porque `.claude/skills/` é sempre reinstalado do zero a cada `npx`.

**Fluxo de edição:**
- **Regra de componente** → edite no **boilerplate** (`docs/design-system/`) → propague a cópia pra cá (`assets/design-system/`).
- **Protocolo** → edite **aqui** (`assets/px-protocol.md`) → propague pro boilerplate (`docs/px-protocol.md`).
- **Skill** → edite **aqui** (`skills/`) e suba a versão em `package.json` + o changelog do `install.mjs` (ver `CHANGELOG.md`) — não precisa propagar pra lugar nenhum, o próximo `npx` já leva a versão nova.

Ao sincronizar pro boilerplate, **nunca** `git add -A` (o working tree de lá costuma ter WIP do time) — stageie só os caminhos que você mudou.
