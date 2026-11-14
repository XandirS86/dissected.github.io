"""Vorschaubild (Open Graph, 1200 × 630) für № 06 im Plakatstil der Rubrik sport, Komposition B:
blaue Fläche, großer gelber Kreis rechts oben angeschnitten, kleiner gelber Kreis links unten, dünne schwarze Verbindung.
Liegt im Repo unter charts/ (wie 004_vorschau.py, 005_vorschau.py) und wird von dort gestartet, weil theme.py importiert wird:
    cd charts && python 006_vorschau.py
Ausgabe: ../og/006-rueckkauf.png. Nur für Linkvorschauen."""
import os
import theme  # noqa: F401  (setzt die Schrift Jost)
from theme import FARBEN, SCHRIFT
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

H = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(H, '..', 'og')
os.makedirs(OUT, exist_ok=True)
WEISS = '#ffffff'
flaeche = FARBEN['blau']
f = plt.figure(figsize=(12, 6.3), dpi=100)
ax = f.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1200)
ax.set_ylim(0, 630)
ax.axis('off')
ax.add_patch(Rectangle((0, 0), 1200, 630, color=flaeche, lw=0))
ax.add_patch(Rectangle((0, 616), 1200, 14, color=FARBEN['schwarz'], lw=0))
# Komposition B
ax.add_patch(Circle((1040, 520), 230, color=FARBEN['gelb'], lw=0))
ax.add_patch(Circle((150, 110), 46, color=FARBEN['gelb'], lw=0))
ax.add_patch(Rectangle((150, 108), 890, 4, color=FARBEN['schwarz'], lw=0))
ax.add_patch(Rectangle((1038, 110), 4, 410, color=FARBEN['schwarz'], lw=0))
# Text
ax.text(60, 560, 'nr. 06 · sport · fußball · im entwurf · nachtrag zu nr. 01', fontsize=17, color=WEISS, fontproperties=SCHRIFT[500], va='top')
ax.text(60, 525, 'DER\nRÜCKKAUF', fontsize=60, color=WEISS, fontproperties=SCHRIFT[700], va='top', linespacing=1.0)
# Sätze des Autors aus dem Lead, keine eigene Zusammenfassung (Entscheidung 14.11.2026)
ax.text(60, 290, 'Sturz der FIFA! Ahh nein, doch nicht; alles beim Alten…\nUnd der Aufstand vom August? Niedergeschlagen!\n25 Millionen Dollar je Verband, ohne Bedingung.',
        fontsize=20, color=WEISS, fontproperties=SCHRIFT[400], va='top', linespacing=1.35)
ax.text(60, 40, 'a xandir, dissected · dissected.eu', fontsize=15, color=WEISS, fontproperties=SCHRIFT[500], va='bottom')
f.savefig(os.path.join(OUT, '006-rueckkauf.png'), dpi=100, facecolor=flaeche)
plt.close(f)
print('og/006-rueckkauf.png erzeugt')
