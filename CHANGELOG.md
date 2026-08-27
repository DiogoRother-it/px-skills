# Changelog

Todas as versões instaláveis via `npx github:DiogoRother-it/px-skills` / `npx @centralit/px-skills`.
O instalador imprime só a versão mais recente no terminal — o histórico completo vive aqui.

## 1.15.0 — 2026-08-27

A 1.14.0 fez a cadeia **recusar** base fora do padrão. Mas quem está com skills velhas não tem esse portão — e não tem como saber que ele existe. Esta versão fecha o degrau anterior: o repo passa a **avisar sozinho**, sem ninguém precisar lembrar de rodar o instalador.

### Hook `SessionStart`

O instalador planta `.claude/hooks/check-versao.mjs` e declara o hook em `.claude/settings.json`. Ao abrir o Claude Code no repo, três checagens rodam:

| Checagem | Como | Custo |
|---|---|---|
| Skills atrás da versão atual | `raw.githubusercontent.com` — o `px-skills` é **público**, não precisa de token | rede, cache de 6h |
| Sandbox sem `boilerplate-upstream` | `git remote` | local |
| `CENTRALIT_TOKEN` ausente | variável de ambiente | local |

As duas últimas só rodam se o repo for um sandbox do PX — detectado pelo bloco `registries.@centralit` no `components.json`. Num repo qualquer o hook fica quieto.

A saída alimenta os dois lados: `systemMessage` para a pessoa ver, e `additionalContext` para o assistente saber que precisa oferecer a atualização antes de rodar qualquer skill da cadeia.

### As quatro regras do arquivo

Escritas no topo dele porque cada uma corrige uma forma conhecida de o hook virar problema:

- **Silêncio quando está tudo certo.** Aviso que aparece toda sessão vira ruído, e as pessoas aprendem a ignorar — que é exatamente a falha que ele existe para evitar.
- **Nunca quebra a sessão.** Tudo dentro de `try/catch`; offline, VPN ou GitHub fora do ar terminam em silêncio.
- **Nunca chama `process.exit()`.** Com o `fetch` ainda em voo isso derruba o libuv no Windows (assertion em `async.c`) — aconteceu no teste, e o script passou a terminar sozinho.
- **Nunca faz `git fetch`.** Rede no `SessionStart` trava a abertura e pode pedir credencial de repo privado. A medição de idade da base continua sendo do `px-proto` Passo 3A, que roda quando ela importa.

### O `settings.json` do time não é sobrescrito

O instalador lê, mescla e grava — preservando `permissions` e qualquer `SessionStart` que já exista, e sem duplicar o hook quando roda de novo. Se o arquivo estiver **malformado**, ele **não grava**: avisa e segue. Um `settings.json` quebrado desliga todas as configurações daquele arquivo, e clobberar apagaria trabalho do time.

### Escopo, decidido explicitamente

Notificação **só local**, e audiência **só UX/PX** — quem roda as skills e pode agir. Sem webhook, sem canal, sem secret, sem GitHub Action.

Os devs não entram aqui de propósito: eles não rodam skills, e a informação que lhes serve (sobre qual base o pacote foi construído) já viaja no `procedencia.md` desde a 1.14.0.

### Limite conhecido

O hook só existe onde o instalador rodou. Quem nunca mais rodar `npx github:DiogoRother-it/px-skills` não o recebe — a primeira instalação a partir daqui é que o planta, e dali em diante ele se mantém. Não há como alcançar retroativamente um repo que ninguém toca.

**Achado não resolvido:** o `.claude/skills/` do **boilerplate** tem as 38 skills e **nenhum** `.px-skills-version`. Foram copiadas à mão, então o boilerplate distribui skills velhas sem stamp para todo mundo que clona. O hook não corrige isso: sem stamp, a checagem de versão nem roda. Precisa de uma passada no boilerplate.

Arquivos: `assets/hooks/check-versao.mjs` (novo), `install.mjs`, `package.json`.

---

## 1.14.0 — 2026-08-27

**Um UX ficou dois meses sem acesso ao boilerplate e a cadeia não sinalizou.** Ele seguiu especificando, prototipando e entregando handoff normalmente. As entregas chegaram ao dev com regra de negócio correta, visual divergente e um documento de anatomia que afirmava a procedência errada de cada valor. Nenhum passo falhou, nenhum aviso apareceu, e os problemas no dev pareciam aleatórios porque a causa não estava no pacote — estava na base sobre a qual o pacote foi construído.

Esta versão não acrescenta capacidade. Ela fecha os quatro pontos onde a cadeia **falhava em aberto**.

### A causa: duas linhas de suprimento, uma delas invisível

A biblioteca de componentes não vem do clone. Vem de um **registry shadcn privado** (`@centralit`, 52 itens), declarado no `components.json` e autenticado por `Authorization: Bearer ${CENTRALIT_TOKEN}`. Clone e registry são acessos **distintos** — dá pra ter um e não ter o outro.

O `CENTRALIT_TOKEN` **não era mencionado em nenhuma skill**. E o `px-setup` afirmava o oposto: *"Sem token no fluxo de sandbox. O acesso ao repo privado é o login normal do GitHub."* Verdadeiro para o `git clone`, falso para o registry. As duas coisas estavam conflacionadas.

### O gatilho: uma linha sem prefixo

O `px-proto` mandava `npx shadcn add <componente>`. Sem `@centralit/`, isso resolve no shadcn **público** — e **funciona**. Retorna 200, escreve o arquivo, entrega o default `new-york`. Sem token, todo componente que faltava entrava por esse caminho.

- Agora é `npx shadcn@latest add @centralit/<componente>`, com o prefixo **obrigatório**.
- ⛔ **A forma sem prefixo é proibida.** Falha do `add` do registry (401/404) é **acesso**, não componente faltando: bloqueia e volta pro `px-setup`.
- Componente ausente no registry é decisão de design system, não de proto — vira Pergunta em aberto com dono. Não se inventa primitiva.

### O que apagava o rastro: `rm -rf .git`

O `px-setup` cortava o git do sandbox pra não empurrar rascunho no boilerplate do time. A intenção era certa; o efeito colateral foi deixar o sandbox **inauditável** — sem commit de origem, sem `git fetch`, sem idade. Um sandbox que envelhece meses divergia sem sinal nenhum.

Agora: `git remote rename origin boilerplate-upstream` + `git remote set-url --push boilerplate-upstream no-push`. Protege o boilerplate (a intenção original) **e** mantém a procedência medível. O push do `px-handoff` continua por branch órfã, como já era.

### Os portões que não pegaram

O `px-proto` Passo 3 conferia três coisas: servidor rodando, tokens no `index.css`, componentes em `src/components/ui/`. **Todas as três são verdadeiras** num projeto Vite qualquer com componentes vanilla. Existência não é procedência.

Passo 3 virou **Portão de procedência e ambiente**, e falha fechado:
- **Base auditável?** `boilerplate-upstream` presente e apontando pro repo certo.
- **Idade da base?** `> 30 dias` ou `> 20 commits` atrás → ⚠️ avisa com o número exato. Não bloqueia; base velha só precisa ser **dita** — é o que separa "decidimos assim" de "ninguém sabia".
- **Registry alcançável?** Token + bloco `registries` → ⛔ bloqueia.
- **Catálogo do DS presente?** `ds-components_v4.md` é consultado no Passo 4. Ausente, o proto improvisava de memória.

O `px-handoff` tinha **mais de 40 itens de portão e nenhum verificava origem.** Todos conferem coerência *interna*: refs mortas, IDs de RN, lint de copy, nomes de arquivo. Um pacote construído inteiramente fora do padrão passa em todos.

### O documento que mentia

O achado mais grave. A `anatomia-visual.md` tem a coluna **"Origem: Boilerplate (default já correto — não customizar) × Override do projeto"**. Essa classificação exige comparar com o componente real do registry. Sem ele, preenchida por dedução, a coluna **não fica vazia — fica afirmativamente errada**, instruindo o dev a preservar exatamente o que ele precisa substituir.

- Sem o Passo 3A verde, cada linha vai como `Origem: NÃO APURADA` com pendência e dono. **É pior errar aqui do que deixar em branco.**
- Linha `NÃO APURADA` no fechamento bloqueia a aprovação do proto e a saída do handoff.

### `procedencia.md` — obrigatório em todo pacote

Sete campos, todos com valor real (nunca "atual" ou "última"): commit da base, data, distância do `main`, registry alcançado, componentes fora do registry, versão das skills, origem dos tokens. O `px-proto` apura no Passo 3A; o `px-handoff` transcreve e valida.

Procedência indeterminável **não impede a entrega** — obriga a declarar `Procedência: NÃO AUDITÁVEL` em destaque no `handoff.md`, com dono. Um pacote sem procedência que não se declara é indistinguível de um pacote conforme; era exatamente esse o estado anterior.

### Sem regressão

Decisão explícita do líder: **os handoffs já entregues não serão reauditados.** O ajuste vale a partir daqui. Sandbox montado antes desta versão não tem `boilerplate-upstream` — o Passo 3A detecta, avisa que a base não é auditável e oferece remontar pelo `px-setup`.

Arquivos: `px-setup/SKILL.md`, `px-proto/SKILL.md`, `px-handoff/SKILL.md`, `px-handoff/templates/handoff-manifest.md`, `install.mjs`, `package.json`.

---

## 1.13.0 — 2026-08-26

**Diagnóstico num projeto real (5 histórias entregues) mostrou que a 1.12.0 consertou o eixo errado.** A 1.12.0 proibiu fluxo e público como unidade de recorte. As duas regras **foram cumpridas** naquele projeto — e as histórias estavam grandes de qualquer forma. O que faltava era teto: uma tela de **uma rota só**, com 6 abas e um modal de 3 abas, passa em todos os testes de recorte e chega ao dev com **18 critérios de aceite**.

### O teto contável (`px-story` S2)

Acima de **13 CA** ou **13 cenários BDD** a história não fecha sem proposta explícita de quebra por aba, bloco ou overlay. O líder pode recusar, mas o motivo fica escrito na história (`Escopo mantido acima do teto:`) e a Definition of Ready cobra.

O teste de rota da 1.12.0 pega escopo **largo**; o teto pega escopo **fundo**. São falhas diferentes, e uma não cobre a outra.

**O 13 é calibrado, não estético.** O corte foi rodado contra as 5 histórias reais: precisa reprovar as de 14, 15, 18 e 20 critérios e **passar** a de 13, que tem escopo correto (1 rota, 0 abas) e sofre só de BDD verboso. O 12 proposto no diagnóstico reprovava essa também. O corte tem que ficar entre 13 e 14, e 14 deixa passar uma que precisava quebrar.

### Aba conta como item (`px-epic` B3)

- Tela com **3 ou mais abas independentes** entra no backlog **já quebrada**, uma linha por aba. Aba que só reordena a mesma lista não conta.
- `Modal conta como item` passou a dizer **explicitamente** "inclusive modal com abas próprias" — a regra já existia e não estava sendo lida assim.
- ⛔ **"G" virou estado proibido no fechamento do épico.** O campo Tamanho (P/M/G) existia desde sempre e **nada o consumia**: no projeto auditado, "Detalhe com 5 sub-abas" foi classificado **M**, mesmo bucket de um catálogo simples. Agora item G volta ao recorte antes de virar `px-request`.

### ID de regra de negócio: quatro convenções viraram uma

O achado mais grave do diagnóstico, e o único que já contaminou entrega. O repo tinha **quatro** convenções concorrentes:

| Onde | Convenção | Escopo |
|---|---|---|
| `px-request` Bloco 9 | `RN-01` | **nenhum** — reiniciava a cada tela |
| `px-request` Bloco 9b | `RN-UI-01` | **nenhum** |
| `px-request` template | `RN-01` na tabela pronta | **nenhum** — replantava a colisão |
| `px-epic` consolidação | `RN-[SIGLA]-001` | projeto |

A `px-request` roda **uma vez por tela**, então `RN-01` reiniciava em cada tela. Resultado medido no projeto: **10 IDs com até 5 significados incompatíveis** (`RN-02` era lifecycle de status, entrada de aba, clique em linha, busca em tempo real e ausência de botão, dependendo do fluxo). E o inverso: dark mode existia com **5 IDs diferentes**; o lifecycle de status, com **3**, escrito por extenso em 3 histórias. Uma história fechou com **18 de 18 CA sem âncora**, resolvendo rastreabilidade com a faixa `RN-02 a RN-16`.

**Convenção única agora, em todo o repo:** `RN-<SIGLA>-<DOMÍNIO>-<NN>` (ex: `RN-VIT-STATUS-01`), num **único** `regras-negocio.md` por iniciativa. É a extensão da que a `px-epic` já declarava, não foi inventada aqui. `RN-UI-…` está **aposentado**: regra de variante de UI é regra de negócio como outra qualquer.

- ⛔ **RN numerada por tela ou por fluxo é proibida.**
- **Consultar antes de criar:** se a regra já existe, cita-se o ID; não se redige de novo.
- **`px-handoff` mudou o arquivamento:** era `regras-negocio.md` **por fluxo**, o que fazia a mesma regra ser reescrita em N arquivos que divergem na primeira correção. Agora é **um** arquivo na raiz do pacote, e o arquivo por fluxo fica opcional — se existir, **lista só os IDs** que aquele fluxo usa. Dois itens novos no portão de saída: nenhum ID repetido apontando para regras diferentes, e nenhuma regra repetida apontando para IDs diferentes.

### O que foi deliberadamente NÃO mudado

O diagnóstico testou e **refutou** três hipóteses que pareciam óbvias. Registrar isso evita "consertar" o que funciona:

- **Recorte por público:** ausente no projeto. A regra da 1.12.0 foi cumprida integralmente, nenhuma tela virou duas histórias por persona. Não foi reforçada.
- **Granularidade de CA:** os CA estão em granularidade de comportamento/estado, não de campo. Um deles descreve um modal de 6 campos em **um** CA. O problema é o oposto do suspeitado: CA densos, não numerosos.
- **Recorte por camada técnica:** ausente. As fronteiras de integração estão marcadas **dentro** da história, que é o comportamento correto.

### Sobre a 1.12.0

A regra ⛔ `Não use o fluxo como ID` (`px-handoff`) nasceu **da** entrega auditada, não antes dela. O `mapa-de-telas.md` daquele projeto usa o formato hoje proibido porque foi escrito antes de a regra existir. Não é descumprimento: é a evidência que produziu a regra.

Arquivos: `px-story/SKILL.md`, `px-epic/SKILL.md`, `px-epic/templates/spec.md`, `px-request/SKILL.md`, `px-request/templates/request.md`, `px-handoff/SKILL.md`, `px-handoff/templates/px-handoff.md`, `px-handoff/templates/handoff-manifest.md`.

**Ficou de fora (diagnosticado, não aplicado):** âncora de RN por CA proibindo faixa; destino declarado para item de épico de delta; disciplina de `Contexto:` no BDD; registro de emenda no cabeçalho da história; verificação de saída do `mapa-de-telas.md`.

---

## 1.12.0 — 2026-08-26

**A unidade de recorte da história era ambígua no texto, e o ID da história colidia.** Duas regras que já estavam certas na prática, mas escritas de um jeito que autorizava história do tamanho de um fluxo.

**O que estava escrito:**
- `px-epic`, regra de ouro do recorte: "fatia vertical de valor = **tela/fluxo** observável". Tela e fluxo tratados como sinônimos, na frase que define o recorte do backlog inteiro.
- `px-handoff`, coluna `ID`: "identificador estável **por fluxo** (ex: `VIT-CAT`, `VIT-DET`)". Mas a tabela é **uma linha por tela** e tem coluna `Fluxo` separada. Os exemplos só funcionavam porque ali fluxo e tela coincidiam. No primeiro fluxo com duas telas, as duas histórias recebem o mesmo ID — quebrando exatamente a rastreabilidade história ↔ código que a 1.11.0 introduziu a tabela para dar.

**O que fica:**
- **Uma história = uma tela** (ou um modal com lógica própria). **Fluxo é agrupamento, não unidade de recorte**: fluxo com três telas navegáveis são três itens no backlog. **Público também não é recorte**: tela que serve dois públicos continua uma história, com um passo a passo por público (`px-story` S4b) — duplicar por persona faz a mesma UI ser especificada duas vezes, com divergência garantida.
- **ID por tela**, formato `<PROD>-<FLUXO>-<TELA>` (`VIT-CAT-LISTA`, `VIT-CAT-DET`); com um fluxo só, o segmento do meio cai (`VIT-LISTA`). O ID nasce com a tela e nunca é renumerado nem reaproveitado; tela quebrada em duas depois gera ID novo para a nova e mantém o da antiga.
- **Trava nova em `px-story` S2 (Granularidade):** teste explícito antes de perguntar ao líder — se a história atravessa duas telas navegáveis, é fluxo, não história, e quebra. Fluxo virando história é a causa número um de história grande demais para fechar num ciclo, que foi o feedback que chegou.
- **Template da história ganhou o cabeçalho de ID.** A S7 exigia "cabeçalho com ID estável, ordem de implementação e arquivo da UI" desde a 1.11.0, mas o `templates/px-story.md` não tinha nenhum dos três campos — o item da Definition of Ready não tinha onde ser cumprido.

Arquivos: `px-epic/SKILL.md`, `px-handoff/SKILL.md`, `px-story/SKILL.md`, `px-story/templates/px-story.md`.

---

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
