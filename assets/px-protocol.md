# Protocolo de Interação UX/PX — Central IT

> Documento portátil que acompanha as skills PX. As skills referenciam estas seções por nome
> ("Protocolo de Interação UX", "Skill Prompting Conventions"). Mantenha-o no repo do produto
> (ou aponte o `CLAUDE.md`/`AGENTS.md` do projeto para ele) para as skills operarem sem buraco.

> **Origem canônica.** As **regras de uso de componente** (`docs/design-system/*`) são canônicas no **centralit-boilerplate** (a biblioteca de componentes). As **skills** e este **protocolo** são canônicos no **px-skills**. Regra de componente nova nasce no boilerplate; a skill a absorve. Não inverta a direção ao editar.

## Hierarquia de documentos

1. `docs/design-system/ds-foundations_v4.md` — tokens, escalas, princípios de base
2. `docs/design-system/ds-components_v4.md` — specs de componente + árvores "Qual usar?" + mapeamento shadcn/ui
3. `docs/design-system/ds-patterns.md` — estruturas de tela reutilizáveis
4. `docs/design-system/Engineering-directives_v4.md` — como as regras viram código
5. `src/index.css` — tokens visuais reais do projeto (prevalece para valor de cor)
6. `src/components/ui/<componente>.tsx` — **a fonte de anatomia**, e a mais atual das seis
7. `src/showcase/` — exemplo de composição. **Auditável, nunca verdade**

**Em conflito, por tipo de pergunta:**

| A pergunta é sobre | Manda |
|---|---|
| Anatomia (partes, props, o que já vem pronto) | o `.tsx` do componente |
| Comportamento e regra de uso | os documentos de DS |
| Valor de cor | o `src/index.css` |
| Exemplo de composição | o `showcase/`, conferido contra os dois de cima |

> **O `.tsx` entrou nesta lista por causa de defeito medido.** A hierarquia antiga parava no
> CSS, e com isso a fonte mais completa do design system ficava de fora: **17 dos 53
> componentes não têm entrada própria no `ds-components_v4.md`**, e os que têm não descrevem
> as decisões que os comentários do arquivo tomam. Uma cadeia inteira de especificação e
> revisão deixou passar seis divergências do DS lendo só os documentos.
>
> **O `showcase/` é auditável, nunca verdade.** Ao copiar dele, confira contra a spec e
> contra o `.tsx`; divergiu, a spec ganha e o showcase vira débito registrado.

## Regras não-negociáveis

- Componentes sempre via `npx shadcn add [nome]`; nunca copiar de outra fonte manualmente.
- **Protótipo de handoff nasce no boilerplate, em TSX, com os componentes reais. Nunca em HTML vanilla nem via CDN.** O que atravessa pro dev é o **fonte da UI**; HTML standalone é preview pra PO (`px-preview`), nunca referência de implementação. Medido em 2026-09-18: SmartCity semana-37 e CIT Contracts saíram como HTML de 3 mil a 34 mil linhas sem uma classe Tailwind, enquanto o dev usava a mesma biblioteca que nós componente por componente. A LLM do dev reinterpretou o HTML inteiro e cada dev obteve um resultado diferente.
- Nunca aceitar o visual default do shadcn sem reestilizar para bater com o design system.
- Espaçamento sempre em múltiplos de 8px (`lint:spacing` antes de dar por pronto).
- Ícones via Lucide, tamanho por prop `size` (16/20/24).
- Radius sempre via `--radius`; cor sempre via token (nunca hex no `className`).
- Sem travessão e sem caixa alta total em texto de interface.
- Apenas 1 botão primário por tela/contexto.
- **Tabela sem rolagem horizontal** — se as colunas não cabem, reduzir/realocar colunas (priorizar, expansão, drawer de detalhe), nunca ativar `overflow-x`. Ver Table família em `ds-components_v4.md`.
- **Um overlay por vez, nunca empilhar** — proibido Modal sobre Modal, Popover sobre Modal, Popover sobre Drawer; sempre *switch* (fecha um, abre o outro). Única sobreposição aceita: **Drawer pode disparar Modal/Dialog**. Ver Overlay/Surface em `ds-components_v4.md`.
- Componente sem equivalente no shadcn/Radix: compor com primitivas e documentar (exceção: Data Grid avançado via TanStack Table).
- **Divergência do design system é declarada com motivo, ou é defeito.** Vale para componente que está **dentro** do catálogo e é usado diferente do que a spec ou o `.tsx` mandam: default trocado, parte omitida, anatomia alterada, composição à mão onde existe componente pronto. Onde declarar: `px-request` Bloco 11c e `px-proto` Passo 4b. O gate ⚠️ cobre o que **não** existe no catálogo; este cobre o que existe.

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
- **Passo 4 — Estados + handoff:** cobrir a matriz de estados (default/loading/empty/error/disabled/read-only/…), mock data, e seguir o handoff → dev (fechado pela `px-handoff`).

> Abrangência: vale para TODO componente, por mais trivial. Nenhum componente entra sem propósito (Passo 0) e estados (Passo 4).

## Handoff → dev (obrigatório)

- O fechamento é a skill **`px-handoff`**: monta o pacote (escopo entregue, Definition of Done, flows/personas, fronteiras de integração e o **carimbo de sprint**) e despacha a mecânica de git pra `px-setup` Passo 4.
- **A forma da entrega é verificada, nunca perguntada.** A `px-handoff` inspeciona o repo do dev (`package.json`, pasta `components/ui`, alias de import, CSS de tokens). Dev com shadcn + Tailwind → o **fonte da UI é obrigatório**, com os imports reescritos pro alias do dev. Só um repo **sem** shadcn justifica o caminho de referência visual, e a evidência vai escrita no `handoff.md`. "Stack diferente" declarado sem evidência é declaração inválida.
- **Cada artefato declara o público, e engenharia só recebe da `px-handoff`.** O pacote é para o dev; o preview navegável (`px-preview`) é para PO, stakeholder, cliente e usuário. Mandar HTML por chat, e-mail ou Teams para o dev não é atalho de entrega: é o formato errado no canal errado, sem versão e sem procedência.
- Trabalhar em branch **por funcionalidade/fluxo** (`ux/<funcionalidade>`) a partir da `main` — nunca commit direto; integração via Merge Request. Num repo real a branch nasce no início; no sandbox, na entrega.
- **Sprint é carimbo de entrega, não de branch** — a branch atravessa sprints. O sprint vai no título do MR (`[Sprint NN] ux(<funcionalidade>): ...`) e no campo `Sprint` do `PX-PROGRESS`.
- Validação visual completa via Playwright: todas as telas e todos os estados
  (default/loading/empty/error/disabled/read-only/hover/foco/responsivo), **meta de 99% de fidelidade**,
  evidências anexadas ao MR.

## Skill Prompting Conventions

- **Decisões enumeráveis** (variação, modo, sim/não, caminho, fonte) → pergunta estruturada (`AskUserQuestion`), 2–4 opções, recomendada marcada `(Recomendado)`.
- **Valores livres** (nome de iniciativa em kebab-case, slug, copy, cores de marca) → texto livre.
- **Gate de governança** — qualquer "Outro"/fora do catálogo é marcado ⚠️ REQUER VALIDAÇÃO UX/PX e não avança sem aprovação.
- **No-pause mode** — se o líder pediu para não pausar, converter cada pergunta em item de *Perguntas em aberto* e seguir com a recomendação de maior confiança. Exceção: o gate ⚠️ do "Outro" nunca é auto-resolvido.
- **Idioma** — artefatos no idioma do usuário (pt-BR), com acentuação correta.

## Cadeia de skills PX

`px-start` (projeto novo) **ou** `px-audit` (redesign de produto existente) → `px-intake` (problema vago) → `px-kickoff` (personas + UI KIT) → `px-epic` (se iniciativa) → `px-request` (por tela) → **`px-proto`** (protótipo visual fiel → PX valida e aprova) → `px-story` (história + BDD) → `ux-flows` (jornada) → `px-tour` (onboarding guiado do fluxo) → [`px-preview` — opcional, revisão da equipe interna] → `px-handoff` (fecha: DoD + sprint + flows), que despacha pra até dois destinos independentes: `px-setup` Passo 4 (branch `ux/<funcionalidade>` + Merge Request) → dev valida com `ux-flows`/`ux-persona` + Playwright; **e/ou** `px-sync` → repo central do PX (espelho completo, pra outro PX continuar idealizando).

**`px-proto` (obrigatório após cada `px-request`).** Constrói a tela **dentro do boilerplate** (Vite + localhost), em **duas pastas**: `src/<produto>/` (a UI, em TSX, com os componentes reais do `src/components/ui/` e os tokens reais do `src/index.css`) e `src/proto/` (a demo descartável: seletor de papel e estado, fixtures). O PX revisa no localhost com HMR, itera e só aprova quando está correto. Nenhuma tela vira `px-story` sem passar pelo proto aprovado. ⛔ **Nunca gera HTML standalone, vanilla ou via CDN**: a versão anterior deste parágrafo dizia o contrário e foi a porta por onde meses de entrega saíram como HTML sem componente. O fonte de `src/<produto>/` é o que a `px-handoff` entrega ao dev.

**`px-preview` (opcional, para revisão interna).** Empacota o app React do produto (boilerplate já construído) num HTML standalone para a equipe interna revisar o conjunto de telas antes de fechar o handoff para os devs. Posiciona-se depois do `px-story` e antes do `px-handoff`. Diferente do `px-proto`: requer o app funcionando; diferente do `px-handoff`: é revisão, não entrega.

**`px-tour` (ao fechar cada fluxo lógico, antes da `px-handoff`).** Gera o onboarding guiado sobre o componente Onboarding Guiado do DS: um tour acionável por fluxo lógico (= um flow do `ux-flows`) e um tour global que encadeia todos, filtrados em runtime pelas permissões do usuário (RBAC granular, nunca tour por perfil). Compila de artefatos prontos (flow, histórias, requests, relatórios do `ux-persona`); não inventa passo, âncora nem permissão. A `px-handoff` leva `tours/` no pacote e o GATE confere as âncoras.

**`px-sync` (opcional, quando há repo central do PX).** Sobe o espelho completo de trabalho (produto + `planning/` + `docs/`) pro repo central, sempre `main` fast-forward e gated por aceite explícito. Independente do `px-handoff`: um entrega pro dev (pacote reduzido), o outro sincroniza o time de PX (espelho completo).

O terreno técnico (repo/branch/scaffold) do produto é sempre da `px-setup`. `px-handoff` e `px-sync` também rodam git, mas só no próprio destino gated e sempre com aceite explícito antes do push (branch órfã pro dev; `main` fast-forward pro repo central) — nunca no terreno técnico que a `px-setup` já preparou.

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
**Alvo de build:** App React (boilerplate)
**Stack do dev (verificada):** <shadcn + Tailwind sobre <Radix | Base UI>, alias `<prefixo>` · repo <URL/branch> em <data> | sem shadcn: referência visual, evidência no handoff.md | ainda não verificada>
**Branch:** ux/<funcionalidade>
**Sprint:** <Sprint NN · AAAA-Www | a definir na px-handoff>

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
