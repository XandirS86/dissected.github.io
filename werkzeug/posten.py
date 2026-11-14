# -*- coding: utf-8 -*-
"""Postet neue Analysen und Nachträge auf Mastodon und Bluesky. Auslöser ist allein der Feed:
neuer <item> = neue Analyse, geänderter <item> (Titel, Text oder Datum) = Nachtrag. Text = Titel, Teasersatz, Link.
Konten in werkzeug/konten.json (öffentlich), Schlüssel aus der Umgebung: MASTODON_TOKEN, BLUESKY_APP_PASSWORD.
Ohne Schlüssel oder mit --trocken: nur Protokoll. Gepostetes steht in werkzeug/gepostet.json (gegen Doppelposts).
Aufruf: python werkzeug/posten.py --von <commit> --bis <commit> [--trocken]"""
import os, re, sys, json, hashlib, html, datetime, urllib.request, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seite as S

KONTEN = os.path.join(S.WURZEL, 'werkzeug', 'konten.json')
PROTOKOLL = os.path.join(S.WURZEL, 'werkzeug', 'gepostet.json')
FEEDS = {'de': 'de/feed.xml', 'en': 'en/feed.xml'}
GRENZE = {'mastodon': 500, 'bluesky': 300}

def arg(name, standard=''):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv and sys.argv.index(name) + 1 < len(sys.argv) else standard

def items(text):
    aus = {}
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)  # der Feed-Kommentar enthält das Wort <item>
    for block in re.findall(r'<item>(.*?)</item>', text, re.S):
        def feld(n):
            m = re.search(rf'<{n}>(.*?)</{n}>', block, re.S)
            return html.unescape(m.group(1).strip()) if m else ''
        guid = feld('guid') or feld('link')
        aus[guid] = {'titel': feld('title'), 'text': feld('description'), 'link': feld('link'), 'datum': feld('pubDate')}
    return aus

def kennung(e):
    return hashlib.sha256((e['titel'] + '|' + e['text'] + '|' + e['datum']).encode('utf-8')).hexdigest()[:16]

def kuerzen(titel, text, link, grenze, nachtrag):
    kopf = ('Nachtrag · ' if nachtrag else '') + titel
    fest = len(kopf) + 2 + 2 + len(link)
    platz = grenze - fest
    if platz < 20:
        return kopf + '\n\n' + link
    if len(text) > platz:
        text = text[:platz - 1].rsplit(' ', 1)[0].rstrip(' ,;:') + '…'
    return kopf + '\n\n' + text + '\n\n' + link

def og_bild(link):
    p = S.url_zu_pfad(link)
    if not os.path.exists(S.voll(p)):
        return None
    k = S.kopf(S.lesen(p))
    return k['og'].get('og:image')

def anfrage(url, daten=None, kopfzeilen=None, roh=None):
    body = roh if roh is not None else (json.dumps(daten).encode('utf-8') if daten is not None else None)
    k = {'User-Agent': 'dissected-veroeffentlichen'}
    k.update(kopfzeilen or {})
    if body is not None and 'Content-Type' not in k:
        k['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=body, headers=k, method='POST' if body is not None else 'GET')
    with urllib.request.urlopen(req, timeout=60) as r:
        inhalt = r.read()
        try:
            return json.loads(inhalt.decode('utf-8'))
        except Exception:
            return inhalt

def mastodon_posten(konf, token, text, sprache, kennung_):
    daten = urllib.parse.urlencode({'status': text, 'language': sprache, 'visibility': 'public'}).encode('utf-8')
    antwort = anfrage(konf['mastodon_url'].rstrip('/') + '/api/v1/statuses', roh=daten,
                      kopfzeilen={'Authorization': 'Bearer ' + token, 'Idempotency-Key': kennung_,
                                  'Content-Type': 'application/x-www-form-urlencoded'})
    return antwort.get('url') if isinstance(antwort, dict) else None

def bluesky_facetten(text):
    f = []
    for m in re.finditer(r'https?://[^\s]+', text):
        a = len(text[:m.start()].encode('utf-8')); b = len(text[:m.end()].encode('utf-8'))
        f.append({'index': {'byteStart': a, 'byteEnd': b}, 'features': [{'$type': 'app.bsky.richtext.facet#link', 'uri': m.group(0)}]})
    return f

def bluesky_posten(konf, passwort, text, sprache, titel, teaser, link):
    pds = konf.get('bluesky_pds', 'https://bsky.social').rstrip('/')
    sitzung = anfrage(pds + '/xrpc/com.atproto.server.createSession', {'identifier': konf['bluesky_handle'], 'password': passwort})
    jwt, did = sitzung['accessJwt'], sitzung['did']
    auth = {'Authorization': 'Bearer ' + jwt}
    embed = {'$type': 'app.bsky.embed.external', 'external': {'uri': link, 'title': titel, 'description': teaser[:300]}}
    bild = og_bild(link)
    if bild:
        try:
            with urllib.request.urlopen(urllib.request.Request(bild, headers={'User-Agent': 'dissected-veroeffentlichen'}), timeout=30) as r:
                png = r.read()
            if len(png) < 950_000:
                blob = anfrage(pds + '/xrpc/com.atproto.repo.uploadBlob', roh=png, kopfzeilen={**auth, 'Content-Type': 'image/png'})
                embed['external']['thumb'] = blob['blob']
        except Exception as e:
            print('   Bluesky: Vorschaubild nicht hochgeladen,', e)
    record = {'$type': 'app.bsky.feed.post', 'text': text, 'createdAt': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
              'langs': [sprache], 'facets': bluesky_facetten(text), 'embed': embed}
    antwort = anfrage(pds + '/xrpc/com.atproto.repo.createRecord', {'repo': did, 'collection': 'app.bsky.feed.post', 'record': record}, auth)
    return antwort.get('uri') if isinstance(antwort, dict) else None

def main():
    von, bis, trocken = arg('--von'), arg('--bis', 'HEAD'), '--trocken' in sys.argv
    konf = json.load(open(KONTEN, encoding='utf-8')) if os.path.exists(KONTEN) else {}
    protokoll = json.load(open(PROTOKOLL, encoding='utf-8')) if os.path.exists(PROTOKOLL) else {}
    m_token, b_pass = os.environ.get('MASTODON_TOKEN', ''), os.environ.get('BLUESKY_APP_PASSWORD', '')
    kanaele = []
    if konf.get('mastodon_url') and m_token: kanaele.append('mastodon')
    if konf.get('bluesky_handle') and b_pass: kanaele.append('bluesky')
    if not kanaele:
        trocken = True
    aufgaben = []
    for sprache, feed in FEEDS.items():
        if not os.path.exists(S.voll(feed)):
            continue
        neu = items(S.lesen(feed))
        alt = items(S.datei_bei_commit(von, feed)) if von and set(von) != {'0'} else neu
        for guid, e in neu.items():
            kz = kennung(e)
            if protokoll.get(guid) == kz:
                continue
            if guid not in alt:
                aufgaben.append((sprache, guid, e, kz, False))
            elif kennung(alt[guid]) != kz:
                aufgaben.append((sprache, guid, e, kz, True))
    if not aufgaben:
        print('Posten: keine neuen oder geänderten Feed-Einträge'); return 0
    fehler = 0
    for sprache, guid, e, kz, nachtrag in aufgaben:
        print(('Nachtrag' if nachtrag else 'Neu') + f' [{sprache}] {e["titel"]}')
        gepostet = []
        for kanal in (kanaele or ['mastodon', 'bluesky']):
            text = kuerzen(e['titel'], e['text'], e['link'], GRENZE[kanal], nachtrag)
            if trocken:
                print(f'   {kanal} (Trockenlauf, {len(text)} Zeichen):\n      ' + text.replace('\n', '\n      ')); continue
            try:
                if kanal == 'mastodon':
                    url = mastodon_posten(konf, m_token, text, sprache, kz)
                else:
                    url = bluesky_posten(konf, b_pass, text, sprache, e['titel'], e['text'], e['link'])
                print(f'   {kanal}: gepostet', url or ''); gepostet.append(kanal)
            except Exception as ex:
                print(f'   {kanal}: FEHLER {ex}'); fehler += 1
        if not trocken and len(gepostet) == len(kanaele):
            protokoll[guid] = kz
    if not trocken:
        with open(PROTOKOLL, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(protokoll, f, ensure_ascii=False, indent=1); f.write('\n')
    return 1 if fehler else 0

if __name__ == '__main__':
    sys.exit(main())
