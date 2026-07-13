---
name: px-kickoff
description: Entrevista de setup de identidade à prova de balas para um projeto novo que consome este design system. Roda o Nível Projeto do Protocolo de Interação UX — descobre TODOS os públicos-alvo e GERA o UI KIT (styleguide de identidade) a partir de inputs do líder, uma pergunta de cada vez, com exemplo e default. Feita para que até quem não é UX consiga definir a identidade do projeto sem deixar buraco. Use ao iniciar um projeto novo, definir marca/identidade, ou quando alguém diz "vamos começar o projeto X", "gerar o UI kit", "quem é o público".
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: kickoff
---

# px-kickoff — entrevista de identidade do projeto

Roda **uma vez por projeto**, antes de qualquer tela. É o "Nível Projeto" do Protocolo de Interação UX (ver `CLAUDE.md`). Produz dois artefatos que TODO o resto consome: os **públicos-alvo** e o **UI KIT** de identidade.

A biblioteca de componentes é coringa (universal). O UI KIT é o que **dá rosto** a este projeto. Se ele sair vago, todo projeto fica com cara de rascunho — por isso a entrevista aqui é minuciosa.

Você é **chato de propósito.** Não assume nada sobre marca nem sobre quem usa.

Contexto inicial via slash: `$ARGUMENTS` (nome do projeto, briefing, referências). Se vazio, comece perguntando o nome do projeto e um resumo do que é.

## As 7 regras da entrevista (inegociáveis)

1. **Uma coisa de cada vez** — uma pergunta (ou micro-lote) por rodada; espere a resposta.
2. **Sempre explique o porquê** em linguagem de gente (ex: o que é um "token", por que contraste importa).
3. **Sempre dê exemplo + default recomendado**, marcado — quem responde só precisa dizer "pode ser o recomendado".
4. **Enumerou? Pergunta estruturada** (`AskUserQuestion`, recomendada marcada). Livre só para cores/nomes/valores.
5. **"Não sei / tanto faz" não trava** — proponha o default, **registre como Premissa** e siga. Exceção: a aprovação final do UI KIT sempre exige o líder (mexe em valores visuais reais).
6. **Eco ao fim de cada bloco** — repita o que capturou e confirme.
7. **Nunca pule um bloco em silêncio** — responder ou marcar N/A com motivo. Definition of Ready no fim não tem campo vazio.

## Idioma

Conduza em pt-BR.

## Passo 0 — Bootstrap (onde a skill roda) — obrigatório antes de tudo

**Por que importa:** o kickoff **escreve tokens no `src/index.css`** do produto. Se rodar dentro do boilerplate, rebranda o próprio boilerplate — erro grave.
**Fazer, antes de qualquer pergunta:**
- Confirmar que estamos no **projeto consumidor** (o repo do produto), não no boilerplate coringa.
- Se o projeto ainda não existe, **criar a partir do boilerplate** (scaffold Vite+shadcn) — ou, se o alvo é só um protótipo, seguir pelo `agile-proto` (que tem stack própria e não toca no `index.css`).
- **Nunca** aplicar tokens de identidade de um produto no repositório do boilerplate. Artefatos de planejamento (`planning/<projeto>/`) podem morar junto; tokens reais, só no produto.

## Modo "proponho e valido" (contra o interrogatório)

Ser chato **não** é fazer 15 micro-perguntas. Quando o domínio, um protótipo ou uma marca já dão base, **proponha o bloco preenchido** (ex: o perfil A2–A6 de um público, ou a paleta) e peça **validação** — "isto bate, ou ajusto?". Continua sendo "uma coisa de cada vez": a coisa passa a ser *confirmar um rascunho*, não responder do zero. Só caia em pergunta aberta quando não houver base pra propor.

---

# PARTE A — Público(s)-alvo

> Objetivo: descobrir **quem** usa o produto. Nunca assumir um público só — é comum haver dois ou mais (ex: gestor interno + cidadão final), e eles pedem interfaces diferentes.

## A1 — Quantos públicos existem
**Por que importa:** define quantas lentes o design precisa servir. Perder um público = uma parte dos usuários fica de fora.
**Perguntar:** "Quem vai usar esse produto? Me diga todos os tipos de pessoa — não só o principal." — *ex: "analista de TI que concede acesso" + "colaborador que só consulta o próprio".* Se vier um só, provoque: "tem alguém que só lê? algum administrador? alguém de fora da empresa?"

## A2 → A6 — Para CADA público (repita o bloco inteiro por público)
Faça um de cada vez; não misture os públicos.
- **A2 — Quem é:** papel/cargo/perfil. *ex: "gestor de acessos".*
- **A3 — Contexto de uso:** "onde, quando e em que aparelho ela usa? Sob pressão?" — *ex: desktop, horário comercial, correndo em dia de admissão.* Decide densidade e prioridade mobile/desktop.
- **A4 — Familiaridade:** "o quanto ela entende do assunto? E de sistemas em geral?" (leigo ↔ especialista, nos dois eixos) — decide quanto a interface explica e se cabe atalho de power-user.
- **A5 — Necessidade principal:** "qual a UMA coisa que ela mais precisa resolver aqui?" — vira a prioridade da tela.
- **A6 — Impacto no design:** traduza para regra de UI — *ex: leigo → labels explícitos, menos jargão; power-user → densidade, atalhos.*

## A7 — Conflitos e prioridade
**Por que importa:** quando dois públicos querem coisas opostas (densidade × simplicidade), a UI precisa decidir — senão fica ruim para os dois.
**Perguntar:** "Onde esses públicos querem coisas diferentes? Quem manda em cada tela?" — *ex: gestor age / auditor só lê → mesma tela muda por permissão.*

## A8 — Persona reutilizável (ux-persona)
**Por que importa:** cada público pode virar um persona que o dev usa depois pra validar a usabilidade (`ux-persona`).
**Fazer:** mapear cada público a um persona bundled (`novice`, `rushed`, `skeptical`, `mobile`, `accessibility`, `power-user`) ou marcar "criar próprio em `e2e/personas/`". *default: o mais próximo dos bundled.*

**Eco da Parte A:** liste todos os públicos com uma linha cada e confirme antes de ir pro UI KIT. Salve em `planning/<projeto>/publico-alvo.md`.

---

# PARTE B — UI KIT / Styleguide de identidade

> Objetivo: **gerar** a identidade visual do projeto a partir dos inputs do líder — ele valida, a IA materializa. Explique cada conceito para quem não é designer.

## B1 — Fonte da identidade
**Por que importa:** define se a IA **extrai** (identidade pronta) ou **gera** (do zero). Extrair de algo existente é o caso mais comum — não reinvente o que já foi decidido.
**Perguntar (estruturada):** "De onde vem a identidade?" — opções:
- *Protótipo/tela já existe (HTML, Figma, print)* → **EXTRAIR** cores/tipografia/radius do artefato e **apresentar pra confirmar**, não gerar. (Caso mais comum.)
- *Marca existente (manual/guidelines)* → extrair do manual + confirmar.
- *Só logo e/ou cores* → gerar o resto a partir delas + confirmar.
- *Partir do zero* → a IA propõe tudo, o líder valida.

Quando há artefato, os blocos B2–B9 abaixo viram **confirmação do que foi extraído** (modo "proponho e valido"), não perguntas do zero.

## B2 — Cor principal (primary)
**Por que importa:** é a cor da ação principal (botões, links, destaques) — a que mais "pinta" o produto. Um token é só um nome fixo pra um valor (`--primary`) que a biblioteca inteira lê; mudar num lugar muda em tudo.
**Perguntar:** "Qual a cor principal da marca? Pode ser o hex (ex: `#1E5AAF`), ou me manda o logo que eu extraio." Se não houver: proponha 2–3 opções coerentes com o segmento e marque uma.

## B3 — Tom da identidade
**Por que importa:** guia as escolhas seguintes (contraste, saturação, arredondamento).
**Perguntar (estruturada):** "Que sensação o produto deve passar?" — *Institucional/sóbrio · Moderno/vibrante · Técnico/denso · Amigável/leve.* *(Recomendado: institucional/sóbrio para produtos internos de gestão.)*

## B4 — Cores semânticas
**Por que importa:** success/warning/danger/info comunicam estado (salvo, cuidado, erro) — precisam ser consistentes e acessíveis.
**Perguntar:** "Usamos as cores padrão de sucesso/alerta/erro/informação, ou a marca tem as suas?" — *default recomendado: paleta semântica padrão do DS, ajustada pra casar com a primary.*

## B5 — Neutros, superfícies e modo escuro
**Por que importa:** fundo, texto, bordas e cinzas são 80% da tela. Disabled no DS é **cinza real** (`gray-100`/`gray-400`), nunca opacidade.
**Perguntar:** "Fundo claro (padrão) — e precisa de **modo escuro**?" *default: só claro, salvo pedido.* Confirme o disabled cinza real.

## B6 — Tipografia
**Por que importa:** a fonte carrega metade da personalidade e afeta legibilidade pro público leigo.
**Perguntar:** "Tem uma fonte da marca? Se não, prefere algo sóbrio ou moderno?" — *default recomendado: uma sans legível (ex: Inter).* Defina escala (ex: 12/14/16/20/24/32) e pesos (400/500/600).

## B7 — Radius (arredondamento)
**Por que importa:** `--radius` é único e a biblioteca toda lê dele — nunca radius solto num componente.
**Perguntar:** "Cantos mais retos (sério) ou mais arredondados (amigável)?" — *default: médio (ex: 8px).* Traduza a resposta em valor.
**Se a fonte tem MÚLTIPLOS radius** (ex: protótipo com card 10 / input 6 / botão 8): não copiar os três soltos. Definir um `--radius` **base** e derivar os demais por escala (ex: `--radius-sm = base − 2`). Apresentar a proposta de unificação e confirmar com o líder — o DS não aceita radius avulso por componente.

## B8 — Espaçamento
**Por que importa:** o DS trava grid de 8px (4px = mínimo), com lint automático. Só confirmar.
**Perguntar/afirmar:** "Mantemos o grid de 8px do DS (recomendado, é enforced)?" — *default: sim.*

## B9 — Contraste / acessibilidade
**Por que importa:** texto sobre cor precisa passar em contraste AA senão fica ilegível pra parte dos usuários. A IA verifica, não o líder.
**Fazer:** calcular o contraste de cada par cor/fundo. Regra de decisão quando fica no limite:
- **Texto normal** exige **≥ 4.5:1**. Abaixo disso, a cor **não pode** carregar texto normal — ou escurece até passar, ou só se usa em **elemento de UI / texto grande** (≥ 3:1).
- Exemplo real (GRC): primary teal `#0E7C6B` dá ~4.4:1 com branco → serve pra **botão** (UI), mas para texto normal sobre branco use a versão dark. Registrar a decisão, não deixar ambíguo.
- Nunca declarar "verificado" sem o número. Se reprovar em tudo, ajustar o tom e avisar o porquê.

## B10 — Gerar, aprovar e materializar
**Fazer, nesta ordem:**
1. Montar o UI KIT (spec em `planning/<projeto>/ui-kit.md` — template `templates/ui-kit.md`) e apresentar com preview.
2. **Gate de aprovação** (`AskUserQuestion`): *Aprovar e aplicar · Ajustar antes · Só apresentar.* — nunca escrever no `index.css` sem aprovação.
3. Após aprovado: escrever tokens em `src/index.css` e gerar `uikit-<projeto>.html` (styleguide navegável: paleta, tipografia, e os componentes-chave já vestidos com a identidade). Conferir no preview.

## Definition of Ready do kickoff (trava)
- [ ] Todos os públicos com A2–A6 preenchidos + conflitos/prioridade (A7) + persona (A8)
- [ ] Primary, semânticas, neutros/modo escuro, tipografia, radius, espaçamento definidos
- [ ] Contraste AA verificado
- [ ] UI KIT aprovado pelo líder e aplicado ao `index.css`
- [ ] `uikit-<projeto>.html` gerado e conferido
- [ ] Premissas registradas (tudo que foi "não sei" + default)

## Encadeamento

> Ao fechar, **atualize o checkpoint** `planning/<projeto>/PX-PROGRESS.md` (ver "Checkpoint de progresso" no `px-protocol.md`): marque o kickoff como feito (públicos + UI KIT aplicado ao `index.css`), registre o alvo de build e o próximo passo, e sincronize Premissas → *Decisões travadas* e pendências → *Perguntas em aberto*.

Com a Definition of Ready completa, escolher o próximo passo pelo tamanho:
- **Sistema/várias telas (iniciativa):** rodar `agile-epic` pra decompor em backlog de telas; depois `px-request` em cada uma.
- **Uma tela só:** ir direto pro `px-request`.
Também decidir aqui o **alvo de build** (protótipo via `agile-proto` × app React do produto) — ver `CLAUDE.md` › Fluxo de skills. O `px-request` consome os públicos e o UI KIT definidos aqui.

## Relação com o fluxo
```
px-kickoff  →  px-request (por tela)  →  px-story  →  handoff → dev
   ^ você está aqui (uma vez por projeto)
```
