---
name: px-proto
description: Cria componentes/páginas de protótipo dentro do boilerplate (Vite + localhost) usando os componentes reais do shadcn, os tokens reais do UI KIT e mock data do px-request. O PX trabalha no localhost com HMR — vê, ajusta, aprova. Obrigatório após o px-request e antes do px-story. Use quando o líder disser "gera o proto", "quero ver como fica", "prototipar a tela", "visualizar a spec", ou ao fechar um px-request.
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: proto
---

# px-proto — protótipo visual no boilerplate (Vite + localhost)

Esta skill cria o protótipo da tela **dentro do boilerplate**, usando os componentes reais do shadcn/ui, os tokens reais do `src/index.css` e o servidor de desenvolvimento Vite. O PX vê a tela no localhost com HMR — ajusta em tempo real, aprova — e só então a tela vira história (`px-story`). O protótipo fica em `src/proto/` e não é código de produção.

**Por que no boilerplate:** componentes reais, tokens reais, HMR. Standalone HTML via CDN é uma aproximação — aqui é o mesmo stack do produto, só com mock data e diretório separado.

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
- Se não existe → `npx shadcn add <componente>` antes de codar.
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

## Passo 3 — Verificar o ambiente

1. Servidor rodando? Se não, `npm run dev` em background.
2. `src/index.css` tem os tokens do UI KIT? Se não, avise que o `px-kickoff` precisa materializar primeiro.
3. Todos os componentes do inventário (Passo 1) estão em `src/components/ui/`? Se não, instale os que faltam agora.

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

## Passo 5 — Criar o arquivo do protótipo

Crie `src/proto/<slug-da-tela>.tsx`:

```tsx
// PROTO: <Nome da Tela> — <slug do px-request>
// Descartável. Não é código de produção.
// Aprovado em: [data de aprovação]

import { useState } from "react"
// Importar componentes reais — NUNCA reimplementar
// ex: import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
// ex: import { Badge } from "@/components/ui/badge"
// ex: import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

// ── Mock data (Bloco 4 do px-request) ─────────────────────────
const MOCK_ITEMS = [
  // valores realistas — nomes, datas, números plausíveis
  // nunca "Lorem Ipsum", nunca "Usuário 1"
]

// ── Switcher de estado ─────────────────────────────────────────
type Estado = "default" | "loading" | "empty" | "error" // ajustar ao B7

export function ProtoNomeDaTela() {
  const [estado, setEstado] = useState<Estado>("default")

  return (
    <div className="min-h-screen bg-background">
      {/* Barra de estado — visível só neste proto */}
      <div className="flex items-center gap-2 px-4 py-2 bg-muted text-xs text-muted-foreground border-b">
        <span>Estado proto:</span>
        {(["default", "loading", "empty", "error"] as Estado[]).map((e) => (
          <button
            key={e}
            onClick={() => setEstado(e)}
            className={`px-2 py-1 rounded border text-xs ${
              estado === e
                ? "bg-primary text-primary-foreground border-primary"
                : "border-border bg-transparent"
            }`}
          >
            {e}
          </button>
        ))}
      </div>

      <div className="p-8">
        {estado === "loading" && <EstadoLoading />}
        {estado === "empty"   && <EstadoEmpty />}
        {estado === "error"   && <EstadoError />}
        {estado === "default" && <EstadoDefault />}
      </div>
    </div>
  )
}

function EstadoDefault() {
  // Variação exata com componentes reais
  return null
}
function EstadoLoading() {
  // Skeleton que preserva o layout — usar <Skeleton> do shadcn
  return null
}
function EstadoEmpty() {
  // Mensagem + CTA — nunca tela morta
  return null
}
function EstadoError() {
  // Mensagem explicando como resolver + ação de recuperação
  return null
}
```

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

## Passo 9 — Aprovação e encerramento

Quando aprovado:

1. Adicione no topo: `// Aprovado em: YYYY-MM-DD`
2. Atualize `PX-PROGRESS.md` — proto aprovado, caminho `src/proto/<slug>.tsx`
3. **Lint de copy:** rodar `npm run lint:travessao` e `npm run lint:caixa-alta` e confirmar que não há violação em texto novo. Copy nova de UI — onboarding, tooltip, empty/error, título — é o ponto de maior risco.
4. Eco:
   > *"Proto de [tela] aprovado. Arquivo em `src/proto/<slug>.tsx` — referência visual pro dev. Rota `/proto/<slug>` pode ser removida após implementação. Próximo passo: `px-story` — quer seguir?"*

---

## Onde fica

`src/proto/<slug-da-tela>.tsx` (boilerplate, temporário)

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
- **Proto não é código de produção** — sem abstrações, sem otimizações. Referência visual descartável.

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
