# Especificação de Histórias — [Nome do Módulo]

> [Descrição de escopo em 2–3 linhas: o que este módulo cobre.]
> Referência: `planning/<iniciativa>/epics/NN-<epico>/00-overview.md` (e levantamento original, se houver).
>
> Versão 1.0 · [data]

---

## CONTEÚDO

**Implementado**
- [ID — Título](#id--titulo)

**Planejado**
- [ID — Título](#id--titulo)

**Boundary / Faltando entendimento**
- [ID — Título](#id--titulo)

---

## [ID] — [Título]

**Módulo:** [Produto] · `[módulo]` · [Contexto/tela]
**Papel:** [papel do usuário]
**Status:** [✅ Implementado · vX.Y | 🔜 Planejado | 🔶 Boundary | ⚠️ Faltando entendimento]

### História de Usuário

Como [papel], quero [ação], para [benefício].

### Critérios de Aceite

- [CA 1]
- [CA 2]

### Regras de Negócio (se houver)

- **RN-[SIGLA]-[DOMÍNIO]-001** [regra]

### Estados de UI

`default` · `loading` · `vazio` · `erro`

### Cenários BDD

**[Nome do cenário — happy path]**
- Dado [contexto]
- Quando [ação]
- Então [resultado]

**[Nome do cenário — exceção]**
- Dado [contexto]
- Quando [ação]
- Então [resultado]

### Nota de UX/PX (se houver)

[texto]

### Fronteiras de Integração

Nenhuma — opera sobre dados já mockados/carregados.
<!-- ou: > ⚑ **Boundary:** [o que precisa ser substituído por API/low-code/terceiro] -->

<!-- Nota de implementação (detalhe técnico não-visível), se houver: -->
> [nota]

---

<!-- Salvar em: planning/<iniciativa>/spec/<modulo>.md — um arquivo por módulo principal -->
