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

| Tela / fluxo | O que faz hoje | Fonte (repo/URL/doc) | Prioritária p/ redesign? |
|---|---|---|---|
| [nome] | [1 linha] | [ex: repo · print login.png · pág.3 do PDF] | [sim/não] |

## 3. Públicos e jornadas atuais (B3)

| Público | Jornada principal (passos) |
|---|---|
| [ex: gestor] | [entra → filtra → abre → aprova] |

## 4. Diagnóstico de usabilidade (B4)

> Rodado via `ux-flows` + `ux-persona` sobre as jornadas priorizadas. Achados por dimensão da rubrica.

| # | Tela / fluxo | Dimensão | Achado (observável) | Severidade |
|---|---|---|---|---|
| 1 | [tela] | [Descoberta/Clareza/Feedback/Fricção/Beco/Fidelidade/Autenticidade] | [o que trava/atrapalha] | [Crítico/Alto/Médio/Baixo] |

**Estados observados × não-observáveis** (só quando a fonte foi documento estático):

| Tela | Observável no material | NÃO observável (vira Pergunta em aberto) |
|---|---|---|
| [tela] | [default, vazio] | [loading, erro, hover, foco, read-only, responsivo] |

## 5. Mapa de lacunas atual → DS (B5)

> Por tela: como cada componente atual se mapeia ao design system e o que fazer.

### [Tela X]

| Componente atual | Divergência de anatomia | Variação canônica do DS | Ação |
|---|---|---|---|
| [ex: tabela caseira] | [off-grid, hex hardcoded, estado vazio ausente] | [Data Table] | [Reestilizar / Trocar / Compor / ⚠️ Outro] |

> ⚠️ **Gate "Outro":** [componentes sem equivalente no catálogo — REQUER VALIDAÇÃO UX/PX antes de avançar]

## 6. Backlog de redesign priorizado (B6)

> Ordem por impacto × esforço. Cada item vira uma tela no `px-epic` (AS-IS → TO-BE).

| Ordem | Tela | AS-IS (o que é) | TO-BE (o que vira) | Tipo | Público |
|---|---|---|---|---|---|
| 1 | [tela] | [estado atual] | [estado alvo] | [quick win / reestruturação] | [público] |

## 7. Definition of Ready da auditoria (B7)

- [ ] Objetivo do redesign + critério de sucesso (B1)
- [ ] Inventário AS-IS, prioritárias marcadas (B2)
- [ ] Públicos + jornadas atuais (B3)
- [ ] Diagnóstico com achados + severidade (B4)
- [ ] Mapa de lacunas atual→DS, ação por componente (B5)
- [ ] Backlog priorizado, AS-IS→TO-BE (B6)
- [ ] Premissas registradas
- [ ] Perguntas em aberto com dono

## Premissas

- [decisões assumidas por default, revisáveis]

## Perguntas em aberto

- [pendências com dono — inclui acesso ao produto, se faltou percorrer]

## Encadeamento

- [ ] Produto sem identidade no DS → `px-kickoff` (personas + UI KIT)
- [ ] Identidade ok → `px-epic` (decompor o backlog de redesign)
- Cada tela → `px-request` → `px-story` → px-handoff → dev
