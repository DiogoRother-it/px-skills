#!/usr/bin/env python3
"""Formas das marcas, descritas como dados no produtos.json (grade de 64 x 64).

Cada marca é uma lista de peças. Uma peça é uma primitiva com transformações opcionais;
o script transforma tudo em contornos de pontos e escreve um <path> por peça.

Uso:
  python3 formas.py produtos.json verificar            # grade, área ocupada e diagonais de cada marca
  python3 formas.py produtos.json canvas opcoes.html   # fase 3: opções de cada módulo lado a lado

Primitivas (campo "tipo"):
  poligono   {"pontos": [[x, y], ...]}
  retangulo  {"x", "y", "largura", "altura"}
  barra      {"de": [x, y], "ate": [x, y], "espessura"}         barra reta de ponta reta
  regular    {"cx", "cy", "r", "lados", "inicio": -90}           hexágono, triângulo, losango...
  circulo    {"cx", "cy", "r"}
  anel       {"cx", "cy", "r", "espessura", "de"?, "ate"?}       sem de/ate = anel inteiro;
                                                                 com de/ate = arco (graus, 0 = direita,
                                                                 crescendo no sentido horário)
  path       {"d": "M...", "transform"?}                        desenho livre (curvas Bézier, ilustração)
  arquivo    {"caminho": "logo.svg"}                             traz os <path> de um SVG feito fora (Figma,
                                                                 Illustrator), escalado para a grade; caminho
                                                                 relativo ao produtos.json
  texto      {"texto": "SV", "x", "y", "tamanho", "peso"?, "fonte"?}   letra ou monograma (proposta; para
                                                                 entregar, converta em curvas)
  path, arquivo e texto não recebem transformação e ficam fora da conferência de área.

Estilo (produtos.json > familia.estilo), vale para todas as peças:
  "preenchimento": "solido" | "contorno"   contorno = só o traço, com "traco" de espessura (padrão 4)
  "cantos": "retos" | "redondos"           redondos arredonda as quinas com "raio" (padrão 2)
  "gradiente": true                         a peça vai da "cor" à "cor2" do módulo (só nas versões coloridas)
Uma peça pode fugir do estilo com "contorno": true ou false.

Transformações (em qualquer primitiva, menos path), aplicadas nesta ordem:
  "espelhar": "horizontal" | "vertical"   em torno do centro (32, 32)
  "girar": graus, "centro": [32, 32]      sentido horário
  "mover": [dx, dy]
  "repetir": {"vezes": n, "girar": graus} ou {"vezes": n, "mover": [dx, dy]}
  "agente": true                          a peça que vai na cor de acento nas versões -acento
"""
import html
import json
import math
import os
import sys

GRADE = 64
C = GRADE / 2
ESTILO = {}
BASE = "."


def configurar(dados, caminho_json="."):
    """Chamar uma vez depois de ler o produtos.json: guarda o estilo e a pasta para peças do tipo arquivo."""
    global ESTILO, BASE
    ESTILO = dict(dados.get("familia", {}).get("estilo") or {})
    BASE = os.path.dirname(os.path.abspath(caminho_json))


def _importar_svg(caminho):
    import re
    txt = open(os.path.join(BASE, caminho), encoding="utf-8").read()
    vb = re.search(r'viewBox="([-\d.\s,]+)"', txt)
    x0, y0, w, h = [float(v) for v in re.split(r"[\s,]+", vb.group(1).strip())] if vb else (0, 0, GRADE, GRADE)
    k = GRADE / max(w, h)
    dx, dy = (GRADE - w * k) / 2 - x0 * k, (GRADE - h * k) / 2 - y0 * k
    return [(d, f"translate({_f(dx)} {_f(dy)}) scale({k:.4g})") for d in re.findall(r'<path[^>]*?\sd="([^"]+)"', txt)]


def _f(v):
    v = round(v, 2)
    return f"{v:g}" if v != 0 else "0"


def _arco(cx, cy, r, a0, a1, passo=3.0):
    n = max(2, int(math.ceil(abs(a1 - a0) / passo)) + 1)
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / (n - 1))),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / (n - 1)))) for i in range(n)]


def _contornos(p):
    """Devolve (contornos, tem_curva). O furo do anel vem no sentido contrário (área com sinal)."""
    t = p["tipo"]
    if t == "poligono":
        return [[tuple(q) for q in p["pontos"]]], False
    if t == "retangulo":
        x, y, w, h = p["x"], p["y"], p["largura"], p["altura"]
        return [[(x, y), (x + w, y), (x + w, y + h), (x, y + h)]], False
    if t == "barra":
        (x0, y0), (x1, y1), e = p["de"], p["ate"], p["espessura"]
        dx, dy = x1 - x0, y1 - y0
        n = math.hypot(dx, dy)
        ox, oy = -dy / n * e / 2, dx / n * e / 2
        return [[(x0 + ox, y0 + oy), (x1 + ox, y1 + oy), (x1 - ox, y1 - oy), (x0 - ox, y0 - oy)]], False
    if t == "regular":
        a0, k = p.get("inicio", -90), p["lados"]
        return [[(p["cx"] + p["r"] * math.cos(math.radians(a0 + 360 * i / k)),
                  p["cy"] + p["r"] * math.sin(math.radians(a0 + 360 * i / k))) for i in range(k)]], False
    if t == "circulo":
        return [_arco(p["cx"], p["cy"], p["r"], 0, 360)[:-1]], True
    if t == "anel":
        cx, cy, r, e = p["cx"], p["cy"], p["r"], p["espessura"]
        if "de" in p and "ate" in p:
            fora = _arco(cx, cy, r, p["de"], p["ate"])
            dentro = _arco(cx, cy, r - e, p["ate"], p["de"])
            return [fora + dentro], True
        return [_arco(cx, cy, r, 0, 360)[:-1], _arco(cx, cy, r - e, 360, 0)[:-1]], True
    raise ValueError(f"tipo de peça desconhecido: {t!r}")


def _transformar(pts, p):
    if p.get("espelhar") == "horizontal":
        pts = [(2 * C - x, y) for x, y in pts][::-1]
    elif p.get("espelhar") == "vertical":
        pts = [(x, 2 * C - y) for x, y in pts][::-1]
    if p.get("girar"):
        cx, cy = p.get("centro", [C, C])
        a = math.radians(p["girar"])
        c, s = math.cos(a), math.sin(a)
        pts = [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]
    if p.get("mover"):
        dx, dy = p["mover"]
        pts = [(x + dx, y + dy) for x, y in pts]
    return pts


def expandir(pecas):
    """Lista de dicts {contornos, d, agente, curva}, já com repetições e transformações."""
    saida = []
    for p in pecas:
        base = {"agente": bool(p.get("agente")), "contorno": p.get("contorno"), "curva": True, "contornos": None}
        if p["tipo"] == "path":
            saida.append({**base, "d": p["d"], "transform": p.get("transform")})
            continue
        if p["tipo"] == "arquivo":
            saida += [{**base, "d": d, "transform": t} for d, t in _importar_svg(p["caminho"])]
            continue
        if p["tipo"] == "texto":
            saida.append({**base, "texto": p})
            continue
        rep = p.get("repetir") or {"vezes": 1}
        for i in range(rep["vezes"]):
            q = dict(p)
            if i and rep.get("girar"):
                q["girar"] = q.get("girar", 0) + rep["girar"] * i
            if i and rep.get("mover"):
                mx, my = q.get("mover", [0, 0])
                q["mover"] = [mx + rep["mover"][0] * i, my + rep["mover"][1] * i]
            cont, curva = _contornos(q)
            cont = [_transformar(c, q) for c in cont]
            d = " ".join("M" + " L".join(f"{_f(x)} {_f(y)}" for x, y in c) + " Z" for c in cont)
            saida.append({"contornos": cont, "d": d, "agente": bool(p.get("agente")),
                          "contorno": p.get("contorno"), "curva": curva})
    return saida


def pecas_do_modulo(m):
    """As peças valendo: as do módulo, ou as da opção escolhida."""
    if m.get("pecas"):
        return m["pecas"]
    for o in m.get("opcoes", []):
        if o["id"] == m.get("escolhida"):
            return o["pecas"]
    if m.get("opcoes"):
        return m["opcoes"][0]["pecas"]
    raise ValueError(f"o módulo {m['id']} não tem peças nem opções")


def _tinta(cor, x):
    """Atributos de pintura conforme o estilo da família."""
    contorno = x["contorno"] if x.get("contorno") is not None else ESTILO.get("preenchimento") == "contorno"
    redondo = ESTILO.get("cantos") == "redondos"
    junta = "round" if redondo else "miter"
    if contorno:
        return (f'fill="none" stroke="{cor}" stroke-width="{_f(ESTILO.get("traco", 4))}" '
                f'stroke-linejoin="{junta}" stroke-linecap="{"round" if redondo else "butt"}"')
    if redondo:
        return f'fill="{cor}" stroke="{cor}" stroke-width="{_f(2 * ESTILO.get("raio", 2))}" stroke-linejoin="round"'
    return f'fill="{cor}" fill-rule="evenodd"'


def svg(pecas, cor, tam=None, rotulo=None, cls="", acento=None, anim=False, cor2=None):
    """acento: cor da peça do agente (None = igual ao resto).
    cor2: com familia.estilo.gradiente, a peça vai de cor a cor2.
    anim: marca cada peça com --i (ordem) e data-agente, para a página animar."""
    t = f' width="{tam}" height="{tam}"' if tam else ""
    a = f' role="img" aria-label="{html.escape(rotulo)}"' if rotulo else ' aria-hidden="true"'
    c = f' class="{cls}"' if cls else ""
    defs, base = "", cor
    if ESTILO.get("gradiente") and cor2:
        gid = "g" + "".join(ch for ch in (cor + cor2) if ch.isalnum())
        defs = (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">'
                f'<stop offset="0" stop-color="{cor}"/><stop offset="1" stop-color="{cor2}"/></linearGradient></defs>')
        base = f"url(#{gid})"

    def extra(i, x):
        if not anim:
            return ""
        return f' style="--i:{i}"' + (' data-agente="1"' if x["agente"] else "")

    partes = []
    for i, x in enumerate(expandir(pecas)):
        k = acento if (acento and x["agente"]) else base
        if x.get("texto"):
            p = x["texto"]
            fonte = p.get("fonte") or "var(--fm, Inter), Inter, sans-serif"
            partes.append(f'<text x="{_f(p.get("x", C))}" y="{_f(p.get("y", 44))}" font-size="{_f(p.get("tamanho", 32))}" '
                          f'font-weight="{p.get("peso", 700)}" font-family="{html.escape(fonte)}" '
                          f'text-anchor="{p.get("ancora", "middle")}" fill="{k}"{extra(i, x)}>{html.escape(p["texto"])}</text>')
            continue
        tr = f' transform="{x["transform"]}"' if x.get("transform") else ""
        partes.append(f'<path d="{x["d"]}" {_tinta(k, x)}{tr}{extra(i, x)}/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {GRADE} {GRADE}"{t}{a}{c}>{defs}{"".join(partes)}</svg>'


def pecas_do_logo(fam):
    """Símbolo do logo: o do logo, a opção escolhida, ou as peças da marca-mãe."""
    lg = fam.get("logo") or {}
    if lg.get("pecas"):
        return lg["pecas"]
    for o in lg.get("opcoes", []):
        if o["id"] == lg.get("escolhida"):
            return o["pecas"]
    if lg.get("opcoes"):
        return lg["opcoes"][0]["pecas"]
    return (fam.get("marca_mae") or {}).get("pecas")


# ---------- conferência ----------

def _area(c):
    return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(c, c[1:] + c[:1])) / 2


def _razao(dx, dy):
    if abs(dx) < 1e-6 or abs(dy) < 1e-6:
        return None
    r = abs(dy / dx)
    return f"{r:.2g}:1" if r >= 1 else f"1:{1 / r:.2g}"


def medir(pecas):
    xs, ys, area, diag, fora, sem = [], [], 0.0, {}, False, 0
    for x in expandir(pecas):
        if not x["contornos"]:
            sem += 1
            continue
        area += abs(sum(_area(c) for c in x["contornos"]))
        for c in x["contornos"]:
            for px, py in c:
                xs.append(px); ys.append(py)
                fora |= not (-0.01 <= px <= GRADE + 0.01 and -0.01 <= py <= GRADE + 0.01)
            if not x["curva"]:
                for (x0, y0), (x1, y1) in zip(c, c[1:] + c[:1]):
                    r = _razao(x1 - x0, y1 - y0)
                    if r:
                        diag[r] = diag.get(r, 0) + 1
    caixa = (min(xs), min(ys), max(xs), max(ys)) if xs else (0, 0, 0, 0)
    return {"area": 100 * area / GRADE ** 2, "caixa": caixa, "diagonais": diag, "fora": fora,
            "agentes": sum(1 for x in expandir(pecas) if x["agente"]), "pecas": len(expandir(pecas)), "sem_medida": sem}


def verificar(dados):
    linhas, areas, ok = [], [], True
    itens = [(m["nome"], pecas_do_modulo(m), True) for m in dados["modulos"]]
    if pecas_do_logo(dados["familia"]):
        itens.insert(0, ("logo", pecas_do_logo(dados["familia"]), False))
    itens += [(f"ícone {i['nome']}", i["pecas"], False)
              for i in (dados["familia"].get("icones") or {}).get("de_marca", [])]
    for nome, pecas, eh_marca in itens:
        m = {"nome": nome}
        r = medir(pecas)
        if eh_marca and not r["sem_medida"]:
            areas.append((m["nome"], r["area"]))
        x0, y0, x1, y1 = r["caixa"]
        diag = ", ".join(f"{k} ({v})" for k, v in sorted(r["diagonais"].items())) or "nenhuma"
        linhas.append(f"{m['nome']:<22} {r['pecas']} peças · agente: {r['agentes']} · "
                      + (f"tinta não medida ({r['sem_medida']} peça(s) de texto, path ou arquivo) · " if r["sem_medida"] else f"tinta {r['area']:.0f}% · ")
                      + f"caixa {_f(x0)},{_f(y0)} a {_f(x1)},{_f(y1)} · diagonais: {diag}")
        if r["fora"]:
            linhas.append(f"  ✗ {m['nome']}: há ponto fora da grade de {GRADE}")
            ok = False
        if eh_marca and dados["familia"].get("acento") and r["agentes"] == 0:
            linhas.append(f"  ! {m['nome']}: nenhuma peça marcada como agente; as versões -acento saem iguais à base")
    if areas:
        med = sorted(a for _, a in areas)[len(areas) // 2]
        for nome, a in areas:
            if med and abs(a - med) / med > 0.25:
                linhas.append(f"  ! {nome}: tinta {a:.0f}% contra a mediana de {med:.0f}%; lado a lado vai pesar diferente")
    print("\n".join(linhas))
    print("Diagonais são as razões altura:largura das arestas retas. Confira com as regras da linguagem.")
    if ESTILO.get("preenchimento") == "contorno":
        print("Estilo em contorno: a tinta é medida pela forma cheia; compare o peso olhando o canvas.")
    return ok


# ---------- canvas de opções (fase 3) ----------

def canvas(dados, destino):
    fam = dados["familia"]
    acento = (fam.get("acento") or {}).get("cor")
    escuro = fam.get("fundo_escuro", "#0E1420")
    tm = (fam.get("tipografia") or {}).get("marca") or {}
    fonte_link = (f'<link rel="stylesheet" href="{html.escape(tm["fonte_url"])}">'
                  if str(tm.get("fonte_url", "")).startswith("https://fonts.googleapis.com/") else "")
    fm = html.escape(tm.get("familia", "Inter"))
    blocos = []
    lg = fam.get("logo") or {}
    if lg.get("opcoes"):
        cards = []
        for o in lg["opcoes"]:
            pc, cor = o["pecas"], lg.get("cor", "#0E1420")
            esc = ' <span class="esc">escolhida</span>' if o["id"] == lg.get("escolhida") else ""
            cards.append(f"""<li class="op"><div class="op-cab"><b>Opção {html.escape(str(o['id']))}</b>{esc}</div>
<div class="vistas"><span class="claro">{svg(pc, cor, 64, acento=acento, cor2=lg.get('cor2'))}</span><span class="esc-f">{svg(pc, '#FFFFFF', 64, acento=acento)}</span></div>
<div class="peq"><span class="claro">{svg(pc, cor, 24)}{svg(pc, cor, 16)}</span><span class="esc-f">{svg(pc, '#FFFFFF', 24)}{svg(pc, '#FFFFFF', 16)}</span></div>
<p>{html.escape(o.get('porque', ''))}</p></li>""")
        blocos.append(f"""<section><h2>Logo · {html.escape(lg.get('nome', fam.get('sistema', '')))}</h2><ul class="ops">{''.join(cards)}</ul></section>""")
    for m in dados["modulos"]:
        opcoes = m.get("opcoes") or [{"id": "única", "porque": m.get("porque", ""), "pecas": pecas_do_modulo(m)}]
        cards = []
        for o in opcoes:
            pc, cor = o["pecas"], m["cor"]
            esc = ' <span class="esc">escolhida</span>' if o["id"] == m.get("escolhida") else ""
            cards.append(f"""<li class="op"><div class="op-cab"><b>Opção {html.escape(str(o['id']))}</b>{esc}</div>
<div class="vistas"><span class="claro">{svg(pc, cor, 64, acento=acento, cor2=m.get('cor2'))}</span><span class="esc-f">{svg(pc, '#FFFFFF', 64, acento=acento)}</span></div>
<div class="peq"><span class="claro">{svg(pc, cor, 24)}{svg(pc, cor, 16)}</span><span class="esc-f">{svg(pc, '#FFFFFF', 24)}{svg(pc, '#FFFFFF', 16)}</span></div>
<p>{html.escape(o.get('porque', ''))}</p></li>""")
        blocos.append(f"""<section><h2>{html.escape(m['nome'])} <span>{html.escape(m.get('verbo', ''))}</span></h2>
<ul class="ops">{''.join(cards)}</ul></section>""")
    doc = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Opções de marca</title>{fonte_link}
<style>
:root {{ --fm:"{fm}"; --bg:#EEF0F4; --card:#FFFFFF; --fg:#0E1420; --muted:#55607A; --linha:#D6DBE4; --escuro:{escuro}; color-scheme:light }}
@media (prefers-color-scheme:dark) {{ :root:not([data-theme="light"]) {{ --bg:#0B1019; --card:#121A29; --fg:#E8ECF2; --muted:#9AA4B5; --linha:#263042; color-scheme:dark }} }}
:root[data-theme="dark"] {{ --bg:#0B1019; --card:#121A29; --fg:#E8ECF2; --muted:#9AA4B5; --linha:#263042; color-scheme:dark }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:15px/1.5 system-ui,-apple-system,sans-serif }}
.pag {{ max-width:1120px; margin:0 auto; padding:40px 16px 64px; display:flex; flex-direction:column; gap:40px }}
h1 {{ margin:0; font-size:28px }} h2 {{ margin:0 0 12px; font-size:18px }} h2 span {{ color:var(--muted); font-weight:400; font-size:14px }}
.intro {{ color:var(--muted); max-width:66ch; margin:8px 0 0 }}
.ops {{ list-style:none; margin:0; padding:0; display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:12px }}
.op {{ background:var(--card); border-radius:12px; padding:16px; display:flex; flex-direction:column; gap:12px }}
.op-cab {{ display:flex; gap:8px; align-items:center }} .esc {{ font-size:12px; padding:2px 8px; border-radius:6px; box-shadow:inset 0 0 0 1px var(--linha) }}
.vistas, .peq {{ display:flex; gap:8px }}
.claro, .esc-f {{ display:flex; gap:12px; align-items:center; justify-content:center; padding:12px; border-radius:10px; flex:1 }}
.claro {{ background:#FFFFFF; box-shadow:inset 0 0 0 1px #D6DBE4 }} .esc-f {{ background:var(--escuro) }}
.op p {{ margin:0; color:var(--muted); font-size:14px }}
</style></head><body><div class="pag">
<header><h1>Opções de marca: {html.escape(fam.get('nome', ''))}</h1>
<p class="intro">Duas ou três opções do logo e de cada módulo, em 64, 24 e 16 px, no claro e no escuro. Escolha uma por módulo, ou peça uma mistura.</p></header>
{''.join(blocos)}
</div></body></html>
"""
    with open(destino, "w", encoding="utf-8") as f:
        f.write(doc)
    print("canvas em", os.path.abspath(destino))


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[2] not in ("verificar", "canvas"):
        print(__doc__)
        sys.exit(2)
    with open(sys.argv[1], encoding="utf-8") as f:
        dados = json.load(f)
    configurar(dados, sys.argv[1])
    if sys.argv[2] == "verificar":
        sys.exit(0 if verificar(dados) else 1)
    canvas(dados, sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(sys.argv[1]) or ".", "opcoes.html"))
