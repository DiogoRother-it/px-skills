#!/usr/bin/env python3
"""Gera a página do styleguide a partir do produtos.json.

Uso:
  python3 pagina.py produtos.json [saida.html]     # padrão: <pasta do json>/styleguide.html

Seções: marcas, regras da linguagem, cores com a tabela de contraste e as reservadas, header
claro e escuro a 24 px, tamanhos 16/24/32/64, um accordion por módulo (com os campos opcionais
que a família usa) e o que falta decidir. A página segue o contrato de Artifact (title curto,
tokens de cor no :root com modo escuro, fundo explícito no body, sem rolagem horizontal) e pode
ser publicada como está.
"""
import html
import json
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contraste import conferir  # noqa: E402
from formas import configurar, pecas_do_logo, pecas_do_modulo, svg  # noqa: E402
from gerar import banner, logo  # noqa: E402

E = html.escape
ROTULOS = {
    "acento": "Acento e onde aparece",
    "textura": "Textura",
    "frase_home": "Frase da home",
    "marca_animada": "Marca animada",
    "movimento": "Assinatura de movimento",
}


def rico(t):
    """Escapa e aceita **negrito**."""
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", E(t or ""))


def falta(txt="Não definido"):
    return f'<span class="falta">{txt}</span>'


def _uri_svg(s):
    from urllib.parse import quote
    return "data:image/svg+xml," + quote(s)


def campo(chave, valor, m, pc, acento):
    if chave == "acento":
        onde = "".join(f"<li>{rico(o)}</li>" for o in valor.get("onde", []))
        return (f'<span class="sw" style="--cor:{E(valor["cor"])}"></span><span class="mono">{E(valor["cor"])}</span>'
                + (f'<ul class="lista">{onde}</ul>' if onde else ""))
    if chave == "textura":
        tile = valor.get("svg")
        amostra = f'<div class="tex" style="background-image:url(\'{_uri_svg(tile)}\')"></div>' if tile else ""
        return amostra + f'<span>{rico(valor.get("nome", ""))}{" · " if valor.get("descricao") else ""}{rico(valor.get("descricao", ""))}</span>'
    if chave == "frase_home":
        fonte = f'<span>{rico(valor["fonte"])}</span>' if valor.get("fonte") else ""
        return f'<p class="frase">“{E(valor.get("texto", ""))}”</p>{fonte}'
    if chave == "marca_animada":
        tipo = valor.get("tipo", "respirar")
        return (f'<span class="anim anim-{E(tipo)}">{svg(pc, "#FFFFFF", 56, acento=acento, anim=True)}</span>'
                f'<span>{rico(valor.get("descricao", ""))} <span class="mono">({E(tipo)})</span></span>')
    if chave == "movimento":
        dur, curva = valor.get("duracao", "240ms"), valor.get("curva", "ease-out")
        return (f'<span class="mov" style="--dur:{E(dur)};--curva:{E(curva)};--cor:{E(m["cor"])}"><i></i></span>'
                f'<span>{rico(valor.get("descricao", ""))} <span class="mono">{E(dur)} · {E(curva)}</span></span>')
    return f"<span>{rico(str(valor))}</span>"


def secao_logo(dados, acento):
    fam = dados["familia"]
    lg = fam.get("logo")
    if not lg:
        return ""
    cor, txt = lg.get("cor", "#0E1420"), lg.get("cor_texto", "#0E1420")
    esc = fam.get("cor_escuro", "#FFFFFF")
    arr = lg.get("arranjos", ["simbolo", "horizontal", "vertical"])
    pecas = pecas_do_logo(fam)
    nomes = {"simbolo": "Símbolo", "horizontal": "Horizontal", "vertical": "Vertical"}
    figs = "".join(
        f'<figure><div class="lg-par"><span class="lg-claro">{logo(dados, a, cor, txt, acento, lg.get("cor2"))}</span>'
        f'<span class="lg-escuro">{logo(dados, a, esc, esc, acento)}</span></div><figcaption>{nomes.get(a, a)}</figcaption></figure>'
        for a in arr if a != "simbolo" or pecas)
    prot = ""
    if pecas:
        k = lg.get("protecao", 0.25)
        prot = (f'<div class="lg-prot" style="--p:{k * 96:g}px"><span>{svg(pecas, "var(--fg)", 96, acento=acento)}</span></div>'
                f'<p>Área de proteção: {k * 100:.0f}% da altura do símbolo em volta do logo, sem texto nem outro elemento.</p>')
    mini = lg.get("minimo_px", 24)
    hor = logo(dados, "horizontal", "var(--fg)", "var(--fg)").replace("<svg ", '<svg height="%d" ' % mini, 1)
    simb_min = svg(pecas, "var(--fg)", mini) if pecas else ""
    minimo = (f'<div class="lg-min">{simb_min}<span style="height:{mini}px;display:inline-flex">{hor}</span>'
              f'<span class="mono">{mini} px</span></div><p>Tamanho mínimo: {mini} px de altura. Abaixo disso, use só o símbolo, ou nada.</p>')
    proib = "".join(f"<li>{rico(x)}</li>" for x in lg.get("proibidos", []))
    br = lg.get("briefing") or {}
    brief = "".join(f"<li><b>{E(r)}:</b> {rico(', '.join(br[k]) if isinstance(br.get(k), list) else str(br.get(k)))}</li>"
                    for k, r in (("transmitir", "Transmite"), ("evitar", "Evita"), ("referencias", "Referências")) if br.get(k))
    dec = {"manter": "Logo atual mantido", "refinar": "Logo atual refinado", "criar": "Logo novo"}.get(lg.get("decisao"), "")
    return f"""<section aria-labelledby="t-l"><h2 id="t-l">Logo</h2>
{f'<p>{E(dec)}{" · " + rico(lg["porque"]) if lg.get("porque") else ""}</p>' if dec or lg.get("porque") else ""}
<div class="lg-grade">{figs}</div>
<div class="duas-col"><div class="cartao">{prot}</div><div class="cartao">{minimo}</div></div>
{f'<div class="duas-col"><div class="cartao"><span class="rotulo">Briefing</span><ul class="lista">{brief}</ul></div>' if brief else '<div class="duas-col">'}
{f'<div class="cartao"><span class="rotulo">Não fazer</span><ul class="lista">{proib}</ul></div>' if proib else ""}</div></section>"""


def secoes_de_marca(dados, acento):
    """Tipografia, ícones, banners e animações: só aparecem se a família tiver o campo."""
    fam, out = dados["familia"], []
    tip = fam.get("tipografia")
    if tip:
        tm = tip.get("marca") or {}
        usos = "".join(f"<li>{rico(u)}</li>" for u in tm.get("uso", []))
        nomes = "".join(f"<span>{E(m['nome'])}</span>" for m in dados["modulos"])
        regras = "".join(f"<li>{rico(r)}</li>" for r in tip.get("regras", []))
        out.append(f"""<section aria-labelledby="t-t"><h2 id="t-t">Tipografia</h2><div class="duas-col">
<div class="cartao"><span class="rotulo">Marca · {E(tm.get("familia", "não definida"))}{" · " + E(tm["origem"]) if tm.get("origem") else ""}</span>
<div class="esp-marca">{E(fam.get("sistema", "").split(" (")[0] or "Aa")}</div><div class="esp-nomes">{nomes}</div>
{f'<ul class="lista">{usos}</ul>' if usos else ""}</div>
<div class="cartao"><span class="rotulo">Interface · {E(tip.get("interface", "Inter, pelo DS @cit"))}</span>
<div class="esp-ui"><span class="h1">Título de página</span><span class="h2">Título de seção</span><span class="b">Texto padrão do sistema, em 14 px, com a escala do DS.</span></div>
<p>A interface segue a escala tipográfica do DS. A fonte de marca entra só onde a lista ao lado diz.</p></div></div>
{f'<ul class="regras">{regras}</ul>' if regras else ""}</section>""")
    ic = fam.get("icones")
    if ic:
        claro = fam.get("cor_icone", "#0E1420")
        itens = "".join(
            f'<li><div class="duas"><span class="f-claro">{svg(i["pecas"], claro, 40, acento=acento)}</span>'
            f'<span class="f-escuro">{svg(i["pecas"], "#FFFFFF", 40, acento=acento)}</span></div>'
            f'<b>{E(i["nome"])}</b><p>{rico(i.get("uso", ""))}</p></li>' for i in ic.get("de_marca", []))
        out.append(f"""<section aria-labelledby="t-i"><h2 id="t-i">Ícones</h2>
<p><b>Na interface:</b> {rico(ic.get("interface", "Lucide em 16, 20 e 24 px, pelo DS @cit. Ícone de ação nunca é desenhado aqui."))}</p>
{f'<p><b>De marca:</b> desenhados com as regras da família, para estado vazio, abertura, banners e materiais. Nunca no lugar de um ícone de ação.</p><ul class="icones">{itens}</ul>' if itens else ""}</section>""")
    if fam.get("banners"):
        figs = "".join(
            f'<figure>{banner(dados, b)[0]}<figcaption><span class="mono">{E(b["id"])}</span> · '
            f'{"×".join(str(x) for x in b.get("formato", [1200, 400]))} px{" · " + rico(b["uso"]) if b.get("uso") else ""}</figcaption></figure>'
            for b in fam["banners"])
        out.append(f'<section aria-labelledby="t-b"><h2 id="t-b">Banners</h2><div class="banners">{figs}</div></section>')
    mv = fam.get("movimento")
    animadas = [m for m in dados["modulos"] if (m.get("campos") or {}).get("marca_animada")]
    if mv or animadas:
        linhas = "".join(f'<tr><td class="mono">--movimento-{E(k)}</td><td class="mono">{E(str(v))}</td></tr>'
                         for k, v in ((mv or {}).get("duracoes") or {}).items())
        if (mv or {}).get("curva"):
            linhas += f'<tr><td class="mono">--movimento-curva</td><td class="mono">{E(mv["curva"])}</td></tr>'
        gal = "".join(
            f'<figure><span class="anim anim-{E(m["campos"]["marca_animada"].get("tipo", "respirar"))}">'
            f'{svg(pecas_do_modulo(m), "#FFFFFF", 56, acento=acento, anim=True)}</span><figcaption>{E(m["nome"])}</figcaption></figure>'
            for m in animadas)
        regras = "".join(f"<li>{rico(r)}</li>" for r in (mv or {}).get("regras", []))
        out.append(f"""<section aria-labelledby="t-a"><h2 id="t-a">Animações</h2>
<p>Dentro das faixas do DS (100 a 500 ms), só com transform e opacity, e paradas quando o sistema pede menos movimento.</p>
{f'<div class="galeria">{gal}</div>' if gal else ""}
{f'<div class="tab"><table><thead><tr><th>Token</th><th>Valor</th></tr></thead><tbody>{linhas}</tbody></table></div>' if linhas else ""}
{f'<ul class="regras">{regras}</ul>' if regras else ""}</section>""")
    return "\n".join(out)


def pagina(dados):
    fam, mods = dados["familia"], dados["modulos"]
    acento = (fam.get("acento") or {}).get("cor")
    escuro = fam.get("fundo_escuro", "#0E1420")
    fundo = fam.get("fundo_app", "#EEF0F4")
    minimo = fam.get("minimo_contraste", 3.0)
    usados = fam.get("campos", [])
    linhas, problemas, avisos = conferir(dados, imprimir=False)
    n = len(mods)

    cards = "".join(
        f'<li class="prod" style="--cor:{E(m["cor"])}">{svg(pecas_do_modulo(m), "var(--l)", rotulo="Marca " + m["nome"], cls="marca", acento=acento)}'
        f'<div class="nome"><b>{E(m["nome"])}</b><span>{E(m.get("verbo", ""))}</span></div><p>{rico(m.get("porque", ""))}</p></li>'
        for m in mods)

    regras = "".join(f"<li>{rico(r)}</li>" for r in fam.get("regras", []))
    mae = fam.get("marca_mae") or {}
    mae_txt = f'<p>Regras tiradas de <b>{E(mae.get("nome", ""))}</b>{": " + rico(mae["descricao"]) if mae.get("descricao") else ""}.</p>' if mae else ""

    tab = "".join(
        f'<tr style="--cor:{E(l["cor"])}"><td><span class="sw"></span>{E(l["nome"])}</td><td class="mono">{E(l["cor"])}</td>'
        f'<td class="num">{l["branco"]:.1f}:1</td><td class="num">{l["fundo"]:.1f}:1</td>'
        f'<td>{"passa" if l["passa"] else "<b class=nao>não passa</b>"}</td></tr>' for l in linhas)
    reservadas = "".join(
        f'<li><span class="sw" style="--cor:{E(r["cor"])}"></span><span class="mono">{E(r["cor"])}</span> {rico(r.get("motivo", ""))}</li>'
        for r in fam.get("cores_reservadas", []))
    if acento:
        reservadas += f'<li><span class="sw" style="--cor:{E(acento)}"></span><span class="mono">{E(acento)}</span> acento da família ({rico(fam["acento"].get("papel", "peça do agente"))})</li>'
    alertas = "".join(f"<li>{E(p)}</li>" for p in problemas + avisos)

    def header(cor_fn):
        return "".join(
            f'<div class="hd-item">{svg(pecas_do_modulo(m), cor_fn(m), cls="hd-m", cor2=m.get("cor2") if cor_fn(m) == m["cor"] else None)}<b>{E(m["nome"])}</b>'
            + (f'<span>· {E(m["verbo"])}</span>' if m.get("verbo") else "") + "</div>" for m in mods)

    tams = "".join(
        f'<div class="tam"><div class="tl">{"".join(svg(pecas_do_modulo(m), "var(--l)", t) for m in mods)}</div><span>{t} px</span></div>'
        for t in (16, 24, 32, 64))

    acc = []
    for m in mods:
        pc = pecas_do_modulo(m)
        campos = m.get("campos") or {}
        dl = [("Marca e verbo",
               f'<div class="duas"><span class="f-claro">{svg(pc, m["cor"], 40, cor2=m.get("cor2"))}</span>'
               f'<span class="f-escuro">{svg(pc, "#FFFFFF", 40, acento=acento)}</span></div>'
               f'<span>{E(m["nome"])}{" · " + E(m["verbo"]) if m.get("verbo") else ""}</span>'),
              ("Cor", f'<span class="sw" style="--cor:{E(m["cor"])}"></span><span class="mono">{E(m["cor"])}</span>')]
        for k in usados:
            dl.append((ROTULOS.get(k, k), campo(k, campos[k], m, pc, acento) if campos.get(k) else falta()))
        for x in campos.get("extras", []):
            dl.append((x["rotulo"], f'<span>{rico(x["texto"])}</span>'))
        pend = m.get("pendencias") or []
        dl.append(("Para decidir", ('<ul class="lista">' + "".join(f"<li>{rico(p)}</li>" for p in pend) + "</ul>") if pend else "<span>Nada pendente.</span>"))
        corpo = "".join(f"<dt>{E(a)}</dt><dd>{b}</dd>" for a, b in dl)
        acc.append(f'<details class="sg" style="--cor:{E(m["cor"])}"><summary><span class="sg-cab">'
                   f'{svg(pc, "var(--l)", 28, acento=acento)}<b>{E(m["nome"])}</b><span class="sg-verbo">{E(m.get("verbo", ""))}</span></span>'
                   f'<span class="sw" title="Cor do módulo"></span></summary><dl class="sg-dl">{corpo}</dl></details>')

    secoes = secoes_de_marca(dados, acento)
    sec_logo = secao_logo(dados, acento)
    tm = (fam.get("tipografia") or {}).get("marca") or {}
    fonte_link = ""
    if str(tm.get("fonte_url", "")).startswith("https://fonts.googleapis.com/"):
        fonte_link = f'<link rel="stylesheet" href="{E(tm["fonte_url"])}">'
    fonte_marca = E(tm.get("familia", "Inter"))
    comum = "".join(f"<li>{rico(c)}</li>" for c in fam.get("comum_aos_modulos", []))
    pend = "".join(f"<li>{rico(p)}</li>" for p in fam.get("pendencias", []))
    eyebrow = " · ".join(x for x in [fam.get("sistema"), "marcas dos módulos", fam.get("status")] if x)

    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(fam.get("nome", "Styleguide"))}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
{fonte_link}
<style>
:root {{ --bg:{fundo}; --card:#FFFFFF; --fg:#0E1420; --muted:#55607A; --linha:#D6DBE4; --l:var(--cor,#0E1420); --escuro:{escuro};
  --f:"Inter",system-ui,-apple-system,sans-serif; --mono:"JetBrains Mono",ui-monospace,Menlo,monospace; --fm:"{fonte_marca}",var(--f); color-scheme:light }}
@media (prefers-color-scheme:dark) {{ :root:not([data-theme="light"]) {{ --bg:#0B1019; --card:#121A29; --fg:#E8ECF2; --muted:#9AA4B5; --linha:#263042; --l:#FFFFFF; color-scheme:dark }} }}
:root[data-theme="dark"] {{ --bg:#0B1019; --card:#121A29; --fg:#E8ECF2; --muted:#9AA4B5; --linha:#263042; --l:#FFFFFF; color-scheme:dark }}
* {{ box-sizing:border-box }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:15px/1.5 var(--f) }}
.pag {{ max-width:1120px; margin:0 auto; padding:40px 16px 64px; display:flex; flex-direction:column; gap:48px }}
h1 {{ margin:0; font-size:32px; font-weight:600; letter-spacing:-.02em; text-wrap:balance }}
h2 {{ margin:0; font-size:20px; font-weight:600; letter-spacing:-.01em }}
p {{ margin:0; color:var(--muted); line-height:1.6; max-width:66ch }}
.eyebrow {{ font-family:var(--mono); font-size:12px; letter-spacing:.06em; text-transform:uppercase; color:var(--muted) }}
section, .topo {{ display:flex; flex-direction:column; gap:16px }}
.fila {{ list-style:none; margin:0; padding:0; display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); gap:12px }}
.prod {{ background:var(--card); border-radius:12px; padding:20px 16px; display:flex; flex-direction:column; gap:12px; min-width:0 }}
.prod .marca {{ width:64px; height:64px }}
.nome {{ display:flex; gap:6px; align-items:baseline; flex-wrap:wrap }} .nome b {{ font-weight:600 }} .nome span {{ color:var(--muted); font-size:13px }}
.prod p {{ font-size:13px; line-height:1.5 }}
ul.regras, .lista, .pend {{ margin:0; padding-left:20px; color:var(--muted); line-height:1.7; max-width:72ch }}
ul.regras b, .pend b, .lista b {{ color:var(--fg); font-weight:600 }}
.tab {{ overflow-x:auto; background:var(--card); border-radius:12px; max-width:100% }}
table {{ border-collapse:collapse; width:100%; font-size:14px }}
th, td {{ text-align:left; padding:12px 16px; border-bottom:1px solid var(--linha); white-space:nowrap }}
th {{ font-weight:500; color:var(--muted); font-size:12px }} tr:last-child td {{ border-bottom:0 }}
.nao {{ color:#B42318 }}
@media (prefers-color-scheme:dark) {{ :root:not([data-theme="light"]) .nao {{ color:#FDA29B }} }}
:root[data-theme="dark"] .nao {{ color:#FDA29B }}
.sw {{ display:inline-block; width:14px; height:14px; background:var(--cor); margin-right:10px; vertical-align:-2px; box-shadow:0 0 0 1px var(--linha); flex:none }}
.mono {{ font-family:var(--mono); font-size:13px }} .num {{ font-variant-numeric:tabular-nums }}
.res {{ list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:6px; color:var(--muted) }}
.alertas {{ margin:0; padding:12px 16px 12px 36px; border-radius:12px; background:var(--card); color:var(--muted); line-height:1.6 }}
.hd {{ display:flex; flex-wrap:wrap; gap:10px 28px; align-items:center; padding:16px 20px; border-radius:12px; font-size:14px }}
.hd.claro {{ background:#FFFFFF; color:#0E1420; box-shadow:inset 0 0 0 1px #D6DBE4 }} .hd.escuro {{ background:var(--escuro); color:#FFFFFF }}
.hd-item {{ display:flex; align-items:center; gap:8px }} .hd-item span {{ color:#7C879B }} .hd-m {{ width:24px; height:24px }}
.tams {{ display:flex; flex-direction:column; gap:16px; background:var(--card); border-radius:12px; padding:24px; overflow-x:auto }}
.tam {{ display:flex; align-items:center; gap:16px }} .tl {{ display:flex; gap:16px; align-items:center; flex-wrap:wrap }}
.tam span {{ font-family:var(--mono); font-size:12px; color:var(--muted) }}
.sg-lista {{ display:flex; flex-direction:column; gap:8px }}
.sg {{ background:var(--card); border-radius:12px }}
.sg summary {{ list-style:none; cursor:pointer; display:flex; align-items:center; justify-content:space-between; gap:12px; padding:14px 20px; min-height:44px; border-radius:12px }}
.sg summary::-webkit-details-marker {{ display:none }}
.sg summary:focus-visible {{ outline:2px solid var(--fg); outline-offset:2px }}
.sg summary::after {{ content:""; width:8px; height:8px; border-right:1.5px solid var(--muted); border-bottom:1.5px solid var(--muted); transform:rotate(45deg); transition:transform .2s; flex:none }}
.sg[open] summary::after {{ transform:rotate(225deg) }}
.sg summary .sw {{ margin:0 0 0 auto }}
.sg-cab {{ display:flex; align-items:center; gap:12px; min-width:0 }} .sg-cab b {{ font-weight:600 }} .sg-verbo {{ color:var(--muted); font-size:13px }}
.sg-dl {{ margin:0; padding:4px 20px 20px; display:grid; grid-template-columns:200px minmax(0,1fr) }}
.sg-dl dt, .sg-dl dd {{ padding:14px 0; border-top:1px solid var(--linha); margin:0 }}
.sg-dl dt {{ color:var(--muted); font-size:13px; padding-right:16px }}
.sg-dl dd {{ display:flex; flex-wrap:wrap; align-items:center; gap:8px 12px; line-height:1.55; min-width:0 }}
.sg-dl dd > span {{ color:var(--muted); max-width:66ch }}
@media (max-width:640px) {{ .sg-dl {{ grid-template-columns:1fr }} .sg-dl dd {{ border-top:0; padding-top:0 }} }}
.duas {{ display:flex; gap:8px }}
.f-claro, .f-escuro {{ display:grid; place-items:center; width:56px; height:56px; border-radius:10px }}
.f-claro {{ background:#FFFFFF; box-shadow:inset 0 0 0 1px #D6DBE4 }} .f-escuro {{ background:var(--escuro) }}
.tex {{ width:120px; height:64px; border-radius:10px; background-color:var(--escuro); opacity:.7 }}
.frase {{ color:var(--fg); font-size:16px; font-weight:500; flex-basis:100% }}
.falta {{ font-family:var(--mono); font-size:12px; color:var(--muted); padding:2px 8px; border-radius:6px; box-shadow:inset 0 0 0 1px var(--linha) }}
.anim {{ display:grid; place-items:center; width:88px; height:88px; border-radius:10px; background:var(--escuro) }}
.anim-respirar svg {{ animation:respirar 3.2s ease-in-out infinite }}
@keyframes respirar {{ 50% {{ transform:scale(.92); opacity:.8 }} }}
.anim-montar path {{ animation:montar 2.8s calc(var(--i) * .18s) ease-out infinite both }}
@keyframes montar {{ 0% {{ opacity:0; transform:translateY(6px) }} 25%, 80% {{ opacity:1; transform:none }} 100% {{ opacity:0 }} }}
.anim-pulsar-agente path[data-agente] {{ animation:pulsar 1.6s ease-in-out infinite; transform-box:fill-box; transform-origin:center }}
@keyframes pulsar {{ 50% {{ transform:scale(.8); opacity:.6 }} }}
.mov {{ position:relative; width:120px; height:24px; border-radius:12px; box-shadow:inset 0 0 0 1px var(--linha) }}
.mov i {{ position:absolute; top:4px; left:4px; width:16px; height:16px; border-radius:50%; background:var(--l); animation:mover var(--dur) var(--curva) infinite alternate }}
@keyframes mover {{ to {{ left:100px }} }}
@media (prefers-reduced-motion:reduce) {{ .anim *, .mov i {{ animation:none !important }} }}
footer {{ font-size:13px; color:var(--muted) }}
.cartao {{ background:var(--card); border-radius:12px; padding:24px; display:flex; flex-direction:column; gap:16px; min-width:0 }}
.duas-col {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:12px }}
.esp-marca {{ font-family:var(--fm); font-weight:800; font-size:48px; line-height:1.1; color:var(--fg); overflow-wrap:anywhere }}
.esp-nomes {{ display:flex; flex-wrap:wrap; gap:8px 20px; font-family:var(--fm); font-weight:700; font-size:22px; color:var(--fg) }}
.esp-ui {{ display:flex; flex-direction:column; gap:6px; color:var(--fg) }}
.esp-ui .h1 {{ font-size:24px; font-weight:700 }} .esp-ui .h2 {{ font-size:20px; font-weight:600 }} .esp-ui .b {{ font-size:14px }}
.rotulo {{ font-family:var(--mono); font-size:12px; color:var(--muted) }}
.icones {{ list-style:none; margin:0; padding:0; display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:12px }}
.icones li {{ background:var(--card); border-radius:12px; padding:16px; display:flex; flex-direction:column; gap:10px }}
.icones p {{ font-size:13px }}
.banners {{ display:flex; flex-direction:column; gap:16px }}
.banners figure {{ margin:0; display:flex; flex-direction:column; gap:8px }}
.banners svg {{ width:100%; height:auto; border-radius:12px; display:block }}
.banners figcaption {{ font-size:13px; color:var(--muted) }}
.lg-grade {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:12px }}
.lg-grade figure {{ margin:0; display:flex; flex-direction:column; gap:8px }} .lg-grade figcaption {{ font-size:13px; color:var(--muted) }}
.lg-par {{ display:grid; grid-template-rows:1fr 1fr; gap:8px }}
.lg-claro, .lg-escuro {{ display:grid; place-items:center; padding:24px; border-radius:12px; min-height:120px }}
.lg-claro {{ background:#FFFFFF; box-shadow:inset 0 0 0 1px #D6DBE4 }} .lg-escuro {{ background:var(--escuro) }}
.lg-claro svg, .lg-escuro svg {{ max-width:100%; height:64px; width:auto }}
.lg-prot {{ align-self:flex-start; padding:var(--p); outline:1.5px dashed var(--muted); outline-offset:-1px; border-radius:4px }}
.lg-prot span {{ display:block; outline:1px solid var(--linha) }} .lg-prot svg {{ display:block }}
.lg-min {{ display:flex; align-items:center; gap:16px; flex-wrap:wrap }} .lg-min svg {{ width:auto }}
.galeria {{ display:flex; flex-wrap:wrap; gap:16px }}
.galeria figure {{ margin:0; display:flex; flex-direction:column; gap:6px; align-items:center }}
.galeria figcaption {{ font-size:12px; color:var(--muted) }}
</style></head><body><main class="pag">
<div class="topo"><span class="eyebrow">{E(eyebrow)}</span><h1>{E(fam.get("nome", ""))}</h1><p>{rico(fam.get("intro", ""))}</p></div>
{sec_logo}
<section aria-labelledby="t-m"><h2 id="t-m">As {n} marcas</h2><ul class="fila">{cards}</ul></section>
<section aria-labelledby="t-r"><h2 id="t-r">O que as {n} têm em comum</h2>{mae_txt}<ul class="regras">{regras}</ul></section>
<section aria-labelledby="t-c"><h2 id="t-c">Cores</h2>
<p>Uma cor por módulo, com pelo menos {minimo:g}:1 no branco e no fundo da aplicação ({E(fundo)}), o mínimo para elemento gráfico. Ficam de fora as cores reservadas abaixo.</p>
<div class="tab"><table><thead><tr><th>Módulo</th><th>Cor</th><th>No branco</th><th>No fundo {E(fundo)}</th><th>Resultado</th></tr></thead><tbody>{tab}</tbody></table></div>
{f'<h2>Cores reservadas</h2><ul class="res">{reservadas}</ul>' if reservadas else ""}
{f'<ul class="alertas">{alertas}</ul>' if alertas else ""}
</section>
<section aria-labelledby="t-h"><h2 id="t-h">No header, a 24 px</h2>
<div class="hd claro">{header(lambda m: m["cor"])}</div>
<div class="hd escuro">{header(lambda m: fam.get("cor_escuro", "#FFFFFF"))}</div>
<div class="tams">{tams}</div></section>
{secoes}
<section aria-labelledby="t-s"><h2 id="t-s">Styleguide de cada módulo</h2>
{f'<ul class="regras">{comum}</ul>' if comum else ""}
<div class="sg-lista">{"".join(acc)}</div></section>
{f'<section aria-labelledby="t-p"><h2 id="t-p">Para decidir</h2><ol class="pend">{pend}</ol></section>' if pend else ""}
<footer>Gerado de produtos.json em {date.today().strftime("%d/%m/%Y")}.</footer>
</main></body></html>
"""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    with open(sys.argv[1], encoding="utf-8") as f:
        dados = json.load(f)
    configurar(dados, sys.argv[1])
    destino = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(sys.argv[1]) or ".", "styleguide.html")
    with open(destino, "w", encoding="utf-8") as f:
        f.write(pagina(dados))
    print("página em", os.path.abspath(destino))
