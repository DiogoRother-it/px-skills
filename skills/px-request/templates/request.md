# Request de UI — <Tela/Componente>

**Origem:** `px-request` · **Iniciativa:** <iniciativa> · **Data:** <YYYY-MM-DD>
**Status:** em entrevista | ready

## B1 — Propósito
- **Pra que serve (1 frase):**
- **Dor que resolve / como é hoje:**
- **Critério de sucesso:**

## B2 — Público desta tela
- **Público(s):** (de `../publico-alvo.md`)
- **Prioridade quando conflitam:**
- **Familiaridade (por público):**

## B3 — Contexto e navegação
- **Como chega:**
- **Traz dado do passo anterior?:**
- **Pra onde vai ao concluir:**
- **Rota:**

## B4 — Conteúdo e dados
| Campo/Coluna | Tipo | Formato | Origem (API/mock) |
|---|---|---|---|
| | | | |
- **Volume esperado:**
- **Ordenação padrão / busca / filtro:**

## B5 — Ações e permissões
| Ação | Primária/Secundária/Destrutiva | Quem pode | Chave de permissão | Confirmação? | Âncora `data-onb` |
|---|---|---|---|---|---|
| | | | | | |
- **Ação em lote:**

## B6 — Variação do componente
- **Família / árvore "Qual usar?":**
- **Recomendada:** <X> — **porque:**
- **Alternativas (trade-off):**
- **Escolha do líder:**
- **"Outro" (se houver):** ⚠️ REQUER VALIDAÇÃO UX/PX — [ ] aprovado

## B7 — Estados e mensagens
| Estado | Comportamento | Mensagem/CTA |
|---|---|---|
| default | | |
| loading | | |
| empty | | |
| error | | |
| disabled/read-only | | |
| success | | |

## B8 — Copy literal
- **Títulos:**
- **Botões:**
- **Mensagens (vazio/erro/sucesso):**

## B9 — Regras de negócio e validações

<!-- ID global por iniciativa: RN-<SIGLA>-<DOMÍNIO>-<NN>. NUNCA reinicie em 01 nesta tela —
     consulte o regras-negocio.md da iniciativa e cite o ID se a regra já existir. -->

| ID | Regra | Validação |
|---|---|---|
| RN-<SIGLA>-<DOMÍNIO>-01 | | |

## B10 — Responsividade e acessibilidade
- **Mobile (o que colapsa/vira menu):**
- **Teclado / cor não isolada:**
- **Modo escuro:**

## B11 — Fora de escopo, com veredito item a item
-

### B11.1 — Portão de cobertura da auditoria (redesign)

<!-- Todo item numerado da auditoria recebe veredito. Item sem veredito reprova a DoR.
     Contagem literal, nunca resumo: "16 ações em dois níveis" se escreve como as 16.
     Tela nova, sem auditoria de origem: escrever N/A e o motivo.
     Antes de concluir: ler as PR-* abertas sobre cada região. Pendência aberta é insumo
     obrigatório do veredito — a resposta pode já estar escrita lá. -->

| Item da auditoria | Veredito (em escopo / fora de escopo) | Motivo / para onde vai | `PR-*` consultada |
|---|---|---|---|
| | | | [PR-NN / nenhuma] |

## B11b — Divergências declaradas do legado (só em redesign)

<!-- Nenhuma? Escrever "nenhuma divergência do legado". Em branco é ambíguo.

     Trava de origem, nas duas direções:
     1. Linha que ACRESCENTA CAPACIDADE cita a evidência da AUSÊNCIA no legado — arquivo e
        linha da função que não existe, ou da lista de constantes que não a contém.
     2. Item que a spec trata como PARIDADE de ação ou de estado cita o caminho que o PRODUZ
        no legado (arquivo:linha do handler/função/constante, ou da superfície que grava o
        estado). Não citou, não é paridade: é PROPOSTA (linha aqui) ou NÃO VERIFICADO
        (Pergunta em aberto com dono, e não pode ser citado como paridade depois).
     Template, diretiva, DOM, enum e contador NÃO respondem "produz?" — só mostram/conhecem. -->

| # | O legado faz | Aqui faz | Acrescenta capacidade? | Evidência no legado (`arquivo:linha`) | Por quê | Quem decidiu / quando |
|---|---|---|---|---|---|---|
| | | | [sim/não] | [ex: `...Controller.js:16` declara só APPROVAL_ACTION e REJECT_ACTION; não há `abstainRequest`] | | |

**Paridade de ação e de estado — caminho que produz no legado:**

<!-- Uma linha por ação e por estado que esta spec trata como paridade. Exibição pura
     (nome, data, número só lido) não entra aqui. Sem evidência, muda o veredito. -->

| Ação ou estado | Caminho que o produz no legado (`arquivo:linha`) | Veredito |
|---|---|---|
| | | [PARIDADE / PROPOSTA / NÃO VERIFICADO] |

## B11c — Divergências declaradas do design system (sempre)

<!-- Nenhuma? Escrever "nenhuma divergência do design system".
     Default trocado, escala trocada, parte omitida, anatomia do variant errado,
     composição à mão onde existe componente pronto, ícone fora da convenção,
     tooltip de seção em vez de por campo, hierarquia de ação invertida. -->

| # | O DS manda | Aqui faz | Por quê | Quem decidiu / quando |
|---|---|---|---|---|
| | | | | |

## B12 — Definition of Ready
- [ ] B1–B11c respondidos ou N/A com motivo
- [ ] Todo item numerado da auditoria com veredito (B11.1)
- [ ] Divergências do legado declaradas, ou "nenhuma" (B11b)
- [ ] Linha de "acrescenta capacidade" com evidência da ausência no legado (B11b)
- [ ] Paridade de ação/estado com o caminho que a produz citado (B11b)
- [ ] `PR-*` abertas das regiões desta tela lidas, ou "nenhuma" (B11.1)
- [ ] Divergências do design system declaradas, ou "nenhuma" (B11c)
- [ ] Premissas registradas abaixo
- **Premissas (respostas "não sei" + default assumido):**
  -

## Próximo passo
- [ ] `px-story` — história com aceite + usabilidade + BDD

<!-- Salvar em: planning/<iniciativa>/requests/<slug-da-tela>.md -->
