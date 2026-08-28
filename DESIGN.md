# a schley, dissected · Designsystem v0.2

Eine Schrift. Vier Farben. Ein Raster. Drei Formen.
Laute Hülle, ruhiger Text. Jede Analyse ist ein Einzelstück – aber nur im Kopf.

---

## 1. Was fest ist und was frei ist

| Fest (Template, nie anfassen)           | Frei (pro Analyse komponiert)                    |
|-----------------------------------------|--------------------------------------------------|
| Kopfzeile, Fußzeile, Navigation         | Akzentfarbe (`--akzent`: rot, blau oder gelb)    |
| Lesekörper: Zeilenmaß, Typo, Abstände   | Komposition im Plakatkopf (Formen, Position)     |
| Analysekopf-Felder (daten, methode, konfidenz, stand) | Kapitelzahl und -titel               |
| Chart- und Tabellenstil                 | Welche Charts, welche Marginalien                |
| Archiv, Startseiten-Logik               | —                                                |

Die Regel: Wenn du merkst, dass du für eine Analyse den Lesekörper ändern willst, ist das
ein Änderungswunsch am System – nicht am Stück.

---

## 2. Tokens

### Farbe
| Token      | Hex       | Rolle                                                  |
|------------|-----------|--------------------------------------------------------|
| `--weiss`  | `#ffffff` | Grund. Immer.                                          |
| `--schwarz`| `#111111` | Text, Linien, Balken. Nie reines `#000`.               |
| `--rot`    | `#d7261e` | Akzent 1                                               |
| `--gelb`   | `#f2c200` | Akzent 2 (nie für Text auf Weiß – Kontrast reicht nicht)|
| `--blau`   | `#1b4fa0` | Akzent 3                                               |
| `--grau`   | `#5c5c5c` | Sekundärtext, Bildunterschriften                        |
| `--grau-hell`| `#9a9a9a`| Metadaten, Nummern im Archiv                           |

Pro Analyse gilt genau eine Akzentfarbe (`--akzent`). Sie färbt: Nummer, Kapitelzahlen,
Hypothesen-Balken, Fußnotenziffern, Konfidenz, die aktuelle Säule im Chart, die Plakatfläche.
Die beiden anderen Primärfarben erscheinen nur in den Formen des Kopfes.

### Schrift
- **Jost** (Google Fonts, offene Futura-Nachfolgerin). Gewichte 400 / 500 / 700. Nichts anderes.
- Titel: 700, Versalien, `line-height .95`, `letter-spacing -.01em`, max. 14 Zeichen breit.
- Meta, Navigation, Kapitel, Tabellenköpfe: 12–13 px, Kleinschreibung, `letter-spacing .2em`.
- Lesetext: 17 px, 400, `line-height 1.7`, Zeilenmaß 64 Zeichen, normale Rechtschreibung.
- Zahlen: immer `tabular-nums`.
- Untertitel und Bildunterschriften in normaler Rechtschreibung – Kleinschreibung nur für Labels.

### Raster
- Seitenbreite 1120 px, Seitenrand 40 px, Grundmodul 40 px.
- Startseite: Plakat 3 : 2 (Text : Komposition), Vorgänger 1 : 1 : 1.
- Artikel: Lesekörper 3 : 1 (Text : Marginalie). Analysekopf 1 : 1.
- Archiv: 1 : 3 (Filter : Liste).
- Linien: 3 px für Strukturkanten (unter Kopfzeile, unter Plakat, über Fußzeile),
  1 px für Innenkanten, `#ddd` für Tabellenzeilen.

### Formen
Kreis, Quadrat, Dreieck, Balken. Heute rein gestalterisch; sobald Rubriken entstehen,
werden sie zu Rubrikzeichen (siehe 6).

---

## 3. Den Plakatkopf komponieren

Jede Analyse bringt drei Dinge mit:

```html
<section class="plakat" style="--akzent:var(--rot)">          <!-- 1. Akzentfarbe -->
  <div class="plakat__text"> … meta, titel, untertitel … </div>
  <a class="komposition" href="…">                              <!-- 2. Komposition -->
    <span class="form form--kreis gelb"   style="width:260px;height:260px;top:40px;right:-70px"></span>
    <span class="form form--quadrat blau" style="width:90px;height:150px;bottom:0;left:0"></span>
    <span class="form form--balken schwarz" style="width:100%;height:14px;top:0;left:0"></span>
  </a>
</section>
```

Regeln für gute Kompositionen (aus den Bauhaus-Plakaten abgeleitet):
- **Zwei bis vier Formen**, nicht mehr. Eine dominiert (mind. 60 % der Fläche berühren).
- **Anschnitt**: mindestens eine Form läuft über den Rand hinaus (negative `top/right/bottom/left`).
- **Kontrast der Größen**: die größte Form ist mindestens dreimal so groß wie die kleinste.
- **Drei Farben plus Schwarz, nie Weiß als Form** – Weiß ist der Grund.
- Der Artikel-Kopf (`.analysekopf__farbe`) wiederholt die Komposition kleiner, mit denselben
  Formen. So erkennt man das Stück auf der Startseite wieder.

Drei Grundmuster, die immer funktionieren:
1. *Der große Kreis* – ein Kreis gelb oder blau, angeschnitten rechts oben, ein kleines Quadrat links unten.
2. *Die Diagonale* – ein schwarzer Balken, `transform:rotate(-12deg)`, ein Kreis darüber, ein Quadrat darunter.
3. *Das Raster* – drei gleich große Quadrate in drei Farben, versetzt im 40-px-Modul.

---

## 4. Der Analysekopf (Pflichtfelder)

| Feld       | Inhalt                                                            |
|------------|-------------------------------------------------------------------|
| daten      | Quellen, Zeitraum, Stichprobe                                     |
| methode    | Modell, Zerlegung, wichtigste Definition – in maximal zwei Zeilen |
| konfidenz  | hoch / mittel / niedrig – und im letzten Kapitel begründet        |
| stand      | Erstveröffentlichung, letzte Änderung                             |

Dazu im Text als erstes Element die **Hypothese** (ein Satz, `.hypothese`).
Die Kapitel sind nummeriert, weil eine Analyse eine Reihenfolge hat: Befund → Zerlegung → Bedeutung.

---

## 5. Charts und Tabellen

Vorlage: `charts/zentrum-anteil.svg`. Standard (Isotype/Neurath statt Dashboard):
- Flächen: schwarz, ein Wert in `--akzent` (der, um den es geht). Keine Farbverläufe, keine Schatten.
- Nur die Nullinie (2 px schwarz). Keine Gitterlinien, kein Rahmen, keine Y-Achse – Werte stehen am Balken.
- Schrift Jost, Labels 12 px grau, Werte 12 px 500 schwarz.
- Eine Anmerkung im Chart erlaubt (gestrichelt, `--akzent`), z. B. der Tiefpunkt.
- SVG, `viewBox 640 × 300` für Vollbreite, 640 × 200 für Nebencharts. Kein PNG.
- Erzeugung: matplotlib mit festem Theme (kommt als `charts/theme.py`), Export als SVG,
  danach nichts mehr von Hand anfassen.

Tabellen: nur horizontale Linien, Zahlen rechtsbündig mit Tabellenziffern, Kopf klein und gesperrt,
die entscheidende Zeile `.hervor`.

---

## 6. Rubriken – die Tür, die offen bleibt

Heute: Jede Analyse hat ein Thema-Wort (fußball, bildung, governance …) und ein Zeichen.
Ab ~15 Analysen: Thema-Wörter zu 3–5 Rubriken bündeln, jeder Rubrik ein Zeichen zuweisen
(Kreis, Quadrat, Dreieck, Balken, Halbkreis). Das Zeichen erscheint dann in Vorgänger-Leiste,
Archivfilter und Analysekopf. Farben bleiben pro Stück frei – so kollidiert Rubrik nie mit Akzent.

---

## 7. Sprachen

Jede Analyse erscheint in jeder Sprache der Seite. Struktur: ein Ordner pro Sprache
(`/de/`, `/en/`, später `/fr/` …), darin dieselben Seiten mit übersetzten Dateinamen
(`archiv.html` / `archive.html`). Gemeinsam bleiben `styles.css`, `marginalien.js`, `fonts/`, `charts/`.

- Marke, Nummerierung, Akzentfarbe und Komposition sind in allen Sprachen identisch – nur Text wechselt.
- Charts existieren pro Sprache (`001-titel.de.svg`, `001-title.en.svg`), erzeugt aus demselben Aufruf mit übersetzten Labels.
- Jede Seite trägt `hreflang`-Links auf ihre Schwesterfassungen und den Sprachwechsel `de · en` in der Kopfzeile.
- Die Wurzel `index.html` leitet nach Browsersprache weiter, Standard Englisch.
- Neue Sprache: Ordner anlegen, Sprachkürzel in `index.html` (Wurzel) und in alle Sprachwechsel eintragen, Impressum/Datenschutz übersetzen (deutsche Fassung bleibt rechtlich maßgeblich).

## 8. Einspruch – die Rückkopplung als Designelement

Unter jeder Analyse steht der Seziertisch: die Sektion `einspruch` / `objections`.
Drei Prinzipien, die Trolling strukturell ausschließen (nicht anonym, nicht sofort, nicht ungeprüft):

1. **Form erzwingt Methode.** Ein Einspruch hat dieselbe Struktur wie eine Analyse:
   Aussage → Einwand → Beleg. Der `mailto:`-Link belegt Betreff und Körper vor. Kein Drittanbieter.
2. **Kuratierte Veröffentlichung.** Einsprüche erscheinen zeitversetzt, mit Replik, als Paar
   (`.einspruch__paar`: links Einwand, rechts Replik am Akzentbalken). Regel auf der Seite:
   Der stärkste Einwand wird immer veröffentlicht.
3. **Sichtbare Konsequenz.** Trifft ein Einwand, bekommt die Replik das Tag „hat die analyse geändert",
   der Analysekopf einen neuen Stand, die Konfidenz ggf. eine Stufe tiefer. Der Leser sieht,
   dass er den Autor seziert hat.

Später, wenn Diskussion außerhalb entsteht: Webmentions (Bluesky/Mastodon) als zweite Spalte
unter der Sektion; giscus nur, falls das Publikum GitHub-affin ist. Nie: Disqus, anonyme Sofort-Kommentare.

## 9. Überführung nach Astro

```
src/
  layouts/Analyse.astro        ← Kopfzeile, Analysekopf, Lesekörper-Grid, Fußzeile
  components/Plakat.astro      ← nimmt akzent + slot für die Formen
  components/Chart.astro       ← bindet SVG ein, setzt figure/figcaption
  i18n/de.json, en.json        ← alle UI-Strings (archiv, daten, konfidenz …)
  content/analysen/de/012-zentrum.md
  content/analysen/en/012-centre.md
  styles/global.css            ← = styles.css
astro.config: i18n { defaultLocale: "en", locales: ["de","en"] }
```

Frontmatter je Analyse:

```yaml
nummer: 12
titel: Das Zentrum kehrt zurück
untertitel: Passquoten in der Bundesliga 2015–2026 – und warum das Pressing der eigentliche Treiber ist.
thema: fußball
datum: 2026-08-27
akzent: rot
daten: "FBref, Opta · 2015/16 – 2025/26"
methode: "Zonenmodell 3 × 3 · Passherkunft, nicht Ziel"
konfidenz: hoch
hypothese: Der Anteil zentraler Pässe steigt seit 2019 wieder – nicht wegen Taktikmoden, sondern wegen des Pressings.
komposition:
  - {form: kreis, farbe: gelb, w: 260, h: 260, top: 40, right: -70}
  - {form: quadrat, farbe: blau, w: 90, h: 150, bottom: 0, left: 0}
  - {form: balken, farbe: schwarz, w: "100%", h: 14, top: 0, left: 0}
```

Startseite = neueste Analyse als Plakat + die drei davor. Archiv = alle, absteigend.
Marginalien: im Prototyp mit `margin-top` von Hand gesetzt; in Astro über ein kleines Script,
das jede Marginalie an ihrem `<sup class="ref">` ausrichtet (oder Tufte-CSS-Sidenotes übernehmen).

Hosting: GitHub Pages über Actions, eigene Domain später per CNAME.
Impressum und Datenschutz als statische Seiten – Pflicht bei regelmäßig redaktionellem Inhalt.
