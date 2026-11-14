# -*- coding: utf-8 -*-
"""Erzeugt sitemap.xml aus den Seiten: Canonical und hreflang aus den Köpfen, lastmod aus dem letzten Commit
der Datei, Seiten mit noindex ausgeschlossen. Schreibt nur, wenn sich etwas ändert.
Aufruf: python werkzeug/sitemap_bauen.py [--pruefen]  (--pruefen: nur vergleichen, Exit 1 bei Abweichung)"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seite as S

KOMMENTAR = '<!-- Wird von werkzeug/sitemap_bauen.py aus den Seiten erzeugt (Canonical, hreflang, lastmod = letzter Commit der Datei). Nicht von Hand pflegen. -->'

def gewicht(p):
    name = p.split('/')[-1]
    if name == 'index.html': return 0, '1.0'
    if name in ('archiv.html', 'archive.html'): return 1, '0.7'
    if name in ('ueber.html', 'about.html'): return 2, '0.6'
    if name in ('impressum.html', 'legal.html'): return 3, '0.2'
    if name in ('datenschutz.html', 'privacy.html'): return 4, '0.2'
    if '/analysen/' in p or '/analyses/' in p: return 5, '0.9'
    return 6, '0.5'

def nummer(p):
    m = re.search(r'/(\d{3})-', p)
    return int(m.group(1)) if m else 999

def bauen():
    seiten = []
    for p in S.alle_seiten():
        k = S.kopf(S.lesen(p))
        if S.indexierbar(p, k):
            seiten.append((p, k))
    seiten.sort(key=lambda pk: (gewicht(pk[0])[0], nummer(pk[0]), 0 if pk[0].startswith('de/') else 1, pk[0]))
    zeilen = ['<?xml version="1.0" encoding="UTF-8"?>', KOMMENTAR,
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for p, k in seiten:
        zeilen += ['  <url>', f'    <loc>{k["canonical"]}</loc>', f'    <lastmod>{S.git_datum(p)}</lastmod>',
                   f'    <priority>{gewicht(p)[1]}</priority>']
        reihenfolge = sorted(k['hreflang'].items(), key=lambda kv: {'de': 0, 'en': 1, 'x-default': 9}.get(kv[0], 5))
        for lang, url in reihenfolge:
            zeilen.append(f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{url}"/>')
        zeilen.append('  </url>')
    zeilen.append('</urlset>')
    return '\n'.join(zeilen) + '\n', len(seiten)

if __name__ == '__main__':
    text, n = bauen()
    alt = S.lesen('sitemap.xml') if os.path.exists(S.voll('sitemap.xml')) else ''
    if '--pruefen' in sys.argv:
        if alt == text:
            print(f'sitemap.xml aktuell ({n} Seiten)'); sys.exit(0)
        print('sitemap.xml weicht vom erzeugten Stand ab'); sys.exit(1)
    if S.schreiben('sitemap.xml', text):
        print(f'sitemap.xml neu geschrieben ({n} Seiten)')
    else:
        print(f'sitemap.xml unverändert ({n} Seiten)')
