# Engineering Directives v4 — Stack shadcn/ui

Documento de regras de implementação técnica. Agnóstico de produto — vale para qualquer projeto que adote shadcn/ui como base de componentes. Substitui o v3 nesses projetos. O v3 permanece válido para projetos no padrão antigo (artifact HTML standalone, sem build).

> **Hierarquia de documentos**
> - `ds-foundations.md` — tokens, escalas, princípios de base. Fonte da regra.
> - `ds-components.md` — specs de comportamento de componente + mapeamento pro shadcn/ui.
> - `ds-patterns.md` — estruturas de tela.
> - `uikit-[projeto].html` — tokens visuais concretos do projeto. Prevalece sobre este arquivo para valores visuais.
> - **Engineering Directives v4** (este arquivo) — como as regras acima viram código nesta stack. Não redefine valor nenhum, só mecanismo de aplicação.

---

## Stack técnica

- React + TypeScript, com bundler real (Vite ou Next.js)
- Tailwind CSS configurado via build — nunca via CDN
- shadcn/ui como base de componentes (Radix UI por baixo)
- Lucide como biblioteca de ícones
- Inter como fonte padrão (sobrescrita pelo UI Kit do projeto, se aplicável)

Instalação de componente sempre via CLI (`npx shadcn add [componente]`) — nunca copiar código de componente manualmente de outro lugar. O arquivo gerado passa a viver no repositório e pode ser editado livremente: você é dono do código a partir da instalação.

---

## Mecanismo de aplicação das regras de Foundations

Esta seção não define regra nova — só diz como cada regra do `ds-foundations.md` vira código nesta stack.

| Regra (definida em Foundations) | Como aplicar nesta stack |
|---|---|
| Cor sempre via token | Tokens como CSS variables no `:root`/`@theme`, mapeados no `tailwind.config`. Lint bloqueia hex hardcoded em `className` |
| Espaçamento em múltiplos de 8px | Restringir a escala de espaçamento do Tailwind no `tailwind.config` a valores que resultam em 8/16/24/32/48px. Lint bloqueia classe fora da escala |
| Border radius na escala (4/8/12/16/999) | Uma única variável `--radius` no `:root`; os demais valores derivam dela via `calc()`. Não declarar radius solto em componente individual |
| Ícones via Lucide | Importar de `lucide-react`, tamanho via prop `size` (16/20/24). Não precisa de helper de CSS — é SVG com dimensão própria, sem espaço fantasma de glifo de fonte |
| Foco visível padrão | Usar a classe `focus-visible:ring-2` já presente nos componentes shadcn, com a cor do token `ring` ajustada pro projeto |
| Motion (`transform`/`opacity` apenas) | Componentes shadcn com animação (Dialog, Accordion, etc.) já seguem isso via Radix + `tailwindcss-animate`. Não adicionar animação de outra propriedade |
| Sem gradiente decorativo | Revisão manual — não é lintável |
| UX Writing (sem travessão, sem caixa alta total) | Lint de conteúdo separado, varre strings literais em JSX. Independente do shadcn |

---

## Regras específicas de shadcn

1. **Nunca aceitar a aparência default do componente sem reestilizar.** Ao adicionar um componente pela primeira vez, ajustar suas classes Tailwind pra bater com `ds-components.md`/`ds-patterns.md` e os tokens do projeto. A partir daí, esse arquivo é a versão canônica do componente — não reestilizar de novo a cada uso.

2. **Todo componente adicionado precisa ser auditado pro grid de 8px antes do commit.** O código gerado pelo shadcn não garante isso por padrão (`px-3`, `py-2.5` são comuns e ficam fora do grid). Corrigir manualmente ou via lint antes de considerar o componente pronto.

3. **Componente sem equivalente direto no shadcn/Radix** — compor com primitivas existentes (ex: Multi Select = `Command` + `Popover` + `Badge`) e documentar a composição no próprio arquivo do componente. Não inventar solução fora do ecossistema Radix sem necessidade.

4. **Exceção documentada: Data Grid avançado.** Não existe em shadcn nem por composição — usar uma biblioteca headless externa (ex: TanStack Table) por trás, mantendo a casca visual em Tailwind/shadcn.

5. **`position: fixed` é esperado e correto** em Dialog, Sheet, Popover, Tooltip — shadcn usa portal do Radix pra isso de propósito. A restrição de `position:fixed` do v3 só vale para artifacts HTML standalone fora de um app real (caso raro, ex: mockup sem repositório).

---

## Processo de handoff → dev (obrigatório)

Todo developer handoff summary produzido pelo UX carrega, além do resumo de mudanças, um **checklist de Definition of Done** que o dev é obrigado a cumprir antes de abrir o PR. Dois itens são não-negociáveis:

1. **Branch intermediária obrigatória.** Nunca commitar nem mesclar direto na `main`. O dev cria uma branch de trabalho (`feat/…`, `fix/…`) a partir da `main` atualizada, implementa nela e só integra via PR revisado. Isola a mudança e permite validar antes do merge.

2. **Validação visual COMPLETA via Playwright, com zero perda de UI.** Antes do PR, o dev roda o Playwright para renderizar e capturar **todas** as telas/rotas e **todos** os estados de cada componente (default, loading, empty, error, disabled, read-only, foco, hover e responsivo nos breakpoints Mobile / Tablet / Desktop). O objetivo é garantir que nenhuma UI existente foi perdida, quebrada ou regredida pela mudança. O critério é cobertura: nenhuma seção do showcase e nenhum estado documentado no handoff pode ficar sem validação.
   - **Meta de fidelidade: 99% de alinhamento** entre a interface entregue pelo UX (o que o dev está puxando do design system) e o que é reproduzido na branch intermediária. O Playwright é a ferramenta **fortemente recomendada** para fechar esse gap — comparar tela a tela, estado a estado, até a reprodução bater com a referência. Divergência não é "detalhe do dev": é regressão a corrigir antes do PR.
   - Evidências (screenshots/trace por breakpoint) anexadas ao PR.
   - Qualquer diferença visual não intencional bloqueia o merge até ser resolvida.

### Bloco de Definition of Done (colar ao final de todo handoff)

```markdown
## Definition of Done (obrigatório para o dev)
- [ ] Trabalho feito em branch intermediária a partir da `main` atualizada (nunca commit direto em `main`); integração só via PR.
- [ ] Validação visual COMPLETA com Playwright: todas as telas e todos os estados (default / loading / empty / error / disabled / read-only / hover / foco / responsivo) renderizados e conferidos.
- [ ] Zero perda de UI: nenhuma seção, variante ou estado existente foi removido, quebrado ou regredido.
- [ ] Evidências do Playwright (screenshots/trace por breakpoint Mobile/Tablet/Desktop) anexadas ao PR.
- [ ] `tsc -b` verde e `npm run lint:spacing` limpo.
```

---

## Gestão de contexto de chat

Quando o contexto da conversa estiver longo e consumindo tokens excessivos, sinalizar o usuário ao final da resposta, após concluir a entrega, como última linha:

> ⚠️ **Contexto longo detectado.** Recomendo abrir um novo chat e colar o prompt de continuidade.

Critérios: muitas iterações no mesmo arquivo, respostas ignorando regras já estabelecidas, ou histórico pesado o suficiente pra afetar precisão. Sempre concluir a entrega antes de sinalizar.
