#!/usr/bin/env python3
"""Gera os arquivos da identidade a partir do produtos.json (a fonte única).

Uso:
  python3 gerar.py produtos.json [pasta-de-saida]     # padrão: <pasta do json>/svg

Saída:
  <id>.svg, <id>-escuro.svg, <id>-acento.svg, <id>-escuro-acento.svg   marcas dos módulos
      (na cor do módulo; branca; com a peça do agente na cor de acento). Sem acento, só as duas primeiras.
  icones/<id>.svg, icones/<id>-escuro.svg                              ícones de marca (familia.icones.de_marca)
  banners/<id>.svg                                                     banners (familia.banners)
  logo/simbolo*.svg, logo/horizontal*.svg, logo/vertical*.svg         logo do produto (familia.logo), claro e -escuro
  tokens.css                                                           variáveis para o index.css do produto

Não apaga nada: SVGs que estão na pasta e não vieram desta rodada são listados como sobrando.
"""
import html
import json
import os
import sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from formas import configurar, pecas_do_logo, pecas_do_modulo, svg  # noqa: E402

E = html.escape


def modulo(dados, mid):
    return next((m for m in dados["modulos"] if m["id"] == mid), None)


def banner(dados, b):
    """SVG do banner: fundo, textura opcional, título e subtítulo na fonte de marca, marca à direita."""
    fam = dados["familia"]
    w, h = b.get("formato", [1200, 400])
    m = modulo(dados, b.get("modulo")) if b.get("modulo") else None
    fundo = {"escuro": fam.get("fundo_escuro", "#0E1420"), "cor": (m or {}).get("cor")}.get(b.get("fundo", "escuro")) \
        or b.get("fundo") or fam.get("fundo_escuro", "#0E1420")
    texto = b.get("cor_texto", "#FFFFFF")
    acento = (fam.get("acento") or {}).get("cor")
    fonte = ((fam.get("tipografia") or {}).get("marca") or {}).get("familia", "Inter")
    peso = (((fam.get("tipografia") or {}).get("marca") or {}).get("pesos") or [700])[-1]
    pad = h * 0.16
    tam = h * 0.62
    tex = ""
    tile = ((m or {}).get("campos") or {}).get("textura", {}).get("svg") if b.get("textura") else None
    if tile:
        tex = (f'<defs><pattern id="t-{E(b["id"])}" width="48" height="48" patternUnits="userSpaceOnUse">'
               f'<image href="data:image/svg+xml,{quote(tile)}" width="48" height="48"/></pattern></defs>'
               f'<rect width="{w}" height="{h}" fill="url(#t-{E(b["id"])})" opacity=".08"/>')
    marca = ""
    pecas = pecas_do_modulo(m) if m else pecas_do_logo(fam)
    if pecas:
        marca = svg(pecas, texto, acento=acento).replace(
            "<svg ", f'<svg x="{w - pad - tam:g}" y="{(h - tam) / 2:g}" width="{tam:g}" height="{tam:g}" ', 1)
    t1, t2 = h * 0.13, h * 0.065
    y1 = h / 2 - (t2 * 0.6 if b.get("subtitulo") else -t1 * 0.35)
    sub = (f'<text x="{pad:g}" y="{y1 + t2 * 2.1:g}" font-family="{E(fonte)}, Inter, sans-serif" font-size="{t2:g}" '
           f'fill="{texto}" opacity=".8">{E(b["subtitulo"])}</text>') if b.get("subtitulo") else ""
    rot = b.get("titulo", "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{E(rot)}">'
            f'<rect width="{w}" height="{h}" fill="{fundo}"/>{tex}'
            f'<text x="{pad:g}" y="{y1:g}" font-family="{E(fonte)}, Inter, sans-serif" font-weight="{peso}" '
            f'font-size="{t1:g}" fill="{texto}">{E(rot)}</text>{sub}{marca}</svg>'), fundo, texto


def _fonte_marca(fam):
    tm = (fam.get("tipografia") or {}).get("marca") or {}
    return tm.get("familia", "Inter"), (tm.get("pesos") or [700])[-1]


def logo(dados, arranjo, cor, cor_texto, acento=None, cor2=None):
    """Logo em três arranjos: simbolo, horizontal (símbolo + nome ao lado) e vertical (nome embaixo)."""
    fam = dados["familia"]
    lg = fam.get("logo") or {}
    pecas = pecas_do_logo(fam)
    nome = lg.get("nome") or fam.get("sistema", "").split(" (")[0]
    fonte, peso = _fonte_marca(fam)
    rot = f'role="img" aria-label="Logo {E(nome)}"'
    simb = (lambda x, y, t: svg(pecas, cor, acento=acento, cor2=cor2).replace(
        "<svg ", f'<svg x="{x:g}" y="{y:g}" width="{t:g}" height="{t:g}" ', 1)) if pecas else (lambda *a: "")
    if arranjo == "simbolo" and pecas:
        return svg(pecas, cor, rotulo=f"Logo {nome}", acento=acento, cor2=cor2)
    txt = lambda x, y, t, anc: (f'<text x="{x:g}" y="{y:g}" font-family="{E(fonte)}, Inter, sans-serif" font-weight="{peso}" '
                                f'font-size="{t:g}" text-anchor="{anc}" fill="{cor_texto}">{E(nome)}</text>')
    if arranjo == "vertical":
        w = max(64, len(nome) * 0.62 * 20) + 8
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} 96" {rot}>'
                f'{simb((w - 64) / 2, 0, 64)}{txt(w / 2, 92, 20, "middle")}</svg>')
    tw = len(nome) * 0.6 * 30
    x = 80 if pecas else 0
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x + tw + 4:g} 64" {rot}>'
            f'{simb(0, 0, 64)}{txt(x, 43, 30, "start")}</svg>')


def tokens_css(dados):
    fam = dados["familia"]
    linhas = [":root {", "  /* Identidade do produto, gerada do produtos.json. Integre ao index.css do produto. */"]
    if fam.get("acento"):
        linhas.append(f"  --marca-acento: {fam['acento']['cor']};")
    for m in dados["modulos"]:
        linhas.append(f"  --produto-{m['id']}: {m['cor']};")
        ac = ((m.get("campos") or {}).get("acento") or {}).get("cor")
        if ac:
            linhas.append(f"  --produto-{m['id']}-acento: {ac};")
    tm = (fam.get("tipografia") or {}).get("marca")
    if tm:
        linhas.append(f"  --fonte-marca: \"{tm['familia']}\", var(--font-sans, Inter), sans-serif;")
    mv = fam.get("movimento") or {}
    for k, v in (mv.get("duracoes") or {}).items():
        linhas.append(f"  --movimento-{k}: {v};")
    if mv.get("curva"):
        linhas.append(f"  --movimento-curva: {mv['curva']};")
    linhas.append("}")
    return "\n".join(linhas) + "\n"


def _escrever(pasta, nome, conteudo, feitos):
    os.makedirs(pasta, exist_ok=True)
    with open(os.path.join(pasta, nome), "w", encoding="utf-8") as f:
        f.write(conteudo + "\n")
    feitos.add(os.path.join(pasta, nome))


def gerar(dados, saida):
    fam = dados["familia"]
    acento = (fam.get("acento") or {}).get("cor")
    claro_escuro = fam.get("cor_escuro", "#FFFFFF")
    feitos = set()
    for m in dados["modulos"]:
        pc, cor, rot = pecas_do_modulo(m), m["cor"], f"Marca {m['nome']}"
        c2 = m.get("cor2")
        versoes = {"": svg(pc, cor, rotulo=rot, cor2=c2), "-escuro": svg(pc, claro_escuro, rotulo=rot)}
        if acento:
            versoes["-acento"] = svg(pc, cor, rotulo=rot, acento=acento, cor2=c2)
            versoes["-escuro-acento"] = svg(pc, claro_escuro, rotulo=rot, acento=acento)
        for suf, conteudo in versoes.items():
            _escrever(saida, f"{m['id']}{suf}.svg", conteudo, feitos)
    lg = fam.get("logo")
    if lg:
        cor_l, txt_l = lg.get("cor", fam.get("fundo_escuro", "#0E1420")), lg.get("cor_texto", "#0E1420")
        for arr in lg.get("arranjos", ["simbolo", "horizontal", "vertical"]):
            if arr == "simbolo" and not pecas_do_logo(fam):
                continue
            _escrever(os.path.join(saida, "logo"), f"{arr}.svg", logo(dados, arr, cor_l, txt_l, acento, lg.get("cor2")), feitos)
            _escrever(os.path.join(saida, "logo"), f"{arr}-escuro.svg", logo(dados, arr, claro_escuro, claro_escuro, acento), feitos)
    icones = (fam.get("icones") or {}).get("de_marca", [])
    cor_icone = fam.get("cor_icone", "#0E1420")
    for i in icones:
        _escrever(os.path.join(saida, "icones"), f"{i['id']}.svg", svg(i["pecas"], cor_icone, rotulo=i["nome"], acento=acento), feitos)
        _escrever(os.path.join(saida, "icones"), f"{i['id']}-escuro.svg", svg(i["pecas"], claro_escuro, rotulo=i["nome"], acento=acento), feitos)
    for b in fam.get("banners", []):
        _escrever(os.path.join(saida, "banners"), f"{b['id']}.svg", banner(dados, b)[0], feitos)
    _escrever(saida, "tokens.css", tokens_css(dados).rstrip("\n"), feitos)
    existentes = set()
    for raiz, _, arqs in os.walk(saida):
        existentes |= {os.path.join(raiz, a) for a in arqs if a.endswith(".svg")}
    sobrando = sorted(os.path.relpath(f, saida) for f in existentes - feitos)
    print(f"{len(feitos)} arquivos em {os.path.normpath(saida)} "
          f"({'logo, ' if lg else ''}{len(dados['modulos'])} marcas, {len(icones)} ícones de marca, {len(fam.get('banners', []))} banners, tokens.css)")
    if not acento:
        print("! a família não tem acento: só as versões base e -escuro das marcas foram geradas")
    if fam.get("banners") or lg:
        print("! logo e banners usam a fonte de marca como texto: para entregar fora da web, exporte em PNG ou converta o texto em curvas")
    if sobrando:
        print("! sobrando na pasta (não apaguei):", ", ".join(sobrando))
    return feitos


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    with open(sys.argv[1], encoding="utf-8") as f:
        dados = json.load(f)
    configurar(dados, sys.argv[1])
    gerar(dados, sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(sys.argv[1]) or ".", "svg"))
