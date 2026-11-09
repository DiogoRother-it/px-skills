#!/usr/bin/env node
// Traz os docs de design system das FONTES para assets/design-system/<ds>/.
//
// Direção (decidida em 2026-11-09): cada repositório de DS é a fonte do próprio documento, e este
// pacote só distribui. Nunca edite assets/design-system/<ds>/*.md à mão: a mudança se perde no
// próximo sync. Mude na fonte e rode este script antes de publicar uma versão das skills.
//
// Uso (na raiz do px-skills, com acesso git aos dois repositórios):
//   node scripts/sync-ds.mjs                 traz os dois
//   node scripts/sync-ds.mjs --so=cit        traz só um (cit | boilerplate)
//   node scripts/sync-ds.mjs --verificar     só compara; sai com 1 se algum estiver atrás da fonte
//
// Não entra no pacote publicado (fica fora de "files" no package.json).

import { execFileSync } from "node:child_process"
import { copyFileSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs"
import { tmpdir } from "node:os"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"

const PKG = join(dirname(fileURLToPath(import.meta.url)), "..")
const ARQUIVOS = ["ds-foundations_v4.md", "ds-components_v4.md", "ds-patterns.md", "Engineering-directives_v4.md"]

export const FONTES = {
  cit: {
    rotulo: "@cit",
    repo: "https://gitlab.cithyper.click/centralit/shadcn.git",
    ref: "main",
    caminho: "docs/design-system",
  },
  boilerplate: {
    rotulo: "boilerplate-cit",
    repo: "https://github.com/DiogoRother-it/centralit-boilerplate.git",
    ref: "main",
    caminho: "docs/design-system",
    // A 0.4.0 trouxe o Onboarding Guiado, que a px-tour usa. Fonte abaixo disso apagaria a seção
    // que o pacote já distribui. Só passa com --forcar.
    versaoMinima: "0.4.0",
  },
}

const args = process.argv.slice(2)
const so = args.find((a) => a.startsWith("--so="))?.slice(5)
const verificar = args.includes("--verificar")
const forcar = args.includes("--forcar")
const git = (cwd, ...a) => execFileSync("git", a, { cwd, encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] }).trim()
const cmp = (a, b) => {
  const pa = String(a).split(".").map(Number), pb = String(b).split(".").map(Number)
  for (let i = 0; i < 3; i++) if ((pa[i] || 0) !== (pb[i] || 0)) return (pa[i] || 0) - (pb[i] || 0)
  return 0
}

if (so && !FONTES[so]) {
  console.error(`--so=${so} não existe. Use: ${Object.keys(FONTES).join(" | ")}`)
  process.exit(2)
}

let atrasados = 0
for (const [ds, f] of Object.entries(FONTES)) {
  if (so && so !== ds) continue
  const tmp = mkdtempSync(join(tmpdir(), `sync-ds-${ds}-`))
  try {
    git(tmp, "clone", "-q", "--depth", "1", "--filter=blob:none", "--sparse", "--branch", f.ref, f.repo, "fonte")
    const dir = join(tmp, "fonte")
    git(dir, "sparse-checkout", "set", "--no-cone", `/${f.caminho}/`, "/package.json")
    const commit = git(dir, "rev-parse", "HEAD")
    const data = git(dir, "log", "-1", "--format=%cI")
    const pkgPath = join(dir, "package.json")
    const versao = existsSync(pkgPath) ? JSON.parse(readFileSync(pkgPath, "utf8")).version ?? null : null

    if (f.versaoMinima && versao && cmp(versao, f.versaoMinima) < 0 && !forcar) {
      console.error(`✖ ${f.rotulo}: a fonte está na ${versao}, abaixo da ${f.versaoMinima}. Nada foi trocado.`)
      console.error(`  Publique a ${f.versaoMinima} na fonte, ou rode com --forcar se for de propósito.`)
      atrasados++
      continue
    }

    const destino = join(PKG, "assets", "design-system", ds)
    const diferentes = ARQUIVOS.filter((a) => {
      const novo = join(dir, f.caminho, a), atual = join(destino, a)
      if (!existsSync(novo)) throw new Error(`${f.rotulo}: falta ${f.caminho}/${a} na fonte`)
      return !existsSync(atual) || readFileSync(novo, "utf8") !== readFileSync(atual, "utf8")
    })

    if (verificar) {
      if (diferentes.length) {
        console.log(`! ${f.rotulo}: atrás da fonte (${commit.slice(0, 7)}) em ${diferentes.join(", ")}`)
        atrasados++
      } else console.log(`✓ ${f.rotulo}: igual à fonte (${commit.slice(0, 7)})`)
      continue
    }

    mkdirSync(destino, { recursive: true })
    for (const a of ARQUIVOS) copyFileSync(join(dir, f.caminho, a), join(destino, a))
    const origem = { ds, rotulo: f.rotulo, repo: f.repo, ref: f.ref, caminho: f.caminho, commit, data, versao }
    writeFileSync(join(destino, "ORIGEM.json"), JSON.stringify(origem, null, 2) + "\n")
    console.log(`✓ ${f.rotulo}: ${commit.slice(0, 7)}${versao ? ` (v${versao})` : ""}, ${diferentes.length ? `mudou ${diferentes.join(", ")}` : "sem mudança"}`)
  } finally {
    rmSync(tmp, { recursive: true, force: true })
  }
}
if (atrasados) process.exitCode = 1
