---
name: px-proto
description: Cria a tela do protótipo dentro do boilerplate (Vite + localhost) usando os componentes reais do shadcn, os tokens reais do UI KIT e mock data do px-request. Constrói em DUAS pastas obrigatoriamente: a UI, que é destinada à produção e o dev copia sem editar, e a demo do protótipo (seletores de papel e estado, dados de exemplo), que é descartável. O PX trabalha no localhost com HMR — vê, ajusta, aprova. Obrigatório após o px-request e antes do px-story. Use quando o líder disser "gera o proto", "quero ver como fica", "prototipar a tela", "visualizar a spec", ou ao fechar um px-request.
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: proto
---

# px-proto — protótipo visual no boilerplate (Vite + localhost)

Esta skill cria o protótipo da tela **dentro do boilerplate**, usando os componentes reais do shadcn/ui, os tokens reais do `src/index.css` e o servidor de desenvolvimento Vite. O PX vê a tela no localhost com HMR — ajusta em tempo real, aprova — e só então a tela vira história (`px-story`).

**A tela nasce em duas pastas, e a distinção importa mais que qualquer outra regra desta skill:** `src/<produto>/` guarda a **UI, que é destinada à produção** e é entregue ao dev com a instrução de copiar sem editar; `src/proto/` guarda o **demo**, que é descartável. Tratar o protótipo inteiro como descartável é o que produz código que o dev não consegue reaproveitar, e é a causa raiz da divergência visual entre protótipo e implementação.

**Por que no boilerplate:** componentes reais, tokens reais, HMR. Aqui é o mesmo stack do produto, só com mock data e diretório separado.

> ⛔ **HTML standalone (vanilla ou via CDN) não é aproximação aceitável: é a causa raiz medida da divergência.** Em 2026-09-18 o time de dev do SmartCity mostrou o que recebia: HTML de 3.407 linhas sem uma classe Tailwind e sem uma fronteira de componente, enquanto o repo deles tinha a nossa biblioteca inteira, byte a byte. A LLM do dev precisou reinterpretar cada região, e cada dev obteve um resultado diferente. Uma tela que existe só como `.html` **não é protótipo desta skill e não é aprovável** (Passo 9). Se o líder pedir "gera um HTML", a resposta é: o proto nasce em TSX aqui; o HTML pra PO sai depois pelo `px-preview`.

> **Este fonte vai ser COPIADO por outro time, não lido.** Quando o dev implementa na mesma stack, a `px-handoff` entrega `src/<produto>/` com a instrução de copiar sem editar. Escreva pensando nisso: nome de variável que se explica, `// INTEGRATION BOUNDARY:` nas fronteiras, e nenhum truque que você não queira ver rodando em produção. É o que permite fidelidade 1:1 sem ninguém redesenhar a partir de screenshot, e sem ninguém redigitar centenas de decisões visuais.
>
> **Se o dev precisar editar um arquivo da camada de UI para rodar no projeto dele, é defeito nosso** e conserta-se na origem. A demo é outra história: `src/proto/` não é biblioteca, não é pacote, não vai para produção, e o PX não mantém. A fronteira de propriedade está registrada na `px-handoff`.

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

> **Por que este passo mudou.** Ele já existia e mesmo assim deixou passar um accordion
> reimplementado à mão, uma paginação sem elipse, um chevron duplo e uma busca difusa,
> todos com componente canônico disponível. A causa não foi desleixo: o inventário antigo
> perguntava **se** o componente existe, nunca **o que ele já entrega**. Existir e ser usado
> como o design system manda são duas verificações diferentes, e só a primeira estava aqui.
> As skills protegiam contra o que não está no catálogo; contra o que está e é usado errado,
> não havia nada.

### 1a — Varredura de candidatos (antes de escolher qualquer coisa)

Para **cada** widget da spec, varra `src/components/ui/` de duas formas e liste **todos** os
candidatos que casam o comportamento, não só o primeiro que serve:

1. **Por nome** — `ls src/components/ui/` e case pelo nome óbvio.
2. **Por palavra-chave de comportamento** — `grep -ril "<comportamento>" src/components/ui/`
   com o verbo do widget (*abrir/fechar, colapsar, expandir, buscar, filtrar, selecionar
   vários, paginar, empilhar, arrastar*). É esta varredura que acha o candidato cujo nome
   você não conhecia.

⛔ **Achou um que serve e parou de procurar? O passo não foi cumprido.** A regra "componente
existente se usa" é satisfeita formalmente por **qualquer** componente existente, inclusive
o errado. "Grupo colapsável" foi mapeado para `collapsible.tsx`, que existe, e a regra ficou
cumprida no papel enquanto o `accordion.tsx` — o certo, com anatomia de linha de tabela
comentada decisão por decisão — nunca entrou na conversa.

**Dois ou mais candidatos → o Passo 2 é obrigatório**, e a escolha vai registrada com o
motivo. Não é o construtor que decide se o caso é ambíguo: **a contagem de candidatos
decide.** Ambiguidade auto-declarada é o mesmo que ambiguidade não declarada.

Pares que já produziram defeito e que quase sempre aparecem juntos na varredura:

| Widget que você tem | Candidatos que a varredura precisa devolver |
|---|---|
| Bloco que abre e fecha | `accordion` **e** `collapsible` |
| Lista com busca | `combobox`, `multi-select` **e** `select` |
| Menu de opções | `dropdown-menu` **e** `navigation-menu` |
| Overlay lateral | `sheet` **e** `responsive-dialog` |
| Confirmação | `dialog` **e** `alert-dialog` |
| Grupo de botões alternáveis | `toggle-group` **e** `button-group` |

### 1b — O inventário lê o COMPONENTE, não a doc

Este mapeamento é **público** — mostre ao PX antes de codar.

| Widget da spec | Candidatos (1a) | Escolhido | O que o `.tsx` já entrega | O que os comentários dele já decidiram | O que a doc acrescenta | Instalar? |
|---|---|---|---|---|---|---|
| Bloco colapsável de tarefa | `accordion`, `collapsible` | `accordion.tsx` | `AccordionItem/Trigger/Content`, `type="single"`, `collapsible` | "cada item é um card idêntico a uma row da tabela (variante spaced)"; "corpo clicável = a row: px-4, py-4" | sem entrada própria → **o componente é a spec** | não |
| Rodapé de paginação | `pagination` | `pagination.tsx` → `TablePagination` | contagem, seletor de itens por página, elipse, anatomia por variant | "no card do spaced a borda sai: o card já é a moldura" | §Pagination: elipse obrigatória, default 10, texto "Mostrando X a Y de Z" | não |
| Seleção múltipla com busca | `multi-select`, `combobox` | `multi-select.tsx` | `variant`, `countLabel`, `maxVisible`, **`filter`**, `readOnly`, `aria-label` | "o `cmdk` filtra por correspondência difusa: passe `filter` quando a lista for grande" | sem entrada própria → **o componente é a spec** | não |

**Como preencher as três colunas do meio (é aqui que o passo tem valor):**

- **O que o `.tsx` já entrega** — abra o arquivo e liste as **props e os subcomponentes
  exportados**. Não resuma: nomeie. Uma prop que existe e você não viu vira reimplementação
  à mão, e reimplementação à mão é divergência com aparência de trabalho.
- **O que os comentários dele já decidiram** — os componentes desta biblioteca são
  comentados decisão por decisão, e **essas decisões não estão em lugar nenhum além do
  arquivo**. É a régua mais precisa que existe, e ela é invisível para quem lê só a doc.
- **O que a doc acrescenta** — o "quando usar / não usar", a variação, o proibido. **Se não
  houver entrada no `ds-components_v4.md`, escreva literalmente "sem entrada própria → o
  componente é a spec"** e siga. Metade da biblioteca está nessa situação, e tratar ausência
  de entrada como ausência de régua foi exatamente o buraco por onde os defeitos passaram.

⛔ **Trava:** linha com qualquer das três colunas do meio vazia **reprova o inventário**.
"Não li o arquivo" não é preenchimento válido, e "é óbvio" também não.

**Regras (as de sempre, mantidas):**
- Se existe em `src/components/ui/` → usar obrigatoriamente, nunca reimplementar.
- Se não existe → `npx shadcn@latest add @centralit/<componente>` antes de codar. **O prefixo `@centralit/` é obrigatório.**
- ⛔ **`npx shadcn add <componente>` sem o prefixo é proibido.** A forma sem prefixo resolve no shadcn **público** e **funciona** — entrega o default `new-york` em vez do componente da Central IT. Não dá erro, não dá aviso: o proto inteiro nasce sobre a base errada e a `anatomia-visual.md` do Passo 8b registra os valores vanilla como se fossem "default do boilerplate — não customizar", instruindo o dev a preservar o que ele deve substituir. Foi exatamente esse o mecanismo do incidente do sandbox sem token.
- **Se o `add` do registry falhar** (401/404) → ⛔ **pare**. É acesso, não é componente faltando. Volte ao `px-setup` Passo 2b. Nunca instale a versão pública como contorno, nunca implemente o componente à mão.
- **Componente que não existe no registry** (53 itens em `public/r/`) → é decisão de design system, não de proto. Registre como Pergunta em aberto com dono; não invente primitiva.
- `<table>` HTML nativo, `<span>` com classes manuais, `<button>` sem primitiva shadcn → **proibidos** quando existe equivalente no catálogo.

Componentes que **sempre** existem no boilerplate e **nunca** devem ser reimplementados:

| Elemento | Usar |
|---|---|
| Tabela (qualquer variação) | `Table, TableHeader, TableBody, TableRow, TableHead, TableCell` |
| Rodapé de paginação de tabela | `TablePagination` (de `pagination.tsx`) — nunca compor à mão |
| Badge / status / chip | `Badge` com `variant` ou `className` |
| Botão icon-only | `Button size="icon"` + `Tooltip` obrigatório |
| Loading de bloco | `Skeleton` |
| Toast / feedback | `Sonner` (toast) |
| Confirmação destrutiva | `AlertDialog` |
| Qualquer overlay | `Dialog`, `Sheet` (drawer), `Popover` — nunca div posicionada |

---

## Passo 2 — Gate de ambiguidade (antes de codar)

**O gate dispara por contagem, não por percepção.** Duas entradas o acionam, e nenhuma delas
depende de alguém achar que o caso é difícil:

1. **A varredura do Passo 1a devolveu dois ou mais candidatos** para o mesmo widget. Não
   importa se um deles parece obviamente melhor: liste os dois, diga o que os distingue e
   registre a escolha com o motivo.
2. **A variação de componente não está explícita na px-request.**

> **Por que a mudança.** Antes, ambiguidade era **auto-declarada**: quem inventariava
> decidia se o caso era ambíguo, e a regra "componente existente se usa" ficava cumprida ao
> escolher qualquer candidato existente. Foi assim que um grupo colapsável virou
> `collapsible` sem que o `accordion` — o certo — fosse sequer citado. Quem escolhe em
> silêncio não sabe que escolheu.

Elementos que tipicamente exigem confirmação:

| Padrão ambíguo | Pergunta obrigatória |
|---|---|
| Seletor de opções (período, filtro, modo) | ToggleGroup, Select dropdown, ou botões segmentados? |
| Ícone ao lado de texto ou em contexto de seção | Decorativo (muted) ou funcional (primary/destructive)? |
| Elemento que parece clicável mas spec não define ação | É clicável? O que acontece ao clicar? |
| Card com visual de destaque (borda, cor de fundo) | Aplica em todos ou só nos que têm condição de risco/alerta? |
| Header de tela | Breadcrumb com navegação ou só H1 (sem router nesta tela)? |
| Chips / pills | Display apenas ou filtros clicáveis? Se clicáveis, o que filtram? |

Use `AskUserQuestion` para esses casos — 2–4 opções com a recomendada marcada. Resolva todos
antes de escrever a primeira linha de código. **Ambiguidade resolvida em silêncio =
retrabalho garantido.**

**Registrar a escolha.** Toda resolução deste passo entra no inventário do Passo 1b (coluna
"Escolhido") **com o motivo**, e não só no chat. Escolha sem motivo escrito não sobrevive à
próxima sessão, e é ela que o `px-story` e o `px-handoff` vão citar.

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
6. `docs/design-system/ds-components_v4.md` existe? O Passo 4 consulta esse catálogo. Se faltar, rode `npx github:DiogoRother-it/px-skills` — o instalador o entrega. **Nunca improvise a anatomia de memória**: catálogo ausente produz componente plausível e anatomia errada. ⚠️ **O catálogo é a fonte de comportamento, não de anatomia** — anatomia sai do `.tsx`, e 17 dos 53 componentes não têm entrada no catálogo (Passo 4). Ter o documento não dispensa abrir o arquivo.
7. Todos os componentes do inventário (Passo 1) estão em `src/components/ui/`? Se não, instale os que faltam **pelo registry** (`@centralit/<nome>`), respeitando as regras do Passo 1.

**Registrar o resultado.** Anote no `PX-PROGRESS` a linha de procedência apurada aqui: commit da base, data, distância do `main` e versão das skills. É o dado que o `px-handoff` estampa no pacote — e sem ele nenhuma entrega é rastreável depois.

---

## Passo 4 — Mapear a variação: hierarquia de fontes

**Cada pergunta tem uma fonte, e não é sempre a mesma.** Consultar só o
`ds-components_v4.md` deixa você cego para metade do catálogo: **17 dos 53 componentes não
têm entrada própria lá** (23, contando só entrada com o próprio nome), e entre eles estão
`accordion`, `collapsible`, `multi-select`, `badge`, `dropdown-menu` e `toggle-group` — que
é exatamente onde a cadeia errou.

| A pergunta é sobre | A fonte é | Regra |
|---|---|---|
| **Anatomia** — partes, props, o que já vem pronto | o `.tsx` em `src/components/ui/` | É a fonte mais completa e a mais atual. Sem entrada na doc, **o componente É a spec** |
| **Comportamento e regra** — quando usar, qual variação, o proibido | `docs/design-system/ds-components_v4.md` | É onde vivem as árvores "Qual usar?" e o "não usar" |
| **Valor de cor** | `src/index.css` | O CSS real prevalece sobre a doc para valor visual |
| **Exemplo de composição** | `src/showcase/` | **Auditável, nunca verdade** — ver abaixo |

⚠️ **O `src/showcase/` é auditável, nunca verdade.** Ele é um exemplo escrito por alguém, não
uma spec. **Ao copiar dele, confira contra a spec e contra o `.tsx` antes de colar.**
Divergiu? **A spec ganha**, e a divergência do showcase vira débito externo registrado no
`PX-PROGRESS` (é do boilerplate, não deste projeto). Isto não é formalidade: o
`showcase/Dados.tsx` chegou a ter duas paginações que divergiam da spec e uma da outra, e é o
arquivo que todo projeto novo copia. Copiar dele sem conferir propaga o defeito com cara de
padrão da casa.

**Do catálogo, extraia:**

- **Anatomia:** partes do componente
- **Estados:** quais são específicos desta variação
- **Regras visuais:** sizing, spacing, comportamentos obrigatórios
- **Overlay:** regras de empilhamento (se aplicável)

### Como saber se a família tem variação (critério, não lista)

⛔ **Não existe lista fechada de famílias com variação.** A lista que ficava aqui (Table,
Card, Select, Date Picker, Upload, Overlay) fazia o passo se cumprir **vazio** sempre que o
componente não estava nela: Accordion e Pagination não estavam, então ninguém abriu a spec da
paginação, que existe no `ds-components_v4.md` desde sempre e nunca tinha sido lida.

**O critério:** um componente tem variação a decidir quando **qualquer** destas for verdade:

1. O `.tsx` expõe prop de forma (`variant`, `size`, `density`, `type`, `mode`, `collapsible`)
   — o default dela **é uma decisão**, e decisão por omissão é decisão não declarada.
2. A varredura do Passo 1a devolveu mais de um candidato para o mesmo trabalho.
3. A entrada na doc tem seção "Variações" ou árvore "Qual usar?".
4. O componente aceita composição com outro (rodapé de tabela, campo com máscara, overlay
   que dispara overlay).

Nenhuma sendo verdade, escreva **"sem variação a decidir"** na linha do inventário. O passo
se cumpre com uma frase escrita, nunca com silêncio.

**Exemplos de famílias com variação** (é exemplo, não inventário — o critério acima é que manda):

| Família | Variações |
|---|---|
| Table | Básica · Com Interações (sort/select) · Com Expansão · Data Grid avançada · variant `spaced`/`divided` · densidade |
| Pagination | Números · setas prev/next · com seletor de itens por página · rodapé por variant da tabela (`TablePagination`) |
| Card | Resumo · Informativo · Interativo |
| Select | Base · Com Busca · Multi · Async · Combobox |
| Accordion / Collapsible | Item de lista com anatomia de row (`accordion`) · primitivo cru (`collapsible`) |
| Date Picker | Single · Range · Date Time |
| Upload | Campo simples · Dropzone · Multi-arquivo |
| Overlay | Drawer · Modal · Dialog · AlertDialog · Popover |

---

## Passo 4b — Divergências do design system (obrigatório, mesmo que seja "nenhuma")

**Toda divergência do DS é declarada com motivo, ou é defeito.** Não existe terceira
categoria. Este bloco espelha o `Bloco 11b` do `px-request`, que já existe para divergências
do **legado** e funciona: num redesign recente cinco divergências do legado foram declaradas
e nenhuma virou defeito, enquanto seis divergências do **design system** passaram inteiras
pela cadeia porque não havia onde declará-las.

Conta como divergência do DS, e por isso precisa de linha:

- **Default trocado** — usar 20 por página quando a spec diz 10, `variant="divided"` quando o
  default é `spaced`, densidade compacta onde a spec não pede.
- **Anatomia alterada** — remover borda, trocar padding, mudar altura de um componente do
  catálogo.
- **Parte omitida** — rodapé sem elipse, sem seletor de itens por página, sem contagem.
- **Composição à mão** onde existe componente pronto (`TablePagination` é o caso conhecido).
- **Hierarquia de ação** invertida — primária à esquerda, duas primárias no mesmo contexto.
- **Ícone fora da convenção** da casa (chevron duplo onde o DS usa simples).
- **Tooltip de seção** onde a regra pede tooltip por campo, e vice-versa.

**Formato — escreva no `px-request` da tela, no Bloco 11c**, e ecoe aqui:

| # | O DS manda | Aqui faz | Por quê | Quem decidiu / quando |
|---|---|---|---|---|

**Se não houver nenhuma, escreva literalmente "nenhuma divergência do design system".** Bloco
em branco não é "não houve": é "ninguém olhou", e os dois são indistinguíveis depois.

⛔ **Trava:** divergência encontrada na revisão do líder que **não** está neste bloco é
defeito da cadeia, não ajuste de gosto — e volta como correção, não como pedido novo.

---

## Passo 5 — Criar os DOIS arquivos do protótipo

> ⛔ **Nunca escreva a tela num arquivo só.** Todo protótipo nasce em duas pastas.
> Esta é a regra que mais impacta fidelidade visual no handoff, e não é negociável.

| Arquivo | O que contém | Destino |
|---|---|---|
| `src/<produto>/tela-<slug>.tsx` | **A UI.** Recebe dados, papel de usuário, estado de carga e navegação por parâmetro | Vai para produção. O dev copia e **não edita** |
| `src/proto/page-<slug>.tsx` | **A demo.** Seletor de papel, seletor de estado, tema, dados de exemplo, navegação de protótipo | Descartável |

**Por que:** enquanto UI e demo moram no mesmo arquivo, o dev é obrigado a **editar** para extrair a interface, e quem edita reescreve. Toda reescrita muda um espaçamento, uma variante, uma ordem. É a causa raiz da divergência visual entre protótipo e implementação, e revisão humana não pega isso de forma confiável.

**A dependência é direcional:** a demo conhece a UI; a UI nunca conhece a demo. Declare a camada criando `src/<produto>/README.md` com a linha `camada: ui`, e `npm run lint:camadas` passa a barrar qualquer import da UI para `proto/`.

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

### 5d — A demo

```tsx
// DEMO DO PROTÓTIPO — <nome da tela>.
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

> **Sinal de que a separação está certa:** o arquivo da demo fica curto, na ordem de 100 a 150 linhas, independente do tamanho da tela. Se ele passar disso, tem UI vazando para dentro dele.

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
- **Âncoras de onboarding (`data-onb`)** — toda candidata a âncora do B5 do request recebe `data-onb="<id>"` no **invólucro visível**, nunca no controle nativo (Input com ícone, Select e Combobox repassam `data-*` ao elemento interno e o recorte do guia abraçaria só ele: envolva num `<div data-onb>` do tamanho do controle). Sem âncora no proto, o `px-tour` não tem alvo.
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

**Por que importa (só no caminho de referência visual, legado sem shadcn; no caminho do fonte, ver a Dispensa abaixo):** quando o protótipo é entregue como **referência visual**, o dev reimplementa na stack dele. Todo valor que você decidiu enquanto construía — altura, padding, sombra, espessura de anel, largura de drawer, se um componente é o default da lib ou um override — existe **só no seu código** até ser escrito. Se não for registrado agora, alguém terá que fazer engenharia reversa do CSS depois, sob pressão de entrega e sem o contexto da decisão. Foi exatamente o que custou a correção da entrega SmartCity semana-33.

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

0. ⛔ **A tela existe como `.tsx` em `src/<produto>/`, com imports de `@/components/ui/`?** Tela que existe só como `.html` (vanilla ou CDN), ou só dentro de `src/proto/`, **não é aprovável**: volte ao Passo 5. É este item que impede a entrega de sair como HTML pro dev.
1. Adicione no topo: `// Aprovado em: YYYY-MM-DD`
2. Confirme que a anatomia do Passo 8b está completa para todos os componentes do inventário, **com a coluna "Origem" apurada** (não `NÃO APURADA`)
2a. Confirme que o inventário do Passo 1b tem as três colunas do meio preenchidas em **todas** as linhas, e que o Passo 4b tem veredito (uma divergência declarada por linha, ou "nenhuma divergência do design system" por extenso)
2b. Confirme que a procedência do Passo 3A está registrada no `PX-PROGRESS` — commit da base, data, distância do `main`, versão das skills
3. Atualize `PX-PROGRESS.md` — proto aprovado, caminho `src/proto/<slug>.tsx`
4. **Lint de copy:** rodar `npm run lint:travessao` e `npm run lint:caixa-alta` e confirmar que não há violação em texto novo. Copy nova de UI — onboarding, tooltip, empty/error, título — é o ponto de maior risco.
5. Eco:
   > *"Proto de [tela] aprovado. UI em `src/<produto>/tela-<slug>.tsx` (é o fonte que atravessa pro dev) e demo em `src/proto/page-<slug>.tsx`. Anatomia registrada em `anatomia-visual.md` ([N] componentes). Rota `/proto/<slug>` pode ser removida após implementação. Próximo passo: `px-story` — quer seguir?"*

---

## Onde fica

- `src/<produto>/tela-<slug>.tsx` — a UI (vai para produção)
- `src/<produto>/tipos.ts` — os contratos de dado
- `src/proto/page-<slug>.tsx` — a demo (descartável)
- `src/proto/fixtures.ts` — o conteúdo de exemplo, fonte única

---

## Regras consolidadas

- **Nunca gerar sem px-request aprovado.**
- **Inventário de componentes antes da primeira linha** (Passo 1) — público, mostrado ao PX, e **lendo o `.tsx`**: props, decisões comentadas e o que a doc acrescenta. Coluna vazia reprova o inventário.
- **Varredura de candidatos antes de escolher** (Passo 1a) — por nome **e** por comportamento. Dois ou mais candidatos → Passo 2 obrigatório. Ambiguidade é decidida pela contagem, nunca auto-declarada.
- **Ambiguidade de variação → pergunta, nunca escolha silenciosa** (Passo 2), com a escolha e o motivo registrados no inventário.
- **Hierarquia de fontes** (Passo 4): anatomia no `.tsx` · comportamento no `ds-components_v4.md` · cor no `index.css` · exemplo no `showcase/`, que é **auditável, nunca verdade**. Sem entrada na doc, **o componente é a spec**.
- **Divergência do design system declarada com motivo, ou é defeito** (Passo 4b) — inclusive "nenhuma", escrita por extenso.
- **Componente shadcn disponível → uso obrigatório**, nunca reimplementação manual.
- **Ícone em contexto** → sempre perguntar se é decorativo (muted) ou funcional (primary/destructive).
- **Elemento que parece clicável mas spec não define ação** → sinalizar, não inventar comportamento.
- **Borda, cor de destaque, visual de alerta em cards** → confirmar se aplica a todos ou só aos que têm condição.
- **Header de tela** → confirmar se tem breadcrumb/router ou só H1.
- **Switcher de estado obrigatório** — todos os estados do B7.
- **A UI é código destinado à produção; a demo é descartável.** Não trate o protótipo inteiro como descartável: a pasta de UI é entregue com a instrução "copie, não edite", e é isso que elimina a divergência visual. Só `src/proto/` é jogado fora.
- **Contrato de dado pela forma do contrato, nunca `typeof MOCK[0]`.** Ausente não é vazio; variante é união discriminada.
- **Uma fixture só**, em `src/proto/fixtures.ts`, de dados puros. Tela não declara mock próprio.
- **`npm run lint:camadas` verde** antes de considerar o proto pronto.

---

## Relação com o fluxo

```
px-request (spec aprovada)
    ↓
px-proto  ←  você está aqui
    │   inventário (lê o .tsx) → gate de ambiguidade por contagem → hierarquia de fontes
    │   → divergências do DS declaradas → implementação → HMR → aprovação
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
