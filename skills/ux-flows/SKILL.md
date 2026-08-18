---
name: ux-flows
description: Registra uma jornada completa (multi-tela, de um público real) como um flow executável em e2e/flows/, para o ux-persona percorrer e o Playwright do dev validar depois. Compila os passos a partir de histórias já prontas (px-story) ou, na falta delas, pergunta a jornada direto (ex durante um px-audit). Não substitui o BDD nem o passo a passo por tela do px-story — agrega os dois numa jornada contínua entre telas. Use quando alguém disser "gera o flow", "registra essa jornada", "quero rodar o ux-persona nisso", "cria o flow de teste dessa tela", ou quando o px-story/px-audit oferecerem "gerar o flow do ux-flows".
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: flows
---

# ux-flows — registra a jornada como flow executável

Um **flow** é uma jornada contínua de um público real, do início ao fim, escrita como **ações de interface** (nunca rota/URL interna) — a mesma unidade que uma persona vai percorrer no `ux-persona` e que o Playwright do dev vai automatizar depois. Ele não é o BDD (que testa UM comportamento por vez, tela a tela) nem o "fluxo principal" do `px-story` S4b (que é passo a passo de UMA tela) — o flow **agrega vários desses** na ordem em que o público realmente atravessa o produto (ex: "gestor: entra → filtra pedidos → abre um → aprova", como já mapeado no `px-kickoff`/`px-audit`).

Diferente das skills `px-*`, isto **não é uma entrevista pesada**. Na maioria dos casos o flow é **compilado** de artefatos que já existem — a IA monta, mostra, e o líder só confirma.

Contexto inicial via slash: `$ARGUMENTS` (nome da jornada, ou referência às histórias/telas envolvidas).

## Duas fontes de entrada

**Modo compilar (preferencial — quando já existem histórias prontas):**
- Reúna as `px-story` das telas que compõem a jornada, na ordem em que o público as percorre.
- De cada uma, herde o bloco **S4b (Fluxo principal passo a passo)** e o **público** ancorado em S1.
- Encadeie os passos das várias telas numa única sequência numerada, sem duplicar o texto do BDD — cada passo aponta pro cenário Gherkin correspondente (`ver BDD: <cenário> em <story>`), igual o próprio S4b já faz dentro de uma tela.
- Mostre a jornada compilada e peça confirmação — não é pergunta aberta, é validação de rascunho.

**Modo descrever (fallback — quando ainda não há histórias, ex: dentro de um `px-audit` Bloco 3):**
- Pergunte, uma vez: "Qual a jornada principal desse público? Quais os passos, do início ao fim?" — *ex: "gestor: entra → filtra pedidos → abre um → aprova".*
- Registre os passos como ações de interface. Se um passo não tiver um resultado observável claro, pergunte-o (não invente).

## Regras (poucas, mas inegociáveis)

1. **Ações de interface, nunca rota interna.** Todo passo é algo que se clica/preenche na tela — espelha a regra de ouro do `ux-persona`/BDD. Se um passo só existe como URL direta, ele não é um passo válido do flow.
2. **Derivado, não inventado.** No modo compilar, os passos vêm de S4b + BDD; no modo descrever, vêm da resposta do líder. Nunca complete um passo "porque faz sentido".
3. **Cada passo tem um ponto de verificação observável** (o que deveria estar na tela ali — o mesmo "Então" do BDD, quando existir). Sem isso, `ux-persona` não tem como julgar se o passo "funcionou".
4. **Marque o(s) público(s) e a(s) persona(s) sugerida(s)** para percorrer o flow (herdado de `publico-alvo.md` → persona bundled do `ux-persona`, ou "criar próprio").
5. **Eco antes de salvar.** Mostre o flow compilado/descrito e confirme com o líder.

## Formato e onde salvar

Use `templates/flow.md`. Salve em:

```
e2e/flows/<slug-da-jornada>.md
```

`slug` kebab-case da jornada (não da tela) — ex: `aprovar-pedido-gestor.md`. Se o produto já tem `PX-PROGRESS.md`, registre o caminho do flow lá.

## Quando NÃO usar

- **Uma tela isolada, sem jornada multi-tela** e sem necessidade de walkthrough qualitativo → o BDD do `px-story` já cobre; não crie um flow de um passo só.
- **Quer só testar comportamento determinístico** (isto salvou? isto retornou erro?) → é Playwright, não um flow.

## Encadeamento

Com o flow salvo, ofereça: "Quer rodar o `ux-persona` nesse flow agora, com qual persona?" Se ainda não há persona definida pro público, aponte para os 6 personas bundled do `ux-persona` (ou "criar próprio").

## Relação com o fluxo

```
px-story (S4b + BDD, por tela)  ─┐
px-audit (B3, jornada atual)     ┼─→  ux-flows (agrega em jornada)  →  ux-persona (percorre)  →  Playwright do dev (automatiza)
                                 ┘
```
