---
name: px-sync
description: Sincroniza o repositório CENTRAL do PX (o monorepo/núcleo onde vivem produto, planning e docs de vários projetos — ex "px-projects") com o estado completo de trabalho. Diferente do px-handoff (que entrega um pacote reduzido pro repo do DEV), o px-sync sobe o espelho completo pra que o time de PX puxe a versão mais atual e continue a idealização. Protege pastas marcadas como intocáveis (ex uma prova de conceito paralela) e nunca apaga trabalho alheio sem confirmação. Use quando o líder disser "atualizar o repo central do PX", "sincronizar o núcleo", "subir a versão mais atual pro time de PX continuar", "salvar o estado de idealização no git", "push pro repo dos PX", "espelhar meu trabalho no núcleo".
compatibility: claude-code
metadata:
  audience: px-ux
  workflow: sync
---

# px-sync — sincroniza o repo central do PX

Times de PX costumam trabalhar num **monorepo central** (ex `px-projects`) onde vivem vários produtos/iniciativas ao mesmo tempo. Esta skill sobe o **estado completo de trabalho** desse monorepo, de forma que qualquer PX que clone/puxe tenha a **versão mais atual** para continuar idealizando outros fluxos do sistema.

**Não confundir com `px-handoff`:**

| | `px-handoff` | `px-sync` (aqui) |
|---|---|---|
| Destino | Repo do **dev** | Repo **central** do PX |
| Conteúdo | Reduzido: HTML + UI Kit + stories | **Completo**: produto + `planning/` + `docs/` + `.claude/` + config |
| Git | Branch **órfã** (limpa) | **`main`**, fast-forward, histórico preservado |
| Propósito | Implementar | Seguir idealizando |

**Público:** o líder UX/PX. Seja direto: confirme o escopo, proteja o que não pode ser tocado, e só então faça o push (sempre gated).

Contexto inicial via slash: `$ARGUMENTS` (opcional — resumo do que está sendo sincronizado). Se vazio, infira do diff.

## Prompting

Segue `Skill Prompting Conventions` do `CLAUDE.md`. Decisões enumeráveis via `AskUserQuestion`; toda decisão traz o porquê + default recomendado; eco antes de despachar.

## Princípio central

> **O repo central carrega tudo que o próximo PX precisa para assumir o projeto e seguir idealizando.** A régua de cada arquivo é: *"isso ajuda o próximo PX a continuar?"* — não "é produto ou não".

**Entra** (conhecimento que permite continuar):
- Produto (HTML, UI Kit dos protótipos).
- **Hub de protótipos navegáveis**, se o produto mantiver um (ex `<produto>/protos/index.html`, gerado pelo `ux-flows`/fluxo de proto pra facilitar acesso de stakeholders/QA) — só links pro arquivo real, nunca cópia. **Manutenção obrigatória:** todo proto novo criado ou removido desde o último sync precisa refletir aqui antes do commit — checar isso é parte do BLOCO 1.
- `planning/` — o registry: PX-PROGRESS, épicos, requests, **stories** (incl. reformuladas), decisões, auditorias.
- `docs/` — design system + `px-protocol.md` (as regras que o projeto segue).
- `CLAUDE.md` — onboarding do projeto.
- `.claude/launch.json` — como subir os previews.

**Não entra** (ambiente/tooling, não conhecimento de produto):
- `.mcp.json` e qualquer config de MCP/ambiente/segredo.
- `.claude/skills/` — **as skills PX têm distribuição central**; versioná-las no repo do projeto cria duas fontes da verdade que divergem. O próximo PX instala as skills do canal central (`px-skills`). (Se um projeto NÃO tiver canal central, aí sim as skills entram.)

> Regra durável: manter essas exclusões no `.gitignore` do projeto (`.mcp.json`, `.claude/skills/`) para que o "espelho" seja automático e o `launch.json` continue versionado.

---

# Os blocos do sync

> Avance na ordem. Nunca pule o BLOCO 2 (proteções) — foi a ausência dele que quase apagou trabalho num incidente real.

## BLOCO 1 — Escopo (o que vai subir)
**Decidir:** confirmar que o push leva o estado completo.
**Por que importa:** o repo central depende do registry (`planning/`) e das decisões pra retomar o trabalho. Deixar de fora quebra a continuidade.
**Fazer:**
- Rodar `git status -sb` e resumir os três blocos: **modificados**, **novos (untracked)**, **removidos**.
- Escopo padrão = **tudo que não está no `.gitignore`** (produto, `planning/`, `docs/`, `.claude/`, `CLAUDE.md`, `.mcp.json`).
- **Protos navegáveis:** se o diff criou/removeu/renomeou um `.html` de protótipo do produto, atualizar o hub de protos (card + link relativo) antes de seguir, se este projeto mantiver um. Nunca sobe proto novo sem entrada correspondente no índice.
- Confirmar que nenhum segredo real está fora do `.gitignore` (`.env`, tokens, credenciais). Se houver, **bloquear** e ajustar o `.gitignore` antes.

## BLOCO 2 — Proteções (barreira obrigatória antes de qualquer commit)
**Por que importa:** o repo central é compartilhado. Um push descuidado apaga trabalho de terceiros ou reescreve histórico do time.
**Verificar, nesta ordem:**

1. **Branch de backup.** Criar `backup/<contexto>-<AAAA-MM-DD>` apontando pro estado atual antes de qualquer operação que altere histórico (reset/rebase). Barato e reversível.
2. **Preservar pastas intocáveis.** Pergunte/confirme se este projeto tem alguma pasta marcada como fora do escopo do sync (ex: uma prova de conceito paralela tipo `pov/`, um experimento isolado). Se houver, confirme que o diff **não a toca** — `git diff --name-only origin/main..HEAD | grep -i <marcador>`. Se retornar algo, parar e confirmar com o líder.
3. **Não apagar projetos alheios sem confirmação.** Se o working tree mostra **deleções em massa** de diretórios que não são o foco atual (outros produtos), **surfar a lista e confirmar a intenção** via `AskUserQuestion` antes de commitar. Deleção intencional de projeto inteiro do repo compartilhado exige aceite explícito do líder.
4. **Backup físico do que for arriscado.** Se um alinhamento (`reset --hard`) puder sobrescrever um arquivo modificado importante, copiar pro scratchpad antes e restaurar depois.

## BLOCO 3 — Sincronizar com o remoto (antes de commitar)
**Decidir:** como conciliar o local com o `origin/main`.
**Fazer:**
- `git fetch origin`.
- **Em dia** (`main` = `origin/main`) → seguir direto pro BLOCO 4.
- **Atrás** (só faltam commits do remoto) → integrar (`pull`/rebase) e resolver conflitos antes de commitar.
- **Divergiu** (à frente E atrás) → com a branch de backup do BLOCO 2 já criada, alinhar a base ao remoto (`reset --hard origin/main`) e reaplicar o trabalho local por cima, de modo que o push final seja **fast-forward**. Nunca force-push no `main` compartilhado sem aceite explícito.

## BLOCO 4 — Commits organizados
**Por que importa:** o time lê o histórico pra entender a evolução. Commits temáticos > um commit monolítico.
**Fazer:**
- Separar em commits lógicos quando fizer sentido (ex: `chore:` para remoções estruturais, `feat(<área>):` para o trabalho de produto, `docs:` para registry/decisões).
- **Escrever a mensagem via arquivo** (`git commit -F <arquivo>`) ou aspas simples seguras — **nunca** here-string de PowerShell (`@'...'@`) dentro do Bash, que vaza `@` para o assunto do commit.
- Encerrar a mensagem com `Co-Authored-By` conforme a convenção do harness.

## BLOCO 5 — Eco e push (gated)
**Fazer, nesta ordem:**
1. Passar pelo **GATE** abaixo — só avança se tudo verde.
2. Apresentar o eco final e aguardar **aceite explícito** do líder.
3. Só então `git push origin main`.
4. Confirmar o push com o range de hashes (ex: `48df22f..636fc35`).

## GATE — Barreira de saída (antes do eco final)

**Qualquer item ✗ bloqueia o push.**

**Proteções**
- [ ] Branch de backup criada
- [ ] Pastas intocáveis verificadas como intactas (ou alteração explicitamente autorizada)
- [ ] Nenhuma deleção de projeto alheio sem confirmação do líder
- [ ] Nenhum segredo fora do `.gitignore`

**Push**
- [ ] `main` será **fast-forward** sobre `origin/main` (sem force, sem reescrever histórico compartilhado)
- [ ] Mensagens de commit limpas (sem `@` vazado, sem placeholders)
- [ ] Aceite explícito do líder para o push

## Eco final

Antes de fechar, repita em 3–4 linhas: *"Sync do repo central: **N** commits fast-forward sobre `origin/main`. Sobe: **<resumo>**. Preservado: <pastas intocáveis> + <o que for sensível>. Backup: `backup/<...>`. Confirma o `git push origin main`?"*. Só então faça o push.

## Regras

- **Espelho completo**, não pacote reduzido — isso é `px-handoff`, não `px-sync`.
- **Nunca faz push sem aceite explícito do líder.**
- **Sempre cria branch de backup** antes de operação que altere histórico.
- **Pastas intocáveis são intocáveis** salvo pedido explícito.
- **Nunca apaga projeto alheio do repo compartilhado** sem confirmação.
- **Fast-forward no `main`** — nunca force-push sem aceite.
- **Mensagem de commit via arquivo** — nunca here-string de PowerShell no Bash.

## Relação com o fluxo

```
                              ┌─→ px-handoff → repo do DEV (pacote reduzido, implementar)
px-request → px-story → ...  ─┤
                              └─→ px-sync    → repo CENTRAL do PX (espelho completo, idealizar)
```

> `px-sync` e `px-handoff` são destinos diferentes do mesmo trabalho. A `px-handoff` pergunta o destino no início e delega pra `px-sync` quando o alvo é o repo central (ou ambos).
