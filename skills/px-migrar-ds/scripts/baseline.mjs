#!/usr/bin/env node
// Baseline visual da migração: captura telas e estados antes de mexer e compara depois.
//
// Uso (rodar de dentro do projeto do produto, que precisa ter o pacote `playwright`):
//   node baseline.mjs capturar rotas.json <pasta> [--base http://localhost:5173]
//   node baseline.mjs comparar <pasta-antes> <pasta-depois>
//
// rotas.json:
// [
//   {"nome": "lista-vazia", "caminho": "/alunos?filtro=nenhum"},
//   {"nome": "cadastro-erro", "caminho": "/alunos/novo",
//    "antes": [{"clicar": "button[type=submit]"}, {"esperar": 300}]},
//   {"nome": "menu-hover", "caminho": "/", "antes": [{"passar": "nav a:first-child"}]},
//   {"nome": "busca-foco", "caminho": "/", "antes": [{"focar": "input[type=search]"}]},
//   {"nome": "busca-preenchida", "caminho": "/", "antes": [{"preencher": ["input[type=search]", "Maria"]}]}
// ]
// Login: crie uma rota "login" com "antes" preenchendo os campos com a credencial de teste do seed
// do projeto; a sessão vale para as rotas seguintes.
//
// Saída: <pasta>/<nome>@desktop.png e <nome>@celular.png (página inteira) + <pasta>/relatorio.json
// com os erros de console e as requisições que falharam em cada tela.
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const VISTAS = { desktop: { width: 1440, height: 900 }, celular: { width: 390, height: 844 } };
const [cmd, ...args] = process.argv.slice(2);

async function capturar(arqRotas, pasta, base) {
  let chromium;
  try {
    ({ chromium } = await import("playwright"));
  } catch {
    console.error("Falta o pacote playwright neste projeto. Instale como dependência de desenvolvimento e rode de novo.");
    process.exit(2);
  }
  const rotas = JSON.parse(readFileSync(arqRotas, "utf8"));
  mkdirSync(pasta, { recursive: true });
  const relatorio = {};
  const browser = await chromium.launch();
  for (const [vista, viewport] of Object.entries(VISTAS)) {
    const ctx = await browser.newContext({ viewport, reducedMotion: "reduce" });
    const page = await ctx.newPage();
    for (const r of rotas) {
      const erros = [];
      const onConsole = (m) => m.type() === "error" && erros.push(m.text());
      const onFalha = (q) => erros.push(`falhou: ${q.url()}`);
      page.on("console", onConsole);
      page.on("requestfailed", onFalha);
      await page.goto(new URL(r.caminho, base).href, { waitUntil: "networkidle" });
      for (const a of r.antes || []) {
        if (a.clicar) await page.click(a.clicar);
        if (a.passar) await page.hover(a.passar);
        if (a.focar) await page.focus(a.focar);
        if (a.preencher) await page.fill(a.preencher[0], a.preencher[1]);
        if (a.esperar) await page.waitForTimeout(a.esperar);
      }
      await page.waitForTimeout(r.esperar ?? 200);
      await page.screenshot({ path: join(pasta, `${r.nome}@${vista}.png`), fullPage: true, animations: "disabled" });
      page.off("console", onConsole);
      page.off("requestfailed", onFalha);
      relatorio[`${r.nome}@${vista}`] = erros;
      console.log(`${r.nome}@${vista}${erros.length ? `  (${erros.length} erro(s))` : ""}`);
    }
    await ctx.close();
  }
  await browser.close();
  writeFileSync(join(pasta, "relatorio.json"), JSON.stringify(relatorio, null, 2));
  console.log(`baseline em ${pasta}`);
}

function hash(p) {
  return createHash("sha1").update(readFileSync(p)).digest("hex");
}

function comparar(antes, depois) {
  const pngs = (d) => new Set(readdirSync(d).filter((f) => f.endsWith(".png")));
  const a = pngs(antes), d = pngs(depois);
  const iguais = [], mudaram = [], sumiram = [], novas = [];
  for (const f of a) {
    if (!d.has(f)) sumiram.push(f);
    else (hash(join(antes, f)) === hash(join(depois, f)) ? iguais : mudaram).push(f);
  }
  for (const f of d) if (!a.has(f)) novas.push(f);
  const erros = (p) => (existsSync(join(p, "relatorio.json")) ? JSON.parse(readFileSync(join(p, "relatorio.json"), "utf8")) : {});
  const ea = erros(antes), ed = erros(depois);
  const errosNovos = Object.entries(ed).filter(([k, v]) => v.length > (ea[k] || []).length).map(([k]) => k);
  console.log(`iguais: ${iguais.length} · mudaram: ${mudaram.length} · sumiram: ${sumiram.length} · novas: ${novas.length}`);
  if (mudaram.length) console.log("\nMudaram (abra o par e confira se a mudança era esperada):\n  " + mudaram.join("\n  "));
  if (sumiram.length) console.log("\nSumiram (a tela ou o estado deixou de existir?):\n  " + sumiram.join("\n  "));
  if (errosNovos.length) console.log("\nErro de console novo em:\n  " + errosNovos.join("\n  "));
  process.exit(sumiram.length || errosNovos.length ? 1 : 0);
}

if (cmd === "capturar" && args.length >= 2) {
  const i = args.indexOf("--base");
  await capturar(args[0], args[1], i >= 0 ? args[i + 1] : "http://localhost:5173");
} else if (cmd === "comparar" && args.length === 2) {
  comparar(args[0], args[1]);
} else {
  console.log("node baseline.mjs capturar rotas.json <pasta> [--base URL]\nnode baseline.mjs comparar <antes> <depois>");
  process.exit(2);
}
