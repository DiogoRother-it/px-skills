# Personas de usabilidade — quem julgou esta entrega

> **Template reutilizável da `px-handoff`.** Copie para `handoff-ux/<label>/personas/personas.md`
> e preencha. Os arquivos de persona (`<slug>.md`) ficam **nesta mesma pasta**, no estado exato
> em que foram usados — inclusive com os ajustes de contexto do projeto já aplicados. As jornadas
> que elas percorreram ficam em `../flows/`.

## Por que isto vai no pacote

Os **critérios de usabilidade** dos critérios de aceite não saíram de preferência de quem escreveu a história: cada um nasceu de uma persona percorrendo a tela de verdade e travando em algum ponto (`ux-persona`, Fase 1). Sem saber **quem** julgou, o critério chega ao dev como regra sem dono — e a primeira alteração de implementação que "simplifica a tela" desfaz exatamente o que ele protegia, sem que nada apite.

Serve pra três coisas concretas:

1. **Ler o CA de usabilidade sabendo por quem ele foi escrito.** "Sem jargão técnico no rótulo" existe porque o público real tem familiaridade baixa com o assunto, não por gosto de quem redigiu.
2. **Decidir sozinho no detalhe que a spec não cobre.** A persona é a régua que o PX usaria na dúvida.
3. **Revalidar depois de implementar.** O dev roda a mesma persona sobre o mesmo fluxo e compara com o que o PX encontrou.

## Personas usadas nesta entrega

| Persona | Arquivo | Origem | Público real que representa | Jornada percorrida |
|---|---|---|---|---|
| `<slug>` | `<slug>.md` | bundled `ux-persona` / custom do projeto | `<público levantado no kickoff>` | `../flows/<jornada>.md` |

**Personas deliberadamente NÃO usadas** (e por quê) — a ausência é decisão, não esquecimento:
- `<slug>` — `<motivo: público não atendido nesta leva / fluxo não exposto a esse contexto>`

## Customização por contexto do projeto

<!-- Uma seção por persona. Bundled usada sem ajuste: escrever "usada sem ajuste" e seguir. -->

### `<slug>`
- **Origem:** `<bundled ux-persona v<versão> | custom, derivado de <público>>`
- **O que foi ajustado:** `<qual campo do persona mudou e para quê>`
- **Por que o contexto do projeto exigiu:** `<o que no produto, no público ou no ambiente de uso pediu o ajuste>`
- **O que NÃO se ajusta:** o vocabulário da narração e o comportamento ao travar. Mexer neles muda a régua no meio do jogo e invalida a comparação com as rodadas anteriores.

## O que cada persona encontrou, e onde isso foi parar

| Persona | Jornada (passo) | Fricção observada | Virou |
|---|---|---|---|
| `<slug>` | `../flows/<jornada>.md` (passo `<N>`) | `<o que travou ou incomodou>` | `CA-<NN>` de `../<fluxo>/stories/<historia>.md` |

> Se uma fricção **não** virou critério (foi aceita como custo consciente), registre assim mesmo, com o motivo. Fricção conhecida e aceita é diferente de fricção não observada, e o dev precisa distinguir as duas antes de "consertar" o que foi decidido.

## Flows entregues (`../flows/`)

| Jornada | Público | Telas na ordem | Personas que percorreram | Observação |
|---|---|---|---|---|
| `<jornada>.md` | `<público>` | `<tela 1>` → `<tela 2>` | `<slug>` | `<passo N: tela não entregue nesta leva, se houver>` |

O flow é escrito em **ações de interface, nunca rota** — cada passo já traz o ponto de verificação observável. É o mesmo artefato que o **Playwright automatiza**: o BDD das histórias cobre um comportamento por tela, o flow cobre a travessia entre elas, que é onde o defeito de fluxo aparece.

> Jornada que atravessa tela **não entregue nesta leva**: o passo permanece no flow, **marcado**. Cortar o passo faz a jornada mentir; deixar sem marca faz procurar tela que não existe.

## Como revalidar depois de implementar

1. Percorrer a jornada de `../flows/<jornada>.md` **assumindo a persona**, clicando pela interface — nunca por rota direta, e nunca já sabendo o caminho certo.
2. Comparar com a tabela acima: fricção que reaparece é **regressão**; fricção nova é **achado novo**.
3. Achado novo volta pro PX. Não se resolve inventando componente fora do UI Kit — o catálogo é o mesmo dos dois lados.

> **Escopo:** o relatório bruto de cada rodada (diário da persona + diagnóstico) é material **interno** de diagnóstico e não viaja no pacote. O que o dev precisa é **quem** julgou, **com que régua**, e **o que sobrou disso como critério** — está nas tabelas acima.
