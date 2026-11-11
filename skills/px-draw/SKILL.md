---
name: px-draw
description: Exploração visual antes da spec, em dois formatos à escolha do UX. HTML único para testar uma ideia a fundo (vista do problema, vista da proposta e painel de testes), ou canvas de propostas no Artifacts (tipo Design), com linhas de comparação lado a lado, telas numeradas que funcionam de verdade (PLAY), post-its e comentários, como um quadro do Figma. Visual neutro no discovery inicial; design system do projeto (`@cit` ou `boilerplate-cit`) quando ele já está definido. Ao fechar, descarta e vai para px-start, ou vira referência para px-request. Use quando quiser explorar ou comparar ideias visualmente antes de especificar: "rascunhar uma ideia", "explorar visualmente", "ver como ficaria", "montar variações", "comparar propostas", "montar um canvas", "levar opções pra reunião", "discovery ainda muito vago".
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: draw
---

# px-draw: explorar e comparar ideias visualmente

Esta skill produz **exploração visual de baixo custo** antes da spec. Não é entrega: é ferramenta de raciocínio e de conversa com o time. Não toca no código do produto, não gera componentes React do sandbox e não substitui a `px-request`.

Ela tem **dois formatos**, e o UX escolhe no Passo 0:

| Formato | Para quê | Parece com |
|---|---|---|
| **HTML único** | Testar **uma** ideia a fundo: validar um comportamento, simular situações, mostrar o problema e a proposta | Uma página com a interface funcionando e um painel de testes |
| **Canvas de propostas** | **Comparar** caminhos e fluxos lado a lado e levar para reunião | Um quadro do Figma: linhas de telas, post-its, comentários |

**Os dois são interativos.** Isso precisa ficar claro para o UX: no canvas, cada tela tem **PLAY** e funciona de verdade (clique, estados, campos), não é imagem estática.

**Público:** o líder UX/PX.

**Quando NÃO usar:** o problema já está definido e só existe um caminho → vá direto para `px-request`. O `px-draw` é exploração, não padrão de trabalho.

Contexto inicial via slash: `$ARGUMENTS` (ideia ou conceito a explorar). Se vazio, pergunte o que a pessoa quer visualizar.

## Princípios

- **Fora do produto.** Nada vai para `src/`, nada toca o `index.css` do sandbox, nada importa do projeto React.
- **Descartável por design.** Não precisa ser perfeito; precisa responder a pergunta.
- **Sem dado inventado.** Nada de lorem ipsum nem número fictício que pareça real. O que faltar vira placeholder explícito (`[valor da nota]`).
- **Justificativa fora da tela.** Hipótese, prós e contras vão no post-it (canvas) ou na vista do problema (HTML), nunca dentro da interface simulada.

## Passo 0: qual formato?

Pergunte (`AskUserQuestion`), explicando o porquê de cada um:

- **HTML único: testar uma ideia (Recomendado quando há uma proposta só).** "Uma página com a interface funcionando e um painel para simular situações, por exemplo 24 abas abertas numa janela de 1024 px. Bom para validar comportamento."
- **Canvas de propostas: comparar caminhos (Recomendado quando há 2 ou mais caminhos, ou quando vai para reunião).** "Um quadro como o do Figma, com linhas de telas lado a lado. Cada tela tem PLAY e funciona de verdade; você e o time podem comentar e mexer no quadro."

**O canvas só existe onde a ferramenta de Artifacts está disponível** (app do Claude, claude.ai). Se a sessão não tiver a ferramenta `Artifact`, diga isso numa linha e siga com o HTML único. Nunca simule um canvas dentro de um HTML.

## Passo 1: entender o que explorar

Pergunte (ou infira de `$ARGUMENTS`), uma coisa de cada vez:
- **O quê:** qual ideia, fluxo ou tela?
- **Por quê:** que decisão essa exploração vai destravar?
- **Hoje existe?** Se o produto já tem essa tela, a versão de hoje entra na comparação (linha "Hoje" no canvas, "Comparar com hoje" no HTML). Peça prints, se houver.
- **Só no canvas: quais perguntas de design?** Cada pergunta vira uma linha do quadro. Ex.: "Ao clicar em Emitir, o que a venda mostra?", "Popups: como fica o de confirmação?". Para cada linha, pergunte se é **fluxo** (telas em sequência) ou **variações** (A, B, C da mesma tela).

### Visual: neutro ou design system?

Decida pelo estado do projeto, sem perguntar se a resposta for óbvia:
- **Projeto com design system definido** (sandbox com `docs/design-system/ORIGEM.md`, ou `ds` no `PX-PROGRESS`) → use o DS do projeto (`@cit` ou `boilerplate-cit`): tokens de cor, tipografia, raio e anatomia dos componentes descritos em `docs/design-system/`. A proposta fica comparável com o produto real.
- **Discovery inicial, sem DS nem identidade** → visual neutro: cinzas (`#f5f5f5`, `#e0e0e0`, `#666`, `#1a1a1a`) e um acento placeholder (`#3b82f6`). Identidade vem no `px-kickoff`.

Eco antes de produzir: *"Vou montar [HTML único | canvas] de [X], [N telas / linhas], visual [neutro | `@cit` | `boilerplate-cit`], [com | sem] comparação com hoje. Confirma?"*

## Passo 2A: HTML único

Um arquivo `.html` autocontido, sem dependências externas, salvo em `planning/<iniciativa>/draw/<nome>.html` (ou na pasta que o UX indicar). Se a sessão tiver a ferramenta `Artifact`, ofereça publicar como página para compartilhar.

**Estrutura (o modelo de referência é a página "Abas internas fluidas"):**
1. **Cabeçalho** com o nome da ideia e um seletor entre as vistas.
2. **Vista "Problema"**: contexto em 2 a 3 frases, print atual anotado com marcadores numerados (se houver) e os pontos que quebram, um cartão por ponto.
3. **Vista "Proposta"**: a interface simulada funcionando de verdade, numa janela no tamanho real e escalada para caber na tela.
4. **Painel de testes**, visualmente separado da interface (borda tracejada, título "Painel de testes", nota "Fica fora da interface. Serve só para simular situações."). Controles típicos: quantidade de itens, largura da janela (1024, 1366, 1920 px), ações que forçam estados (erro, vazio, não salvo) e o interruptor **"Comparar com hoje"**.
5. Opcional: "Caminhos para discutir", com as alternativas descartadas ou em aberto.

**Regras:**
- Cores como variáveis CSS no `:root`; espaçamento em múltiplos de 8 px; layout com flex ou grid.
- Ícones em SVG inline de traço simples; nunca emoji, nunca biblioteca externa.
- JavaScript só para a interação simulada e o painel de testes.
- Acessível como desenhado: `<button>`, `<a href>` e `<input>` com `<label>` de verdade, foco visível, `aria-label` em botão só de ícone.

## Passo 2B: canvas de propostas

Crie um Artifact a partir do tipo **Design** (canvas) e siga as instruções que o tipo devolve ao ser criado. Elas mandam no formato dos arquivos; esta seção diz **o que** montar.

**Organização do quadro (o modelo de referência é o canvas "Propostas UX · próxima reunião"):**
- **Uma linha por pergunta de design**, com um título (nota `title1`) que diz o que está sendo decidido. Ex.: *"Emissão 1 · Ao clicar em Emitir: o que a venda mostra, de uma nota a várias"*.
- **Fluxo:** telas numeradas na ordem do uso (`1 · Nova venda`, `2 · Revisar e emitir`, `3 · …`). Bifurcação vira letra: `4a · Aguardando`, `4b · Rejeitada`.
- **Variações:** `A · …`, `B · …`, `C · …`, da mesma tela, lado a lado.
- **Comparação em linhas:** quando há o "hoje", ele vem **em cima**, a proposta no meio e uma variante (modo escuro, outra densidade) embaixo, alinhadas coluna a coluna. Prefixe o nome: `Hoje · Confirmar exclusão`, `Proposta · Confirmar exclusão`.
- **Post-its ao lado das telas:** hipótese da linha, o que muda em relação a hoje, achados e o que falta decidir. Amarelo para hipótese e decisão em aberto; verde para achado.
- **Páginas** para separar temas grandes (ex.: "Propostas", "Hoje"), quando o quadro passar de umas 4 linhas.
- **Todas as telas interativas** (`is_interactive`): botões, campos e estados funcionam pelo PLAY. Quando uma tela leva a outra do mesmo fluxo, ligue as duas.
- Tamanhos: tela de sistema web em 1280 a 1440 px de largura; celular em 390×844.

**Ao entregar o link, diga ao UX, com estas palavras ou parecidas:** *"Cada tela tem PLAY: abre a tela funcionando para clicar e testar. Dá para comentar direto no quadro e mover as telas. Compartilhe o link com o time antes da reunião."*

**Revisões:** quando o UX pedir ajuste, mexa só nas telas citadas. O quadro pode ter sido editado à mão no meio do caminho; o que está publicado é a versão atual.

## Regras de copy (os dois formatos)

- **TRAVESSÃO:** proibido `—` (em dash) e `–` (en dash) em qualquer texto de interface visível. Usar ponto, vírgula, ponto e vírgula ou reescrever. Nos títulos de linha e nomes de tela do canvas, o separador é `·`.
- **CAIXA ALTA:** proibida caixa alta total em labels e títulos. Sem `text-transform: uppercase`.
- Texto em português do Brasil, no tom do produto.

## Passo 3: decidir o destino

Ao fechar, apresente as saídas:

| Decisão | Quando | Próximo passo |
|---|---|---|
| **Descartar** | A exploração clareou o problema, mas não serve de referência visual | `px-start` (projeto novo) ou volta para quem pediu |
| **Usar como referência** | Uma proposta foi escolhida | `px-request` para especificar a tela real |

No canvas, peça ao UX que diga **qual variação venceu em cada linha** (ou que ficou em aberto) e registre isso.

Se houver `planning/<iniciativa>/PX-PROGRESS.md`, atualize com: formato, link do canvas ou caminho do HTML, decisão por linha e próximo passo.

## Eco final

**Verificação antes de fechar:** releia todo texto visível. Algum `—`, `–` ou CAIXA ALTA TOTAL? Algum dado inventado com cara de real? Corrija antes de fechar.

*"[HTML | Canvas] de [X] pronto: [N telas / linhas], visual [neutro | DS]. Copy revisada. Decisão: [descartar | referência, variação escolhida por linha]. Próximo passo: [`px-start` | `px-request`]. Confirma?"*

## Relação com o fluxo

```
ideia ou caminhos em aberto  →  px-draw
                                  ├─ HTML único (testar uma ideia)
                                  └─ canvas de propostas (comparar caminhos)
                                            │
                          ┌─────────────────┴─────────────────┐
                          ▼                                   ▼
                     descartou                         virou referência
                          │                                   │
                      px-start                           px-request
```

> `px-draw` vive **fora** da cadeia PX padrão: é uma válvula de exploração. O fluxo normal começa no `px-start`.
