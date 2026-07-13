# Handoff → dev: <funcionalidade>

**Funcionalidade/fluxo:** `<funcionalidade>` · **Branch:** `ux/<funcionalidade>`
**Sprint:** `Sprint NN · <AAAA-Www>` · **Data:** `<AAAA-MM-DD>`
**Origem:** `planning/<funcionalidade>/` (px-request → px-story)

## 1. Escopo desta entrega
| História | Tela | Status | Entra nesta leva? |
|---|---|---|---|
| `<ID>` | `<slug>` | ✅ ready | Sim |

**Fica pra próxima leva (e por quê):**
-

## 2. Definition of Done (régua de "entregue")
- [ ] Telas seguem o UI KIT (tokens, sem hex/radius solto, grid de 8px)
- [ ] Todos os estados por tela (default/loading/empty/error/disabled/read-only/hover/foco/responsivo)
- [ ] Todos os breakpoints (Mobile/Tablet/Desktop/Widescreen)
- [ ] Validação visual via Playwright — meta de 99% de fidelidade, evidências no MR
- [ ] Cenários BDD passam (feliz + vazio + erro + permissão + 1 regra de negócio)
- [ ] DoD específico da funcionalidade: `<se houver>`

## 3. Validação pelo usuário (flows + personas)
| História | Flow (ux-flows) | Persona(s) (ux-persona) |
|---|---|---|
| `<ID>` | `e2e/flows/<id>.md` | `<persona por público>` |

> Validar **pela interface** (clicar/preencher), nunca por rota interna.

## 4. Fronteiras de integração (mock → real)
- ⚑ **Boundary:** `<dependência>` — `<o que precisa ser substituído>`
- (ou) Nenhuma — opera sobre dados já mockados/carregados.

## 5. Rastreabilidade
- **Histórias:** `planning/<funcionalidade>/stories/*.md`
- **Specs:** `planning/<funcionalidade>/requests/*.md`
- **Público-alvo:** `planning/<funcionalidade>/publico-alvo.md`
- **UI KIT:** `planning/<funcionalidade>/ui-kit.md`
- **Checkpoint:** `planning/<funcionalidade>/PX-PROGRESS.md`

## 6. Despacho da entrega
- [ ] `PX-PROGRESS.md` atualizado (histórias entregues, campo `Sprint`, próximo passo)
- [ ] Entrega git despachada pra `px-setup` Passo 4 — MR `[Sprint NN] ux(<funcionalidade>): <resumo>` (`ux/<funcionalidade>` → `main`), corpo = este documento

## Perguntas em aberto
- `<pendência>` — dono: `<nome>`  (ou "nenhuma")

<!-- Salvar em: planning/<funcionalidade>/handoff.md -->
