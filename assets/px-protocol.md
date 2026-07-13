# Protocolo de Interação UX/PX — Central IT

> Documento portátil que acompanha as skills PX. As skills referenciam estas seções por nome
> ("Protocolo de Interação UX", "Skill Prompting Conventions"). Mantenha-o no repo do produto
> (ou aponte o `CLAUDE.md`/`AGENTS.md` do projeto para ele) para as skills operarem sem buraco.

## Hierarquia de documentos

1. `docs/design-system/ds-foundations_v4.md` — tokens, escalas, princípios de base
2. `docs/design-system/ds-components_v4.md` — specs de componente + árvores "Qual usar?" + mapeamento shadcn/ui
3. `docs/design-system/ds-patterns.md` — estruturas de tela reutilizáveis
4. `docs/design-system/Engineering-directives_v4.md` — como as regras viram código
5. `src/index.css` — tokens visuais reais do projeto (prevalece para valor de cor)

Em conflito: o CSS real prevalece para valor visual; os documentos prevalecem para comportamento e regra.

## Regras não-negociáveis

- Componentes sempre via `npx shadcn add [nome]`; nunca copiar de outra fonte manualmente.
- Nunca aceitar o visual default do shadcn sem reestilizar para bater com o design system.
- Espaçamento sempre em múltiplos de 8px (`lint:spacing` antes de dar por pronto).
- Ícones via Lucide, tamanho por prop `size` (16/20/24).
- Radius sempre via `--radius`; cor sempre via token (nunca hex no `className`).
- Sem travessão e sem caixa alta total em texto de interface.
- Apenas 1 botão primário por tela/contexto.
- Componente sem equivalente no shadcn/Radix: compor com primitivas e documentar (exceção: Data Grid avançado via TanStack Table).

## Protocolo de Interação UX (obrigatório antes de qualquer UI)

A IA nunca desenha a partir de um prompt vago. Interroga o propósito e ancora na biblioteca. Dois níveis:

### Nível Projeto — uma vez, ao iniciar um projeto novo
- **Setup A — Público(s)-alvo:** identificar todos os papéis. Nunca assumir público único sem confirmar.
- **Setup B — UI KIT / identidade:** a IA gera o UI KIT a partir de inputs do líder (cores, referências, tom); o líder valida. Materializado em `src/index.css` + styleguide (`uikit-[projeto].html`). Nenhum token entra sem validação do líder.

### Nível Tela/Componente — recorrente, a cada pedido
- **Passo 0 — Propósito primeiro:** objetivo de negócio, público, onde vive. Pedido vago → não construir.
- **Passo 1 — Ancorar na biblioteca:** consultar `ds-components_v4.md`. O pedido mapeia para uma família com variações. Reusar antes de criar.
- **Passo 2 — Recomendar + perguntar:** recomendar a variação (justificar pelo "Quando usar"), listar alternativas, perguntar. Se o comando já nomeou a variação, confirmar em eco e seguir.
- **Passo 3 — "Outro" (fora do catálogo) = gate:** marca **⚠️ REQUER VALIDAÇÃO UX/PX** e não avança sem aprovação do líder.
- **Passo 4 — Estados + handoff:** cobrir a matriz de estados (default/loading/empty/error/disabled/read-only/…), mock data, e seguir o handoff → dev.

> Abrangência: vale para TODO componente, por mais trivial. Nenhum componente entra sem propósito (Passo 0) e estados (Passo 4).

## Handoff → dev (obrigatório)

- Trabalhar em branch intermediária a partir da `main` (nunca commit direto; integração via PR).
- Validação visual completa via Playwright: todas as telas e todos os estados
  (default/loading/empty/error/disabled/read-only/hover/foco/responsivo), **meta de 99% de fidelidade**,
  evidências anexadas ao PR.

## Skill Prompting Conventions

- **Decisões enumeráveis** (variação, modo, sim/não, caminho, fonte) → pergunta estruturada (`AskUserQuestion`), 2–4 opções, recomendada marcada `(Recomendado)`.
- **Valores livres** (nome de iniciativa em kebab-case, slug, copy, cores de marca) → texto livre.
- **Gate de governança** — qualquer "Outro"/fora do catálogo é marcado ⚠️ REQUER VALIDAÇÃO UX/PX e não avança sem aprovação.
- **No-pause mode** — se o líder pediu para não pausar, converter cada pergunta em item de *Perguntas em aberto* e seguir com a recomendação de maior confiança. Exceção: o gate ⚠️ do "Outro" nunca é auto-resolvido.
- **Idioma** — artefatos no idioma do usuário (pt-BR), com acentuação correta.

## Cadeia de skills PX

`px-start` (projeto novo) **ou** `px-audit` (redesign de produto existente) → `px-intake` (problema vago) → `px-kickoff` (personas + UI KIT) → `px-epic` (se iniciativa) → `px-request` (por tela) → `px-story` (história + BDD) → handoff → dev valida com `ux-flows`/`ux-persona` + Playwright.

## Checkpoint de progresso (PX-PROGRESS) — obrigatório

A cadeia PX é longa e roda em várias sessões de chat. Quando o contexto de um chat é resumido/perdido, o que falta pra retomar não é "mandar continuar" — é **saber exatamente onde o trabalho parou**. Por isso, **toda skill da cadeia grava um checkpoint** ao concluir seu passo. Retomar então nunca precisa de skill dedicada: em um chat novo, basta *"leia o `PX-PROGRESS.md` da iniciativa e continue de onde parou"*.

**Onde:** `planning/<iniciativa>/PX-PROGRESS.md` — um por iniciativa/produto, na raiz da pasta de planejamento (junto dos artefatos que a cadeia já grava). Versionado no Git; entra no PR do handoff sem custo. Para redesign, use o mesmo slug de produto do `px-audit` (`planning/<produto>/PX-PROGRESS.md`).

**Quando gravar:** no fecho de cada skill, **depois** da Definition of Ready e do eco final, **antes** de disparar a próxima skill. Se o arquivo não existe, criar; se existe, **atualizar** (nunca duplicar) — marcar o passo concluído em *Feito*, mover o foco pra *Próximo passo*, e sincronizar *Decisões travadas* e *Perguntas em aberto*.

**De onde vem o conteúdo (não inventar):** o estado real dos artefatos da iniciativa + as decisões já ecoadas na sessão. *Decisões travadas* espelha as Premissas confirmadas e os gates ⚠️ **REQUER VALIDAÇÃO UX/PX** já aprovados (com quem aprovou e quando); *Perguntas em aberto* espelha a lista de pendências com dono (no-pause mode). O checkpoint é o registro citável desse estado — é, na prática, o prompt de continuidade versionado (CLAUDE.md › regra 17).

**Formato (seguir):**

```markdown
# PX-PROGRESS — <iniciativa>

> Checkpoint da cadeia PX. Para retomar em um chat novo:
> "Leia planning/<iniciativa>/PX-PROGRESS.md e continue de onde parou."

**Etapa atual:** <skill · foco>
**Última atualização:** <AAAA-MM-DD>
**Alvo de build:** <App React (boilerplate) | Protótipo HTML>

## Feito
- [x] <skill> — <resultado em 1 linha + caminho do artefato>

## Em andamento
- [ ] <skill> — <foco atual>

## Decisões de produto travadas
- <decisão> (<Premissa confirmada | ⚠️ gate aprovado por <líder> em <data>>)

## Próximo passo
<skill + o que fazer>

## Perguntas em aberto
- <pendência> — dono: <nome>  (ou "nenhuma")
```
