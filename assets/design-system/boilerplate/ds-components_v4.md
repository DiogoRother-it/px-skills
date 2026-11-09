# DS Components v4 — Stack shadcn/ui

> **O que é este arquivo**
> Specs de comportamento de todos os componentes do Design System — anatomia, estados, variações, tamanhos, regras de uso e acessibilidade.
> Define o "o quê" e o "como" de cada componente, independente de produto.
> Idêntico ao `ds-components.md` original, com uma seção nova: mapeamento de cada componente pro shadcn/ui.
>
> **Quando consultar**
> Sempre que for construir, revisar ou validar um componente. Antes de qualquer implementação, verificar: o componente existe aqui? Quais são seus estados? Há variação mais adequada ao contexto? O shadcn já resolve isso pronto, ou precisa de composição?
>
> **Hierarquia dos documentos**
> `ds-foundations_v4.md` → tokens, escalas, princípios (consultar para valores de base)
> `ds-components_v4.md` (este) → specs de componente + mapeamento shadcn/ui
> `ds-patterns.md` → como componentes se organizam em telas
> `uikit-[projeto].html` → implementação visual real (prevalece sobre este arquivo para valores visuais)
> `Engineering-directives_v4.md` → regras de implementação técnica na stack shadcn/ui
>
> **Regra geral**
> Sempre reutilizar um componente existente antes de criar um novo. Se nenhum componente existente serve, sinalizar — não inventar.

---

## Hierarquia de fontes por tipo de pergunta

> **Esta seção é a regra, não uma convenção.** Ela existe porque uma cadeia inteira de
> especificação, protótipo e revisão deixou passar seis divergências do design system em
> componentes que estavam **dentro** do catálogo. A causa medida: quem construía consultava
> só este documento, e este documento não é a fonte mais completa nem a mais atual para
> **anatomia**.

| A pergunta é sobre | A fonte é | Por quê |
|---|---|---|
| **Anatomia** — quais partes o componente tem, quais props aceita, o que já vem pronto | o `.tsx` em `src/components/ui/` | É o mais completo e o mais atual. Os componentes desta biblioteca são comentados decisão por decisão, e essas decisões não estão em lugar nenhum além do arquivo |
| **Comportamento e regra de uso** — quando usar, qual variação, o que é proibido | este documento | É onde o "quando usar / não usar" e as árvores de decisão vivem |
| **Valor de cor** | `src/index.css` | O CSS real prevalece sobre a doc para valor visual |
| **Exemplo de composição** | `src/showcase/` | **Auditável, nunca verdade.** Ver a regra abaixo |

**O showcase é auditável, nunca verdade.** Ao copiar dele, confira contra a spec deste
documento e contra o `.tsx`. Se divergir, **a spec ganha** e a divergência do showcase vira
débito registrado. Isto não é desconfiança gratuita: o `showcase/Dados.tsx` chegou a ter
duas paginações que divergiam desta spec e uma da outra, e é o arquivo que todo projeto novo
copia.

### Sem entrada neste documento, o componente É a spec

**17 dos 53 componentes da biblioteca não têm entrada própria aqui** (23, se a conta for
"entrada com o próprio nome", sem contar as famílias). Para todos eles vale a regra
explícita, e não a suposição de que "não está documentado, então posso fazer como quiser":

> Componente sem entrada neste documento → **o `.tsx` dele é a spec**. Anatomia, props,
> defaults e decisões saem do arquivo e dos comentários dele. Divergir do arquivo é a mesma
> coisa que divergir de uma spec escrita, e precisa ser declarado como divergência.

Os que hoje não têm entrada própria:

`accordion` · `alert-dialog` · `badge` · `collapsible` · `command` · `dropdown-menu` ·
`field` · `internal-control` · `label` · `multi-select` · `navigation-menu` ·
`password-input` · `responsive-dialog` · `separator` · `toggle` · `toggle-group` ·
`unsaved-guard`

⚠️ **Dois pares desta lista são armadilha de escolha, e já produziram defeito:**
`accordion` × `collapsible` (os dois abrem e fecham conteúdo; o `accordion` é o item de
lista com anatomia de linha de tabela, o `collapsible` é o primitivo cru) e
`multi-select` × `combobox` (os dois abrem lista com busca; um é múltipla escolha, o outro
é escolha única). Antes de escolher entre eles, abra os dois arquivos.

---

## Mapeamento shadcn/ui

Antes de implementar qualquer componente abaixo, checar esta tabela. "Direto" significa que o shadcn resolve pronto via CLI. "Composição" significa montar com mais de uma primitiva shadcn/Radix — documentar a composição no próprio arquivo do componente quando isso acontecer. "Sem equivalente" significa que não existe solução shadcn/Radix, nem por composição — precisa de biblioteca externa ou construção própria.

| Componente | Status shadcn/ui | Observação |
|---|---|---|
| Button | Direto | `Button`, variantes via prop `variant` |
| Icon Button | Direto | `Button` com `size="icon"` |
| Button Group | Composição | Flex de `Button`, ou `ToggleGroup` para variante segmentada |
| Floating Action Button | Sem equivalente | Construir com `Button` + posicionamento próprio |
| Split Button | Composição | `Button` + `DropdownMenu` |
| Input Text | Direto | `Input` |
| Textarea | Direto | `Textarea` |
| Select Base | Direto | `Select` |
| Select com Busca (Autocomplete) | Composição | `Popover` + `Command` |
| Multi Select | Composição | `Popover` + `Command` + `Badge` (receita da comunidade, não vem pronta) |
| Async Select | Composição | Mesma base do Select com Busca + estado de loading próprio |
| Combobox | Composição | `Popover` + `Command` |
| Checkbox | Direto | `Checkbox` |
| Radio | Direto | `RadioGroup` |
| Switch | Direto | `Switch` |
| Date Picker Single | Composição | `Calendar` + `Popover` |
| Date Range Picker | Composição | `Calendar` (modo range) + `Popover` |
| Date Time Picker | Composição | `Calendar` + `Popover` + input de hora à parte — sem receita pronta |
| Slider (Single/Range/Step) | Direto | `Slider` — range e step são configuração do mesmo componente |
| Upload (todas as variações) | Sem equivalente | Não existe no shadcn. Usar input file nativo estilizado, ou lib externa (ex: react-dropzone) para variação com dropzone |
| Alert | Direto | `Alert` |
| Toast | Direto | `Sonner` (recomendação oficial do shadcn/ui para toast) |
| Loading | Sem equivalente | Não existe componente próprio — usar spinner customizado simples |
| Skeleton | Direto | `Skeleton` |
| Progress | Direto | `Progress` |
| Navbar | Composição | `NavigationMenu` + layout próprio |
| Sidebar | Direto | `Sidebar` (componente oficial do shadcn/ui) |
| Tabs | Direto | `Tabs` |
| Breadcrumb | Direto | `Breadcrumb` |
| Pagination | Direto | `Pagination` |
| Stepper | Sem equivalente | Não existe pronto — construir sobre `Progress`/lista numerada, ou usar lib externa |
| Link | N/A | Elemento nativo estilizado, não é componente shadcn |
| Card (todas as variações) | Direto | `Card` — variações (Resumo/Informativo/Interativo) são composição de conteúdo, não componentes diferentes |
| Data Table básica | Direto | `Table` |
| Table com Interações / Expansão | Composição | `Table` + `TanStack Table` por trás para ordenação/seleção |
| Data Grid avançada | Sem equivalente | Exceção documentada — usar `TanStack Table` (ou similar) como motor, casca visual em Tailwind/shadcn |
| Drawer | Direto | `Sheet` (nome do componente no shadcn/ui) |
| Modal | Direto | `Dialog` |
| Dialog (confirmação) | Direto | `Dialog` (mesma base do Modal, conteúdo mais enxuto) — ou `AlertDialog` para confirmação destrutiva |
| Popover | Direto | `Popover` |
| Tooltip | Direto | `Tooltip` |

---

## Índice de componentes

- **Actions** → Button, Icon Button, Button Group, Floating Action Button, Split Button
- **Inputs** → Input Text, Textarea, Select (família), Combobox, Checkbox, Radio, Switch, Date Picker (família), Slider (família), Upload (família)
- **Feedback** → Alert, Toast, Loading, Skeleton, Progress
- **Navegação** → Navbar, Sidebar, Tabs, Breadcrumb, Pagination, Stepper, Link
- **Data Display** → Card (família), Table (família)
- **Overlay / Surface** → Drawer, Modal, Dialog, Popover, Tooltip

---

## Actions

Componentes que permitem ao usuário **executar ações** — pontos de decisão e interação direta.

**Usar quando:** o usuário precisa executar uma ação, existe decisão clara a ser tomada, ou é necessário disparar evento no sistema.
**Não usar quando:** a intenção é navegar (→ Navegação), exibir informação (→ Data Display), coletar dado (→ Inputs), ou comunicar estado (→ Feedback).

**Hierarquias possíveis:** Primária / Secundária / Terciária / Danger
**Formatos:** Texto + ícone / Apenas texto / Apenas ícone
**Tamanhos:** Small (32px) / Medium (40px) / Large (48px)
**Estados universais:** Default / Hover / Focus / Active / Disabled / Loading

**Regras gerais de Actions:**
- Apenas uma ação primária por contexto
- Labels claros e orientados à ação
- Ações destrutivas sempre usam Danger
- Fornecer feedback imediato após ação

**Qual usar?**

```
Ação principal da tela (salvar, enviar, confirmar)?
  → Button primário (só 1 por contexto)

Ação de apoio, importância visual reduzida?
  → Button secundário / terciário / ghost

Só ícone, espaço curto (toolbar, linha de tabela)?
  → Icon Button (exige tooltip)

Várias ações relacionadas lado a lado?
  → Button Group (ou segmentado via ToggleGroup)

Uma ação principal + variações no mesmo botão?
  → Split Button

Ação flutuante persistente (criar novo, sempre visível)?
  → Floating Action Button (exige tooltip)
```

---

### Button

**Descrição**
Executa ações dentro da interface. Comunica intenção, prioridade e consequência.

**Anatomia:** Container + Label + Ícone (opcional, `startIcon` e/ou `endIcon` — slots explícitos, não ícone solto misturado no texto) + Indicador de loading (opcional)

**Quando usar:** o usuário precisa executar uma ação clara com destaque na interface.
**Não usar:** ação secundária demais (→ Link), sem ação clara definida, excesso de botões na mesma área.

**Variações**

| Variação | Uso | Destaque |
|---|---|---|
| Primário | Ação principal da tela | Máximo |
| Secundário | Ações alternativas | Menor que primário |
| Terciário | Ações de baixo impacto | Discreto (ghost/text) |
| Danger | Ações destrutivas ou irreversíveis | Uso com cautela |

**Tamanhos:** Small (32px) / Medium (40px) / Large (48px)

**Ícone:** `startIcon` (esquerda), `endIcon` (direita), os dois juntos, ou nenhum — os três casos são só composição, não variações separadas do componente.

**Loading:**
- Desabilita o botão sozinho (não precisa passar `disabled` junto)
- Botão só-ícone: o spinner **substitui o ícone inteiro**
- Botão com label: o spinner **nasce sempre na posição de `endIcon`**, substituindo-o se houver um — nunca na posição de `startIcon`

**Regras:**
- **Apenas 1 botão primário por tela**
- Labels orientados à ação: "Salvar", "Enviar", "Excluir" — nunca "OK" ou "Confirmar" sem contexto
- Danger apenas em ações críticas
- Loading state durante processamento — não permite múltiplos cliques em ações críticas

**Acessibilidade:** Tab/Enter/Space, foco visível, label acessível (especialmente ícone-only), contraste adequado.

---

### Icon Button

**Descrição**
Botão representado apenas por ícone. Usado para ações compactas.

**Anatomia:** Container circular ou quadrado + Ícone

**Quando usar:** espaços reduzidos, ações recorrentes e reconhecíveis (editar, excluir), toolbars.
**Não usar:** quando a ação não é óbvia; ações críticas sem label.

**Tamanhos:** Small (32px) / Medium (40px) / Large (48px)

**Regras:**
- Ícone deve ser universalmente compreensível no contexto
- **Tooltip sempre obrigatório** — não é condicional a "quando a ação não é óbvia", vale para todo botão só-ícone sem exceção. Reforçado em nível de tipo na implementação (ver `Engineering-directives_v4.md`)
- Usar `aria-label` descritivo sempre (derivado automaticamente do texto do tooltip, se não for passado outro)

---

### Button Group

**Descrição**
Agrupamento de botões relacionados organizados como unidade.

**Anatomia:** Container do grupo + Botões (2 ou mais)

**Quando usar:** ações relacionadas, alternativas de escolha, filtros ou modos de visualização.
**Não usar:** ações não relacionadas, mais de 5 opções (considerar outro padrão).

**Variações:** Horizontal / Vertical / Segmentado (seleção única)
**Tamanhos:** Small (32px) / Medium (40px) / Large (48px)

**Regras:** Botões devem ser do mesmo contexto. Limitar a 3–5 itens.

---

### Floating Action Button (FAB)

**Descrição**
Botão flutuante que representa uma **ação principal global**, geralmente fixo na tela.

**Anatomia:** Container circular + Ícone

**Quando usar:** ação principal recorrente, interfaces mobile, criação rápida ("+ adicionar").
**Não usar:** quando há muitas ações diferentes, interfaces densas com muitas ações já visíveis.

**Regras:**
- Apenas 1 FAB por tela, representando ação principal global
- Sempre só-ícone → tooltip obrigatório, mesma regra do Icon Button
- Variação "speed dial": clique revela sub-ações empilhadas em coluna acima do botão principal (sem primitiva shadcn/Radix, ver mapeamento). Cada sub-ação também é só-ícone → também exige tooltip

---

### Split Button

**Descrição**
Combina ação principal com menu de ações secundárias.

**Anatomia:** Botão principal + Divisor + Botão secundário (abre menu) + Dropdown

**Quando usar:** existe ação padrão + variações, ações relacionadas com frequência diferente.
**Não usar:** apenas uma ação disponível, quando o menu pode confundir o usuário.

**Regra:** Ação principal deve ser clara; itens do menu devem ser diretamente relacionados.

---

## Inputs

Componentes que permitem ao usuário **inserir, selecionar ou modificar dados**.

**Usar quando:** usuário precisa fornecer dados, configurar algo, ou há fluxo de formulário.
**Não usar quando:** a informação é apenas exibida (→ Data Display), a ação é executar algo (→ Actions), intenção é navegar (→ Navegação).

**Regras gerais de Inputs:**
- Placeholder não substitui label — label deve ser sempre visível
- Campos obrigatórios claramente indicados
- Mensagens de erro específicas e úteis (não "campo inválido")
- Validação consistente em todos os inputs do sistema
- Labels associados corretamente (acessibilidade)

**Qual usar?**

```
Texto curto de linha única (nome, e-mail)?
  → Input Text

Texto longo (observações, descrição)?
  → Textarea

Escolher de uma lista pré-definida?
  → Select (ver família: Base / Busca / Multi / Async)

Digitar valor livre OU escolher da lista?
  → Combobox

Uma data ou período?
  → Date Picker (ver família)

Escolha binária ligada/desligada, efeito imediato?
  → Switch

Marcar uma ou várias opções (requer submissão)?
  → Checkbox

Escolher exatamente uma entre poucas opções visíveis?
  → Radio

Valor num intervalo, precisão não crítica?
  → Slider (ver família)

Enviar arquivo?
  → Upload (ver família)
```

---

### Input Text

**Descrição**
Entrada de dados textuais. Base para campos de busca e selects com digitação.

**Anatomia:** Label (opcional) + Campo + Placeholder + Helper text (opcional) + Mensagem de erro + Contador de caracteres (opcional) + Ícone (opcional, esquerda ou direita)

**Quando usar:** inserir dados textuais curtos ou médios, preencher formulários, realizar buscas, informações abertas sem opções pré-definidas.
**Não usar:** conjunto fechado de opções (→ Select), formato rígido (→ componente especializado), conteúdo longo (→ Textarea).

**Altura padrão:** 40px

**Estados:** Default / Focus (borda ativa) / Erro (borda vermelha + mensagem abaixo) / Disabled (fundo `gray-100`, texto `gray-400` — nunca opacidade reduzida, ver `ds-foundations_v4.md` §1)

**Validação:** pode ocorrer em tempo real, ao blur, ou ao submeter o formulário.

**Contador de caracteres:** opcional, é uma variável — pode existir ou não. Implementado via props `showCount` + `maxLength` juntos; sem os dois, não aparece nada. Posição: abaixo do campo, alinhado à direita.

---

### Textarea

**Descrição**
Entrada de textos longos e não estruturados — descrições, observações, justificativas.

**Anatomia:** Label (opcional) + Campo multilinha + Placeholder + Helper text (opcional) + Mensagem de erro + Contador de caracteres (opcional)

**Quando usar:** descrições longas, observações, comentários, conteúdo aberto não estruturado.
**Não usar:** conteúdo curto (→ Input Text), formato específico (→ componente especializado), seleção de opções (→ Select/Checkbox).

**Altura padrão:** 200px (comporta múltiplas linhas sem scroll imediato)

**Estados:** Default / Focus / Erro / Disabled (fundo `gray-100`, texto `gray-400` — nunca opacidade reduzida, ver `ds-foundations_v4.md` §1)

**Contador de caracteres:** opcional, é uma variável — pode existir ou não. Implementado via props `showCount` + `maxLength` juntos; sem os dois, não aparece nada. Posição: abaixo do campo, alinhado à direita.

---

### Select (família)

Permite selecionar uma ou mais opções de listas pré-definidas. Quatro variações por complexidade.

**Estrutura compartilhada:** Label (opcional, associado via `htmlFor`/`id` — clicar no label ativa o campo) + Campo de seleção + Placeholder + Helper text (opcional) + Mensagem de erro. Altura padrão: **40px**. Disabled: mesmo cinza real do Input/Button (`gray-100`/`gray-400`), vale nas 4 variações (Base, Busca, Multi, Async).

**Qual usar?**

```
Até ~10 opções?
  → Select Base

Mais de 10–15 opções, usuário precisa buscar?
  → Select com Busca (Autocomplete)

Usuário pode inserir valor que não está na lista?
  → Input ou Combobox

Pode selecionar mais de uma opção?
  → Multi Select

Dados vêm de API ou lista muito grande?
  → Async Select
```

**Select Base** — seleção simples de listas curtas. Abre dropdown ao clicar, fecha após seleção.

**Select com Busca (Autocomplete)** — filtragem por digitação. Usar para listas com 10+ opções. Suporta busca parcial.

**Multi Select** — múltiplas seleções. Exibe itens selecionados como chips. Permite remoção individual.

**Async Select** — dados carregados dinamicamente via API. Sempre incluir loading state e tratamento de erro.

---

### Combobox

**Descrição**
Combina campo de texto livre com lista de sugestões. O usuário pode digitar um valor novo ou selecionar uma opção existente.

**Diferença do Select com Busca:** no Select com Busca, o valor final deve ser da lista. No Combobox, o usuário pode inserir valor fora da lista.

**Quando usar:** autocomplete com possibilidade de valor livre, sugestões não exaustivas.

---

### Checkbox

**Descrição**
Seleção múltipla ou confirmação de uma opção. Requer submissão para efeito.

**Quando usar:** múltiplas opções independentes, confirmação de termos, seleção em lista.
**Não usar:** estado binário com efeito imediato (→ Switch), seleção única exclusiva (→ Radio).

**Estados:** Default / Checked / Indeterminate / Hover / Focus / Disabled

**Regra:** área de clique deve incluir o label — nunca só o checkbox visual.

---

### Radio

**Descrição**
Seleção única exclusiva entre opções de um grupo.

**Quando usar:** escolha exclusiva obrigatória entre opções, decisão que precisa ser explícita.
**Não usar:** múltiplas seleções (→ Checkbox), estado binário imediato (→ Switch), muitas opções (→ Select).

**Regras:**
- Sempre organizar em grupo lógico com label de grupo
- Deve haver sempre estado inicial claro (pré-selecionado ou nenhum, quando permitido)
- Limitar a 5–7 opções; mais do que isso → Select

---

### Switch

**Descrição**
Estado binário (ligado/desligado) com efeito **imediato**, sem necessidade de confirmação.

**Quando usar:** ativar/desativar funcionalidade, efeito instantâneo, ação reversível.
**Não usar:** decisão que precisa de confirmação (→ Checkbox), dentro de formulário com submissão posterior.

**Estados:** Off / On / Hover / Focus / Disabled

**Regra:** mudança reflete imediatamente no sistema — se precisar de salvar, usar Checkbox.

---

### Date Picker (família)

Seleção de datas. Três variações por necessidade.

**Estrutura compartilhada:** Label (opcional) + Input + Placeholder com formato + Overlay de calendário + Navegação de mês/ano. Altura padrão: **40px**.

**Qual usar?**

```
Uma única data?
  → Date Picker (Single)

Intervalo de datas (início e fim)?
  → Date Range Picker

Data + horário?
  → Date Time Picker

Existem restrições de negócio (limites, datas bloqueadas)?
  → Tipo escolhido + validações configuradas
```

**Date Picker Single** — calendário para data única. Fecha após seleção. Padrão default do shadcn/Calendar, sem sidebar nem etapa de confirmação. Bloqueio de datas via prop `disabledDates` (ex: data de nascimento não pode ser futura → `{ after: new Date() }`).

**Date Range Picker** — dois calendários lado a lado (via `numberOfMonths={2}` do Calendar, que já resolve nativamente clique início/fim e troca de ordem). Diferente do Single: **não aplica direto** — sidebar de atalhos (Hoje/Ontem/Últimos 7 dias/Este mês/Mês anterior/Este trimestre/Trimestre anterior/Este ano, com detecção automática do atalho ativo pelas datas atuais) + contador de dias selecionados + rodapé com Limpar/Aplicar. Modelo herdado do range picker legado do projeto — mantido de propósito por já validado com o usuário. Usa `showOutsideDays={false}` (só aqui, não no Single/DateTime): num picker de dois meses, o dia que vaza pro mês vizinho apareceria duplicado e, quando é início/fim do período, pintado nos dois calendários.

**Date Time Picker** — Calendar (`mode="single"`) + Popover + campo de hora à parte. A hora usa `<Input type="time">` nativo (HH:mm, granularidade de minuto) em vez de selects de hora/minuto: mais simples e já traz teclado/acessibilidade de graça. Segue o mesmo padrão de duas etapas do Range Picker — edita em estado `pending` e só confirma via Limpar/Aplicar. Enquanto não houver data selecionada, o campo de hora e o botão Aplicar ficam desabilitados (o dia define a base; a hora só faz merge sobre ela). Bloqueio de datas via `disabledDates`, igual ao Single.

---

### Slider (família)

Seleção de valores em intervalo contínuo ou discreto.

**Estrutura compartilhada:** Label (opcional) + Track + Thumb + Valor mínimo e máximo.

**Qual usar?**

```
Valor único?
  → Slider (Single Value)

Intervalo (mínimo e máximo)?
  → Range Slider

Valores discretos com incrementos definidos?
  → Slider com Step/Ticks
```

**Regra geral:** usar slider apenas quando a interação visual agrega valor. Para precisão crítica, usar Input.

**Implementação:** as três variações são o mesmo `Slider` do shadcn/Radix, muda só a prop — Single `value={[n]}` (um thumb), Range `value={[a, b]}` (dois thumbs, Radix já ordena e limita), Step `step={n}` (incrementos discretos). Disabled é cinza real (Gray-200 track / Gray-300 range e thumb / Gray-100 fundo do thumb), não opacidade reduzida — mesma regra do Button/Input; como o Radix propaga `data-disabled` pra Track/Range/Thumb, cada parte é pintada direto. Focus ring alinhado ao resto do boilerplate (`ring-[3px]`, não o `ring-4` que vem do shadcn). Exibir o valor atual ao lado do Label quando ele importa pro usuário.

---

### Upload (família)

Envio de arquivos. Quatro variações por complexidade.

**Qual usar?**

```
Um único arquivo, fluxo simples?
  → Upload Simples

Múltiplos arquivos?
  → Upload Múltiplo

Imagens ou conteúdo visual com preview?
  → Upload com Preview

Arquivos grandes, upload demorado, precisa de feedback de progresso?
  → Upload Assíncrono (com progresso)

Drag and drop melhora a experiência?
  → Adicionar Dropzone ao tipo escolhido
```

**Regras gerais:** informar restrições antes da interação (tipo, tamanho máximo), permitir remover/cancelar, tratar erros por arquivo.

**Implementação:** sem primitiva no shadcn/Radix (o registry tem 61 componentes, nenhum de arquivo) — construído sobre `<input type="file">` nativo. As quatro variações e o dropzone são combinações de props do mesmo componente `Upload`: Simples (padrão), Múltiplo (`multiple`), Preview (`preview` → thumbnail de imagem via `URL.createObjectURL`), Assíncrono (`simulateUpload` → barra de progresso) e Dropzone (`dropzone` → área de arrastar-e-soltar, soma a qualquer variação). O **dropzone é feito na mão** com os eventos nativos de drag (`onDragOver/onDragLeave/onDrop`), sem lib externa (decisão do projeto: evitar dependência). O progresso assíncrono é **MOCK** (timer), sem backend — trocar por progresso real de XHR/fetch na integração. A barra de progresso é interna e provisória (div + width dinâmico via `style`, regra 13) até o componente `Progress` do shadcn entrar na base; marcada com `INTEGRATION BOUNDARY`. Disabled é cinza real (Gray-200/100/400), não opacidade. Erro é por arquivo (tipo/tamanho), com cor `destructive`.

---

## Feedback

Componentes que comunicam ao usuário o **estado do sistema, resultado de ações ou informações relevantes**.

**Regras gerais:**
- Mensagens claras, objetivas e úteis — nunca "Erro ocorreu"
- Feedback de erro deve explicar como resolver
- Evitar múltiplos feedbacks simultâneos conflitantes
- Usar nível de interrupção adequado à gravidade

**Níveis de interrupção:**
- Não intrusivo → Toast, Skeleton
- Moderadamente intrusivo → Alert inline
- Altamente intrusivo → Modal, Dialog

**Qual usar?**

```
Confirmar resultado de uma ação, sem interromper (salvo, enviado)?
  → Toast

Comunicar estado persistente na tela (aviso, erro de formulário)?
  → Alert inline (4 variantes semânticas)

Conteúdo ainda carregando, quero preservar o layout?
  → Skeleton

Operação com duração/etapas mensuráveis?
  → Progress (linear/circular)

Espera curta e indeterminada?
  → Loading (spinner)

Decisão que precisa interromper e bloquear o fluxo?
  → Modal / Dialog (ver Overlay / Surface)
```

---

### Alert

**Descrição**
Mensagens importantes e persistentes dentro da interface, sem bloquear o fluxo.

**Anatomia:** Ícone (opcional) + Título (opcional) + Texto + Ação (opcional) + Fechar (opcional)

**Quando usar:** mensagens que precisam persistir (problemas de configuração, avisos de contexto), feedback dentro de formulário.
**Não usar:** mensagens temporárias (→ Toast), situação que exige bloqueio (→ Modal/Dialog).

**Variações:** Success / Error / Warning / Info. Com ou sem ação. Inline ou full-width.

**Estados:** Default / Dismissed

**Implementação:** `shadcn add alert` ("Direto"), mas reescrito de grid pra **flex** (regra de layout do projeto) e estendido pras 4 variantes semânticas (o shadcn só traz `default`/`destructive`). Ícone é automático por variante (Info/CheckCircle2/AlertTriangle/XCircle do Lucide), sobrescrevível via `icon` (ou `icon={null}` pra esconder) — cor + ícone juntos, nunca cor como único sinal. Fundo tingido `/10` + borda `/30`–`/40`; **título em `foreground` e descrição em `muted-foreground`** de propósito, pra garantir contraste AA sem depender da cor semântica no texto (amber/red em texto pequeno falham AA). Ação via prop `action`; fechar via `onDismiss` (botão ícone-only com tooltip).

---

### Toast

**Descrição**
Feedback temporário e não intrusivo após uma ação.

**Anatomia:** Texto + Ícone (opcional) + Ação (opcional)

**Quando usar:** confirmação rápida pós-ação, feedback leve de sistema.
**Não usar:** mensagens críticas que exigem leitura; situações que requerem ação obrigatória.

**Variações:** Success / Error / Warning / Info

**Comportamento:** aparece automaticamente, some após tempo definido (tempo suficiente para leitura). Evitar múltiplos simultâneos.

**Implementação:** `shadcn add sonner` ("Direto", base Sonner). Monta-se `<Toaster />` uma vez no root e dispara com `toast.success/error/warning/info("Título", { description?, action? })`. Anatomia: ícone + título + **descrição opcional** (o segundo parâmetro `description` do Sonner, usar quando o UX pedir) + ação. Divergências do que o shadcn gera:
- **Removido o next-themes** — o dark mode do projeto é a classe `.dark` manual, então o tema é lido dela direto, sem depender de `ThemeProvider`.
- **Superfície neutra (popover)** — sem fundo tingido; o sinal semântico vem do ícone + do texto (cor nunca é o único sinal).
- **Ícone preenchido (filled)** por variante: disco na cor semântica via `fill="var(--…)"` no ícone Lucide + glifo no token `-foreground` (branco em success/error/info, escuro no warning) — garante contraste do glifo. Setado inline no `sonner.tsx`.
- **Título** em `popover-foreground` e **descrição** em `muted-foreground`, estilizados no index.css (mesma filosofia do Alert, texto sempre legível). A descrição usa `!important` porque o Sonner injeta a cor dela com seletor mais específico em runtime.
- **Posição fixa topo-direita** (`position="top-right"`).
- **Barra de contagem regressiva** por toast: pseudo-elemento `::after` que encolhe (`scaleX` 1→0) na duração do toast (`--toast-duration`, default 4000ms), na cor da variante (primary quando sem tipo). Pausa no hover (junto com o auto-dismiss do Sonner) e é desligada em `prefers-reduced-motion`. Duração custom exige passar o mesmo valor em `style: { "--toast-duration" }` na chamada.
- Spinner de loading respeita `motion-reduce`.

---

### Loading

**Descrição**
Indica processamento em andamento.

**Anatomia:** Spinner ou barra de progresso indeterminada

**Quando usar:** aguardar resposta do sistema, operação sem duração previsível.
**Não usar:** carregamento longo de conteúdo estruturado (→ Skeleton).

**Variações:** Inline / Fullscreen. Tamanhos: Small / Medium / Large.

**Implementação:** sem base no shadcn — composição própria sobre o spinner `Loader2` do Lucide (mesmo do Button), `animate-spin` com `motion-reduce`. Tamanhos Small 16 / Medium 24 / Large 48 (spinner de progresso, não ícone de UI — daí sair da escala 16/20/24). Inline (default) é um `<span role=status>` com label opcional; fullscreen é um overlay `position:fixed inset-0 z-50` com backdrop `bg-background/80` e spinner centralizado (fixed é overlay, não layout — permitido). Sem label, um texto `sr-only` "Carregando" garante o anúncio pro leitor de tela. A alternativa "barra indeterminada" do doc já é o `Progress` sem `value` — não duplicado aqui.

---

### Skeleton

**Descrição**
Representa o layout enquanto o conteúdo carrega. Reduz percepção de espera.

**Anatomia:** Blocos estruturais que espelham o layout real do conteúdo

**Quando usar:** carregamento de conteúdo com estrutura conhecida (cards, listas, tabelas).
**Não usar:** ações rápidas (< 300ms) — usar Loading.

**Variações:** Texto / Card / Lista / Tabela

**Regra:** Skeleton deve refletir o layout real — não usar blocos genéricos que não correspondem ao conteúdo final.

**Implementação:** `shadcn add skeleton` ("Direto"). É um único bloco pulsante (`bg-muted`, radius via `--radius`), sem variantes — as variações Texto/Card/Lista/Tabela são **composições**: monta-se o layout com vários `<Skeleton>` de tamanhos diferentes espelhando o conteúdo real. Pulsação respeita `prefers-reduced-motion` (`motion-reduce:animate-none`).

---

### Progress

**Descrição**
Indica o progresso de uma tarefa com duração conhecida.

**Anatomia:** Barra ou indicador circular + Valor percentual (opcional)

**Quando usar:** processos longos com duração estimável (upload, processamento em lote).
**Não usar:** processos rápidos (→ Loading).

**Variações:** Determinado (valor conhecido) / Indeterminado (duração variável). Linear / Circular.

**Regra:** nunca usar progresso falso — deve refletir o estado real.

**Implementação:** `shadcn add progress` traz só o **linear determinado**. Estendido pra cobrir a matriz inteira: **linear indeterminado** (`<Progress />` sem `value` → barra desliza; keyframe `progress-indeterminate` em `index.css`, só `transform`, com `motion-reduce`) e **circular** (`<CircularProgress>`, composição SVG própria — não existe no shadcn; determinado via `stroke-dashoffset`, indeterminado via `animate-spin`, `showValue` opcional pro % central). O gráfico circular é SVG (não ícone Lucide) porque é encoding de dado contínuo, permitido pela regra de ícones. É o `Progress` que fecha o `INTEGRATION BOUNDARY` da barra do Upload assíncrono.

---

## Navegação

Componentes que permitem ao usuário **se mover entre páginas, seções ou estados do sistema**.

**Usar quando:** o usuário precisa mudar de contexto, navegar entre páginas ou entender sua localização.
**Não usar quando:** a intenção é executar uma ação (→ Button), exibir dado (→ Data Display), ou coletar dado (→ Inputs).

**Regras gerais:**
- Estado ativo sempre visível
- Labels claros e descritivos
- Estrutura semântica adequada (nav, ul, li)
- Evitar profundidade excessiva de hierarquia

**Qual usar?**

```
Navegação principal entre páginas, no topo?
  → Navbar

Muitas seções / hierarquia, acesso lateral constante?
  → Sidebar (vira Drawer no mobile)

Alternar visões do MESMO contexto, sem trocar de página?
  → Tabs

Mostrar onde o usuário está numa hierarquia de 3+ níveis?
  → Breadcrumb

Percorrer páginas de uma listagem grande?
  → Pagination

Fluxo linear com etapas sequenciais (wizard)?
  → Stepper

Levar a outra página/recurso dentro de um texto?
  → Link
```

---

### Navbar

**Descrição**
Organiza e dá acesso às principais áreas do sistema. Geralmente posicionada no topo.

**Anatomia:** Logo/Branding + Links de navegação + Itens de ação + Menu do usuário + Busca (opcional) + Indicadores (ex: notificações)

**Quando usar:** sistema com múltiplas áreas principais, acesso rápido necessário, consistência entre páginas.
**Não usar:** aplicação de tela única, navegação já resolvida por Sidebar dominante, interface focada/imersiva.

**Variações:** Com links / Com dropdown / Com busca / Com ações / Fixa (sticky) / Scrollável

**Tamanho padrão:** 56px de altura

**Estados:** Default / Hover (itens) / Active (página atual) / Focus / Scroll (com sombra)

**Regras:**
- Apenas itens essenciais — evitar excesso de links
- Logo à esquerda, ações à direita (padrão reconhecível)
- Deve ser responsiva (colapsar em telas menores)

---

### Sidebar

**Descrição**
Navegação lateral para sistemas com muitas seções ou hierarquia mais profunda. Geralmente lateral esquerda.

**Anatomia:** Logo/Branding (opcional) + Itens de navegação + Grupos de categorias + Ícones (opcional) + Estado ativo + Submenus (opcional) + Ações secundárias + Controle de colapso

**Quando usar:** sistema com muitas seções, hierarquia de navegação (níveis), acesso constante a áreas principais.
**Não usar:** sistema simples (poucas páginas), navegação linear, espaço horizontal crítico.

**Variações:** Expandida (com labels) / Colapsada (apenas ícones) / Com submenus (accordion) / Fixa / Retrátil (overlay)

**Tamanhos:** Largura expandida: 256px / Largura colapsada: 64px / Altura: 100% da viewport

**Estados:** Default / Hover / Active / Focus / Expandido / Colapsado / Submenu aberto

**Regras:**
- Máximo 2–3 níveis de hierarquia
- Em mobile: virar Drawer
- Em modo colapsado: tooltip ao hover para labels

**Implementação:** `shadcn add sidebar` ("Direto", componente oficial). Composição em `sidebar.tsx` sobre `SidebarProvider` (estado open/collapsed com persistência via cookie `sidebar_state`, 7 dias) + atalho de teclado **Ctrl/Cmd+B** para colapsar/expandir. Larguras via CSS var: **expandida 16rem (256px)**, **colapsada em ícone 4rem (64px)**, **mobile 18rem (288px)**. No mobile (`useIsMobile`, hook `@/hooks/use-mobile`) a Sidebar vira **Sheet** (Drawer), conforme a regra do DS. Modo colapsado usa `collapsible="icon"` com **Tooltip automático** nos itens (a label vira tooltip ao hover). Submenus via `SidebarMenuSub`. Usada como app-shell na demo do `src/App.tsx`. Cores próprias do sidebar via tokens `--sidebar-*` no `index.css`.

> **Responsividade:** parcial — o colapso desktop↔ícone e a virada mobile→Sheet estão validados. Auditoria responsiva completa da biblioteca (todos os breakpoints, todos os componentes) segue como dívida transversal no backlog (ver `CONTINUITY.md`).

---

### Tabs

**Descrição**
Navegação paralela entre seções de mesmo nível dentro de um contexto.

**Quando usar:** conteúdo dividido em seções claras e relacionadas, usuário precisa alternar entre visões do mesmo contexto.
**Não usar:** navegação entre páginas diferentes (→ Navbar/Sidebar), mais de 7 tabs visíveis, conteúdo pouco relacionado entre si.

**Variações:** Horizontal / Vertical / Com ícone / Com badge (contador)

**Estados:** Default / Hover / Active (tab atual) / Focus / Disabled

**Regras:** cada tab deve ter conteúdo substancialmente diferente; usar tabs para separar, não para fragmentar artificialmente.

**Implementação:** `shadcn add tabs` ("Direto", Radix). Dois estilos via prop `variant` no `TabsList`: **`line`** (sublinhado, indicador embaixo do item ativo — estilo preferido do projeto) e **`default`** (segmentado, fundo `muted`). Disabled trocado de opacidade pra cinza real (`text-gray-400`); `gap-1.5` do trigger ajustado pra `gap-2` (grid). Orientação horizontal/vertical via `orientation`; ícone/badge entram como filhos do `TabsTrigger`.

---

### Breadcrumb

**Descrição**
Indica a localização atual do usuário na hierarquia do sistema.

**Quando usar:** hierarquia de navegação com 3+ níveis, usuário precisa entender o caminho percorrido.
**Não usar:** sistemas flat sem hierarquia, tela inicial/raiz.

**Separador padrão:** `/` ou `›`

**Regra:** último item (página atual) não é clicável.

**Implementação:** `shadcn add breadcrumb` ("Direto"). `gap-1.5`/`gap-2.5` ajustados pra `gap-2`; separador (`ChevronRight`) e ellipsis alinhados à escala de ícone (16px). Último item é o `BreadcrumbPage` (`aria-current="page"`, sem link) e usa a **cor `primary`** (decisão do projeto — página atual destacada).

---

### Pagination

**Descrição**
Controla a navegação entre páginas de uma listagem.

**Quando usar:** listagens com volume alto de dados que não cabem em tela única.
**Não usar:** listas curtas (mostrar tudo), quando scroll infinito faz mais sentido para o contexto.

**Variações:** Com números de página / Com setas prev/next / Com seletor de itens por página

**Regras:** indicar sempre a página atual; mostrar quantidade total quando possível.

**Regras não-negociáveis (as três que a cadeia já errou):**

1. **Elipse obrigatória** quando a janela de páginas não cabe. Nunca listar todas as páginas: com 40 páginas o rodapé vira uma régua de 40 botões. Usar o `PaginationEllipsis`, que existe e é exportado.
2. **Contagem em texto**, na forma **"Mostrando 1 a 10 de 124 resultados"**. ⚠️ **Sem travessão:** a forma "Mostrando X-Y de Z", que esta spec pedia antes com **en dash**, viola a regra dura de copy do próprio design system. Escrever "a".
3. **Seletor de itens por página é um controle**, um `Select` de verdade (10/25/50/100, default 10). Texto fixo dizendo "10 resultados por página" **não** é o seletor: é a aparência dele sem a função.

**Anatomia por variant da tabela que o rodapé acompanha:**

| Variant da `Table` | Rodapé | Borda interna do `PaginationContent` |
|---|---|---|
| `spaced` (default) | Card compacto `w-fit`, com a anatomia de uma linha da tabela | **Sai.** O card já é a moldura; mantê-la produz moldura dupla e engorda o rodapé de 58px para 68px |
| `divided` | Faixa `border-t` de largura cheia, contagem à esquerda e controles à direita | **Fica.** Não há moldura externa |

**Implementação:** `shadcn add pagination` ("Direto"; usa `buttonVariants`). Gotcha corrigida: a variante da página ativa vinha como `outline` (inexistente no nosso Button) → trocada por `secondary`; padding `px-2.5` do prev/next ajustado pro grid (`px-4`). Página ativa = `isActive` no `PaginationLink`. Decisões do projeto: **textos e aria-labels em português** ("Anterior"/"Próximo"/"Mais páginas"/"paginação"); **borda `gray-100`** em volta dos controles (no `PaginationContent`).

⛔ **Não compor o rodapé de tabela à mão.** O `pagination.tsx` exporta **`TablePagination`**, que já entrega contagem, seletor de itens por página, elipse e a anatomia certa por variant. As props têm exatamente os nomes que o `useTablePagination` devolve, então o ponto de uso é `<TablePagination {...pg} onPageChange={pg.setPage} onPageSizeChange={pg.setPageSize} variant="divided" itemLabel="tickets" />`. As três regras acima eram cumpridas de forma diferente em cada cópia enquanto a composição era manual; agora não sobra o que divergir.

---

### Stepper

**Descrição**
Indica o progresso em fluxos com múltiplas etapas lineares.

**Quando usar:** fluxo de cadastro/configuração com etapas sequenciais, onboarding, wizard.
**Não usar:** navegação não linear, fluxos simples de 1–2 etapas.

**Variações:** Horizontal / Vertical / Com labels / Apenas ícones

**Estados:** Não iniciado / Em andamento / Concluído / Erro / Desabilitado

**Regras:** o usuário deve poder ver todas as etapas e entender sua posição. Não ocultar etapas futuras.

---

### Onboarding Guiado

**Descrição**
Motor de onboarding white label em quatro superfícies que formam um fluxo único: gatilho (bússola ao lado do título da seção), modal de boas vindas, tour ancorado em elementos reais da tela e pesquisa de satisfação ao concluir. Substitui o Tour Guiado (`tour`, descontinuado em 0.4.0).

**Quando usar:** onboarding de novo usuário numa tela de operação (lista, formulário, painel), apresentar uma jornada que atravessa telas, ensinar uma ação (abrir menu, painel, aba) mostrando onde clicar.
**Não usar:** dica pontual num único elemento (usar Tooltip), fluxo de poucos passos dentro de um formulário (usar Stepper), tela de consulta pura (não pede guia).

**Regra da porta única:** nem o disparo automático nem o gatilho manual levam direto ao passo a passo. Os dois abrem o modal, e só "Iniciar Tour Guiado" começa a sequência. O guia é marcado como visto no instante em que o modal aparece: quem fecha sem fazer nada não é abordado de novo automaticamente; o chamariz do gatilho continua convidando até o primeiro clique consciente.

**Variações (superfícies):**
- `Onboarding.Ajuda`: Button ícone (Compass) + Tooltip. Pulsa com anel enquanto o usuário não engajou.
- `Onboarding.Intro` + `Onboarding.Intro.Topicos`: Dialog com prosa, lista de tópicos e três saídas (iniciar, suporte, agora não).
- `Onboarding` (executor): recorte no overlay, radar (passo explicativo) ou anel (passo de ação), cartão em **balão** (janela com 700px ou mais de altura, ao lado do alvo, clampado à janela com 12px de folga) ou em **faixa** (abaixo de 700px, presa à borda com mais folga; alvo estreito e alto vira trilho e a faixa recua). Também renderiza a pesquisa.
- Pesquisa de satisfação: Dialog com escala de 5 pontos (`aria-pressed`, ícones Lucide com rótulo textual), comentário opcional, agradecimento por 1600ms.

**Estados:** inativo (gatilho com ou sem chamariz) / intro / passo explicativo (Voltar a partir do 2º; Finalizar no último) / passo de ação (sem Próximo, selo "Clique no destaque", anel, interação presa ao alvo mais o cartão) / com dica / aguardando alvo (`aguardarAlvo`: recorte segue o alvo, cartão espera 3 quadros estáveis, teto 1500ms) / alvo não encontrado (cartão centralizado com aviso, Próximo e Pular disponíveis) / faixa / csat (vazio, nota selecionada, enviado, dispensado) / reduced-motion (tudo estático).

**Vocabulário do passo** (`PassoOnboarding`): `target` (seletor, convenção `[data-onb="nome"]`), `title`, `content`, `placement` (`top|bottom|left|right|auto`), `spotlightClicks`, e em `data`: `acao`, `aguardarAlvo`, `avancarQuandoAparecer`, `rolar`, `dica`. Qualquer outra chave é livre para `aoEntrarPasso` dirigir a tela (fechar painel, trocar aba).

**Regras de autoria de guia:**
- Nunca ancore em elemento mais alto que a janela. Ancore no cabeçalho da seção ou no elemento interno que a copy explica.
- Ancore no invólucro visível, não no controle nativo. Componentes compostos (Input com ícone ou afixo, Select, Combobox) repassam `data-*` ao elemento interno, e o recorte abraçaria só ele, sem ícone e borda. Envolva o componente num `<div data-onb="...">` do tamanho do controle.
- Rolar é decisão do guia inteiro: se um passo tem `rolar`, todos os ancorados na página têm. Flutuante e gaveta ficam de fora.
- Passo de ação perto da borda de baixo precisa de `placement` explícito.
- Alvo condicional não vira passo: o que ele ensinaria entra no passo do campo que decide se ele aparece.
- Monte os passos condicionalmente; array vazio é a forma correta de dizer "nada a ensinar" (desliga auto disparo e chamariz).
- Tela de escrita não pede cliques que deixem alteração pendente. Passo final que dispara ação descreve, não pede o clique.
- O guia pode atravessar uma gaveta; nesse caso segure o fechamento dela enquanto `controle.ativo`. Ao concluir, devolva a tela ao estado em que o guia a encontrou.
- Jornada entre telas: `marcarContinuacaoOnboarding` na origem, `consumirContinuacaoOnboarding` no destino com `emCurso: true`. O total da jornada é declarado desde o passo 1.
- As três pontas (`useOnboarding`, `Onboarding.Intro`, `Onboarding`) precisam estar na árvore. Depois de um merge, varra os usos de `useOnboarding(` e confirme.

**Personalização pelo UI Kit:** cor, forma, tamanho, tipografia e movimento saem de variáveis `--onb-*` (`--onb-cor`, `--onb-superficie`, `--onb-raio`, `--onb-largura`, `--onb-largura-compacta`, `--onb-fonte`, `--onb-duracao-transicao`, `--onb-duracao-moldura`, `--onb-duracao-pulso`, entre outras) com default derivado dos tokens do projeto. Redeclarar no `index.css` do produto prevalece. Textos por `textos` no hook. Empilhamento: overlay e recorte em `z-index: 100`, radar, anel e cartão em 101; gavetas e modais do aplicativo (z-50) ficam abaixo.

**Implementação:** sem componente no shadcn; composição própria em `src/components/ui/onboarding/` sobre Button, Card, Dialog, Textarea e Tooltip, sem `react-joyride`. `use-onboarding.ts` (máquina de estados), `geometria.ts` (funções puras, testadas), `use-alvo.ts` (medição por quadro, espera de alvo, observação de surgimento), `use-interacao-presa.ts`, `rolagem.ts` (movimento mínimo no container certo, desconto do sticky), `persistencia.ts` (adapter localStorage, dois métodos obrigatórios), `continuacao.ts` (sessionStorage), `onboarding.css` (variáveis, moldura cônica com `@property`, radar, anel, chamariz, reduced-motion). Superfície de QA no cartão: `data-onboarding-alvo`, `data-onboarding-acao`, `data-onboarding-passo` e o contador em `[data-slot=onboarding-contador]`. Precisa de `TooltipProvider` na árvore.

> **Tour Guiado (`tour`) foi descontinuado na 0.4.0 do boilerplate** e substituído pelo Onboarding Guiado acima. Migração: `steps {path, anchor, title, description}` → `passos {target, title, content}` com `target` = `[data-onb="x"]`; `storageKey` → `id` (+ `versao`); `TourTrigger` → `Onboarding.Ajuda`; `TourOverlay` → `Onboarding.Intro` + `Onboarding`; passo em outra página → `marcarContinuacaoOnboarding` na origem e `jornada: { ...consumirContinuacaoOnboarding(id), emCurso: true }` no destino. Não use `tour` em tela nova.

---

### Link

**Descrição**
Navegação textual para outro contexto, página ou âncora.

**Quando usar:** referências internas ou externas, ações secundárias onde Button seria muito pesado visualmente.
**Não usar:** ações que modificam dados (→ Button), navegação principal (→ Navbar/Sidebar).

**Variações:** Inline (dentro de texto) / Standalone (link isolado)

**Regras:** underline em hover/focus, cor distinta do texto comum, indicar links externos.

**Implementação:** sem componente no shadcn — `<a>` nativo estilizado (`link.tsx`). Cor `primary`, underline só no hover/focus (`underline-offset-4`), focus ring `ring-[3px]` do boilerplate. Prop `external` adiciona o ícone `ArrowUpRight` (Lucide) + `target="_blank"` + `rel="noopener noreferrer"`. `inline-flex` serve tanto inline (dentro de texto) quanto standalone.

---

## Data Display

Componentes para **exibir dados, conteúdo e informações estruturadas**.

---

### Card (família)

Container visual para agrupar informações relacionadas. Três variações por tipo de conteúdo.

**Estrutura compartilhada:** Container + Header (opcional) + Corpo + Footer (opcional)

**Qual usar?**

```
Exibir métricas ou KPIs?
  → Card de Resumo (Dashboard)

Conteúdo descritivo, sem interação principal?
  → Card Informativo

Interação direta (clicar, executar ação)?
  → Card Interativo
```

**Card de Resumo (Dashboard)**
Para indicadores e métricas. Anatomia: Container + Título + Valor principal (destaque) + Indicador secundário (variação) + Gráfico (opcional). Pode atualizar dinamicamente e permitir drill-down.

**Card Informativo**
Leitura de conteúdo, sem ação. Priorizar escaneabilidade e hierarquia clara. Usar quando dados são descritivos, não estruturados em tabela.

**Card Interativo**
Clicável total ou com ações internas. Deve indicar claramente a interatividade (hover state, cursor). Evitar múltiplos pontos clicáveis conflitantes.

---

### Table (família)

Organiza dados estruturados em linhas e colunas. Quatro variações por complexidade e nível de interação.

**Estrutura compartilhada:** Cabeçalho (colunas) + Linhas (dados) + Células + Estados (loading, empty, erro)

> **Regra — sem rolagem horizontal (inegociável).** Uma tabela **não deve** ter scroll horizontal. Se as colunas não cabem na largura disponível, a saída **nunca** é ativar `overflow-x`; é **reduzir colunas**, nesta ordem de preferência:
> 1. **Priorizar** — mantenha só as colunas essenciais pra tarefa; corte o secundário.
> 2. **Realocar** — mova o secundário pra **Table com Expansão** (detalhe na linha), tooltip, ou um **Drawer de detalhe** ao clicar na linha.
> 3. **Repensar a densidade** — se ainda não cabe, a tela provavelmente pede outra abordagem (cards, agrupamento), não uma tabela mais larga.
>
> No mobile isso é ainda mais crítico: colunas secundárias colapsam/somem (ver responsividade), nunca viram scroll lateral. Exceção real: **Data Grid** com colunas configuráveis pelo usuário pode ter scroll como último recurso — mas o default segue sendo reduzir colunas.

**Qual usar?**

```
Apenas visualizar dados, sem interação?
  → Data Table (básica)

Usuário precisa selecionar, editar, excluir ou ordenar?
  → Table com Interações

Precisa mostrar detalhes adicionais sem poluir a tabela?
  → Table com Expansão

Manipulação avançada: edição inline, filtros complexos, alta densidade?
  → Data Grid (avançada)
```

**Data Table (básica)**
Leitura passiva, sem interação complexa. Priorizar legibilidade e alinhamento correto de dados. Variações: com/sem zebra striping, com/sem footer.

**Table com Interações**
CRUDs e gestão de dados. Suporta ações por linha (inline ou menu contextual), seleção com checkbox, e ordenação por coluna. Não sobrecarregar cada linha com excesso de ações.

**Table com Expansão**
Para dados hierárquicos. Clique na linha expande/recolhe conteúdo adicional abaixo. Não esconder informação crítica na expansão.

**Data Grid (avançada)**
Alto nível de interação. Suporta edição inline, drag and drop, filtros avançados, colunas configuráveis (redimensionar, reordenar, ocultar). Requer performance e consistência robustas.

---

## Overlay / Surface

Componentes que aparecem **sobre o conteúdo principal**, mantendo ou interrompendo o contexto da tela.

> **Regra — um overlay por vez, nunca empilhar (inegociável).** Overlay não sobe em cima de overlay. Quando um novo precisa aparecer, faça **switch** (fecha o atual e abre o próximo no lugar), nunca cascata:
> - **Modal sobre Modal → proibido.** Sempre switch.
> - **Popover sobre Modal / Popover sobre Drawer → proibido.** O Popover é leve e contextual; não dispara overlay pesado por cima — faz switch.
> - **Drawer → Modal/Dialog → permitido.** Esta é a **única** sobreposição aceita: um Drawer pode disparar um Modal (ex: formulário no Drawer → confirmação). O inverso (Modal abrindo Drawer) não.
>
> Motivo: pilha de overlays confunde o foco, o Escape e o "onde eu estou". Switch mantém um único contexto ativo. Confirmação destrutiva dentro de um Modal → resolver **inline** no próprio Modal, não abrir um Dialog por cima.

**Qual usar?**

```
Tarefa secundária num painel lateral, sem sair da tela?
  → Drawer (Sheet)

Conteúdo/fluxo focado que interrompe o contexto?
  → Modal

Confirmar/decidir algo curto (inclui ação destrutiva)?
  → Dialog (AlertDialog para destrutivo)

Conteúdo contextual por clique, ancorado a um elemento?
  → Popover

Dica curta ao passar mouse/foco, sem interação?
  → Tooltip

No mobile, um Modal ficaria apertado?
  → Modal vira Drawer (padrão do projeto)
```

---

### Drawer

**Descrição**
Painel lateral que desliza sobre a interface para tarefas secundárias, sem navegação completa para outra tela.

**Anatomia:** Overlay + Container lateral + Header (título + fechar) + Body (conteúdo) + Footer (ações, quando aplicável)

**Quando usar:** tarefa secundária sem precisar sair da tela, formulários rápidos de edição, filtros avançados, visualização de detalhes complementares.
**Não usar:** fluxo longo ou complexo (→ página dedicada), múltiplas etapas complexas, conteúdo que exige leitura extensa.

**Variações:** Lateral direito (padrão) / Lateral esquerdo / Full height / Compacto / Com footer fixo / Sem footer

**Tamanhos:** Pequeno / Médio / Grande / Full

**Estados:** Aberto / Fechado / Carregando / Erro / Vazio

**Comportamento:**
- Abre sobre interface sem navegação de página
- Pode ser fechado por: botão fechar, clique no overlay, tecla Escape
- Foco do teclado preso dentro do Drawer enquanto aberto
- Scroll da página principal bloqueado

**Regras:**
- Apenas um Drawer ativo por vez
- **Pode disparar um Modal/Dialog** por cima (única sobreposição aceita — ex: formulário no Drawer → confirmação); nunca outro Drawer nem um Popover
- Fechamento não deve perder dados sem aviso (quando há formulário)
- Não substituir navegação principal

---

### Modal

**Descrição**
Bloqueia a interface para focar o usuário em uma tarefa específica.

**Anatomia:** Overlay + Container + Título + Conteúdo + Ações + Fechar

**Quando usar:** fluxos importantes que exigem atenção total, formulários complexos, confirmações críticas.
**Não usar:** ações simples de confirmação (→ Dialog), feedback leve (→ Toast), conteúdo que cabe num Drawer.

**Variações:** Simples / Formulário / Fullscreen

**Tamanhos:** Small / Medium / Large / Fullscreen

**Regras:**
- Deve ter ação clara e fechar explícito
- **Nunca Modal sobre Modal** — sempre switch (ver "um overlay por vez" no topo de Overlay/Surface). Confirmação dentro do Modal → inline, não Dialog por cima.
- Pode ser disparado por um Drawer; nunca abre um Drawer por cima de si.
- Conteúdo longo demais → considerar Drawer ou página

---

### Dialog

**Descrição**
Componente para **decisões rápidas e confirmações** — versão mínima de Modal.

**Anatomia:** Título + Mensagem + Ações (geralmente Confirmar + Cancelar)

**Quando usar:** confirmar ação, alertar sobre decisão, ação destrutiva que precisa de confirmação.
**Não usar:** fluxos complexos (→ Modal), informação sem ação necessária (→ Alert).

**Variações:** Confirmar/Cancelar / Destrutivo (Danger)

**Tamanho:** Pequeno (fixo)

**Regras:** linguagem objetiva, ação principal clara, ações destrutivas em Danger.

---

### Popover

**Descrição**
Conteúdo contextual com interação, exibido próximo ao elemento de origem.

**Anatomia:** Container + Conteúdo + Ações (opcional)

**Quando usar:** ações rápidas contextuais, informações interativas que precisam de espaço, mini formulários.
**Não usar:** conteúdo complexo que precisa de mais espaço (→ Modal ou Drawer).

**Comportamento:** Abre próximo ao elemento, fecha ao clicar fora ou pressionar Escape.

**Regras:**
- Não deve bloquear fluxo principal.
- **Nunca abre Modal nem Drawer por cima** — se a ação precisa de um overlay pesado, faça switch (fecha o Popover e abre o overlay no lugar).

---

### Tooltip

**Descrição**
Exibe informação complementar ao interagir com um elemento (hover ou focus).

**Anatomia:** Container + Texto curto

**Quando usar:** explicar ícones sem label, dar contexto rápido sobre elemento, complementar informação densa.
**Não usar:** informação essencial para a tarefa (não pode depender de hover), conteúdo longo.

**Posições:** Top / Bottom / Left / Right

**Comportamento:** aparece no hover/focus, some automaticamente. Texto máximo: 1–2 linhas.

**Regra:** não depender apenas de hover — garantir acessibilidade via focus também.
