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
| `../../preview/<label>-proto.html` | **Caminho do fonte:** referência visual e navegável, fora do pacote. Só para olhar e comparar; o código é `<produto>/` |
| `prototipo/` | **Caminho da referência visual (legado):** HTML unificado single-file **ou** build do protótipo (ver `README.md`) |
| `ui-kit.md` | Tokens de cor, tipografia, status e identidade do produto |

> Caminho do fonte: não há HTML nem build **dentro** do pacote; o preview fica em `preview/` na raiz da branch, com README dizendo que não é código. Legado: se o `prototipo/` é o build (não single-file), o HTML unificado com `data-story` fica como pendência (via `px-preview`). Registrar aqui.

## 2a. Forma do protótipo (verificada no repo do dev, nunca perguntada)

**Repo inspecionado:** `<URL · branch>` · **Data da inspeção:** `<AAAA-MM-DD>`

| Verificação | Achado |
|---|---|
| `package.json` (tailwind, primitiva, cva) | `<linhas coladas do grep, com o caminho do arquivo>` |
| Pasta `components/ui` do dev | `<caminho> · <N> componentes · faltam no dev: <lista> · faltam no sandbox: <lista>` |
| Alias de import da biblioteca no app de destino | `<@/ | @smart-gov/shared/ | …>` |
| CSS de tokens | `<arquivo global> (+ <tema por app>, se houver)` |

**Veredito:** `<FONTE (obrigatório) | Referência visual — Stack do dev verificada: sem shadcn>`
**Regra de tradução de import aplicada no pacote:** `<from "@/components/ui/" → from "<alias-dev>/components/ui/" | nenhuma, alias igual>`
**Primitiva:** `<Radix, igual à nossa | Base UI: ver props que mudam em pre-requisitos.md>`

## 3. Histórias, regras de negócio e specs (por fluxo)

<!-- O pacote é self-contained: cada fluxo leva sua história, suas RNs e as specs que a história referencia. -->

| Fluxo | História | RNs que usa | Specs referenciadas |
|---|---|---|---|
| `<fluxo-a>` | `stories/<historia>.md` | `RN-<SIGLA>-<DOMÍNIO>-01`, `…-04` | `<spec>.md` (se houver) |
| `<fluxo-b>` | `stories/<historia>.md` | `RN-<SIGLA>-<DOMÍNIO>-02` | — |

O BDD completo (feliz + vazio + erro + permissão) e os critérios de usabilidade estão nos arquivos `stories/`; as regras de negócio (RN) vivem num **único `regras-negocio.md` na raiz do pacote** — a coluna acima cita os IDs, não repete o enunciado.

## 4. Personas e flows de validação (quem julgou, e em que jornada)

<!-- Detalhe completo em personas/personas.md. Aqui fica só o resumo de uma linha por persona. -->

| Persona | Público real que representa | Jornada percorrida | Ajuste de contexto |
|---|---|---|---|
| `<slug>` | `<público>` | `flows/<jornada>.md` | `<o que mudou / usada sem ajuste>` |

Os **critérios de usabilidade** de cada história saíram destas rodadas. Ao mudar a tela na implementação, a régua é a persona, não a preferência de quem implementa. Para revalidar depois de pronto, ver `personas/personas.md`.

**Flows entregues** (`flows/`) — jornada multi-tela em ações de interface, com ponto de verificação por passo. É o artefato que o **Playwright automatiza**: o BDD cobre um comportamento por tela, o flow cobre a travessia entre elas.

| Jornada | Público | Telas na ordem | Observação |
|---|---|---|---|
| `flows/<jornada>.md` | `<público>` | `<tela 1>` → `<tela 2>` | `<passo N: tela não entregue nesta leva, se houver>` |

> Nenhuma persona rodou ou nenhum flow existe nesta leva: declarar aqui, com o motivo. Em branco é indistinguível de esquecimento.

**Tours de onboarding entregues** (`tours/`) — um tour acionável por fluxo lógico e o global que encadeia todos, montados em runtime pelas permissões do usuário. Detalhe em `tours/tours.md`.

| Guia | Telas na ordem | Passos (máx.) | Pendências de permissão |
|---|---|---|---|
| `<produto>-<fluxo>` | `<tela 1>` → `<tela 2>` | N | `<chave a confirmar | nenhuma>` |
| `<produto>-global` | fluxos `<f1>` → `<f2>` | soma | |

> Nenhum tour gerado nesta leva: declarar aqui, com o motivo.

## 5. Fronteiras de integração (mock → real)
- ⚑ **Boundary:** `<dependência>` — `<o que precisa ser substituído>`
- (ou) Nenhuma — opera sobre dados já mockados/carregados.

## 6. Definition of Done (resumo)
- Biblioteca de componentes: `<@centralit obrigatória | dev adapta à stack>`.
- Referência visual: `<preview/<label>-proto.html fora do pacote, com README (caminho do fonte) | HTML single-file com data-story | build em prototipo/ (single-file pendente)>`.
- Pacote self-contained: 0 referência a caminho externo; RNs e specs referenciadas incluídas.
- Personas e flows: `<P personas em personas/ e J jornadas em flows/ | nenhuma rodou nesta leva, motivo declarado>`.
- Tours: `<N tours de fluxo + global em tours/ | nenhum nesta leva, motivo declarado>`.

## Perguntas em aberto
- `<pendência>` — dono: `<nome>` · aguardando: `<o que falta>`
- (ou) Nenhuma.

<!-- Salvar em: handoff-ux/<label>/handoff.md -->
