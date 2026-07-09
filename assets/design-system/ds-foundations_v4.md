# DS Foundations v4 — Stack shadcn/ui

> **O que é este arquivo**
> Define os elementos fundamentais que sustentam todas as interfaces — cores, tipografia, espaçamento, ícones, grid, motion, border radius, sombras e princípios de UX.
> São as regras de base. Nenhum componente ou pattern existe fora dessas definições.
> Idêntico ao `ds-foundations.md` original, exceto a seção 5 (Ícones), atualizada para a stack shadcn/ui.
>
> **Hierarquia dos documentos**
> `ds-foundations_v4.md` (este) → base visual e princípios, agnóstico de produto
> `ds-components_v4.md` → specs de comportamento de componente + mapeamento shadcn/ui
> `ds-patterns.md` → estruturas de tela reutilizáveis
> `uikit-[projeto].html` → tokens reais de cor e componentes implementados (prevalece sobre este arquivo para valores visuais)
> `Engineering-directives_v4.md` → como essas regras viram código na stack shadcn/ui

---

## 1. Cores

### O que é
Sistema de tokens visuais que comunicam identidade, hierarquia, estados e feedback. Cores nunca devem ser usadas de forma arbitrária — sempre por papel semântico.

### Papéis semânticos
- **Primary** → ações principais e destaque
- **Neutral** → textos, backgrounds, bordas
- **Feedback / Success** → confirmações e estados positivos
- **Feedback / Error** → erros e estados destrutivos
- **Feedback / Warning** → alertas e atenção necessária
- **Feedback / Info** → informações complementares
- **Disabled** → papel próprio, não é "a cor original com opacidade reduzida". Testado e aprovado: fundo `gray-100` / texto e ícone `gray-400` (escala Tailwind), sempre igual independente da variante do componente (um botão Primary desabilitado fica com a mesma aparência que um Danger desabilitado)

### Regras de uso
- Usar cores por papel semântico, não por aparência ("quero essa cor porque é bonita" não é critério)
- Sempre usar tokens (`var(--token)`), nunca valores hexadecimais hardcoded
- Garantir contraste mínimo WCAG AA entre texto e fundo
- Não usar cor como único indicador de estado — sempre combinar com texto ou ícone
- Limitar número de cores competindo na mesma tela
- **Disabled nunca é "reduzir a opacidade da cor original"** — trocar para o papel Disabled (`gray-100`/`gray-400`) explicitamente

### Hierarquia visual por cor
- Alta ênfase → cores mais fortes (primary)
- Média ênfase → neutros mais escuros
- Baixa ênfase → neutros claros

> **Tokens reais de cor vivem no `uikit-[projeto].html`.** Este arquivo define os papéis; o UIKit define os valores.

---

## 2. Tipografia

### O que é
Sistema de estilos de texto que define hierarquia visual, legibilidade e consistência entre produtos. Baseado na fonte **Inter**.

### Escala tipográfica

| Estilo | Tamanho | Peso | Uso |
|---|---|---|---|
| Display | 32–40px | 700 | Títulos de página principais, hero |
| H1 | 24–28px | 700 | Cabeçalhos primários de seção |
| H2 | 20–22px | 600 | Cabeçalhos secundários |
| H3 | 16–18px | 600 | Subtítulos de bloco |
| Body Large | 16px | 400 | Leitura principal |
| Body | 14px | 400 | Texto padrão do sistema |
| Body Small | 12px | 400 | Metadados, labels secundários |
| Caption | 11–12px | 400–500 | Legenda, eyebrow |

### Regras de uso
- Nunca usar `text-transform: uppercase` — usar `font-weight` e `letter-spacing` para hierarquia
- Nunca pular níveis de hierarquia (H1 → H4 sem H2 e H3)
- Manter line-height adequado para legibilidade (mínimo 1.4 para body)
- Limitar variações de peso na mesma tela (máx. 2–3 pesos distintos)
- Em labels e eyebrows: title case (primeira letra de cada palavra em maiúscula), nunca caixa alta completa

### Hierarquia progressiva
Precisa aumentar destaque? → Aumente peso antes de aumentar tamanho. Use cor com moderação.
Precisa reduzir destaque? → Use tons neutros mais suaves. Prefira Caption para informações secundárias.

---

## 3. Espaçamento

### O que é
Escala baseada em múltiplos de 8px que define distâncias entre elementos. Responsável por ritmo visual, organização e hierarquia.

### Escala
| Valor | Uso |
|---|---|
| 4px | Mínimo — detalhes internos, ajustes finos, ícone + texto |
| 8px | Pequeno — itens diretamente relacionados |
| 16px | Padrão — elementos dentro da mesma seção |
| 24px | Separação de blocos distintos |
| 32px | Seções principais |
| 48px+ | Separações de áreas grandes |

### Regras de uso
- **Nunca** usar valores fora da escala (3px, 10px, 13px, 27px, etc.)
- Elementos relacionados → espaçamento menor
- Separação de grupos → espaçamento maior
- Em layouts responsivos: manter proporção da escala, não necessariamente os valores absolutos
- Componentes shadcn/ui vêm com espaçamento próprio por padrão — auditar e ajustar pra essa escala antes de considerar o componente pronto (ver `Engineering-directives_v4.md`)

---

## 4. Grid

### O que é
Sistema de colunas, margens e espaçamentos horizontais que define como elementos são posicionados e como o layout se adapta a diferentes dispositivos.

### Breakpoints

**Mobile (390–480px)**
- 4 colunas | Margin: 16px | Gutter: 16px
- Layouts simples e lineares, preferir coluna única

**Tablet (481–1024px)**
- 8 colunas | Margin: 24px | Gutter: 24px
- Distribuição equilibrada, cards em múltiplas colunas

**Desktop Base (1025–1440px)**
- 12 colunas | Margin: 40px | Gutter: 24px
- Quando houver sidebar: fixa em 256px, subtraída da área de conteúdo
- Layouts complexos (dashboards, sistemas) costumam usar sidebar — não é obrigatória

**Widescreen (+1440px)**
- 12 colunas centralizadas | Margin: 280px | Gutter: 24px
- Quando houver sidebar: fixa em 256px
- Conteúdo centralizado para melhor legibilidade

### Regras de uso
- Sempre alinhar componentes às colunas do grid
- Quando houver sidebar, mantê-la fixa em 256px; o conteúdo respeita essa área
- Nunca esticar conteúdo até as bordas em widescreen
- Não criar alinhamentos manuais fora das colunas

### Navegação (casca definida por projeto)
O tipo de casca de navegação é **escolha de cada projeto**, não uma regra do design system. Opções válidas:
- **Sidebar** fixa (256px no desktop) — comum em sistemas/dashboards com muitas seções
- **Navbar** no topo — comum em produtos com poucas seções
- **Sidebar + navbar** combinadas
- **Nenhuma das duas** — conteúdo em tela cheia

No mobile, a navegação normalmente colapsa em **menu hambúrguer** ou **navegação inferior (bottom nav)** — o bottom nav aparece mais em apps do que em sites de fato responsivos.

---

## 5. Ícones

### O que é
Biblioteca **Lucide** como padrão único para todos os produtos. Três tamanhos oficiais. Lucide é a biblioteca de ícones do ecossistema shadcn/ui — cada ícone é um componente SVG com dimensão própria via prop `size`, sem o problema de espaço fantasma que ícones baseados em glifo de fonte têm.

### Escala

| Tamanho | Uso |
|---|---|
| **16px (Small)** | Elementos densos: tabelas, chips, metadados, ações secundárias |
| **20px (Medium)** | Uso padrão: botões, inputs, menus, listas |
| **24px (Large)** | Destaque: navegação principal, headers, empty states |

### Regras de uso
- Sempre usar Lucide (`lucide-react`) — nunca ícone inline customizado fora da biblioteca, nunca emoji
- Respeitar a escala (16 / 20 / 24px via prop `size`) — nunca tamanhos arbitrários
- Manter alinhamento óptico com textos adjacentes
- Usar o mesmo ícone para a mesma ação em todo o sistema (ex: delete é sempre `Trash2`)
- Ícones são suporte à informação, não substituto completo de texto em contextos críticos

---

## 6. Border Radius

### Escala

| Valor | Uso |
|---|---|
| **0px** | Sem arredondamento — elementos rígidos, tabelas |
| **4px** | Leve — pequenos elementos |
| **8px** | Padrão — botões, cards simples, inputs |
| **12px** | Intermediário — cards destacados, containers |
| **16px** | Alto — modais, elementos de destaque |
| **999px / full** | Total — chips, avatars, badges |

### Regras de uso
- Sempre usar valores da escala — nunca 3px, 7px, 10px ou valores arbitrários
- Manter consistência entre estados (hover, active, disabled seguem o mesmo radius do default)
- Radius menor para elementos estruturais; maior para elementos de ação ou destaque
- Usar full radius apenas quando faz sentido semântico (pills, chips)
- Na stack shadcn/ui: definir uma única variável `--radius` no `:root` e derivar os demais valores por `calc()`, não declarar radius solto por componente

---

## 7. Sombras

### Escala semântica

| Token | Uso |
|---|---|
| `--sh-flat` | Elementos discretos, sem elevação visível |
| `--sh-card` | Cards padrão, leve separação do fundo |
| `--sh-priority` | Cards em destaque, elevação moderada |
| `--sh-modal` | Modais e drawers, máxima elevação |

### Regras de uso
- Sombra comunica hierarquia e elevação — usar de forma consistente
- Não usar gradientes decorativos — gradientes apenas para encoding de dado físico/contínuo
- Valores reais vivem no `uikit-[projeto].html`

---

## 8. Motion

### O que é
Animações e transições que indicam mudanças de estado, orientam o usuário e criam continuidade na experiência.

### Timings padrão

| Tipo | Duração |
|---|---|
| Micro interações (hover, focus) | 100–150ms |
| Transições padrão (dropdown, tooltip) | 150–250ms |
| Componentes maiores (modal, drawer) | 250–400ms |
| Entradas/saídas de bloco grande | 300–500ms |

### Princípios
- **Rapidez** — animações não devem atrasar interação
- **Suavidade** — sem saltos bruscos, usar easing natural (evitar linear puro)
- **Consistência** — mesma interação = mesmo padrão de animação
- **Intenção** — toda animação tem motivo funcional, não decorativo

### Regras de implementação
- Apenas `transform` e `opacity` via `@keyframes`
- Sempre incluir `prefers-reduced-motion` — a interface deve funcionar sem animações
- Não empilhar múltiplas animações simultâneas na mesma tela
- Componentes shadcn/ui com animação (Dialog, Accordion, etc.) já seguem isso via Radix + `tailwindcss-animate`

---

## 9. Acessibilidade

### Princípio base
Acessibilidade não é camada adicional — é aplicada em todos os componentes e interfaces desde o início.

### Contraste
- Garantir contraste suficiente entre texto e fundo (referência WCAG AA)
- Manter contraste adequado em todos os estados (hover, disabled, focus)
- Nunca reduzir contraste por razões estéticas

### Navegação por teclado
- Toda interação deve ser possível via teclado
- Elementos interativos devem ter estado de foco visível (`box-shadow: 0 0 0 3px rgba(...)` — ver Engineering Directives)
- Ordem de navegação deve seguir hierarquia visual da interface

### Semântica e estrutura
- Usar elementos HTML semânticos corretos
- Hierarquia clara de títulos sem pular níveis
- Não depender apenas de cor para transmitir informação

### Feedback e estados
- Sempre fornecer feedback claro para ações do usuário
- Estados de sucesso, erro e loading devem ser perceptíveis visual e semanticamente
- Mensagens de erro devem explicar o problema e como resolver

---

## 10. Princípios de UX

Usados como critério de decisão quando não existe regra explícita de componente ou padrão.

### Os 7 princípios

**1. Clareza acima de tudo**
A interface deve ser fácil de entender sem necessidade de explicação.
Priorizar textos claros, evitar ambiguidade em ações e informações, tornar evidente o que o usuário pode ou deve fazer.

**2. Hierarquia guia a atenção**
A informação mais importante deve ser percebida primeiro.
Usar tamanho, espaçamento e contraste para hierarquia. Destacar ações principais de forma consistente. Evitar que elementos compitam visualmente.

**3. Consistência reduz esforço cognitivo**
Elementos iguais devem se comportar e parecer iguais em todo o sistema.
Manter padrões de componentes. Reutilizar soluções existentes. Evitar variações desnecessárias.

**4. Eficiência na jornada**
O usuário deve concluir tarefas com o menor esforço possível.
Reduzir etapas desnecessárias. Evitar redundância. Priorizar fluxos diretos e previsíveis.

**5. Feedback é essencial**
Toda ação do usuário deve ter resposta clara da interface.
Comunicar sempre o resultado das ações. Tornar visíveis os estados de sucesso, erro e loading. Evitar ações "silenciosas".

**6. Previsibilidade cria confiança**
A interface deve se comportar de forma consistente e esperada.
Padrões devem se repetir em contextos similares. Evitar mudanças inesperadas de comportamento. Manter lógica consistente entre fluxos.

**7. Simplicidade não é ausência de complexidade**
Simplicidade é sobre reduzir o esforço de entendimento, não remover funcionalidades.
Organizar complexidade de forma progressiva. Mostrar informações no momento certo. Evitar sobrecarga visual e cognitiva.

### Como usar
Estes princípios entram na conversa quando há dúvida sobre estrutura de tela, organização de informação, hierarquia de ações, ou comportamento de fluxo — não quando há regra de componente já definida.

---

## 11. Convenções de tokens

### Nomenclatura
Tokens devem representar **função e contexto**, não aparência visual. Esta nomenclatura é a mesma convenção usada pelo shadcn/ui — não é coincidência, facilita a ponte entre este documento e os componentes reais.

```
primary / primary-foreground
secondary / secondary-foreground
muted / muted-foreground
accent / accent-foreground
destructive / destructive-foreground
background / foreground
border / input / ring
```

### Regras
- Nunca usar valor de cor hardcoded — sempre `var(--token)` ou classe mapeada
- Em conflito entre documentos: UIKit prevalece para tokens visuais; DS prevalece para specs de comportamento
