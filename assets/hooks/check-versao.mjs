#!/usr/bin/env node
// Hook SessionStart — avisa o UX quando o terreno saiu do padrão.
//
// Plantado pelo install.mjs em <projeto>/.claude/hooks/ e disparado pelo
// SessionStart declarado em <projeto>/.claude/settings.json.
//
// Três checagens, todas baratas:
//   1. Skills desatualizadas   → rede (px-skills é público), cache de 6h
//   2. Sandbox sem procedência → local, instantâneo
//   3. CENTRALIT_TOKEN ausente → local, instantâneo
//
// Regras de ouro deste arquivo:
//   - SILÊNCIO QUANDO ESTÁ TUDO CERTO. Aviso que aparece toda sessão vira ruído
//     e as pessoas aprendem a ignorar — que é exatamente a falha que ele existe
//     para evitar.
//   - NUNCA QUEBRA A SESSÃO. Qualquer erro termina sem output e sem status ruim.
//   - NUNCA CHAMA process.exit(). Com o fetch ainda em voo isso derruba o libuv
//     no Windows (assertion em async.c). O script termina sozinho.
//   - NUNCA FAZ git fetch. Rede em SessionStart trava a abertura e pode pedir
//     credencial. A medição de idade da base é do px-proto (Passo 3A), que roda
//     no momento em que ela importa.

import { existsSync, readFileSync, writeFileSync } from "node:fs"
import { join } from "node:path"
import { execFileSync } from "node:child_process"

const RAIZ = process.cwd()
const STAMP = join(RAIZ, ".claude", "skills", ".px-skills-version")
const CACHE = join(RAIZ, ".claude", "skills", ".px-skills-check")
const REMOTO =
  "https://raw.githubusercontent.com/DiogoRother-it/px-skills/main/package.json"
const CACHE_MS = 6 * 60 * 60 * 1000 // 6h — a versão não muda de hora em hora
const TIMEOUT_MS = 4000

const cmp = (a, b) => {
  const pa = String(a).split(".").map(Number)
  const pb = String(b).split(".").map(Number)
  for (let i = 0; i < 3; i++) if ((pa[i] || 0) !== (pb[i] || 0)) return (pa[i] || 0) - (pb[i] || 0)
  return 0
}

async function versaoRemota() {
  // Cache primeiro: SessionStart roda em toda sessão, rede não.
  try {
    const c = JSON.parse(readFileSync(CACHE, "utf8"))
    if (Date.now() - c.ts < CACHE_MS && c.latest) return c.latest
  } catch {}

  const ac = new AbortController()
  const t = setTimeout(() => ac.abort(), TIMEOUT_MS)
  try {
    const r = await fetch(REMOTO, { signal: ac.signal })
    if (!r.ok) return null
    const { version } = await r.json()
    if (!version) return null
    try {
      writeFileSync(CACHE, JSON.stringify({ ts: Date.now(), latest: version }) + "\n")
    } catch {}
    return version
  } catch {
    return null // offline, VPN, GitHub fora do ar — silêncio, não é problema do UX
  } finally {
    clearTimeout(t) // sem isso o timer segura o event loop
  }
}

// É um sandbox do PX? A marca é o registry @centralit no components.json.
function ehSandboxPx() {
  try {
    const cj = join(RAIZ, "components.json")
    if (!existsSync(cj)) return false
    return JSON.parse(readFileSync(cj, "utf8"))?.registries?.["@centralit"] != null
  } catch {
    return false
  }
}

function temProcedencia() {
  try {
    const out = execFileSync("git", ["remote"], {
      cwd: RAIZ,
      encoding: "utf8",
      timeout: 2000,
      stdio: ["ignore", "pipe", "ignore"],
    })
    return out.split(/\r?\n/).includes("boilerplate-upstream")
  } catch {
    return false
  }
}

async function main() {
  const avisos = []
  const contexto = []

  // 1. Skills desatualizadas
  if (existsSync(STAMP)) {
    const local = readFileSync(STAMP, "utf8").trim()
    const remota = await versaoRemota()
    if (remota && cmp(local, remota) < 0) {
      avisos.push(
        `Skills PX desatualizadas: ${local} instalada, ${remota} disponível.`,
        `Atualizar: npx github:DiogoRother-it/px-skills`,
      )
      contexto.push(
        `As skills PX deste repo estão na ${local}; a atual é a ${remota}. ` +
          `Antes de rodar qualquer skill da cadeia PX, ofereça atualizar com ` +
          `\`npx github:DiogoRother-it/px-skills\` e avise que o portão de procedência ` +
          `e as regras de recorte podem ter mudado. Não bloqueie o trabalho por isso.`,
      )
    }
  }

  // 2 e 3 — só fazem sentido num sandbox do PX
  if (ehSandboxPx()) {
    if (!temProcedencia()) {
      avisos.push(
        `Sandbox sem procedência: o remote 'boilerplate-upstream' não existe.`,
        `A base não é auditável — não dá para medir o quanto ela divergiu do boilerplate.`,
      )
      contexto.push(
        `Este sandbox não tem o remote \`boilerplate-upstream\`, então a procedência da base ` +
          `é indeterminável (provavelmente montado antes da 1.14.0, quando o px-setup fazia ` +
          `\`rm -rf .git\`). Se o trabalho for virar handoff, o \`procedencia.md\` terá que ` +
          `sair como NÃO AUDITÁVEL. Ofereça remontar o sandbox pelo px-setup.`,
      )
    }
    if (!process.env.CENTRALIT_TOKEN) {
      avisos.push(
        `CENTRALIT_TOKEN ausente: o registry @centralit não responde sem ele.`,
        `Componente instalado agora cai no shadcn público, que funciona e entrega o default errado.`,
      )
      contexto.push(
        `\`CENTRALIT_TOKEN\` não está no ambiente. Todo \`npx shadcn add @centralit/...\` vai ` +
          `falhar por autenticação, e a forma sem prefixo cairia no shadcn público em silêncio. ` +
          `⛔ Não instale componente por esse caminho: resolva o token primeiro (px-setup Passo 2b).`,
      )
    }
  }

  // Silêncio quando está tudo certo.
  if (!avisos.length) return

  process.stdout.write(
    JSON.stringify({
      systemMessage: "⚠️  px-skills\n" + avisos.map((l) => "   " + l).join("\n"),
      hookSpecificOutput: {
        hookEventName: "SessionStart",
        additionalContext: contexto.join("\n\n"),
      },
    }),
  )
}

// Blindagem final: o hook nunca pode derrubar a sessão nem sinalizar erro.
try {
  await main()
} catch {}
