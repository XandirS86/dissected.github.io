"""
Chart-Theme für alwy schley — analysen.
Erzeugt SVG-Diagramme im Stil der Seite: schwarz, ein Akzent, nur Nullinie, Werte am Balken.

Nutzung (Python 3, matplotlib):
    from theme import balken, linie
    balken(["15/16","16/17","17/18"], [41,39,37],
           hervor=-1,                       # Index des hervorgehobenen Werts (-1 = letzter)
           akzent="rot",                    # rot | blau | gelb
           fussnote="anteil zentraler pässe in %",
           anmerkung=(1, "tiefpunkt"),      # optional: (index, text)
           out="001-beispiel.svg")

Beide Funktionen schreiben ein SVG mit 640 × 300 px, das im Artikel per
<img src="../../charts/DATEI.svg"> eingebunden wird. Nichts von Hand nachbearbeiten.

Sprachen: Pro Sprache ein Aufruf mit übersetzten Labels/Fußnote und Sprachkürzel im Namen:
    001-titel.de.svg  ·  001-title.en.svg  ·  später 001-titre.fr.svg
Werte und Farben bleiben identisch, nur der Text wechselt.
"""
import os, glob
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams, font_manager

# Jost liegt als TTF neben diesem Skript (charts/ttf/). Text wird in Pfade gewandelt,
# damit das SVG überall gleich aussieht – auch als <img> eingebunden.
_TTF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ttf")
for _f in glob.glob(os.path.join(_TTF, "*.ttf")):
    font_manager.fontManager.addfont(_f)
SCHRIFT = {w: font_manager.FontProperties(fname=os.path.join(_TTF, f)) for w, f in
           ((400, "Jost-400-Book.ttf"), (500, "Jost-500-Medium.ttf"), (700, "Jost-700-Bold.ttf"))}

FARBEN = {"rot": "#d7261e", "blau": "#1b4fa0", "gelb": "#f2c200",
          "schwarz": "#111111", "grau": "#5c5c5c", "grauhell": "#9a9a9a"}

rcParams.update({
    "font.family": "Jost*",
    "font.size": 10.5,
    "svg.fonttype": "path",        # Text als Pfade: unabhängig von installierten Schriften
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
    "axes.spines.bottom": True, "axes.edgecolor": FARBEN["schwarz"], "axes.linewidth": 2,
    "xtick.color": FARBEN["grau"], "ytick.color": FARBEN["grau"],
    "xtick.major.size": 0, "ytick.major.size": 0,
    "axes.grid": False, "figure.dpi": 100,
})

def _fig():
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    fig.subplots_adjust(left=0.06, right=0.98, top=0.88, bottom=0.2)
    return fig, ax

def _abschluss(fig, ax, fussnote, out):
    ax.set_yticks([])
    for lab in ax.get_xticklabels():
        lab.set_color(FARBEN["grau"]); lab.set_fontproperties(SCHRIFT[400]); lab.set_fontsize(10)
    if fussnote:
        fig.text(0.06, 0.04, fussnote, color=FARBEN["grau"], fontsize=10, fontproperties=SCHRIFT[400])
    fig.savefig(out, format="svg", bbox_inches=None, transparent=True)
    plt.close(fig)
    return out

def balken(labels, werte, hervor=-1, akzent="rot", fussnote="", anmerkung=None,
           einheit="", dezimal=0, out="chart.svg"):
    fig, ax = _fig()
    n = len(werte)
    farben = [FARBEN["schwarz"]] * n
    if hervor is not None:
        farben[hervor % n] = FARBEN[akzent]
    ax.bar(range(n), werte, width=0.66, color=farben, linewidth=0)
    ax.set_xticks(range(n)); ax.set_xticklabels(labels)
    ax.set_ylim(0, max(werte) * 1.18)
    for i, w in enumerate(werte):
        txt = f"{w:.{dezimal}f}".replace(".", ",") + einheit
        ist_hervor = hervor is not None and i == hervor % n
        ax.text(i, w + max(werte) * 0.02, txt, ha="center", va="bottom", fontsize=10.5,
                color=FARBEN[akzent] if ist_hervor else FARBEN["schwarz"],
                fontproperties=SCHRIFT[700 if ist_hervor else 500])
    if anmerkung:
        i, text = anmerkung
        ax.plot([i, i], [werte[i] + max(werte) * 0.13, max(werte) * 1.16],
                color=FARBEN[akzent], lw=1, ls=(0, (3, 3)))
        ax.text(i + 0.15, max(werte) * 1.14, text, color=FARBEN["grau"], fontsize=10, va="top", fontproperties=SCHRIFT[400])
    ax.tick_params(axis="x", pad=8)
    return _abschluss(fig, ax, fussnote, out)

def linie(labels, reihen, akzent="rot", fussnote="", out="chart.svg", dezimal=0, einheit=""):
    """reihen: dict name -> werte. Die erste Reihe ist schwarz, die zweite im Akzent, weitere grau."""
    fig, ax = _fig()
    palette = [FARBEN["schwarz"], FARBEN[akzent], FARBEN["grauhell"], FARBEN["grau"]]
    for k, (name, werte) in enumerate(reihen.items()):
        c = palette[k % len(palette)]
        ax.plot(range(len(werte)), werte, color=c, lw=2.5, solid_capstyle="round")
        ax.text(len(werte) - 1 + 0.15, werte[-1], f"{name}  {werte[-1]:.{dezimal}f}{einheit}".replace(".", ","),
                color=c, va="center", fontsize=10.5, fontproperties=SCHRIFT[500])
    ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels)
    ax.set_xlim(-0.3, len(labels) - 1 + 2.2)
    lo = min(min(v) for v in reihen.values()); hi = max(max(v) for v in reihen.values())
    ax.set_ylim(lo - (hi - lo) * 0.25, hi + (hi - lo) * 0.25)
    ax.tick_params(axis="x", pad=8)
    return _abschluss(fig, ax, fussnote, out)

if __name__ == "__main__":
    balken(["15/16","16/17","17/18","18/19","19/20","20/21","21/22","22/23","23/24","24/25","25/26"],
           [41,39,37,36,35,36,38,40,42,43,44], hervor=-1, akzent="rot",
           anmerkung=(4, "tiefpunkt 2019/20"),
           fussnote="anteil zentraler pässe in %, alle 18 vereine (beispieldaten)",
           out="001-beispiel.svg")
    linie(["2019","2020","2021","2022","2023","2024","2025"],
          {"gymnasium": [2.31,2.28,2.24,2.19,2.15,2.12,2.10], "gesamtschule": [2.62,2.58,2.55,2.50,2.47,2.44,2.41]},
          akzent="blau", dezimal=2, fussnote="abiturdurchschnitt (beispieldaten)", out="beispiel-linie.svg")
    print("charts erzeugt")
