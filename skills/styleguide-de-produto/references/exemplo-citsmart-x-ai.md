# Exemplo: família Lâmina e ponto (CITSmart X AI, novembro de 2026)

O caso que originou a skill. Serve para mostrar o método funcionando, **não** para copiar a linguagem: outro sistema tira as regras da própria marca-mãe.

- Página: https://claude.ai/artifact/7BXggFg6SmZZPjZejapHLu
- Scripts originais: repositório `px-projects`, pasta `citsmart-x-front-manager/planning/marcas/` (`formas.py`, `gerar.py`, `paleta.py`, `produtos.json`, `README.md`).

## Como cada fase aconteceu

1. **Entrevista.** Sete produtos, cada um com um verbo do ciclo: Hive detecta, Autonomous age, ITSM registra, GRCS comprova, Agility executa, Aura conversa, HyperAgents orquestra. Marca-mãe: a marca oficial do Autonomous (escolhida pelo Derick), com guia da marca. Fundo da aplicação `#EEF0F4`. Acento: o verde-limão da IA (`#A6CE39`). Reservadas: roxo, a escala de criticidade e o próprio verde-limão.
2. **Regras.** A primeira proposta repetia a lâmina e o quadrado em todos os produtos e foi **recusada**: família não é o mesmo símbolo repetido. A segunda tirou seis regras da marca do Autonomous: grade de 64 com a mesma área; só cortes retos; peças sólidas separadas por vão; inclinação de 2:1 nas diagonais; uma peça é o agente, em verde; uma cor só na interface.
3. **Formas.** Cada produto ganhou forma ligada ao verbo: favo partido com a célula encontrada no centro (Hive), três linhas de um chamado (ITSM), visto em duas peças (GRCS), dois chevrons (Agility), aspas (Aura), seis agentes em volta de um núcleo (HyperAgents). O Autonomous ficou como estava. A peça do agente de cada um foi escolhida junto com a forma.
4. **Cores.** Uma cor fria por produto, todas com pelo menos 3:1 no branco e no `#EEF0F4` (de 4,2:1 no Hive a 18,4:1 no HyperAgents), sem roxo, sem criticidade e sem o verde da IA.
5. **Página.** Marcas, regras, tabela de contraste, header claro e escuro a 24 px, tamanhos de 16 a 64, e um accordion por produto com acento no protótipo e cor proposta, textura do vidro, pergunta da home, desenho do Morning Call, papel no ecossistema e o que falta decidir.
6. **Entrega.** SVGs em quatro versões em `proto-react/public/marca/produtos/`; a versão `-escuro-acento` virou a fonte do desenho de pixels do Morning Call de cada produto.

## O que aprendemos

- **A forma vem do verbo, não do nome.** "Comprova" deu o visto; "GRCS" não daria nada.
- **A peça de acento dá unidade** mais do que qualquer forma repetida: o verde aparece sempre numa peça só, com um significado em cada produto.
- **Conferir contraste antes de mostrar.** Duas cores do protótipo (o teal do Hive e o do Autonomous) eram quase iguais e não passavam 3:1 no fundo; o script pegou isso.
- **Deixar o que falta decidir na página.** Uma cor por produto ou uma só, qual peça é o agente e a validação com o dono da marca ficaram visíveis para todo mundo.
- **Campos opcionais saíram do protótipo,** não de uma lista pronta: textura, pergunta da home e Morning Call existiam no X AI. Em outro sistema, pergunte o que existe lá.

## Em formato de dados

A marca do Autonomous no formato desta skill:

```json
{"id": "autonomous", "nome": "Autonomous", "verbo": "Age", "cor": "#0B6FA4",
 "porque": "A lâmina e o ponto formam um A, pronto para agir.",
 "pecas": [
   {"tipo": "poligono", "pontos": [[12, 54], [34, 10], [47, 10], [25, 54]]},
   {"tipo": "retangulo", "x": 40, "y": 42, "largura": 12, "altura": 12, "agente": true}
 ]}
```
