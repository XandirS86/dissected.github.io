"""Charts fuer / for no. 04 - Versprochen: ja. Zuständig: jein. (Landeshebel der Wahlprogramme, AURYN Teil 1).
Daten: 004-daten.json (DATA-Objekt des Dashboards, Stand 56c, 17.10.2026). Regeln: theme.py / DESIGN.md.
Farblogik seit 18.10.2026 wie in den interaktiven Grafiken der Seite: Gelb = Landeshebel (D voll, B schraffiert),
Schwarz = Bund / EU, Grau = Kommunen, Hellgrau = Selbstverwaltung / Dritte, gerastert = unbestimmt. Gelb ist nie Hervorhebung."""
import json, os
import theme
from theme import FARBEN, SCHRIFT
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

S, Y, G, GH, W = FARBEN["schwarz"], FARBEN["gelb"], FARBEN["grau"], FARBEN["grauhell"], "#ffffff"
plt.rcParams["hatch.linewidth"] = 1.1
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
# Balkenstil je Code: (Füllung, Kantenfarbe, Schraffur); Textfarbe auf dem Balken
STIL = {"D": (Y, Y, None), "B": (Y, S, "////"), "F": (S, S, None), "K": (G, G, None), "S": (GH, GH, None), "U": (W, GH, "...."), "KS": (G, G, None)}
TEXT = {"D": S, "B": S, "F": W, "K": W, "S": S, "U": S, "KS": W}
def balken(ax, y, v, left, code, height=0.6, sep=True):
    fill, edge, hatch = STIL[code]
    ax.barh(y, v, left=left, height=height, color=fill, edgecolor=edge, hatch=hatch, linewidth=0.8 if code == "U" else 0)
    if sep and code != "U":  # weiße Trennkante wie in der interaktiven Grafik; U behält seine graue Kontur
        ax.barh(y, v, left=left, height=height, color="none", edgecolor=W, linewidth=1.2)
LEGENDE = ("gelb: landeshebel d + b (schraffiert: land mit anderen) · schwarz: bund / eu", "grau: kommunen, dritte · gerastert: unbestimmt, kein weg benannt")

# --- 1: der eine Balken (Kernaussage 1) ---
def c1():
    f, ax = fig(2.1, left=0.02, right=0.98, bottom=0.30, top=0.80)
    x = 0
    for c, l in CODES:
        v = D["totp"][c]
        balken(ax, 0, v, x, c)
        if v >= 4:
            ax.text(x + v / 2, 0, f"{de(v)} %", ha="center", va="center", fontsize=10.5, color=TEXT[c],
                    fontproperties=SCHRIFT[700 if c in ("D", "B") else 500], bbox=dict(boxstyle="square,pad=0.15", fc=W, ec="none", alpha=0.85) if c in ("B", "U") else None)
        x += v
    db = D["DB"]
    ax.plot([0, db], [0.55, 0.55], color=S, lw=2); ax.plot([0, 0], [0.5, 0.6], color=S, lw=2); ax.plot([db, db], [0.5, 0.6], color=S, lw=2)
    ax.text(db / 2, 0.72, f"landeshebel d + b: {de(db)} %", ha="center", va="bottom", fontsize=11, color=S, fontproperties=SCHRIFT[700])
    ax.text((db + 100) / 2, 0.72, f"nicht allein einlösbar: {de(100 - db)} %", ha="center", va="bottom", fontsize=11, color=G, fontproperties=SCHRIFT[500])
    ax.set_xlim(0, 100); ax.set_ylim(-0.6, 1.1); nackt(ax, links=False); ax.set_yticks([])
    fertig(f, ax, "alle 28.071 positionen der 48 programme · gelb: landeshebel (schraffiert: mit anderen) · gerastert: kein weg", "hebel")

# --- 2: die vier Adressaten außerhalb des Hebels (Kernaussage 2) ---
def c2():
    items = [("U", "unbestimmt, kein weg benannt"), ("F", "bund / eu"), ("K", "kommunen"), ("S", "selbstverwaltung / dritte")]
    f, ax = fig(2.6, left=0.38, bottom=0.18)
    ys = range(len(items))[::-1]
    for y, (c, l) in zip(ys, items):
        v = D["totp"][c]
        balken(ax, y, v, 0, c, sep=False)
        ax.text(v + 0.5, y, f"{de(v)} %", va="center", fontsize=10.5, color=S, fontproperties=SCHRIFT[500])
    ylabels(ax, ys, [l for _, l in items]); ax.set_xlim(0, 32); nackt(ax)
    fertig(f, ax, "die 39 % außerhalb des landeshebels, aufgeteilt nach adressat · anteil an allen 28.071 positionen", "adressat")

# --- 3: Streudiagramm U-Anteil gegen Hebel (Kernaussage 3) ---
def c3():
    f, ax = fig(3.4, left=0.12, bottom=0.18, top=0.95)
    xs = [r["Up"] for r in rows]; ys = [r["DB"] for r in rows]
    ax.scatter(xs, ys, s=34, color=S, zorder=3, linewidths=0)
    m, b = D["ols"]; ax.plot([14, 42], [m * 14 + b, m * 42 + b], color=GH, lw=2, ls=(0, (4, 3)), zorder=2)
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
def hebelbalken(items, name, fuss, left):
    f, ax = fig(3.0 if len(items) < 8 else 3.2, left=left, bottom=0.18)
    ys = range(len(items))[::-1]
    for y, it in zip(ys, items):
        ax.barh(y, it["DB"], height=0.62, color=Y, linewidth=0)
        ax.text(it["DB"] + 0.7, y, f'{de(it["DB"])} %', va="center", fontsize=10.5, color=S, fontproperties=SCHRIFT[500])
    ax.axvline(D["DB"], color=S, lw=1, ls=(0, (3, 3)))
    ax.text(D["DB"] + 0.6, -0.75, f'alle 48: {de(D["DB"])} %', fontsize=9.5, color=G, fontproperties=SCHRIFT[400])
    ylabels(ax, ys, [it["name"] for it in items]); ax.set_xlim(0, 80); ax.set_ylim(-1.1, len(items) - 0.4); nackt(ax)
    fertig(f, ax, fuss, name)
def c4(): hebelbalken(sorted(P, key=lambda p: -p["DB"]), "parteien", "landeshebel je partei, alle acht programme zusammengerechnet · gelb: landeshebel d + b · gestrichelt: alle 48", 0.14)

# --- 5: Matrix Land × Partei (Kernaussage 5) ---
def mix(t):  # weiß → gelb, wie die Gelbstufen der interaktiven Matrix
    a, b = (255, 251, 224), (242, 194, 0); k = 0.25 + 0.75 * t
    return "#%02x%02x%02x" % tuple(round(a[i] + (b[i] - a[i]) * k) for i in range(3))
def c5():
    lands = [l["name"] for l in sorted(L, key=lambda l: -l["DB"])]; parts = ["SPD", "Grüne", "CDU", "AfD", "Linke", "BSW"]
    vals = [r["DB"] for r in rows]; lo, hi = min(vals), max(vals)
    f, ax = fig(3.8, left=0.22, right=0.99, bottom=0.12, top=0.90)
    for i, land in enumerate(lands):
        rs = sorted([r for r in rows if r["land"] == land], key=lambda r: -r["DB"])
        for j, pn in enumerate(parts):
            r = next(x for x in rs if x["partei"] == pn); rank = rs.index(r) + 1
            y = len(lands) - 1 - i
            ax.add_patch(plt.Rectangle((j - 0.47, y - 0.47), 0.94, 0.94, color=mix((r["DB"] - lo) / (hi - lo)), lw=0))
            ax.text(j, y, de(r["DB"]), ha="center", va="center", fontsize=10.5, color=S if rank != 6 else G,
                    fontproperties=SCHRIFT[700 if rank == 1 else 400])
    for j, pn in enumerate(parts): ax.text(j, len(lands) - 0.35, pn, ha="center", va="bottom", fontsize=10, color=S, fontproperties=SCHRIFT[500])
    ylabels(ax, range(len(lands))[::-1], lands, 400); ax.set_xlim(-0.5, len(parts) - 0.5); ax.set_ylim(-0.5, len(lands) + 0.3)
    nackt(ax, links=False); ax.tick_params(left=False)
    fertig(f, ax, "landeshebel in % je programm · kräftigeres gelb: höherer hebel · fett: rang 1 im land, grau: rang 6", "matrix")

# --- 6 und 8: Stapel je Partei / je Land ---
def stapel(items, name, fuss, left=0.14):
    f, ax = fig(3.0, left=left, right=0.98, bottom=0.18)
    ys = range(len(items))[::-1]
    for y, it in zip(ys, items):
        x = 0
        for key, code in (("Dp", "D"), ("Bp", "B"), ("Fp", "F"), ("KSp", "KS"), ("Up", "U")):
            v = it[key]
            balken(ax, y, v, x, code, height=0.62)
            if v >= 6:
                ax.text(x + v / 2, y, de(v, 0), ha="center", va="center", fontsize=9.5, color=TEXT[code], fontproperties=SCHRIFT[500],
                        bbox=dict(boxstyle="square,pad=0.12", fc=W, ec="none", alpha=0.85) if code in ("B", "U") else None)
            x += v
    ylabels(ax, ys, [it["name"] for it in items]); ax.set_xlim(0, 100); nackt(ax)
    ax.text(0, len(items) + 0.15, LEGENDE[0], fontsize=9, color=G, fontproperties=SCHRIFT[400])
    ax.text(0, len(items) - 0.3, LEGENDE[1], fontsize=9, color=G, fontproperties=SCHRIFT[400])
    ax.set_ylim(-0.6, len(items) + 0.65)
    fertig(f, ax, fuss, name)

def anteile(g): return dict(name=g["name"], Dp=g["Dp"], Bp=g["Bp"], Fp=g["Fp"], KSp=g["Kp"] + g["Sp"], Up=g["Up"])
def c6(): stapel([anteile(p) for p in sorted(P, key=lambda p: -p["DB"])], "gruende", "verteilung der positionen je partei, summe 100 % · beschriftet ab 6 %")

# --- 7: Länder (Kernaussage 7) ---
def c7(): hebelbalken(sorted(L, key=lambda l: -l["DB"]), "laender", "landeshebel je land, alle programme zusammengerechnet · gelb: landeshebel d + b · gestrichelt: alle 48", 0.26)

# --- 8: Verteilung je Land, sortiert nach dem Anteil unbestimmt (Kernaussage 8) ---
def c8(): stapel([anteile(l) for l in sorted(L, key=lambda l: l["Up"])], "offen", "verteilung je land, summe 100 % · sortiert nach dem anteil unbestimmt · beschriftet ab 6 %", left=0.26)

# --- 9: Spannweite je Land (Kernaussage 9) ---
def c9():
    ls = sorted(L, key=lambda l: -(l["max"] - l["min"])); f, ax = fig(3.6, left=0.26, right=0.98, bottom=0.16)
    ys = range(len(ls))[::-1]
    for y, l in zip(ys, ls):
        rs = sorted([r for r in rows if r["land"] == l["name"]], key=lambda r: r["DB"]); lo, hi = rs[0], rs[-1]
        ax.plot([lo["DB"], hi["DB"]], [y, y], color=Y, lw=6, solid_capstyle="round", zorder=2)
        ax.scatter([r["DB"] for r in rs], [y] * len(rs), s=30, color=S, zorder=3, linewidths=0)
        ax.text(lo["DB"] - 0.8, y, lo["partei"], ha="right", va="center", fontsize=9.5, color=G, fontproperties=SCHRIFT[400])
        ax.text(hi["DB"] + 0.8, y, f'{hi["partei"]} · {de(hi["DB"] - lo["DB"])} punkte', ha="left", va="center", fontsize=9.5, color=G, fontproperties=SCHRIFT[400])
    ylabels(ax, ys, [l["name"] for l in ls]); ax.set_xlim(30, 100); ax.set_ylim(-0.7, len(ls) - 0.3); nackt(ax)
    fertig(f, ax, "jeder punkt ein programm · gelbes band: niedrigstes bis höchstes programm des landes", "spannweite")

if __name__ == "__main__":
    for fn in (c1, c2, c3, c4, c5, c6, c7, c8, c9): fn()
    print("9 charts erzeugt (004-*.de.svg)")
