"""Vorschaubild (Open Graph, 1200 × 630) für № 04 im Plakatstil der Rubrik gesellschaft: gelbe Fläche, rotes Dreieck, schwarzer Balken, Titel in Jost.
Ausgabe: ../og/004-versprochen.png. Einzige Rasterdatei der Seite; nur für Linkvorschauen (Social Media, Messenger)."""
import os
import theme
from theme import FARBEN, SCHRIFT
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, '..', 'og'); os.makedirs(OUT, exist_ok=True)
f = plt.figure(figsize=(12, 6.3), dpi=100); ax = f.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1200); ax.set_ylim(0, 630); ax.axis('off')
ax.add_patch(Rectangle((0, 0), 1200, 630, color=FARBEN['gelb'], lw=0))
ax.add_patch(Rectangle((0, 616), 1200, 14, color=FARBEN['schwarz'], lw=0))
ax.add_patch(Polygon([(830, -20), (1250, -20), (1040, 520)], closed=True, color=FARBEN['rot'], lw=0))
ax.add_patch(Rectangle((60, 500), 44, 44, color=FARBEN['schwarz'], lw=0))
ax.text(60, 470, 'nr. 04 · gesellschaft · landtagswahlen', fontsize=17, color=FARBEN['schwarz'], fontproperties=SCHRIFT[500], va='top')
ax.text(60, 400, 'VERSPROCHEN: JA.\nZUSTÄNDIG: JEIN.', fontsize=58, color=FARBEN['schwarz'], fontproperties=SCHRIFT[700], va='top', linespacing=1.0)
ax.text(60, 170, '48 Wahlprogramme, 28.071 Versprechen, eine Frage:\nDarf das Land das überhaupt entscheiden?', fontsize=21, color=FARBEN['schwarz'], fontproperties=SCHRIFT[400], va='top', linespacing=1.35)
ax.text(60, 40, 'a xandir, dissected · dissected.eu', fontsize=15, color=FARBEN['schwarz'], fontproperties=SCHRIFT[500], va='bottom')
f.savefig(os.path.join(OUT, '004-versprochen.png'), dpi=100, facecolor=FARBEN['gelb']); plt.close(f)
print('og/004-versprochen.png erzeugt')
