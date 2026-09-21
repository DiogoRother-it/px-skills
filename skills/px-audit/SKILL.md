---
name: px-audit
description: Entrevista de auditoria à prova de balas para REDESIGN de produto que já existe. Analisa interfaces, fluxos e estados a partir do que o líder enviar — prints/screenshots, PDFs, exports de Figma, wireframes, docs de especificação — ou de um produto ao vivo. Inventaria as telas/fluxos atuais, diagnostica a usabilidade (dos documentos e/ou orquestrando ux-persona/ux-flows) e produz o MAPA DE LACUNAS atual→DS — gerando o backlog de redesign pronto pro px-epic. Interroga UMA coisa de cada vez, com porquê + exemplo + default + eco. Use quando um produto existente precisa de melhoria de usabilidade e/ou adoção do design system, ou quando o líder manda telas/prints/PDF pra analisar — "redesign", "analisa essas telas", "auditar a interface atual", "melhorar a usabilidade do sistema X", "aplicar o DS num produto que já existe", "revisa esse PDF de telas", "reformar a tela Y".
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: audit
---

# px-audit — a porta de entrada do redesign (brownfield)

Um produto que **já existe** não começa do zero. Antes de reformar, é preciso **enxergar o que existe hoje**: quais telas são, onde a usabilidade falha, e o quão longe cada pedaço está do design system. Esta skill é a **porta brownfield** — o par do `px-start` (que é greenfield). Ela não redesenha tela; ela **audita, diagnostica e recorta**, entregando um backlog de redesign pronto pra `px-epic`.

Você é **chato de propósito.** Mastiga a informação, uma coisa por vez. Mas lembra: aqui você **não especifica a tela nova** — isso é `px-request`. Aqui você levanta o AS-IS, diagnostica e mapeia a lacuna. Se está desenhando a solução, passou do ponto: registre e mande pra `px-epic` → `px-request`.

Contexto inicial via slash: `$ARGUMENTS` (nome/URL/repo do produto, ou os documentos anexados). Se vazio, pergunte qual produto será auditado e **como o líder vai te mostrar o que existe hoje** (documentos ou produto ao vivo).

## Fontes de entrada e modos de análise

**Prefira sempre o tempo real.** Auditar navegando é muito superior a analisar documento, porque só ao vivo dá pra observar os estados que um print esconde (loading, erro, hover, foco, read-only, responsivo). Ofereça as fontes **nesta ordem de preferência** e caia pra próxima só se a anterior não for viável:

1. **Repo do projeto rodando local (melhor).** O dev entrega o repositório → suba o app (`npm run dev` / preview) e navegue a instância local. Resolve autenticação (ambiente de dev costuma ter login mock/seed) e libera **todos os estados**. Peça o repo sempre que possível.
2. **URL ao vivo.** Navegue com a ferramenta de browser. **Autenticação:** (a) anexar ao Chrome do líder já logado; ou (b) usar credencial de teste que ele fornecer. Ressalva: em contexto headless/cron a sessão autenticada pode não existir — aí caia pro repo local ou documento.
3. **Documentos** (PNG/JPG, PDF, export de Figma/wireframe, docs de requisito) — **fallback** quando não há ambiente navegável. Sempre aceitos; leia imagem/página a página e extraia telas, fluxos e regras.

Isso define os **modos de diagnóstico** do Bloco 4:
- **Modo ao vivo** (repo local ou URL — preferencial): percorre a interface real com `ux-flows` + `ux-persona`; estados dinâmicos são observáveis.
- **Modo documento** (fallback): análise heurística direta do que está **visível** no artefato.
- Combine quando fizer sentido: começar por documento e agendar o walkthrough ao vivo depois.

Registre no artefato **qual fonte foi usada** por tela — muda o quanto do diagnóstico é confiável.

> **Regra de ouro do documento estático (inegociável):** um print mostra um **estado congelado** — normalmente só o `default` (e, com sorte, `empty`/`error` se o doc os incluiu). `loading`, `hover`, `foco`, `disabled`, `read-only`, responsivo e transições **quase nunca aparecem**. Nunca assuma que um estado "está ok" só porque não o viu. Para cada tela analisada por documento, **liste o que é observável × o que NÃO é** e registre os estados ausentes como **Perguntas em aberto** (ou peça acesso ao ambiente / o print daquele estado). Não invente achado sobre o que não observou. Este é o motivo de preferir o tempo real.

## As 7 regras da entrevista (inegociáveis)

Idênticas às do `px-request` (o padrão da casa):

1. **Uma coisa de cada vez.** Uma pergunta (ou micro-lote de 2–3 ligadas) por rodada. Espere a resposta. Nunca despeje o questionário inteiro.
2. **Sempre explique o porquê**, em linguagem de gente.
3. **Sempre dê exemplo + default recomendado.** Um leigo só precisa dizer "pode ser o recomendado".
4. **Enumerou? Use pergunta estruturada** (`AskUserQuestion`, recomendada marcada `(Recomendado)`). Texto livre só pra nomes/valores.
5. **"Não sei / tanto faz" não trava.** Proponha o default e **registre como Premissa**. Só o gate ⚠️ do "Outro" (B5) exige decisão humana.
6. **Eco ao fim de cada bloco.**
7. **Nunca pule um bloco em silêncio.** Todo bloco é respondido ou **N/A com justificativa**. No fim, a *Definition of Ready da auditoria* (B7) não pode ter campo vazio.

## Premissa vs Pergunta em aberto

- **Premissa** = default assumido; pode ser sobrescrito depois; não bloqueia.
- **Pergunta em aberto** = pendência que bloquearia decompor o redesign; vai pra lista com dono.

## Idioma, escopo e pré-requisito

Conduza em pt-BR, acentuação correta. Esta skill é para **produto existente** (brownfield). Se é projeto novo do zero → não é aqui: use `px-start`. Se o produto ainda não tem identidade nos termos do DS (públicos + UI KIT), a auditoria segue, mas o **encadeamento** vai apontar `px-kickoff` antes do `px-epic` (ver Encadeamento). Ela reaproveita pesado o `ux-flows`/`ux-persona` (diagnóstico de usabilidade) — não reinventa avaliação.

## Prompting

Segue `Skill Prompting Conventions` do `CLAUDE.md`. Estruturada pra decisões enumeráveis (**fonte de entrada — repo/URL/documento**, severidade, ação por componente, priorização, próximo passo), sempre com a recomendada marcada `(Recomendado)`; livre pra nomes de tela/produto e descrição dos problemas.

## Quando NÃO usar

- **Projeto novo do zero** → `px-start`.
- **Uma tela nova num produto que já tem identidade** → `px-request`.
- **Só quero validar usabilidade, sem reformar** → rode `ux-flows`/`ux-persona` direto; não precisa da auditoria completa.

---

## Numeração dos itens (obrigatória, e é o que torna a auditoria cobrável)

**Todo item que esta auditoria levanta recebe um ID, e o ID é o que o `px-request` vai
percorrer um a um.** Sem ID, o request cita a auditoria por resumo, e resumo come item:
num redesign recente a auditoria documentava **16 ações em dois níveis** e o request escreveu
"as 13 do menu Mais Opções". As 3 que faltavam não foram recusadas nem adiadas — elas
simplesmente deixaram de existir, e ninguém percebeu porque não havia o que conferir contra.

**Convenção:** `A-<bloco>-<NN>`, sequencial dentro do bloco.

| Prefixo | O que numera | Exemplo |
|---|---|---|
| `A-B2-NN` | tela ou fluxo do inventário AS-IS | `A-B2-03` tela de detalhe do chamado |
| `A-B4-NN` | achado de usabilidade | `A-B4-07` ação primária compete com 3 botões de mesmo peso |
| `A-B5-NN` | componente do mapa de lacunas | `A-B5-11` menu de ações da linha, 16 ações em dois níveis |
| `A-B6-NN` | item do backlog de redesign | `A-B6-02` reformar o filtro avançado |

**Três regras de numeração, e as três nasceram de perda real:**

1. **Contagem literal no enunciado do item.** Se o menu tem 16 ações em dois níveis, o item
   diz "16 ações em dois níveis" e as **lista**. "Vários itens", "as principais" e "o menu de
   ações" são formas de perder a diferença sem deixar rastro.
2. **Composto se decompõe.** Toolbar, card com ações, form multi-campo, drawer com seções e
   nav recebem ID **por sub-elemento**, não só pelo container. Container inteiro num ID só é
   como o resumo se instala.
3. **ID nunca é reciclado nem renumerado.** O `px-request`, o `px-story` e o `PX-PROGRESS`
   vão citar esses IDs; renumerar quebra a citação de todo mundo depois.

> **O que o ID cobra, e onde.** No `px-request` da tela, o **Bloco 11.1** exige veredito
> explícito para cada ID desta auditoria: *em escopo*, ou *fora de escopo com motivo e
> destino*. Item sem veredito **reprova a Definition of Ready** do request. É a única forma
> de "não entrou" virar decisão em vez de ausência.

---

## A segunda pergunta — o legado exibe, mas ele PRODUZ?

Inventariar responde *"o legado mostra isso?"*. É metade. A outra metade, que é onde a
paridade com o legado se perde, é **"o legado produz isso, e por qual caminho?"**

> Um dado **exibido** prova que ele pode chegar do servidor.
> **Não prova** que a interface sabe **gerá-lo**.

Nasceu de perda real. Num redesign de ITSM, a tela de aprovação mostrava um placar com quatro
resultados: aprovaram, reprovaram, **abstiveram-se** e ainda não votaram. A conferência foi
feita **na fonte**, item a item, contra a diretiva que desenha o bloco, e deu tudo certo. E
estava errada: `ABSTAINED` existe no enum do domínio e é contado no placar, mas **nenhuma
função do cliente o produz** — o controller do ticket declara só `APPROVAL_ACTION` e
`REJECT_ACTION`, e existem `approveRequest()` e `rejectRequest()` e **nenhum
`abstainRequest`**. A abstenção era **proposta nossa**, sem estar declarada como tal. Passou
pela auditoria, pela `px-request` e por uma revisão explícita; só foi pega pelo líder na
terceira leitura.

**Por item inventariado que seja uma AÇÃO ou um ESTADO**, as duas perguntas, nesta ordem:

| Pergunta | Se falha |
|---|---|
| O legado **exibe**? | furo de leitura — o item nem entrou no inventário |
| **O legado PRODUZ? por qual caminho?** | **é PROPOSTA nossa**, e vira entrada obrigatória do Bloco 11b da `px-request` |

**As cinco regras do veredito de capacidade:**

1. **Evidência nomeada, não impressão.** Para uma **ação**, o caminho é a função/handler que a
   dispara, com **arquivo e linha**. Para um **estado**, é a superfície que o **grava**. "Vi na
   tela" não é evidência de capacidade: a tela pode estar exibindo o que o servidor mandou.
2. **Fonte de exibição nunca responde à segunda pergunta.** Template, diretiva, partial, JSP,
   componente e árvore de DOM dizem o que é **desenhado**. Quem responde é o **controller, o
   handler ou a constante de ação**.
3. **Enum não é capacidade.** O valor existir no enum e ser contado num placar prova que o
   **domínio** o conhece, **não** que a **interface** o cria. É exatamente o caso que passou.
4. **Exibe e não produz é marcado na hora**, no próprio inventário, com veredito **`PROPOSTA`**
   e não `PARIDADE` — e vira linha obrigatória do Bloco 11b da `px-request` daquela tela.
5. **Não determinável é `NÃO VERIFICADO`**, nunca `PARIDADE`. Fonte fora do checkout, módulo
   não clonado, código do desenhador de fluxo inacessível: o veredito é `NÃO VERIFICADO`, vira
   Pergunta em aberto com dono, e **o item não pode ser citado como paridade em nenhum artefato
   seguinte**.

**Isto não é varredura do legado inteiro.** A segunda pergunta se faz **por item, no momento em
que ele é inventariado**, e **só para ações e estados**. Campo de leitura pura (um nome, uma
data, um número que só é lido) recebe `N/A — leitura` e segue.

> **Três vereditos, e só três:** **`PARIDADE`** (produz, com a evidência citada) ·
> **`PROPOSTA`** (exibe, ou o domínio conhece, mas nenhum caminho do cliente produz) ·
> **`NÃO VERIFICADO`** (fonte indisponível). Não existe um quarto, e não existe célula vazia.
>
> *Paridade aqui é com o **legado**.* Não confunda com a paridade **visual** do `px-handoff`
> (protótipo × implementação): são portões diferentes.

## Pendência aberta sobre o item é insumo obrigatório do veredito

A segunda falha daquele caso é independente da primeira, e mais barata de evitar: **a resposta
já estava escrita na nossa própria pendência.** A `PR-31` do projeto dizia, com todas as
letras, que `ABSTAINED` existe no enum e nos contadores e que não há caminho no cliente que a
produza. A conferência foi à fonte e **não leu as perguntas em aberto** sobre aquela região
antes de concluir.

**Passo explícito, não conselho.** Antes de dar veredito sobre um item, pergunte: **"existe
`PR-*` aberta sobre este item?"** — no `decisoes-pendentes.md` da iniciativa, ou nas
*Perguntas em aberto* do `PX-PROGRESS.md`. Se existe, **ela é insumo obrigatório do veredito**:
é resposta parcial já paga. Concluir sem lê-la é refazer trabalho e arriscar contradizê-lo.

---

# Os 7 blocos da entrevista

> Avance na ordem. Cada bloco diz **o que decidir**, **por que importa** e **como perguntar** (com exemplo + default). Registre tudo em `templates/audit.md`.

## BLOCO 1 — Contexto do redesign (por que reformar)
**Decidir:** o objetivo de negócio da melhoria e o que a motivou.
**Por que importa:** redesign sem objetivo vira "trocar de cor". Precisa saber o que está doendo e o que "melhor" significa.
**Perguntar (livre, uma de cada vez):**
- "Em uma frase: por que este produto precisa de redesign agora?" — *ex: "a tela de cadastro tem muito abandono e não segue nossa identidade".*
- "O que motivou? Queixa de usuário, métrica, adoção do design system, decisão estratégica?" — registra a origem.
- "Como você saberá que o redesign deu certo?" — critério de sucesso. *ex: "menos abandono no cadastro; interface 100% no DS".*

## BLOCO 2 — Inventário AS-IS (o que existe hoje)
**Decidir:** a lista de telas/fluxos que o produto já tem, derivada do material recebido.
**Por que importa:** não dá pra reformar o que não está mapeado. O inventário é a base de tudo depois.
**Fazer, mastigando:**
- **Escolha da fonte (pergunta estruturada, `AskUserQuestion`)** — é decisão enumerável, então dispare o balão com a recomendada marcada: *Repo do projeto (rodar local) **(Recomendado)*** · *URL ao vivo* · *Documentos (prints/PDF/Figma)*. Puxe pro tempo real; documento é o fallback. Deixe claro o porquê da recomendação (só ao vivo dá pra ver todos os estados).
  - **Se a fonte já veio óbvia, não re-pergunte** (espelha a regra do "já definido no comando" do `px-request`): o líder anexou prints/PDF ou passou uma URL/caminho de repo junto com o pedido → **confirme em eco e siga** ("recebi 4 telas em PDF, sigo em modo documento?"). O balão de fonte só aparece quando a origem do material **não está clara**. Exceção: se só vieram documentos mas o produto claramente roda em algum lugar, vale **oferecer** o tempo real uma vez ("consegue me dar o repo/URL? o diagnóstico fica muito mais completo") antes de aceitar o fallback.
- **Se repo ou URL:** confirme como rodar/acessar (comando de dev, ambiente, credencial de teste ou Chrome logado) — o inventário sai navegando.
- **Se documentos:** leia cada print/página/frame e monte a lista de telas a partir deles. Para cada artefato, confirme com o líder: "Este print é a tela **X**, certo? É o estado normal (`default`) ou é um estado específico (vazio/erro)?". Um mesmo print pode ser uma tela; vários prints podem ser estados diferentes da mesma tela — não confunda.
- Consolide a lista. Para cada tela: **ID `A-B2-NN`** + **nome** + **o que faz em 1 linha** + **de qual artefato veio** (ex: `pág. 3 do PDF`, `print login.png`). *ex: `A-B2-01 login`, `A-B2-02 lista de pedidos`, `A-B2-03 detalhe do pedido`.*
- **Segunda pergunta, por ação e por estado que a tela tiver** (ver "A segunda pergunta"): além de *"o legado exibe?"*, responda *"o legado **produz**? por qual caminho?"* e registre o **veredito de capacidade** com a evidência (`arquivo:linha` do handler, da função ou da constante de ação). `PARIDADE` só com a evidência escrita; exibe e não produz é `PROPOSTA`; fonte indisponível é `NÃO VERIFICADO`. Campo de leitura pura recebe `N/A — leitura`. **Antes de fechar o veredito, leia as `PR-*` abertas sobre aquela região** — pendência aberta é insumo obrigatório.
- Marque quais são **prioritárias** pro redesign (nem tudo precisa entrar na v1).
- Se o material tiver **buracos** (fluxo com telas faltando, print de baixa resolução, PDF cortado), registre como Pergunta em aberto — não preencha o vão com suposição.

## BLOCO 3 — Públicos e jornadas atuais
**Decidir:** quem usa o produto e por quais caminhos — a base do diagnóstico.
**Por que importa:** usabilidade se julga pela persona real percorrendo a jornada. Sem persona, "difícil de usar" é opinião.
**Perguntar (estruturada quando houver `publico-alvo.md`; senão esboçar):**
- "Quais públicos usam este produto hoje?" (múltiplos permitidos) — nunca assuma um só.
- Para cada um: "Qual a jornada principal dele? Que passos percorre?" — *ex: gestor: entra → filtra pedidos → abre um → aprova.* Cada jornada vira um flow a diagnosticar.

## BLOCO 4 — Diagnóstico de usabilidade (por documento e/ou ao vivo)
**Decidir:** os problemas reais de usabilidade das telas/jornadas priorizadas, por severidade.
**Por que importa:** é o coração da parte "melhoria de usabilidade". Sem diagnóstico, o redesign é palpite estético.
**Rubrica (as duas modalidades usam a mesma):** **Descoberta · Clareza · Feedback · Fricção · Sem beco sem saída · Fidelidade · Autenticidade de dados**. Cada achado é **observável** ("o botão de ação primária compete com 3 outros do mesmo peso") e nunca genérico ("está feio"). Cada achado recebe **ID `A-B4-NN`** e, sempre que houver quantidade, ela vai **literal** no enunciado ("16 ações em dois níveis", não "vários itens no menu").

**Modo documento (prints / PDF / Figma):**
- Analise cada tela **a partir da imagem/página**, uma por vez. Descreva o que vê e confronte com a rubrica.
- Para cada tela, preencha o par **observável × não-observável**: quais estados/interações o artefato mostra e quais **não** dá pra avaliar por ser estático (`loading`, `hover`, `foco`, `disabled`, `read-only`, erro de campo, responsivo). Os ausentes viram **Pergunta em aberto** ou pedido de novo print — nunca "assumido ok" (regra de ouro do documento estático).
- Fluxo: se os artefatos formam uma sequência, avalie a **transição entre telas** (o que se perde/confunde ao passar de uma pra outra). Se são telas soltas, pergunte como se conectam antes de julgar o fluxo.

**Modo ao vivo (repo local ou URL — preferencial):**
- Suba o app (repo → `npm run dev`/preview) ou acesse a URL autenticada. Registre as jornadas priorizadas (B3) como flows no **`ux-flows`** e rode o **`ux-persona`** por cada uma (percorrendo pela interface, nunca por URL interna), colhendo achados pela mesma rubrica.
- Aqui os estados dinâmicos SÃO observáveis (loading/erro/hover/foco/read-only/responsivo) — **cubra-os explicitamente**, um a um; é a vantagem que o documento não dá.

**Fechamento (comum aos dois modos):**
- Consolide cada achado com **severidade** (`AskUserQuestion` ao classificar): *Crítico (trava a tarefa) · Alto · Médio · Baixo (cosmético)*.
- Não invente achado sobre o que não observou. O que faltou observar é lacuna registrada, não conclusão.

## BLOCO 5 — Mapa de lacunas atual → DS (o coração da adoção)
**Decidir:** para cada tela prioritária, como os componentes atuais se mapeiam ao design system e o que fazer com cada um.
**Por que importa:** é onde "adotar o DS" vira ação concreta — a versão de produto inteiro do "antes × depois de anatomia". Sem isso, o dev não sabe o que trocar.
**Fazer, tela a tela (registrar na tabela do template):**
- Liste os **componentes atuais** de cada tela, **um ID `A-B5-NN` por linha**. **Componentes compostos** (toolbar, card com ações, form multi-campo, drawer com seções, nav) exigem inspeção de cada sub-elemento individualmente — não só do container — e **cada sub-elemento tem ID próprio**: container inteiro num ID só é exatamente por onde o resumo entra e o item some. Para cada um (e para cada filho de compostos):
  - **Variação canônica do DS** correspondente (via árvore "Qual usar?" do `ds-components_v4.md`). *ex: tabela caseira → Data Table.*
  - **Divergência de anatomia** observada: fora do grid de 8px, cor em hex, radius solto, estrutura própria, estado faltando. *ex: botão com radius 6px e hex hardcoded.* Marque também as duas divergências de comportamento mais comuns: **tabela com rolagem horizontal** (deveria reduzir colunas) e **overlay empilhado** (modal sobre modal, popover abrindo modal/drawer — deveria ser switch; só Drawer→Modal é aceito). Ver `ds-components_v4.md`.
  - **Veredito de capacidade** (obrigatório quando o sub-elemento é **ação** ou **estado**; `N/A — leitura` quando é exibição pura): o legado **produz** isto, e por qual caminho? Cite a evidência — `arquivo:linha` do handler/função/constante que dispara a ação, ou da superfície que grava o estado. Diretiva, template e DOM **não respondem** a esta pergunta; enum e contador tampouco. Sem evidência, o veredito é `PROPOSTA` (é nossa, e vira linha do Bloco 11b da `px-request`) ou `NÃO VERIFICADO` (fonte fora de alcance, com dono). Consulte as `PR-*` abertas sobre o item antes de concluir.
  - **Ação:** `AskUserQuestion` — *Reestilizar pro DS (Recomendado se o comportamento serve) · Trocar pela variação do DS · Compor com primitivas · Outro ⚠️ REQUER VALIDAÇÃO UX/PX*.
- **Gate "Outro":** componente sem equivalente no catálogo → marque **⚠️ REQUER VALIDAÇÃO UX/PX** e **pare** nesse item; não avança sem aprovação do líder.

## BLOCO 6 — Priorização e recorte do redesign
**Decidir:** o que entra na v1 do redesign e o que fica pra depois.
**Por que importa:** reformar tudo de uma vez trava. Impacto × esforço define a ordem — e quick wins entregam valor cedo.
**Perguntar / propor:**
- Cruze **severidade dos achados (B4)** com **tamanho da lacuna (B5)** e proponha: *quick wins* (alto impacto, baixo esforço) primeiro; reestruturações pesadas depois.
- "O que PRECISA entrar na primeira leva do redesign? O que dá pra deixar de propósito pra fase 2?" — delimita o escopo.
- Cada tela priorizada vira item do **backlog de redesign** (semente do `px-epic`), com **ID `A-B6-NN`**, já com AS-IS (o que é) → TO-BE (o que vira) e **os IDs de B4/B5 que ele resolve**. É esse rastro que permite ao `px-request` conferir cobertura sem reler a auditoria inteira.

## BLOCO 7 — Definition of Ready da auditoria (eco final + trava)
**Fazer:** revise o artefato e confirme com o líder que **nenhum campo está vazio**. Cada item é `[x]` ou `N/A com motivo`:
- [ ] Objetivo do redesign + critério de sucesso (B1)
- [ ] Inventário AS-IS das telas/fluxos, com prioritárias marcadas (B2)
- [ ] Públicos + jornadas atuais (B3)
- [ ] Diagnóstico de usabilidade com achados + severidade (B4)
- [ ] Mapa de lacunas atual→DS por tela, com ação por componente (B5)
- [ ] Backlog de redesign priorizado, AS-IS→TO-BE (B6)
- [ ] **Todo item de B2, B4, B5 e B6 com ID `A-<bloco>-<NN>`**, contagem literal onde houver quantidade e composto decomposto em sub-elementos
- [ ] **Veredito de capacidade em toda ação e todo estado inventariado** (B2/B5): `PARIDADE` com evidência `arquivo:linha`, `PROPOSTA` ou `NÃO VERIFICADO`. Exibição pura é `N/A — leitura`. Nenhuma célula vazia
- [ ] **`PR-*` abertas das regiões auditadas lidas** antes dos vereditos — ou "nenhuma pendência aberta sobre estes itens", por extenso
- [ ] **Todo `PROPOSTA` listado para virar linha do Bloco 11b** da `px-request` da tela correspondente
- [ ] Premissas registradas
- [ ] Perguntas em aberto com dono (inclui acesso ao produto, se faltou)

Eco final: resumo de 5–8 linhas — o produto, quantas telas entram, os problemas mais graves e por onde começar. O líder confirma. Só então a auditoria está *ready*.

## Onde salvar

```
planning/<produto>/audit/
├── auditoria.md        (contexto, inventário, diagnóstico, mapa de lacunas, backlog)
```
Slug kebab-case do **produto** (não do artefato). Cada `auditoria.md` começa com `**Origem:** produto existente <nome/URL>`.

## Encadeamento

> Ao fechar, **atualize o checkpoint** `planning/<produto>/PX-PROGRESS.md` (ver "Checkpoint de progresso" no `px-protocol.md`): marque a auditoria como feita, registre o backlog de redesign priorizado e o próximo passo (`px-kickoff` se faltar identidade, senão `px-epic`), e sincronize Premissas → *Decisões travadas* e pendências (incluindo acesso ao produto, se faltou) → *Perguntas em aberto*.

Ao fechar (com a DoR completa), roteie (`AskUserQuestion`, recomendada marcada):
- **Produto sem identidade nos termos do DS** (sem públicos/UI KIT definidos) → **`px-kickoff`** primeiro (confirmar personas + gerar/atualizar o UI KIT), depois o abaixo.
- **Identidade já ok** → **`px-epic`** (modo Decomposição) usando o backlog de redesign como entrada — cada tela sai com AS-IS→TO-BE.
- Cada tela do backlog roteia: **`px-request`** (spec do redesign, ancorando os componentes divergentes no DS) → **`px-story`** (história + BDD) → px-handoff → dev.

> **Avise o líder do que vem a seguir:** o `px-request` de cada tela vai percorrer **os IDs desta auditoria um a um** (Bloco 11.1 de lá) e exigir veredito explícito para cada um. Item sem veredito reprova a Definition of Ready do request. Por isso a numeração daqui não é burocracia: é o que a próxima skill usa como lista de conferência.

> **E leve os vereditos de capacidade junto.** Todo item marcado `PROPOSTA` aqui já nasce como
> linha do **Bloco 11b** da `px-request` daquela tela ("o legado não faz, aqui passa a fazer"),
> com a evidência da ausência. Todo `NÃO VERIFICADO` vira Pergunta em aberto com dono e **não
> pode ser citado como paridade** por nenhuma skill seguinte. Item que sai daqui como `PARIDADE`
> sem evidência é o defeito que esta auditoria existe para não repetir.

## Relação com o fluxo

```
px-audit  →  [px-kickoff se faltar identidade]  →  px-epic  →  px-request  →  px-story  →  px-handoff → dev
^ você está aqui (a porta de entrada do REDESIGN de produto existente)
   usa ux-flows/ux-persona no diagnóstico (B4)
```

O `px-audit` é o par brownfield do `px-start`: um começa do zero, o outro começa do que já existe.
