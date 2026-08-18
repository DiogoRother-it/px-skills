---
name: px-change
description: Faixa leve para ALTERAÇÃO LOCALIZADA em tela que já existe — adicionar um campo, trocar um ícone, ajustar paginação, incluir um botão de copiar, mudar um label. Não substitui o px-request (tela ou fluxo novo) nem o px-epic (sistema inteiro): é a entrada certa para ajustes incrementais dentro de um projeto PX com UI Kit definido. Garante o que a edição ad-hoc pula — estados impactados, ancoragem no DS/UI Kit, copy revisada e atualização do checkpoint. Use quando alguém disser "quero adicionar um campo", "trocar um ícone", "ajustar o label", "incluir um botão de copiar", "mudar a paginação" em tela que já existe.
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: change
---

# px-change — alteração localizada em tela existente

Uma alteração pontual em tela que já existe **não é uma tela nova**. "Adicionar um campo de busca" ou "trocar o ícone de exportação" são ajustes — não justificam a entrevista completa do `px-request`. Mas também não podem ser feitos de forma ad-hoc: sem ancoragem no DS, sem verificar os estados impactados e sem revisar a copy, o ajuste vaza as regras que a cadeia PX garante.

Esta skill resolve isso em blocos enxutos: entende o ajuste, verifica o impacto, ancora no componente certo, revisa a copy e fecha com lint e checkpoint.

> **Roteamento em projeto PX ativo:** qualquer mudança de UI dentro de um projeto com UI Kit definido entra pela cadeia PX — `px-request` para tela ou fluxo novo, `px-change` para ajuste localizado em tela que já existe. **Nunca** usar o pre-coding-pass global dentro de um projeto PX ativo: ele é agnóstico ao design system e não garante ancoragem nos tokens nem lint de copy. O pre-coding-pass global vale apenas para projetos fora do design system.

Contexto inicial via slash: `$ARGUMENTS` (descrição do ajuste). Se vazio, pergunte o que a pessoa quer mudar e em qual tela.

## Regras de condução (enxutas, mas não puladas)

1. **Uma coisa de cada vez.** Uma pergunta (ou micro-lote de 2–3 muito ligadas) por rodada.
2. **Sempre explique o porquê.** Ajuste pequeno não dispensa o motivo.
3. **Sempre dê exemplo + default recomendado.** Quem responde só precisa dizer "pode ser o recomendado".
4. **Enumerou? Pergunta estruturada.** `AskUserQuestion` com 2–4 opções.
5. **"Não sei / tanto faz" não trava.** Proponha o default, registre como Premissa e siga.
6. **Eco ao fim de cada bloco.** *"Então até aqui: ... — confirma?"*
7. **Nunca pule um bloco em silêncio.** Todo bloco é respondido ou marcado N/A com justificativa.

## Premissa vs Pergunta em aberto

- **Premissa** = decisão que a IA tomou por default; o líder pode sobrescrever depois. Não bloqueia.
- **Pergunta em aberto** = decisão pendente que bloquearia o ajuste se não resolvida.

---

# Os 5 blocos do ajuste

## BLOCO 1 — Propósito e escopo do ajuste (o que muda)
**Decidir:** o que será alterado, onde, e por quê.
**Por que importa:** sem o escopo explícito, o ajuste pode crescer sem controle ou invadir o território do `px-request`.
**Perguntar (livre, uma de cada vez):**
- "Em uma frase: o que você quer mudar?" — *ex: "adicionar um campo de busca no topo da tabela de usuários".*
- "Em qual tela/arquivo? Me informe o caminho ou slug." — *ex: `src/pages/users/index.tsx`.*
- "Por que agora? Qual o gatilho ou necessidade?" — registra a origem.

**Gate de tamanho:** se o ajuste envolver mais de uma tela, novos fluxos ou componentes inteiramente novos, **pare e encaminhe** pro `px-request` (componente/fluxo novo) ou `px-epic` (várias telas). Este gate é obrigatório.

**Eco:** *"Então: ajuste em [tela/arquivo], propósito [X] — confirma?"*

## BLOCO 2 — Estados de UI impactados (só os que mudam)
**Decidir:** quais estados do componente afetado precisam ser revisados ou atualizados.
**Por que importa:** um ajuste pequeno pode impactar mais estados do que parece — ex: adicionar um campo obrigatório afeta os estados de validação, error e disabled.
**Fazer:** para o elemento alterado, verificar quais destes estados mudam (não a matriz inteira — só os impactados):
- **default** — muda o visual no estado normal?
- **loading** — o carregamento é afetado?
- **empty** — o estado vazio precisa de ajuste?
- **error / validação** — há nova regra ou mensagem de erro?
- **disabled / read-only** — a mudança altera quem pode ver ou interagir?
- **success** — o feedback de sucesso muda?
- **responsivo** — o ajuste se comporta diferente no mobile?

Marque N/A com motivo para os estados que não são afetados. **Nunca assuma que só o estado default muda.**

**Eco:** *"Estados impactados: [lista] — confirma?"*

## BLOCO 3 — Ancoragem no DS/UI Kit (qual componente usar)
**Decidir:** qual componente do design system ou UI Kit do projeto é usado neste ajuste.
**Por que importa:** reusar antes de criar é a regra central. Um componente avulso não ancorado no catálogo quebra a consistência visual e o lint.
**Fazer:**
- "O ajuste usa um componente que já existe no catálogo (`src/components/ui/`)?" — *ex: Badge, Button, Input, Tooltip.*
- Se sim: confirmar a variação exata.
- Se não existe: **gate "Outro"** — marcar **⚠️ REQUER VALIDAÇÃO UX/PX** e **não avançar** sem aprovação explícita do líder. Nunca criar componente customizado em silêncio.
- Se for só mudança de token/classe (ex: cor, spacing, label): confirmar que usa `var(--token)` ou classe Tailwind, nunca valor hardcoded.

**Eco:** *"Componente: [X], variação [Y] — confirma?"*

## BLOCO 4 — Copy dos textos novos ou alterados
**Decidir:** o texto literal de qualquer elemento que muda.
**Por que importa:** o dev não inventa copy. E copy nova de UI é o ponto de maior risco para vazar travessão e caixa alta.

**Constraints obrigatórias (proibições duras, não referências ao DS):**
- **TRAVESSÃO:** proibido `—` (em dash) e `–` (en dash) em qualquer texto de interface visível — títulos, labels, eyebrows, tooltips, mensagens de empty/error, alt. Usar ponto, vírgula, ponto-e-vírgula ou reescrever. Hífen `-` em palavra composta (ex: "mercado-alvo") é permitido.
- **CAIXA ALTA:** proibida caixa alta total em labels/eyebrows/títulos. Usar title case (ex: "Educação", não "EDUCAÇÃO"). Hierarquia por peso e letter-spacing, nunca por caixa alta.

**Perguntar:**
- "Qual o texto exato de cada elemento alterado?" — *ex: label do botão, placeholder do campo, mensagem de vazio/erro.*
- Se o líder não tiver o texto pronto, **proponha** respeitando as constraints acima e registre como Premissa.

**Verificação antes de fechar este bloco:** releia todo texto novo. Algum tem `—`, `–` ou CAIXA ALTA TOTAL? Se sim, corrija antes de fechar.

**Eco:** *"Copy: [texto exato por elemento] — confirma?"*

## BLOCO 5 — Checklist de fechamento
**Fazer, antes de implementar:**
- [ ] Propósito e escopo confirmados (B1) e dentro do limite de "ajuste localizado"
- [ ] Estados impactados mapeados, N/A justificados (B2)
- [ ] Componente do catálogo confirmado ou gate ⚠️ aprovado (B3)
- [ ] Copy literal revisada: sem travessão (— / –) e sem caixa alta total (B4)
- [ ] Lint de copy rodado após implementar: `npm run lint:travessao` e `npm run lint:caixa-alta`
- [ ] Checkpoint atualizado: ajuste registrado em `planning/<iniciativa>/PX-PROGRESS.md`
- [ ] Registro do módulo atualizado (se houver `planning/<iniciativa>/requests/<slug>.md` correspondente)

**Eco final:** *"Ajuste [X] em [tela]: [N] estados impactados, componente [Y], copy revisada, lint pendente. Confirma para implementar?"*

## Quando NÃO usar

- **Tela ou fluxo novo** → `px-request` (entrevista completa dos 12 blocos).
- **Sistema inteiro ou múltiplas telas** → `px-epic` para decompor, depois `px-request` por tela.
- **Redesign de uma tela inteira** → `px-audit` (porta brownfield) para diagnosticar o AS-IS antes de mudar.
- **Projeto fora do design system (sem UI Kit definido)** → pre-coding-pass global. Mas se o projeto tem identidade PX, **nunca** o pre-coding-pass global — ele não ancora nos tokens nem garante lint de copy.

## Onde salvar

Não há um artefato autônomo obrigatório para ajustes localizados. Registre o ajuste de uma das formas:
- **Se houver request existente para a tela:** adicionar nota de alteração ao final de `planning/<iniciativa>/requests/<slug>.md`.
- **Se não houver:** criar `planning/<iniciativa>/changes/<slug-da-tela>-<data>.md` com os blocos preenchidos.

Em ambos os casos, atualizar o checkpoint `planning/<iniciativa>/PX-PROGRESS.md`.

## Encadeamento

> Ao fechar, **atualize o checkpoint** `planning/<iniciativa>/PX-PROGRESS.md`: registre o ajuste como feito, com referência ao arquivo e aos estados impactados. Se o ajuste revelou necessidade de mudança maior, registre como Pergunta em aberto e roteia pro `px-request`.

Após implementar:
- Rodar `npm run lint` (inclui `lint:travessao` e `lint:caixa-alta`) para confirmar que nenhuma copy nova vaza as regras.
- Se o ajuste virou algo maior: "Isso cresceu — quer abrir um `px-request` formal para a tela?"

## Relação com o fluxo

```
ajuste localizado em tela que já existe:
  px-change  →  implementação  →  lint  →  checkpoint atualizado

tela nova ou fluxo novo:
  px-request  (não use o px-change)

sistema inteiro / várias telas:
  px-epic  →  px-request por tela  (não use o px-change)

projeto sem UI Kit / fora do design system:
  pre-coding-pass global  (não use o px-change — ele pressupõe UI Kit definido)
```

> `px-change` é irmão do `px-request`: ambos especificam o que será implementado, mas em escalas diferentes. O `px-change` é para o ajuste que cabe numa tarde; o `px-request` é para a tela que cabe numa semana. Se durante o `px-change` ficar claro que o ajuste é maior do que parece — encaminhe pro `px-request`.
