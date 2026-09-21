---
name: px-tour
description: Gera o onboarding guiado de um fluxo lógico ao fechar a cadeia PX, sobre o componente Onboarding Guiado do design system — um tour acionável por fluxo (ex. "Novo contrato", "Visualizar contrato") e um tour global que encadeia todos, montados em runtime pelas permissões do usuário (RBAC granular). Não é entrevista: compila os passos de artefatos já prontos (flow do ux-flows, px-story, px-request, mapa de telas, relatórios do ux-persona) e só pede confirmação. Use quando o líder disser "gera o tour", "cria o onboarding desse fluxo", "quero o guia dessa jornada", "monta o tour global", ou quando ux-flows/px-story/px-handoff oferecerem o onboarding. Posição: depois da última px-story do fluxo e do ux-flows, antes da px-handoff.
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: tour
---

# px-tour — onboarding guiado por fluxo lógico

Um **tour** aqui é o guia do componente **Onboarding Guiado** (`ds-components_v4.md` → Onboarding Guiado; anatomia em `src/components/ui/onboarding/`, que é a spec do que já vem pronto): bússola ao lado do título da seção, modal de boas vindas, passos ancorados em elementos reais da tela e pesquisa de satisfação ao concluir. Esta skill **não desenha o componente**: escreve os passos, as âncoras e a fiação que o produto precisa para o guia rodar.

A unidade é o **fluxo lógico**, que na cadeia PX já existe com nome: é a **jornada registrada pelo `ux-flows`** (`e2e/flows/<slug>.md`) e o valor da coluna `Fluxo` do `mapa-de-telas.md`. Um flow, um tour acionável. Por cima, um **tour global** encadeia os fluxos na ordem da jornada do público e segue direto de um para o outro, sem pausa.

Como o `ux-flows`, isto **não é entrevista pesada**. Os passos são compilados de artefatos que já existem; a IA monta, mostra, o líder confirma. Toda pergunta nova ao líder é uma fonte de erro que um artefato anterior já respondeu.

Contexto inicial via slash: `$ARGUMENTS` (slug do flow, nome do fluxo lógico, ou "global").

## Regras (inegociáveis)

1. **Derivado, não inventado.** Passo, âncora, copy, rota e permissão vêm de artefato. Fonte ausente **degrada de forma declarada** (tabela do Passo 0), nunca em silêncio e nunca "porque faz sentido".
2. **Um flow, um tour.** O global é a **concatenação por referência** dos passos dos fluxos: cada passo é escrito uma vez, em `passos/<tela>.ts`, e serve às duas jornadas. Tela repetida entre fluxos entra no global **uma vez**, na primeira ocorrência.
3. **Passo por evidência, não por tela.** Cada passo aponta para uma **fricção de Descoberta** registrada pelo `ux-persona` ou para a **ação principal** da jornada. "Um passo por tela porque toda tela merece" produz ruído e o usuário pula. Entre 3 e 7 passos por fluxo; fluxo com menos de 3 passos (depois do filtro de permissão) **não ganha gatilho próprio**, só entra no global.
4. **Permissão em runtime, nunca tour por perfil.** RBAC granular gera perfis compostos que não existem quando o tour é escrito. Cada passo carrega a chave de permissão da ação que ensina (`<recurso>.<ação>`); os passos de cada tela são uma **função de `can`**, e o total da jornada é somado **depois** do filtro. Nunca escreva um tour para "o perfil X".
5. **Âncora no invólucro visível, nunca no controle nativo.** Convenção `[data-onb="<id>"]`, id em kebab-case derivado do ID estável da história: `<id-da-historia>-<acao>` (ex. `vit-lista-filtrar`). Componente composto (Input com ícone, Select, Combobox) repassa `data-*` ao elemento interno e o recorte abraçaria só ele: envolva num `<div data-onb>` do tamanho do controle.
6. **Regras de autoria da spec valem como trava.** Nunca ancorar em elemento mais alto que a janela; alvo condicional não vira passo (o que ele ensinaria entra no passo do campo que decide se ele aparece); rolar é decisão do guia inteiro; passo de ação perto da borda de baixo tem `placement` explícito; tela de escrita não pede clique que deixe alteração pendente; passo final que dispara ação **descreve**, não pede o clique; array vazio é a forma correta de dizer "nada a ensinar".
7. **Copy do passo é copy de UI.** Título curto, `content` em uma ou duas frases, verbo igual ao rótulo literal do botão (B8 do request). Sem travessão, sem caixa alta total. Rodar `lint:travessao` e `lint:caixa-alta` antes de aprovar.
8. **Nada aprovado no papel.** O tour roda no proto ou no app antes de fechar, e o `ux-persona` novato percorre a jornada **com o tour ativo**. Se a persona ainda trava em Descoberta com o guia ligado, o passo está errado.

## Prompting

Decisões enumeráveis (quais fluxos entram, ordem do global, mobile, disparo automático, pesquisa) → pergunta estruturada (`AskUserQuestion`), 2–4 opções, recomendada marcada. Valores livres (id do guia, copy) → propostos prontos, o líder ajusta. No-pause mode → cada pergunta vira Premissa com a recomendação de maior confiança.

---

## Passo 0 — Ingerir as fontes (gate)

Leia, nesta ordem, e ecoe o que herdou antes de qualquer proposta:

| Fonte | Caminho | O que sai dela |
|---|---|---|
| Flow da jornada | `e2e/flows/<slug>.md` | ordem das telas, passos em ações de interface, público, ponto de verificação por passo |
| Histórias das telas | `planning/<ini>/stories/<slug>.md` | **ID estável** (cabeçalho), arquivo da UI, S4b passo a passo, regras de visibilidade condicional (com ID), RBAC (triggers) em S6 |
| Requests das telas | `planning/<ini>/requests/<slug>.md` | B1 propósito (o **porquê** que vira `content`), B3 **rota**, B5 ações + chave de permissão + **candidatas a âncora**, B6 variação (tela, gaveta, aba), B7 estados (o que existe só com dado), B8 copy literal |
| Mapa de telas | `handoff-ux/<label>/mapa-de-telas.md` ou o rascunho da iniciativa | rota e ordem de implementação, quando o request não trouxer a rota |
| Relatórios de persona | `e2e/reports/<flow>__<persona>.md` | fricções na dimensão **Descoberta**: onde a persona não achou algo. São os passos de maior valor |
| Público-alvo | `planning/<ini>/publico-alvo.md` | familiaridade (leigo ↔ especialista): decide disparo automático ou só gatilho |
| Mapa de permissões | `planning/<ini>/rbac-*.md` | chave canônica `<recurso>.<ação>` por trigger, quando o produto tem RBAC mapeado |
| Alvo de build | `PX-PROGRESS.md` (campo **Alvo de build**) | App React → gera código; Protótipo HTML → gera **só a spec** (`tours.md`) |

**Degradação declarada (nunca silenciosa):**

| Falta | Faça |
|---|---|
| Flow | Não descreva a jornada aqui. Chame `ux-flows` (modo compilar) e volte |
| Relatório de persona | Passos pela ação principal de cada tela; marque cada um como **Premissa: sem evidência de Descoberta** |
| Rota (B3 e mapa) | Pergunte uma vez, registre no request; sem resposta vira **pendência com dono** |
| Chave de permissão (`rbac-*.md`, S6, B5) | Passo sem `permission`, marcado **Pendência: chave de permissão a definir pelo dev** em `pre-requisitos.md` |
| Proto aprovado ou fonte com `data-onb` | Liste as âncoras que faltam como diff para o `px-proto`/dev; não aprove o tour sem alvo |
| História de alguma tela do flow | Tela não entregue nesta leva: **marque** o passo, não o remova (mesma regra do `flows/`) |

**Eco do Passo 0:** "Vou partir disto: fluxo **X** com telas A → B → C (flow `slug`), públicos P, N fricções de Descoberta registradas, rotas conhecidas para A e B, permissões mapeadas em `rbac-<x>.md`, alvo de build App React — certo?"

## Passo 1 — Inventário de fluxos e ordem do global

1. Liste os flows da iniciativa em `e2e/flows/`. Cada um é um tour candidato.
2. Para cada flow, monte a tabela **tela → ID da história → rota → arquivo da UI → primeira tela do fluxo (gatilho)**.
3. **Pergunte (estruturada):** "Quais fluxos entram nesta leva de onboarding?" (opções = os flows; múltiplos).
4. **Ordem do global:** proponha a ordem da jornada do público no `px-epic` B2 (a mesma da coluna de ordem do `mapa-de-telas.md`) e confirme. Não é a ordem alfabética nem a de implementação.
5. **Global por conjunto de permissões, nunca por perfil:** o global é um só, filtrado em runtime. Se as jornadas de dois públicos não compartilham nenhuma tela, proponha dois globais (um por público) e registre a decisão.

## Passo 2 — Seleção dos passos por tela

Para cada tela do flow, na ordem da jornada:

1. **Candidatas** = ação principal (B5), pontos de entrada da tela (B3: menu, filtro, busca) e toda fricção de **Descoberta** do relatório de persona que aponta para um elemento desta tela.
2. **Ranqueie:** fricção registrada primeiro, ação principal em seguida, o resto fica de fora. Aplique o teto de 7 por fluxo.
3. **Trave pela spec:**
   - alvo que só existe **com dado** (linha da tabela, card de resultado) → ancore no contêiner ou no estado vazio (B7), nunca na primeira linha. O tour de primeiro acesso roda sem dado;
   - alvo **condicional** (só aparece com certo valor ou permissão) → não vira passo; o que ele ensinaria vai no passo do campo que decide;
   - alvo **dentro de gaveta, modal ou aba** (B6) → passo de **ação** no gatilho (`data.acao`, ensina onde clicar) seguido, se necessário, de passo no interior com `data.aguardarAlvo: true`. A tela segura o fechamento da gaveta enquanto `controle.ativo` e devolve o estado ao concluir. Nunca passo no interior sem o passo de ação antes;
   - **tela de escrita** (formulário) → passos explicativos; nenhum passo pede clique que deixe alteração pendente; o passo final que salvaria **descreve** o botão;
   - passo que **navega para outra tela** (último da tela, dentro da jornada) → passo de ação; a origem chama `marcarContinuacaoOnboarding` antes de navegar e o destino consome com `emCurso: true` (Passo 6);
   - `variant`: alvo em navbar/sidebar não rola; alvo no corpo com a página rolável → `data.rolar: true` em **todos** os passos ancorados daquela página, ou em nenhum.
4. **Eco por tela:** tabela `# | âncora (data-onb) | tipo (explicativo/ação) | evidência (fricção X / ação principal) | permissão | observação`. O líder confirma antes da próxima tela.

## Passo 3 — Copy dos passos

- `title`: nome da ação ou do elemento, como a tela o chama (B8). Até 40 caracteres.
- `content`: o **porquê** (B1: que trabalho a pessoa vem fazer) em uma ou duas frases, citando o rótulo literal do botão. Nunca "clique aqui para clicar".
- `data.dica`: só para informação secundária real (atalho, limite, regra de negócio com ID em B9). Sem dica é o default.
- Modal de entrada (`Onboarding.Intro`): `titulo` = nome do fluxo; `descricao` = narrativa S1 da primeira história ("Como…, quero…, para…") reescrita em segunda pessoa; `Topicos` = um item por tela do fluxo.
- Proibições duras: travessão (`—`, `–`) e caixa alta total. Rode `npm run lint:travessao` e `npm run lint:caixa-alta` sobre os arquivos gerados.

## Passo 4 — Permissões

1. Para cada passo, a chave da ação que ele ensina, na convenção `<recurso>.<ação>` do modelo agnóstico de permissões (`visualizar` base; `gerenciar` pressupõe `visualizar`; ação sensível nomeada pressupõe `gerenciar`). Fonte, nesta ordem: linha do `rbac-*.md` → campo RBAC (triggers) da história (S6) → B5 do request → pendência.
2. Passo explicativo de elemento sempre visível → sem `permission`.
3. Os passos da tela viram `(can) => PassoOnboarding[]`. O `total` da jornada é calculado na **primeira tela**, somando os passos filtrados de todas as telas do guia.
4. **Piso em runtime:** guia de fluxo com menos de 3 passos após o filtro → `passos: []` na primeira tela (desliga chamariz e disparo automático); os passos continuam no global.
5. `can` é **fronteira de integração** (a função de autorização do produto). Marque `// INTEGRATION BOUNDARY:` e registre no handoff.

## Passo 5 — Decisões do UX responsável (estruturadas)

- **Mobile:** "As âncoras existem no layout mobile deste produto?" → *Sim, ancorar nos dois layouts* · *Não, passos vazios abaixo do breakpoint (Recomendado quando o produto é consulta no mobile)*. Sidebar vira Sheet no mobile: passo tipo "aba" precisa de âncora no Sheet, ou some.
- **Disparo automático do tour de fluxo na primeira tela:** *Sim (Recomendado para público leigo em B2)* · *Só pelo gatilho*. O global **nunca** dispara sozinho.
- **Pesquisa de satisfação ao concluir:** *Ativa (default do componente)* · *Desligada*. A resposta sai por `onEvento`, fronteira de integração.
- **Gatilho do global:** decisão já tomada pela Central: `Onboarding.Ajuda` no **menu de ajuda do shell** (navbar/sidebar). É divergência declarada do DS (a spec coloca a bússola ao lado do título da seção): registre em `tours.md` › Divergências, com o motivo "o global não tem seção".

No-pause mode: cada uma vira Premissa com a opção recomendada.

## Passo 6 — Gerar os arquivos

Só no alvo **App React**. No alvo **Protótipo HTML**, gere apenas `tours.md` (spec) e as âncoras como lista para o `px-proto`.

```
src/onboarding/
├── passos/<tela-slug>.ts        # (can) => PassoOnboarding[]  ← única fonte por tela
├── guias.ts                     # FLUXOS {id, telas[]}, GLOBAL {id, fluxos[]}, VERSAO por guia
├── use-guia-da-tela.ts          # resolve a jornada em curso (global > fluxo > avulso), filtra por can,
│                                #   soma o total, aplica o piso, monta useOnboarding
├── continuacao.ts               # marcarContinuacaoSeAtivo(controle): chamado no handler que navega
└── gatilho-global.tsx           # Onboarding.Ajuda do global, no menu de ajuda do shell
e2e/tours/<fluxo-slug>.spec.ts   # Playwright percorre o tour do fluxo e o trecho dele no global
planning/<iniciativa>/tours/tours.md   # spec legível (templates/tours.md)
```

O modelo de código de cada arquivo está em `templates/onboarding-tela.md`. Regras de fiação que o modelo já carrega e que você confere tela a tela:

- **Três pontas na árvore** de toda tela que participa: `useGuiaDaTela` (hook), `<Onboarding.Intro>` e `<Onboarding controle>`. Sem o executor ou o modal, o hook marca o guia como visto e a bússola não abre nada. Depois de gerar, varra `useOnboarding(` e `useGuiaDaTela(` e confirme.
- `<Onboarding.Ajuda>` ao lado do título da seção **só na primeira tela de cada fluxo**; o global tem o gatilho no shell.
- `id` do guia único no produto: `<produto>-<fluxo-slug>` e `<produto>-global`. `versao` começa em 1; **subir a versão** sempre que passos mudarem, para reexibir uma vez a quem já viu.
- Persistência: default do componente (`localStorage`, prefixo `centralit`). Produto que quer estado no servidor troca o adapter (`jaViu` + `marcarComoVisto`): fronteira de integração.
- `TooltipProvider` na árvore (o componente exige).
- Todas as âncoras `data-onb` referenciadas nos passos **existem no fonte** (`proto/` ou `src/`). As que faltam vão como diff para o `px-proto` ou como item de `pre-requisitos.md`.

## Passo 7 — Verificar (portão executável)

Rode e cole a saída no eco final:

```bash
# toda âncora referenciada nos passos existe no fonte
for a in $(grep -rhoE 'data-onb="[^"]+"' src/onboarding/passos | sort -u); do
  grep -rq "$a" src proto 2>/dev/null || echo "ÂNCORA SEM ALVO: $a"
done
# toda rota dos guias existe no router ou no mapa de telas
npx tsc --noEmit -p tsconfig.app.json
npm run lint:travessao
npm run lint:caixa-alta
```

Depois, o teste que importa: abra o app, rode o tour de cada fluxo e o global; rode o `ux-persona` novato no flow **com o tour ativo**. Fricção de Descoberta que persiste = passo errado, volte ao Passo 2.

## Definition of Ready (trava + eco final)

- [ ] Fontes ingeridas e ecoadas; toda falta **declarada** (Passo 0)
- [ ] Um tour por flow desta leva; ordem do global confirmada (Passo 1)
- [ ] Cada passo com evidência (fricção ou ação principal); 3 a 7 por fluxo; alvo condicional e alvo só-com-dado tratados (Passo 2)
- [ ] Copy literal de B8 nos passos; lints de travessão e caixa alta verdes (Passo 3)
- [ ] Chave de permissão por passo ou pendência declarada; total somado após o filtro; piso em runtime (Passo 4)
- [ ] Mobile, disparo automático e pesquisa decididos ou como Premissa; divergência do gatilho global declarada (Passo 5)
- [ ] Três pontas na árvore em toda tela; `Ajuda` só na primeira tela do fluxo; ids e versões únicos (Passo 6)
- [ ] Zero "ÂNCORA SEM ALVO"; typecheck verde; tour rodado no navegador; persona novata percorreu com o guia (Passo 7)
- [ ] Fronteiras de integração listadas: `can`, `onEvento`, adapter de persistência

**Eco final:** *"Onboarding da leva: **N** tours de fluxo (`<slugs>`) e o global com **T** passos filtráveis, **A** âncoras (todas com alvo), **P** passos com permissão e **Q** pendências de chave, mobile **<sim | passos vazios>**, disparo automático **<sim | não>**, pesquisa **<ativa | desligada>**. Arquivos em `src/onboarding/` e `planning/<ini>/tours/tours.md`. Fronteiras: `can`, `onEvento`<, persistência>. Confirma?"*

## Onde salvar

- Código: `src/onboarding/` e `e2e/tours/` (alvo App React).
- Spec: `planning/<iniciativa>/tours/tours.md` (sempre; é o que a `px-handoff` copia para `tours/` do pacote).

> Ao fechar, **atualize o checkpoint** `planning/<iniciativa>/PX-PROGRESS.md` (ver "Checkpoint de progresso" no `px-protocol.md`): marque o tour do fluxo como feito (com os caminhos), aponte a `px-handoff` em *Próximo passo*, e sincronize decisões (mobile, disparo, pesquisa, gatilho global) → *Decisões travadas* e chaves de permissão pendentes → *Perguntas em aberto*.

## Encadeamento

Com os tours gerados, ofereça: "Quer rodar o `ux-persona` novato no flow com o tour ativo agora?" Em seguida, `px-handoff`: o pacote leva `tours/` (a spec `tours.md` mais os arquivos de `src/onboarding/` no caminho do fonte) e o GATE confere as âncoras.

## Quando NÃO usar

- **Dica pontual num único elemento** → Tooltip. **Poucos passos dentro de um formulário** → Stepper. **Tela de consulta pura** não pede guia (regra da spec).
- **Flow ainda não registrado** → `ux-flows` primeiro. **Histórias sem proto aprovado** → `px-proto` primeiro; sem âncora no fonte não há tour.

## Relação com o fluxo

```
px-request (B3 rota · B5 permissão + candidatas a âncora)  ─┐
px-proto   (data-onb no invólucro visível)                   ┼─→  px-story (ID · S6 RBAC)  →  ux-flows  →  px-tour  →  px-handoff (tours/)
ux-persona (fricções de Descoberta em e2e/reports/)         ─┘                                     ↑ revalida com o tour ativo
```
