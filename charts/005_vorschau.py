"""Vorschaubild (Open Graph, 1200 × 630) für № 05 im Plakatstil der Rubrik gesellschaft: gelbe Fläche, rotes Dreieck, schwarze Elemente, Titel in Jost.
Bild zu № 05: die Waage. Rotes Dreieck als Auflager, schwarzer Balken, zwei gleiche Gewichte, und sie steht trotzdem schief.
Ausgabe: ../og/005-graustufen.png. Nur für Linkvorschauen (Social Media, Messenger)."""
import math
import os
import theme
from theme import FARBEN, SCHRIFT
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, '..', 'og'); os.makedirs(OUT, exist_ok=True)
f = plt.figure(figsize=(12, 6.3), dpi=100); ax = f.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1200); ax.set_ylim(0, 630); ax.axis('off')
ax.add_patch(Rectangle((0, 0), 1200, 630, color=FARBEN['gelb'], lw=0))
ax.add_patch(Rectangle((0, 616), 1200, 14, color=FARBEN['schwarz'], lw=0))

PX, PY, WINKEL = 1010, 212, math.radians(8)          # Auflagepunkt (Spitze des Dreiecks), Neigung des Balkens


def gedreht(punkte):
    """Punkte im Koordinatensystem des Balkens (Ursprung = Auflagepunkt) in Bildkoordinaten."""
    c, s = math.cos(WINKEL), math.sin(WINKEL)
    return [(PX + x * c - y * s, PY + x * s + y * c) for x, y in punkte]


ax.add_patch(Polygon([(870, -20), (1150, -20), (PX, PY)], closed=True, color=FARBEN['rot'], lw=0))                 # Auflager
ax.add_patch(Polygon(gedreht([(-235, 0), (235, 0), (235, 36), (-235, 36)]), closed=True, color=FARBEN['schwarz'], lw=0))   # Balken
for mitte in (-165, 165):                                                                                         # zwei gleiche Gewichte
    ax.add_patch(Polygon(gedreht([(mitte - 32, 36), (mitte + 32, 36), (mitte + 32, 100), (mitte - 32, 100)]), closed=True, color=FARBEN['schwarz'], lw=0))

ax.text(60, 540, 'nr. 05 · gesellschaft · abtreibung', fontsize=17, color=FARBEN['schwarz'], fontproperties=SCHRIFT[500], va='top')
ax.text(60, 480, 'GRAUSTUFEN\nZWISCHEN GEWISSHEIT\nUND GEWISSHEIT', fontsize=46, color=FARBEN['schwarz'], fontproperties=SCHRIFT[700], va='top', linespacing=1.0)
ax.text(60, 190, 'Ab wann verdient werdendes Leben Schutz,\nund was heißt das für die Frau, die es trägt?', fontsize=21, color=FARBEN['schwarz'], fontproperties=SCHRIFT[400], va='top', linespacing=1.35)
ax.text(60, 40, 'a xandir, dissected · dissected.eu', fontsize=15, color=FARBEN['schwarz'], fontproperties=SCHRIFT[500], va='bottom')
f.savefig(os.path.join(OUT, '005-graustufen.png'), dpi=100, facecolor=FARBEN['gelb']); plt.close(f)
print('og/005-graustufen.png erzeugt')
