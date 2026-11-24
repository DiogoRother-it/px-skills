# Fase 1: entrevista

Se a skill foi chamada pela `px-migrar-ds`, leia antes o diagnóstico dela (`planning/<produto>/migracao-ds/diagnostico.md`): stack, cores, fontes e telas atuais já estão lá. Pergunte só o que faltar.

Uma pergunta de cada vez. Explique o porquê em uma linha, dê um exemplo e um padrão recomendado. "Não sei" não trava: use o padrão, registre como premissa em `familia.pendencias` e siga.

## Blocos

1. **O sistema.** Nome, o que faz, quem usa. *Por quê:* a forma de cada módulo nasce do que ele faz para alguém.
2. **Os módulos.** Lista com nome e, para cada um, **um verbo** do que ele faz para o usuário (Registra, Comprova, Mede, Avisa). *Por quê:* o verbo é a ponte entre o nome e a forma, e vira o subtítulo no header. Se o UX não souber o verbo, proponha 2 ou 3 por módulo (`AskUserQuestion`).
   - Ids em kebab-case, sem acento (`hyper-agents`, `avaliacao`): viram nome de arquivo.
3. **O logo do produto.** Existe? Peça o arquivo (SVG de preferência; PNG ou PDF servem). Só registre a situação aqui (tem e é bom, tem e precisa de ajuste, não tem): a decisão e o briefing completo são a fase 2 ([`logo.md`](logo.md)).
4. **A marca de referência (marca-mãe).** De onde vem a linguagem além do logo: a marca da empresa, do cliente ou da área, e o guia da marca, se houver. *Sem logo e sem marca-mãe:* o logo criado na fase 2 vira a referência.
5. **Onde as marcas vão viver.** Header, menu lateral, login, home, favicon, materiais. *Por quê:* define os tamanhos que precisam ler bem (16 px no favicon e no menu, 24 px no header).
6. **Fundo da aplicação.** A cor do fundo onde as marcas aparecem (padrão `#EEF0F4`) e o fundo escuro (padrão `#0E1420`). Busque no `src/index.css` ou nos tokens do DS antes de perguntar.
7. **Cores reservadas.** O que nenhum módulo pode usar: cores de estado (erro, sucesso, atenção, info), a cor da IA, a cor da marca-mãe, cores de outra família que convive na mesma tela. Busque nos tokens do DS e confirme com o UX.
8. **Acento.** Uma peça de cada marca muda de cor nas versões com acento (no X AI, a peça do agente em verde-limão)? `AskUserQuestion`: "Sim, com a cor da marca-mãe (Recomendado se ela tiver uma cor de destaque)", "Sim, outra cor", "Não". Sem acento, o `gerar.py` faz só duas versões.
9. **Uma cor por módulo ou uma só.** `AskUserQuestion`. Uma por módulo ajuda a reconhecer o módulo no menu; uma só deixa a identidade só para a forma e é mais fácil de manter.
10. **Tipografia de marca.** Qual fonte a marca-mãe usa e se há licença para web. *Por quê:* a fonte de marca aparece no nome do produto e nos banners; a interface continua na Inter do DS. Busque no guia da marca antes de perguntar.
11. **Ícones de marca.** Onde o produto precisa de desenho próprio além da marca: estado vazio, abertura, onboarding, banners. *Por quê:* ícone de ação é Lucide e não se desenha; ícone de marca, sim.
12. **Banners e materiais.** Quais (login, boas-vindas, novidade, e-mail, apresentação), em que formato e com que texto. Se o UX não souber, proponha login 1200 x 400 e novidade 1200 x 400.
13. **Animações.** Onde a marca anima (carregamento, abertura, login) e se algum módulo tem um movimento próprio. *Por quê:* animação sem lugar definido vira enfeite que atrapalha a tela de trabalho.
14. **Campos opcionais do styleguide.** Mostre a lista de [`campos-do-styleguide.md`](campos-do-styleguide.md) (`AskUserQuestion` com `multiSelect`) e grave os escolhidos em `familia.campos`.
15. **Estilo de partida.** Se o UX já tem um estilo em mente (geométrico, contorno, arredondado, gradiente, monograma, desenho livre), registre; se não, ele se decide na fase 3 a partir do logo. Não assuma o estilo do CITSmart X AI.
16. **Quem valida.** Nome de quem aprova a família (o dono da marca-mãe, o PO). Vai para o README e para as pendências.

## Saída

O esqueleto do `produtos.json` em `planning/<sistema>/marcas/`, a partir de `exemplo/produtos.json`, sem formas e sem cores ainda (as cores podem ficar `"#000000"` provisórias). Eco com tudo e o ok do UX.
