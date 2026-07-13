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
- Consolide a lista. Para cada tela: **nome** + **o que faz em 1 linha** + **de qual artefato veio** (ex: `pág. 3 do PDF`, `print login.png`). *ex: `login`, `lista de pedidos`, `detalhe do pedido`.*
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
**Rubrica (as duas modalidades usam a mesma):** **Descoberta · Clareza · Feedback · Fricção · Sem beco sem saída · Fidelidade · Autenticidade de dados**. Cada achado é **observável** ("o botão de ação primária compete com 3 outros do mesmo peso") e nunca genérico ("está feio").

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
- Liste os **componentes atuais** de cada tela. Para cada um:
  - **Variação canônica do DS** correspondente (via árvore "Qual usar?" do `ds-components_v4.md`). *ex: tabela caseira → Data Table.*
  - **Divergência de anatomia** observada: fora do grid de 8px, cor em hex, radius solto, estrutura própria, estado faltando. *ex: botão com radius 6px e hex hardcoded.*
  - **Ação:** `AskUserQuestion` — *Reestilizar pro DS (Recomendado se o comportamento serve) · Trocar pela variação do DS · Compor com primitivas · Outro ⚠️ REQUER VALIDAÇÃO UX/PX*.
- **Gate "Outro":** componente sem equivalente no catálogo → marque **⚠️ REQUER VALIDAÇÃO UX/PX** e **pare** nesse item; não avança sem aprovação do líder.

## BLOCO 6 — Priorização e recorte do redesign
**Decidir:** o que entra na v1 do redesign e o que fica pra depois.
**Por que importa:** reformar tudo de uma vez trava. Impacto × esforço define a ordem — e quick wins entregam valor cedo.
**Perguntar / propor:**
- Cruze **severidade dos achados (B4)** com **tamanho da lacuna (B5)** e proponha: *quick wins* (alto impacto, baixo esforço) primeiro; reestruturações pesadas depois.
- "O que PRECISA entrar na primeira leva do redesign? O que dá pra deixar de propósito pra fase 2?" — delimita o escopo.
- Cada tela priorizada vira item do **backlog de redesign** (semente do `px-epic`), já com AS-IS (o que é) → TO-BE (o que vira).

## BLOCO 7 — Definition of Ready da auditoria (eco final + trava)
**Fazer:** revise o artefato e confirme com o líder que **nenhum campo está vazio**. Cada item é `[x]` ou `N/A com motivo`:
- [ ] Objetivo do redesign + critério de sucesso (B1)
- [ ] Inventário AS-IS das telas/fluxos, com prioritárias marcadas (B2)
- [ ] Públicos + jornadas atuais (B3)
- [ ] Diagnóstico de usabilidade com achados + severidade (B4)
- [ ] Mapa de lacunas atual→DS por tela, com ação por componente (B5)
- [ ] Backlog de redesign priorizado, AS-IS→TO-BE (B6)
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
- Cada tela do backlog roteia: **`px-request`** (spec do redesign, ancorando os componentes divergentes no DS) → **`px-story`** (história + BDD) → handoff → dev.

## Relação com o fluxo

```
px-audit  →  [px-kickoff se faltar identidade]  →  px-epic  →  px-request  →  px-story  →  handoff → dev
^ você está aqui (a porta de entrada do REDESIGN de produto existente)
   usa ux-flows/ux-persona no diagnóstico (B4)
```

O `px-audit` é o par brownfield do `px-start`: um começa do zero, o outro começa do que já existe.
