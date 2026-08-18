---
name: ux-persona
description: Roda um walkthrough qualitativo de usabilidade em DUAS fases isoladas — primeiro um subagente cego assume uma persona e navega o produto DE VERDADE (repo local ou URL), narrando em primeira pessoa o que sentiu a cada passo; depois você assume o chapéu de UX Designer e diagnostica cada fricção relatada pela rubrica de 7 dimensões (Descoberta, Clareza, Feedback, Fricção, Sem beco sem saída, Fidelidade, Autenticidade de dados), com severidade e proposta ancorada no DS. Diferente do Playwright (que confirma que o código faz o que devia), isto confirma COMO uma pessoa sente tentando usar. Use quando o líder disser "roda o ux-persona", "testa como um usuário leigo/com pressa/cético/no celular", "simula um usuário nessa tela", "quero saber onde essa jornada trava emocionalmente", ou quando px-audit/px-story/px-epic oferecerem o walkthrough do ux-persona sobre um flow.
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: usability-walkthrough
---

# ux-persona — usuário sintético + diagnóstico UX

Duas coisas que **não podem acontecer no mesmo contexto**: sentir como um usuário real sentiria, e já saber a regra de design que devia ter sido seguida. Um humano nunca teria as duas ao mesmo tempo — e se você tentar fazer as duas na mesma passada, a segunda contamina a primeira: você "sente" a confusão que sabe que deveria sentir, não a que sentiria de fato.

Por isso esta skill roda em **duas fases com contextos separados**:

1. **Fase 1 — Persona (subagente cego).** Um subagente novo, que só recebe o persona + o flow — nunca o design system, o `CLAUDE.md` do produto, nem o código — navega o produto **de verdade** e narra em primeira pessoa.
2. **Fase 2 — UX Designer (você, no thread principal, com todo o contexto).** Lê o diário da Fase 1 como dado observacional e diagnostica.

## Por que isto não é o Playwright

O Playwright do dev (citado no protocolo como validação pós-handoff) confirma **comportamento determinístico**: o botão existe, o clique dispara o request certo, o estado muda. Ele não sabe dizer se a pessoa **achou** o botão, se **hesitou**, se **desistiu no meio**. `ux-persona` cobre exatamente essa lacuna — é qualitativo, não substitui asserção de teste. Os dois convivem: Playwright garante que funciona, `ux-persona` garante que **dá pra usar** e mostra **como pareceu usar**.

## Pré-requisitos (gate — não pule)

Confirme os três antes de começar. Falta algum → resolva antes, não improvise:

1. **Um flow.** `e2e/flows/<slug>.md`. Não existe? Ofereça rodar `ux-flows` primeiro (ou aceite um flow ad-hoc de uma tela só, se for isso mesmo que o líder quer).
2. **Uma persona.** Um dos 6 bundled (`templates/persona-*.md` — ver lista abaixo) ou um custom em `e2e/personas/<slug>.md`. Sem público mapeado ainda? Aponte pro `px-kickoff` A8.
3. **Um alvo de verdade, navegável.** Repo local rodando (`npm run dev`/preview — preferencial, todos os estados dinâmicos observáveis) ou URL ao vivo autenticada. **Recuse rodar contra print/PDF/mockup estático** — sentimento simulado sobre imagem congelada é encenação, não dado. Se só houver documento, direcione pro `px-audit` modo documento (ele foi feito pra esse caso; isto aqui não foi).

**Gate de ferramenta:** a Fase 1 exige (a) um jeito de abrir um subagente isolado (a ferramenta de subagente/Task do Claude Code) e (b) ferramentas de navegação de browser disponíveis no ambiente (nesta sessão, o MCP de browser; em outro ambiente, pode ser outro MCP equivalente — Playwright MCP, chrome-devtools, etc.). Se nenhum dos dois existir no ambiente, **diga isso explicitamente e pare** — não finja a Fase 1 narrando "como se" tivesse navegado.

## Os 6 personas bundled

Cada um em `templates/persona-<slug>.md`, com contexto de uso, familiaridade, paciência, o que faz quando trava, e o vocabulário da narração:

| Persona | Em uma linha |
|---|---|
| `novice` | Leigo no assunto e em sistemas; lê tudo, não infere ícone sem rótulo, desiste só depois de tentar de novo com calma. |
| `rushed` | Pressa real, pula texto, quer o caminho mais curto, desiste rápido se não achar de cara. |
| `skeptical` | Desconfia de cada ação, relê antes de confirmar, quer certeza antes de qualquer coisa que pareça irreversível. |
| `mobile` | Uma mão, tela pequena, sinal instável; se irrita com alvo de toque pequeno e com texto cortado. |
| `accessibility` | Presta atenção em contraste, foco visível, ordem de leitura e tamanho de alvo — sinaliza o que um leitor de tela/teclado teria dificuldade. |
| `power-user` | Já conhece o produto, quer atalho e densidade, se incomoda com passo redundante ou confirmação repetida. |

Público sem persona óbvio entre os 6 → criar um custom em `e2e/personas/<slug>.md` (mesmo formato), a partir do perfil já levantado em `publico-alvo.md` (A2–A6 do `px-kickoff`).

## Fase 1 — o walkthrough (subagente isolado)

**Monte o prompt do subagente só com:**
- O persona inteiro (`templates/persona-<slug>.md` ou o custom).
- O flow inteiro (`e2e/flows/<slug>.md`) — os passos, não o resultado esperado de cada um em linguagem de "requisito"; se o flow expõe demais a intenção de design ("deveria mostrar X"), reescreva o passo como a persona o enxergaria ("preciso encontrar onde aprovar isto").
- A instrução: navegar **clicando pela interface, nunca por URL/rota interna** (mesma regra de ouro do BDD) e, a cada passo, registrar:
  - **O que vi** (só o que está de fato na tela — ancore com screenshot/leitura de página, nunca lembrança).
  - **O que tentei.**
  - **Senti** — na voz e vocabulário do persona (ver campo "Vocabulário da narração" do template).
  - **Travou?** Sim/Não. Se sim, tentar como **aquele** persona tentaria (novice tenta de novo mais devagar; rushed desiste; skeptical procura outra tela; mobile procura rolar; accessibility procura foco/label; power-user procura atalho) — nunca "sabendo" o caminho certo.
- **Nunca inclua** neste prompt: nomes de token/componente do DS, o `CLAUDE.md` do produto, a rubrica de dimensões, ou qualquer coisa que revele "o que estava certo".

**O que o subagente devolve:** um diário estruturado, um bloco por passo do flow (observação / ação tentada / sentimento / travou-ou-não / referência de screenshot).

Rodando **mais de uma persona no mesmo flow** → uma Fase 1 nova e isolada por persona, sempre do zero. Nunca reaproveite o diário de uma persona pra "ajudar" outra — cada rodada não sabe que a anterior existiu.

## Fase 2 — o diagnóstico (você, com o contexto todo)

Agora sim, carregue a rubrica e o DS. Leia o diário como um pesquisador lê a gravação de um teste de usabilidade — **não reabra a UI para "corrigir" a leitura antes de registrar o achado da persona.**

Para cada trava ou fricção relatada no diário:

1. **Mapeie a UMA dimensão da rubrica** (a mesma do `px-audit`/`px-story`): **Descoberta · Clareza · Feedback · Fricção · Sem beco sem saída · Fidelidade · Autenticidade de dados**.
2. **Classifique a severidade:** Crítico (trava a tarefa) · Alto · Médio · Baixo (cosmético).
3. **Proponha a solução ancorada no DS** — componente/token/padrão existente que resolveria (via `ds-components_v4.md`). Se não houver equivalente no catálogo, marque **⚠️ REQUER VALIDAÇÃO UX/PX** — mesmo gate de sempre, não invente componente novo aqui.

**Regra de ouro herdada do `px-audit`:** nunca lance achado sobre o que a persona não observou ou não tentou. O diário é a única fonte factual da Fase 2 — se ele não registrou algo, isso é lacuna (rode de novo cobrindo aquele passo), não conclusão.

## Formato e onde salvar

Use `templates/report.md` (Parte 1 = diário bruto da Fase 1; Parte 2 = diagnóstico da Fase 2; tabela final achado × dimensão × severidade × proposta). Salve em:

```
e2e/reports/<flow-slug>__<persona-slug>.md
```

## Fechamento — para onde os achados vão

- **Achado pequeno, localizado numa tela** → `px-change`.
- **Achado que exige repensar a tela** → `px-request` (nova spec da tela).
- **Vários achados espalhados, produto inteiro** → alimenta o backlog do `px-epic` ou do `px-audit` (Bloco 5/6), se estiver dentro de uma auditoria.

## Quando NÃO usar

- **Sem alvo navegável de verdade** (só print/PDF/mockup) → use `px-audit` modo documento.
- **Só quer confirmar que o comportamento funciona** (salvou, retornou erro, mudou o estado) → isso é Playwright do dev, não esta skill.
- **Quer inventariar telas/componentes atuais antes de diagnosticar** → isso é `px-audit` Bloco 2; esta skill entra depois, no Bloco 4, ou isolada sobre um flow já existente.

## Relação com o fluxo

```
ux-flows (gera o flow)  →  ux-persona (percorre: Fase 1 sente → Fase 2 diagnostica)  →  px-change / px-request / px-epic / px-audit
                                                                                      (achado vira ação, conforme o tamanho)

Também roda pós-handoff: dev valida com ux-flows/ux-persona + Playwright (ver px-protocol.md).
```
