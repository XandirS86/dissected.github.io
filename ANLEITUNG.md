# a schley, dissected · Anleitung

Alles hier ist fertig. Zwei Aufgaben bleiben: einmalig online stellen (A) und pro Analyse
die Artikel einbauen (B) – in jeder Sprache.

## Ordnerstruktur

```
index.html            Sprachweiche (leitet nach Browsersprache auf de/ oder en/)
404.html              Fehlerseite, zweisprachig
styles.css · marginalien.js · fonts/ · charts/    gemeinsam für alle Sprachen
de/   index · archiv · ueber · impressum · datenschutz · feed.xml · analysen/001-kurztitel.html
en/   index · archive · about · legal · privacy · feed.xml · analyses/001-short-title.html
```

---

## A · Einmalig: online stellen (ca. 20 Minuten)

1. **Lücken füllen** – gelb markierte Stellen (`<span class="luecke">`) in
   `de/impressum.html`, `de/datenschutz.html`, `de/ueber.html` und den englischen Gegenstücken
   `en/legal.html`, `en/privacy.html`, `en/about.html`. Danach `<span class="luecke">`/`</span>` löschen.
2. **GitHub-Konto** anlegen (github.com).
3. **Repository** „New repository" → Name exakt `NUTZERNAME.github.io` (dein Nutzername) → Public → Create. Dadurch liegt die Seite an der Wurzel: `https://NUTZERNAME.github.io/` – wichtig für die eigene Domain.
4. **Hochladen:** „Add file → Upload files", kompletten Ordnerinhalt hineinziehen
   (inkl. `de/`, `en/`, `charts/`, `fonts/` und `.nojekyll`). „Commit changes".
5. **Pages:** Settings → Pages → „Deploy from a branch" → `main` / `/ (root)` → Save.
   Nach 1–2 Minuten live: `https://NUTZERNAME.github.io/`
6. **Feeds:** in `de/feed.xml` und `en/feed.xml` `DEINE-DOMAIN` durch die eigene Domain ersetzen
   (solange keine da ist: `NUTZERNAME.github.io`).
7. **Einspruch-Adresse:** in beiden Artikelvorlagen `EINSPRUCH_MAIL` durch die E-Mail-Adresse
   ersetzen, an die Einsprüche gehen sollen (gern eine eigene, z. B. einspruch@…).

---

## A2 · Eigene Domain (empfohlen, ca. 20 Minuten + Wartezeit)

Damit in der Adresse kein GitHub steht:

1. Domain beim Registrar kaufen (z. B. INWX oder Hetzner; Verfügbarkeit dort prüfen).
2. Beim Registrar im DNS setzen:
   - vier A-Records für die nackte Domain: `185.199.108.153`, `185.199.109.153`,
     `185.199.110.153`, `185.199.111.153`
   - einen CNAME für `www` auf `NUTZERNAME.github.io`
3. Im Repository: Settings → Pages → „Custom domain" → Domain eintragen → Save.
   GitHub legt dabei eine Datei `CNAME` ins Repository – nicht löschen.
4. Sobald der Haken „Enforce HTTPS" wählbar ist (bis zu 24 h): aktivieren.
5. `DEINE-DOMAIN` in beiden Feeds eintragen.

Danach ist die Seite nur noch unter der Domain sichtbar; die GitHub-Adresse leitet weiter.

---

## B · Pro Analyse (ca. 45 Minuten ohne Schreiben – zwei Sprachen)

### 1. Charts – einmal pro Sprache
In `charts/` (Python 3 + matplotlib):
```python
from theme import balken
balken(labels, werte, hervor=-1, akzent="rot", anmerkung=(4, "tiefpunkt"),
       fussnote="anteil in %", out="002-titel.de.svg")
balken(labels, werte, hervor=-1, akzent="rot", anmerkung=(4, "low point"),
       fussnote="share in %",  out="002-title.en.svg")
```
Gleiche Werte, gleiche Farbe, nur Text übersetzt.

### 2. Artikel – einmal pro Sprache
`de/analysen/001-kurztitel.html` → kopieren zu `002-kurztitel.html`;
`en/analyses/001-short-title.html` → `002-short-title.html`.
In beiden die markierten Stellen `[A]` bis `[F]` anfassen:

| Stelle | Was                                                                  |
|--------|----------------------------------------------------------------------|
| `[A]`  | Akzentfarbe `--akzent` – in beiden Sprachen dieselbe                 |
| `[B]`  | Nummer, Thema, Datum, Titel, `<title>`, `<meta description>`, Formen  |
| `[C]`  | daten / konfidenz / methode / stand                                  |
| `[D]`  | Hypothese, Kapitel, Text, Chart-Pfad (`../../charts/002-….de.svg`), Tabellen |
| `[E]`  | Marginalien: `data-ref` = Fußnotenziffer                             |
| `[F]`  | Im `<head>` die `hreflang`-Links und in der Kopfzeile den Sprachwechsel auf die Schwesterdatei zeigen lassen (`../../en/analyses/002-short-title.html` bzw. umgekehrt) |

Kapitel: 1 der befund · 2 die zerlegung · 3 was das bedeutet — 1 the finding · 2 the breakdown · 3 what it means.

### 3. Startseiten – beide
`de/index.html` und `en/index.html`: Plakat auf die neue Analyse setzen (Nummer, Thema, Datum,
Titel, Untertitel, Links, Akzent, Formen – Akzent und Formen identisch in beiden Sprachen).
Ab № 02: `<p class="folgt">…</p>` durch die Leiste aus `de/vorgaenger-leiste.html` bzw.
`en/previous-strip.html` ersetzen.

### 4. Archiv, Feed – beide
- `de/archiv.html`, `en/archive.html`: Zeile oben einfügen, Zähler anpassen.
- `de/feed.xml`, `en/feed.xml`: `<item>` oben einfügen, `lastBuildDate` anpassen.

### 5. Einsprüche pflegen
Einsprüche kommen per E-Mail, strukturiert in Aussage / Einwand / Beleg. Du entscheidest, was
veröffentlicht wird – mit der Regel, die auf der Seite steht: Der stärkste Einwand kommt immer rein.
Pro veröffentlichtem Einspruch im Artikel (beide Sprachen) ein `<div class="einspruch__paar">`
nach dem Muster in der Vorlage: links Einwand mit Name/Ort/Datum (nur mit Zustimmung), rechts
deine Replik. Wenn der Einwand die Analyse ändert: Tag `hat die analyse geändert` stehen lassen,
im Analysekopf „stand · letzte änderung" und ggf. die Konfidenz anpassen, die Änderung im Text
vornehmen. Solange kein Einspruch vorliegt: Beispiel-Block löschen, `einspruch__leer` mit Datum lassen.

### 6. Prüfen, hochladen
Lokal `index.html` öffnen (leitet weiter), in beiden Sprachen alle Links und den Sprachwechsel
klicken, Fenster schmal ziehen. Dann „Upload files".

---

## Schreibregel für zwei Sprachen

Die englische Fassung ist keine Übersetzung, sondern dieselbe Analyse für ein Publikum ohne
deutschen Kontext: Wo der deutsche Text „Abitur" sagt, braucht der englische einen Halbsatz
Erklärung; wo der deutsche auf Bundesliga-Wissen baut, der englische nicht. Zahlen, Charts,
Konfidenz und Hypothese sind identisch – der Rest darf sich unterscheiden.

## Neue Sprache (z. B. fr)

1. Ordner `fr/` als Kopie von `en/` anlegen, Dateinamen und alle Texte übersetzen.
2. In der Wurzel-`index.html` das Kürzel in `sprachen` aufnehmen.
3. In allen Kopfzeilen den Sprachwechsel um `fr` ergänzen, in allen `<head>`s den `hreflang`-Link.
4. Charts mit `.fr.svg` erzeugen.

Spätestens hier lohnt Astro: Sprachen werden dann eine Konfigurationszeile, UI-Texte eine
JSON-Datei, und pro Analyse schreibst du nur noch zwei Markdown-Dateien. Vorgehen in `DESIGN.md`, Abschnitt 8.

## Kompositionsregeln (Kurzfassung)
Zwei bis vier Formen, eine dominiert, mindestens eine angeschnitten. Drei Farben plus Schwarz,
Weiß nie als Form. Artikelkopf wiederholt die Startseiten-Komposition kleiner. Eine Akzentfarbe
pro Analyse, identisch in allen Sprachen.
