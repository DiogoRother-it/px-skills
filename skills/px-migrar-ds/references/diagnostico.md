# Etapa 1: diagnóstico

Nada no código muda nesta etapa. A saída é `planning/<produto>/migracao-ds/diagnostico.md` + a pasta `baseline/`.

## 1. O produto hoje

Leia antes de perguntar. Responda com caminho de arquivo, não com impressão.

- **Stack:** framework, versão, CSS (Tailwind, CSS Modules, SCSS, styled-components, CSS puro), biblioteca de componentes (MUI, Bootstrap, Ant, PrimeNG, própria).
- **Tokens e estilos globais:** onde ficam as variáveis, o tema e o reset. Liste os valores de cor, fonte, raio, sombra e espaçamento em uso.
- **Componentes compartilhados:** pasta, lista e quem usa cada um (conte as referências).
- **Como o estilo é aplicado:** classes utilitárias, estilo inline, tema da biblioteca, `!important`. Isso define o risco de troca global.
- **Testes e build:** como roda, o que existe (unitário, e2e), se passa hoje. Se já falha antes de mexer, registre: não é regressão nossa.
- **Telas e rotas:** lista completa, com como chegar em cada estado (login de teste, dado de seed, ação que provoca erro ou vazio).

## 2. Baseline

Veja [`baseline.md`](baseline.md). Sem baseline, a etapa 4 não começa.

## 3. Mapa de lacunas

Uma tabela por tipo. Coluna **Destino** sempre aponta para um token ou componente do `@cit` (consulte `ds-components_v4.md`: famílias, variações e o "Quando usar").

| Hoje | Onde aparece | Função | Destino no @cit | Tipo |
|---|---|---|---|---|
| `#E53935` | alertas, validação de formulário | erro | `--destructive` | troca direta |
| `.btn-outline-primary` | 34 telas | ação secundária | `Button variant="outline"` | troca direta |
| `DataGrid` com rolagem horizontal | Relatórios | tabela larga | Table + colunas priorizadas | conflito (ver conflitos-com-o-ds.md) |
| Stepper próprio | Cadastro | assistente em passos | sem equivalente | ⚠️ |

Tipos: **troca direta**, **adaptação** (equivalente com diferença de prop ou de comportamento; diga qual), **sem equivalente ⚠️**, **conflito** com regra inegociável.

Não presuma correspondência pelo nome: compare props, estados e comportamento antes de dizer "troca direta".

## 4. Identidade atual

O que o produto já tem de marca, para a `styleguide-de-produto` aproveitar: logo e variações, cores que identificam o produto ou módulos, fonte usada em títulos, ícones próprios, banners, animações, guia de marca. Diga se já existe styleguide e onde.

## 5. Profundidade

Recomende uma das três (ver SKILL.md, etapa 1) com o motivo, e pergunte. Registre a escolha em *Decisões travadas*.

## 6. Riscos e estratégia

- **Riscos de regressão:** estilos globais com `!important`, componentes com muitos usos, temas sobrescritos, CSS que depende da ordem de import, testes de snapshot que vão quebrar por mudança visual esperada.
- **Conflitos com o DS** encontrados (com a tela) e a proposta para cada um.
- **Estratégia recomendada:** em que ordem e por quê, o que dá para fazer atrás de flag ou por tela.

## Modelo do arquivo

```markdown
# Diagnóstico da migração para o @cit: <produto>

**Data:** AAAA-MM-DD · **Fonte:** repo local | URL | documentos · **Baseline:** planning/<produto>/migracao-ds/baseline/

## Produto hoje
## Mapa de lacunas
### Tokens
### Componentes
## Conflitos com o DS (decisão do UX)
## Sem equivalente no @cit (⚠️)
## Identidade atual
## Profundidade recomendada
## Riscos e estratégia
## Perguntas em aberto
```
