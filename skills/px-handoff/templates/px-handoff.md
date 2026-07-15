# Handoff → dev: semana-<NN>

**Semana:** `semana-<NN> · <AAAA-Www>` · **Data:** `<AAAA-MM-DD>`

## 1. Escopo desta entrega

| Fluxo | História | Tela | Entra nesta leva? |
|---|---|---|---|
| `<fluxo-a>` | `<ID>` | `<slug>` | Sim |
| `<fluxo-b>` | `<ID>` | `<slug>` | Sim |

**Fica pra próxima leva (e por quê):**
-

## 2. Protótipo visual e UI Kit

| Arquivo | O que cobre |
|---|---|
| `<Produto>-Prototipo.html` | Todos os fluxos desta leva |
| `ui-kit.md` | Tokens de cor, tipografia e identidade deste produto |

> O HTML é a **referência visual e de comportamento**. O UI Kit define quais tokens aplicar.

## 3. Histórias de negócio

<!-- Uma seção por fluxo. Dentro de cada fluxo, uma subseção por história. -->

### Fluxo: `<fluxo-a>`

#### `<ID>` — <título da história>

**Como** `<persona>`, **quero** `<ação>` **para** `<objetivo>`.

**Critérios de aceite (BDD):**
```
Dado <contexto>
Quando <ação>
Então <resultado esperado>
```

**Regras de negócio:**
- `<regra>`

**Rastreabilidade na tela:** `<descrição do elemento>` · anchor: `data-story="<ID>"`

---
<!-- repetir bloco de história para cada história do fluxo -->
<!-- repetir bloco de fluxo para cada fluxo desta leva -->

## 4. Fronteiras de integração (mock → real)
- ⚑ **Boundary:** `<dependência>` — `<o que precisa ser substituído>`
- (ou) Nenhuma — opera sobre dados já mockados/carregados.

## Perguntas em aberto
- `<pendência>` — dono: `<nome>` · aguardando: `<o que falta para resolver>`
- (ou) Nenhuma.

<!-- Salvar em: ux/semana-<NN>/handoff.md -->
