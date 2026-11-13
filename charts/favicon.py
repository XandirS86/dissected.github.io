"""Favicon-Satz für a xandir, dissected: roter Kreis, von einem Schnitt zerlegt (wie favicon.svg).
Ausgabe (Wurzel der Seite): favicon.ico (16/32/48), favicon-96.png, apple-touch-icon.png (180, weißer Grund).
Nur Pillow nötig. Nach Änderung der Marke: Skript laufen lassen, favicon.svg von Hand angleichen."""
import os
import numpy as np
from PIL import Image, ImageDraw

H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, '..')
ROT = (215, 38, 30, 255)
S = 1024  # Zeichenfläche, wird verkleinert (weiche Kanten)

def marke(grund):
    """Kreis cx=40 cy=28 r=28, Schnitt y=29..35 um -12° gedreht, im Raster 64 → S."""
    k = S / 64
    bild = Image.new('RGBA', (S, S), grund)
    z = ImageDraw.Draw(bild)
    z.ellipse([(40 - 28) * k, (28 - 28) * k, (40 + 28) * k, (28 + 28) * k], fill=ROT)
    schnitt = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(schnitt).rectangle([-20 * k, 29 * k, 84 * k, 35 * k], fill=(255, 255, 255, 255))
    schnitt = schnitt.rotate(12, center=(32 * k, 32 * k), resample=Image.BICUBIC)
    # Schnitt in Grundfarbe über den Kreis legen (bei durchsichtigem Grund: ausstanzen)
    if grund[3] == 0:
        alpha = bild.getchannel('A')
        maske = Image.eval(schnitt.getchannel('A'), lambda a: 255 - a)
        bild.putalpha(Image.fromarray(np.minimum(np.array(alpha), np.array(maske))))
    else:
        farbe = Image.new('RGBA', (S, S), grund)
        bild = Image.composite(farbe, bild, schnitt.getchannel('A'))
    return bild

def klein(bild, n):
    return bild.resize((n, n), Image.LANCZOS)

durchsichtig = marke((0, 0, 0, 0))
weiss = marke((255, 255, 255, 255))
klein(durchsichtig, 96).save(os.path.join(OUT, 'favicon-96.png'), optimize=True)
klein(weiss, 180).save(os.path.join(OUT, 'apple-touch-icon.png'), optimize=True)
klein(durchsichtig, 256).save(os.path.join(OUT, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
print('favicon-96.png, apple-touch-icon.png, favicon.ico erzeugt')
