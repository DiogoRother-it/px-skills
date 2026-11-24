---
name: px-migrar-ds
description: Migra um produto que veio de outra área para o design system oficial @cit e dá a ele uma identidade de produto (logo, marcas, cores, tipografia de marca, ícones de marca, banners, animações), sem redesenhar e sem quebrar nada. Faz o diagnóstico (com baseline visual de todas as telas e estados), aciona a skill styleguide-de-produto para a identidade, planeja e implementa em passos pequenos, validando cada um contra a baseline, com o ok do UX entre etapas. Use quando alguém disser "aplicar o DS nesse produto", "migrar para o @cit", "esse sistema veio de outra área", "adequar ao novo design system", "trocar a paleta do produto", "padronizar o visual com o DS". Não é para redesign de usabilidade (isso é px-audit) nem para projeto novo (px-start).
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: migracao-ds
---

# px-migrar-ds: levar um produto para o @cit, com identidade própria

Um produto chegou de outra área, com o visual dele. Esta skill o adequa ao design system `@cit` e dá a ele uma identidade de produto, **preservando tudo o que já funciona**. É migração, não redesign: a tela continua com o mesmo conteúdo, na mesma ordem e com o mesmo comportamento, só que no DS.

Ela trabalha em par com a **`styleguide-de-produto`**: esta skill cuida da base (tokens, componentes, estados) e chama a outra na etapa 2 para a camada de marca (logo do produto, marca de cada módulo, cores, tipografia de marca, ícones de marca, banners e animações, em qualquer estilo).

Siga o **Protocolo de Interação UX** e as **Skill Prompting Conventions** do `docs/px-protocol.md` (uma pergunta de cada vez, `AskUserQuestion` para escolhas, eco antes de avançar). Contexto via slash: `$ARGUMENTS` (produto, repositório, URL). Se vazio, pergunte qual produto e como acessar o código.

## Fontes oficiais

- **DS `@cit`:** fonte em `gitlab.cithyper.click/centralit/shadcn`; regras em `docs/design-system/` do repositório (`ds-foundations_v4.md`, `ds-components_v4.md`, `ds-patterns.md`, `Engineering-directives_v4.md`). Se o repositório não tiver essa pasta, a `px-setup` traz o DS. O `boilerplate-cit` (registry `@centralit`) foi descontinuado: não use.
- **Identidade do produto:** o styleguide da `styleguide-de-produto` (`planning/<produto>/marcas/`: `produtos.json`, `tokens.css`, SVGs e a página).
- **Protocolo:** `docs/px-protocol.md`, com as regras inegociáveis.
- **Em conflito:** o CSS real do DS vale para valor visual; os documentos valem para regra e comportamento.

## Regras (valem em todas as etapas)

1. **Nada de comportamento muda.** Regra de negócio, dados, APIs, integrações, rotas, fluxos, textos, campos, ações, estados, hierarquia e posição dos elementos ficam como estão.
2. **Reuse o DS.** Use o componente oficial do `@cit` (via `npx shadcn add`), sem solução paralela, sem recriar o que existe e sem dependência nova fora do DS.
3. **Mapeie pela função, não pela aparência.** Nenhuma troca global de cor, classe ou estilo sem saber onde e para que cada uma é usada. Vermelho de erro vira o token de erro, e não "o vermelho mais parecido".
4. **Acessibilidade e responsividade não pioram.** O contraste novo passa (4.5:1 em texto e 3:1 em elemento gráfico); foco, teclado e o comportamento no celular continuam funcionando.
5. **Conflito entre "preservar" e uma regra inegociável do DS** (tabela com rolagem horizontal, overlay empilhado, mais de um botão primário, caixa alta, ícone fora do Lucide, espaçamento fora da grade de 8): não corrija por conta própria. Liste como decisão do UX, com o risco e uma proposta. Veja [`references/conflitos-com-o-ds.md`](references/conflitos-com-o-ds.md).
6. **Sem equivalente no DS, ou mudança estrutural com risco:** pare, documente e proponha. Marque **⚠️ REQUER VALIDAÇÃO UX/PX**.
7. **Uma etapa por vez, com ok explícito.** Ao fim de cada etapa (e de cada passo da etapa 4), apresente o resumo e espere o ok. No **no-pause mode**, as perguntas viram pendências, mas **a passagem de uma etapa para a outra nunca é automática**.

Esta skill não roda git: a branch `ux/migracao-ds-<produto>` e os commits ficam com a `px-setup` (Passo 4). Ao fim de cada passo, diga o que deve entrar no commit.

## Etapa 1: diagnóstico (sem tocar no código)

Siga [`references/diagnostico.md`](references/diagnostico.md). Em resumo:

1. **O produto hoje:** stack, estrutura, onde estão tokens, estilos globais e componentes compartilhados, como os estilos são aplicados.
2. **Baseline:** capturas de todas as telas e estados (default, hover, foco, vazio, erro, loading, desabilitado), no desktop e no celular, com [`scripts/baseline.mjs`](scripts/baseline.mjs) (como usar em [`references/baseline.md`](references/baseline.md)). É a régua de "não regrediu". Sem baseline, a etapa 4 não começa.
3. **Mapa de lacunas:** cada token, cor e componente atual com o destino no `@cit` (troca direta, adaptação, sem equivalente ⚠️, ou conflito com regra inegociável).
4. **Identidade:** o que o produto já tem de marca (logo, cores, fonte, ícones, banners) e se existe styleguide. Isso alimenta a etapa 2.
5. **Profundidade** (`AskUserQuestion`, a decisão é do UX):
   - **Só tokens** (Recomendado quando a stack não é React/shadcn e reescrever não está no escopo): troca cores, fonte, raio, espaçamento e sombra por variáveis do DS; os componentes continuam os do produto.
   - **Tokens + componentes** (Recomendado quando a stack é React): troca também os componentes pelos do `@cit`.
   - **Reescrita no sandbox `@cit`**: quando o produto não comporta o DS. Sai do escopo desta skill e vira `px-audit` → `px-epic`.
6. **Riscos de regressão** e a estratégia recomendada.

Salve em `planning/<produto>/migracao-ds/diagnostico.md`, apresente e **espere o ok**.

## Etapa 2: identidade do produto

**Invoque a skill `styleguide-de-produto`** e passe o diagnóstico: as cores, a fonte e as marcas atuais já estão lá. Ela levanta as perguntas do logo (manter, refinar ou criar, com briefing) e entrega o logo, a marca de cada módulo, as cores conferidas por contraste, a tipografia de marca, os ícones de marca, os banners, as animações, o `tokens.css` e o styleguide publicado.

- Se o produto já tem styleguide aprovado, confirme com o UX e pule para a etapa 3.
- O que é base continua do DS: Inter e a escala na interface, Lucide nos ícones de ação, espaçamento, cores de estado e as faixas de duração das animações.

Ao voltar, registre no diagnóstico o link do styleguide, o caminho do `tokens.css` e as pendências. **Espere o ok.**

## Etapa 3: plano

Passos pequenos, nesta ordem (pule o que a profundidade escolhida não cobre):

1. Tokens globais do `@cit` e o `tokens.css` do styleguide no `index.css`.
2. Cores e variáveis de design.
3. Tipografia (Inter e a escala do DS; a fonte de marca só nos usos do styleguide).
4. Espaçamento, bordas, raios e elevações.
5. Componentes compartilhados.
6. Componentes de página.
7. Estados de interação (hover, foco, ativo, desabilitado, loading, erro).
8. Identidade aplicada: logo no header, no login e no favicon, marcas dos módulos, ícones de marca nos estados vazios, banners e animações.

Para cada passo: o que muda, arquivos, componentes, dependências, riscos e como vai ser validado. Use o modelo em [`references/relatorio.md`](references/relatorio.md#plano). Salve em `planning/<produto>/migracao-ds/plano.md` e **espere o ok**.

## Etapa 4: implementação, um passo por vez

- Token oficial sempre que existir; sem valor solto, sem hex no `className`, sem variável duplicada. Não apague variável ainda em uso: procure as referências antes.
- Componente oficial preservando props, eventos, validações e estados.
- Depois de cada passo, valide: build, testes existentes, console sem erro novo, interações, responsividade e **comparação com a baseline** (`baseline.mjs comparar`). Toda tela que mudou é olhada; mudança que não era esperada é regressão.
- Erro ou regressão se corrige antes de seguir. "Visualmente ok" não fecha passo.
- Resumo do passo (modelo em [`references/relatorio.md`](references/relatorio.md#resumo-de-passo)), atualização do `PX-PROGRESS` e **espere o ok** antes do próximo.

## Entrega

Relatório final em `planning/<produto>/migracao-ds/relatorio.md` (modelo em [`references/relatorio.md`](references/relatorio.md#relatório-final)): arquivos alterados, tokens e componentes trocados ou adaptados, telas impactadas, antes e depois, testes, problemas resolvidos, decisões (com quem aprovou), pendências, o que precisa de validação manual e o link do styleguide. Depois, o fechamento segue pela `px-handoff`.

## Pronto quando

- O produto segue o `@cit` na profundidade combinada e a identidade aprovada no styleguide.
- Nenhuma regressão funcional ou visual contra a baseline; acessibilidade e responsividade mantidas.
- Toda decisão ⚠️ resolvida ou registrada com dono.

## Checkpoint

Grave `planning/<produto>/PX-PROGRESS.md` no formato do protocolo ao fim de cada etapa e de cada passo: *Etapa atual* (`px-migrar-ds · etapa N, passo M`), *Feito*, *Decisões travadas* (profundidade, conflitos resolvidos, identidade aprovada), *Próximo passo* e *Perguntas em aberto*. Para retomar num chat novo: "Leia o PX-PROGRESS e continue de onde parou."

## Quando não usar

- O produto precisa de **redesign de usabilidade** (fluxo ruim, tela confusa): `px-audit`. Esta skill não melhora UX além do que o DS exige.
- **Projeto novo:** `px-start`.
- **Só a identidade**, sem migrar o DS: `styleguide-de-produto` direto.
- **Ajuste pontual** numa tela que já está no DS: `px-change`.
