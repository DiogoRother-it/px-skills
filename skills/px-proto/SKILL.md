---
name: px-proto
description: Cria a tela do protótipo dentro do boilerplate (Vite + localhost) usando os componentes reais do shadcn, os tokens reais do UI KIT e mock data do px-request. Constrói em DUAS pastas obrigatoriamente: a UI, que é destinada à produção e o dev copia sem editar, e o andaime do protótipo (seletores de papel e estado, dados de exemplo), que é descartável. O PX trabalha no localhost com HMR — vê, ajusta, aprova. Obrigatório após o px-request e antes do px-story. Use quando o líder disser "gera o proto", "quero ver como fica", "prototipar a tela", "visualizar a spec", ou ao fechar um px-request.
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: proto
---

# px-proto — protótipo visual no boilerplate (Vite + localhost)

Esta skill cria o protótipo da tela **dentro do boilerplate**, usando os componentes reais do shadcn/ui, os tokens reais do `src/index.css` e o servidor de desenvolvimento Vite. O PX vê a tela no localhost com HMR — ajusta em tempo real, aprova — e só então a tela vira história (`px-story`).

**A tela nasce em duas pastas, e a distinção importa mais que qualquer outra regra desta skill:** `src/<produto>/` guarda a **UI, que é destinada à produção** e é entregue ao dev com a instrução de copiar sem editar; `src/proto/` guarda o **andaime**, que é descartável. Tratar o protótipo inteiro como descartável é o que produz código que o dev não consegue reaproveitar, e é a causa raiz da divergência visual entre protótipo e implementação.

**Por que no boilerplate:** componentes reais, tokens reais, HMR. Standalone HTML via CDN é uma aproximação — aqui é o mesmo stack do produto, só com mock data e diretório separado.

> **Este fonte vai ser COPIADO por outro time, não lido.** Quando o dev implementa na mesma stack, a `px-handoff` entrega `src/<produto>/` com a instrução de copiar sem editar. Escreva pensando nisso: nome de variável que se explica, `// INTEGRATION BOUNDARY:` nas fronteiras, e nenhum truque que você não queira ver rodando em produção. É o que permite fidelidade 1:1 sem ninguém redesenhar a partir de screenshot, e sem ninguém redigitar centenas de decisões visuais.
>
> **Se o dev precisar editar um arquivo da camada de UI para rodar no projeto dele, é defeito nosso** e conserta-se na origem. O andaime é outra história: `src/proto/` não é biblioteca, não é pacote, não vai para produção, e o PX não mantém. A fronteira de propriedade está registrada na `px-handoff`.

**Por que obrigatório:** spec textual não substitui revisão visual. Erros de hierarquia, densidade, estados e copy só aparecem quando você vê a tela. Corrigir aqui é grátis; corrigir depois do dev é caro.

**Público:** o líder UX/PX. Esta skill conversa pouco e entrega depressa — mas faz as perguntas certas antes de codar, não depois.

Contexto inicial via slash: `$ARGUMENTS` (caminho do `px-request`, nome da tela, ou descrição). Se vazio, peça.

---

## Passo 0 — Ingerir a px-request

Leia `planning/<iniciativa>/requests/<slug>.md`. Extraia:

- **Tela / componente:** nome + propósito em 1 frase
- **Público principal:** papel + nível de familiaridade
- **Variação definida:** qual componente do catálogo (ex: "Table com Expansão")
- **Estados a cobrir:** lista do B7 (default, loading, empty, error, disabled, success)
- **Ações principais:** botões, menus, ações em linha
- **Mock data:** campos e valores (Bloco 4)

Se o `px-request` não existir ou estiver sem Definition of Ready, **pare**: rode `px-request` antes.

---

## Passo 1 — Inventário de componentes (obrigatório antes de escrever qualquer linha)

Liste todos os widgets da spec e mapeie cada um a um componente em `src/components/ui/`. Este mapeamento é **público** — mostre ao PX antes de codar.

**Formato:**

| Widget da spec | Componente em src/components/ui/ | Instalar? |
|---|---|---|
| Tabela de feed | `table.tsx` → `Table, TableBody...` | não |
| Badge de severidade | `badge.tsx` → `Badge` | não |
| Seletor de período | ⚠️ ambíguo — ver Passo 2 | — |
| Botão icon-only com tooltip | `button.tsx` + `tooltip.tsx` | não |
| Skeleton de loading | `skeleton.tsx` → `Skeleton` | não |

**Regras:**
- Se existe em `src/components/ui/` → usar obrigatoriamente, nunca reimplementar.
- Se não existe → `npx shadcn@latest add @centralit/<componente>` antes de codar. **O prefixo `@centralit/` é obrigatório.**
- ⛔ **`npx shadcn add <componente>` sem o prefixo é proibido.** A forma sem prefixo resolve no shadcn **público** e **funciona** — entrega o default `new-york` em vez do componente da Central IT. Não dá erro, não dá aviso: o proto inteiro nasce sobre a base errada e a `anatomia-visual.md` do Passo 8b registra os valores vanilla como se fossem "default do boilerplate — não customizar", instruindo o dev a preservar o que ele deve substituir. Foi exatamente esse o mecanismo do incidente do sandbox sem token.
- **Se o `add` do registry falhar** (401/404) → ⛔ **pare**. É acesso, não é componente faltando. Volte ao `px-setup` Passo 2b. Nunca instale a versão pública como contorno, nunca implemente o componente à mão.
- **Componente que não existe no registry** (52 itens em `public/r/`) → é decisão de design system, não de proto. Registre como Pergunta em aberto com dono; não invente primitiva.
- Se é ambíguo (mais de um componente possível) → vai para o Passo 2.
- `<table>` HTML nativo, `<span>` com classes manuais, `<button>` sem primitiva shadcn → **proibidos** quando existe equivalente no catálogo.

Componentes que **sempre** existem no boilerplate e **nunca** devem ser reimplementados:

| Elemento | Usar |
|---|---|
| Tabela (qualquer variação) | `Table, TableHeader, TableBody, TableRow, TableHead, TableCell` |
| Badge / status / chip | `Badge` com `variant` ou `className` |
| Botão icon-only | `Button size="icon"` + `Tooltip` obrigatório |
| Loading de bloco | `Skeleton` |
| Toast / feedback | `Sonner` (toast) |
| Confirmação destrutiva | `AlertDialog` |
| Qualquer overlay | `Dialog`, `Sheet` (drawer), `Popover` — nunca div posicionada |

---

## Passo 2 — Gate de ambiguidade (antes de codar)

Qualquer widget onde a variação de componente **não está explícita na px-request** gera uma pergunta — nunca uma escolha silenciosa. Elementos que tipicamente exigem confirmação:

| Padrão ambíguo | Pergunta obrigatória |
|---|---|
| Seletor de opções (período, filtro, modo) | ToggleGroup, Select dropdown, ou botões segmentados? |
| Ícone ao lado de texto ou em contexto de seção | Decorativo (muted) ou funcional (primary/destructive)? |
| Elemento que parece clicável mas spec não define ação | É clicável? O que acontece ao clicar? |
| Card com visual de destaque (borda, cor de fundo) | Aplica em todos ou só nos que têm condição de risco/alerta? |
| Header de tela | Breadcrumb com navegação ou só H1 (sem router nesta tela)? |
| Chips / pills | Display apenas ou filtros clicáveis? Se clicáveis, o que filtram? |

Use `AskUserQuestion` para esses casos — 2–4 opções com a recomendada marcada. Resolva todos antes de escrever a primeira linha de código. **Ambiguidade resolvida em silêncio = retrabalho garantido.**

---

## Passo 3 — Portão de procedência e ambiente

**Este passo falha fechado.** Qualquer item com ✗ **bloqueia o proto** — não existe "seguir por enquanto". Presença de arquivo não é procedência: um projeto Vite qualquer, com componentes vanilla e tokens escritos à mão, passa em todo teste de existência e reprova em todo teste de origem. Verificar de onde a base veio é o único jeito de a cadeia perceber que está construindo fora do padrão.

**A — Procedência da base (novo)**

1. **É uma cópia do boilerplate?** `git remote -v` deve mostrar `boilerplate-upstream` apontando pra `centralit-boilerplate`.
   - ✗ Sem remote nenhum → sandbox montado antes da 1.14.0 (quando o `px-setup` fazia `rm -rf .git`) **ou** projeto que nunca veio do boilerplate. Nos dois casos a procedência é indeterminável: **avise explicitamente** que a base não é auditável e ofereça remontar o sandbox pelo `px-setup`.
   - ✗ Remote de outro repo → não é o ateliê do PX. Pare.
2. **Qual a idade da base?** `git fetch boilerplate-upstream` e depois `git log --oneline HEAD..boilerplate-upstream/main | wc -l` + `git log -1 --format=%cd HEAD`.
   - **> 30 dias ou > 20 commits atrás** → ⚠️ avise o líder com o número exato antes de codar. Base velha não bloqueia, mas **precisa ser dita**: é o que distingue "decidimos trabalhar assim" de "ninguém sabia".
3. **Registry alcançável?** `CENTRALIT_TOKEN` no ambiente **e** bloco `registries.@centralit` no `components.json`.
   - ✗ → ⛔ **bloqueia.** Sem o token, todo `add` do Passo 1 cai no shadcn público em silêncio. Encaminhe pro `px-setup` Passo 2b.

**B — Ambiente**

4. Servidor rodando? Se não, `npm run dev` em background.
5. `src/index.css` tem os tokens do UI KIT? Se não, avise que o `px-kickoff` precisa materializar primeiro. (Os tokens também chegam por `npx shadcn@latest add @centralit/theme` — ver `docs/registry.md` no boilerplate.)
6. `docs/design-system/ds-components_v4.md` existe? O Passo 4 consulta esse catálogo. Se faltar, rode `npx github:DiogoRother-it/px-skills` — o instalador o entrega. **Nunca improvise a anatomia de memória**: catálogo ausente produz componente plausível e anatomia errada.
7. Todos os componentes do inventário (Passo 1) estão em `src/components/ui/`? Se não, instale os que faltam **pelo registry** (`@centralit/<nome>`), respeitando as regras do Passo 1.

**Registrar o resultado.** Anote no `PX-PROGRESS` a linha de procedência apurada aqui: commit da base, data, distância do `main` e versão das skills. É o dado que o `px-handoff` estampa no pacote — e sem ele nenhuma entrega é rastreável depois.

---

## Passo 4 — Mapear a variação no catálogo

Com a variação definida (px-request Bloco 6 + confirmações do Passo 2), consulte `docs/design-system/ds-components_v4.md`:

- **Anatomia:** partes do componente
- **Estados:** quais são específicos desta variação
- **Regras visuais:** sizing, spacing, comportamentos obrigatórios
- **Overlay:** regras de empilhamento (se aplicável)

**Variações do catálogo:**

| Família | Variações |
|---|---|
| Table | Básica · Com Interações (sort/select) · Com Expansão · Data Grid avançada |
| Card | Resumo · Informativo · Interativo |
| Select | Base · Com Busca · Multi · Async · Combobox |
| Date Picker | Single · Range · Date Time |
| Upload | Campo simples · Dropzone · Multi-arquivo |
| Overlay | Drawer · Modal · Dialog · AlertDialog · Popover |

---

## Passo 5 — Criar os DOIS arquivos do protótipo

> ⛔ **Nunca escreva a tela num arquivo só.** Todo protótipo nasce em duas pastas.
> Esta é a regra que mais impacta fidelidade visual no handoff, e não é negociável.

| Arquivo | O que contém | Destino |
|---|---|---|
| `src/<produto>/tela-<slug>.tsx` | **A UI.** Recebe dados, papel de usuário, estado de carga e navegação por parâmetro | Vai para produção. O dev copia e **não edita** |
| `src/proto/page-<slug>.tsx` | **O andaime.** Seletor de papel, seletor de estado, tema, dados de exemplo, navegação de protótipo | Descartável |

**Por que:** enquanto UI e andaime moram no mesmo arquivo, o dev é obrigado a **editar** para extrair a interface, e quem edita reescreve. Toda reescrita muda um espaçamento, uma variante, uma ordem. É a causa raiz da divergência visual entre protótipo e implementação, e revisão humana não pega isso de forma confiável.

**A dependência é direcional:** o andaime conhece a UI; a UI nunca conhece o andaime. Declare a camada criando `src/<produto>/README.md` com a linha `camada: ui`, e `npm run lint:camadas` passa a barrar qualquer import da UI para `proto/`.

### 5a — A UI

```tsx
// Tela <Nome>: a UI, e só a UI.
//
// Estado de interface (filtro aberto, aba ativa, formulário de modal) é dela.
// Dados, papel de usuário, estado de carga e navegação entram por parâmetro.

import { useState } from "react"
// Componentes reais do DS — NUNCA reimplementar
// ex: import { Table, TableBody, TableCell } from "@/components/ui/table"

import type { EstadoTela, Papel } from "@/<produto>/tipos"

export function TelaNome({
  itens,
  papel,
  podeEditar,
  estado = "default",
  onAbrirItem,
  onSalvar,
  onTentarNovamente,
}: {
  itens: Item[]
  papel: Papel
  /** Já resolvido por quem chama, incluindo a regra de consulta-only no mobile. */
  podeEditar: boolean
  estado?: EstadoTela
  onAbrirItem?: (item: Item) => void
  onSalvar?: (dados: DadosDoForm) => void
  onTentarNovamente?: () => void
}) {
  // Estado de INTERFACE fica aqui. Estado de AMBIENTE vem por parâmetro.
  const [busca, setBusca] = useState("")

  return (
    <main className="mx-auto max-w-7xl px-6 py-8">
      {estado === "loading" && <EsqueletoDaLista />}
      {estado === "empty"   && <EstadoVazio mensagem="..." />}
      {estado === "error"   && <EstadoErro mensagem="..." onTentarNovamente={onTentarNovamente} />}
      {estado === "default" && <ListaDeItens itens={itens} onAbrir={onAbrirItem} />}
    </main>
  )
}
```

### 5b — O contrato de dado

Em `src/<produto>/tipos.ts`, declarado **pela forma do contrato, não pela forma do mock**:

```ts
export type Item = {
  id: string
  nome: string
  /** Ausente enquanto não classificado. NUNCA string vazia fazendo papel de ausência. */
  categoria?: string
  /** Lista vazia é legítima. Diferente de ausência. */
  tags: string[]
}
```

Duas regras, e as duas nasceram de divergência real em pacote entregue:

1. **Ausente não é vazio.** Campo que pode não existir é opcional. Quem renderiza precisa distinguir "não informado" de "informado como vazio", senão a decisão de exibição (travessão, esconder o bloco, mostrar zero) acaba no adaptador que o dev escreve, e cada adaptador decide diferente.
2. **Variante é união discriminada**, não tipo largo com tudo opcional. Tipo largo empurra "este registro tem este bloco?" para runtime, e é ali que o comportamento diverge.

`typeof MOCK[0]` como tipo de prop é **proibido**: amarra a UI à forma do dado de exemplo.

### 5c — A fixture

Todo conteúdo de exemplo em **um módulo só**, `src/proto/fixtures.ts`, de dados puros: sem React, sem JSX, sem import de componente ou asset. As telas não declaram mock próprio.

Isso não é organização, é pré-requisito do aceite visual: se protótipo e implementação renderizarem conteúdo diferente, o diff acusa diferença de **dado** em vez de diferença de **implementação**, em toda tela cujo layout dependa do tamanho do conteúdo. O desfecho previsível é alguém subir a tolerância até o teste calar.

### 5d — O andaime

```tsx
// ANDAIME DO PROTÓTIPO — <nome da tela>.
// Este arquivo NÃO é a UI. A UI está em @/<produto>/*. Aqui vive só o que existe
// para demonstrar: seletor de papel, seletor de estado, tema e dados de exemplo.

import { useEffect, useState } from "react"
import { MOCK_ITENS } from "@/proto/fixtures"
import { TelaNome } from "@/<produto>/tela-nome"
import type { EstadoTela, Papel, Tema } from "@/<produto>/tipos"

const ESTADOS_PROTO = ["default", "loading", "empty", "error"] as const

export function ProtoPageNome() {
  const [papel, setPapel] = useState<Papel>("consultor")
  const [estado, setEstado] = useState<(typeof ESTADOS_PROTO)[number]>("default")
  const [tema, setTema] = useState<Tema>(() => (localStorage.getItem("proto-tema") as Tema) ?? "dark")

  useEffect(() => {
    localStorage.setItem("proto-tema", tema)
    document.documentElement.classList.toggle("dark", tema === "dark")
  }, [tema])

  return (
    <div className={tema}>
      {/* Barra de controle do protótipo. Não existe no produto final. */}
      <div className="flex flex-wrap items-center gap-2 border-b bg-muted px-4 py-2 text-xs text-muted-foreground">
        <span>Estado:</span>
        {ESTADOS_PROTO.map((e) => (
          <button key={e} onClick={() => setEstado(e)} className="rounded border px-2 py-1 text-xs">{e}</button>
        ))}
        <span className="ml-2">Papel:</span>
        {(["consultor", "produto"] as Papel[]).map((p) => (
          <button key={p} onClick={() => setPapel(p)} className="rounded border px-2 py-1 text-xs">{p}</button>
        ))}
      </div>

      <TelaNome
        itens={MOCK_ITENS}
        papel={papel}
        podeEditar={papel === "produto"}
        estado={estado as EstadoTela}
        onAbrirItem={() => { window.location.href = "/proto/page-detalhe" }}
        onTentarNovamente={() => setEstado("default")}
      />
    </div>
  )
}
```

> **Sinal de que a separação está certa:** o arquivo do andaime fica curto, na ordem de 100 a 150 linhas, independente do tamanho da tela. Se ele passar disso, tem UI vazando para dentro dele.

### Regras de implementação

- **Componente shadcn existe → usar obrigatoriamente.** Nunca `<table>` nativo quando `Table` existe; nunca `<span>` com classes manuais quando `Badge` existe; nunca `<button>` sem `Tooltip` quando é icon-only.
- **Tokens via classes Tailwind** — `bg-primary`, `text-foreground`, `border-border`. Nunca hex hardcoded.
- **Inline style só para valores dinâmicos** — largura de barra de progresso, cor calculada por dado. Layout estático → classes.
- **Espaçamento em múltiplos de 8px** — `p-2`(8) / `p-4`(16) / `p-6`(24) / `p-8`(32) / `p-12`(48).
- **Ícones via Lucide** — `import { X } from "lucide-react"`, prop `size` 16/20/24.
- **Mock data realista** — nomes, datas, valores plausíveis. Sem "Lorem Ipsum", sem "Usuário 1".
- **Switcher de estado obrigatório** — cobrir todos os estados do B7.
- **Sem scroll horizontal** — colapsar colunas secundárias se necessário.
- **Um overlay por vez** — drawer pode abrir modal; nunca empilhar overlay sobre overlay.
- **Copy sem travessão nem caixa alta.** Todo texto novo ou alterado — labels, placeholders, mensagens de estado vazio/erro, títulos — deve respeitar: proibido `—` (em dash) e `–` (en dash); proibida caixa alta total em labels/títulos. Verificar antes de marcar o proto como aprovado.

---

## Passo 6 — Registrar a rota do proto

**React Router (Vite SPA):** rota `/proto/<slug>` em `src/main.tsx` ou `src/router.tsx`.

**TanStack Start / file-based routing:** criar `src/routes/proto/<slug>.tsx` exportando o componente como default.

A rota é descartável — removida junto com `src/proto/` após a implementação real.

Informe: *"Proto disponível em `localhost:PORT/proto/<slug>` — abrindo no navegador."*

---

## Passo 7 — Abrir no navegador e apresentar

Abra o localhost. Confirme: renderizou sem erro no console? Switcher funciona? Tokens aplicados?

*"Proto da tela [X] aberto — [N] estados no switcher. Revise e me diga o que ajustar."*

---

## Passo 8 — Ciclo de ajuste (HMR)

1. PX aponta o ajuste
2. Edite `src/proto/<slug>.tsx`
3. HMR aplica — sem recarregar
4. PX vê e decide

Tipos comuns: hierarquia, copy, layout de colunas, densidade, comportamento de estado, responsivo.

Cada ajuste é aplicado direto, sem perguntar. O PX vê e manda mais ou aprova.

---

## Passo 8b — Registrar a anatomia do que foi construído (obrigatório antes de aprovar)

**Por que importa:** o protótipo é entregue como **referência visual**, e o dev reimplementa na stack dele. Todo valor que você decidiu enquanto construía — altura, padding, sombra, espessura de anel, largura de drawer, se um componente é o default da lib ou um override — existe **só no seu código** até ser escrito. Se não for registrado agora, alguém terá que fazer engenharia reversa do CSS depois, sob pressão de entrega e sem o contexto da decisão. Foi exatamente o que custou a correção da entrega SmartCity semana-33.

**Este é o momento barato de registrar.** A informação está na sua mão; depois ela vira arqueologia.

**Fazer:** para cada componente/região do inventário do Passo 1, acrescentar (ou atualizar) uma entrada em `planning/<iniciativa>/anatomia-visual.md`:

| Campo | O que registrar |
|---|---|
| **Região/componente** | header, moldura da tabela, linha, drawer, dropdown, card de KPI, chart… |
| **Valores exatos** | altura, padding, gap, raio, sombra, fonte/peso, largura. Números, não adjetivos. |
| **Origem** | **Boilerplate** (default da lib já correto — *não customizar*) × **Override do projeto** (identidade própria — *aplicar*) |
| **Base apurada** | Commit do `boilerplate-upstream` e data, conforme o Passo 3A. Preencher com o valor real, nunca "atual" |
| **Componente da lib** | qual componente/hook cobre a região (`Table variant="spaced"`, `sheet.tsx`, `useTableSort`…) |
| **Intenção**, quando não for óbvia | *ex: "body do drawer em `--surface-soft` e footer em `--surface` separa conteúdo de ações — não uniformizar"* |

**Registrar também, sempre que aplicável:**
- **Bespoke sem equivalente na lib** — diga como foi composto e o que preservar se o dev trocar de abordagem (*ex: donut via `conic-gradient`; se usar lib de chart, manter anel de 20px e as cores do dicionário de status*).
- **Gambiarra de protótipo que NÃO deve ser replicada** — workaround de contexto de empilhamento, delay artificial de skeleton, valor fora da escala de 8px. Diga explicitamente o que normalizar.
- **Equivalência de biblioteca** quando a do proto difere da do dev (ícones, por exemplo): equivalência **semântica**, nunca cópia de glifo.

> ⛔ **A coluna "Origem" é indeterminável sem o registry.** Classificar um valor como "Boilerplate — não customizar" exige comparar com o componente real de `@centralit`. Se o Passo 3A não passou, você não tem esse referencial: preenchida por dedução, a coluna não fica vazia — fica **afirmativamente errada**, e manda o dev preservar exatamente o que ele precisa substituir. Sem o Passo 3A verde, marque cada linha como `Origem: NÃO APURADA` e registre a pendência com dono. É pior errar aqui do que deixar em branco.
>
> **Trava:** componente no inventário do Passo 1 sem entrada na anatomia **bloqueia a aprovação**. A `px-handoff` cobra a completude deste arquivo no DoD dela — se ficar para lá, já é tarde.
>
> **Dispensa:** se a entrega ao dev for de **componentes reais na mesma stack** dele, registre "N/A — entrega em componentes" e siga. Nesse caso o componente **é** a spec.

## Passo 9 — Aprovação e encerramento

Quando aprovado:

1. Adicione no topo: `// Aprovado em: YYYY-MM-DD`
2. Confirme que a anatomia do Passo 8b está completa para todos os componentes do inventário, **com a coluna "Origem" apurada** (não `NÃO APURADA`)
2b. Confirme que a procedência do Passo 3A está registrada no `PX-PROGRESS` — commit da base, data, distância do `main`, versão das skills
3. Atualize `PX-PROGRESS.md` — proto aprovado, caminho `src/proto/<slug>.tsx`
4. **Lint de copy:** rodar `npm run lint:travessao` e `npm run lint:caixa-alta` e confirmar que não há violação em texto novo. Copy nova de UI — onboarding, tooltip, empty/error, título — é o ponto de maior risco.
5. Eco:
   > *"Proto de [tela] aprovado. Arquivo em `src/proto/<slug>.tsx` — referência visual pro dev. Anatomia registrada em `anatomia-visual.md` ([N] componentes). Rota `/proto/<slug>` pode ser removida após implementação. Próximo passo: `px-story` — quer seguir?"*

---

## Onde fica

- `src/<produto>/tela-<slug>.tsx` — a UI (vai para produção)
- `src/<produto>/tipos.ts` — os contratos de dado
- `src/proto/page-<slug>.tsx` — o andaime (descartável)
- `src/proto/fixtures.ts` — o conteúdo de exemplo, fonte única

---

## Regras consolidadas

- **Nunca gerar sem px-request aprovado.**
- **Inventário de componentes antes da primeira linha** (Passo 1) — público, mostrado ao PX.
- **Ambiguidade de variação → pergunta, nunca escolha silenciosa** (Passo 2).
- **Componente shadcn disponível → uso obrigatório**, nunca reimplementação manual.
- **Ícone em contexto** → sempre perguntar se é decorativo (muted) ou funcional (primary/destructive).
- **Elemento que parece clicável mas spec não define ação** → sinalizar, não inventar comportamento.
- **Borda, cor de destaque, visual de alerta em cards** → confirmar se aplica a todos ou só aos que têm condição.
- **Header de tela** → confirmar se tem breadcrumb/router ou só H1.
- **Switcher de estado obrigatório** — todos os estados do B7.
- **A UI é código destinado à produção; o andaime é descartável.** Não trate o protótipo inteiro como descartável: a pasta de UI é entregue com a instrução "copie, não edite", e é isso que elimina a divergência visual. Só `src/proto/` é jogado fora.
- **Contrato de dado pela forma do contrato, nunca `typeof MOCK[0]`.** Ausente não é vazio; variante é união discriminada.
- **Uma fixture só**, em `src/proto/fixtures.ts`, de dados puros. Tela não declara mock próprio.
- **`npm run lint:camadas` verde** antes de considerar o proto pronto.

---

## Relação com o fluxo

```
px-request (spec aprovada)
    ↓
px-proto  ←  você está aqui
    │   inventário → gate de ambiguidade → implementação → HMR → aprovação
    │
    └── [aprovado]
          ↓
      px-story (história + BDD)
          ↓
      [px-preview — opcional, formato de entrega externa]
          ↓
      px-handoff (DoD + sprint → devs)
```

> Nenhuma tela vai para `px-story` sem proto aprovado no localhost.
