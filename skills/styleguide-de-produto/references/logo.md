# Fase 2: logo do produto

O logo vem antes das marcas dos módulos, porque é dele (ou da marca-mãe) que sai a linguagem da família. Uma pergunta de cada vez, com o porquê e um padrão recomendado.

## 1. A decisão

`AskUserQuestion`:

- **Manter o logo atual** (Recomendado quando o logo é conhecido pelos clientes e está em bom estado): só documentamos (arranjos, proteção, mínimo, proibidos).
- **Refinar** (Recomendado quando a ideia é boa e o desenho está ruim: bitmap, detalhe que some a 16 px, muitas cores, fonte genérica): mesma ideia, desenho novo na grade.
- **Criar um novo**: o produto não tem logo, ou o atual não serve mais. Peça quem aprova (normalmente o PO e quem cuida da marca da empresa).

Peça sempre o arquivo do logo atual, se existir (SVG de preferência).

## 2. Briefing (refinar ou criar)

Uma de cada vez. Grave em `familia.logo.briefing`.

1. **O que o produto faz, em uma frase, para quem.** *Por quê:* o símbolo nasce do que o produto faz, como as marcas dos módulos nascem do verbo.
2. **O que o logo precisa transmitir.** Três palavras, no máximo (ex.: "confiança, rapidez, simples"). Ofereça exemplos ligados ao produto.
3. **O que evitar.** Clichês do setor (cadeado em segurança, engrenagem em TI, chapéu de formatura em educação), cores de concorrente, qualquer coisa que o cliente rejeitou antes.
4. **Referências.** Logos de que o UX ou o PO gostam, e por quê. A marca da empresa ou da área, se o produto precisa parecer da família.
5. **Composição** (`AskUserQuestion`): símbolo + nome (Recomendado: o símbolo sozinho vira favicon e marca de módulo), só nome (logotipo), ou monograma (letras).
6. **Estilo de partida** (`AskUserQuestion`): geométrico sólido, contorno, arredondado, gradiente, monograma, desenho livre, ou "propor três estilos diferentes" (Recomendado quando o UX não tem preferência). O estilo final se fecha na fase 3.
7. **Onde vai viver.** Header (24 px), favicon (16 px), login, e-mail, apresentação, impresso. *Por quê:* define o tamanho mínimo e se precisa de uma versão só com o símbolo.
8. **Nome.** Como o nome aparece no logo: grafia, maiúsculas e minúsculas, com ou sem o nome da empresa.

## 3. Opções

2 ou 3 opções em `familia.logo.opcoes`, cada uma com um `porque` que cita o briefing ("o anel aberto é a turma, como pedido em *acolhimento*"). Quando o UX pediu "propor três estilos", cada opção é um estilo diferente.

Para opções em estilos diferentes, o `familia.estilo` vale para todas: use `"contorno": true/false` na peça, ou desenhe a opção como `path` ou `arquivo`. Mostre no canvas (`formas.py canvas`) e pergunte qual fica (`AskUserQuestion` com as opções + "Misturar ou refazer").

## 4. Documentar o escolhido

Em `familia.logo`:

| Campo | Padrão | O que é |
|---|---|---|
| `nome` | o nome do sistema | como o nome aparece no logo |
| `cor`, `cor2`? | — | cor do símbolo no claro (e a segunda cor, se houver gradiente) |
| `cor_texto` | `#0E1420` | cor do nome no claro (precisa de 4.5:1) |
| `arranjos` | `["simbolo", "horizontal", "vertical"]` | quais versões gerar |
| `protecao` | `0.25` | área livre em volta, em fração da altura do símbolo |
| `minimo_px` | `24` | altura mínima; abaixo disso, só o símbolo |
| `proibidos` | — | 3 a 5 usos proibidos (mudar cor, distorcer, sombra, fundo sem contraste) |
| `decisao`, `porque`, `briefing` | — | aparecem na página |

## Quando o UX traz o logo pronto

Coloque o SVG na pasta `marcas/` e use `{"tipo": "arquivo", "caminho": "logo-atual.svg"}` nas peças. O script lê os `<path>` e ajusta à grade de 64. Se o SVG tiver texto, gradiente ou máscara, peça ao UX para exportar com o texto convertido em curvas e uma cor só por peça.
