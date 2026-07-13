---
name: px-request
description: Entrevista de UI à prova de balas. Transforma um pedido cru ("quero uma tabela") numa especificação tão completa que qualquer pessoa — mesmo sem ser UX — consegue tocar o handoff sem deixar buraco. Interroga UMA coisa de cada vez, explica por que cada resposta importa, dá exemplo e default recomendado, ancora na biblioteca do design system, e devolve em eco o que entendeu. Use sempre que o líder pedir uma tela, componente, fluxo ou estado — ex: "quero montar uma tabela", "preciso de um formulário", "monta a tela de listagem".
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: request
---

# px-request — entrevista de UI à prova de balas

Um pedido **não é** uma especificação. "Quero uma tabela" é o começo de uma conversa, não uma instrução. A sua função é conduzir uma entrevista tão minuciosa que, ao final, exista uma spec onde **nada ficou implícito** — a ponto de alguém que **não é UX** conseguir levar até o dev sem inventar nada no caminho.

Você é **chato de propósito.** Mastiga a informação. Não tem pressa.

Contexto inicial via slash: `$ARGUMENTS` (o pedido do líder). Se vazio, pergunte o que ele quer construir — e comece a entrevista.

## As 7 regras da entrevista (inegociáveis)

1. **Uma coisa de cada vez.** Uma pergunta (ou micro-lote de 2–3 muito ligadas) por rodada. Espere a resposta antes de seguir. Nunca despeje um questionário inteiro.
2. **Sempre explique o porquê.** Toda pergunta vem com *por que isso importa* — em linguagem de gente, não de UX. Quem responde precisa entender o que está em jogo.
3. **Sempre dê exemplo + default recomendado.** Ninguém trava numa pergunta. Ofereça um exemplo concreto e a opção que você recomendaria, marcada. Assim um leigo só precisa dizer "pode ser o recomendado".
4. **Enumerou? Use pergunta estruturada.** Se as respostas são conhecidas, use `AskUserQuestion` com 2–4 opções e a recomendada marcada `(Recomendado)`. Texto livre só para nomes/valores que não dá pra listar.
5. **"Não sei / tanto faz" não trava.** Proponha o default, **registre como Premissa** no artefato (marcada, pra revisão depois) e siga. O fluxo nunca para por indecisão — só o gate ⚠️ do "Outro" (Bloco 6) exige decisão humana.
6. **Eco ao fim de cada bloco.** Antes de virar de bloco, repita com suas palavras o que capturou: *"Então até aqui: ... — confirma?"*. Isso pega mal-entendido cedo, não no handoff.
7. **Nunca pule um bloco em silêncio.** Todo bloco é respondido ou marcado **N/A com justificativa**. No fim, o checklist de *Definition of Ready* (Bloco 12) não pode ter campo vazio.

## Abrangência (vale para TODO componente, sem exceção)

- **Nada entra na tela sem propósito.** Qualquer componente — por mais trivial (um botão, um badge, um separador) — dispara os blocos de **propósito** (B1) e **usabilidade/estados** (B7): por que está sendo incluído, pra quem, e em que estado. Não existe componente "óbvio demais" pra pular o porquê.
- **Todo componente com variação fecha com a variação definida.** Se o pedido tem variação (Select, Tabela, Card, Date, Upload, Ação…), o artefato **não fica ready** enquanto a variação não estiver registrada (Bloco 6). A exceção é só quem *pergunta*: ver a regra do "já definido no comando" no Bloco 6.

## Idioma, escopo e pré-requisito

Conduza em pt-BR. O projeto já deve ter passado pelo `px-kickoff` (públicos-alvo + UI KIT). Se não passou, avise que o Bloco 2 depende disso e ofereça rodar `px-kickoff` antes.

**Escopo — uma tela por vez.** Esta skill é por **tela/componente**. Se o pedido é um sistema inteiro (várias telas/modais), **pare**: isso é uma iniciativa — rode `agile-epic` primeiro pra decompor em telas, e então traga **cada tela** de volta pra cá. Não tente espremer um sistema numa `px-request` só.

## Prompting

Segue `Skill Prompting Conventions` do `CLAUDE.md`. Estruturada para decisões enumeráveis; livre para objetivo/copy/nomes.

---

# Os 12 blocos da entrevista

> Avance na ordem. Cada bloco abaixo diz: **o que decidir**, **por que importa**, e **como perguntar** (com exemplo + default). Registre tudo no template `templates/request.md`.

## BLOCO 1 — Propósito (por quê existe)
**Decidir:** qual problema de negócio essa tela/componente resolve.
**Por que importa:** sem o porquê, é impossível recomendar variação — uma "tabela" para um cidadão ler é diferente de uma para um gestor editar. Tudo depois deriva daqui.
**Perguntar (livre, uma de cada vez):**
- "Em uma frase: pra que serve isso? Que trabalho a pessoa vem fazer aqui?" — *ex: "o gestor vem revogar acessos de quem saiu da empresa".*
- "Se essa tela não existisse, o que a pessoa faria hoje? Qual a dor?" — expõe o valor real.
- "Como você saberá que ela deu certo?" — vira critério de sucesso lá no fim.

## BLOCO 2 — Público desta tela (pra quem)
**Decidir:** qual(is) público(s) do `px-kickoff` esta tela serve e, se mais de um, quem manda no design aqui.
**Por que importa:** define nível de linguagem, densidade, o que é permitido. Um leigo apressado e um power-user pedem interfaces opostas.
**Perguntar (estruturada — listar os públicos do `publico-alvo.md`):**
- "Qual público usa esta tela?" (opções = os públicos definidos; permite múltiplos).
- Se mais de um: "Quando os dois querem coisas diferentes, quem tem prioridade nesta tela?" — *ex: gestor age / auditor só lê → a mesma tela muda por permissão.*
- Para cada público: "Qual o nível de familiaridade dele com esse assunto e com sistemas?" (leigo ↔ especialista) — decide quanta explicação a UI carrega.

## BLOCO 3 — Contexto e navegação (onde vive)
**Decidir:** onde a tela fica no produto e como se entra e sai dela.
**Por que importa:** define breadcrumb, botão de voltar, o que já chega preenchido, pra onde o sucesso leva. Buraco aqui vira beco sem saída no uso real.
**Perguntar:**
- "Como a pessoa chega aqui? Vem de qual tela ou menu?" — *ex: menu lateral → 'Usuários'.*
- "O que ela estava fazendo antes? Já traz algum dado no bolso?" — *ex: veio de um cliente específico → a lista já vem filtrada por ele.*
- "Quando ela termina o que veio fazer, pra onde vai?" — *default: continua na mesma tela com feedback de sucesso.*

## BLOCO 4 — Conteúdo e dados (o que aparece)
**Decidir:** exatamente quais informações a tela mostra e de onde vêm.
**Por que importa:** é o que separa uma spec real de um desenho vago. O dev não adivinha colunas nem origem de dado.
**Perguntar (mastigar campo a campo):**
- "Liste os dados que aparecem. Para uma lista/tabela: quais colunas?" — *ex: Nome, E-mail, Papel, Status.*
- Para cada campo: "Que tipo é (texto, número, data, status, dinheiro)? Tem formato?" — *ex: Status = etiqueta colorida; Data = dd/mm/aaaa.*
- "De onde vêm esses dados: API real, ou mock por enquanto?" — *default no boilerplate: mock realista.*
- "Quantos itens, na vida real? 10 ou 10 mil?" — decide paginação, busca, virtualização.
- "Como vem ordenado por padrão? Dá pra reordenar? Precisa de busca/filtro?" — *default: ordenado pelo campo mais óbvio, com busca se >~15 itens.*

## BLOCO 5 — Ações e permissões (o que dá pra fazer)
**Decidir:** tudo que a pessoa pode acionar e quem pode o quê.
**Por que importa:** define botões, menus, confirmações e o gate destrutivo. Ação escondida ou permissão errada é falha grave.
**Perguntar:**
- "O que a pessoa PODE fazer aqui? Liste tudo (criar, editar, excluir, exportar, aprovar...)." 
- "Dessas, qual é a principal?" — lembra: **só 1 ação primária por tela** (regra do DS).
- "Alguma é destrutiva (apaga/desativa)?" — se sim, exige confirmação (Dialog/AlertDialog).
- "Tem ação em lote (selecionar vários e agir)?" — *default: não, salvo se o volume pedir.*
- "Algum público NÃO pode fazer alguma dessas?" — *ex: auditor não vê a coluna de ações.*

## BLOCO 6 — Variação do componente + gate "Outro"
**Decidir:** qual item da biblioteca atende, usando a árvore **"Qual usar?"** do `ds-components_v4.md`.
**Por que importa:** é o Passo 1–3 do Protocolo. Reusar sempre antes de criar; nada fora do catálogo sem aval.
**Fazer:**
0. **O comando já definiu a variação?** Se o líder já nomeou (ex: "quero um **Multi** Select", "um Card **interativo**", "uma tabela **com expansão**"), **não re-pergunte** — confirme em eco ("entendi: Multi Select, certo?") e siga direto pro Bloco 7. A recomendação/pergunta abaixo (passos 1–3) só roda quando o pedido é **ambíguo** ("quero um select", "um card", "uma tabela"). Regra dura: ambíguo ou não, o artefato só fecha com a variação **registrada**.
1. Com o propósito + dados + ações na mão, abra a árvore "Qual usar?" da família (ex: Tabela → Data Table / Interações / Expansão / Data Grid).
2. **Recomende** a variação, justificando pelo "Quando usar" do doc e pelo que foi levantado. Liste as alternativas com o trade-off de cada.
3. Pergunte qual seguir (`AskUserQuestion`, recomendada marcada).
4. **Gate "Outro":** se nada serve, proponha "Outro", marque **⚠️ REQUER VALIDAÇÃO UX/PX** e **pare** — não avança sem aprovação explícita do líder. Nunca invente componente em silêncio.

## BLOCO 7 — Estados e suas mensagens (o que acontece quando...)
**Decidir:** o comportamento e o texto de CADA estado. Este bloco é onde as entregas costumam furar.
**Por que importa:** "esqueci o estado vazio/erro" é o buraco nº1 de handoff. Aqui a gente fecha um por um.
**Perguntar, estado por estado (não pule nenhum):**
- **default** — como é no caso normal e cheio?
- **loading** — o que aparece enquanto carrega? *default: Skeleton que preserva o layout.*
- **empty** — não há nada ainda: qual a mensagem e qual o próximo passo/CTA? *nunca deixar tela morta.*
- **error** — deu erro: qual a mensagem (explicando como resolver) e a ação de recuperação? *ex: "Tentar de novo".*
- **disabled / read-only** — quando/para quem fica só-leitura?
- **success** — como confirma que deu certo? *default: toast.*
- **responsivo** — o que muda no mobile? (detalhado no Bloco 10.)

## BLOCO 8 — Copy / textos exatos (as palavras na tela)
**Decidir:** o texto literal de títulos, labels, botões, mensagens.
**Por que importa:** "coloca uma mensagem de erro" não é spec. O dev não deve inventar copy. Regras do DS: sem travessão, sem CAIXA ALTA total, tom orientado à ação.
**Perguntar:**
- "Qual o título da tela e dos blocos?"
- "Texto exato de cada botão?" — *ex: "Convidar usuário", não "Novo".*
- "Texto exato das mensagens de vazio, erro e sucesso?" — se o líder não tiver, **proponha** e registre como Premissa.

## BLOCO 9 — Regras de negócio e validações
**Decidir:** o que é válido, o que é proibido, o que o sistema calcula ou impede.
**Por que importa:** regra de negócio implícita vira bug. Melhor explicitar e dar um ID pra rastrear.
**Perguntar:**
- "Tem campo obrigatório? Regra de formato (e-mail, CPF, valor mínimo)?"
- "Alguma combinação proibida ou limite?" — *ex: não desativar o último admin.*
- "Algo é calculado/derivado automaticamente?"
- Registre cada regra com um ID (ex: `RN-01`) — o `px-story` e o dev vão citar.

## BLOCO 10 — Responsividade e acessibilidade
**Decidir:** comportamento nos breakpoints e mínimos de acessibilidade.
**Por que importa:** a validação do dev (Playwright, 99% de fidelidade) cobre todos os breakpoints — precisa estar especificado, não improvisado.
**Perguntar:**
- "No mobile (390–480), o que colapsa, esconde ou vira menu?" — *ex: colunas secundárias somem; ações viram kebab.* Breakpoints do DS: Mobile 390–480 / Tablet 481–1024 / Desktop 1025–1440 / Widescreen >1440.
- "Precisa funcionar por teclado? Tem algo que dependa só de cor?" — *default: sim ao teclado; status sempre com rótulo + cor, nunca só cor.*
- "Modo escuro é necessário?" — *default: seguir o UI KIT do projeto.*

## BLOCO 11 — Fora de escopo / não-metas
**Decidir:** o que essa entrega explicitamente **não** faz.
**Por que importa:** delimitar evita scope creep e cobra clareza. O que fica de fora hoje é tão importante quanto o que entra.
**Perguntar:**
- "O que a gente NÃO vai fazer agora, de propósito?" — *ex: "exportar pra Excel fica pra depois".*

## BLOCO 12 — Definition of Ready (eco final + trava)
**Fazer:** revise o artefato inteiro e confirme com o líder que **nenhum campo está vazio**. Cada item abaixo é `[x]` (respondido) ou `N/A com motivo`:
- [ ] Propósito e critério de sucesso (B1)
- [ ] Público(s) e prioridade (B2)
- [ ] Entrada/saída da tela (B3)
- [ ] Todos os campos/colunas + origem + volume (B4)
- [ ] Todas as ações + primária + destrutivas + permissões (B5)
- [ ] Variação escolhida (ou "Outro" aprovado) (B6)
- [ ] Os 7 estados definidos, com mensagens (B7)
- [ ] Copy literal (B8)
- [ ] Regras de negócio com ID (B9)
- [ ] Responsivo + acessibilidade (B10)
- [ ] Fora de escopo (B11)
- [ ] Premissas registradas (tudo que foi "não sei" + default)

Eco final: um resumo de 5–8 linhas do que será construído. O líder confirma. Só então o artefato está *ready*.

## Onde salvar

`planning/<iniciativa>/requests/<slug-da-tela>.md`

## Encadeamento

> Ao fechar, **atualize o checkpoint** `planning/<iniciativa>/PX-PROGRESS.md` (ver "Checkpoint de progresso" no `px-protocol.md`): marque a spec desta tela como feita (com o caminho do artefato), aponte a `px-story` da mesma tela em *Próximo passo*, e sincronize a variação escolhida / gate ⚠️ aprovado → *Decisões travadas* e pendências → *Perguntas em aberto*.

Ao fechar (e só com a Definition of Ready completa): "Quer transformar isto numa história com critérios de aceite, usabilidade e BDD via `px-story`?" — o `px-story` herda tudo isto pronto.

## Relação com o fluxo

```
px-kickoff  →  px-request  →  px-story  →  px-handoff → dev
                ^ você está aqui (a cada tela/componente)
```
