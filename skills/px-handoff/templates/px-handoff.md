# Handoff → dev: <funcionalidade>

**Funcionalidade/fluxo:** `<funcionalidade>`
**Sprint:** `Sprint NN · <AAAA-Www>` · **Data:** `<AAAA-MM-DD>`

## 1. Escopo desta entrega
| História | Tela | Status | Entra nesta leva? |
|---|---|---|---|
| `<ID>` | `<slug>` | ✅ ready | Sim |

**Fica pra próxima leva (e por quê):**
-

## 2. Protótipo visual e UI Kit

| Arquivo | O que cobre |
|---|---|
| `<funcionalidade>.html` | `<telas/fluxos incluídos>` |
| `planning/<funcionalidade>/ui-kit.md` | Tokens de cor, tipografia e identidade deste produto |

> O HTML é a **referência visual e de comportamento**. O UI Kit define quais tokens aplicar (cores de marca, primária, etc.). Implementar usando a biblioteca `@centralit` — os componentes já carregam radius e espaçamento corretos; o UI Kit define os valores de cor.

## 3. Histórias de negócio

> Mesmas histórias do Agility. Uma seção por história.

### `<ID>` — <título da história>

**Como** `<persona>`, **quero** `<ação>` **para** `<objetivo>`.

**Critérios de aceite (BDD):**
```
Dado <contexto>
Quando <ação>
Então <resultado esperado>
```

**Regras de negócio:**
- `<regra>`

**Rastreabilidade na tela:** `<descrição do elemento — ex: "Botão 'Confirmar exclusão' no modal de exclusão de registro">` · anchor: `data-story="<ID>"`

---
<!-- repetir bloco acima para cada história desta leva -->

## 4. Fronteiras de integração (mock → real)
- ⚑ **Boundary:** `<dependência>` — `<o que precisa ser substituído>`
- (ou) Nenhuma — opera sobre dados já mockados/carregados.

## Perguntas em aberto
- `<pendência>` — dono: `<nome>` · aguardando: `<o que falta para resolver>`
- (ou) Nenhuma.

<!-- Salvar em: planning/<funcionalidade>/handoff.md -->
