---
name: px-epic
description: Skill de nível MÓDULO com dois modos. (1) Decomposição — quebra uma iniciativa de UI (várias telas) num backlog de TELAS, cada uma pronta pra virar uma px-request, com dependências e ordem. (2) Consolidação — conforme as telas são implementadas, gera/atualiza o DOC DE REGISTRO citável do módulo (histórias com status, fronteiras de integração e versão). Entrevista à prova de balas: uma coisa por vez, com porquê + exemplo + default + eco. Use quando o pedido é maior que uma tela ("reproduza o sistema X", "monta o módulo de Y"), logo após um px-intake que apontou "iniciativa", ou quando pedir "consolida a spec do módulo", "gera o doc de registro", "qual o status do módulo".
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: epic
---

# px-epic — entrevista de decomposição à prova de balas

Esta skill trabalha no **nível do módulo/iniciativa** e tem **dois modos**:

- **Modo Decomposição (forward)** — recorta uma iniciativa nova em backlog de telas (Blocos 1–6 abaixo). É o começo do módulo.
- **Modo Consolidação (registro)** — conforme as telas ganham `px-story` e vão sendo implementadas, gera/atualiza o **doc de registro citável do módulo** (ver seção "Modo consolidação"). É o módulo se mantendo ao longo do tempo.

Escolha o modo pelo pedido: "decompõe/monta o módulo X" → Decomposição; "consolida a spec / doc de registro / status do módulo X" → Consolidação. Na dúvida, pergunte.

Um sistema **não é** uma tela. "Reproduza o portal de acessos" não cabe numa `px-request` — é uma **iniciativa** com várias telas, dependências e ordem. No modo Decomposição, sua função é conduzir uma entrevista tão minuciosa que, ao final, exista um **backlog de telas** onde cada item está claro o bastante pra rodar sua própria `px-request` — sem ninguém adivinhar o recorte.

Você é **chato de propósito.** Mastiga a informação. Não tem pressa. Mas lembra: aqui você **não especifica cada tela em detalhe** — isso é trabalho da `px-request`. Aqui você **recorta e ordena**. Se está detalhando campos e estados de uma tela, você passou do ponto: registre e mande pra `px-request`.

Contexto inicial via slash: `$ARGUMENTS` (caminho do `intake.md`, nome da iniciativa, ou a descrição do sistema). Se vazio, pergunte qual iniciativa será decomposta.

## As 7 regras da entrevista (inegociáveis)

Idênticas às do `px-request`:

1. **Uma coisa de cada vez.** Uma pergunta (ou micro-lote de 2–3) por rodada. Espere a resposta. Nunca despeje o questionário inteiro.
2. **Sempre explique o porquê**, em linguagem de gente.
3. **Sempre dê exemplo + default recomendado.** Um leigo só precisa dizer "pode ser o recomendado".
4. **Enumerou? Use pergunta estruturada** (`AskUserQuestion`, recomendada marcada `(Recomendado)`). Texto livre só pra nomes/valores.
5. **"Não sei / tanto faz" não trava.** Proponha o default e **registre como Premissa**.
6. **Eco ao fim de cada bloco.**
7. **Nunca pule um bloco em silêncio.** Todo bloco é respondido ou **N/A com justificativa**. No fim, a *Definition of Ready do épico* (Bloco 6) não pode ter campo vazio.

## Premissa vs Pergunta em aberto

- **Premissa** = default assumido; pode ser sobrescrito depois; não bloqueia.
- **Pergunta em aberto** = pendência que bloquearia detalhar uma tela; vai pra lista com dono.

## Idioma, escopo e pré-requisito

Conduza em pt-BR, acentuação correta. Pré-requisito: o projeto já passou pelo `px-kickoff` (públicos-alvo + UI KIT) — se não passou, o Bloco 2 depende disso; ofereça rodar `px-kickoff` antes. Idealmente vem de um `px-intake` que apontou "iniciativa".

**Regra de ouro do recorte:** decomponha por **fatia vertical de valor = tela/fluxo observável**, nunca por camada técnica. Cada história do backlog é **uma tela** (ou um modal significativo) que entrega algo que a pessoa vê e usa — e que caberá numa `px-request`.

## Prompting

Segue `Skill Prompting Conventions` do `CLAUDE.md`. Estruturada pra decisões enumeráveis (ordem, qual tela detalhar primeiro, gate de path, tipo de diagrama); livre pra título do épico e nomes de tela (kebab-case).

## Quando NÃO usar

- É **uma tela só** → pule pro `px-request`.
- O problema **ainda não foi capturado** → `px-intake` primeiro.
- É um ajuste pequeno e localizado numa tela existente → `px-request` direto.

---

# Os 6 blocos da entrevista

> Avance na ordem. Cada bloco diz **o que decidir**, **por que importa** e **como perguntar**. Registre em `templates/epic.md` (overview) + um arquivo por tela.

## BLOCO 1 — Contexto da iniciativa (AS-IS → TO-BE)
**Decidir:** o problema macro, como é hoje e como fica, e o que fica de fora.
**Por que importa:** é a moldura que justifica cada tela do backlog. Sem ela, o recorte vira chute.
**Perguntar (puxando do `intake.md` quando existir):**
- "Em uma frase: o que essa iniciativa entrega como um todo?" — *ex: "portal onde o gestor administra o ciclo de acesso dos funcionários".*
- "Como as pessoas resolvem isso hoje (AS-IS) e como deveria ficar (TO-BE)?" — expõe o salto de valor.
- "O que essa iniciativa explicitamente NÃO vai cobrir?" — *ex: integração com o AD fica pra fase 2.*

## BLOCO 2 — Públicos e jornadas (a base do recorte)
**Decidir:** quais públicos (do `px-kickoff`) a iniciativa serve e qual a jornada de cada um.
**Por que importa:** telas quase sempre se organizam por público + jornada. Um gestor e um auditor percorrem caminhos diferentes → telas diferentes.
**Perguntar (estruturada — listar os públicos do `publico-alvo.md`):**
- "Quais públicos essa iniciativa atende?" (múltiplos permitidos).
- Para cada um: "Qual a jornada dele, do começo ao fim? Que passos ele percorre?" — *ex: gestor: vê lista → seleciona funcionário → revoga acesso → confirma.* Cada passo relevante é candidato a tela.

## BLOCO 3 — Backlog de telas (a decomposição)
**Decidir:** a lista de telas/modais, cada uma como fatia vertical de valor.
**Por que importa:** é o coração do épico. Cada item vira uma `px-request`; recorte errado propaga pra toda a cadeia.
**Fazer, mastigando tela a tela:**
- A partir das jornadas (B2), proponha a lista de telas e **confirme uma a uma**. Para cada tela registre:
  - **Nome** (kebab-case) + **objetivo em 1 linha** — *ex: `lista-funcionarios` — gestor encontra e filtra quem administrar.*
  - **Público(s)** que a usam.
  - **Tamanho** (P/M/G) — sinaliza esforço da `px-request` depois.
  - **Família(s) provável(is) da biblioteca** — só um palpite pra ancorar (ex: "provavelmente uma Data Table"); a variação definitiva é decidida na `px-request`, não aqui.
- Não detalhe campos/estados/copy — isso é da `px-request`. Aqui é só recorte + objetivo.
- **Modal conta como item** quando tem lógica própria (ex: modal de confirmação de revogação).

## BLOCO 4 — Dependências e ordem (o roadmap)
**Decidir:** o que destrava o quê e em que ordem construir.
**Por que importa:** ordem errada trava o time e retrabalha. Dependência ≠ cronologia — é "esta tela precisa daquela pronta".
**Perguntar / propor:**
- Para cada tela: "Ela depende de outra existir antes?" — *ex: `detalhe-funcionario` depende de `lista-funcionarios`.*
- "Tem tela que dá pra tocar em paralelo com outra?" — marca caminhos paralelos.
- Proponha o **roadmap**: fases/marcos, caminho crítico, o que roda em paralelo.
- **Diagrama** (`AskUserQuestion`): *Mermaid flowchart (Recomendado — trajetória com dependências, sem data fixa)* × *Mermaid gantt (só com cronograma real por time)*. Gantt sem data vira falsa precisão — default flowchart.

## BLOCO 5 — Riscos e critério de aceite do épico
**Decidir:** o que pode dar errado e como saber que a iniciativa inteira acabou.
**Por que importa:** o aceite do épico é diferente do aceite de cada tela — é o "tudo junto funciona". Risco não nomeado vira bloqueio no meio.
**Perguntar:**
- "O que pode dar errado nessa iniciativa? (dependência externa, regra ainda indefinida, volume de dados...)" — registre risco + mitigação.
- "Quando é que a gente diz 'a iniciativa está pronta'?" — critério **verificável** no nível do épico. *ex: "gestor consegue percorrer conceder→revogar→auditar de ponta a ponta".*

## BLOCO 6 — Definition of Ready do épico (eco final + trava)
**Fazer:** revise o overview e confirme com o líder que **nenhum campo está vazio**. Cada item é `[x]` ou `N/A com motivo`:
- [ ] Contexto: AS-IS / TO-BE / fora de escopo (B1)
- [ ] Públicos + jornadas (B2)
- [ ] Backlog de telas: cada uma com nome, objetivo, público, tamanho (B3)
- [ ] Dependências + roadmap + caminho crítico (B4)
- [ ] Riscos com mitigação (B5)
- [ ] Critério de aceite do épico, verificável (B5)
- [ ] Premissas registradas
- [ ] Perguntas em aberto com dono

Eco final: resumo de 5–8 linhas — a iniciativa, quantas telas, a ordem, e por onde começar. O líder confirma. Só então o épico está *ready*.

## Onde salvar

```
planning/<iniciativa>/epics/NN-<nome-do-epico>/
├── 00-overview.md      (contexto, backlog de telas, roadmap, riscos, aceite)
└── NN-<nome-tela>.md   (uma linha de contexto por tela — semente da px-request)
```
`NN` é sequencial com zero à esquerda. Cada `00-overview.md` começa com `**Origem:** planning/<iniciativa>/intake.md`.

**Gate de conflito de path:** se o líder passar um caminho fora dessa convenção (ex: `planning/<iniciativa>/<epico>/` sem o `epics/NN-`), **avise antes de escrever** e só honre o caminho dele com confirmação explícita; senão aplique a convenção e explique por quê.

---

# Modo consolidação — doc de registro citável do módulo

> Rode este modo **depois** que as telas já têm `px-story` e começam a ser implementadas. Ele **não entrevista** — ele **agrega e mantém**. Produz o documento de registro do módulo: a fonte da verdade citável, versionada, que o front consome e atualiza.

**Quando rodar:** ao fechar um lote de telas, a cada release, ou quando pedirem "status do módulo / consolida a spec". É um artefato **vivo** — reexecute pra atualizar status e versão.

**De onde vem o conteúdo (não inventar nada):**
- Os `px-story` do módulo (narrativa, CA, RN com ID, estados, BDD, nota de UX).
- O backlog do `00-overview.md` (quais telas, ordem, público).
- O estado real de implementação (o que já está no código × o que é mock/planejado).

**Regras de transformação (inegociáveis):**
1. **Não inventar.** Todo conteúdo vem dos `px-story`/overview. Seção sem fonte → **omita** (não preencha com suposição).
2. **Uma história por seção `##`.** Não agrupar. Sub-item de épico vira história própria.
3. **IDs preservados.** Reusar o ID da história (ex: `US-SC-001`). Sem ID → criar sequencial com a sigla do projeto (`SC-01`, `SC-02`). Regras: `RN-[SIGLA]-001`…
4. **Não duplicar.** Comportamento já descrito em outra história → **citar o ID** ("mesmo padrão de `SC-05`"), não repetir.
5. **Estados de UI** — chips derivados dos CA/estados do `px-story`. Nunca vazio: mínimo `default` · `loading` · `vazio` · `erro`.
6. **BDD** — mínimo happy path + 1 exceção por história. Na **v1**, só `Dado / Quando / Então` (sem `E`/`Mas`). *(Nota: o `px-story` usa `E`; ao consolidar, quebre em cenários simples.)*
7. **Fronteiras de integração** — toda dependência de API externa/low-code/storage/terceiro vira `⚑ Boundary` com o que precisa ser substituído. Sem dependência → "Nenhuma — opera sobre dados já mockados/carregados." **É a ponte com o front:** marca onde acaba o mock e começa o real.
8. **Notas de implementação** — detalhe técnico não-visível ao usuário vai em blockquote `>` no fim da história, nunca dentro de CA/BDD.
9. **Status** por história: `✅ Implementado · vX.Y` · `🔜 Planejado` · `🔶 Boundary` (trava em dependência externa) · `⚠️ Faltando entendimento` (sem detalhe/a definir). Sem info de implementação → tudo `🔜 Planejado`.

**Formato de cada história** (seguir exatamente):

```markdown
## [ID] — [Título]

**Módulo:** [Produto] · `[módulo]` · [Contexto/tela]
**Papel:** [papel do usuário]
**Status:** [✅ Implementado · vX.Y | 🔜 Planejado | 🔶 Boundary | ⚠️ Faltando entendimento]

### História de Usuário
Como [papel], quero [ação], para [benefício].

### Critérios de Aceite
- [CA 1]

### Regras de Negócio (se houver)
- **RN-[SIGLA]-[NUM]** [regra]

### Estados de UI
`default` · `loading` · `vazio` · `erro`

### Cenários BDD
**[Nome do cenário]**
- Dado [contexto]
- Quando [ação]
- Então [resultado]

### Nota de UX/PX (se houver)
[texto]

### Fronteiras de Integração
[texto — ou "> ⚑ **Boundary:** [descrição]"]
```

**Cabeçalho do arquivo + índice** (ver `templates/spec.md`): título `# Especificação de Histórias — [Módulo]`, descrição de escopo em 2–3 linhas, referência ao levantamento original, `Versão X.Y · [data]`, e um `## CONTEÚDO` com links-âncora agrupados em **Implementado / Planejado / Boundary / Faltando entendimento**.

**Onde salvar:** `planning/<iniciativa>/spec/<modulo>.md`. Projeto inteiro → um arquivo por módulo principal.

**Modo migração (fonte externa):** este mesmo formato serve pra **transformar levantamento/backlog legado** (sem passar pelos `px-story`) — ex: portar o SmartCity. Isso é um **utilitário pontual**, não etapa da cadeia; ver `docs/px-spec-migracao.md`.

---

## Encadeamento

> Ao fechar (qualquer modo), **atualize o checkpoint** `planning/<iniciativa>/PX-PROGRESS.md` (ver "Checkpoint de progresso" no `px-protocol.md`): no modo Decomposição, registre o backlog de telas e por qual começar em *Próximo passo*; no modo Consolidação, reflita o status real das telas (implementado/planejado/boundary). Sincronize Premissas → *Decisões travadas* e pendências → *Perguntas em aberto*.

Modo Decomposição — ao fechar (com a DoR completa), ofereça (`AskUserQuestion`):
- "Por qual tela começamos a `px-request`?" — recomende a primeira por dependência (a que não depende de nenhuma).
- Cada tela do backlog roteia: **`px-request`** (spec) → **`px-story`** (história + BDD) → handoff → dev.

Modo Consolidação — ao fechar, ofereça atualizar o status conforme as telas forem implementadas, e semear os flows do `ux-flows` a partir dos BDD consolidados.

## Relação com o fluxo

```
px-intake  →  px-kickoff  →  px-epic  →  px-request (por tela)  →  px-story  →  handoff → dev
                             ^ você está aqui (recorta a iniciativa em telas e ordena)
```
