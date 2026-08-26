# Handoff → dev: <label>

**Rótulo:** `<label>` (`semana-<NN> · <AAAA-Www>` ou `v<N>`) · **Data:** `<AAAA-MM-DD>` · **Repositório:** `<caminho/URL do repo do dev | sem repo oficial ainda — organizado localmente, push pendente>`

## 1. Escopo desta entrega

| Fluxo | História | Rota / referência | Entra? |
|---|---|---|---|
| `<fluxo-a>` | `<título>` | `<rota do proto>` | Sim |
| `<fluxo-b>` | `<título>` | `<rota do proto>` | Sim |

**Fica pra próxima leva (e por quê):**
-

## 2. Referência visual e UI Kit

| Arquivo | O que cobre |
|---|---|
| `prototipo/` | Referência visual navegável — HTML unificado single-file **ou** build do protótipo (ver `README.md`) |
| `ui-kit.md` | Tokens de cor, tipografia, status e identidade do produto |

> Se o `prototipo/` é o build (não single-file), o **HTML unificado com `data-story`** fica como pendência (via `px-preview`). Registrar aqui.

## 3. Histórias, regras de negócio e specs (por fluxo)

<!-- O pacote é self-contained: cada fluxo leva sua história, suas RNs e as specs que a história referencia. -->

| Fluxo | História | RNs que usa | Specs referenciadas |
|---|---|---|---|
| `<fluxo-a>` | `stories/<historia>.md` | `RN-<SIGLA>-<DOMÍNIO>-01`, `…-04` | `<spec>.md` (se houver) |
| `<fluxo-b>` | `stories/<historia>.md` | `RN-<SIGLA>-<DOMÍNIO>-02` | — |

O BDD completo (feliz + vazio + erro + permissão) e os critérios de usabilidade estão nos arquivos `stories/`; as regras de negócio (RN) vivem num **único `regras-negocio.md` na raiz do pacote** — a coluna acima cita os IDs, não repete o enunciado.

## 4. Fronteiras de integração (mock → real)
- ⚑ **Boundary:** `<dependência>` — `<o que precisa ser substituído>`
- (ou) Nenhuma — opera sobre dados já mockados/carregados.

## 5. Definition of Done (resumo)
- Biblioteca de componentes: `<@centralit obrigatória | dev adapta à stack>`.
- Referência visual: `<HTML single-file com data-story | build em prototipo/ (single-file pendente)>`.
- Pacote self-contained: 0 referência a caminho externo; RNs e specs referenciadas incluídas.

## Perguntas em aberto
- `<pendência>` — dono: `<nome>` · aguardando: `<o que falta>`
- (ou) Nenhuma.

<!-- Salvar em: handoff-ux/<label>/handoff.md -->
