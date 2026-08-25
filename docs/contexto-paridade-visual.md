# Contexto: paridade visual entre protótipo e implementação

> Documento de continuidade. Leia inteiro antes de mexer em qualquer coisa desta iniciativa.
> Não é instalado nos projetos: `install.mjs` copia `skills/` e `assets/`, não `docs/`.
> Última atualização: 24/08/2026 · px-skills 1.11.0

---

## 1. O objetivo

**A UI que o UX aprova é a UI que entra em produção, em qualquer projeto, sem reescrita e sem ninguém comparar tela no olho.**

Quatro condições:

1. O dev **copia** a interface em vez de reinterpretar
2. O que ele copia **compila** e resolve todos os imports
3. Divergência é **detectada por máquina**, com imagem, não por revisão
4. Vale para **todo projeto**, por padrão da esteira, não por esforço de quem está atento

Estado hoje: 1 e 2 feitos e publicados. 3 montado e **nunca executado**. 4 tem a regra publicada e nenhum projeto além do piloto migrado.

## 2. Onde cada coisa mora (não inverter a direção)

Isto é o que mais se erra nesta iniciativa, e foi o motivo de este documento existir. O trabalho é **genérico da esteira**, não de um produto. Artefato genérico dentro de repo de projeto vira cópia órfã que ninguém atualiza.

| O que | Casa canônica | Por quê |
|---|---|---|
| Skills e protocolo | **px-skills** | Já era a regra do repo |
| Regra de uso de componente, tokens, lints de código | **centralit-boilerplate** | Já era a regra do repo |
| Template do harness de paridade | **px-skills** (`assets/`) | Genérico, e todo projeto precisa |
| Gerador do PDF de requisitos | **px-skills** (`assets/`) | Genérico |
| Instância do harness (matriz de estados, exceções do produto) | **repo do projeto** | Só faz sentido com os dados daquele produto |
| Mapa de telas, pré-requisitos preenchidos | **pacote de handoff do projeto** | Instância |

**Regra prática:** se o arquivo funcionaria igual em outro produto trocando só nomes, ele é genérico e não mora no projeto.

## 3. O diagnóstico que originou tudo

A divergência visual entre protótipo aprovado e tela implementada **não vinha de desatenção do dev.** Vinha do formato da entrega.

A esteira mandava escrever a tela num arquivo só, com o andaime de demonstração (seletor de papel, seletor de estado, tema, mock) costurado dentro da interface. Para extrair a UI, o dev era obrigado a **editar**. Quem edita reescreve. Cada reescrita muda um espaçamento, uma variante, uma ordem.

Medido numa peça real, um card de produto: **18 decisões visuais que o design system não dita.** Uma delas um `text-[11px]`, fora da escala. Um dev seguindo o DS corretamente escreveria `text-xs` (12px), estaria certo, e a tela sairia diferente. Multiplicado pelas peças de um pacote, são centenas de decisões reproduzidas de olho.

O segundo problema, do mesmo tamanho: **o gate de saída do handoff conferia presença de arquivo e nunca executava nada.** Um pacote saiu montado com uma tela que não compilava e ficou cinco dias registrado como verde.

## 4. O que já está publicado

**centralit-boilerplate, PR #4, mergeado.** Publica `@centralit/tour`; corrige o bug do `navbar` (a prop `tooltip` no hambúrguer quebra sem `TooltipProvider`, e todo projeto novo herdava); sobe `check-camadas.mjs` e `check-tipografia.mjs`; escreve a regra das duas pastas no `CLAUDE.md`.

**px-skills 1.10.0, PR #3, mergeado.** `px-proto` passa a construir em duas pastas (Passo 5 reescrito, com template de UI, contrato, fixture e andaime). `px-handoff` ganha a seção PORTÃO EXECUTÁVEL.

**px-skills 1.11.0, PR #4, mergeado.** Ordem das histórias e rastreabilidade história para código: o `mapa-de-telas.md` passa a carregar ordem e ID estável, inventário de peças obrigatório, e `px-story` ganha as regras de numeração.

## 5. O que é genérico e está no lugar errado

Precisa ser movido para cá. Nada disso deveria estar num repo de projeto.

| Arquivo hoje | Destino |
|---|---|
| `<projeto>/handoff-ux/v1/paridade/paridade.spec.ts` | `assets/paridade/` |
| `<projeto>/handoff-ux/v1/paridade/hooks.ts` | `assets/paridade/` |
| `<projeto>/handoff-ux/v1/paridade/playwright.config.ts` | `assets/paridade/` |
| `<projeto>/handoff-ux/v1/paridade/README.md` | `assets/paridade/` como template; os números do produto saem |
| `<projeto>/handoff-ux/v1/paridade/gates.md` | O conteúdo é a esteira. Vira seção da `px-handoff` ou do `px-protocol.md` |
| `<projeto>/tools/gerar-pdf-qa.mjs` + README | `assets/tools/` |
| `pre-requisitos.md` (os 7 itens genéricos) | Template em `assets/`; o preenchido fica no projeto |

**Fica no projeto, porque é instância:** `matriz-estados.json`, as entradas de `excecoes.md`, `mapa-de-telas.md`, `pre-requisitos.md` preenchido.

**Decisão pendente antes de mover:** o `install.mjs` copia `assets/design-system/*` e `assets/px-protocol.md` para todo projeto. Se o harness for para `assets/`, decidir se o instalador passa a copiá-lo também. A favor: todo projeto ganha o harness sem esforço. Contra: projeto que não usa Playwright recebe arquivo morto.

## 6. Duas armadilhas que eu criei e não consertei

As duas são do mesmo tipo, e é o tipo mais perigoso: **portão que fica verde sem ter verificado nada.**

**`lint:camadas` é opt-in.** Ele só roda se o projeto declarar `camada: ui` no README da pasta de UI. Se ninguém declarar, ele imprime "nenhuma camada declarada" e **sai com sucesso**. É exatamente o falso verde do `tsc` sem `-p` que esta iniciativa existe para combater, reproduzido por mim.
*Correção:* falhar quando encontrar `src/proto/` com arquivos de tela e nenhuma camada declarada. Se existe andaime, tem que existir camada.

**O gate do `px-handoff` não detecta projeto ainda misturado.** Alguém pode empacotar um projeto metade separado achando que a skill resolveu.
*Correção:* medir o tamanho dos arquivos do andaime. O sinal documentado é 100 a 150 linhas independente do tamanho da tela; um arquivo de tela em `proto/` com 800 linhas denuncia UI vazando.

## 7. A suposição mais arriscada, e ela não foi testada

**Nenhum dev consumiu o pacote ainda.** O modelo inteiro depende de uma suposição sem evidência: que "copie a pasta e não edite" funciona no repositório deles.

Não sabemos se o alias resolve, se o Tailwind deles compila as classes, se o roteador pluga onde previmos, se o hook de sessão do harness é preenchível com a autenticação que eles têm. O `pre-requisitos.md` lista os sete pontos de falha conhecidos, mas conhecido não é testado.

**O que fazer antes de escalar a regra para todos os projetos:** um piloto de uma tela só, a menor. O dev pluga no repositório dele e roda. Se copiar sem editar uma linha, a suposição está validada. Se precisar editar, descobrimos onde o modelo quebra com uma tela em vez de com cinco, e corrigimos na origem antes de virar padrão.

É o teste mais barato e mais informativo disponível. Tudo que for construído sem ele é aposta.

## 8. O ângulo que ainda não foi trabalhado

Tudo que existe hoje assume **handoff**: um instantâneo copiado num momento. Isso resolve "a primeira entrega sai fiel" e **não** resolve "continua fiel".

No instante em que o dev copia, as duas versões bifurcam. Nossa correção não chega nele, a dele não chega em nós, e cada delta é um pacote novo, uma cópia nova, uma bifurcação nova. O harness detecta o afastamento; ninguém é dono de fechar.

O ângulo alternativo: **publicar a camada de UI do produto pelo registry**, como o design system já é. Um delta deixa de ser pacote e passa a ser `npx shadcn add @<produto>/<tela>` de novo, com versão. A cópia do dev fica rastreável a um número.

A separação em duas pastas é a pré-condição disso. Implica decidir quem mantém a camada, e por isso não foi feito.

## 9. Pendências abertas com terceiros

**Do time de desenvolvimento** (pedidos meus, sem resposta ainda):
- A linha exata das flags do Chrome headless para hover. **Item mais urgente:** sem ela, as comparações de foco e hover do harness comparam dois estados de repouso, ou seja, cobertura falsa. Melhor remover o bloco do que entregar verde sem medir.
- Os 6 pontos restantes das 9 divergências deliberadas que eles relataram.
- Quantos componentes o kit deles tem e quais divergem, em especial o que corrige a direção do hover, que é fix deles que não temos.
- Como semear carregando, vazio e erro pela resposta de rede. Se der para forçar nos dois lados, esses estados saem do "fora de escopo" e entram na comparação automática.

**Nosso, sem dono:** o drift entre projeto e design system. Projetos ficam arquivos atrás sem nada avisar. Exige skill própria ou ligar o `DesignSync`.

**Projetos não migrados:** dois apps React no boilerplate continuam com UI e andaime misturados, e um deles não usa a pasta `proto/`, então o gate nem ativa lá. Precisa de decisão de convenção antes da migração. Outros dois projetos entregam HTML standalone e não têm caminho de paridade nenhum.

## 10. Armadilhas técnicas já pagas (não reintroduza)

**`npx tsc --noEmit` sem `-p` compila zero arquivo e sai com sucesso.** O `tsconfig.json` da raiz do boilerplate tem `"files": []` e só `references`. Medido: com erro de tipo plantado, sem `-p` dá exit 0 e nenhuma linha; com `-p tsconfig.app.json` dá exit 2 e a mensagem. **Todo gate novo tem que ser rodado uma vez contra erro plantado**, e a mensagem registrada. Sem essa prova, não conte o gate.

**`npm run lint` é corrente com `&&` começando pelo oxlint.** Se o oxlint acha erro, os lints do DS não rodam e a saída não deixa claro. Ao investigar falha, rodar cada um separado.

**`check-caixa-alta` tem falso positivo** com identificador em maiúscula dentro de template literal (`${TINT[x]}` foi acusado como copy em caixa alta). Gate que dá falso positivo é gate que o time aprende a ignorar. Vale corrigir a heurística.

**PDF do pdfkit: rodapé abaixo da margem cria página.** Escrever o número da página fora da área útil faz o pdfkit entender transbordo e abrir página nova, uma por rodapé. Gerou 111 páginas em vez de 37. Correção: zerar `page.margins.bottom` antes de escrever e restaurar depois.

**PDF do pdfkit: `grep` não serve para verificar conteúdo.** Ele faz kerning e quebra as palavras em glifos separados, então busca por substring nunca acha, mesmo sem compressão. Usar extrator de verdade (`pdfjs-dist`).

**Glifo fora de Latin-1 vira caixa preta no PDF.** As fontes padrão do pdfkit são WinAnsi. Trocar por equivalente ASCII, não remover.

**Contradição entre `description` e corpo da skill faz a trava ganhar.** A própria 1.8.1 documentou isso, e eu repeti na 1.10.0: a `description` do `px-proto` anunciava que o protótipo não é código de produção, contradizendo a regra nova. Ao mudar regra central de uma skill, revisar `description` e introdução.

## 11. Como verificar que está tudo de pé

```bash
# no repo de um projeto que usa o boilerplate
npx tsc --noEmit -p tsconfig.app.json   # 0 erros
npm run lint                            # inclui lint:camadas
npm run lint:tipografia                 # fora da corrente, decisão pendente
npm run build

# ordem dos critérios de aceite, dentro do pacote de handoff
for f in $(find . -path "*/stories/*.md"); do
  seq=$(grep -oE "CA-[0-9]+" "$f" | sed 's/CA-//' | awk '!v[$0]++' | tr '\n' ' ')
  ord=$(echo "$seq" | tr ' ' '\n' | grep -v '^$' | sort -n | tr '\n' ' ')
  [ "$seq" != "$ord" ] && echo "FORA DE ORDEM: $f"
done
```

## 12. Ordem sugerida para retomar

1. **Consertar as duas armadilhas da seção 6.** São ~10 linhas cada e sem elas a condição 4 do objetivo depende de atenção humana, que é o que a iniciativa existe para remover.
2. **Mover o que a seção 5 lista**, decidindo antes a questão do `install.mjs`.
3. **Rodar o piloto da seção 7** antes de migrar mais projeto. É o que valida ou derruba a suposição central.
4. Só então migrar os projetos pendentes.

O item 3 tem prioridade sobre o 4 mesmo parecendo menor. Migrar cinco telas de um projeto com o modelo não validado é multiplicar por cinco um retrabalho possível.
