"""Charts fuer / for no. 04 - Versprochen: ja. Zuständig: jein. (Landeshebel der Wahlprogramme, AURYN Teil 1).
Daten: 004-daten.json (DATA-Objekt des Dashboards, Stand 56c, 17.10.2026). Regeln: theme.py / DESIGN.md.
Akzent gelb (Rubrik gesellschaft): die Fläche, um die es geht, ist gelb; alles andere schwarz oder grau."""
import json, os
import theme
from theme import FARBEN, SCHRIFT
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

S, Y, G, GH, W = FARBEN["schwarz"], FARBEN["gelb"], FARBEN["grau"], FARBEN["grauhell"], "#ffffff"
H = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(H, "004-daten.json"), encoding="utf-8"))
rows, P, L = D["rows"], D["parteien"], D["laender"]
de = lambda x, n=1: f"{x:.{n}f}".replace(".", ",")

def fig(h=3.0, left=0.16, bottom=0.16, top=0.93, right=0.97):
    f, ax = plt.subplots(figsize=(6.4, h))
    f.subplots_adjust(left=left, right=right, top=top, bottom=bottom)
    return f, ax

def fertig(f, ax, fussnote, name, x0=0.02):
    if fussnote: f.text(x0, 0.03, fussnote, color=G, fontsize=10, fontproperties=SCHRIFT[400])
    f.savefig(os.path.join(H, f"004-{name}.de.svg"), format="svg", transparent=True); plt.close(f)

def nackt(ax, links=True):
    ax.set_xticks([]); ax.tick_params(left=False, bottom=False)
    for s in ("top", "right", "bottom"): ax.spines[s].set_visible(False)
    ax.spines.left.set_visible(links)
    if links: ax.spines.left.set_linewidth(2); ax.spines.left.set_color(S)

def ylabels(ax, ys, namen, w=500):
    ax.set_yticks(list(ys)); ax.set_yticklabels(namen)
    for lab in ax.get_yticklabels(): lab.set_fontproperties(SCHRIFT[w]); lab.set_fontsize(10.5); lab.set_color(S)

CODES = [("D", "land allein"), ("B", "land mit anderen"), ("F", "bund / eu"), ("K", "kommunen"), ("S", "selbstverwaltung / dritte"), ("U", "unbestimmt")]
def farbe(c): return {"D": Y, "B": Y, "F": S, "K": G, "S": G, "U": GH}[c]

# --- 1: der eine Balken (Kernaussage 1) ---
def c1():
    f, ax = fig(2.1, left=0.02, right=0.98, bottom=0.30, top=0.80)
    x = 0
    for c, l in CODES:
        v = D["totp"][c]
        ax.barh(0, v, left=x, height=0.6, color=farbe(c), edgecolor=W, linewidth=1.5)
        if v >= 4:
            ax.text(x + v / 2, 0, f"{c} {de(v)} %", ha="center", va="center", fontsize=10.5,
                    color=S if c in ("D", "B") else W, fontproperties=SCHRIFT[700 if c in ("D", "B") else 500])
        x += v
    db = D["DB"]
    ax.plot([0, db], [0.55, 0.55], color=S, lw=2); ax.plot([0, 0], [0.5, 0.6], color=S, lw=2); ax.plot([db, db], [0.5, 0.6], color=S, lw=2)
    ax.text(db / 2, 0.72, f"landeshebel d + b: {de(db)} %", ha="center", va="bottom", fontsize=11, color=S, fontproperties=SCHRIFT[700])
    ax.text((db + 100) / 2, 0.72, f"nicht allein einlösbar: {de(100 - db)} %", ha="center", va="bottom", fontsize=11, color=G, fontproperties=SCHRIFT[500])
    ax.set_xlim(0, 100); ax.set_ylim(-0.6, 1.1); nackt(ax, links=False); ax.set_yticks([])
    fertig(f, ax, "alle 28.071 positionen der 48 programme nach zuständigkeit · gelb: das land hat den hebel", "hebel")

# --- 2: die vier Adressaten außerhalb des Hebels (Kernaussage 2) ---
def c2():
    items = [("U", "unbestimmt, kein weg benannt"), ("F", "bund / eu"), ("K", "kommunen"), ("S", "selbstverwaltung / dritte")]
    f, ax = fig(2.6, left=0.38, bottom=0.18)
    ys = range(len(items))[::-1]
    for y, (c, l) in zip(ys, items):
        v = D["totp"][c]; col = Y if c == "U" else S
        ax.barh(y, v, height=0.6, color=col, linewidth=0)
        ax.text(v + 0.5, y, f"{de(v)} %", va="center", fontsize=10.5, color=S, fontproperties=SCHRIFT[700 if c == "U" else 500])
    ylabels(ax, ys, [l for _, l in items]); ax.set_xlim(0, 32); nackt(ax)
    fertig(f, ax, "die 39 % außerhalb des landeshebels, aufgeteilt nach adressat · anteil an allen 28.071 positionen", "adressat")

# --- 3: Streudiagramm U-Anteil gegen Hebel (Kernaussage 3) ---
def c3():
    f, ax = fig(3.4, left=0.12, bottom=0.18, top=0.95)
    xs = [r["Up"] for r in rows]; ys = [r["DB"] for r in rows]
    ax.scatter(xs, ys, s=34, color=S, zorder=3, linewidths=0)
    m, b = D["ols"]; ax.plot([14, 42], [m * 14 + b, m * 42 + b], color=Y, lw=2.5, ls=(0, (4, 3)), zorder=2)
    for r, dx, dy, ha, va in [(D["hi"], 0.7, -0.3, "left", "top"), (D["lo"], -0.7, 0.3, "right", "bottom")]:
        ax.text(r["Up"] + dx, r["DB"] + dy, f'{r["kurz"]} {r["partei"]} · {de(r["DB"])} %', fontsize=9.5, ha=ha, va=va, color=S, fontproperties=SCHRIFT[500])
    ax.set_xlim(12, 44); ax.set_ylim(38, 80)
    ax.set_xticks([15, 20, 25, 30, 35, 40]); ax.set_xticklabels([f"{v} %" for v in (15, 20, 25, 30, 35, 40)])
    ax.set_yticks([40, 50, 60, 70, 80]); ax.set_yticklabels([f"{v} %" for v in (40, 50, 60, 70, 80)])
    for lab in ax.get_xticklabels() + ax.get_yticklabels(): lab.set_fontproperties(SCHRIFT[400]); lab.set_fontsize(9.5); lab.set_color(G)
    ax.tick_params(left=False, bottom=False, pad=4)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.spines.left.set_visible(True); ax.spines.left.set_linewidth(1); ax.spines.left.set_color(GH); ax.spines.bottom.set_linewidth(2)
    ax.text(43.5, 78.5, f'gestrichelt: lineare anpassung\nkorrelation hebel–u {de(D["rU"], 2)}, hebel–bund {de(D["rF"], 2)}', ha="right", va="top", fontsize=9.5, color=G, fontproperties=SCHRIFT[400], linespacing=1.3)
    ax.set_ylabel("landeshebel d + b", fontsize=10, color=G, fontproperties=SCHRIFT[400])
    fertig(f, ax, "48 programme · waagerecht: anteil unbestimmter positionen (u) · rechts = vager, unten = kleinerer hebel", "streuung")

# --- 4: Parteien (Kernaussage 4) ---
def c4():
    ps = sorted(P, key=lambda p: -p["DB"]); f, ax = fig(3.0, left=0.14, bottom=0.18)
    ys = range(len(ps))[::-1]
    for y, p in zip(ys, ps):
        col = Y if p is ps[0] or p is ps[-1] else S
        ax.barh(y, p["DB"], height=0.62, color=col, linewidth=0)
        ax.text(p["DB"] + 0.7, y, f'{de(p["DB"])} %', va="center", fontsize=10.5, color=S, fontproperties=SCHRIFT[700 if col == Y else 500])
    ax.axvline(D["DB"], color=S, lw=1, ls=(0, (3, 3)))
    ax.text(D["DB"] + 0.6, -0.75, f'alle 48: {de(D["DB"])} %', fontsize=9.5, color=G, fontproperties=SCHRIFT[400])
    ylabels(ax, ys, [p["name"] for p in ps]); ax.set_xlim(0, 80); ax.set_ylim(-1.1, len(ps) - 0.4); nackt(ax)
    fertig(f, ax, "landeshebel je partei, alle acht programme zusammengerechnet · gelb: erste und letzte", "parteien")

# --- 5: Matrix Land × Partei (Kernaussage 5) ---
def c5():
    lands = [l["name"] for l in sorted(L, key=lambda l: -l["DB"])]; parts = ["SPD", "Grüne", "CDU", "AfD", "Linke", "BSW"]
    f, ax = fig(3.8, left=0.22, right=0.99, bottom=0.12, top=0.90)
    for i, land in enumerate(lands):
        rs = sorted([r for r in rows if r["land"] == land], key=lambda r: -r["DB"])
        for j, pn in enumerate(parts):
            r = next(x for x in rs if x["partei"] == pn); rank = rs.index(r) + 1
            y = len(lands) - 1 - i
            if rank == 1: ax.add_patch(plt.Rectangle((j - 0.5, y - 0.5), 1, 1, color=Y, lw=0))
            ax.text(j, y, de(r["DB"]), ha="center", va="center", fontsize=10.5, color=S if rank != 6 else G,
                    fontproperties=SCHRIFT[700 if rank == 1 else 400])
    for j, pn in enumerate(parts): ax.text(j, len(lands) - 0.35, pn, ha="center", va="bottom", fontsize=10, color=S, fontproperties=SCHRIFT[500])
    ylabels(ax, range(len(lands))[::-1], lands, 400); ax.set_xlim(-0.5, len(parts) - 0.5); ax.set_ylim(-0.5, len(lands) + 0.3)
    nackt(ax, links=False); ax.tick_params(left=False)
    fertig(f, ax, "landeshebel in % je programm · gelb: rang 1 im land · grau: rang 6", "matrix")

# --- 6: Gründe je Partei (Kernaussage 6) ---
def stapel(items, name, fuss):
    f, ax = fig(3.0, left=0.14, right=0.98, bottom=0.18)
    ys = range(len(items))[::-1]
    for y, it in zip(ys, items):
        x = 0
        for key, col, lab in (("DBp", Y, "hebel"), ("Fp", S, "F"), ("KSp", G, ""), ("Up", GH, "U")):
            v = it[key]
            ax.barh(y, v, left=x, height=0.62, color=col, edgecolor=W, linewidth=1)
            if v >= 6:
                ax.text(x + v / 2, y, de(v, 0), ha="center", va="center", fontsize=9.5, color=S if col in (Y, GH) else W, fontproperties=SCHRIFT[500])
            x += v
    ylabels(ax, ys, [it["name"] for it in items]); ax.set_xlim(0, 100); nackt(ax)
    ax.text(0, len(items) - 0.3, "gelb: landeshebel d + b   schwarz: bund / eu   grau: kommunen, dritte   hellgrau: unbestimmt", fontsize=9.5, color=G, fontproperties=SCHRIFT[400])
    ax.set_ylim(-0.6, len(items) + 0.2)
    fertig(f, ax, fuss, name)

def anteile(g): return dict(name=g["name"], DBp=g["Dp"] + g["Bp"], Fp=g["Fp"], KSp=g["Kp"] + g["Sp"], Up=g["Up"])
def c6(): stapel([anteile(p) for p in sorted(P, key=lambda p: -p["DB"])], "gruende", "verteilung der positionen je partei, summe 100 % · beschriftet ab 6 %")

# --- 7: Länder (Kernaussage 7) ---
def c7():
    ls = sorted(L, key=lambda l: -l["DB"]); f, ax = fig(3.2, left=0.26, bottom=0.18)
    ys = range(len(ls))[::-1]
    for y, l in zip(ys, ls):
        col = Y if l["stadtstaat"] else S
        ax.barh(y, l["DB"], height=0.62, color=col, linewidth=0)
        ax.text(l["DB"] + 0.7, y, f'{de(l["DB"])} %', va="center", fontsize=10.5, color=S, fontproperties=SCHRIFT[700 if col == Y else 500])
    ax.axvline(D["DB"], color=S, lw=1, ls=(0, (3, 3)))
    ax.text(D["DB"] + 0.6, -0.75, f'alle 48: {de(D["DB"])} %', fontsize=9.5, color=G, fontproperties=SCHRIFT[400])
    ylabels(ax, ys, [l["name"] for l in ls]); ax.set_xlim(0, 80); ax.set_ylim(-1.1, len(ls) - 0.4); nackt(ax)
    fertig(f, ax, "landeshebel je land, alle sechs programme zusammengerechnet · gelb: stadtstaaten", "laender")

# --- 8: Offenlassen und Bund je Land (Kernaussage 8) ---
def c8():
    ls = sorted(L, key=lambda l: l["Up"]); f, ax = fig(3.4, left=0.26, bottom=0.18)
    ys = range(len(ls))[::-1]
    for y, l in zip(ys, ls):
        ax.barh(y + 0.19, l["Up"], height=0.34, color=Y, linewidth=0); ax.barh(y - 0.19, l["Fp"], height=0.34, color=S, linewidth=0)
        ax.text(l["Up"] + 0.5, y + 0.19, f'{de(l["Up"])} %', va="center", fontsize=9.5, color=S, fontproperties=SCHRIFT[700])
        ax.text(l["Fp"] + 0.5, y - 0.19, f'{de(l["Fp"])} %', va="center", fontsize=9.5, color=G, fontproperties=SCHRIFT[400])
    ylabels(ax, ys, [l["name"] for l in ls]); ax.set_xlim(0, 36); ax.set_ylim(-0.7, len(ls)); nackt(ax)
    ax.text(0.5, len(ls) - 0.35, "gelb: unbestimmt (u)   schwarz: bund / eu (f)", fontsize=9.5, color=G, fontproperties=SCHRIFT[400])
    fertig(f, ax, "anteil je land, sortiert nach dem gelben balken · beim bund liegen alle zwischen 9 und 13 %", "offen")

# --- 9: Spannweite je Land (Kernaussage 9) ---
def c9():
    ls = sorted(L, key=lambda l: -(l["max"] - l["min"])); f, ax = fig(3.6, left=0.26, right=0.98, bottom=0.16)
    ys = range(len(ls))[::-1]
    for y, l in zip(ys, ls):
        rs = sorted([r for r in rows if r["land"] == l["name"]], key=lambda r: r["DB"]); lo, hi = rs[0], rs[-1]
        col = Y if l is ls[0] else S
        ax.plot([lo["DB"], hi["DB"]], [y, y], color=col, lw=3, solid_capstyle="round", zorder=2)
        ax.scatter([r["DB"] for r in rs], [y] * len(rs), s=30, color=col, zorder=3, linewidths=0)
        ax.text(lo["DB"] - 0.8, y, lo["partei"], ha="right", va="center", fontsize=9.5, color=G, fontproperties=SCHRIFT[400])
        ax.text(hi["DB"] + 0.8, y, f'{hi["partei"]} · {de(hi["DB"] - lo["DB"])} punkte', ha="left", va="center", fontsize=9.5, color=S if col == Y else G, fontproperties=SCHRIFT[700 if col == Y else 400])
    ylabels(ax, ys, [l["name"] for l in ls]); ax.set_xlim(30, 100); ax.set_ylim(-0.7, len(ls) - 0.3); nackt(ax)
    fertig(f, ax, "jeder punkt ein programm · linie von niedrigstem zu höchstem programm des landes · gelb: größte spannweite", "spannweite")

if __name__ == "__main__":
    for fn in (c1, c2, c3, c4, c5, c6, c7, c8, c9): fn()
    print("9 charts erzeugt (004-*.de.svg)")
