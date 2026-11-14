# -*- coding: utf-8 -*-
"""Prüft die Seite vor der Veröffentlichung: Köpfe nach der Checkliste in DESIGN.md, interne Links, Bilder,
Sitemap und Feeds. Fehler beenden mit Exit 1 (Workflow rot, Push-Hook bricht ab), Warnungen nur melden.
Aufruf: python werkzeug/pruefen.py [--leise]"""
import os, re, sys, xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seite as S

fehler, warnungen = [], []
def F(p, text): fehler.append(f'{p}: {text}')
def W(p, text): warnungen.append(f'{p}: {text}')

seiten = S.alle_seiten()
koepfe = {p: S.kopf(S.lesen(p)) for p in seiten}
indexierbare = [p for p in seiten if S.indexierbar(p, koepfe[p])]
kanon_zu_pfad = {koepfe[p]['canonical']: p for p in indexierbare}

def existiert(p):
    return os.path.isfile(S.voll(p))

def ziel_pfad(seite_p, href):
    """Interner Link -> Repo-Pfad, oder None für externe und besondere Links."""
    h = href.strip()
    if not h or h.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:')):
        return None
    if re.match(r'^[a-z]+://', h):
        return S.url_zu_pfad(h) if h.startswith(S.HOST) else None
    h = h.split('#')[0].split('?')[0]
    if not h:
        return None
    if h.startswith('/'):
        ziel = h[1:]
    else:
        ziel = os.path.normpath(os.path.join(os.path.dirname(seite_p), h)).replace(os.sep, '/')
        if ziel.startswith('..'):
            return 'AUSSERHALB:' + h
    if ziel == '' or ziel.endswith('/'):
        ziel += 'index.html'
    return ziel

for p in seiten:
    if p in S.FRAGMENTE:
        continue  # Vorlagen ohne eigenen Kopf, per robots.txt gesperrt
    k = koepfe[p]
    text = S.lesen(p)
    body = text.split('</head>', 1)[-1]
    if k['streutext']:
        F(p, f'Streutext im <head>: {k["streutext"]}')
    for e in k['jsonld_fehler']:
        F(p, f'JSON-LD nicht lesbar: {e}')
    # Links und Bilder prüfen wir auf allen Seiten, Köpfe nur auf indexierbaren
    for m in re.finditer(r'<(?:a|link)\b[^>]*?href="([^"]*)"', text):
        z = ziel_pfad(p, m.group(1))
        if z is None:
            continue
        if z.startswith('AUSSERHALB:'):
            F(p, f'Link führt aus der Seite heraus: {z[11:]}'); continue
        if not existiert(z):
            F(p, f'Link ins Leere: {m.group(1)}')
    for m in re.finditer(r'<img\b[^>]*>', body):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag)
        if not src:
            F(p, 'Bild ohne src'); continue
        z = ziel_pfad(p, src.group(1))
        if z and not existiert(z):
            F(p, f'Bild fehlt: {src.group(1)}')
        if 'alt=' not in tag:
            F(p, f'Bild ohne alt: {src.group(1)}')
        if not re.search(r'\swidth="\d+"', tag) or not re.search(r'\sheight="\d+"', tag):
            F(p, f'Bild ohne width/height: {src.group(1)}')
        d = re.search(r'data-dunkel="([^"]+)"', tag)
        if d:
            zd = ziel_pfad(p, d.group(1))
            if zd and not existiert(zd):
                F(p, f'Dunkler Zwilling fehlt: {d.group(1)}')
    if not S.indexierbar(p, k):
        continue
    # Kopf nach Checkliste
    if not k['title']:
        F(p, 'kein <title>')
    elif len(k['title']) > 110:
        W(p, f'Titel sehr lang ({len(k["title"])} Zeichen)')
    if not k['description']:
        F(p, 'keine Beschreibung')
    else:
        if len(k['description']) > 200:
            F(p, f'Beschreibung zu lang ({len(k["description"])} Zeichen)')
        elif len(k['description']) > 160:
            W(p, f'Beschreibung über 160 Zeichen ({len(k["description"])})')
    if k['canonical'] != S.HOST + '/' + p:
        F(p, f'Canonical passt nicht zum Pfad: {k["canonical"]}')
    if not k['robots'] or 'max-image-preview:large' not in k['robots']:
        W(p, 'ohne robots max-image-preview:large')
    hl = k['hreflang']
    if not hl:
        F(p, 'keine hreflang-Angaben')
    else:
        eigene = 'en' if p.startswith('en/') else 'de'
        if hl.get(eigene) != k['canonical']:
            F(p, f'hreflang {eigene} zeigt nicht auf die Seite selbst')
        if 'x-default' not in hl:
            F(p, 'hreflang x-default fehlt')
        for lang, url in hl.items():
            zp = S.url_zu_pfad(url)
            if zp not in koepfe:
                F(p, f'hreflang {lang} zeigt auf fehlende Seite {url}'); continue
            if lang != 'x-default' and zp != p:
                gegen = koepfe[zp]['hreflang']
                if gegen.get(eigene) != k['canonical']:
                    F(p, f'hreflang nicht symmetrisch: {zp} verweist nicht zurück')
    og = k['og']
    for feld in ('og:type', 'og:title', 'og:description', 'og:url', 'og:site_name', 'og:locale'):
        if feld not in og:
            F(p, f'{feld} fehlt')
    if og.get('og:url') and og['og:url'] != k['canonical']:
        F(p, 'og:url weicht vom Canonical ab')
    if 'og:image' in og:
        bild = S.url_zu_pfad(og['og:image'])
        if not existiert(bild):
            F(p, f'og:image fehlt als Datei: {og["og:image"]}')
        for feld in ('og:image:width', 'og:image:height', 'og:image:alt'):
            if feld not in og:
                W(p, f'{feld} fehlt')
        if k['twitter'].get('twitter:card') != 'summary_large_image':
            W(p, 'twitter:card ist nicht summary_large_image, obwohl ein Bild da ist')
    else:
        F(p, 'og:image fehlt')
    if og.get('og:description') != k['description']:
        F(p, 'og:description weicht von der Beschreibung ab')
    if 'twitter:description' in k['twitter'] and k['twitter']['twitter:description'] != k['description']:
        F(p, 'twitter:description weicht von der Beschreibung ab')
    if og.get('og:type') == 'article':
        art = next((j for j in k['jsonld'] if isinstance(j, dict) and j.get('@type') == 'Article'), None)
        if not art:
            F(p, 'Artikel ohne JSON-LD Article')
        else:
            for feld in ('headline', 'description', 'image', 'datePublished', 'dateModified', 'author', 'mainEntityOfPage'):
                if feld not in art:
                    F(p, f'JSON-LD Article ohne {feld}')
            if art.get('description') != k['description']:
                F(p, 'JSON-LD description weicht von der Beschreibung ab')
            if art.get('dateModified') and k['article'].get('article:modified_time') and art['dateModified'] != k['article']['article:modified_time']:
                F(p, 'dateModified und article:modified_time unterscheiden sich')
        for feld in ('article:published_time', 'article:modified_time', 'article:section'):
            if feld not in k['article']:
                W(p, f'{feld} fehlt')
        if not any(isinstance(j, dict) and j.get('@type') == 'BreadcrumbList' for j in k['jsonld']):
            W(p, 'ohne BreadcrumbList')
        if 'loading="lazy"' not in body and len(re.findall(r'<img\b', body)) > 1:
            W(p, 'mehrere Bilder, keines lazy')

# Sitemap
try:
    baum = ET.parse(S.voll('sitemap.xml'))
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    locs = [u.find('s:loc', ns).text.strip() for u in baum.getroot().findall('s:url', ns)]
    for p in indexierbare:
        if koepfe[p]['canonical'] not in locs:
            F('sitemap.xml', f'fehlt: {p}')
    for loc in locs:
        zp = S.url_zu_pfad(loc)
        if zp not in koepfe:
            F('sitemap.xml', f'Eintrag ohne Datei: {loc}')
        elif not S.indexierbar(zp, koepfe[zp]):
            F('sitemap.xml', f'nicht indexierbare Seite eingetragen: {loc}')
    if len(locs) != len(set(locs)):
        F('sitemap.xml', 'doppelte Einträge')
except Exception as e:
    F('sitemap.xml', f'nicht lesbar: {e}')

# Feeds
for feed, ordner in (('de/feed.xml', 'de/analysen/'), ('en/feed.xml', 'en/analyses/')):
    try:
        baum = ET.parse(S.voll(feed))
        links = [i.find('link').text.strip() for i in baum.getroot().iter('item')]
        for p in indexierbare:
            if p.startswith(ordner) and S.HOST + '/' + p not in links:
                F(feed, f'kein Eintrag für {p}')
        for l in links:
            zp = S.url_zu_pfad(l)
            if not existiert(zp):
                F(feed, f'Eintrag ohne Datei: {l}')
        if baum.getroot().find('channel/{http://www.w3.org/2005/Atom}link') is None:
            W(feed, 'ohne atom:link rel=self')
    except Exception as e:
        F(feed, f'nicht lesbar: {e}')

leise = '--leise' in sys.argv
if not leise:
    for w in warnungen:
        print('WARNUNG', w)
for f in fehler:
    print('FEHLER', f)
print(f'Geprüft: {len(seiten)} Seiten, davon {len(indexierbare)} indexierbar · Fehler: {len(fehler)} · Warnungen: {len(warnungen)}')
sys.exit(1 if fehler else 0)
