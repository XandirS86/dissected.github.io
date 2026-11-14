# -*- coding: utf-8 -*-
"""Meldet geänderte Seiten per IndexNow (Bing, Yandex u. a.). Der Schlüssel ist der Dateiname der
Schlüsseldatei im Wurzelverzeichnis (<schlüssel>.txt); Google kennt IndexNow nicht, dort zählt die Sitemap.
Aufruf: python werkzeug/indexnow.py --von <commit> --bis <commit> [--trocken]
Scheitert nie hart: Fehler werden gemeldet, Exit bleibt 0 (ein verpasster Ping ist kein Grund, eine Veröffentlichung zu stoppen)."""
import os, re, sys, json, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seite as S

def arg(name, standard=''):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv and sys.argv.index(name) + 1 < len(sys.argv) else standard

def schluessel():
    for name in os.listdir(S.WURZEL):
        if re.fullmatch(r'[0-9a-f]{32}\.txt', name):
            inhalt = open(S.voll(name), encoding='utf-8').read().strip()
            if inhalt == name[:-4]:
                return inhalt
    return None

von, bis, trocken = arg('--von'), arg('--bis', 'HEAD'), '--trocken' in sys.argv
dateien = S.geaenderte_dateien(von, bis)
urls = []
for p in dateien:
    if not p.endswith('.html') or not os.path.exists(S.voll(p)):
        continue
    k = S.kopf(S.lesen(p))
    if S.indexierbar(p, k):
        urls.append(k['canonical'])
if not urls:
    print('IndexNow: keine geänderten indexierbaren Seiten'); sys.exit(0)
key = schluessel()
if not key:
    print('IndexNow: keine Schlüsseldatei im Wurzelverzeichnis, übersprungen'); sys.exit(0)
daten = {'host': S.HOST.split('//')[1], 'key': key, 'keyLocation': f'{S.HOST}/{key}.txt', 'urlList': urls}
print('IndexNow:', len(urls), 'Adressen' + (' (Trockenlauf)' if trocken else ''))
for u in urls:
    print('  ', u)
if trocken:
    sys.exit(0)
try:
    req = urllib.request.Request('https://api.indexnow.org/indexnow', data=json.dumps(daten).encode('utf-8'),
                                 headers={'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'dissected-veroeffentlichen'})
    with urllib.request.urlopen(req, timeout=30) as r:
        print('IndexNow: Antwort', r.status)
except Exception as e:
    print('IndexNow: nicht gelungen,', e)
sys.exit(0)
