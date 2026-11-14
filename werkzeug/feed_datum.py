# -*- coding: utf-8 -*-
"""Setzt lastBuildDate in de/feed.xml und en/feed.xml auf das jüngste pubDate der Einträge.
Die Einträge selbst bleiben Handarbeit des Autors (der Feed ist die Sendeliste für posten.py).
Aufruf: python werkzeug/feed_datum.py"""
import os, re, sys, email.utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seite as S

for feed in ('de/feed.xml', 'en/feed.xml'):
    if not os.path.exists(S.voll(feed)):
        continue
    text = S.lesen(feed)
    daten = []
    for d in re.findall(r'<pubDate>([^<]+)</pubDate>', re.sub(r'<!--.*?-->', '', text, flags=re.S)):
        try:
            daten.append((email.utils.parsedate_to_datetime(d.strip()), d.strip()))
        except Exception:
            print(f'{feed}: pubDate nicht lesbar: {d}'); sys.exit(1)
    if not daten:
        print(f'{feed}: keine Einträge'); continue
    juengstes = max(daten)[1]
    neu, n = re.subn(r'<lastBuildDate>[^<]*</lastBuildDate>', f'<lastBuildDate>{juengstes}</lastBuildDate>', text, count=1)
    if n != 1:
        print(f'{feed}: kein lastBuildDate gefunden'); sys.exit(1)
    print(f'{feed}: lastBuildDate ' + ('gesetzt auf ' + juengstes if S.schreiben(feed, neu) else 'unverändert'))
