#!/usr/bin/env python3
"""Confere as cores dos módulos contra o branco, o fundo da aplicação e as cores reservadas.

Uso:
  python3 contraste.py produtos.json           # tabela; sai com código 1 se alguma cor não passa
  python3 contraste.py --cor "#2B8A50" [--fundo "#EEF0F4"]   # testar uma cor solta

Regras (todas lidas de produtos.json > familia):
  - minimo_contraste (padrão 3.0): mínimo para elemento gráfico (WCAG 1.4.11), no branco e em fundo_app;
  - cores_reservadas: [{"cor", "motivo"}]; a cor de um módulo não pode ficar perto delas
    (distância ΔE76 menor que distancia_minima, padrão 20);
  - dois módulos com ΔE menor que 12 geram aviso (lado a lado, ninguém distingue).
  - banners: o texto precisa de 4.5:1 sobre o fundo do banner;
  - movimento.duracoes fora das faixas do DS (100 a 500 ms) geram aviso.
Quando uma cor não passa, o script sugere a mesma matiz escurecida até passar.
"""
import colorsys
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BRANCO = "#FFFFFF"


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def lum(h):
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (f(c) for c in rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def cr(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def lab(h):
    def lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb(h))
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def de(a, b):
    return sum((p - q) ** 2 for p, q in zip(lab(a), lab(b))) ** 0.5


def hexa(r, g, b):
    return "#" + "".join(f"{round(max(0, min(1, c)) * 255):02X}" for c in (r, g, b))


def sugerir(h, fundos, minimo):
    """Mesma matiz e saturação, escurecendo até passar em todos os fundos."""
    hh, l, s = colorsys.rgb_to_hls(*rgb(h))
    while l > 0:
        c = hexa(*colorsys.hls_to_rgb(hh, l, s))
        if all(cr(c, f) >= minimo for f in fundos):
            return c
        l -= 0.01
    return None


def conferir(dados, imprimir=True):
    fam = dados["familia"]
    fundo = fam.get("fundo_app", "#EEF0F4")
    minimo = fam.get("minimo_contraste", 3.0)
    dmin = fam.get("distancia_minima", 20)
    reservadas = fam.get("cores_reservadas", [])
    acento = (fam.get("acento") or {}).get("cor")
    linhas, problemas, avisos = [], [], []
    for m in dados["modulos"]:
        c = m["cor"]
        b, f = cr(c, BRANCO), cr(c, fundo)
        perto = [r for r in reservadas if de(c, r["cor"]) < dmin]
        if acento and de(c, acento) < dmin:
            perto.append({"cor": acento, "motivo": "acento da família"})
        passa = b >= minimo and f >= minimo and not perto
        linhas.append({"id": m["id"], "nome": m["nome"], "cor": c, "branco": b, "fundo": f, "passa": passa,
                       "perto": perto})
        if b < minimo or f < minimo:
            s = sugerir(c, [BRANCO, fundo], minimo)
            problemas.append(f"{m['nome']}: {c} tem {b:.1f}:1 no branco e {f:.1f}:1 no fundo {fundo}; "
                             f"mínimo {minimo:g}:1." + (f" Sugestão na mesma matiz: {s}." if s else ""))
        for r in perto:
            problemas.append(f"{m['nome']}: {c} fica perto de {r['cor']} ({r.get('motivo', 'reservada')}), "
                             f"ΔE {de(c, r['cor']):.0f}, mínimo {dmin}.")
        ac = (m.get("campos") or {}).get("acento") or {}
        if ac.get("cor") and ac["cor"].upper() != c.upper():
            ab = cr(ac["cor"], BRANCO)
            if ab < minimo:
                avisos.append(f"{m['nome']}: o acento de interface {ac['cor']} tem {ab:.1f}:1 no branco; "
                              "use só como fundo translúcido ou faixa, nunca como texto ou ícone sozinho.")
    lg = fam.get("logo") or {}
    if lg.get("cor"):
        for nome_f, f in (("branco", BRANCO), ("fundo", fundo)):
            if cr(lg["cor"], f) < minimo:
                problemas.append(f"Logo: {lg['cor']} tem {cr(lg['cor'], f):.1f}:1 no {nome_f}; mínimo {minimo:g}:1.")
    if lg.get("cor_texto") and cr(lg["cor_texto"], BRANCO) < 4.5:
        problemas.append(f"Logo: o nome em {lg['cor_texto']} tem {cr(lg['cor_texto'], BRANCO):.1f}:1 no branco; texto pede 4.5:1.")
    if fam.get("banners"):
        from gerar import banner
        for b in fam["banners"]:
            _, bf, bt = banner(dados, b)
            if cr(bf, bt) < 4.5:
                problemas.append(f"Banner {b['id']}: texto {bt} sobre {bf} tem {cr(bf, bt):.1f}:1; texto pede 4.5:1.")
    faixas = [(100, 150), (150, 250), (250, 400), (300, 500)]
    for k, v in ((fam.get("movimento") or {}).get("duracoes") or {}).items():
        try:
            ms = float(str(v).replace("ms", "")) if "ms" in str(v) else float(str(v).replace("s", "")) * 1000
        except ValueError:
            continue
        if not any(a <= ms <= b for a, b in faixas):
            avisos.append(f"Movimento {k} = {v}: fora das faixas do DS (100 a 500 ms).")
    mods = dados["modulos"]
    for i, a in enumerate(mods):
        for b in mods[i + 1:]:
            d = de(a["cor"], b["cor"])
            if d < 12:
                avisos.append(f"{a['nome']} e {b['nome']} estão quase iguais (ΔE {d:.0f}).")
    if acento:
        avisos.append(f"Acento {acento}: {cr(acento, BRANCO):.1f}:1 no branco e "
                      f"{cr(acento, fam.get('fundo_escuro', '#0E1420')):.1f}:1 no fundo escuro.")
    if imprimir:
        print(f"{'Módulo':<16} {'Cor':<8}  {'Branco':>7}  {'Fundo ' + fundo:>14}  Resultado")
        for l in linhas:
            print(f"{l['nome']:<16} {l['cor']:<8}  {l['branco']:>6.1f}:1  {l['fundo']:>12.1f}:1  "
                  f"{'passa' if l['passa'] else 'NÃO PASSA'}")
        for p in problemas:
            print("✗", p)
        for a in avisos:
            print("!", a)
    return linhas, problemas, avisos


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    if args[0] == "--cor":
        c = args[1]
        fundo = args[args.index("--fundo") + 1] if "--fundo" in args else "#EEF0F4"
        print(f"{c}: {cr(c, BRANCO):.2f}:1 no branco, {cr(c, fundo):.2f}:1 em {fundo}")
        s = sugerir(c, [BRANCO, fundo], 3.0)
        if s and s.upper() != c.upper():
            print(f"Mais escura que passa nos dois com 3:1: {s}")
        sys.exit(0)
    from formas import configurar
    with open(args[0], encoding="utf-8") as f:
        dados = json.load(f)
    configurar(dados, args[0])
    _, problemas, _ = conferir(dados)
    sys.exit(1 if problemas else 0)
