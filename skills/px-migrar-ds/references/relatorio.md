# Modelos: plano, resumo de passo e relatório final

## Plano

`planning/<produto>/migracao-ds/plano.md`

```markdown
# Plano da migração para o @cit: <produto>

**Profundidade:** só tokens | tokens + componentes · **Styleguide:** <link> · **Baseline:** <pasta>

| # | Passo | O que muda | Arquivos | Componentes | Depende de | Risco | Como valido |
|---|---|---|---|---|---|---|---|
| 1 | Tokens globais | variáveis do @cit + tokens.css no index.css | src/index.css | todos (indireto) | nada | baixo | build, baseline de todas as telas |
| 2 | Cores | cores soltas → tokens semânticos | ... | ... | 1 | ... | ... |
```

## Resumo de passo

Ao fim de cada passo da etapa 4, na conversa e anexado ao fim do `plano.md`:

```markdown
### Passo N: <nome>, AAAA-MM-DD

- **Alterações:** o que mudou, em uma linha por item.
- **Arquivos:** lista.
- **Validação:** build ok/falhou · testes X de Y · console sem erro novo · interações conferidas: ... · responsivo conferido em 390 e 1440.
- **Contra a baseline:** telas que mudaram (esperado) e telas que mudaram sem ser esperado (regressão, com o que foi feito).
- **Problemas:** o que apareceu e como resolveu.
- **Pendências:** o que ficou, com dono.
- **Commit sugerido:** `ux(<produto>): <passo>` com os arquivos acima.
```

## Relatório final

`planning/<produto>/migracao-ds/relatorio.md`

```markdown
# Relatório da migração para o @cit: <produto>

**Período:** ... · **Profundidade:** ... · **Styleguide:** <link> · **Branch:** ux/migracao-ds-<produto>

## Resumo
Duas ou três frases: o que o produto era, o que é agora, o que ficou de fora.

## Arquivos modificados
## Tokens e estilos substituídos
| Antes | Depois | Onde |
## Componentes
### Trocados pelo @cit
### Adaptados (e por quê)
### Sem equivalente (⚠️, com a decisão)
## Identidade aplicada
Logo no header, no login e no favicon, marcas dos módulos, ícones de marca, banners, animações, fonte de marca: onde entrou.
## Telas impactadas (antes e depois)
## Testes e validações
## Problemas encontrados e como foram resolvidos
## Decisões (com quem aprovou e quando)
## Precisa de validação manual
## Pendências
```
