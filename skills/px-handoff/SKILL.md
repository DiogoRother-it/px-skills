---
name: px-handoff
description: Skill de FECHAMENTO da cadeia PX. Monta o pacote de handoff pro dev a partir das histórias já ready — consolida a referência visual navegável (HTML unificado ou build do protótipo), o UI Kit do produto, as histórias de negócio (BDD), as regras de negócio por fluxo e as specs referenciadas, tudo self-contained e organizado por fluxo. Não envia código-fonte nem artefatos internos. Use ao fechar um lote de telas prontas pra levar pro dev — "fechar o handoff", "preparar a entrega pro dev", "empacotar pro desenvolvimento", "qual sprint essa entrega entra", "finalizar o fluxo".
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: handoff
---

# px-handoff — o fechamento da cadeia (entrega pro dev)

Esta skill **fecha** o ciclo de uma entrega: pega as histórias que já estão *ready* (saíram do `px-story`) e monta o **pacote de handoff** que o dev vai consumir — referência visual navegável, UI Kit, histórias de negócio, regras de negócio e specs referenciadas, organizadas por fluxo.

**Contrato de entrega:** o dev recebe um pacote **self-contained** (nada aponta para fora dele):
- **Referência visual navegável** — HTML unificado single-file (com âncoras `#view-*`/`data-story`) quando existir; senão, o **build do protótipo** em `prototipo/`.
- **UI Kit** do produto (`ui-kit.md`, tokens reais).
- **Histórias de negócio** por fluxo (`stories/`, BDD + CA + estados).
- **Regras de negócio por fluxo** (`regras-negocio.md`) — as RNs NÃO podem ficar só no request interno.
- **Specs referenciadas** por qualquer história (ex.: spec de aba/componente) — copiadas para dentro do fluxo.
- **README.md** do pacote (como ver, como está organizado).

O PX é referência visual — o dev implementa na stack do projeto. Ela **não desenha tela** (isso é `px-request`/`px-story`): fecha o ciclo, monta o pacote e (quando há repo do dev) executa o push.

**Público desta skill:** o líder UX/PX. Seja direto: monte o pacote a partir do que já existe, pergunte só o que muda a decisão, confirme e feche.

Contexto inicial via slash: `$ARGUMENTS` (rótulo da entrega, lista de fluxos, ou restrições — ex.: "sem gitlab ainda, só organizar as pastas"). Se vazio, pergunte qual é a entrega sendo fechada.

## Prompting

Segue `Skill Prompting Conventions` do `CLAUDE.md`. Estruturada pra decisões enumeráveis; livre pra nota de release. Toda decisão traz o porquê + default recomendado; eco antes de despachar.

## Pré-requisito (checar antes de montar)

- **Histórias ready:** já passaram pelo `px-story` (BDD *ready*). Se alguma ainda está em `px-request`, avise que o handoff nasce incompleto e ofereça fechar a `px-story` faltante antes.
- **Referência visual (em camadas — não bloqueie cedo demais):**
  1. **Ideal:** HTML unificado single-file (via `px-preview`), com `#view-*` por fluxo e `data-story` por elemento acionador.
  2. **Fallback aceitável:** o projeto é um app React/Vite sem single-file → usar o **build de produção** (`dist/`) copiado para `prototipo/` como referência visual (servir via servidor estático). Marcar o single-file + `data-story` como **pendência** (não bloqueia a entrega). Se não houver build, ofereça gerar (`npm run build`) ou rodar `px-preview`.
  3. **Último recurso:** só link do localhost (registrar no README que a referência visual é o dev server).
  Só bloqueie se não houver **nenhuma** referência visual possível.
- **Delta automático:** varra as histórias `.md` *ready* e compare com entregas anteriores (`handoff-ux/*/`) para montar o delta desta leva. O PX confirma o que entra.

**Perguntas obrigatórias antes de montar o pacote (`AskUserQuestion`):**
> 1. "Esse projeto já aderiu de forma completa à biblioteca de componentes `@centralit`?"
>    **Sim** → DoD interno inclui a obrigatoriedade de usar os componentes da biblioteca.
>    **Não** → DoD interno registra que o dev adapta a referência visual conforme a stack do projeto.
> 2. "Já existe o repositório oficial do dev para receber a entrega?"
>    **Sim** → peça o caminho local/URL; o push roda no BLOCO 6.
>    **Não / ainda não** → organize o pacote **localmente** em `handoff-ux/<label>/` na raiz do projeto atual e **pule o push** (fica pendente para quando o repo existir). Registre isso no `handoff.md`.
> 3. "Além do repo do dev, este projeto também mantém um repositório CENTRAL do PX (um monorepo/núcleo onde vivem produto, planning e docs de várias iniciativas)?"
>    **Sim** → ao final deste handoff, ofereça rodar `px-sync` pra espelhar o estado completo de trabalho nesse repo central. **É um destino independente do handoff**: o pacote reduzido (aqui) vai pro dev; o espelho completo (`px-sync`) vai pro núcleo — um não substitui o outro, e não bloqueia o push do BLOCO 6.
>    **Não** → seguir só com o destino dev; não oferecer `px-sync` no fechamento.

---

# Os blocos do handoff

> Não é entrevista de descoberta (isso já foi feito). É **consolidação**: puxe do que existe, sanitize, confirme, carimbe. Avance na ordem. Registre no template `templates/px-handoff.md`.

## BLOCO 1 — Escopo da entrega (o que entra nesta leva)
**Decidir:** quais histórias prontas vão neste handoff — e o que viaja junto de cada uma.
**Por que importa:** uma leva pode ter mais histórias do que o dev integra num sprint. E uma história sem as RNs e specs que ela cita chega incompleta.
**Fazer:**
- Varrer as histórias *ready* ainda não entregues. Apresentar a lista ao PX e confirmar quais entram. Excluir histórias **obsoletas/tombstoned** (telas mortas).
- Marque o que **fica pra depois** (e por quê) — vira a próxima leva.
- **Para CADA fluxo que entra, o pacote leva:**
  - a **história** (`stories/<historia>.md`);
  - as **regras de negócio** (`regras-negocio.md`) — extraídas da seção "Regras de negócio" do request de origem, **sanitizadas** (ver BLOCO 6). Sem isso o dev fica com os CA mas sem a fonte das regras;
  - toda **spec referenciada** pela história (ex.: "ver `spec-da-aba.md`") — copiada para o fluxo e sanitizada.
- **Recorte dev-facing vs. interno:** aplicar o `templates/handoff-manifest.md`. Entram também **decisões de produto canônicas** (`decisoes/*.md`) e **mapa de permissões/triggers** (`rbac-*.md`) quando existirem. Ficam de fora **os arquivos** de checkpoint (`PX-PROGRESS`), prompts de continuidade, discovery/auditoria, épicos e requests **como arquivos** — mas o **conteúdo essencial** deles (RNs, specs referenciadas) é extraído para os `.md` do pacote. Se a iniciativa tiver muitos `.md` internos, gravar/atualizar `planning/<iniciativa>/HANDOFF-MANIFEST.md` e confirmar o recorte com o PX.

## BLOCO 2 — Carimbo da entrega (o "quando/qual versão")
**Decidir:** o rótulo desta entrega — define o nome da pasta `handoff-ux/<label>/`.
**Fazer (`AskUserQuestion` para o rótulo):**
- Aceita **`semana-<NN>`** (com a semana ISO, ex.: `semana-29 · 2026-W29`) **ou** um rótulo de versão **`v<N>`** (ex.: `v1`) quando o time versiona por entrega, não por semana.
- Use o rótulo que o PX indicar; se ele já disse no contexto inicial (ex.: "v1"), não repergunte.

## BLOCO 3 — Definition of Done (checklist interna — não vai no pacote do dev)
**Por que importa:** a régua que o PX usa pra confirmar que o pacote está completo *antes* de fechar.
**Verificar antes de avançar pro BLOCO 4:**
- [ ] Referência visual presente e navegável (HTML unificado single-file **ou** build em `prototipo/`).
- [ ] Se HTML single-file: cobre todos os estados (default/loading/empty/error/disabled/read-only/hover/foco/responsivo) e breakpoints (Mobile/Tablet/Desktop/Widescreen). Se build: idem coberto pelo próprio app.
- [ ] UI Kit do produto presente e atualizado (tokens reais de cor, tipografia, identidade).
- [ ] Histórias com BDD completo (feliz + vazio + erro + permissão).
- [ ] `regras-negocio.md` presente em cada fluxo (ou RNs inlined na história).
- [ ] Toda spec referenciada por uma história está incluída no pacote.
- [ ] Nomes de arquivo sem prefixos numéricos (`historia-nome.md`, não `01-...`).
- [ ] Copy sem travessão (— / –) e sem caixa alta total em toda a referência visual e nos `.md`.

## BLOCO 4 — Fronteiras de integração (onde acaba o mock, começa o real)
**Fazer:**
- Consolide as `⚑ Boundary` das histórias: cada dependência de API/low-code/storage/terceiro, com o que precisa ser substituído.
- Sem dependência → "Nenhuma — opera sobre dados já mockados/carregados."

## BLOCO 5 — Perguntas em aberto (confirmar com o PX antes de enviar)
**Fazer (`AskUserQuestion` para cada item):**
- Para cada pendência: **"Isso já tem resposta ou dono confirmado?"**
  - **Tem resposta** → resolve inline. **Tem dono sem resposta** → entra com `dono: <nome>`. **Sem dono e sem resposta** → **não envia**; bloqueia até resolver ou descartar.
- Sem pendências → omitir a seção.

## BLOCO 6 — Fechar: sanitizar, montar, confirmar e despachar

**Fazer, nesta ordem:**

1. **Sanitizar TUDO que entra no pacote** (cópias de stories, RNs extraídas, specs referenciadas). Passo não-negociável — é o que separa "pacote self-contained" de "pacote com links quebrados":
   - **Referências mortas:** nenhum caminho para `planning/`, `src/`, `epics/`, `requests/` que não exista **dentro do pacote**. Reescrever para caminho relativo ao pacote (`../regras-negocio.md`, `../../prototipo/`, `../../ui-kit.md`, `../<spec>.md`) ou remover a linha. Verificação: `grep -r` por `planning/`, `src/proto`, `epics/` no pacote deve dar **zero**.
   - **Terminologia superada:** substituir termos que mudaram pela nomenclatura canônica atual do produto (ex.: papéis antigos → papéis atuais; rótulos de status renomeados). Verificação: `grep` pelos termos antigos = zero.
   - **Copy:** sem travessão (— / –) e sem caixa alta total.
2. **Referência visual:**
   - HTML unificado → plantar `data-story="<ID>"` em cada elemento acionador (estático: no próprio elemento; gerado por JS: no HTML que a função geradora constrói).
   - Build → copiar o `dist/` viável (index + assets, sem registry/config) para `prototipo/`; documentar no README como servir.
3. **Montar** o `handoff.md` (template) + o `README.md` do pacote.
4. **Reconciliar doc:** README e handoff.md devem descrever o conteúdo **real** do pacote (referência visual = HTML single-file ou build; RNs por fluxo; specs incluídas). Nada de "HTML não gerado" se o `prototipo/` está lá.
5. Passar pelo **GATE** — só avança se tudo verde.
6. Apresentar o eco final ao líder e aguardar aceite explícito.
7. **Despachar (condicional ao repo do dev):**
   - **Sem repo do dev** → o pacote já está organizado em `handoff-ux/<label>/` na raiz do projeto; **não há push**. Mostrar a árvore final e registrar no `handoff.md` que o push fica pendente.
   - **Com repo do dev** → montar `handoff-ux/<label>/` **na raiz do repo do dev**, mostrar a árvore, e push via **branch órfã** (push limpo, sem herdar histórico do boilerplate):
     ```
     git checkout --orphan ux/<label>
     git rm -rf .
     git add handoff-ux/<label>/
     git commit -m "ux(<label>): handoff <resumo>"
     git push origin ux/<label>
     ```
     Confirmar o push com o hash do commit.
   - **Se a pergunta 3 confirmou repo central** → depois de despachar (ou mesmo sem repo do dev ainda), oferecer rodar `px-sync` pra espelhar o estado completo de trabalho no núcleo. Não é o mesmo push: `px-sync` sobe produto + `planning/` + `docs/` inteiros no `main` do repo central, fast-forward e gated — nunca dispare sem passar pelo próprio gate do `px-sync`.

**Estrutura da pasta de entrega:**
```
handoff-ux/
└── <label>/                     # semana-<NN> ou v<N>
    ├── handoff.md
    ├── README.md
    ├── ui-kit.md
    ├── prototipo/               # HTML unificado single-file OU build navegável
    └── <fluxo>/
        ├── stories/
        │   └── <historia>.md
        ├── regras-negocio.md
        └── <spec-referenciada>.md   # quando a história referenciar
```
`handoff-ux/` sempre na raiz. Uma pasta por fluxo. HTML/build, UI Kit, README e handoff.md na raiz do rótulo.

## GATE — Barreira de saída (verificar antes do eco final)

**Qualquer item com ✗ bloqueia** — resolver ou declarar como Pergunta em aberto com dono.

**Self-contained (o coração da otimização)**
- [ ] `grep` por `planning/`, `src/proto`, `epics/`, `requests/` no pacote = **zero** (nenhuma referência morta)
- [ ] `grep` pelos termos de terminologia superada = **zero**
- [ ] Toda spec referenciada por uma história está **incluída** no pacote
- [ ] `regras-negocio.md` presente em cada fluxo (ou RNs inlined na história)
- [ ] README.md e handoff.md batem com o conteúdo real (referência visual, RNs, specs)

**Pacote**
- [ ] Referência visual navegável presente (HTML single-file **ou** build em `prototipo/`)
- [ ] Se HTML single-file: `data-story="<ID>"` em cada elemento acionador
- [ ] UI Kit presente e atualizado
- [ ] `handoff.md` sem campos `<placeholder>` vazios

**Histórias**
- [ ] BDD completo (feliz + vazio + erro + permissão) em cada história
- [ ] Rastreabilidade: descrição em texto (+ anchor `data-story` quando há HTML single-file)
- [ ] Nomes de arquivo sem prefixos numéricos
- [ ] Nenhuma story técnica interna do PX — apenas histórias de negócio
- [ ] Copy sem travessão e sem caixa alta total

**Perguntas em aberto**
- [ ] Toda pendência tem dono confirmado

**O que nunca deve sair como arquivo** (ver `templates/handoff-manifest.md`)
- [ ] Nenhum código-fonte (`.tsx`/`.ts`/`.jsx`/`.js` de componente) ou config (`vite.config`, `tsconfig`, `package.json`, `.env`)
- [ ] Nenhum artefato interno: checkpoint (`PX-PROGRESS`), prompt de continuidade, discovery/auditoria, épicos, requests, scratchpad, memória

**O que deve entrar**
- [ ] Regras de negócio por fluxo + specs referenciadas (extraídas/sanitizadas)
- [ ] Decisões de produto canônicas (`decisoes/*.md`) e mapa de permissões (`rbac-*.md`) quando existirem

## Eco final

Antes de fechar, repita em 3–4 linhas: *"Handoff **<label>**: **N** histórias em **M** fluxos, cada fluxo com regras de negócio e specs referenciadas incluídas, referência visual = **<HTML single-file | build em prototipo/>**, UI Kit incluído, **X** fronteiras de integração. Pacote self-contained (0 referência morta). Perguntas em aberto: `<N ou nenhuma>`. **<Push via branch órfã `ux/<label>` no repo do dev | Sem repo ainda: organizado localmente, push pendente>**. **<Repo central: rodar px-sync em seguida | Sem repo central>** — confirma?"*. Só então feche.

## Onde salvar

`handoff-ux/<label>/handoff.md` — o mesmo slug do rótulo.

## Regras

- **Pacote self-contained.** Nenhuma referência a caminho fora do pacote — refs mortas são reescritas para relativas ou removidas na sanitização (BLOCO 6).
- **RNs e specs referenciadas viajam junto**, extraídas do interno e sanitizadas. O request fica de fora como arquivo; seu conteúdo essencial, não.
- **Terminologia canônica.** Termos superados são substituídos pela nomenclatura atual do produto na sanitização.
- **Referência visual em camadas.** HTML unificado single-file com `data-story` é o alvo; o build em `prototipo/` é fallback aceitável; localhost é último recurso. Não bloqueie por não ter o single-file.
- **Doc reconciliada.** README/handoff.md descrevem o que o pacote realmente contém.
- **Push condicional.** Sem repo do dev, organiza localmente e o push fica pendente. Com repo, push sempre via **branch órfã** — nunca a partir do histórico do boilerplate.
- **Não desenha tela** e **não inventa boundary.** Consolida o que `px-request`/`px-story` produziram; o que faltar vira Pergunta em aberto com dono.
- **Nunca executa o push sem aceite explícito do PX.**
- **`handoff-ux/` sempre na raiz.** HTML é sempre unificado — nunca separado por funcionalidade.

## Relação com o fluxo

```
                            ┌─→ dev (referência visual)         [pacote reduzido, branch órfã]
px-request → px-story → px-handoff ─┤
                            └─→ px-sync → repo CENTRAL do PX     [espelho completo, main fast-forward]
                            ^ você está aqui
                            (fecha a cadeia: referência visual + UI Kit + histórias + RNs + specs, por fluxo, self-contained)
```

> `px-handoff` fecha o ciclo: consolida um pacote **self-contained** de referência visual e o entrega (push quando há repo; organização local quando ainda não há). O dev implementa na stack do projeto — o PX é referência, não código de produção. Quando o projeto também mantém um repo central do PX, `px-handoff` pergunta isso logo no início (pergunta 3) e delega pro `px-sync` — são destinos e conteúdos diferentes, nenhum substitui o outro.
