---
name: styleguide-de-produto
description: Cria a identidade de marca de um produto e o styleguide dele, dentro do design system @cit, em qualquer estilo que o UX pedir. Cobre logo do produto (manter, refinar ou criar), marca de cada módulo, cores, tipografia de marca, ícones de marca, banners e animações. Entrevista o UX (com um briefing próprio para o logo), tira de 4 a 6 regras de linguagem da marca de referência, desenha 2 ou 3 opções do logo e de cada módulo num canvas, confere as cores por script de contraste e entrega SVGs, logo em três arranjos, banners, tokens.css, um produtos.json como fonte única e uma página de styleguide publicada. Ensina o método, não uma linguagem pronta. Chamada pela px-migrar-ds na etapa de identidade; também roda sozinha. Use quando alguém disser "logo do produto", "criar as marcas dos módulos", "styleguide do produto", "identidade do produto", "ícone de cada produto", "família de marcas", "banner do produto", "tipografia da marca", ou quando um sistema de outra área chega sem identidade.
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: styleguide
---

# styleguide-de-produto: logo, marcas e styleguide do produto

Esta skill é **a responsável pela marca do produto**: tudo o que faz o produto ser reconhecido como ele, por cima da base do design system `@cit`.

| Frente | O styleguide define | O DS `@cit` já define (não mexer) |
|---|---|---|
| **Logo** | símbolo, nome, arranjos (horizontal, vertical, só símbolo), área de proteção, tamanho mínimo, usos proibidos | — |
| **Marcas dos módulos** | a forma de cada módulo, o verbo, as versões claro/escuro/acento | — |
| **Cores** | a cor do logo e de cada módulo, o acento e onde ele aparece | cores de estado, neutros, disabled |
| **Tipografia** | a fonte de marca e onde ela entra (logo, nome do produto, banners, número de destaque) | a Inter e a escala da interface |
| **Ícones** | os ícones de marca (estado vazio, abertura, materiais), na linguagem da família | os ícones de ação: Lucide 16/20/24 |
| **Banners** | os banners e materiais com marca, cor, fonte e textura | — |
| **Animações** | a marca animada e a assinatura de movimento, como tokens | as faixas de duração (100 a 500 ms), só transform e opacity, `prefers-reduced-motion` |
| **Outros** | textura, frase da home e o que mais o produto tiver | componentes, espaçamento, raio, sombra |

Se o UX quiser mexer numa coluna da direita (outra fonte na interface, um ícone de ação desenhado à mão), é **⚠️ REQUER VALIDAÇÃO UX/PX**: registre o pedido como pendência e não aplique.

**Qualquer estilo.** O método vale para qualquer linguagem visual que o UX pedir: geométrica sólida, contorno, cantos arredondados, gradiente, monograma com letra, desenho livre, ou um SVG feito no Figma. O estilo é uma decisão do UX na fase 3, não uma herança do CITSmart X AI. A família "Lâmina e ponto" do X AI ([`references/exemplo-citsmart-x-ai.md`](references/exemplo-citsmart-x-ai.md)) é só um exemplo do método funcionando.

Siga o **Protocolo de Interação UX** e as **Skill Prompting Conventions** do `docs/px-protocol.md` do repositório (uma pergunta de cada vez, `AskUserQuestion` para escolhas, texto livre para nomes e cores, eco antes de avançar). Esta skill corresponde ao **Setup B (UI KIT / identidade)** do protocolo, no recorte "identidade do produto": nenhum logo, marca, cor ou regra entra sem o ok do UX.

Contexto inicial via slash: `$ARGUMENTS` (nome do sistema, módulos, logo atual, marca de referência). Se vazio, comece pela fase 1. Se veio da `px-migrar-ds`, use o diagnóstico dela (stack, logo, cores e fontes atuais, telas) para pular as perguntas já respondidas.

## Onde ficam as coisas

- **Scripts:** em `scripts/`, ao lado deste arquivo (no repo do produto, `.claude/skills/styleguide-de-produto/scripts/`, instalada pelo px-skills). Rode-os direto daí; não copie para o projeto.
- **Dados do projeto:** uma pasta `marcas/` no planejamento do produto, por exemplo `planning/<sistema>/marcas/`. Pergunte se o UX preferir outra. Ela guarda `produtos.json`, `README.md`, os SVGs que o UX trouxer, `svg/` (com `logo/`, `icones/`, `banners/` e `tokens.css`), `opcoes.html` e `styleguide.html`.
- **Ponto de partida:** copie `exemplo/produtos.json` (um sistema fictício, a Sala Viva) para a pasta do projeto e troque o conteúdo. O formato está em [`references/campos-do-styleguide.md`](references/campos-do-styleguide.md).
- **Produto sem módulos:** um produto só vira um único item em `modulos`; o logo e a marca do módulo podem ser o mesmo desenho.

## Regra de ouro: um ok do UX entre cada fase

Ao fim de cada fase: eco curto do que ficou decidido + pergunta de ok (`AskUserQuestion`: "Aprovar e seguir (Recomendado)", "Ajustar", "Voltar uma fase"). Não avance sem o ok. No **no-pause mode**, registre a decisão como premissa em `familia.pendencias` e siga com a recomendação; o ok do **logo** (fase 2), das **regras e do estilo** (fase 3) e das **formas** (fase 4) nunca é auto-resolvido.

## Fase 1: entrevista

Siga [`references/entrevista.md`](references/entrevista.md). Saída: o esqueleto do `produtos.json` (sistema, situação do logo, marca de referência, fundos, cores reservadas, acento ou não, frentes e campos escolhidos, lista de módulos com id, nome e verbo).

Eco: *"Sistema X, logo [manter | refinar | criar], N módulos (…), referência Y, fundo da aplicação #…, acento [sim, cor #… / não], frentes: … Confirma?"*

## Fase 2: logo do produto

Siga [`references/logo.md`](references/logo.md). Primeiro a decisão (`AskUserQuestion`): **manter** o logo atual, **refinar** (mesma ideia, desenho limpo), ou **criar** um novo. Depois o briefing, uma pergunta de cada vez: o que o logo precisa transmitir, o que evitar, referências, símbolo + nome ou só nome, onde ele vai viver.

- **Manter:** traga o SVG (`{"tipo": "arquivo"}`) e só documente: arranjos, área de proteção, tamanho mínimo e usos proibidos.
- **Refinar ou criar:** 2 ou 3 opções em `familia.logo.opcoes`, cada uma com o porquê ligado ao briefing. Mostre no canvas (`formas.py canvas`) e pergunte qual fica.

Saída: `familia.logo` com a opção escolhida, cor, arranjos, proteção, mínimo e proibidos. Sem logo aprovado, o resto da família não tem de onde tirar a linguagem.

## Fase 3: linguagem e estilo

Siga [`references/linguagem-da-marca.md`](references/linguagem-da-marca.md).

1. **Referência:** a linguagem vem do logo aprovado ou da marca-mãe (a marca da empresa ou da área).
2. **Estilo** (`AskUserQuestion`, com a recomendação que a referência sugere): geométrico sólido, contorno, cantos arredondados, gradiente, monograma/letra, desenho livre ou outro. O estilo vai para `familia.estilo`.
3. **Regras:** de 4 a 6, verificáveis, cada uma citando o que na referência a justifica (grade, tipo de curva, espessura, vão, ângulos, cores, qual peça é o acento).

Regra ou estilo que não vem da referência (invenção nossa) é **⚠️ REQUER VALIDAÇÃO UX/PX**. Saída: `familia.estilo` e `familia.regras`.

## Fase 4: formas (marcas dos módulos e ícones de marca)

Para cada módulo, **2 ou 3 opções** de forma, cada uma ligada ao nome ou ao verbo, todas obedecendo às regras e ao estilo. Escreva as opções em `modulos[].opcoes` (primitivas em [`references/campos-do-styleguide.md`](references/campos-do-styleguide.md#formas)) e marque a peça de acento com `"agente": true`.

```bash
python3 <skill>/scripts/formas.py planning/<sistema>/marcas/produtos.json verificar
python3 <skill>/scripts/formas.py planning/<sistema>/marcas/produtos.json canvas
```

- `verificar` mostra peças, área de tinta, caixa ocupada e as diagonais do logo, de cada marca e de cada ícone. Corrija antes de mostrar: ponto fora da grade, módulo sem peça de acento, tinta muito diferente da mediana (vai pesar diferente lado a lado) e diagonal fora da regra. Peças de texto, path e arquivo não são medidas: compare essas olhando o canvas.
- `canvas` gera `opcoes.html` com as opções do logo e dos módulos lado a lado, em 64, 24 e 16 px, no claro e no escuro. Publique como Artifact (se a sessão tiver a ferramenta) para o UX ver e comentar; senão, abra no navegador.

Pergunte por módulo qual opção fica (`AskUserQuestion` com as opções + "Misturar ou refazer"). Grave `escolhida`.

Com as marcas aprovadas, desenhe os **ícones de marca** que o produto precisa (estado vazio, abertura, banners), com as mesmas regras, em `familia.icones.de_marca`. Ícone de ação nunca entra aqui: é Lucide.

## Fase 5: cores

A cor do logo e uma cor por módulo (ou uma só para todos, se o UX preferir: pergunte). Com gradiente no estilo, cada módulo tem `cor` e `cor2`. Proponha cores que respeitem a paleta da referência e rode:

```bash
python3 <skill>/scripts/contraste.py planning/<sistema>/marcas/produtos.json
python3 <skill>/scripts/contraste.py --cor "#36B5AC" --fundo "#F2F4F7"   # testar uma cor solta
```

O script confere **pelo menos 3:1 no branco e no fundo da aplicação** (o mínimo para elemento gráfico, WCAG 1.4.11) para o logo e os módulos, 4.5:1 para o nome no logo e o texto dos banners, a distância das **cores reservadas** (estados, a cor da IA, a cor da marca-mãe…) e do acento, e avisa quando dois módulos ficam quase iguais. Quando uma cor não passa, ele sugere a mesma matiz escurecida. **Só mostre ao UX cores que passam**; se o UX quiser uma que não passa, registre como ⚠️ e explique o risco.

## Fase 6: tipografia, banners e animações

Uma frente de cada vez, com ok em cada uma. Formato em [`references/campos-do-styleguide.md`](references/campos-do-styleguide.md#identidade-da-família).

- **Tipografia de marca** (`familia.tipografia`). A fonte do nome no logo, normalmente a da marca de referência. Defina a família, no máximo dois pesos e a **lista fechada de usos** (logo, nome do produto no login e no header, título de banner, número de destaque). A interface continua na Inter do DS. Use fonte do Google Fonts (`fonte_url`) ou registre onde a fonte licenciada está.
- **Banners** (`familia.banners`). Pergunte quais o produto precisa (login, boas-vindas, novidade, e-mail) e o formato de cada um. Cada banner junta fundo (escuro ou a cor do módulo), textura opcional, título e subtítulo na fonte de marca e o logo ou a marca do módulo.
- **Animações** (`familia.movimento` e `modulos[].campos.marca_animada` / `movimento`). Tokens de duração dentro das faixas do DS (100 a 500 ms), uma curva e regras de quando a marca anima. A marca animada usa `respirar`, `montar` ou `pulsar-agente`; para outra, descreva e registre como pendência de implementação.
- **Campos por módulo** escolhidos na entrevista (acento e onde aparece, textura, frase da home…).

Rode `contraste.py` de novo ao fim: ele confere os banners e as durações.

## Fase 7: página de styleguide

Preencha as pendências por módulo e as da família. Depois:

```bash
python3 <skill>/scripts/pagina.py planning/<sistema>/marcas/produtos.json
```

A página traz: o logo (arranjos no claro e no escuro, área de proteção, tamanho mínimo, briefing e o que não fazer), as marcas, as regras, a tabela de contraste com as cores reservadas, o header claro e escuro a 24 px, os tamanhos 16/24/32/64, tipografia, ícones, banners, animações, um accordion por módulo e o que falta decidir. Seções sem dado não aparecem. Ela já segue o contrato de Artifact (title curto, tokens com modo escuro, fundo no body, sem rolagem horizontal).

Antes de mostrar, abra a página e confira se o logo e as marcas leem a 16 px, se a fonte de marca carregou e se nada vazou no celular. Ajuste no `produtos.json`, nunca no HTML gerado.

## Fase 8: entrega

```bash
python3 <skill>/scripts/gerar.py planning/<sistema>/marcas/produtos.json [pasta-de-saida]
```

1. **Logo** em `logo/`: `simbolo`, `horizontal` e `vertical`, cada um no claro e em `-escuro`.
2. **Marcas** em quatro versões por módulo: `<id>.svg` (cor do módulo, fundo claro), `<id>-escuro.svg` (branca), `<id>-acento.svg` e `<id>-escuro-acento.svg` (com a peça de acento na cor de acento). Sem acento, só as duas primeiras.
3. **Ícones de marca** em `icones/` (claro e escuro) e **banners** em `banners/`. Logo e banners usam a fonte de marca como texto: para uso fora da web, exporte em PNG ou converta o texto em curvas (Figma, Illustrator).
4. **`tokens.css`**: cor de cada módulo, acento, fonte de marca e tokens de movimento, para integrar ao `index.css` do produto (a `px-migrar-ds` faz isso na etapa de tokens).
5. **`produtos.json`** como fonte única: SVG, página, tokens e código do produto leem dele. Ninguém edita SVG gerado à mão.
6. **Página publicada:** publique o `styleguide.html` como Artifact (carregue a skill `artifact-design` antes, se a sessão pedir) e passe o link. Republique no mesmo link a cada rodada.
7. **`README.md`** da pasta `marcas/`: o que é a identidade, as regras em uma linha cada, como regenerar (os comandos), o link da página e o status (proposta ou validada, por quem e quando).
8. **Checkpoint:** se a iniciativa tiver `PX-PROGRESS.md`, atualize *Feito*, *Decisões travadas* (logo, estilo, regras, formas, cores, fonte, banners e movimento aprovados, com quem aprovou) e *Perguntas em aberto*. Esta skill não roda git: commit e branch ficam com a `px-setup`.

Se a skill foi chamada pela `px-migrar-ds`, devolva para ela: link da página, caminho do `tokens.css` e do `logo/`, e a lista de pendências.

## Definition of Done

- [ ] Logo decidido (manter, refinar ou criar) e aprovado, com arranjos, proteção, mínimo e proibidos.
- [ ] Estilo escolhido e regras de 4 a 6, cada uma ligada à referência, aprovadas pelo UX.
- [ ] Uma forma escolhida por módulo; `formas.py verificar` sem ✗.
- [ ] `contraste.py` sai com código 0.
- [ ] Fonte de marca com usos fechados; banners com texto em 4.5:1; movimento dentro das faixas do DS.
- [ ] Logo, SVGs, ícones, banners e `tokens.css` gerados; página gerada e publicada; README com status.
- [ ] Pendências registradas em `familia.pendencias` (ou "nenhuma").

## Quando não usar

- O sistema já tem identidade validada: use a página só para documentar (fases 5 a 8).
- O pedido é um ícone de interface (ação, navegação): isso é Lucide, pelo DS.
- O produto precisa migrar para o DS: comece pela `px-migrar-ds`, que chama esta skill na hora certa.
- O pedido é a marca da empresa (a marca-mãe) em si: isso é trabalho de branding, fora desta skill.
