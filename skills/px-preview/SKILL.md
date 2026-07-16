---
name: px-preview
description: Empacota a idealização (as telas prontas) num ÚNICO arquivo HTML autocontido para o líder UX enviar ao PO revisar, sem o PO precisar de conta, login, servidor ou instalar nada — ele abre por duplo clique no navegador. Detecta a stack (Vite SPA puro × framework SSR como TanStack Start) e aplica o caminho certo: no sandbox padrão (Vite) só inlina tudo com vite-plugin-singlefile; num app SSR, gera um build client-only paralelo que ignora o SSR e usa hash history. Sempre valida no navegador antes de entregar e, opcionalmente, publica como Artifact do claude.ai para devolver um LINK. Não idealiza nem desenha tela. Use ao fechar um ciclo de telas e querer mandar pro PO: "gerar o HTML pro PO", "empacotar o protótipo", "mandar a idealização pro PO ver", "gerar arquivo único", "quero um link pro PO revisar", "standalone pro product owner".
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: delivery
---

# px-preview — empacota a idealização num HTML pro PO revisar

Esta skill pega as telas que o UX já idealizou e as transforma em **um único arquivo `.html` autocontido**, para enviar ao PO. O PO **não precisa de conta no Claude, login, servidor nem instalar nada** — abre por duplo clique em qualquer navegador. É a entrega **pro PO** (revisão da idealização), diferente da `px-setup` Passo 4, que é a entrega **pro dev**.

**Público desta skill:** o líder UX/PX. Seja direto: pergunte só o que muda a decisão, execute o resto. Nunca peça pra ele digitar comando na mão.

**Por que funciona:** nesta fase o app roda com **dados mockados em memória** (sem back-end). Logo, ele consegue rodar 100% no navegador — basta tirar qualquer SSR do caminho e inlinar tudo num arquivo só.

Contexto inicial via slash: `$ARGUMENTS` (nome do projeto, ou "link" se já quiser publicar). Se vazio, siga o Passo 0.

## Prompting

Segue `Skill Prompting Conventions` do `CLAUDE.md`. Estruturada pra decisões enumeráveis (arquivo × link; stack detectada); livre pra nome do projeto. Toda pergunta traz o porquê + default recomendado; eco antes de executar.

## Passo 0 — Pré-condições (checar em silêncio, só falar se falhar)

O empacotamento só é possível se:

1. **Sem back-end real** — os dados são mock/fixtures em memória (padrão desta fase). Se a tela depende de API real que não está mockada, o arquivo abre mas fica vazio/quebrado. Se for o caso, **pare e avise**: precisa mockar a fronteira antes.
2. **Rotas resolvíveis no cliente** — nada que dependa do servidor pra montar a página.

Se ambas ok, siga.

## Passo 1 — Detectar a stack (define TODO o caminho)

Inspecione o projeto (não pergunte ao UX; descubra você):

- **`package.json`** — tem `vite`? É o esperado. Tem `next`/`@remix-run`? → caso especial (Passo 4).
- **Existe `index.html` na raiz + `src/main.tsx`** e o `vite build` gera `dist/index.html`? → **Vite SPA puro** (Passo 2). É o caso do **sandbox boilerplate**.
- **Tem `@tanstack/react-start` (SSR)?** O `vite build` gera função de servidor e **não** gera `index.html`? → **SSR client-only bypass** (Passo 3).

## Passo 2 — Vite SPA puro (o sandbox padrão) — caminho simples

O `vite build` já produz `dist/index.html` + assets; só falta inlinar tudo num arquivo.

**O sandbox boilerplate já vem pronto:** tem `vite-plugin-singlefile`, o `vite.standalone.config.ts` e o script `build:standalone`. Nesse caso, só:
1. **Roteamento:** se o app usa React Router, garantir **hash history** (`createHashRouter` / `HashRouter`) — sem isso quebra ao abrir por `file://`. Página única (sem router): nada a fazer.
2. Rodar `npm run build:standalone` → `dist-standalone/index.html` (arquivo único).

**Se o projeto NÃO tem o suporte ainda** (não veio do boilerplate):
1. `npm install -D vite-plugin-singlefile`
2. Criar `vite.standalone.config.ts` = config normal + `viteSingleFile()`, com `build.outDir: "dist-standalone"` e `build.assetsInlineLimit: 100_000_000` (inlina imagens). O `viteSingleFile` já força um chunk só — não precisa de `inlineDynamicImports`.
3. Adicionar `"build:standalone": "vite build --config vite.standalone.config.ts"` no `package.json`.
4. Roteamento em hash history (item 1 acima) e rodar o build.

## Passo 3 — App SSR (TanStack Start) — build client-only paralelo

O SSR não gera `index.html` e não abre como arquivo. Solução: um **segundo build, client-only, que ignora o Start**. Referência completa e testada: o projeto **Agility** (`apps/web/vite.standalone.config.ts`, `src/standalone.tsx`, `standalone.html`, ramo standalone no `__root.tsx`).

**Executar (adaptando ao projeto):**
1. `npm install -D vite-plugin-singlefile`
2. `vite.standalone.config.ts` — **sem** o plugin do Start; com `viteSingleFile()`; `define: { "import.meta.env.VITE_STANDALONE": '"1"' }`; `input: standalone.html`; `inlineDynamicImports: true`; `assetsInlineLimit` alto.
3. `standalone.html` — HTML de entrada só com `<div id="app">` + `<script type="module" src="/src/standalone.tsx">`.
4. `src/standalone.tsx` — monta o TanStack Router direto (`createRouter` + `routeTree` + **`createHashHistory`**), com os mesmos providers (Query etc.), via `createRoot(...).render(<RouterProvider .../>)`.
5. No root das rotas (`__root.tsx`), ramificar em `import.meta.env.VITE_STANDALONE === "1"` para **não** renderizar `<html>/<head>/<Scripts>` do Start (o documento vem do `standalone.html`); aplicar o tema no `<html>` via `classList`.
6. Assets: importar imagens (não usar caminho absoluto `/img.jpg`) pra elas inlinarem.
7. `npm run build:standalone` → `dist-standalone/standalone.html`.

## Passo 4 — Next.js / Remix / outros SSR — detectar e orientar

Não force o mesmo caminho. Explique que essa stack precisa de export estático próprio (ex.: `output: export` no Next) e trate caso a caso, ou combine com o dev. **Não entregue um arquivo que você não validou.**

## Passo 5 — Validar no navegador (obrigatório, nunca pular)

Antes de entregar, sirva o arquivo e confira: renderiza? console sem erros? navegação (incl. abrir uma tela/rota) funciona? Se algo quebrar, diagnostique e corrija antes de mandar. **Nunca entregue sem ter aberto.**

## Passo 6 — Entregar: arquivo ou link?

Pergunte (`AskUserQuestion`), porque muda a entrega:

- **Arquivo `.html` (default recomendado)** → copie pra um nome apresentável (ex: `release/<Projeto>-Prototipo.html`) e diga pro UX enviar por e-mail/Drive/Teams. O PO abre por duplo clique. Independe de qualquer conta.
- **Link** → publique como **Artifact do claude.ai** (Tool `Artifact`). Precisa da versão **content-only** (o Artifact envelopa em `<html><head><body>`): gere um HTML só com `<style>` + `#app` + `<script type="module">` (ver `scripts/make-artifact.mjs` do Agility: build `INLINE=0` → concatena o CSS + JS escapando `</script>`). Devolva a URL. Lembre que o Artifact é privado até o UX compartilhar pelo menu da página.

## Eco final

Antes de executar, repita em 3–4 linhas: *"Stack detectada: **X**. Vou gerar **arquivo/link** via **caminho Y** e validar no navegador — confirma?"*. Só então rode.

## Regras (aprendidas na prática)

- **Sempre hash history** quando há roteamento — senão quebra em `file://`.
- **Blindar `localStorage`/`sessionStorage` com try/catch** — o iframe do Artifact pode bloquear storage e derrubar o app.
- **Inlinar imagens** (importar como asset) — caminho absoluto `/img.jpg` não existe num arquivo solto.
- **Nunca tocar no build/deploy/dev normais** — o standalone é sempre um caminho **paralelo** (config + env dedicados).
- **Sempre validar no navegador** antes de entregar.
- **Avisar as limitações ao UX:** fonte via CDN cai pro fallback sob CSP; URLs usam `#`; dados são demo e somem ao recarregar.

## Relação com o fluxo

```
px-request → px-proto (proto validado pelo PX) → px-story → px-preview [OPCIONAL] → px-handoff → dev
                                                                    │
                                              app React construído, empacotado num HTML standalone
                                              para revisão da equipe interna antes de fechar o handoff
```

> `px-preview` é **opcional** — usado quando a equipe interna quer revisar o conjunto de telas no app React antes de fechar o handoff para os devs. Requer o app funcionando (não é para discovery nem para validação visual do PX — isso é o `px-proto`). A `px-setup` Passo 4 é a entrega **pro dev** (branch `ux/` + Merge Request).
