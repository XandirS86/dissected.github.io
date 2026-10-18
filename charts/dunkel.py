"""Dunkle Zwillinge der statischen Grafiken (Dunkelmodus, 18.10.2026): übersetzt jede *.svg nach einer festen Farbtabelle
in *.dunkel.svg. Das Schalter-Skript der Seiten tauscht die Bildquelle (Attribut data-dunkel). Zeichnet nichts neu.
Farbtabelle = Spiegelung der Helligkeit: Schwarz → Textgrau des Dunkelmodus, Grautöne gestuft, Weiß → Grund, Blau und Rot
aufgehellt, Gelb bleibt. Unbekannte Farben werden gemeldet und unverändert gelassen."""
import glob, os, re, sys
H = os.path.dirname(os.path.abspath(__file__))
TABELLE = {
    '#111111': '#c4c4c4', '#141414': '#c4c4c4',   # Text, Balken, Achsen
    '#5c5c5c': '#9a9a9a', '#6b6b6b': '#8f8f8f', '#9a9a9a': '#777777', '#8c8c8c': '#8c8c8c',
    '#b9b9b9': '#555555', '#c8c8c8': '#4a4a4a', '#d0d0d0': '#3f3f3f', '#dddddd': '#333333',
    '#faf8f3': '#1e1e1e', '#ffffff': '#161616',   # Flächen und Lichthöfe → Grund
    '#1b4fa0': '#86aefc', '#e3000b': '#ff6a5e', '#d7261e': '#ff6a5e',
}
unbekannt = {}
n = 0
for f in sorted(glob.glob(os.path.join(H, '*.svg'))):
    if f.endswith('.dunkel.svg'):
        continue
    t = open(f, encoding='utf-8').read()
    def ersatz(m):
        c = m.group(0).lower()
        if c in TABELLE:
            return TABELLE[c]
        if c.startswith('#f') and c[3] in 'cd':   # Gelb-Rampe (#f2c200 … #f7d959) bleibt
            return c
        unbekannt.setdefault(c, set()).add(os.path.basename(f)); return c
    neu = re.sub(r'#[0-9a-fA-F]{6}\b', ersatz, t)
    out = f[:-4] + '.dunkel.svg'
    open(out, 'w', encoding='utf-8').write(neu); n += 1
print(n, 'dunkle Zwillinge geschrieben')
for c, fs in sorted(unbekannt.items()):
    print('unbekannt, unverändert:', c, sorted(fs))
