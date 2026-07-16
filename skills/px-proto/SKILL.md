---
name: px-proto
description: Gera um protótipo HTML standalone fiel — com os tokens reais do UI KIT do projeto e as variações exatas dos componentes do DS — para o PX validar visualmente antes de escrever a história. Obrigatório após o px-request e antes do px-story. Abre no navegador, suporta iterações de ajuste na sessão, e só fecha quando o PX aprova. Use quando o líder disser "gera o proto", "quero ver como fica", "prototipar a tela", "visualizar a spec", ou ao fechar um px-request.
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: proto
---

# px-proto — protótipo visual fiel para validação do PX

Esta skill transforma uma `px-request` aprovada num **protótipo HTML standalone** fiel ao UI KIT e ao catálogo de componentes do projeto. O PX visualiza, pede ajustes na sessão, aprova — e só então a tela vira história (`px-story`). Nenhuma linha de produto é tocada.

**Por que obrigatório:** spec textual não substitui revisão visual. Erros de hierarquia, densidade, estados e copy só aparecem quando você vê a tela. Corrigir aqui é grátis; corrigir depois do dev é caro.

**Público:** o líder UX/PX. Seja direto e visual — esta skill conversa pouco e entrega depressa.

Contexto inicial via slash: `$ARGUMENTS` (caminho do `px-request`, nome da tela, ou descrição). Se vazio, peça.

---

## Passo 0 — Ingerir a px-request (base inegociável)

Leia o artefato `planning/<iniciativa>/requests/<slug>.md`. Extraia e ecoar em 5–8 linhas:

- **Tela / componente:** nome + propósito em 1 frase
- **Público principal:** papel + nível de familiaridade
- **Variação definida:** qual componente do catálogo (ex: "Table com Expansão — variante C")
- **Estados a cobrir:** lista dos estados levantados no B7 (default, loading, empty, error, disabled, success)
- **Ações principais:** o que aparece na tela (botões, menus, ações em linha)
- **Mock data:** campos e valores que vão aparecer

Se o `px-request` não existir ou estiver sem Definition of Ready, **pare**: rode `px-request` antes. O proto nunca nasce de spec incompleta.

Eco: *"Vou prototiar: [tela], variação [X], estados [A/B/C], usando o UI KIT de [projeto] — confirma?"*

---

## Passo 1 — Ingerir o UI KIT do projeto

Leia `planning/<projeto>/ui-kit.md` (ou `src/index.css` se o KIT já foi materializado). Extraia:

- Tokens de cor: `--primary`, `--background`, `--foreground`, `--border`, `--muted`, semânticas
- Família tipográfica + escala de tamanhos
- `--radius` (radius base do projeto)
- Qualquer token adicional registrado

Esses valores vão direto nas variáveis CSS do protótipo. **Nunca usar cores hardcoded nem placeholders.**

Se o UI KIT não existir, avise e ofereça rodar `px-kickoff` antes.

---

## Passo 2 — Mapear a variação no catálogo de componentes

Com a variação definida no `px-request` (Bloco 6), consulte `ds-components_v4.md` e extraia:

- **Anatomia:** quais partes compõem o componente
- **Estados documentados:** quais são os estados deste componente especificamente
- **Regras visuais:** sizing, spacing, comportamentos obrigatórios (ex: tabela sem scroll horizontal)
- **Comportamentos de overlay** (se aplicável): regras de empilhamento

Isso garante que o proto reflita a variação correta — não uma interpretação livre.

**Exemplos de variação que o catálogo define com precisão:**

| Família | Variações disponíveis |
|---|---|
| Table | Básica · Com Interações (sort/select) · Com Expansão · Data Grid avançada |
| Card | Resumo · Informativo · Interativo |
| Select | Base · Com Busca · Multi · Async · Combobox |
| Date Picker | Single · Range · Date Time |
| Upload | Campo simples · Dropzone · Multi-arquivo |
| Overlay | Drawer · Modal · Dialog · AlertDialog · Popover |

A variação escolhida na `px-request` determina exatamente o que renderizar.

---

## Passo 3 — Gerar o protótipo HTML

Gere **um único arquivo HTML autocontido** — React via CDN + Babel + Tailwind CDN — com os tokens do UI KIT injetados como variáveis CSS. Sem dependência de servidor, sem boilerplate, sem tocar em `src/`.

### Estrutura do arquivo

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Proto — [Nome da Tela] · [Projeto]</title>
  <script>
    // Suprimir warnings de desenvolvimento
    const _warn = console.warn.bind(console)
    console.warn = (...args) => {
      if (typeof args[0] === 'string' && (args[0].includes('Tailwind') || args[0].includes('Babel'))) return
      _warn(...args)
    }
  </script>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            primary: 'var(--primary)',
            background: 'var(--background)',
            foreground: 'var(--foreground)',
            muted: 'var(--muted)',
            border: 'var(--border)',
          }
        }
      }
    }
  </script>
  <script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
  <style>
    /* === UI KIT: tokens reais do projeto === */
    :root {
      /* Injetar aqui os tokens extraídos do ui-kit.md / src/index.css */
      --primary: #VALOR_REAL;
      --primary-foreground: #VALOR_REAL;
      --background: #VALOR_REAL;
      --foreground: #VALOR_REAL;
      --muted: #VALOR_REAL;
      --muted-foreground: #VALOR_REAL;
      --border: #VALOR_REAL;
      --input: #VALOR_REAL;
      --ring: #VALOR_REAL;
      --success: #VALOR_REAL;
      --warning: #VALOR_REAL;
      --destructive: #VALOR_REAL;
      --radius: VALOR_REAL;
      /* Família tipográfica do projeto */
      --font-sans: FAMILIA_REAL, system-ui, sans-serif;
    }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: var(--font-sans);
      background: var(--background);
      color: var(--foreground);
      font-size: 14px;
      line-height: 24px;
    }
    /* Focus ring padrão (Engineering Directives) */
    :focus-visible {
      outline: none;
      box-shadow: 0 0 0 3px rgba(var(--ring-rgb, 109 91 208) / 0.1);
      border-color: var(--ring);
    }
    /* Helper de ícone Material Symbols (alinhamento de glifo via CDN) */
    .ms {
      font-family: 'Material Symbols Outlined';
      font-weight: normal;
      font-style: normal;
      display: block;
      overflow: hidden;
      flex-shrink: 0;
      user-select: none;
    }
    .ms-16 { font-size: 16px; width: 16px; height: 16px; line-height: 16px; }
    .ms-20 { font-size: 20px; width: 20px; height: 20px; line-height: 20px; }
    .ms-24 { font-size: 24px; width: 24px; height: 24px; line-height: 24px; }
  </style>
</head>
<body>
  <div id="root"></div>
  <script type="text/babel">
    /* === MOCK DATA — derivado do Bloco 4 do px-request === */
    const MOCK = { /* ... */ }

    /* === ESTADOS === */
    const ESTADOS = ['default', 'loading', 'empty', 'error'] // ajustar ao B7

    /* === COMPONENTE PRINCIPAL === */
    function App() {
      const [estado, setEstado] = React.useState('default')
      return (
        <div style={{ minHeight: '100vh', background: 'var(--background)' }}>
          {/* Switcher de estado (visível no proto, invisível em produção) */}
          <div style={{ padding: '8px 16px', background: 'var(--muted)', display: 'flex', gap: 8, alignItems: 'center', fontSize: 12 }}>
            <span style={{ color: 'var(--muted-foreground)' }}>Estado proto:</span>
            {ESTADOS.map(e => (
              <button key={e} onClick={() => setEstado(e)}
                style={{ padding: '4px 8px', borderRadius: 'var(--radius)', border: '1px solid var(--border)',
                  background: estado === e ? 'var(--primary)' : 'transparent',
                  color: estado === e ? 'var(--primary-foreground)' : 'var(--foreground)',
                  cursor: 'pointer', fontSize: 12 }}>
                {e}
              </button>
            ))}
          </div>
          {/* Conteúdo da tela */}
          <TelaPrincipal estado={estado} />
        </div>
      )
    }

    function TelaPrincipal({ estado }) {
      /* Implementar a variação exata do componente aqui */
      return <div style={{ padding: 32 }}>/* tela */</div>
    }

    ReactDOM.createRoot(document.getElementById('root')).render(<App />)
  </script>
</body>
</html>
```

### Regras de implementação do proto

- **Tokens reais, nunca placeholder** — cor, radius, tipografia vêm do UI KIT extraído no Passo 1.
- **Espaçamento em múltiplos de 8px** — 8 / 16 / 24 / 32 / 48. Nenhum valor fora da escala.
- **Ícones sempre Material Symbols** — nunca emoji, nunca SVG inline, nunca texto `[ícone]`.
- **Switcher de estado visível no topo** — botões para trocar entre os estados do B7. Facilita a revisão sem recarregar.
- **Mock data do B4 injetado** — campos com valores plausíveis (não lorem ipsum). Volume realista (ex: 8–12 linhas numa tabela).
- **Sem animações pesadas** — transições simples só em `opacity`/`transform`; `prefers-reduced-motion` respeitado.
- **Sem scroll horizontal** — se tabela não cabe, colapsar colunas secundárias (regra do DS).
- **Um overlay por vez** — se o fluxo da tela envolve drawer/modal, implementar a abertura correta; nunca empilhar.
- **Layout via Flexbox ou CSS Grid** — nunca float, nunca position para layout estrutural.
- **Nenhum `text-transform: uppercase`** — hierarquia por peso/tamanho.

---

## Passo 4 — Abrir no navegador e apresentar ao PX

Abra o arquivo no navegador (via `preview_start` ou path direto). Confirme:
- Renderizou sem erro no console?
- Switcher de estado funciona em todos os estados do B7?
- Tokens visuais corretos (cores, tipografia, radius)?

Apresente ao PX: *"Proto da tela [X] aberto — [N] estados disponíveis no switcher. Revise e me diga o que ajustar."*

---

## Passo 5 — Ciclo de ajuste (iterativo, na sessão)

O PX revisa e pede mudanças. Para cada rodada:

1. Ouça o ajuste — visual, copy, comportamento de estado, hierarquia
2. Aplique no HTML (Edit no arquivo)
3. Recarregue o navegador
4. Confirme que o ajuste está correto
5. Repita até o PX aprovar

**Tipos comuns de ajuste:**
- Hierarquia visual (peso, tamanho, cor)
- Copy de labels, botões, mensagens de estado
- Layout de colunas ou disposição de ações
- Comportamento de estado (ex: skeleton diferente, toast diferente)
- Densidade (compactar/expandir)
- Responsivo (testar no breakpoint mobile)

Cada ajuste é aplicado direto, sem perguntar — o PX vê o resultado e decide se quer mais.

---

## Passo 6 — Aprovação e encerramento

Quando o PX disser que está aprovado:

1. **Salve o proto** em `planning/<iniciativa>/protos/<slug-da-tela>.html`
2. **Atualize o `PX-PROGRESS.md`** — marque o proto como aprovado, registre o caminho do arquivo
3. **Eco final:**
   > *"Proto de [tela] aprovado. Arquivo salvo em `planning/<iniciativa>/protos/<slug>.html`. Próximo passo: `px-story` para escrever os critérios de aceite, usabilidade e BDD desta tela — quer seguir?"*

---

## Onde salvar

`planning/<iniciativa>/protos/<slug-da-tela>.html`

---

## Regras (aprendidas na prática)

- **Nunca gerar o proto sem px-request aprovado** — spec incompleta gera proto errado, que gera história errada.
- **Variação do catálogo é lei** — não inventar componente nem misturar variações. Se a variação definida não existe no catálogo, é gate ⚠️ — parar e resolver antes de renderizar.
- **UI KIT real é inegociável** — proto com cores placeholder não serve para validação visual; o PX precisa ver a identidade real.
- **Switcher de estado é obrigatório** — o PX não deve ter que pedir "agora me mostra o estado vazio"; ele já está lá.
- **Ajuste direto, sem burocracia** — o proto é uma ferramenta de conversa visual, não um documento. Aplique, mostre, pergunte se quer mais.
- **Mock data realista** — nomes, datas, valores numéricos plausíveis. Sem "Lorem Ipsum", sem "Usuário 1".
- **Proto aprovado não é código de produção** — o boilerplate vai implementar a tela do zero a partir da spec. O proto é referência visual, não base de código.

---

## Relação com o fluxo

```
px-request (spec textual aprovada)
    ↓
px-proto  ←  você está aqui
    │
    ├── iterações de ajuste (na sessão, ilimitadas)
    │
    └── [aprovado pelo PX]
          ↓
      px-story (história + BDD da tela aprovada visualmente)
          ↓
      [px-preview — opcional, revisão da equipe interna]
          ↓
      px-handoff (DoD + sprint → devs)
```

> `px-proto` é **obrigatório** — nenhuma tela vai para `px-story` sem validação visual. O `px-preview` é **opcional** — usado quando a equipe interna quer revisar o conjunto de telas no app React antes de fechar o handoff para os devs.
