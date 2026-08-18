#!/usr/bin/env node
// Instalador das skills PX + docs de design system num repo de produto.
// Uso: rodar DENTRO do repo alvo (o diretório de trabalho vira o destino).
//   npx github:DiogoRother-it/px-skills
// ou, após publicar no npm:
//   npx @centralit/px-skills

import { fileURLToPath } from "node:url"
import { dirname, join, relative } from "node:path"
import {
  cpSync, existsSync, mkdirSync, readFileSync, writeFileSync, readdirSync, statSync,
} from "node:fs"

const PKG = dirname(fileURLToPath(import.meta.url))
const TARGET = process.cwd()

const c = { g: "\x1b[32m", y: "\x1b[33m", b: "\x1b[36m", d: "\x1b[2m", x: "\x1b[0m" }
const log = (m) => console.log(m)
const ok = (m) => log(`${c.g}✓${c.x} ${m}`)
const info = (m) => log(`${c.b}·${c.x} ${m}`)
const warn = (m) => log(`${c.y}!${c.x} ${m}`)

log(`\n${c.b}Instalador de skills PX — Central IT${c.x}`)
log(`${c.d}destino: ${TARGET}${c.x}\n`)

// 1. Skills → <target>/.claude/skills/
const skillsSrc = join(PKG, "skills")
const skillsDest = join(TARGET, ".claude", "skills")
mkdirSync(skillsDest, { recursive: true })
let nSkills = 0
for (const name of readdirSync(skillsSrc)) {
  const src = join(skillsSrc, name)
  if (!statSync(src).isDirectory()) continue
  cpSync(src, join(skillsDest, name), { recursive: true })
  nSkills++
}
ok(`${nSkills} skills instaladas em ${relative(TARGET, skillsDest) || ".claude/skills"}`)

// 2. Docs de design system → <target>/docs/design-system/ (não sobrescreve sem avisar)
const dsSrc = join(PKG, "assets", "design-system")
const dsDest = join(TARGET, "docs", "design-system")
mkdirSync(dsDest, { recursive: true })
let nDocs = 0, nSkipped = 0
for (const f of readdirSync(dsSrc)) {
  const dest = join(dsDest, f)
  if (existsSync(dest)) { nSkipped++; continue }
  cpSync(join(dsSrc, f), dest)
  nDocs++
}
ok(`${nDocs} docs de design system em docs/design-system/${nSkipped ? ` (${nSkipped} já existiam, mantidos)` : ""}`)

// 3. Protocolo → <target>/docs/px-protocol.md
const protoDest = join(TARGET, "docs", "px-protocol.md")
if (!existsSync(protoDest)) {
  cpSync(join(PKG, "assets", "px-protocol.md"), protoDest)
  ok("protocolo em docs/px-protocol.md")
} else {
  warn("docs/px-protocol.md já existe — mantido (revise manualmente se precisar atualizar)")
}

// 4. CLAUDE.md — garante que o projeto aponta para o protocolo
const claudeMd = join(TARGET, "CLAUDE.md")
const pointer = "\n## Protocolo PX/UX\n\nAs skills PX seguem o **Protocolo de Interação UX** e as **Skill Prompting Conventions** em [`docs/px-protocol.md`](docs/px-protocol.md). Leia antes de qualquer trabalho de UI.\n"
if (existsSync(claudeMd)) {
  const cur = readFileSync(claudeMd, "utf8")
  if (!cur.includes("docs/px-protocol.md")) {
    writeFileSync(claudeMd, cur.trimEnd() + "\n" + pointer)
    ok("CLAUDE.md atualizado com ponteiro para o protocolo")
  } else {
    info("CLAUDE.md já referencia o protocolo")
  }
} else {
  writeFileSync(claudeMd, `# CLAUDE.md${pointer}`)
  ok("CLAUDE.md criado com ponteiro para o protocolo")
}

log(`\n${c.g}Pronto.${c.x} Abra o Claude Code neste repo e as skills aparecem no menu \`/\`:`)
log(`${c.d}  /px-setup · /px-start · /px-audit · /px-intake · /px-kickoff · /px-epic · /px-proto${c.x}`)
log(`${c.d}  /px-request · /px-change · /px-story · /px-handoff · /px-preview · /px-sync${c.x}`)
log(`${c.d}  /ux-flows · /ux-persona${c.x} ${c.y}(execução — rodam sobre o produto ao vivo)${c.x}`)
log(`\n${c.y}Pré-requisito de UI:${c.x} a biblioteca de componentes (src/components/ui + tokens) precisa`)
log(`${c.d}  estar no repo — ela vem no bundle do design system, não neste pacote de skills.${c.x}`)
log(`\n${c.b}── O que mudou na v1.6.0 ──────────────────────────────────────${c.x}`)
log(`${c.g}ux-flows${c.x} + ${c.g}ux-persona${c.x} ${c.y}(skills novas, execução)${c.x} — usuário sintético, não são entrevista:`)
log(`${c.d}  · ux-flows registra uma jornada multi-tela como flow em e2e/flows/${c.x}`)
log(`${c.d}  · ux-persona percorre o flow em 2 fases isoladas: subagente cego sente (6 personas${c.x}`)
log(`${c.d}    bundled) → você diagnostica pela rubrica de 7 dimensões do px-audit/px-story${c.x}`)
log(`${c.d}  · Recusa rodar contra mockup estático — só produto navegável de verdade${c.x}`)
log(`\n${c.g}px-sync${c.x} ${c.y}(trazida pro pacote central)${c.x} — antes só existia solta, gitignorada:`)
log(`${c.d}  · Sincroniza produto + planning/ + docs/ com o repo central do PX, gated e fast-forward${c.x}`)
log(`${c.d}  · px-handoff agora pergunta se há repo central e delega pro px-sync ao final${c.x}`)
log(`\n${c.g}Manutenção${c.x} — px-protocol.md e README ajustados:`)
log(`${c.d}  · px-protocol.md descreve os 2 destinos do px-handoff (dev + repo central)${c.x}`)
log(`${c.d}  · Removida a promessa de espelhar skills no boilerplate (sem consumidor real)${c.x}`)
log(`\n${c.d}Histórico completo de versões: CHANGELOG.md${c.x}`)
log(`${c.b}────────────────────────────────────────────────────────────────${c.x}\n`)
