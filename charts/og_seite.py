"""Vorschaubild (Open Graph, 1200 × 630) für die Seite selbst: Startseite, Archiv, Über, Impressum, Datenschutz.
Weißer Grund, schwarzer Balken, die drei Rubrikzeichen (gelber Kreis, rotes Dreieck, blaues Quadrat), Marke und Claim.
Ausgabe: ../og/dissected.<sprache>.png. Nur für Linkvorschauen (Social Media, Messenger). Aufruf aus charts/: python og_seite.py"""
import os
from theme import FARBEN, SCHRIFT
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon

H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, '..', 'og'); os.makedirs(OUT, exist_ok=True)
WEISS = '#ffffff'
TEXTBREITE = 740  # px; rechts davon beginnt die Komposition
BILDER = [
    # datei, kopfzeile, claim (3 zeilen)
    ('dissected.de.png', 'analysen zu sport, gesellschaft und welt',
     'Unabhängig und datenbasiert,\nmit Quellen, Methode und Konfidenz.\nOhne Werbung, ohne Tracking.'),
    ('dissected.en.png', 'analyses of sport, society and the world',
     'Independent and data-driven,\nwith sources, method and confidence.\nNo ads, no tracking.'),
]
for datei, kopf, claim in BILDER:
    f = plt.figure(figsize=(12, 6.3), dpi=100); ax = f.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1200); ax.set_ylim(0, 630); ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 1200, 630, color=WEISS, lw=0))
    ax.add_patch(Rectangle((0, 616), 1200, 14, color=FARBEN['schwarz'], lw=0))
    # Komposition rechts: großer gelber Kreis (angeschnitten), kleines blaues Quadrat, rotes Dreieck davor
    ax.add_patch(Circle((1060, 330), 240, color=FARBEN['gelb'], lw=0))
    ax.add_patch(Rectangle((760, 480), 100, 100, color=FARBEN['blau'], lw=0))
    ax.add_patch(Polygon([(980, 40), (1200, 40), (1090, 230)], closed=True, color=FARBEN['rot'], lw=0))
    # Textblock links: Marke oben, Kopfzeile, Name in einer Zeile (so groß, wie die Textbreite erlaubt), Claim, Adresse
    ax.add_patch(Rectangle((60, 500), 44, 44, color=FARBEN['schwarz'], lw=0))
    ax.text(60, 470, kopf, fontsize=17, color=FARBEN['grau'], fontproperties=SCHRIFT[500], va='top')
    name = ax.text(60, 405, 'a xandir, dissected', fontsize=56, color=FARBEN['schwarz'], fontproperties=SCHRIFT[700], va='top')
    f.canvas.draw()
    while name.get_window_extent(f.canvas.get_renderer()).width > TEXTBREITE - 60 and name.get_fontsize() > 30:
        name.set_fontsize(name.get_fontsize() - 1)
    ax.text(60, 290, claim, fontsize=21, color=FARBEN['schwarz'], fontproperties=SCHRIFT[400], va='top', linespacing=1.3)
    ax.text(60, 36, 'dissected.eu', fontsize=15, color=FARBEN['grau'], fontproperties=SCHRIFT[500], va='bottom')
    f.savefig(os.path.join(OUT, datei), dpi=100, facecolor=WEISS); plt.close(f)
    print('og/' + datei, 'erzeugt, Schriftgröße Name', name.get_fontsize())
