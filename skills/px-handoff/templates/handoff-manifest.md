# Handoff Manifest — recorte dev-facing vs. interno

> **Template reutilizável da `px-handoff`.** Copie para a pasta de planejamento da iniciativa
> (`planning/<iniciativa>/HANDOFF-MANIFEST.md`) e preencha a seção "Instância do projeto".
> Serve para que qualquer UX defina, no mesmo formato, o que entra no pacote do dev e o que
> fica como contexto interno — antes de rodar o BLOCO 6 da `px-handoff`.

## Por que existe

A cadeia PX gera dois tipos de artefato: os que o **dev consome** (contrato + referência) e os que
são **contexto de sessão** (para retomar o trabalho em outro chat). Misturar os dois no pacote vaza
ruído interno pro dev e infla a entrega. Este manifesto fixa o recorte, de forma auditável.

## Regra de bolso

> **Entra no pacote** o que o dev precisa para **implementar e validar** a tela na stack do projeto.
> **Fica de fora** o que só serve para **conduzir o trabalho de PX** (discovery, planejamento, continuidade de chat).
> Na dúvida: se o artefato descreve *o que construir / como deve se comportar / como deve parecer*, é dev-facing.
> Se descreve *como chegamos até aqui* ou *o que fazer no próximo chat*, é interno.

## Categorias — genéricas (valem para qualquer iniciativa)

### ✅ Dev-facing (entra no pacote)
| Categoria | Exemplo de artefato | Papel |
|---|---|---|
| Protótipo HTML unificado | `<Produto>-Prototipo.html` (âncoras `#view-*`) | Referência de fidelidade (visual + comportamento) |
| UI Kit / tokens | `ui-kit.md`, tokens do projeto | Valores reais de identidade |
| Histórias de negócio | `stories/*.md` (CA + BDD + rastreabilidade) | **O contrato** do que fazer |
| Decisões de produto canônicas | `decisoes/*.md` (regras de fluxo, dados, dicionários de status/toasts) | Regras que o dev implementa |
| Mapa de permissões / triggers | `rbac-*.md` (quando o produto tem RBAC) | Checks a plugar |
| Fronteiras de integração | consolidadas no `handoff.md` | Onde acaba o mock, começa o real |

### 🔒 Interno (nunca entra)
| Categoria | Exemplo de artefato | Por quê |
|---|---|---|
| Checkpoint da cadeia PX | `PX-PROGRESS.md` | Estado de sessão, não contrato |
| Prompt de continuidade / contexto de chat | `PROMPT-CONTINUIDADE-*.md`, `contexto-*.md` | Instrução para o próximo chat |
| Discovery / auditoria | `audit/*.md`, `backlog-*.md` | Como chegamos aqui, não o quê construir |
| Planejamento superado | `epics/*.md`, `requests/*.md` | Consolidado pelas stories (request = referência opcional de profundidade) |
| Memória do assistente + scratchpad | `~/.claude/...`, arquivos temporários | Nunca sai |
| Código-fonte e config | `.tsx/.ts/.js` de componente, `vite.config`, `package.json`, `.env` | O dev implementa na própria stack |

> Alinhado ao GATE "O que nunca deve sair" do `SKILL.md`. Este manifesto **expande** o contrato:
> além de HTML + UI Kit + stories, decisões canônicas e mapa de permissões também são dev-facing
> quando existirem.

---

## Instância do projeto — PREENCHER

**Iniciativa:** `<slug>`
**Data:** `<AAAA-MM-DD>`

### Entra no pacote
| Arquivo | Categoria |
|---|---|
| `<caminho>` | `<categoria>` |

### Fica de fora (interno)
| Arquivo | Motivo |
|---|---|
| `<caminho>` | `<categoria>` |

### Casos de borda (decisão explícita)
| Arquivo | Decisão | Justificativa |
|---|---|---|
| `<caminho>` | incluir / não incluir | `<motivo>` |
