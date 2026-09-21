---
iniciativa: <iniciativa>
produto: <slug-do-produto>
leva: <label do handoff | em andamento>
alvo_de_build: <App React | Protótipo HTML>
componente: Onboarding Guiado (ds-components_v4.md) · src/components/ui/onboarding/
atualizado: <AAAA-MM-DD>
---

# Onboarding guiado — <iniciativa>

> Spec legível dos tours. O código canônico (alvo App React) vive em `src/onboarding/`;
> este arquivo é o que o dev lê primeiro e o que a `px-handoff` copia para `tours/`.
> Um tour por fluxo lógico (= um flow do `ux-flows`) e um tour global que encadeia todos,
> montados em runtime pelas permissões do usuário. Nunca tour por perfil.

## Guias

| Guia | `id` | `versao` | Telas na ordem | Gatilho | Disparo automático | Passos (máx. após filtro) |
|---|---|---|---|---|---|---|
| Fluxo `<fluxo-slug>` | `<produto>-<fluxo-slug>` | 1 | `<tela A>` → `<tela B>` | `Onboarding.Ajuda` ao lado do título de `<tela A>` | `<sim | não>` | N |
| Global | `<produto>-global` | 1 | fluxos na ordem: `<f1>` → `<f2>` (tela repetida entra uma vez) | Menu de ajuda do shell | nunca | soma |

**Ordem do global:** herdada da jornada do público em `px-epic` B2 / coluna de ordem do `mapa-de-telas.md`. Segue direto de um fluxo para o outro, sem pausa.

## Passos por tela

<!-- Repetir o bloco por tela. A tela é escrita uma vez e serve ao tour do fluxo e ao global. -->

### `<tela-slug>` · história `<ID-ESTÁVEL>` · rota `<rota>` · arquivo `<src/…>`

| # | Âncora `data-onb` | Tipo | `title` | `content` | `data` | Permissão | Evidência |
|---|---|---|---|---|---|---|---|
| 1 | `<id-historia>-<acao>` | explicativo | `<até 40 chars>` | `<1 a 2 frases, verbo = rótulo B8>` | `rolar` | `<recurso.acao>` ou vazio | `fricção Descoberta: <relatório>` ou `ação principal (B5)` |
| 2 | `<id-historia>-<acao>` | ação | … | … | `acao: "<rotulo>"`, `avancarQuandoAparecer: "[data-onb=…]"` | … | … |
| 3 | `<id-historia>-<acao>` | explicativo | … | … | `aguardarAlvo` (interior de gaveta) | … | … |

- **Modal de entrada:** `titulo` = `<nome do fluxo>`; `descricao` = `<narrativa S1 em segunda pessoa>`; tópicos = `<um por tela>`.
- **Continuação:** o passo N navega para `<tela B>` (passo de ação); a origem marca a continuação, o destino consome com `emCurso: true`.
- **Estado devolvido ao concluir:** `<gaveta fechada | aba original | nada a devolver>`.

## Permissões

Convenção `<recurso>.<ação>` (modelo agnóstico de permissões). Fonte por passo: `rbac-<fluxo>.md` › linha; história S6; request B5.

| Chave | Passos que dependem dela | Fonte | Status |
|---|---|---|---|
| `<recurso>.visualizar` | `<tela>#1, #2` | `rbac-<fluxo>.md` L<nn> | ok |
| `<recurso>.gerenciar` | `<tela>#3` | request B5 (Premissa) | **pendência: confirmar chave com o dev** |

- Piso em runtime: fluxo com menos de 3 passos após o filtro fica sem gatilho próprio; passos seguem no global.
- `can(chave)` é a função de autorização do produto. ⚑ **INTEGRATION BOUNDARY.**

## Decisões do UX responsável

| Decisão | Escolha | Origem |
|---|---|---|
| Mobile | `<âncoras nos dois layouts | passos vazios abaixo do breakpoint>` | `<confirmado por <líder> em <data> | Premissa>` |
| Disparo automático do tour de fluxo | `<sim | só gatilho>` | público `<leigo | especialista>` (B2) |
| Pesquisa de satisfação | `<ativa | desligada>` | |
| Gatilho do global | menu de ajuda do shell | decisão Central |

## Divergências declaradas do design system

| Onde | Spec diz | Fizemos | Motivo |
|---|---|---|---|
| Gatilho do global | bússola ao lado do título da seção | `Onboarding.Ajuda` no menu de ajuda do shell | o global não pertence a uma seção |

## Fronteiras de integração

- ⚑ `can(chave)`: autorização real do produto (hoje: mock em `src/onboarding/use-guia-da-tela.ts`).
- ⚑ `onEvento`: telemetria dos 8 eventos e resposta da pesquisa (hoje: `console.info`).
- ⚑ Persistência: `localStorage` com prefixo `centralit` (default). Trocar o adapter para estado no servidor, se o produto exigir.

## Verificação

- Âncoras sem alvo no fonte: `<0 | lista>`.
- Typecheck, `lint:travessao`, `lint:caixa-alta`: `<verde | saída>`.
- Tour rodado no navegador em `<data>`: fluxo(s) `<…>` e global.
- `ux-persona` novato com o tour ativo: `<relatório | não rodou, motivo>`.

## Pendências

- `<pendência>` — dono: `<nome>` (ou "nenhuma")
