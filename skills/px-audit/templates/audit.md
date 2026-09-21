# Auditoria de redesign — [Produto]

**Origem:** produto existente [nome / URL / repo]
**Data:** [dd/mm/aaaa] · **Responsável:** [líder UX/PX]

---

## 1. Contexto do redesign (B1)

- **Por que reformar:** [uma frase]
- **Motivação:** [queixa / métrica / adoção do DS / estratégia]
- **Critério de sucesso:** [como saberemos que deu certo]

## 2. Inventário AS-IS (B2)

**Fonte analisada:** [repo local rodando / URL ao vivo / documentos — prints/PDF/Figma]
**Onde vive hoje:** [URL / ambiente / repo / lista de arquivos recebidos]

<!-- ID obrigatório: A-B2-NN. Nunca reciclar nem renumerar — o px-request cita estes IDs. -->

| ID | Tela / fluxo | O que faz hoje | Fonte (repo/URL/doc) | Prioritária p/ redesign? |
|---|---|---|---|---|
| A-B2-01 | [nome] | [1 linha] | [ex: repo · print login.png · pág.3 do PDF] | [sim/não] |

### 2.1 Capacidade — o legado PRODUZ? (ações e estados)

<!-- Duas perguntas por item, não uma. "Exibe?" é metade; "produz, por qual caminho?" é a que
     pega proposta nossa disfarçada de paridade.
     PARIDADE  → produz, com evidência arquivo:linha do handler/função/constante de ação
                 (ou da superfície que grava o estado). Template, diretiva, DOM, enum e
                 contador NÃO servem como evidência.
     PROPOSTA  → exibe (ou o domínio conhece), mas nenhum caminho do cliente produz.
                 Vira linha obrigatória do Bloco 11b da px-request da tela.
     NÃO VERIFICADO → fonte fora de alcance. Vira Pergunta em aberto com dono, e o item
                 não pode ser citado como paridade em nenhum artefato seguinte.
     Exibição pura (nome, data, número só lido) → N/A — leitura.
     Antes de fechar o veredito: ler as PR-* abertas sobre a região. -->

| ID da tela | Ação ou estado | Exibe? | Produz? evidência (`arquivo:linha`) | Veredito | `PR-*` consultada |
|---|---|---|---|---|---|
| A-B2-01 | [ex: abster-se na aprovação] | [sim] | [`serviceRequest...Controller.js:16` só APPROVAL_ACTION e REJECT_ACTION; não há `abstainRequest`] | [PARIDADE / PROPOSTA / NÃO VERIFICADO / N/A — leitura] | [PR-31 / nenhuma] |

## 3. Públicos e jornadas atuais (B3)

| Público | Jornada principal (passos) |
|---|---|
| [ex: gestor] | [entra → filtra → abre → aprova] |

## 4. Diagnóstico de usabilidade (B4)

> Rodado via `ux-flows` + `ux-persona` sobre as jornadas priorizadas. Achados por dimensão da rubrica.

<!-- Contagem literal no enunciado: "16 ações em dois níveis", nunca "vários itens". -->

| ID | Tela / fluxo | Dimensão | Achado (observável) | Severidade |
|---|---|---|---|---|
| A-B4-01 | [tela] | [Descoberta/Clareza/Feedback/Fricção/Beco/Fidelidade/Autenticidade] | [o que trava/atrapalha] | [Crítico/Alto/Médio/Baixo] |

**Estados observados × não-observáveis** (só quando a fonte foi documento estático):

| Tela | Observável no material | NÃO observável (vira Pergunta em aberto) |
|---|---|---|
| [tela] | [default, vazio] | [loading, erro, hover, foco, read-only, responsivo] |

## 5. Mapa de lacunas atual → DS (B5)

> Por tela: como cada componente atual se mapeia ao design system e o que fazer.

### [Tela X]

<!-- Um ID por linha, e composto se decompõe: cada sub-elemento tem ID próprio. -->

| ID | Componente atual | Divergência de anatomia | Variação canônica do DS | Produz? evidência (`arquivo:linha`) | Veredito de capacidade | Ação |
|---|---|---|---|---|---|---|
| A-B5-01 | [ex: tabela caseira] | [off-grid, hex hardcoded, estado vazio ausente] | [Data Table] | [N/A — leitura, ou `arquivo:linha` do handler/constante] | [PARIDADE / PROPOSTA / NÃO VERIFICADO / N/A — leitura] | [Reestilizar / Trocar / Compor / ⚠️ Outro] |

> **Veredito de capacidade** é obrigatório em todo sub-elemento que é **ação** ou **estado**;
> exibição pura recebe `N/A — leitura`. `PROPOSTA` aqui vira linha do Bloco 11b da
> `px-request` desta tela. `NÃO VERIFICADO` vira Pergunta em aberto com dono e **não pode
> ser citado como paridade** depois.

> ⚠️ **Gate "Outro":** [componentes sem equivalente no catálogo — REQUER VALIDAÇÃO UX/PX antes de avançar]

## 6. Backlog de redesign priorizado (B6)

> Ordem por impacto × esforço. Cada item vira uma tela no `px-epic` (AS-IS → TO-BE).

| ID | Ordem | Tela | AS-IS (o que é) | TO-BE (o que vira) | Resolve (IDs de B4/B5) | Tipo | Público |
|---|---|---|---|---|---|---|---|
| A-B6-01 | 1 | [tela] | [estado atual] | [estado alvo] | [A-B4-03, A-B5-11] | [quick win / reestruturação] | [público] |

## 7. Definition of Ready da auditoria (B7)

- [ ] Objetivo do redesign + critério de sucesso (B1)
- [ ] Inventário AS-IS, prioritárias marcadas (B2)
- [ ] Públicos + jornadas atuais (B3)
- [ ] Diagnóstico com achados + severidade (B4)
- [ ] Mapa de lacunas atual→DS, ação por componente (B5)
- [ ] Backlog priorizado, AS-IS→TO-BE (B6)
- [ ] Todo item de B2/B4/B5/B6 com ID `A-<bloco>-<NN>`, contagem literal e composto decomposto
- [ ] Veredito de capacidade em toda ação e todo estado (2.1 e B5), com evidência `arquivo:linha` onde for `PARIDADE`
- [ ] `PR-*` abertas das regiões auditadas lidas antes dos vereditos, ou "nenhuma", por extenso
- [ ] Itens `PROPOSTA` listados para virar linha do Bloco 11b da `px-request`
- [ ] Premissas registradas
- [ ] Perguntas em aberto com dono (inclui todo `NÃO VERIFICADO`)

## Premissas

- [decisões assumidas por default, revisáveis]

## Perguntas em aberto

- [pendências com dono — inclui acesso ao produto, se faltou percorrer]

## Encadeamento

- [ ] Produto sem identidade no DS → `px-kickoff` (personas + UI KIT)
- [ ] Identidade ok → `px-epic` (decompor o backlog de redesign)
- Cada tela → `px-request` → `px-story` → px-handoff → dev

> O `px-request` de cada tela dá **veredito explícito a cada ID desta auditoria** (Bloco 11.1
> de lá): em escopo, ou fora de escopo com motivo e destino. Item sem veredito reprova a DoR
> do request.
>
> Os itens marcados `PROPOSTA` em 2.1/B5 entram no **Bloco 11b** do request como "acrescenta
> capacidade", com a evidência da ausência no legado. Os `NÃO VERIFICADO` seguem como
> Perguntas em aberto e não podem ser citados como paridade.
