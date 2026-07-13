# @centralit/px-skills

Instalador da **cadeia de skills PX/UX** da Central IT + os **docs de design system** que elas
referenciam. Feito para o **PX instalar as skills no repo do produto** (a base que o dev entrega
traz só a stack de componentes; as skills não vêm com ela).

## O que instala

- **10 skills** em `.claude/skills/`: `px-setup`, `px-start`, `px-audit`, `px-intake`, `px-kickoff`, `px-epic`, `px-request`, `px-story`, `px-handoff`, `px-preview`
- **Docs de design system** em `docs/design-system/` (foundations, components, patterns, engineering)
- **Protocolo** em `docs/px-protocol.md` (Protocolo de Interação UX + Skill Prompting Conventions)
- Um ponteiro pro protocolo no `CLAUDE.md` do repo (cria se não existir)

O pacote é **autossuficiente**: leva as skills e suas dependências de documentação juntas, então
não quebra se rodado num repo que ainda não tem o design system.

## Como instalar

Rode **dentro do repositório do produto** (o diretório atual vira o destino):

```bash
# direto do GitHub (sem publicar no npm)
npx github:DiogoRother-it/px-skills

# ou, após publicar no npm
npx @centralit/px-skills
```

Depois, abra o Claude Code nesse repo — as skills aparecem no menu `/`:
`/px-setup · /px-start · /px-audit · /px-intake · /px-kickoff · /px-epic · /px-request · /px-story · /px-handoff · /px-preview`

## Pré-requisito

A **biblioteca de componentes** (`src/components/ui/` + tokens em `src/index.css`) precisa estar
no repo para o trabalho de UI. Ela vem no **bundle do design system** entregue ao dev, não neste
pacote — este aqui é só a camada de skills + protocolo, para o PX.

## Duas portas de entrada

- **Projeto novo do zero** → comece por `/px-start`
- **Redesign de produto existente** → comece por `/px-audit` (analisa repo/URL ao vivo ou prints/PDF)

## Manutenção

As skills e os docs aqui são **cópias** das versões canônicas no repo `centralit-boilerplate`.
Ao evoluir as skills/docs lá, ressincronize este pacote e suba a versão em `package.json`.
