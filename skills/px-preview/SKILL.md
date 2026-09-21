---
name: px-preview
description: Opcional. Avalia o projeto e decide o melhor formato para compartilhar as telas construídas com PO e stakeholders que não têm acesso ao localhost — HTML standalone (duplo clique), deploy em Netlify/Vercel, ou Artifact do claude.ai. Detecta a stack e executa o caminho correto. Quem constrói sempre usa o localhost (Vite); o px-preview é só sobre como levar o que foi construído para fora. ⛔ Não é entrega para engenharia: o artefato é um build, não é implementável, e o dev recebe o FONTE pela px-handoff. Use quando o líder disser: "quero mandar pro PO ver", "gerar o HTML pro PO", "subir numa URL", "link pro product owner", "empacotar pra revisão".
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: delivery
---

# px-preview — decide como compartilhar as telas com quem não tem localhost

Esta skill é sobre **formato de entrega externa**, não sobre construção. Quem constrói (o PX/UX) sempre usa o Vite no localhost — é lá que o `px-proto` rodou, é lá que as telas vivem. O `px-preview` responde uma pergunta: *como levar essas telas para o PO ou stakeholder que não tem acesso ao sandbox?*

Três formatos possíveis, dependendo do projeto e do contexto:

| Formato | Quando usar |
|---|---|
| **HTML standalone** (arquivo único, duplo clique) | PO sem acesso a URL; envio por e-mail/Drive/Teams; revisão offline |
| **Deploy em Netlify/Vercel** | PO prefere uma URL; link permanente para múltiplas revisões; equipe distribuída |
| **Artifact do claude.ai** | Revisão pontual via link; sem necessidade de domínio próprio; share rápido |

A skill detecta a stack do projeto para saber qual caminho técnico é viável, e pergunta o contexto de entrega para recomendar o formato certo.

> ⛔ **O público desta skill é PO, stakeholder, cliente e usuário. Engenharia NUNCA recebe daqui.**
>
> O artefato desta skill é um **build**: HTML compilado, com o Tailwind virado regra de CSS e os nomes minificados. Serve para uma pessoa abrir e navegar, e não serve para um dev implementar. Medido em 2026-09-21: um protótipo de 4,7 MB chegou ao dev por chat, com 9.859 chamadas `jsx` compiladas e o fonte completo parado no repo do PX. Isso é da ordem de um milhão de tokens, não cabe na janela de contexto de nenhum modelo, e a IA do dev lê pedaços e infere o resto. Cada dev infere diferente.
>
> **Entrega para engenharia é `px-handoff`, sempre, e o que atravessa é o fonte da UI.** Não existe atalho de "mando o HTML enquanto isso": HTML por chat, e-mail ou Teams para o dev é o formato errado no canal errado, sem versão, sem branch e sem procedência.

**Público desta skill:** o líder UX/PX. Seja direto: pergunte só o que muda a decisão, execute o resto. Nunca peça pra ele digitar comando na mão.

**Por que funciona:** nesta fase o app roda com **dados mockados em memória** (sem back-end). Logo, ele consegue rodar 100% no navegador — basta tirar qualquer SSR do caminho e inlinar tudo num arquivo só (ou fazer deploy estático).

Contexto inicial via slash: `$ARGUMENTS` (nome do projeto, formato desejado, ou vazio). Se vazio, siga o Passo 0.

## Prompting

Segue `Skill Prompting Conventions` do `CLAUDE.md`. Estruturada pra decisões enumeráveis (formato de entrega, stack detectada); livre pra nome do projeto e URL de deploy. Toda pergunta traz o porquê + default recomendado; eco antes de executar.

## Passo 0 — Decidir o formato de entrega

### 0.1 — Portão de destinatário (antes de gerar qualquer coisa)

**"Quem vai receber este arquivo?"** (`AskUserQuestion`)

| Resposta | O que fazer |
|---|---|
| PO, stakeholder, cliente, usuário, revisão interna de produto | seguir para 0.2 |
| **Dev, engenharia, time de desenvolvimento, "vou mandar pro dev ver"** | ⛔ **pare aqui.** Não gere o arquivo. Explique em duas linhas que o build não é implementável e que a entrega de engenharia é o fonte, e ofereça rodar a `px-handoff`. Se o líder insistir porque o dev quer só *olhar*, gere, mas o nome do arquivo e o aviso do Passo 6 são obrigatórios, e diga na cara que aquilo não substitui o handoff |

**Por que este portão existe:** a tabela de formatos acima cita "envio por e-mail/Drive/Teams", e durante meses isso foi lido como autorização para mandar o protótipo ao dev por chat. A skill nunca dizia para quem **não** podia ir. Dizia só como empacotar.

### 0.2 — Formato

Pergunte (`AskUserQuestion`) — porque o caminho técnico muda completamente:

**"Como o PO/stakeholder vai acessar a revisão?"**
- **Arquivo HTML (Recomendado se envio por e-mail/Drive)** — abre por duplo clique, sem instalar nada. Vai para o Passo 2 (build standalone).
- **URL pública (Netlify/Vercel)** — link permanente, acesso de qualquer dispositivo. Vai para deploy estático.
- **Link do claude.ai (Artifact)** — share rápido via URL privada do claude.ai. Vai para o Passo 6.

Se o contexto já estiver claro em `$ARGUMENTS` (ex: "link", "netlify", "html"), não pergunte — infira e eco.

## Passo 0b — Pré-condições técnicas (checar em silêncio, só falar se falhar)

1. **Sem back-end real** — os dados são mock/fixtures em memória (padrão desta fase). Se a tela depende de API real que não está mockada, o arquivo abre mas fica vazio/quebrado. **Pare e avise** se for o caso.
2. **Rotas resolvíveis no cliente** — nada que dependa do servidor pra montar a página.

Se ambas ok, siga para o Passo 1 (detectar stack) e então o caminho do formato escolhido no Passo 0.

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

## Passo 6 — Entregar no formato escolhido no Passo 0

**Arquivo `.html` standalone:**
Copie para **`release/<Projeto>-Preview-PO-<AAAA-MM-DD>.html`** e instrua o PX a enviar por e-mail, Drive ou Teams. O PO abre por duplo clique. Independe de conta ou servidor.

⚠️ **O nome carrega o público de propósito, e a data substitui o versionamento na mão.** Arquivo solto viaja mais longe do que a conversa em que nasceu: um dev que recebe `Agility-Preview-PO-2026-09-21.html` sabe na hora que não é entrega para ele, enquanto `agility 11.html` não diz nada e ainda esconde que existiram dez antes. Nunca entregue com nome genérico, e nunca numere à mão.

**Deploy em Netlify (URL pública):**
1. Confirme que o build standalone foi gerado em `dist-standalone/`
2. `npm install -g netlify-cli` (se não tiver)
3. `netlify deploy --dir dist-standalone --prod` — gera uma URL pública permanente
4. Devolva a URL. O PO acessa de qualquer dispositivo, sem instalar nada.

**Artifact do claude.ai (link rápido):**
Precisa da versão **content-only** (o Artifact envelopa em `<html><head><body>`): gere um HTML só com `<style>` + `#app` + `<script type="module">`. Devolva a URL do Artifact. Lembre que é privado até o PX compartilhar pelo menu da página.

## Eco final

Antes de executar, repita em 3–4 linhas: *"Stack detectada: **X**. Vou gerar **arquivo/link** via **caminho Y** e validar no navegador — confirma?"*. Só então rode.

## Regras (aprendidas na prática)

- **Sempre hash history** quando há roteamento — senão quebra em `file://`.
- **Blindar `localStorage`/`sessionStorage` com try/catch** — o iframe do Artifact pode bloquear storage e derrubar o app.
- **Inlinar imagens** (importar como asset) — caminho absoluto `/img.jpg` não existe num arquivo solto.
- **Nunca tocar no build/deploy/dev normais** — o standalone é sempre um caminho **paralelo** (config + env dedicados).
- **Sempre validar no navegador** antes de entregar.
- **Público é PO, stakeholder, cliente e usuário. Engenharia nunca.** O portão do Passo 0.1 roda antes de gerar arquivo. Entrega para dev é `px-handoff`, e o que atravessa é o fonte da UI, nunca o build.
- **O nome do arquivo declara o público e a data** (`<Projeto>-Preview-PO-<AAAA-MM-DD>.html`). O arquivo sobrevive à conversa; o nome é a única coisa que viaja junto com ele.
- **Avisar as limitações ao UX:** fonte via CDN cai pro fallback sob CSP; URLs usam `#`; dados são demo e somem ao recarregar.

## Relação com o fluxo

```
px-request → px-proto (proto validado pelo PX) → px-story → px-preview [OPCIONAL] → px-handoff → dev
                                                                    │
                                              app React construído, empacotado num HTML standalone
                                              para revisão da equipe interna antes de fechar o handoff
```

> `px-preview` é **opcional** — usado quando a equipe interna quer revisar o conjunto de telas no app React antes de fechar o handoff para os devs. Requer o app funcionando (não é para discovery nem para validação visual do PX — isso é o `px-proto`). A `px-setup` Passo 4 é a entrega **pro dev** (branch `ux/` + Merge Request).
