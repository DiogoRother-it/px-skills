# Relatório ux-persona — <flow-slug> × <persona-slug>

**Flow:** `e2e/flows/<flow-slug>.md`
**Persona:** `e2e/personas/<persona-slug>.md` (ou bundled `templates/persona-<slug>.md`)
**Alvo navegado:** <repo local `npm run dev` / URL> — <observação sobre autenticação/ambiente, se relevante>
**Data:** <data>

---

## Parte 1 — Diário da persona (Fase 1, subagente isolado)

> Primeira pessoa, sem conhecimento do design system nem do "resultado esperado". Um bloco por passo do flow.

### Passo 1 — <descrição do passo, herdada do flow>
- **O que vi:** <só o que estava de fato na tela>
- **O que tentei:** <ação concreta>
- **Senti:** <no vocabulário do persona>
- **Travou?** Sim/Não — <se sim, o que tentou em seguida>
- **Screenshot/evidência:** <referência>

### Passo 2 — <descrição do passo>
- **O que vi:**
- **O que tentei:**
- **Senti:**
- **Travou?**
- **Screenshot/evidência:**

<!-- repetir um bloco por passo do flow -->

---

## Parte 2 — Diagnóstico UX (Fase 2, você com o contexto completo)

> Cada trava/fricção relatada na Parte 1 vira uma linha. Nunca lance achado sobre o que a persona não observou ou não tentou.

| # | Passo | Achado (observável) | Dimensão | Severidade | Proposta (ancorada no DS) |
|---|---|---|---|---|---|
| 1 | Passo 1 | | Descoberta / Clareza / Feedback / Fricção / Sem beco sem saída / Fidelidade / Autenticidade de dados | Crítico/Alto/Médio/Baixo | |

## Fechamento

- **Achados críticos/altos:** <N>
- **Achados sem componente do catálogo que resolva:** <marcar ⚠️ REQUER VALIDAÇÃO UX/PX, se houver>
- **Próximo passo recomendado:** `px-change` (ajuste pontual) · `px-request` (repensar a tela) · `px-epic`/`px-audit` (backlog, se for parte de uma auditoria)
