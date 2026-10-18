"""Vorschaubilder (Open Graph, 1200 × 630) für № 01–03 im Plakatstil der jeweiligen Rubrik (rubriken.css):
sport = blaue Fläche, gelber Kreis; welt = rote Fläche, blaues Quadrat; gesellschaft (№ 04) hat ein eigenes Skript (004_vorschau.py).
Ausgabe: ../og/<nr>-<kurz>.<sprache>.png. Nur für Linkvorschauen (Social Media, Messenger)."""
import os
import theme
from theme import FARBEN, SCHRIFT
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, '..', 'og'); os.makedirs(OUT, exist_ok=True)
WEISS = '#ffffff'
BILDER = [
    # datei, rubrik, kopfzeile, titel (2 zeilen), titelgröße, untertitel (2 zeilen)
    ('001-infantino.de.png', 'sport', 'nr. 01 · sport · fußball', 'DER FALL (DES)\nINFANTINO', 56,
     'Warum der mächtigste Mann des Weltfußballs nicht stürzt.\nEine Vermessung der FIFA auf der Mafia-Skala.'),
    ('001-infantino.en.png', 'sport', 'no. 01 · sport · football', 'THE CASE (AND FALL)\nOF INFANTINO', 50,
     'Why the most powerful man in world football does not fall.\nFIFA measured on the mafia scale.'),
    ('002-reparieren.de.png', 'welt', 'nr. 02 · welt · geoökonomie', 'REPARIEREN\nUNTER BESCHUSS', 56,
     'Warum Russlands Wirtschaft Überschuss meldet\nund zugleich um Benzin ansteht.'),
    ('003-halbe-million.de.png', 'sport', 'nr. 03 · sport · fußball', 'NE HALBE MILLION...\nWOFÜR GENAU?', 52,
     'DFB-Präsident Neuendorf: rund eine halbe Million Euro im Jahr.\nDreizehn Episoden, drei Ebenen, null Gegenstimmen.'),
    ('003-halbe-million.en.png', 'sport', 'no. 03 · sport · football', 'HALF A MILLION...\nFOR WHAT, EXACTLY?', 50,
     'DFB president Neuendorf: around half a million euros a year.\nThirteen episodes, three levels, zero dissenting votes.'),
]
for datei, rubrik, kopf, titel, groesse, unter in BILDER:
    flaeche = FARBEN['blau'] if rubrik == 'sport' else FARBEN['rot']
    f = plt.figure(figsize=(12, 6.3), dpi=100); ax = f.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1200); ax.set_ylim(0, 630); ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 1200, 630, color=flaeche, lw=0))
    ax.add_patch(Rectangle((0, 616), 1200, 14, color=FARBEN['schwarz'], lw=0))
    if rubrik == 'sport':
        ax.add_patch(Circle((1060, 250), 230, color=FARBEN['gelb'], lw=0))
    else:
        ax.add_patch(Rectangle((860, 40), 400, 400, color=FARBEN['blau'], lw=0))
    ax.add_patch(Rectangle((60, 500), 44, 44, color=WEISS, lw=0))
    ax.text(60, 470, kopf, fontsize=17, color=WEISS, fontproperties=SCHRIFT[500], va='top')
    ax.text(60, 400, titel, fontsize=groesse, color=WEISS, fontproperties=SCHRIFT[700], va='top', linespacing=1.0)
    ax.text(60, 170, unter, fontsize=21, color=WEISS, fontproperties=SCHRIFT[400], va='top', linespacing=1.35)
    ax.text(60, 40, 'a xandir, dissected · dissected.eu', fontsize=15, color=WEISS, fontproperties=SCHRIFT[500], va='bottom')
    f.savefig(os.path.join(OUT, datei), dpi=100, facecolor=flaeche); plt.close(f)
    print('og/' + datei, 'erzeugt')
