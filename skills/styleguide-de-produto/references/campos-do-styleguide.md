# O produtos.json e os campos do styleguide

O `produtos.json` é a fonte única. Os quatro scripts leem dele; ninguém edita SVG nem HTML gerado à mão. O exemplo completo está em `exemplo/produtos.json`.

## familia

| Campo | Obrigatório | O que é |
|---|---|---|
| `nome` | sim | Nome da família ("Família Lâmina e ponto"). Vira o título da página. |
| `sistema` | sim | Nome do sistema. |
| `status` | não | "proposta", "validada"… Aparece no topo da página. |
| `intro` | não | Duas ou três frases sobre a família. |
| `marca_mae` | não | `{"nome", "descricao", "pecas"?}`. A referência da linguagem quando não há logo. |
| `logo` | não | O logo do produto (formato em [`logo.md`](logo.md#4-documentar-o-escolhido)), com `pecas` ou `opcoes` + `escolhida`. Sem peças, usa as da marca-mãe. |
| `estilo` | não | `{"preenchimento": "solido" \| "contorno", "traco", "cantos": "retos" \| "redondos", "raio", "gradiente"}`. |
| `regras` | sim | 4 a 6 frases, com o núcleo em `**negrito**`. |
| `acento` | não | `{"nome", "cor", "papel"}`. Sem ele, só duas versões de SVG. |
| `fundo_app` | não | Fundo da aplicação (padrão `#EEF0F4`). |
| `fundo_escuro` | não | Fundo escuro do header e das amostras (padrão `#0E1420`). |
| `cor_escuro` | não | Cor da marca no fundo escuro (padrão `#FFFFFF`). |
| `minimo_contraste` | não | Padrão `3.0`. |
| `distancia_minima` | não | ΔE mínimo para as cores reservadas (padrão `20`). |
| `cores_reservadas` | não | `[{"cor", "motivo"}]`. |
| `tipografia` | não | Fonte de marca e onde ela entra (abaixo). |
| `icones` | não | `{"interface", "de_marca": [...]}` (abaixo). |
| `cor_icone` | não | Cor dos ícones de marca no claro (padrão `#0E1420`). |
| `banners` | não | Lista de banners (abaixo). |
| `movimento` | não | Tokens de movimento da família (abaixo). |
| `campos` | não | Campos opcionais que esta família usa (lista abaixo). |
| `comum_aos_modulos` | não | Frases que valem para todos os módulos, mostradas acima do accordion. |
| `pendencias` | não | O que falta decidir na família. |

## modulos[]

| Campo | Obrigatório | O que é |
|---|---|---|
| `id` | sim | kebab-case, sem acento. Vira nome de arquivo. |
| `nome`, `verbo` | sim | O verbo aparece no header e no cartão. |
| `cor` | sim | Hex. Conferida pelo `contraste.py`. |
| `cor2` | com gradiente | Segunda cor do gradiente. |
| `porque` | sim | Uma frase: por que essa forma. |
| `pecas` | sim, ou `opcoes` | Lista de peças (abaixo). |
| `opcoes` | fase 3 | `[{"id": "A", "porque", "pecas"}]`. |
| `escolhida` | com `opcoes` | Id da opção que vale. Sem `pecas`, os scripts usam a escolhida. |
| `campos` | não | Valores dos campos opcionais. |
| `pendencias` | não | O que falta decidir neste módulo. |

## Formas

Grade de 64 x 64, origem no canto de cima à esquerda, y crescendo para baixo. Ângulos em graus, 0 = direita, crescendo no sentido horário.

| `tipo` | Campos |
|---|---|
| `poligono` | `pontos: [[x, y], ...]` |
| `retangulo` | `x, y, largura, altura` |
| `barra` | `de: [x, y], ate: [x, y], espessura` (ponta reta) |
| `regular` | `cx, cy, r, lados, inicio` (padrão `-90`, ponta para cima) |
| `circulo` | `cx, cy, r` |
| `anel` | `cx, cy, r, espessura`, e `de`/`ate` para um arco |
| `path` | `d`, `transform`? (desenho livre com curvas Bézier) |
| `arquivo` | `caminho` (SVG feito fora; os `<path>` são trazidos e ajustados à grade; caminho relativo ao produtos.json) |
| `texto` | `texto`, `x`, `y`, `tamanho`, `peso`?, `fonte`?, `ancora`? (letra ou monograma; para entregar, converta em curvas) |

`path`, `arquivo` e `texto` não recebem transformação e ficam fora da medição de tinta.

Em qualquer peça das primitivas geométricas: `espelhar` ("horizontal" ou "vertical"), `girar` (graus) com `centro`, `mover: [dx, dy]`, `repetir: {"vezes", "girar" | "mover"}` e `agente: true` para a peça de acento. A ordem é espelhar, girar, mover. Em qualquer peça, `"contorno": true` ou `false` foge do `familia.estilo`.

Exemplo, seis braços em volta de um núcleo (HyperAgents):

```json
[{"tipo": "retangulo", "x": 28.5, "y": 6, "largura": 7, "altura": 14, "repetir": {"vezes": 6, "girar": 60}},
 {"tipo": "retangulo", "x": 27.5, "y": 27.5, "largura": 9, "altura": 9, "agente": true}]
```

## Identidade da família

O DS `@cit` define a base (Inter na interface, Lucide nos ícones de ação, faixas de duração). Estes campos são a camada de marca por cima dela.

**`tipografia`**

```json
{"interface": "Inter, pela escala do DS @cit",
 "marca": {"familia": "Nunito", "fonte_url": "https://fonts.googleapis.com/css2?family=Nunito:wght@700;800&display=swap",
           "pesos": [700, 800], "origem": "a mesma da marca-mãe",
           "uso": ["nome do sistema e dos módulos no login e no header", "título de banner"]},
 "regras": ["**Fonte de marca nunca em texto corrido,** botão, rótulo ou tabela."]}
```

`fonte_url` só do Google Fonts (a página carrega dali). Fonte licenciada fora do Google: deixe sem `fonte_url` e registre onde o arquivo está.

**`icones`**: `{"interface": "Lucide em 16, 20 e 24 px, pelo DS @cit.", "de_marca": [{"id", "nome", "uso", "pecas"}]}`. As peças seguem o mesmo formato das marcas e passam pelo `formas.py verificar`.

**`banners`**: `[{"id", "titulo", "subtitulo"?, "formato": [1200, 400], "fundo": "escuro" | "cor" | "#hex", "modulo"?, "textura"?: true, "cor_texto"?: "#FFFFFF", "uso"?}]`. Com `modulo`, usa a marca e a cor dele (e a textura, se `textura: true` e o módulo tiver uma); sem `modulo`, usa `marca_mae.pecas`. O texto precisa de 4.5:1 sobre o fundo.

**`movimento`**: `{"duracoes": {"micro": "120ms", "padrao": "200ms", "entrada": "360ms"}, "curva": "cubic-bezier(.2,.8,.2,1)", "regras": [...]}`. Vira `--movimento-*` no `tokens.css`. Durações fora de 100 a 500 ms geram aviso.

**`tokens.css`** (gerado): `--produto-<id>`, `--produto-<id>-acento`, `--marca-acento`, `--fonte-marca` e `--movimento-*`. É o que a `px-migrar-ds` integra ao `index.css`.

## Campos opcionais (familia.campos e modulos[].campos)

Escolhidos na entrevista. O que estiver em `familia.campos` aparece no accordion de todo módulo; se o módulo não tiver o valor, aparece "Não definido". Nenhum é obrigatório: um sistema simples pode ficar só com marca, verbo e cor.

| Chave | Valor | Onde aparece / para quê |
|---|---|---|
| `acento` | `{"cor", "onde": ["item ativo do menu (16% no fundo)", "faixa de 3 px no header", ...]}` | A cor de interface do módulo e **sempre os mesmos lugares** onde ela entra. Pode ser diferente da cor da marca; o `contraste.py` avisa se ela não serve para texto ou ícone. |
| `textura` | `{"nome", "descricao", "svg": "<svg ...>"}` | Padrão de fundo (vidro, cabeçalho, card de destaque), com o SVG da peça que se repete, em traço branco. Use em opacidade baixa (5 a 8%). |
| `frase_home` | `{"texto", "fonte"}` | A pergunta ou frase que abre a home do módulo. `fonte`: de onde veio (deck, entrevista, proposta nossa). |
| `marca_animada` | `{"tipo": "respirar" \| "montar" \| "pulsar-agente", "descricao"}` | Carregamento, estado vazio, tela de abertura. A página mostra a animação; respeita `prefers-reduced-motion`. |
| `movimento` | `{"descricao", "duracao": "240ms", "curva": "cubic-bezier(.2,.8,.2,1)"}` | Assinatura de movimento do módulo (entrada de painel, transição). Só quando o módulo tem um movimento que o distingue. |
| `extras` | `[{"rotulo", "texto"}]` | Qualquer outro item próprio do módulo ("No ecossistema", "Só deste produto"). |

Lembre o UX: o que é de todos (componentes, tipografia, espaçamento, cores de estado) vem do DS e **não** entra aqui.
