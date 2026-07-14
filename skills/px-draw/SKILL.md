---
name: px-draw
description: Rascunho HTML descartável para exploração visual rápida em fases de discovery muito iniciais — quando o problema ainda é vago demais para entrar no boilerplate. HTML+CSS inline, sem React, sem tocar no index.css do produto. Ao fechar: ou descarta e vai para px-start (boilerplate), ou usa o rascunho como referência para px-request. Use quando quiser explorar uma ideia visualmente antes de saber se vale o esforço de boilerplate: "rascunhar uma ideia", "explorar visualmente", "ver como ficaria", "só pra ter uma noção", "discovery ainda muito vago".
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: draw
---

# px-draw — rascunho HTML descartável para discovery inicial

Esta skill produz um **rascunho visual de baixo esforço** para explorar ideias em fases de discovery muito iniciais. É descartável por design: não toca no boilerplate, não gera componentes React, não aplica tokens de identidade do produto. Quando o rascunho cumpre seu papel, o PX decide se joga fora e parte pro `px-start`, ou se usa como referência visual pro `px-request`.

**Público:** o líder UX/PX. Use quando o problema ainda é vago demais para justificar montar o boilerplate, mas você precisa de algo concreto para raciocinar ou apresentar.

**Quando NÃO usar:** se o problema já está definido e você sabe que vai construir uma tela real → vá direto pro `px-start` e `px-request`. O `px-draw` é exceção para discovery, não padrão de trabalho.

Contexto inicial via slash: `$ARGUMENTS` (ideia ou conceito a explorar). Se vazio, pergunte o que a pessoa quer visualizar.

## Princípios

- **HTML + CSS inline apenas.** Nenhum framework, nenhuma dependência, nenhum CDN de UI.
- **Fora do boilerplate.** O rascunho não vive em `src/`, não toca em `index.css`, não importa nada do projeto React.
- **Descartável por design.** Não é entrega — é ferramenta de raciocínio. Não precisa ser perfeito.
- **Sem identidade de marca.** Use cores neutras (cinzas, brancos, um acento simples) — sem tentar replicar o UI KIT do projeto. Identidade vem no `px-kickoff`.

## Passo 1 — Entender o que precisa ser explorado

Pergunte (ou infira de `$ARGUMENTS`):
- **O quê:** qual ideia, fluxo ou conceito precisa de forma visual?
- **Por quê:** o que essa exploração vai responder ou desbloquear?
- **Escopo:** uma tela? Um fluxo de 2-3 estados? Um componente isolado?

Eco antes de escrever: *"Vou rascunhar [X] — [N] estados/telas, HTML inline, sem identidade de marca, descartável. Confirma?"*

## Passo 2 — Produzir o rascunho

Gere um arquivo HTML único, autocontido, sem dependências externas:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rascunho — [nome da ideia]</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: system-ui, sans-serif; background: #f5f5f5; color: #1a1a1a; }
  </style>
</head>
<body>
  <!-- estrutura visual aqui -->
</body>
</html>
```

**Regras do rascunho:**
- Cores: neutros (`#f5f5f5`, `#e0e0e0`, `#666`, `#1a1a1a`) + um acento placeholder (`#3b82f6`). Nunca cores do UI KIT do projeto.
- Espaçamento em múltiplos de 8px (8, 16, 24, 32, 48px).
- Layout via flexbox ou grid — nunca float, nunca position para layout.
- Ícones como placeholder textual `[ícone]` — sem SVG externo, sem biblioteca.
- Sem JavaScript, a menos que seja indispensável para mostrar um estado de transição simples.
- Sem `text-transform: uppercase`, sem travessão (`—`/`–`), sem caixa alta completa em texto de interface.

## Passo 3 — Decidir o destino

Ao fechar o rascunho, apresente as duas saídas possíveis:

| Decisão | Quando | Próximo passo |
|---|---|---|
| **Descartar** | O rascunho clarificou o problema mas não serve de referência visual | `px-start` para começar no boilerplate |
| **Usar como referência** | O rascunho virou uma proposta de layout aprovada | `px-request` para especificar a tela real |

Registre a decisão no eco final e, se houver um `PX-PROGRESS.md` para esta iniciativa, atualize-o com o resultado da exploração.

## Eco final

*"Rascunho de [X] pronto — [N] estados explorados. Decisão: [descartar / usar como referência]. Próximo passo: [`px-start` / `px-request`] — confirma?"*

## Relação com o fluxo

```
problema muito vago  →  px-draw (rascunho descartável)
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
        descartou                    virou referência
               │                             │
          px-start                      px-request
    (começa no boilerplate)         (spec da tela real)
```

> `px-draw` vive **fora** da cadeia PX padrão — é uma válvula de exploração para discovery inicial. O fluxo normal começa no `px-start`. Use `px-draw` só quando o problema ainda é vago demais para justificar o boilerplate.
