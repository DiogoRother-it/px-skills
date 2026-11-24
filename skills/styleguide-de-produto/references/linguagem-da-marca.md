# Fase 3: linguagem e estilo

O que faz várias marcas parecerem família não é repetir um símbolo em todas (essa foi a proposta recusada no X AI: mesma lâmina e mesmo quadrado em todos), é **a mesma gramática com formas diferentes**. A fase 3 escolhe o estilo e descreve essa gramática em 4 a 6 regras.

A referência é o **logo aprovado na fase 2** ou, se ele não existir, a marca-mãe.

## Estilo

Pergunte (`AskUserQuestion`), com a recomendação que a referência sugere. Qualquer estilo serve; o que importa é ser um só na família. Como cada um vira dado (`familia.estilo` e as primitivas em [`campos-do-styleguide.md`](campos-do-styleguide.md#formas)):

| Estilo | Combina com | No produtos.json |
|---|---|---|
| **Geométrico sólido** | marcas de corte reto, peças cheias (o X AI) | padrão: primitivas sem `estilo` |
| **Contorno** | linguagem leve, técnica, de ícone | `"estilo": {"preenchimento": "contorno", "traco": 4}` |
| **Arredondado** | marcas amigáveis, educação, saúde, varejo | `"estilo": {"cantos": "redondos", "raio": 2}` (soma com contorno) |
| **Gradiente** | marcas de tecnologia, IA, consumo | `"estilo": {"gradiente": true}` + `cor2` no logo e em cada módulo |
| **Monograma / letra** | produto conhecido pela sigla | peça `{"tipo": "texto"}` (para entregar, converta em curvas) |
| **Desenho livre / ilustrado** | curvas orgânicas, mascote, traço à mão | peça `{"tipo": "path", "d": "..."}` |
| **Feito fora (Figma, Illustrator)** | quando o UX desenha e só quer o sistema em volta | peça `{"tipo": "arquivo", "caminho": "x.svg"}` |

Alerta para o UX, antes de aprovar: gradiente, ilustração e detalhes finos perdem leitura a 16 px. Se o estilo escolhido não lê pequeno, proponha uma versão simplificada para 16 e 24 px e registre como pendência.

## Como olhar a referência

Abra o SVG (ou redesenhe o PNG numa grade de 64) e responda, anotando a medida:

| Pergunta | Exemplos de resposta |
|---|---|
| **Grade e área.** Quanto da grade de 64 ela ocupa? Tem margem? | "ocupa de 10 a 54", "encosta nas bordas" |
| **Corte.** Só retas? Curvas? Que tipo de curva? Canto vivo ou arredondado? | "só cortes retos", "arcos de círculo", "cantos com raio 4" |
| **Espessura.** As peças têm traço constante? Quanto? | "traço de 8", "peças cheias, sem traço" |
| **Peças e vão.** É uma peça ou várias? Quanto de vão entre elas? | "duas peças com vão de 4" |
| **Ângulos.** Que diagonais aparecem? | "inclinação de 2:1", "só 45°", "sem diagonal" |
| **Cor.** Uma cor? Duas? Uma peça de destaque? | "uma cor, o ponto em verde" |
| **O que não tem.** Sombra, gradiente, contorno, textura. | "nada de gradiente nem sombra" |

## Como escrever cada regra

- **Verificável:** dá para olhar uma marca nova e dizer sim ou não. "Moderna" não é regra; "só cortes retos" é.
- **Ligada à referência:** cada regra cita a origem ("a mesma inclinação da lâmina").
- **Curta, com o núcleo em negrito:** `**Inclinação de 2:1** sempre que há diagonal, a mesma da lâmina.` O `pagina.py` transforma `**…**` em negrito.
- **Entre 4 e 6.** Menos que 4 não segura a família; mais que 6 ninguém lembra.

Uma regra quase sempre presente: **qual peça é o acento** (o "agente", o "ponto", o "aluno") e o que ela significa em cada módulo. É ela que dá o "uma peça de cada marca muda de cor".

## Regras que valem sempre (não entram nas 4 a 6, já estão nos scripts)

- Grade de 64 e mesma área aproximada (o `formas.py verificar` mede a tinta).
- Legível a 16 px: peça fina demais some; vão menor que 3 na grade de 64 fecha.
- Uma cor na interface; a versão com acento é para fundo escuro e materiais de marca.

## Gate

Regra ou estilo que não sai da referência (por exemplo, "sem diagonal" quando a marca-mãe tem uma diagonal) é decisão nossa: marque **⚠️ REQUER VALIDAÇÃO UX/PX** e não avance sem o ok.

## Exemplos

- **CITSmart X AI (Lâmina e ponto):** grade de 64; só cortes retos; peças sólidas separadas por vão; diagonal em 2:1; uma peça é o agente, em verde; uma cor só na interface.
- **Sala Viva (exemplo fictício, `exemplo/produtos.json`):** grade de 64; traço único de 8; curva só em arco de círculo; sem diagonal; o ponto é o aluno.
