# Conflitos entre "preservar" e as regras inegociáveis do DS

A migração preserva layout, conteúdo e comportamento. O `@cit` tem regras que não se negociam. Quando as duas coisas batem, **não decida sozinho**: liste no diagnóstico (ou no resumo do passo) com a tela, o risco e uma proposta, e pergunte (`AskUserQuestion`: a proposta como "(Recomendado)", "Manter como está e registrar exceção", "Outro"). A exceção aprovada vai para *Decisões travadas* com quem aprovou.

| Regra do DS | Como achar | Proposta típica | Risco de mudar |
|---|---|---|---|
| **Tabela sem rolagem horizontal** | `overflow-x: auto/scroll` em tabela, grid com muitas colunas | priorizar colunas, linha expansível ou drawer de detalhe | muda onde o dado aparece: valide com quem usa |
| **Um overlay por vez** (só Drawer pode abrir Modal) | modal que abre modal, popover dentro de modal | trocar por *switch* (fecha um, abre o outro) ou mover para Drawer | muda o fluxo: precisa de ok |
| **Um botão primário por tela/contexto** | mais de um botão de destaque | um primário, o resto `outline` ou `ghost` | só visual, baixo |
| **Sem caixa alta total e sem travessão** | `text-transform: uppercase`, textos em maiúsculas, "—" | peso e espaçamento no lugar da caixa alta; texto fica como está até o UX aprovar a mudança de copy | texto é conteúdo: regra 1 manda preservar |
| **Ícones Lucide em 16/20/24** | Font Awesome, Material Icons, SVG solto, emoji | ícone Lucide equivalente pela função; ícone de marca vai para a `styleguide-de-produto` | ícone sem equivalente: ⚠️ |
| **Espaçamento em múltiplos de 8** | valores como 5, 10, 15, 18 px | arredondar para o token mais próximo | pode mudar a densidade: compare na baseline |
| **Cor só por token, nunca hex no `className`** | hex em classe, estilo inline | token semântico pelo papel | baixo, se o mapa por função estiver certo |
| **Disabled é papel próprio** (`gray-100`/`gray-400`) | opacidade reduzida como desabilitado | papel Disabled | baixo |
| **Contraste WCAG AA** | cor nova que não passa | ajustar o token, não a tela | baixo |
| **Componentes via `npx shadcn add`, reestilizados** | componente copiado de outro lugar | instalar pelo registry `@cit` | médio, se o componente copiado tem comportamento próprio |

O que o `@cit` não cobre (componente, padrão de tela) não é conflito, é **sem equivalente**: marque ⚠️ REQUER VALIDAÇÃO UX/PX e proponha composição com primitivas do DS, documentada.
