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
| Procedência da base | `procedencia.md` **na raiz** (commit/data do boilerplate, registry, versão das skills) | Diz sobre qual base o pacote foi construído — sem isso, divergência visual é indiagnosticável |
| Referência visual navegável | `prototipo/` — HTML unificado single-file (`#view-*`/`data-story`) **ou** build do protótipo | Referência de fidelidade (visual + comportamento) |
| UI Kit / tokens | `ui-kit.md`, tokens reais do projeto | Valores reais de identidade |
| Histórias de negócio | `stories/*.md` (CA + BDD + rastreabilidade) | **O contrato** do que fazer |
| Personas de usabilidade | `personas/personas.md` + `personas/<slug>.md` (persona como foi usada, com a customização de contexto declarada) | **Quem julgou a tela e com que régua.** Os critérios de usabilidade dos CA nasceram delas; sem isso o dev recebe a regra sem a razão, e permite revalidar com `ux-persona` depois de implementar |
| Flows de validação | `flows/<jornada>.md` (ponteiros reescritos pro pacote) | **A jornada multi-tela em ações de interface.** É o que o **Playwright do dev automatiza** e o que a persona percorre na revalidação. O BDD cobre um comportamento por tela; o flow cobre a travessia entre elas |
| Tours de onboarding | `tours/tours.md` (+ `tours/onboarding/` no caminho do fonte) | **Um tour por fluxo lógico e o global**, passos ancorados em `data-onb`, filtro por permissão em runtime. O dev pluga `can`, telemetria e persistência |
| Regras de negócio da entrega | `regras-negocio.md` **na raiz** (extraído dos requests, sanitizado, IDs `RN-<SIGLA>-<DOMÍNIO>-<NN>`) | A fonte das regras que os CA verificam |
| Specs referenciadas por uma história | `<spec>.md` no fluxo (ex.: spec de aba/componente) | Detalhe que a história cita e o dev precisa |
| Decisões de produto canônicas | `decisoes/*.md` (regras de fluxo, dados, dicionários de status/toasts) | Regras que o dev implementa |
| Mapa de permissões / triggers | `rbac-*.md` (quando o produto tem RBAC) | Checks a plugar |
| README do pacote | `README.md` | Como ver a referência visual e como está organizado |
| Fronteiras de integração | consolidadas no `handoff.md` | Onde acaba o mock, começa o real |

### 🔒 Interno (nunca entra)
| Categoria | Exemplo de artefato | Por quê |
|---|---|---|
| Checkpoint da cadeia PX | `PX-PROGRESS.md` | Estado de sessão, não contrato |
| Prompt de continuidade / contexto de chat | `PROMPT-CONTINUIDADE-*.md`, `contexto-*.md` | Instrução para o próximo chat |
| Discovery / auditoria | `audit/*.md`, `backlog-*.md` | Como chegamos aqui, não o quê construir |
| Relatório de walkthrough | `e2e/reports/*.md` (diário da persona + diagnóstico) | Material de diagnóstico. O que o dev consome é a **persona** (dev-facing, acima) e o critério que nasceu dela, já dentro da história. O diário bruto é como chegamos ao critério |
| Planejamento superado (como arquivo) | `epics/*.md`, `requests/*.md` | O arquivo fica de fora, mas seu **conteúdo essencial é extraído**: RNs → `regras-negocio.md`, specs referenciadas → `<spec>.md` no fluxo (sanitizados) |
| Memória do assistente + scratchpad | `~/.claude/...`, arquivos temporários | Nunca sai |
| Build compilado **dentro** de `handoff-ux/<label>/` | `dist/`, `standalone.html` misturados ao código | Dentro do pacote ele é lido como entrega, e foi assim que HTML virou referência de implementação. O bundle vai em `preview/<label>-proto.html`, **irmão** de `handoff-ux/`, com `preview/README.md` dizendo que é só referência visual e navegável (dev-facing, fora do pacote) |
| Config de build | `vite.config`, `tsconfig`, `package.json`, `.env` | Ambiente é do repo do dev |
| Biblioteca de componentes | `src/components/ui/**` | Vem do registry `@centralit` (privado, exige `CENTRALIT_TOKEN`), versionada — cópia no pacote duplica biblioteca. O `procedencia.md` declara se o proto usou o registry ou não |

> Alinhado ao GATE do `SKILL.md`. O pacote é **self-contained**: além de referência visual + UI Kit +
> stories, entram as **regras de negócio por fluxo** e as **specs referenciadas** (extraídas do interno e
> sanitizadas), o README, e — quando existirem — decisões canônicas e mapa de permissões. Nada no pacote
> aponta para caminho fora dele.

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
