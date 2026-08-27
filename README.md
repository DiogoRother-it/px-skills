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
- Um **hook de sessão** em `.claude/hooks/check-versao.mjs`, declarado como `SessionStart` no `.claude/settings.json` do repo

O pacote é **autossuficiente**: leva as skills e suas dependências de documentação juntas, então
não quebra se rodado num repo que ainda não tem o design system.

Toda atualização de skill é descrita no terminal ao instalar **e** fica registrada no
[`CHANGELOG.md`](CHANGELOG.md). O terminal mostra **só o delta deste repo**: o instalador grava
a versão em `.claude/skills/.px-skills-version` e, na próxima instalação, resume apenas as
versões que aquele repo ainda não tinha (`1.11.1 → 1.13.0` lista as duas que faltavam). Quem já
está na versão atual não recebe resumo nenhum. O changelog guarda a íntegra.

## O hook de sessão

Ao abrir o Claude Code no repo, o hook checa três coisas e **só fala se alguma estiver errada**:

| Checagem | Quando dispara |
|---|---|
| Skills atrás da versão atual | sempre (o `px-skills` é público; cache de 6h, sem token) |
| Sandbox sem `boilerplate-upstream` | só em sandbox do PX |
| `CENTRALIT_TOKEN` ausente | só em sandbox do PX |

"Sandbox do PX" é detectado pelo bloco `registries.@centralit` no `components.json` — num repo
qualquer as duas últimas nem rodam.

**Silêncio quando está tudo certo é regra, não economia.** Um aviso que aparece toda sessão vira
ruído e as pessoas aprendem a ignorar, que é exatamente a falha que ele existe para evitar.

O hook nunca quebra a sessão: offline, VPN ou GitHub fora do ar terminam em silêncio. Ele também
não faz `git fetch` — rede no `SessionStart` trava a abertura e pode pedir credencial de repo
privado. A idade da base é medida pelo `px-proto` (Passo 3A), no momento em que ela importa.

O `settings.json` existente é **mesclado**, nunca sobrescrito: `permissions` e outros hooks
`SessionStart` são preservados, e reinstalar não duplica a entrada. Se o arquivo estiver
malformado, o instalador avisa e **não grava** — um `settings.json` quebrado desliga todas as
configurações daquele arquivo.

> **Limite:** o hook só existe onde o instalador rodou. Quem nunca mais rodar `npx` não o recebe;
> a primeira instalação a partir da 1.15.0 é que o planta.

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
- **Skill** → edite **aqui** (`skills/`) e faça as três coisas, na ordem: (1) suba a versão no `package.json` — **fonte única**, o `install.mjs` lê dela e nunca tem número escrito à mão; (2) escreva a entrada no `CHANGELOG.md`, que é a íntegra; (3) acrescente a chave da versão em `HIGHLIGHTS`, no fim do `install.mjs`, com **1 a 3 linhas de até ~74 colunas** — é o resumo curto que o UX lê no terminal ao puxar as skills. Não precisa propagar pra lugar nenhum, o próximo `npx` já leva a versão nova.

Ao sincronizar pro boilerplate, **nunca** `git add -A` (o working tree de lá costuma ter WIP do time) — stageie só os caminhos que você mudou.
