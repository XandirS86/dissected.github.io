# -*- coding: utf-8 -*-
"""Gemeinsame Helfer für die Veröffentlichungsautomatik: Seiten finden, Köpfe lesen, Git-Daten.
Nur Standardbibliothek. Pfade sind relativ zur Wurzel des Repos, mit Schrägstrich."""
import os, re, json, subprocess, html, datetime

HOST = 'https://www.dissected.eu'
WURZEL = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
FRAGMENTE = {'de/vorgaenger-leiste.html', 'en/previous-strip.html'}

def rel(p):
    return os.path.relpath(p, WURZEL).replace(os.sep, '/')

def voll(p):
    return os.path.join(WURZEL, *p.split('/'))

def lesen(p):
    with open(voll(p), 'rb') as f:
        return f.read().decode('utf-8').replace('\r\n', '\n')

def schreiben(p, text, eol=None):
    """Schreibt mit den Zeilenenden der bestehenden Datei (sonst LF); gibt True zurück, wenn sich etwas geändert hat."""
    pfad = voll(p)
    alt = open(pfad, 'rb').read() if os.path.exists(pfad) else b''
    if eol is None:
        eol = '\r\n' if b'\r\n' in alt else '\n'
    neu = text.replace('\r\n', '\n').replace('\n', eol).encode('utf-8')
    if neu == alt:
        return False
    with open(pfad, 'wb') as f:
        f.write(neu)
    return True

def alle_seiten():
    seiten = []
    for ordner in ['', 'de', 'en', 'de/analysen', 'en/analyses']:
        d = voll(ordner) if ordner else WURZEL
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if name.endswith('.html'):
                seiten.append((ordner + '/' + name) if ordner else name)
    return seiten

def kopf(text):
    """Liest die SEO-relevanten Felder aus dem <head>."""
    h = text.split('</head>')[0]
    def eins(pat):
        m = re.search(pat, h, re.S)
        return html.unescape(m.group(1).strip()) if m else None
    k = {
        'title': eins(r'<title>(.*?)</title>'),
        'description': eins(r'<meta name="description" content="(.*?)"'),
        'robots': eins(r'<meta name="robots" content="(.*?)"'),
        'canonical': eins(r'<link rel="canonical" href="(.*?)"'),
        'og': {m.group(1): html.unescape(m.group(2)) for m in re.finditer(r'<meta property="(og:[a-z:_]+)" content="(.*?)"', h)},
        'twitter': {m.group(1): html.unescape(m.group(2)) for m in re.finditer(r'<meta name="(twitter:[a-z:_]+)" content="(.*?)"', h)},
        'article': {m.group(1): html.unescape(m.group(2)) for m in re.finditer(r'<meta property="(article:[a-z_]+)" content="(.*?)"', h)},
        'hreflang': {m.group(1): m.group(2) for m in re.finditer(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', h)},
        'jsonld': [],
        'jsonld_fehler': [],
        'streutext': [],
    }
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            k['jsonld'].append(json.loads(m.group(1)))
        except Exception as e:
            k['jsonld_fehler'].append(str(e))
    # Streutext: alles im head außerhalb von Tags, Skripten, Styles und title
    ohne = re.sub(r'<script.*?</script>|<style.*?</style>|<title>.*?</title>|<!--.*?-->', '', h, flags=re.S)
    for t in re.findall(r'>([^<>]+)<', ohne + '<'):
        if t.strip():
            k['streutext'].append(t.strip()[:40])
    rest = re.sub(r'<[^>]+>', '', ohne).strip()
    if rest and not k['streutext']:
        k['streutext'].append(rest[:40])
    return k

def noindex(k):
    return bool(k['robots'] and 'noindex' in k['robots'])

def indexierbar(p, k):
    """Seiten, die Google sehen soll: mit Canonical, ohne noindex, keine Fragmente, keine Fehlerseite."""
    if p in FRAGMENTE or p == '404.html':
        return False
    return bool(k['canonical']) and not noindex(k)

def url_zu_pfad(url):
    """https://www.dissected.eu/de/x.html -> de/x.html; Verzeichnis-URLs auf index.html."""
    if url.startswith(HOST):
        url = url[len(HOST):]
    url = url.split('#')[0].split('?')[0]
    if url.startswith('/'):
        url = url[1:]
    if url == '' or url.endswith('/'):
        url += 'index.html'
    return url

def git(*args):
    return subprocess.run(['git', *args], cwd=WURZEL, capture_output=True, text=True, encoding='utf-8', errors='replace')

def git_datum(p):
    """Datum des letzten Commits, der die Datei berührt hat (YYYY-MM-DD); ohne Historie: heute."""
    r = git('log', '-1', '--format=%cs', '--', p)
    d = r.stdout.strip()
    return d if re.match(r'^\d{4}-\d{2}-\d{2}$', d) else datetime.date.today().isoformat()

def geaenderte_dateien(von, bis):
    """Dateien zwischen zwei Commits; bei unbekanntem Ausgangs-Commit (erster Push, Force-Push) leer."""
    if not von or set(von) == {'0'}:
        return []
    r = git('diff', '--name-only', von, bis)
    if r.returncode != 0:
        return []
    return [z.strip() for z in r.stdout.splitlines() if z.strip()]

def datei_bei_commit(commit, p):
    r = git('show', f'{commit}:{p}')
    return r.stdout.replace('\r\n', '\n') if r.returncode == 0 else ''
