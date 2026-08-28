# Anleitung in einfacher Sprache

Diese Anleitung erklärt alles Schritt für Schritt.
Du brauchst kein Vorwissen. Du brauchst nur:
- einen Computer mit Internet,
- ein E-Mail-Postfach,
- diesen Ordner mit den fertigen Dateien.

Ein paar Wörter vorab, damit alles verständlich ist:

- **GitHub** ist eine Internetseite. Sie speichert Dateien kostenlos.
  Sie kann aus deinen Dateien eine Website machen.
- **Repository** ist das GitHub-Wort für: ein Ordner im Internet.
- **Hochladen** heißt: Dateien von deinem Computer in diesen Internet-Ordner legen.
- **Domain** ist die Adresse einer Website. Zum Beispiel: www.beispiel.de.

---

## Teil 1: Die Website ins Internet bringen

Das machst du nur ein einziges Mal. Es dauert ungefähr eine halbe Stunde.

### Schritt 1: Deine Angaben eintragen

In vier Dateien fehlen noch Angaben von dir.
Die Stellen sind **gelb markiert**.

1. Öffne den Ordner auf deinem Computer.
2. Mache einen Doppelklick auf die Datei `de/impressum.html`.
   Sie öffnet sich im Internet-Browser. Dort siehst du die gelben Stellen.
3. Zum Ändern öffnest du die Datei mit einem Text-Programm:
   Rechtsklick auf die Datei → „Öffnen mit" → **Editor** (Windows) oder **TextEdit** (Mac).
4. Ersetze die gelben Stellen durch deine Angaben:
   deine Adresse, deine E-Mail, das heutige Datum.
5. Lösche danach die Markierung. Sie sieht im Text so aus:
   `<span class="luecke">` vor dem Text und `</span>` nach dem Text.
   Beides löschen. Nur diese Zeichen, nicht deinen Text.
6. Speichern.
7. Das Gleiche machst du in diesen Dateien:
   - `de/datenschutz.html`
   - `de/ueber.html`
   - `en/legal.html` (englisch)
   - `en/privacy.html` (englisch)
   - `en/about.html` (englisch)
8. Noch eine Ersetzung: In den Dateien `de/analysen/001-kurztitel.html`
   und `en/analyses/001-short-title.html` steht das Wort `EINSPRUCH_MAIL`.
   Ersetze es durch deine E-Mail-Adresse. An diese Adresse schreiben dir Leser.

Tipp: Wenn dir das zu fummelig ist, überspringe Schritt 1 erst einmal.
Die Website funktioniert auch so. Du kannst die Angaben später nachtragen.
Aber: Ohne Impressum darf die Seite in Deutschland nicht lange öffentlich sein.

### Schritt 2: Ein Konto bei GitHub anlegen

1. Gehe im Browser auf **github.com**.
2. Klicke auf **Sign up** (heißt: registrieren).
3. Gib eine E-Mail-Adresse, ein Passwort und einen **Benutzernamen** ein.
   Wichtig: Der Benutzername wird Teil deiner Website-Adresse.
   Wähle also einen, der dir gefällt. Zum Beispiel: `schley-dissected`.
4. Folge den Anweisungen bis zum Ende.

### Schritt 3: Einen Internet-Ordner anlegen

1. Du bist bei GitHub angemeldet.
2. Klicke oben rechts auf das **Plus-Zeichen (+)**.
3. Klicke auf **New repository** (heißt: neuer Ordner).
4. Bei „Repository name" tippst du: deinen Benutzernamen, dann `.github.io`.
   Beispiel: Wenn dein Benutzername `schley-dissected` ist,
   tippst du: `schley-dissected.github.io`
   Genau so, ohne Leerzeichen. Das ist wichtig.
5. Wähle **Public** (heißt: öffentlich). Das muss so sein, sonst ist es nicht kostenlos.
6. Klicke unten auf den grünen Knopf **Create repository**.

### Schritt 4: Die Dateien hochladen

1. Du siehst jetzt eine fast leere Seite. Dort steht ein Link:
   **uploading an existing file**. Klicke darauf.
   (Falls du ihn nicht findest: Klicke auf **Add file**, dann auf **Upload files**.)
2. Öffne auf deinem Computer den Ordner mit den Website-Dateien.
3. Markiere **alles** in dem Ordner (Strg + A bzw. Cmd + A).
4. Ziehe alles mit der Maus in das große Feld im Browser.
5. Warte, bis alle Dateien in der Liste stehen. Das kann eine Minute dauern.
6. Scrolle nach unten. Klicke auf den grünen Knopf **Commit changes**
   (heißt: speichern).

### Schritt 5: Die Website einschalten

1. Klicke oben auf **Settings** (heißt: Einstellungen).
2. Klicke links in der Liste auf **Pages**.
3. Unter „Build and deployment" gibt es ein Auswahlfeld bei **Source**.
   Wähle dort: **Deploy from a branch**.
4. Darunter erscheinen zwei Felder. Wähle: **main** und **/ (root)**.
5. Klicke auf **Save**.
6. Warte zwei Minuten. Lade die Seite neu (Taste F5).
7. Oben erscheint deine Adresse, zum Beispiel:
   `https://schley-dissected.github.io/`
8. Klicke darauf. **Das ist deine Website. Sie ist jetzt im Internet.**

---

## Teil 2: Eine eigene Adresse (Domain)

Ohne diesen Teil steht „github" in deiner Adresse.
Mit einer eigenen Adresse steht da nur noch dein Name, zum Beispiel `www.deine-seite.de`.
Das kostet ungefähr 10 bis 20 Euro im Jahr. Dieser Teil ist freiwillig.

### Schritt 1: Adresse kaufen

1. Gehe auf die Seite eines Anbieters. Gut und einfach sind zum Beispiel
   **inwx.de** oder **hetzner.com**.
2. Tippe deinen Wunschnamen in das Suchfeld. Die Seite zeigt dir,
   ob der Name noch frei ist und was er kostet.
3. Kaufe die Adresse. Du brauchst dafür ein Kundenkonto bei dem Anbieter.

### Schritt 2: Die Adresse mit GitHub verbinden

Jetzt sagst du der neuen Adresse, wo deine Website liegt.
Das machst du beim Anbieter, bei dem du die Adresse gekauft hast.

1. Melde dich beim Anbieter an. Suche den Bereich **DNS**
   (das ist das Adressbuch des Internets).
2. Dort legst du **vier Einträge vom Typ A** an. Bei allen vieren:
   - Name: leer lassen oder `@` eintragen
   - Wert: einer dieser vier Zahlenblöcke, für jeden Eintrag einer:
     - `185.199.108.153`
     - `185.199.109.153`
     - `185.199.110.153`
     - `185.199.111.153`
3. Dann legst du **einen Eintrag vom Typ CNAME** an:
   - Name: `www`
   - Wert: deine GitHub-Adresse, zum Beispiel `schley-dissected.github.io`
4. Speichern. Keine Sorge: Man kann hier nichts kaputt machen,
   und jeder Anbieter hat eine Hilfe-Seite mit Bildern dazu.

### Schritt 3: GitHub Bescheid sagen

1. Gehe zurück zu GitHub, in dein Repository, dann **Settings → Pages**.
2. Bei **Custom domain** tippst du deine neue Adresse ein. Klicke **Save**.
3. Warte. Das kann ein paar Stunden dauern.
4. Wenn bei **Enforce HTTPS** ein Häkchen möglich ist: Häkchen setzen.
   (HTTPS heißt: die Verbindung ist verschlüsselt. Das gehört heute dazu.)
5. Fertig. Deine Website ist jetzt unter deiner eigenen Adresse erreichbar.

Zum Schluss: Öffne die Dateien `de/feed.xml` und `en/feed.xml` im Text-Programm.
Ersetze `DEINE-DOMAIN` durch deine neue Adresse. Lade die zwei Dateien
wie in Teil 1, Schritt 4 wieder hoch. GitHub fragt beim Hochladen nicht extra –
die neuen Dateien ersetzen die alten automatisch.

---

## Teil 3: Einen neuen Artikel veröffentlichen

Das machst du bei jeder neuen Analyse. Hier nur der Ablauf in Kurzform –
die genauen Stellen in den Dateien sind in der Datei `ANLEITUNG.md` beschrieben
und in den Dateien selbst mit Kommentaren markiert.

1. **Kopiere die Vorlage.** Die Datei `de/analysen/001-kurztitel.html`
   ist ein Muster-Artikel. Kopiere sie und gib der Kopie einen neuen Namen,
   zum Beispiel `002-mein-thema.html`. Das Gleiche auf Englisch mit
   `en/analyses/001-short-title.html`.
2. **Ersetze die Texte.** Öffne die Kopie im Text-Programm. Ersetze Titel,
   Datum und Texte durch deine Analyse. Die Stellen sind im Code mit
   [A] bis [F] markiert.
3. **Trage den Artikel auf der Startseite ein.** In `de/index.html` und
   `en/index.html` stehen Titel und Link des aktuellen Artikels. Ersetze sie
   durch den neuen.
4. **Trage den Artikel im Archiv ein.** In `de/archiv.html` und `en/archive.html`
   fügst du eine Zeile oben in die Liste ein. Als Muster dient die Zeile,
   die schon da ist.
5. **Prüfe alles auf deinem Computer.** Doppelklick auf `index.html` –
   die Seite öffnet sich im Browser. Klicke alle Links an.
6. **Lade die geänderten Dateien hoch.** Wie in Teil 1, Schritt 4.
   Nach etwa einer Minute ist der Artikel im Internet.

Wichtig zu wissen: Nichts davon ist gefährlich.
Du kannst nichts endgültig kaputt machen.
Wenn etwas falsch aussieht, lädst du einfach die richtige Datei noch einmal hoch.

---

## Wenn du Hilfe brauchst

Du kannst jeden dieser Schritte auch mit Claude zusammen machen:
Beschreibe, wo du stehst und was du siehst – am besten mit einem Bildschirmfoto.
Dann bekommst du den nächsten Schritt genau für deine Situation erklärt.
