# Contexto: paridade visual entre protótipo e implementação

> Documento de continuidade. Leia inteiro antes de mexer em qualquer coisa desta iniciativa.
> Não é instalado nos projetos: `install.mjs` copia `skills/` e `assets/`, não `docs/`.
> Última atualização: 25/08/2026 · px-skills 1.11.1

---

## 1. O objetivo

**A UI que o UX aprova é a UI que entra em produção, em qualquer projeto, sem reescrita e sem ninguém comparar tela no olho.**

Quatro condições:

1. O dev **copia** a interface em vez de reinterpretar
2. O que ele copia **compila** e resolve todos os imports
3. Divergência é **detectada por máquina**, com imagem, não por revisão
4. Vale para **todo projeto**, por padrão da esteira, não por esforço de quem está atento

Estado hoje: 1 e 2 feitos e publicados. 3 montado e **nunca executado**. 4 tem a regra publicada e nenhum projeto além do piloto migrado.

## 2. Onde cada coisa mora (não inverter a direção)

Isto é o que mais se erra nesta iniciativa, e foi o motivo de este documento existir. O trabalho é **genérico da esteira**, não de um produto. Artefato genérico dentro de repo de projeto vira cópia órfã que ninguém atualiza.

| O que | Casa canônica | Por quê |
|---|---|---|
| Skills e protocolo | **px-skills** | Já era a regra do repo |
| Regra de uso de componente, tokens, lints de código | **centralit-boilerplate** | Já era a regra do repo |
| Template do harness de paridade | **px-skills** (`assets/`) | Genérico, e todo projeto precisa |
| Gerador do PDF de requisitos | **px-skills** (`assets/`) | Genérico |
| Instância do harness (matriz de estados, exceções do produto) | **repo do projeto** | Só faz sentido com os dados daquele produto |
| Mapa de telas, pré-requisitos preenchidos | **pacote de handoff do projeto** | Instância |

**Regra prática:** se o arquivo funcionaria igual em outro produto trocando só nomes, ele é genérico e não mora no projeto.

## 3. O diagnóstico que originou tudo

A divergência visual entre protótipo aprovado e tela implementada **não vinha de desatenção do dev.** Vinha do formato da entrega.

A esteira mandava escrever a tela num arquivo só, com o andaime de demonstração (seletor de papel, seletor de estado, tema, mock) costurado dentro da interface. Para extrair a UI, o dev era obrigado a **editar**. Quem edita reescreve. Cada reescrita muda um espaçamento, uma variante, uma ordem.

Medido numa peça real, um card de produto: **18 decisões visuais que o design system não dita.** Uma delas um `text-[11px]`, fora da escala. Um dev seguindo o DS corretamente escreveria `text-xs` (12px), estaria certo, e a tela sairia diferente. Multiplicado pelas peças de um pacote, são centenas de decisões reproduzidas de olho.

O segundo problema, do mesmo tamanho: **o gate de saída do handoff conferia presença de arquivo e nunca executava nada.** Um pacote saiu montado com uma tela que não compilava e ficou cinco dias registrado como verde.

## 4. O que já está publicado

**centralit-boilerplate, PR #4, mergeado.** Publica `@centralit/tour`; corrige o bug do `navbar` (a prop `tooltip` no hambúrguer quebra sem `TooltipProvider`, e todo projeto novo herdava); sobe `check-camadas.mjs` e `check-tipografia.mjs`; escreve a regra das duas pastas no `CLAUDE.md`.

**px-skills 1.10.0, PR #3, mergeado.** `px-proto` passa a construir em duas pastas (Passo 5 reescrito, com template de UI, contrato, fixture e andaime). `px-handoff` ganha a seção PORTÃO EXECUTÁVEL.

**px-skills 1.11.0, PR #4, mergeado.** Ordem das histórias e rastreabilidade história para código: o `mapa-de-telas.md` passa a carregar ordem e ID estável, inventário de peças obrigatório, e `px-story` ganha as regras de numeração.

## 5. O que é genérico e está no lugar errado

Precisa ser movido para cá. Nada disso deveria estar num repo de projeto.

| Arquivo hoje | Destino |
|---|---|
| `<projeto>/handoff-ux/v1/paridade/paridade.spec.ts` | `assets/paridade/` |
| `<projeto>/handoff-ux/v1/paridade/hooks.ts` | `assets/paridade/` |
| `<projeto>/handoff-ux/v1/paridade/playwright.config.ts` | `assets/paridade/` |
| `<projeto>/handoff-ux/v1/paridade/README.md` | `assets/paridade/` como template; os números do produto saem |
| `<projeto>/handoff-ux/v1/paridade/gates.md` | O conteúdo é a esteira. Vira seção da `px-handoff` ou do `px-protocol.md` |
| `<projeto>/tools/gerar-pdf-qa.mjs` + README | `assets/tools/` |
| `pre-requisitos.md` (os 7 itens genéricos) | Template em `assets/`; o preenchido fica no projeto |

**Fica no projeto, porque é instância:** `matriz-estados.json`, as entradas de `excecoes.md`, `mapa-de-telas.md`, `pre-requisitos.md` preenchido.

**Decisão tomada em 25/08/2026: o `install.mjs` NÃO copia o harness.** Ele continua copiando só `assets/design-system/*` e `assets/px-protocol.md`. O harness vai para `assets/paridade/` como **template do repo da esteira**, e quem precisa copia.

Motivo: projeto que não usa Playwright receberia arquivo que não roda, e arquivo que não roda dentro de um projeto é exatamente a cópia órfã que a seção 2 existe para evitar — só que multiplicada por todo projeto instalado.

**O custo dessa escolha é real e fica registrado:** a adoção do harness passa a depender de alguém lembrar, o que arranha a condição 4 do objetivo (valer por padrão da esteira, não por esforço de quem está atento). O contrapeso não é o instalador, é a `px-handoff`: o portão executável é quem cobra, e cobrar no portão não deixa arquivo morto em projeto nenhum. Se depois do piloto da seção 7 ficar claro que a cobrança no portão não basta, esta decisão volta para a mesa.

## 6. As três armadilhas de falso verde — corrigidas em 25/08/2026

Eram duas conhecidas, e uma terceira apareceu ao mexer. Todas do mesmo tipo, que é o mais perigoso: **portão que fica verde sem ter verificado nada.**

**`lint:camadas` era opt-in.** Ele só rodava se o projeto declarasse `camada: ui` no README da pasta de UI. Sem isso, imprimia "nenhuma camada declarada" e **saía com sucesso** — o mesmo defeito do `tsc` sem `-p` que esta iniciativa existe para combater.
*Corrigido:* falha quando existe `src/proto/` com arquivos `.tsx` e nenhuma camada declarada. Se existe andaime, tem que existir camada.
*Provado contra erro plantado:* `✖ check-camadas: existem 1 arquivo(s) de tela em src/proto/ e nenhuma camada de UI declarada`, exit 1. Projeto legítimo sem andaime continua exit 0.

**O gate não detectava projeto ainda misturado.** Se a UI nunca foi extraída, não existe import da UI para fora, e a regra de import fica verde num projeto totalmente misturado.
*Corrigido:* mede o tamanho dos arquivos do andaime. Limite 300 linhas, que é o dobro do topo da faixa documentada (100 a 150) — folga para variação sem deixar passar o caso real de 800 linhas. **Fixtures ficam fora da regra:** são dados puros e crescerem é esperado; acusar fixture seria falso positivo, e gate com falso positivo o time aprende a ignorar.
*Provado contra erro plantado:* andaime de 802 linhas → `✖ 1 arquivo(s) de andaime grande(s) demais (limite: 300 linhas)`, exit 1, com fixture de 900 linhas no mesmo diretório **não** acusada.

**O comando de ordem dos CA estava publicado quebrado** (descoberto em 25/08). A `px-handoff` 1.11.0 anunciou o comando no portão executável; ele foi gravado por heredoc não citado, o shell expandiu o `'^$'` do `grep -v`, e o bloco saiu cortado no meio da terceira linha. Cerca de código aberta, 95 linhas do arquivo duplicadas. Colar no terminal dava erro de sintaxe.
*Corrigido na px-skills 1.11.1:* bloco restaurado, duplicata removida (495 → 393 linhas), e o comando agora **devolve código de saída** — a versão original só imprimia `FORA DE ORDEM:` e terminava em 0, ou seja, mesmo inteiro era um gate que não podia falhar.
*Provado contra erro plantado:* `CA-1 CA-3 CA-2` → `FORA DE ORDEM`, exit 1.

## 7. A suposição mais arriscada, e ela não foi testada

**Nenhum dev consumiu o pacote ainda.** O modelo inteiro depende de uma suposição sem evidência: que "copie a pasta e não edite" funciona no repositório deles.

Não sabemos se o alias resolve, se o Tailwind deles compila as classes, se o roteador pluga onde previmos, se o hook de sessão do harness é preenchível com a autenticação que eles têm. O `pre-requisitos.md` lista os sete pontos de falha conhecidos, mas conhecido não é testado.

**O que fazer antes de escalar a regra para todos os projetos:** um piloto de uma tela só, a menor. O dev pluga no repositório dele e roda. Se copiar sem editar uma linha, a suposição está validada. Se precisar editar, descobrimos onde o modelo quebra com uma tela em vez de com cinco, e corrigimos na origem antes de virar padrão.

É o teste mais barato e mais informativo disponível. Tudo que for construído sem ele é aposta.

## 8. O ângulo que ainda não foi trabalhado

Tudo que existe hoje assume **handoff**: um instantâneo copiado num momento. Isso resolve "a primeira entrega sai fiel" e **não** resolve "continua fiel".

No instante em que o dev copia, as duas versões bifurcam. Nossa correção não chega nele, a dele não chega em nós, e cada delta é um pacote novo, uma cópia nova, uma bifurcação nova. O harness detecta o afastamento; ninguém é dono de fechar.

O ângulo alternativo: **publicar a camada de UI do produto pelo registry**, como o design system já é. Um delta deixa de ser pacote e passa a ser `npx shadcn add @<produto>/<tela>` de novo, com versão. A cópia do dev fica rastreável a um número.

A separação em duas pastas é a pré-condição disso. Implica decidir quem mantém a camada, e por isso não foi feito.

## 9. Pendências abertas com terceiros

**Do time de desenvolvimento** (pedidos meus, sem resposta ainda):
- A linha exata das flags do Chrome headless para hover. **Item mais urgente:** sem ela, as comparações de foco e hover do harness comparam dois estados de repouso, ou seja, cobertura falsa. Melhor remover o bloco do que entregar verde sem medir.
- Os 6 pontos restantes das 9 divergências deliberadas que eles relataram.
- Quantos componentes o kit deles tem e quais divergem, em especial o que corrige a direção do hover, que é fix deles que não temos.
- Como semear carregando, vazio e erro pela resposta de rede. Se der para forçar nos dois lados, esses estados saem do "fora de escopo" e entram na comparação automática.

**Nosso, sem dono:** o drift entre projeto e design system. Projetos ficam arquivos atrás sem nada avisar. Exige skill própria ou ligar o `DesignSync`.

**Projetos não migrados:** dois apps React no boilerplate continuam com UI e andaime misturados, e um deles não usa a pasta `proto/`, então o gate nem ativa lá. Precisa de decisão de convenção antes da migração. Outros dois projetos entregam HTML standalone e não têm caminho de paridade nenhum.

## 10. Armadilhas técnicas já pagas (não reintroduza)

**`npx tsc --noEmit` sem `-p` compila zero arquivo e sai com sucesso.** O `tsconfig.json` da raiz do boilerplate tem `"files": []` e só `references`. Medido: com erro de tipo plantado, sem `-p` dá exit 0 e nenhuma linha; com `-p tsconfig.app.json` dá exit 2 e a mensagem. **Todo gate novo tem que ser rodado uma vez contra erro plantado**, e a mensagem registrada. Sem essa prova, não conte o gate.

**`npm run lint` é corrente com `&&` começando pelo oxlint.** Se o oxlint acha erro, os lints do DS não rodam e a saída não deixa claro. Ao investigar falha, rodar cada um separado.

**`check-caixa-alta` tem falso positivo** com identificador em maiúscula dentro de template literal (`${TINT[x]}` foi acusado como copy em caixa alta). Gate que dá falso positivo é gate que o time aprende a ignorar. Vale corrigir a heurística.

**PDF do pdfkit: rodapé abaixo da margem cria página.** Escrever o número da página fora da área útil faz o pdfkit entender transbordo e abrir página nova, uma por rodapé. Gerou 111 páginas em vez de 37. Correção: zerar `page.margins.bottom` antes de escrever e restaurar depois.

**PDF do pdfkit: `grep` não serve para verificar conteúdo.** Ele faz kerning e quebra as palavras em glifos separados, então busca por substring nunca acha, mesmo sem compressão. Usar extrator de verdade (`pdfjs-dist`).

**Glifo fora de Latin-1 vira caixa preta no PDF.** As fontes padrão do pdfkit são WinAnsi. Trocar por equivalente ASCII, não remover.

**Contradição entre `description` e corpo da skill faz a trava ganhar.** A própria 1.8.1 documentou isso, e eu repeti na 1.10.0: a `description` do `px-proto` anunciava que o protótipo não é código de produção, contradizendo a regra nova. Ao mudar regra central de uma skill, revisar `description` e introdução.

**Heredoc não citado mutila o arquivo em silêncio.** Gravar bloco de shell dentro de um `.md` com `<<EOF` faz o shell expandir `$`, crase e `\` do conteúdo. Foi o que cortou o comando de ordem dos CA no meio e duplicou 95 linhas da `px-handoff` (seção 6). Não houve erro na gravação: o comando terminou com sucesso e o arquivo saiu mutilado. **Sempre `<<'EOF'`, com o delimitador citado.** Depois de gravar, confira contando as cercas de código do arquivo: número ímpar denuncia bloco aberto, e número par não prova pareamento correto, então olhe também as posições.

## 11. Como verificar que está tudo de pé

```bash
# no repo de um projeto que usa o boilerplate
npx tsc --noEmit -p tsconfig.app.json   # 0 erros
npm run lint                            # inclui lint:camadas
npm run lint:tipografia                 # fora da corrente, decisão pendente
npm run build
```

```bash
# ordem dos critérios de aceite, dentro do pacote de handoff
( falhas=0
  for f in $(find . -path "*/stories/*.md"); do
    seq=$(grep -oE "CA-[0-9]+" "$f" | sed 's/CA-//' | awk '!v[$0]++' | tr '\n' ' ')
    ord=$(echo "$seq" | tr ' ' '\n' | grep -v '^$' | sort -n | tr '\n' ' ')
    [ "$seq" = "$ord" ] || { echo "FORA DE ORDEM: $f"; falhas=$((falhas + 1)); }
  done
  [ "$falhas" -eq 0 ] || { echo "✖ $falhas história(s) com CA fora de ordem"; exit 1; }
  echo "✔ CA em ordem em todas as histórias" )
```

## 12. Ordem sugerida para retomar

1. ~~Consertar as armadilhas da seção 6.~~ **Feito em 25/08/2026**, e virou três em vez de duas. As três rodadas contra erro plantado.
2. **Mover o que a seção 5 lista.** A decisão do `install.mjs` está tomada (não copia), então o destino de cada arquivo está definido: harness e gerador de PDF para `assets/`, instâncias ficam no projeto. Separar template de instância arquivo por arquivo, não mover a pasta inteira.
3. **Rodar o piloto da seção 7** antes de migrar mais projeto. É o que valida ou derruba a suposição central.
4. Só então migrar os projetos pendentes.

O item 3 tem prioridade sobre o 4 mesmo parecendo menor. Migrar cinco telas de um projeto com o modelo não validado é multiplicar por cinco um retrabalho possível.

Nenhum dos itens está esperando decisão: a do `install.mjs` saiu em 25/08. O item 3 depende de agenda com o time de desenvolvimento, e é o único com dependência externa.
