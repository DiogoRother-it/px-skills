#!/usr/bin/env node
// Instalador das skills PX + docs de design system num repo de produto.
// Uso: rodar DENTRO do repo alvo (o diretório de trabalho vira o destino).
//   npx github:DiogoRother-it/px-skills
// ou, após publicar no npm:
//   npx @centralit/px-skills

import { fileURLToPath } from "node:url"
import { dirname, join, relative } from "node:path"
import {
  copyFileSync, existsSync, mkdirSync, readFileSync, writeFileSync, readdirSync, statSync,
} from "node:fs"

const PKG = dirname(fileURLToPath(import.meta.url))
const TARGET = process.cwd()

// Cópia recursiva própria. NÃO usar fs.cpSync aqui: no Node 24 (Windows) a versão
// nativa e recursiva do cpSync corrompe o encoding do destino quando o caminho tem
// caractere fora do ASCII ("Relatórios" virava "RelatÃ³rios"), sem lançar erro —
// o instalador contava as skills, e elas iam parar numa pasta irmã com nome quebrado.
// copyFileSync passa pelo mesmo caminho de writeFileSync, que nunca teve o problema.
// copyFileSync também sobrescreve por padrão, então reinstalar não lança exceção.
const copyDir = (src, dest) => {
  mkdirSync(dest, { recursive: true })
  for (const entry of readdirSync(src, { withFileTypes: true })) {
    const s = join(src, entry.name), d = join(dest, entry.name)
    if (entry.isDirectory()) copyDir(s, d)
    else copyFileSync(s, d)
  }
}
const fail = (m) => { console.error(`\x1b[31m✖\x1b[0m ${m}`); process.exit(1) }

// Versão: fonte única é o package.json. Nunca escreva o número à mão aqui.
const VERSION = JSON.parse(readFileSync(join(PKG, "package.json"), "utf8")).version

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

// Marca da versão já instalada neste repo — é o que permite resumir só o delta.
const stampPath = join(skillsDest, ".px-skills-version")
const prev = existsSync(stampPath) ? readFileSync(stampPath, "utf8").trim() : null
let nSkills = 0
const faltando = []
for (const name of readdirSync(skillsSrc)) {
  const src = join(skillsSrc, name)
  if (!statSync(src).isDirectory()) continue
  const dest = join(skillsDest, name)
  copyDir(src, dest)
  // Verificação pós-cópia: contar só o que chegou de fato no destino. "N skills
  // instaladas" sem conferir o arquivo é o falso verde que a 1.17.1 corrigiu.
  if (existsSync(join(dest, "SKILL.md"))) nSkills++
  else faltando.push(name)
}
if (faltando.length) {
  fail(`${faltando.length} skill(s) não chegaram ao destino: ${faltando.join(", ")}\n` +
       `  esperado em ${skillsDest}\n` +
       `  nada foi marcado como instalado; verifique o caminho e rode de novo`)
}
ok(`${nSkills} skills instaladas em ${relative(TARGET, skillsDest) || ".claude/skills"}`)
writeFileSync(stampPath, VERSION + "\n")

// 2. Docs de design system → <target>/docs/design-system/, os do DS QUE ESTE PROJETO USA.
//
// Há dois DS em uso (2026-11-09): o @cit (GitLab, centralit/shadcn) nos sistemas novos e o
// boilerplate-cit (o primeiro, GitHub, centralit-boilerplate) nos antigos, que ainda não viraram a
// chave. Cada um tem o próprio documento, e a fonte é o repositório dele: o pacote traz os dois em
// assets/design-system/<ds>/, atualizados por scripts/sync-ds.mjs a cada versão.
//
// O DS sai do registry do components.json do projeto (raiz ou até dois níveis abaixo):
// "@cit" ou cithyper → @cit; "@centralit" ou centralit-boilerplate → boilerplate-cit. --ds=cit|boilerplate
// manda sobre a detecção. Sem registry conhecido, vale o boilerplate-cit (protótipo HTML e projetos
// antigos). Com os dois DS no mesmo repo (um monorepo de projetos), nada é instalado: rode com --ds
// dentro da pasta do projeto.
//
// SOBRESCREVE, ao contrário de antes: a cópia que nunca era atualizada é o que fez cada projeto ter
// uma versão diferente do mesmo documento. A pasta passa a ser gerada, como .claude/skills/, e o
// ORIGEM.md diz de onde veio. Cópia antiga feita à mão (sem ORIGEM.md) e diferente vai para
// .anterior-<data>/ antes de ser trocada, e o instalador avisa.
const DS = {
  cit: { rotulo: "@cit", sinais: ["@cit", "cithyper"] },
  boilerplate: { rotulo: "boilerplate-cit", sinais: ["@centralit", "centralit-boilerplate"] },
}
const acharComponentsJson = (dir, nivel = 0) => {
  const achados = []
  let entradas = []
  try { entradas = readdirSync(dir, { withFileTypes: true }) } catch { return achados }
  for (const e of entradas) {
    if (e.isFile() && e.name === "components.json") achados.push(join(dir, e.name))
    else if (e.isDirectory() && nivel < 2 && !["node_modules", "dist"].includes(e.name) && !e.name.startsWith("."))
      achados.push(...acharComponentsJson(join(dir, e.name), nivel + 1))
  }
  return achados
}
const dsDoComponentsJson = (arquivo) => {
  let regs = {}
  try { regs = JSON.parse(readFileSync(arquivo, "utf8")).registries || {} } catch { return null }
  const texto = Object.entries(regs).map(([k, v]) => `${k} ${typeof v === "string" ? v : v?.url || ""}`).join(" ")
  return Object.keys(DS).find((ds) => DS[ds].sinais.some((s) => texto.includes(s))) || null
}
const argDS = process.argv.find((a) => a.startsWith("--ds="))?.slice(5)
if (argDS && !DS[argDS]) fail(`--ds=${argDS} não existe. Use --ds=cit ou --ds=boilerplate`)
let dsEscolhido = argDS, motivoDS = "pedido com --ds"
if (!dsEscolhido) {
  const porArquivo = acharComponentsJson(TARGET).map((a) => [relative(TARGET, a), dsDoComponentsJson(a)]).filter(([, ds]) => ds)
  const distintos = [...new Set(porArquivo.map(([, ds]) => ds))]
  if (distintos.length === 1) { dsEscolhido = distintos[0]; motivoDS = `pelo ${porArquivo[0][0]}` }
  else if (distintos.length === 0) { dsEscolhido = "boilerplate"; motivoDS = "sem components.json com registry conhecido" }
  else {
    warn("Este repositório usa os dois design systems; os docs de design system NÃO foram instalados:")
    for (const [a, ds] of porArquivo) warn(`  ${a} → ${DS[ds].rotulo}`)
    warn("  rode o instalador dentro da pasta do projeto, ou com --ds=cit | --ds=boilerplate")
  }
}
if (dsEscolhido) {
  const dsSrc = join(PKG, "assets", "design-system", dsEscolhido)
  const dsDest = join(TARGET, "docs", "design-system")
  const origem = JSON.parse(readFileSync(join(dsSrc, "ORIGEM.json"), "utf8"))
  mkdirSync(dsDest, { recursive: true })
  const origemMd = join(dsDest, "ORIGEM.md")
  const gerada = existsSync(origemMd)
  const anterior = gerada ? (readFileSync(origemMd, "utf8").match(/^\*\*Design system:\*\* (.+)$/m)?.[1] ?? null) : null
  const docs = readdirSync(dsSrc).filter((f) => f.endsWith(".md"))
  const backup = join(dsDest, `.anterior-${new Date().toISOString().slice(0, 10)}`)
  let nGuardados = 0
  for (const f of docs) {
    const dest = join(dsDest, f)
    if (!gerada && existsSync(dest) && readFileSync(dest, "utf8") !== readFileSync(join(dsSrc, f), "utf8")) {
      mkdirSync(backup, { recursive: true })
      copyFileSync(dest, join(backup, f))
      nGuardados++
    }
    copyFileSync(join(dsSrc, f), dest)
  }
  const ref = origem.commit
    ? `${origem.repo.replace(/\.git$/, "")}, commit \`${origem.commit.slice(0, 7)}\` (${origem.data?.slice(0, 10)})`
    : `${origem.repo.replace(/\.git$/, "")}, versão ${origem.versao}`
  writeFileSync(origemMd,
    `# Origem destes documentos\n\n` +
    `**Design system:** ${origem.rotulo}\n\n` +
    `Gerados pelo instalador das skills PX (v${VERSION}) a partir de ${ref}, pasta \`${origem.caminho}/\`.\n\n` +
    `**Não edite aqui.** A fonte é o repositório do design system: mude lá, e a próxima versão das skills\n` +
    `traz a mudança. Uma edição aqui some na próxima instalação.\n` +
    (origem.provisorio ? `\n⚠️ ${origem.provisorio}\n` : ""))
  ok(`docs de design system ${origem.rotulo} em docs/design-system/ (${motivoDS})`)
  if (anterior && anterior !== origem.rotulo) info(`  o projeto trocou de ${anterior} para ${origem.rotulo}`)
  if (nGuardados) warn(`  ${nGuardados} doc(s) antigo(s) e diferente(s) guardado(s) em ${relative(TARGET, backup)}/ antes da troca`)
  if (origem.provisorio) warn("  cópia provisória: a fonte ainda não publicou esta versão (ver docs/design-system/ORIGEM.md)")
}

// 2b. Hook de sessão → <target>/.claude/hooks/ + SessionStart no settings.json
// Avisa o UX quando as skills estão atrás, o sandbox não tem procedência ou falta
// o CENTRALIT_TOKEN. O hook é o que faz o aviso chegar sem ninguém precisar lembrar
// de rodar o instalador.
const hooksDest = join(TARGET, ".claude", "hooks")
mkdirSync(hooksDest, { recursive: true })
// copyFileSync sobrescreve o hook existente; o cpSync antigo lançava exceção não
// tratada na segunda instalação (cpSyncOverrideFile) e abortava o instalador aqui.
copyFileSync(join(PKG, "assets", "hooks", "check-versao.mjs"), join(hooksDest, "check-versao.mjs"))

const settingsPath = join(TARGET, ".claude", "settings.json")
const CMD = "node .claude/hooks/check-versao.mjs"
let settings = {}
let settingsOk = true
if (existsSync(settingsPath)) {
  try {
    settings = JSON.parse(readFileSync(settingsPath, "utf8"))
  } catch {
    // settings.json malformado: NÃO sobrescrever. Um settings quebrado desliga todas
    // as configurações daquele arquivo, e clobberar apagaria trabalho do time.
    settingsOk = false
    warn(".claude/settings.json existe mas não é JSON válido — hook não instalado")
    warn("  corrija o arquivo e rode o instalador de novo")
  }
}
if (settingsOk) {
  settings.hooks ||= {}
  settings.hooks.SessionStart ||= []
  const jaTem = settings.hooks.SessionStart.some((g) =>
    (g?.hooks || []).some((h) => h?.command === CMD),
  )
  if (!jaTem) {
    settings.hooks.SessionStart.push({
      hooks: [{ type: "command", command: CMD, timeout: 10 }],
    })
    writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + "\n")
    ok("hook de sessão em .claude/hooks/ (avisa quando as skills ficam atrás)")
  } else {
    ok("hook de sessão atualizado em .claude/hooks/")
  }
}

// 3. Protocolo → <target>/docs/px-protocol.md
const protoDest = join(TARGET, "docs", "px-protocol.md")
if (!existsSync(protoDest)) {
  mkdirSync(dirname(protoDest), { recursive: true })
  copyFileSync(join(PKG, "assets", "px-protocol.md"), protoDest)
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
log(`${c.d}  /px-request · /px-change · /px-story · /px-tour · /px-handoff · /px-preview · /px-sync${c.x}`)
log(`${c.d}  /ux-flows · /ux-persona${c.x} ${c.y}(execução — rodam sobre o produto ao vivo)${c.x}`)
log(`\n${c.y}Pré-requisito de UI:${c.x} a biblioteca de componentes (src/components/ui + tokens) precisa`)
log(`${c.d}  estar no repo — ela vem no bundle do design system, não neste pacote de skills.${c.x}`)
// 5. Resumo do que veio — só as versões que este repo ainda não tinha.
// Ao publicar uma versão nova: acrescente a chave aqui, 1 a 3 linhas de ~74 colunas.
// Isto é o resumo de leitura rápida; a íntegra vive no CHANGELOG.md.
const HIGHLIGHTS = {
  "1.24.0": [
    "Docs de design system do DS que o projeto usa: @cit ou boilerplate-cit,",
    "  pelo registry do components.json (ou --ds=cit|boilerplate). A pasta",
    "  docs/design-system/ passa a ser gerada e atualizada a cada instalacao,",
    "  com ORIGEM.md; copia antiga a mao vai para .anterior-<data>/.",
    "px-tour SUSPENSA: o componente Onboarding Guiado se perdeu (a 0.4.0 do",
    "  boilerplate nunca foi publicada). A spec esta no boilerplate, em",
    "  docs/propostas/onboarding-guiado.md.",
  ],
  "1.23.0": [
    "px-handoff oferece dois modelos: Tradicional (branch orfa) e Novo (tronco",
    "  ux/ui). Antes de recomendar, analisa o repo do dev: branches ux/*, padrao",
    "  da pasta e sinais de custo. Migrar custoso: Tradicional. Senao: Novo, com",
    "  o Diogo (lider de UX) acompanhando a criacao do tronco e a 1a entrega.",
  ],
  "1.22.1": [
    "A UI deixa de ser 'copiar sem editar': o dev copia e edita so a",
    "  integracao (eventos, tipos, dados, imports, carregamento e erro do back)",
    "  e corrige o que ja existe, avisando o PX. Criar ou mudar o que o usuario",
    "  ve passa pelo PX. Entregas seguintes por diff entre tags com --3way.",
  ],
  "1.22.0": [
    "px-handoff deixa a branch orfa: a entrega vai pelo tronco ux/ui. O tronco",
    "  nasce uma vez; cada entrega e uma branch ux/entrega-<label> tirada do",
    "  ultimo merge, com MR de volta e tag anotada. Pasta handoff-ux/ estavel,",
    "  CHANGELOG.md acumulativo, commits por assunto e historias versionadas.",
    "  O diff entre entregas passa a mostrar so o que mudou.",
  ],
  "1.21.0": [
    "px-request vira a porta unica de mudanca de UI: o Passo 0 classifica o",
    "  pedido e manda ajuste em tela que ja existe para a px-change, sem a",
    "  entrevista de 12 blocos. Se o ajuste cresce, a px-request herda as",
    "  respostas da px-change e recomeca no B2, sem perguntar de novo.",
    "px-proto ganha o Passo 7a: validacao de interacao estado por estado",
    "  (cliques, teclado, Escape, clique fora, viewport, overflow, console,",
    "  copy x comportamento). A aprovacao passa a depender dele.",
  ],
  "1.18.0": [
    "Nova skill px-tour: onboarding guiado por fluxo logico, sobre o",
    "  componente Onboarding Guiado do DS. Um flow, um tour; o global junta",
    "  todos. Passo por evidencia, permissao filtrada em runtime.",
  ],
  "1.17.1": [
    "Instalador: em pasta com acento no caminho (Windows, Node 24) as skills iam",
    "  parar numa pasta irma com nome corrompido e o terminal dizia 'instaladas'.",
    "  Copia reescrita, cada skill conferida no destino, e reinstalar nao aborta.",
  ],
  "1.17.0": [
    "O pacote do dev passa a levar personas/: quem julgou a tela e com que",
    "  regua. Criterio de usabilidade sem a persona vira preferencia de quem",
    "  escreveu, e cai na primeira refatoracao que simplifica a tela.",
    "Junto vai flows/: a jornada que a persona percorreu e que o Playwright",
    "  do dev automatiza. Persona e a regua, flow e a travessia; vao em par.",
    "Cada persona viaja com a customizacao de contexto declarada. Relatorio",
    "  do walkthrough fica interno. Nenhuma rodou? A ausencia e declarada.",
    "Persona cetica ganha o eixo privacidade: por que pedem este dado, quem",
    "  enxerga o que eu preenchi, da pra seguir sem entregar.",
  ],
  "1.16.0": [
    "Divergencia do design system agora e declarada ou e defeito: bloco novo no",
    "  px-request (11c) e no px-proto (4b). O gate ja existia so para o legado.",
    "px-proto le o COMPONENTE, nao so a doc: o inventario lista props e decisoes",
    "  do .tsx, e 17 dos 53 componentes nao tem entrada no ds-components_v4.md.",
    "Ambiguidade deixa de ser auto-declarada — a varredura conta os candidatos.",
    "  Auditoria numerada, e o request da veredito item a item. Nada some calado.",
  ],
  "1.15.0": [
    "Hook de sessao: ao abrir o Claude Code, o repo avisa se as skills estao",
    "  atras, se o sandbox perdeu a procedencia ou se falta CENTRALIT_TOKEN.",
    "Silencio quando esta tudo certo — aviso todo dia vira ruido e e ignorado.",
    "  O instalador planta o hook sozinho; nao ha nada para configurar.",
  ],
  "1.14.0": [
    "Componente instala SEMPRE via registry: npx shadcn add @centralit/<nome>.",
    "  A forma sem prefixo baixa o shadcn publico e nao da erro — virou proibida.",
    "Portao de procedencia no px-proto: base auditavel, idade da base e token do",
    "  registry conferidos antes de codar. Falha fechado, nao segue 'por enquanto'.",
    "px-setup nao corta mais o git do sandbox, e o px-handoff exige procedencia.md",
    "  no pacote: commit da base, registry e versao das skills. Sem ele, nao sai.",
  ],
  "1.13.0": [
    "Teto de tamanho: a história fecha com no máximo 13 CA e 13 cenários BDD,",
    "  ou justifica por escrito. Pega a tela funda que o teste de rota não pegava.",
    "Aba conta como item: tela com 3+ abas independentes entra no backlog já",
    "  quebrada, uma história por aba. Tamanho G virou estado proibido.",
    "ID de regra de negócio unificado: RN-<SIGLA>-<DOMINIO>-<NN>, global por",
    "  iniciativa, num único regras-negocio.md. RN por tela/fluxo é proibida.",
  ],
  "1.12.0": [
    "Uma história = uma TELA. Fluxo e público são agrupamento, não recorte.",
    "ID da história por tela: <PROD>-<FLUXO>-<TELA>, nunca por fluxo.",
  ],
  "1.11.1": [
    "O portão de ordem dos critérios de aceite voltou a rodar (estava quebrado).",
  ],
  "1.11.0": [
    "mapa-de-telas.md carrega ordem de implementação e ID estável por tela.",
  ],
}

const cmp = (a, b) => {
  const pa = a.split(".").map(Number), pb = b.split(".").map(Number)
  for (let i = 0; i < 3; i++) if ((pa[i] || 0) !== (pb[i] || 0)) return (pa[i] || 0) - (pb[i] || 0)
  return 0
}
const rule = (title) => title + " " + "─".repeat(Math.max(4, 64 - title.length))

let titulo, versoes
if (!prev) {
  titulo = `── px-skills ${VERSION}`
  versoes = HIGHLIGHTS[VERSION] ? [VERSION] : []      // 1ª instalação: só a atual
} else if (cmp(prev, VERSION) === 0) {
  titulo = `── px-skills ${VERSION} — já era a versão deste repo`
  versoes = []
} else if (cmp(prev, VERSION) > 0) {
  titulo = `── px-skills ${prev} → ${VERSION} (downgrade)`
  versoes = []
} else {
  titulo = `── px-skills ${prev} → ${VERSION}`
  versoes = Object.keys(HIGHLIGHTS)
    .filter((v) => cmp(v, prev) > 0 && cmp(v, VERSION) <= 0)
    .sort((a, b) => cmp(b, a))
}

log(`\n${c.b}${rule(titulo)}${c.x}`)
for (const v of versoes) {
  log(`${c.g}${v}${c.x}`)
  for (const linha of HIGHLIGHTS[v]) log(`${c.d}  ${linha}${c.x}`)
}
if (!versoes.length && prev && cmp(prev, VERSION) < 0) {
  log(`${c.d}  Sem resumo registrado para esta versão — ver CHANGELOG.md.${c.x}`)
}

if (versoes.length) log(`\n${c.d}Íntegra: CHANGELOG.md${c.x}`)
log(`${c.b}────────────────────────────────────────────────────────────────${c.x}\n`)
