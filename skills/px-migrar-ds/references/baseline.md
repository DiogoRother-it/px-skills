# Baseline: a régua de "não regrediu"

Antes de qualquer mudança, capture todas as telas e estados do produto. Depois de cada passo, capture de novo e compare. É assim que se prova que a migração não quebrou nada.

## 1. Subir o produto

Repositório local rodando (preferido: libera todos os estados e o login de teste do seed) ou URL de homologação. Use o preview do app (`.claude/launch.json` + `preview_start`), não um servidor solto no terminal.

## 2. Listar as rotas e os estados

Crie `planning/<produto>/migracao-ds/rotas.json` (formato no topo de `scripts/baseline.mjs`). Para cada tela, pelo menos:

- **default**;
- **vazio** e **erro**, quando a tela tem lista ou formulário;
- **loading**, se der para segurar (rota lenta de propósito, mock);
- **hover** e **foco** nos componentes compartilhados (botão, campo, item de menu), numa tela que os tenha;
- **desabilitado** e **somente leitura**, onde existirem.

As vistas são sempre duas: desktop (1440) e celular (390). O script desliga animações para a imagem não variar.

Estado que não dá para provocar fica como pergunta em aberto no diagnóstico ("erro de API em Relatórios: sem como provocar no ambiente local").

## 3. Capturar

O script usa o pacote `playwright` do projeto do produto. Se o projeto não tiver, peça ao UX para instalar como dependência de desenvolvimento.

```bash
node .claude/skills/px-migrar-ds/scripts/baseline.mjs capturar planning/<produto>/migracao-ds/rotas.json planning/<produto>/migracao-ds/baseline --base http://localhost:5173
```

Erros de console que já existem ficam em `baseline/relatorio.json`: eles não são regressão nossa.

## 4. Comparar depois de cada passo

```bash
node .claude/skills/px-migrar-ds/scripts/baseline.mjs capturar planning/<produto>/migracao-ds/rotas.json planning/<produto>/migracao-ds/passo-N --base http://localhost:5173
node .claude/skills/px-migrar-ds/scripts/baseline.mjs comparar planning/<produto>/migracao-ds/baseline planning/<produto>/migracao-ds/passo-N
```

O `comparar` diz quais telas mudaram, quais sumiram e onde há erro de console novo. Abra cada par que mudou (leia as duas imagens) e classifique:

- **esperado:** é o que o passo devia mudar (cor, fonte, raio, componente);
- **regressão:** elemento sumiu, mudou de lugar, texto mudou, estado quebrou, layout vazou no celular.

Regressão se corrige antes de fechar o passo. Tela que sumiu ou erro de console novo fazem o script sair com código 1.

## Onde guardar

As capturas ficam em `planning/<produto>/migracao-ds/`. Se o repositório for versionado, pergunte se as imagens entram no Git ou vão só como evidência no Merge Request (o protocolo pede evidência do Playwright anexada).
