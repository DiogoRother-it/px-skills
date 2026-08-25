# Changelog

Todas as versões instaláveis via `npx github:DiogoRother-it/px-skills` / `npx @centralit/px-skills`.
O instalador imprime só a versão mais recente no terminal — o histórico completo vive aqui.

## 1.11.1 — 2026-08-25

**O comando que a 1.11.0 acrescentou ao portão executável foi publicado quebrado, e o arquivo da skill saiu com 95 linhas duplicadas.** Correção de defeito. Nenhuma regra nova.

A 1.11.0 fechou com "novo item no portão executável: verificação de que os critérios de aceite estão em ordem crescente, com o comando pronto". O comando **não estava pronto**: foi gravado por um heredoc não citado, o shell expandiu o `'^$'` de dentro do `grep -v`, e o bloco terminou cortado no meio da terceira linha. O que estava publicado era isto:

```
  ord=$(echo "$seq" | tr ' ' '\n' | grep -v '^
```

A cerca de código ficou aberta, o resto do arquivo foi remontado fora de ordem, e o trecho de `### O -p não é detalhe` até `## Relação com o fluxo` apareceu **duas vezes**, idêntico. Quem colasse o comando no terminal recebia erro de sintaxe.

É o mesmo defeito que esta seção do arquivo existe para combater, na forma mais direta possível: **o gate que verifica a ordem dos critérios não podia rodar.** Ficou cinco versões contado como cobertura e nunca executou.

**Correção:**
- Bloco restaurado inteiro e cercas de código repareadas.
- 95 linhas duplicadas removidas (arquivo de 495 para 393 linhas). O conteúdo das duas cópias era idêntico; nada de regra se perdeu.
- **O comando agora devolve código de saída.** A versão anterior só imprimia `FORA DE ORDEM:` e terminava com exit 0 — ou seja, mesmo se tivesse sido publicado inteiro, era um gate que não podia falhar. Agora conta as falhas e sai 1. O `exit` está dentro de parênteses de propósito: o bloco é feito para ser colado num terminal e precisa devolver código sem derrubar a sessão de quem colou.
- **Rodado contra erro plantado**, como a própria seção manda. Com `CA-1 CA-3 CA-2` numa história: `FORA DE ORDEM: ./stories/quebrado.md`, `✖ 1 história(s) com CA fora de ordem`, exit 1. Com a ordem certa: `✔ CA em ordem em todas as histórias`, exit 0.

**Regra que fica:** ao gravar bloco de shell dentro de arquivo por heredoc, o delimitador vai **citado** (`<<'EOF'`). Sem as aspas o shell come `$`, crase e `\`, e o estrago aparece calado — não houve erro na gravação, só um arquivo mutilado.

**Do lado do `centralit-boilerplate`** (PR próprio), as duas armadilhas de falso verde do `check-camadas.mjs`: ele deixou de sair com sucesso quando existe `src/proto/` e nenhuma camada de UI declarada, e passou a acusar arquivo de andaime acima de 300 linhas, que é o sinal de UI ainda misturada. Fixtures ficam de fora da regra de tamanho.

---


## 1.11.0 — 2026-08-24

**A cadeia tirou o número do nome do arquivo e não colocou a ordem em lugar nenhum.** O gate da `px-handoff` exigia "nomes de arquivo sem prefixos numéricos", com razão: número em nome de arquivo envelhece na primeira história que entra no meio e passa a mentir. Só que a ordem foi embora com ele. O time de desenvolvimento reclamou de duas coisas, e as duas eram nossas: *"não está sendo gerado com ordenação numérica correta"* e *"está difícil de identificar onde a história se reflete no protótipo"*.

Auditando um pacote real, as duas se confirmaram, uma delas de forma mais concreta do que a reclamação sugeria:

- **Não havia ordem alguma** entre os fluxos. Um arquivo de história por fluxo, sem número e sem indicação de por onde começar.
- **Dentro de uma história, os critérios estavam fora de ordem de verdade.** Na história da matriz, os `CA-13`, `CA-14` e `CA-15` estavam entre o `CA-08` e o `CA-09`. Causa: quando um delta acrescenta critérios a uma história já escrita, eles recebem o próximo número livre mas são inseridos onde o assunto encaixa. Quem lê de cima para baixo vê a numeração pular.
- **O `mapa-de-telas.md`, que a 1.9.0 tornou obrigatório justamente para resolver a rastreabilidade, não existia no pacote.** A reclamação do dev era literalmente o artefato que a gente definiu como obrigatório e não entregou.

**`px-handoff`:**
- **O `mapa-de-telas.md` passa a carregar ordem e identificador estável**, não só localização: `# | ID | Fluxo | Tela | Rota | Arquivo da UI | História | Depende de`. A coluna de ordem exige **o motivo escrito em prosa** logo abaixo da tabela, porque ordem sem motivo o dev ignora na primeira pressão de prazo.
- **Inventário de peças obrigatório no mapa** (arquivo → o que é → em quais fluxos aparece). É o que responde "onde isto vive" quando o critério fala de um card, um modal, uma linha ou um selo em vez de da tela inteira. Só é útil com a UI em arquivos separados: num arquivo único de 600 linhas o ponteiro não ajuda ninguém, e é por isso que este item só faz sentido depois da separação de camadas da 1.10.0.
- **A regra de não usar prefixo numérico ganhou a contrapartida explícita.** As duas andam juntas: tirar o número sem colocar a ordem em outro lugar deixa o dev sem saber por onde começar.
- **Novo item no portão executável:** verificação de que os critérios de aceite estão em ordem crescente em cada história, com o comando pronto.

**`px-story`:**
- **Numeração crescente e contígua**, com a ordem no arquivo batendo com a numeração.
- **Regra para delta:** critério novo recebe o próximo número livre e é **inserido na posição numérica**, não no fim da seção.
- **Nunca renumerar para consertar.** Os identificadores são referenciados pelos cenários BDD e pelas regras de negócio; renumerar quebra a rastreabilidade. Reordenar as linhas, mantendo cada número onde nasceu.
- **ID estável no cabeçalho** da história, mais a ordem de implementação e o arquivo da UI onde ela vive.
- Dois itens novos na DoR.

---

## 1.10.0 — 2026-08-24

**A cadeia entregava o fonte, e o dev continuava obrigado a reescrever.** A 1.8.0 abriu o caminho do fonte e a 1.9.0 tirou o bundle do pacote, mas o `px-proto` continuava mandando escrever a tela num arquivo só, com o seletor de papel, o seletor de estado, a alternância de tema e o mock data costurados dentro da própria interface. Na prática o dev recebia código que não conseguia importar: para arrancar o andaime ele tinha que editar, e quem edita reescreve. Toda reescrita muda um espaçamento, uma variante, uma ordem. Medimos numa peça só, o card de produto de um projeto real: **18 decisões visuais que o design system não dita**, sendo uma delas um tamanho de fonte fora da escala que um dev seguindo o DS corretamente escreveria diferente, estando certo. Multiplicado pelas peças de um pacote, são centenas de decisões reproduzidas de olho. Era essa a causa raiz da divergência visual, e nenhuma revisão humana pega isso de forma confiável.

O outro lado do mesmo problema: o **gate de saída da `px-handoff` conferia presença de arquivo e nunca executava nada**. Um pacote foi montado com uma tela que não compilava e ficou cinco dias registrado como verde. Presença de arquivo não é verificação.

**`px-proto` — a tela nasce em duas pastas, e isso vira a regra central da skill:**
- **Passo 5 reescrito de um arquivo para dois.** `src/<produto>/tela-<slug>.tsx` guarda a **UI, que é destinada à produção** e é entregue com a instrução de copiar sem editar; `src/proto/page-<slug>.tsx` guarda o **andaime**, descartável. A dependência é direcional: o andaime conhece a UI, a UI nunca conhece o andaime. Com templates para os quatro arquivos (UI, contrato, fixture, andaime).
- **A regra que dizia que o protótipo inteiro é descartável foi corrigida.** Era ela que produzia código inaproveitável. Só `src/proto/` é jogado fora.
- **Contrato de dado declarado pela forma do contrato, nunca `typeof MOCK[0]`.** Duas regras que nasceram de divergência real em pacote entregue: *ausente não é vazio* (campo que pode não existir é opcional, nunca string vazia fazendo papel de ausência) e *variante é união discriminada* (não tipo largo com tudo opcional). Sem isso, a decisão de exibição acaba no adaptador que o dev escreve, e cada adaptador decide diferente.
- **Fixture única**, de dados puros, em `proto/fixtures.ts`. Tela não declara mock próprio. Não é organização: é pré-requisito do aceite visual, porque conteúdo divergente faz o diff acusar diferença de dado em vez de diferença de implementação, e o desfecho previsível é alguém subir a tolerância até o teste calar.
- **Sinal de sanidade verificável:** o arquivo do andaime fica em 100 a 150 linhas independente do tamanho da tela. Passou disso, tem UI vazando para dentro dele.
- **`description` e introdução alinhadas ao corpo.** A 1.8.1 já ensinou que trava contradizendo o corpo faz a trava ganhar: a `description` anunciava que o protótipo não é código de produção, o que passou a contradizer a regra nova.

**`px-handoff` — portão que executa, antes do portão que confere:**
- **Seção nova PORTÃO EXECUTÁVEL**, com sete comandos e a saída colada no eco final. Vem antes do gate de conteúdo, que continua existindo.
- **A armadilha do `-p` documentada com número medido.** `npx tsc --noEmit` sem o `-p` compila **zero arquivo** e sai com sucesso, porque o `tsconfig.json` da raiz do boilerplate tem `"files": []` e só `references`. Com erro de tipo plantado: sem `-p`, exit 0 e nenhuma linha de saída; com `-p tsconfig.app.json`, exit 2 e a mensagem. Um portão falso é pior que portão nenhum.
- **Regra: gate novo tem que ser provado contra erro plantado** e a mensagem registrada. Sem essa prova, não conte o gate.
- **Tabela de dependências passa a ser derivada por grep, nunca escrita à mão.** Escrever à mão garante que vai divergir do código, e as entradas que faltarem serão justamente as que quebram o build do dev. Aconteceu: faltavam duas, e eram as duas fatais.
- **Checklist de pacote atualizado** para as duas pastas com instrução oposta, o README da camada de UI, a fixture única, o gate de camadas verde, e a pasta `paridade/` com a ordem de precedência (**o contrato do DS vence o protótipo**, e diff nesse ponto não é falha de paridade) mais a lista versionada de exceções com motivo, dono e data. Sem essa linha, o aceite "harness verde" obriga o dev a reimportar defeito nosso para o teste passar.

**No boilerplate** (repositório separado, já mergeado): `check-camadas.mjs` barra import da camada de UI para `proto/`, ativado por declaração `camada: ui` no README da pasta; `check-tipografia.mjs` barra tamanho fora da escala, peso acima de 700 e altura de controle fora de 32/40/48.

---

## 1.9.0 — 2026-08-21

**O caminho do fonte existia, mas o pacote continuava podendo levar o bundle, e nada garantia que o código entregue fosse reusado em vez de reinterpretado.** A 1.8.0 passou a entregar `src/proto/**` quando a stack é a mesma, e ainda dizia que *"o build compilado pode ir também, como visualizador"*. Ou seja: o arquivo mais pesado e mais irreversível que a gente coloca no repo do dev continuava autorizado, justamente no caminho em que ele não acrescenta nada, porque o `proto/` roda. Faltavam também a visão geral das telas (a única crítica de ferramenta de design que um repo não responde de graça), a rastreabilidade em arquivo separado, e a lista do que precisa existir no app do dev para o fonte renderizar igual.

**`px-handoff` — quatro fechamentos no caminho do fonte:**
- **Bundle não entra mais como arquivo.** Ele continua existindo para visualizar e para o PO revisar, mas **publicado**, com o link no `README.md` do pacote. Sem lugar para publicar ainda, vira pendência no `handoff.md` — nunca arquivo. Também listado no `handoff-manifest.md` como o que não entra neste caminho.
- **Nova seção "O recorte: o que preservar, o que reescrever"**, obrigatória no `README.md` do pacote. Markup, classes e tokens, estrutura dos estados de UI e breakpoints são para reusar; roteamento, integração, organização de arquivos, testes e performance são livres. A tabela de propriedade diz de quem é a responsabilidade; esta diz o que acontece com o código, e é ela que faz o resultado sair igual em vez de parecido. O motivo está escrito: reusar é mecânico, reinterpretar não, e quem reinterpreta pode ser uma IA que não pergunta quando fica em dúvida.
- **`mapa-de-telas.md` obrigatório** (`Tela | Rota | Arquivo em proto/ | Histórias`). Resolve três coisas com um arquivo: dá a visão geral que um repositório não dá de graça, aponta onde cada tela vive, e move a rastreabilidade história ↔ componente para **arquivo separado**, em vez de escondida dentro da marcação — que era exatamente a crítica correta que veio dos devs.
- **`pre-requisitos.md` obrigatório**, com 7 itens conferíveis do lado do dev: major do framework e do Tailwind, arquivo de tokens presente e atual, fonte carregada no HTML, plugin de animação, alias de import resolvendo, mesma estratégia de dark mode, e nenhuma classe montada por concatenação de string. São as sete formas conhecidas de o fonte chegar certo e renderizar diferente, e todas falham **em silêncio**. Conferíveis antes de virar retrabalho.

**DoD** ganhou um item por promessa, para que nenhuma delas possa ser afirmada sem estar no pacote.

---

## 1.8.1 — 2026-08-21

**A 1.8.0 abriu o caminho do fonte e esqueceu de desarmar as travas que o proibiam.** O corpo da `px-handoff` passou a mandar entregar `src/proto/**` quando a stack do dev é a mesma, mas a `description` da skill continuava anunciando *"não envia código-fonte"*, o item da DoD continuava exigindo *"nenhum código-fonte (`.tsx`/`.ts`/`.jsx`/`.js` de componente)"* e o `handoff-manifest.md` mantinha código de componente em **🔒 Interno (nunca entra)**. Na prática as travas ganhavam: a `description` enquadra a skill inteira e a DoD é o portão de saída, então o caminho do fonte existia no texto e não acontecia na execução.

**`px-handoff` — os três pontos alinhados ao caminho do fonte:**
- **`description`** reescrita: descreve os dois caminhos (fonte quando a stack é a mesma, referência visual quando não é) em vez de proibir fonte. O que ela nega agora é **config de build** e artefato interno.
- **DoD, bloco "Pacote"** ganhou um item por caminho: **FONTE** (`proto/` + `index.css` com os tokens, build como visualizador) e **REFERÊNCIA VISUAL** (single-file ou build + `anatomia-visual.md` + `mapa-de-consumo.md`). Antes só existia o segundo, o que reprovava silenciosamente todo pacote de stack compartilhada.
- **DoD, bloco "O que nunca deve sair"** separado em duas ideias que estavam colapsadas numa: **config de build** (`vite.config`, `tsconfig`, `package.json`, `.env`) nunca sai; **código de componente** só não sai fora do caminho do fonte. E em nenhum dos dois casos sai `src/components/ui/**`, que vem do registry `@centralit` versionado, porque cópia no pacote duplica biblioteca.
- **`handoff-manifest.md`**: a linha "Código-fonte e config" virou duas, "Config de build" e "Biblioteca de componentes", cada uma com o motivo real.
- **Item do `grep` de referência morta** deixou explícito que procura *referência de import* a `src/proto`, não os arquivos copiados para `proto/` — que devem estar lá.

**Instalador** — o banner anunciava a v1.6.0 desde que o pacote foi para a 1.8.0. Agora imprime a versão corrente e, para quem vem da 1.6.x, aponta a 1.8.0 como a mudança grande.

---

## 1.8.0 — 2026-08-19

**O pipeline destruía o próprio artefato mais valioso no último passo.** A `px-proto` constrói o protótipo **dentro do boilerplate**, em `src/proto/*.tsx`, com os componentes e tokens reais. A `px-handoff` então entregava um **build compilado** como "referência visual" e o fonte ficava para trás. Um bundle é tão impossível de importar quanto HTML vanilla — ninguém faz `import` de `assets/index-abc123.js` — então o dev reduzia espaçamento, sombra e troca de estado a partir de screenshot, mesmo quando rodava exatamente a mesma biblioteca. Encontrado na v1 da Vitrine, cujo `src/proto/` tem ~6.900 linhas escritas contra `@/components/ui/*`, com os mesmos aliases do repo do dev, enquanto o pacote entregava só o `dist`.

**`px-handoff` — a forma do pacote agora depende de uma pergunta explícita:**
- Nova seção **"Forma do protótipo"**, decidida **antes** de montar o pacote: *o dev implementa na mesma stack em que o protótipo foi construído?*
  - **Sim → entregar o FONTE** (`src/proto/**` + `index.css` com os tokens) como referência de implementação. O build vira **visualizador**, não artefato principal. O README documenta de onde vem cada import e que não há dependência nova. Anatomia visual passa a **N/A — o componente é a especificação**.
  - **Não → referência visual + `anatomia-visual.md`** (o caminho da 1.7.0). É o caso de projeto que começou **antes de existir boilerplate** ou de produto legado: nenhum componente atravessa a fronteira, então o visual precisa virar documento. Com a franqueza registrada de que documentação reduz divergência mas não elimina.
- Trava explícita: ⛔ **nunca entregar apenas o build quando o fonte serviria** — é o erro mais silencioso do passo, porque o pacote *parece* completo.
- Nova seção **"Entregar o fonte NÃO é assumir o trabalho do dev"**, com a tabela de fronteira de propriedade (código de produção, arquitetura, integração, testes e manutenção seguem do dev; definição visual e de interação é do PX). Resolve a objeção política real de quem tem área de desenvolvimento própria: **protótipo é sobre propriedade, não sobre formato de arquivo**. Também nomeia o que de fato cruzaria a linha e nunca é necessário — publicar pacote versionado do qual o dev passe a depender, entregar o app de produção, ou commitar no código deles.
- DoD ganhou os itens correspondentes, incluindo o registro da fronteira de propriedade no pacote.

**`px-proto` — quem constrói agora sabe que o fonte será lido por outro time:**
- Nota no topo: o fonte de `src/proto/` é o artefato que vai no handoff quando a stack é compartilhada. Escrever pensando em ser lido — nomes que se explicam, `// MOCK:` e `// INTEGRATION BOUNDARY:` nas fronteiras, nenhum truque que não se queira ver copiado. Reafirma que segue sendo protótipo, sem manutenção do PX.

> **Nota de atribuição.** O protótipo do SmartCity é HTML vanilla porque **o boilerplate ainda não existia** quando aquele projeto começou — não foi desvio de convenção. É exatamente o cenário "stack diferente", e por isso a anatomia visual da 1.7.0 continua sendo a resposta correta **ali**. A partir de 1.8.0 o pacote deixa de tratar build compilado como padrão quando o fonte está disponível.

## 1.7.0 — 2026-08-19

**Fecha a classe de gap que fez a UI divergir na entrega SmartCity semana-33.** O dev recebeu o protótipo como referência visual e reimplementou no boilerplate; o front saiu inconsistente. A auditoria mostrou que a maior parte não era falha do dev: eram regras corretas que existiam **só no JS/CSS do protótipo**, além de três documentos citados pelas specs que nunca entraram no pacote. Os patches abaixo atacam a causa, não o sintoma.

**`px-request` — a spec passa a exigir o número, não o reconhecimento:**
- `BLOCO 9` ganha trava: *"sim, é calculado"* deixa de ser resposta suficiente. Toda regra derivada exige fórmula literal, formatação exata, escopo dos dados e **todo threshold, um por um, em tabela**. Antes, um `RN` do tipo "a prioridade é calculada a partir dos sinais vitais" passava pelo bloco sem nunca registrar os valores de corte — e quem implementa não tem como adivinhar um número.
- `BLOCO 9b` novo — **estado do dado → variante de UI**, obrigatório. Cobre a classe de regra que mais se perde no handoff, porque não é visível num print: a tela mostra só um dos estados. Exige tabela `estado → rótulo/variante/ícone`, mais visibilidade por papel, faixas numéricas que colorem, e conjuntos de coluna distintos quando duas telas reusam o mesmo componente.

**`px-story` — a história passa a trazer de volta o que o proto decidiu:**
- `S3b` novo — **varredura do JS/CSS do proto aprovado** (não só da tela renderizada). Trata **mock estático como ausência de regra** (`espera:'38min'` esconde que nunca houve fórmula), obriga conferir se o mesmo conceito usa o mesmo corte em todos os pontos da tela, e manda marcar números mágicos de mock como artefato, não requisito. Também obriga registrar divergência proto ↔ request em vez de silenciar, com a regra de precedência: a spec aprovada vence o proto desatualizado.

**`px-proto` — registra a anatomia no momento barato:**
- `Passo 8b` novo, obrigatório antes de aprovar: cada componente do inventário do Passo 1 ganha entrada em `anatomia-visual.md` com valores exatos e a coluna **Origem** (default da lib × override do projeto). Registra também bespoke sem equivalente, gambiarra de protótipo que não deve ser replicada, e equivalência de biblioteca. A informação está na mão de quem constrói; depois vira arqueologia de CSS.

**`px-handoff` — consolida, cobra e confere:**
- DoD exige `anatomia-visual.md` quando a entrega **atravessa fronteira de tecnologia**, e `mapa-de-consumo.md` quando **dev e PX usam a mesma biblioteca** — este classifica cada região em 🟢 consumir direto (não customizar) · 🟡 consumir + override · 🔴 compor, e lista os componentes da lib disponíveis e não usados. Sem ele o dev reconstrói do zero o que a lib entrega (tabela, paginação, drawer, toast, skeleton, date picker) e ao mesmo tempo assume como padrão da lib o que é identidade nossa.
- **Conferência de completude** virou trava: comparar `decisoes/` e `stories/` da origem com o pacote, arquivo por arquivo. Ausência sem justificativa bloqueia a entrega. Regra documentada que não é entregue equivale a regra inexistente.

**Divisão de responsabilidade:** a `px-proto` **escreve** a anatomia, a `px-handoff` **cobra**. Não foi criada skill nova — uma skill que rodasse só no fim teria que fazer engenharia reversa de todo o CSS, exatamente o trabalho caro que esta versão elimina.

## 1.6.0 — 2026-08-18

**Duas skills novas de execução** (`ux-*`, não são entrevista — rodam sobre o produto ao vivo):
- `ux-flows` — registra uma jornada multi-tela como flow executável em `e2e/flows/`, compilando de `px-story` já prontas ou perguntando direto quando não há.
- `ux-persona` — percorre o flow em duas fases isoladas: um subagente cego assume uma das 6 personas bundled (`novice`, `rushed`, `skeptical`, `mobile`, `accessibility`, `power-user`) e navega o produto de verdade narrando em primeira pessoa; depois o UX Designer diagnostica cada fricção pela rubrica de 7 dimensões já usada em `px-audit`/`px-story` (Descoberta, Clareza, Feedback, Fricção, Sem beco sem saída, Fidelidade, Autenticidade de dados). Recusa rodar contra mockup estático.
- As duas já eram citadas por nome em `px-audit`, `px-story`, `px-kickoff` e `px-epic` — preenchem uma lacuna que existia desde antes desta versão.

**`px-sync` trazida pro pacote central:**
- Existia solta, presa num único projeto (gitignorada, fora de qualquer canal de distribuição). Agora é genérica e instalável em qualquer projeto: sincroniza o estado completo de trabalho (produto + `planning/` + `docs/`) com o repositório central do PX, sempre `main` fast-forward e gated por aceite explícito.
- `px-handoff` agora pergunta, na abertura, se o projeto mantém um repositório central do PX — se sim, delega pro `px-sync` ao final (destino independente do pacote reduzido que vai pro dev).
- `docs/px-protocol.md` atualizado pra descrever os dois destinos possíveis do `px-handoff` e corrigido quanto à afirmação "nenhuma skill roda git", que já estava desatualizada (o `px-handoff` sempre fez push via branch órfã).

**Manutenção:**
- Removida do README a promessa de propagar skills pro boilerplate (`docs/skills-draft/`) — confirmado que esse espelho não tem consumidor (nada no boilerplate o lê, e o `px-setup` sempre instala as skills frescas via `npx github:DiogoRother-it/px-skills`, nunca de uma cópia local). A propagação de `docs/design-system/` e `docs/px-protocol.md` continua — essas sim são lidas quando o sandbox do PX é o boilerplate clonado.

## 1.5.0 — 2026-08-06

- `px-story`/`px-handoff`: bloco **S4b — Fluxo principal (passo a passo)**, o mapa de revisão rápida da jornada antes do BDD; template `handoff-manifest.md` pro recorte dev-facing vs. interno.
- `px-change` (nova skill): faixa leve para alteração localizada em tela que já existe (campo, ícone, label, paginação) — 5 blocos enxutos (propósito, estados impactados, ancoragem DS, copy, lint), sem passar pela entrevista completa do `px-request`. Gate de tamanho: se crescer para tela/fluxo novo, encaminha pro `px-request`.
- Roteamento PX embutido em `px-start`/`px-intake`/`px-request`/`px-change`: projeto com UI Kit definido sempre entra pela cadeia PX, nunca pelo pre-coding-pass global.
- Proibições de travessão/caixa alta reforçadas em `px-draw`/`px-kickoff`.

## 1.4.2 — 2026-07-16

- `px-proto`: gate explícito de ambiguidade de variação antes de codar + inventário público de todos os widgets → componente shadcn. Tabela nativa / badge manual / tooltip ausente passam a ser proibidos quando o shadcn já resolve.

## 1.4.1 — 2026-07-16

- `px-proto`: migração para Vite/localhost com componentes reais (antes era mockup estático).

## 1.4.0 — 2026-07-16

- `px-proto` (nova skill): validação visual obrigatória depois de cada `px-request` — protótipo HTML standalone com os tokens reais do UI Kit antes de virar `px-story`.

## 1.3.0 — 2026-07-15

- `px-handoff`: correções baseadas em execução real de sprint.

## 1.2.0 — 2026-07-15

- `px-handoff`: entrega limpa — HTML + UI Kit + histórias de negócio, sem artefato interno.

## 1.1.0 — 2026-07-10

- `px-preview` (nova skill): empacotamento standalone do produto pra revisão interna antes do handoff.

## 1.0.0

- Primeira versão instalável da cadeia PX/UX.
