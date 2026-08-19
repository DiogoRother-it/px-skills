# Changelog

Todas as versões instaláveis via `npx github:DiogoRother-it/px-skills` / `npx @centralit/px-skills`.
O instalador imprime só a versão mais recente no terminal — o histórico completo vive aqui.

## 1.7.0 — 2026-08-19

**Fecha a classe de gap que fez a UI divergir na entrega SmartCity semana-33.** O dev recebeu o protótipo como referência visual e reimplementou no boilerplate; o front saiu inconsistente. A auditoria mostrou que a maior parte não era falha do dev: eram regras corretas que existiam **só no JS/CSS do protótipo**, além de três documentos citados pelas specs que nunca entraram no pacote. Os patches abaixo atacam a causa, não o sintoma.

**`px-request` — a spec passa a exigir o número, não o reconhecimento:**
- `BLOCO 9` ganha trava: *"sim, é calculado"* deixa de ser resposta suficiente. Toda regra derivada exige fórmula literal, formatação exata, escopo dos dados e **todo threshold, um por um, em tabela**. Antes, um `RN` do tipo "a prioridade é calculada a partir dos sinais vitais" passava pelo bloco sem nunca registrar os valores de corte — e quem implementa não tem como adivinhar um número.
- `BLOCO 9b` novo — **estado do dado → variante de UI**, obrigatório. Cobre a classe de regra que mais se perde no handoff, porque não é visível num print: a tela mostra só um dos estados. Exige tabela `estado → rótulo/variante/ícone`, mais visibilidade por papel, faixas numéricas que colorem, e conjuntos de coluna distintos quando duas telas reusam o mesmo componente.

**`px-story` — a história passa a trazer de volta o que o proto decidiu:**
- `S3b` novo — **varredura do JS/CSS do proto aprovado** (não só da tela renderizada). Trata **mock estático como ausência de regra** (`espera:'38min'` esconde que nunca houve fórmula), obriga conferir se o mesmo conceito usa o mesmo corte em todos os pontos da tela, e manda marcar números mágicos de mock como artefato, não requisito. Também obriga registrar divergência proto ↔ request em vez de silenciar, com a regra de precedência: a spec aprovada vence o proto desatualizado.

**`px-proto` — registra a anatomia no momento barato:**
- `Passo 8b` novo, obrigatório antes de aprovar: cada componente do inventário do Passo 1 ganha entrada em `anatomia-visual.md` com valores exatos e a coluna **Origem** (default da lib × override do projeto). Registra também bespoke sem equivalente, gambiarra de protótipo que não deve ser replicada, e equivalência de biblioteca. A informação está na mão de quem constrói; depois vira arqueologia de CSS.

**`px-handoff` — consolida, cobra e confere:**
- DoD exige `anatomia-visual.md` quando a entrega **atravessa fronteira de tecnologia**, e `mapa-de-consumo.md` quando **dev e PX usam a mesma biblioteca** — este classifica cada região em 🟢 consumir direto (não customizar) · 🟡 consumir + override · 🔴 compor, e lista os componentes da lib disponíveis e não usados. Sem ele o dev reconstrói do zero o que a lib entrega (tabela, paginação, drawer, toast, skeleton, date picker) e ao mesmo tempo assume como padrão da lib o que é identidade nossa.
- **Conferência de completude** virou trava: comparar `decisoes/` e `stories/` da origem com o pacote, arquivo por arquivo. Ausência sem justificativa bloqueia a entrega. Regra documentada que não é entregue equivale a regra inexistente.

**Divisão de responsabilidade:** a `px-proto` **escreve** a anatomia, a `px-handoff` **cobra**. Não foi criada skill nova — uma skill que rodasse só no fim teria que fazer engenharia reversa de todo o CSS, exatamente o trabalho caro que esta versão elimina.

## 1.6.0 — 2026-08-18

**Duas skills novas de execução** (`ux-*`, não são entrevista — rodam sobre o produto ao vivo):
- `ux-flows` — registra uma jornada multi-tela como flow executável em `e2e/flows/`, compilando de `px-story` já prontas ou perguntando direto quando não há.
- `ux-persona` — percorre o flow em duas fases isoladas: um subagente cego assume uma das 6 personas bundled (`novice`, `rushed`, `skeptical`, `mobile`, `accessibility`, `power-user`) e navega o produto de verdade narrando em primeira pessoa; depois o UX Designer diagnostica cada fricção pela rubrica de 7 dimensões já usada em `px-audit`/`px-story` (Descoberta, Clareza, Feedback, Fricção, Sem beco sem saída, Fidelidade, Autenticidade de dados). Recusa rodar contra mockup estático.
- As duas já eram citadas por nome em `px-audit`, `px-story`, `px-kickoff` e `px-epic` — preenchem uma lacuna que existia desde antes desta versão.

**`px-sync` trazida pro pacote central:**
- Existia solta, presa num único projeto (gitignorada, fora de qualquer canal de distribuição). Agora é genérica e instalável em qualquer projeto: sincroniza o estado completo de trabalho (produto + `planning/` + `docs/`) com o repositório central do PX, sempre `main` fast-forward e gated por aceite explícito.
- `px-handoff` agora pergunta, na abertura, se o projeto mantém um repositório central do PX — se sim, delega pro `px-sync` ao final (destino independente do pacote reduzido que vai pro dev).
- `docs/px-protocol.md` atualizado pra descrever os dois destinos possíveis do `px-handoff` e corrigido quanto à afirmação "nenhuma skill roda git", que já estava desatualizada (o `px-handoff` sempre fez push via branch órfã).

**Manutenção:**
- Removida do README a promessa de propagar skills pro boilerplate (`docs/skills-draft/`) — confirmado que esse espelho não tem consumidor (nada no boilerplate o lê, e o `px-setup` sempre instala as skills frescas via `npx github:DiogoRother-it/px-skills`, nunca de uma cópia local). A propagação de `docs/design-system/` e `docs/px-protocol.md` continua — essas sim são lidas quando o sandbox do PX é o boilerplate clonado.

## 1.5.0 — 2026-08-06

- `px-story`/`px-handoff`: bloco **S4b — Fluxo principal (passo a passo)**, o mapa de revisão rápida da jornada antes do BDD; template `handoff-manifest.md` pro recorte dev-facing vs. interno.
- `px-change` (nova skill): faixa leve para alteração localizada em tela que já existe (campo, ícone, label, paginação) — 5 blocos enxutos (propósito, estados impactados, ancoragem DS, copy, lint), sem passar pela entrevista completa do `px-request`. Gate de tamanho: se crescer para tela/fluxo novo, encaminha pro `px-request`.
- Roteamento PX embutido em `px-start`/`px-intake`/`px-request`/`px-change`: projeto com UI Kit definido sempre entra pela cadeia PX, nunca pelo pre-coding-pass global.
- Proibições de travessão/caixa alta reforçadas em `px-draw`/`px-kickoff`.

## 1.4.2 — 2026-07-16

- `px-proto`: gate explícito de ambiguidade de variação antes de codar + inventário público de todos os widgets → componente shadcn. Tabela nativa / badge manual / tooltip ausente passam a ser proibidos quando o shadcn já resolve.

## 1.4.1 — 2026-07-16

- `px-proto`: migração para Vite/localhost com componentes reais (antes era mockup estático).

## 1.4.0 — 2026-07-16

- `px-proto` (nova skill): validação visual obrigatória depois de cada `px-request` — protótipo HTML standalone com os tokens reais do UI Kit antes de virar `px-story`.

## 1.3.0 — 2026-07-15

- `px-handoff`: correções baseadas em execução real de sprint.

## 1.2.0 — 2026-07-15

- `px-handoff`: entrega limpa — HTML + UI Kit + histórias de negócio, sem artefato interno.

## 1.1.0 — 2026-07-10

- `px-preview` (nova skill): empacotamento standalone do produto pra revisão interna antes do handoff.

## 1.0.0

- Primeira versão instalável da cadeia PX/UX.
