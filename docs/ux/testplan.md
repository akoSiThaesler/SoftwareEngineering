---
title: "Testplan"
---

# Testplan: Usability-Test "Lagerraum Box-Check"

> **Status (23.11.2026):** Entwurf des Teams, mit KI-Unterstützung erstellt und vom Team zu prüfen. Er beruht auf dem [Cognitive Walkthrough](cognitive-walkthrough.html). Die Befund-IDs (CW01 bis CW09) verweisen dorthin. Es liegen noch keine Testergebnisse vor.

## 1 Ziel und Fragen

Der Test soll zeigen, ob eine Person, die das Produkt nicht kennt, mit dem Prototyp ohne Hilfe herausfindet, ob ihre Möbel in eine oder zwei Boxen passen, ein "knapp" richtig versteht und eine Reservierung abschliessen und anpassen kann. Er prüft den Prototyp, nicht die Person.

**Hinweis zum Prototyp:** Der Fallsteckbrief setzt den Bedarf fest auf 14.0 m³ und spricht von 1 oder 2 Boxen. Der Prototyp lässt den Bedarf änderbar (Startwert 14.0 m³) und erlaubt bis zu vier Boxen. Grössenkatalog (S, M, L, XL), Konto, Zahlungsarten, Haltefrist und Reservierungsnummer sind erfunden und in der Oberfläche als Beispiel gekennzeichnet.

| Nr. | Frage an den Test | Bezug zum Walkthrough |
|---|---|---|
| F-A | Wählt die Testperson selbst eine Lösung, oder greift sie zum vorgeschlagenen Vorschlag mit der grössten Box? | CW01 |
| F-B | Versteht sie die Symbole auf den Grössenkarten und den Tab "Anmelden" richtig und wird sie dadurch verunsichert? | CW02, CW09 |
| F-C | Findet sie bei der zweiten Box die eigenen Masse und behält sie die Übersicht über die Summe? | CW03 |
| F-D | Erklärt sie "knapp" und die Knappzone in eigenen Worten richtig? Weiss sie, was sie nachprüfen könnte? | CW04, CW05 |
| F-E | Füllt sie das Formular flüssig aus, oder stört die stehende Fehlerzeile und das Datumsformat? | CW06, CW07 |
| F-F | Unterscheidet sie "Neue Prüfung starten" und "Reservierung stornieren" und findet sie die Datumsänderung? | CW08 |

## 2 Aufbau und Rollen

- **Umfang:** etwa 3 Einzeltests pro Prototyp, je 10 bis 12 Minuten.
- **Rollen je Test:** 1 Moderation (liest vor, hilft nicht, fragt nach), 1 bis 2 Notizen (füllen das Beobachtungsblatt in Abschnitt 6 aus, nehmen die Zeit). Eine Person kann Rolle und Zeitnahme übernehmen.
- **Gerät:** Smartphone oder Browser mit Handy-Breite (etwa 390 × 844 px), Prototyp-Adresse **ohne** Zusatz hinter dem Pfad, damit keine Simulationsleiste erscheint. Bildschirmaufzeichnung nur mit Einverständnis.
- **Raum:** ruhiger Ort, die Testperson hält das Gerät selbst. Die Beobachtenden sitzen seitlich und schauen mit.
- **Material:** dieser Testplan, ausgedrucktes Beobachtungsblatt je Person und Aufgabe, Aufgabenkarten (nur der Text aus Abschnitt 4, einzeln ausgeteilt), Karte mit Beispieldaten (Name "Alex Muster", E-Mail "alex@beispiel.ch").
- **Zurücksetzen vor jedem Test (wichtig):** Der Prototyp speichert Eingaben und eine Reservierung auf dem Gerät und behält sie nach dem Neuladen. Vor jeder Person muss die Moderation deshalb:
  1. eine vorhandene Reservierung stornieren und den Hinweis "Reservierung … storniert." mit "Ausblenden" schliessen, **oder** die Websitedaten des Browsers löschen, **oder** ein neues privates Fenster öffnen (am einfachsten);
  2. "Neue Prüfung starten" bzw. "Neu beginnen" tippen, falls Eingaben stehen.

  "Neue Prüfung starten" allein genügt nicht: Es leert nur die Eingaben, eine Reservierung bleibt bestehen und erscheint auf dem Start als "Deine Reservierung" (siehe CW08). Zwischen den Aufgaben setzt die Moderation nur die Eingaben zurück, und zwar ohne Kommentar.
- **Erreichbar machen (keine grosse Änderung am Prototyp vor dem Test):** Die drei Pfade (Prüfen, zwei Boxen, Reservieren und ändern) funktionieren im Prototyp. Notfall, falls eine Person bei Aufgabe 2 nicht weiterkommt: Die Moderation öffnet den vorbereiteten Link zum Ergebnis, notiert dies als "nein" bei Erfolg und fährt mit Aufgabe 3 fort.

## 3 Einstiegsszenario (vorlesen, ohne Hilfen)

> Stell dir vor: Du ziehst in drei Wochen aus deiner Wohnung aus. Die neue Wohnung ist erst sechs Wochen später frei. In dieser Zeit sollen deine Möbel, Kleider und Kisten sicher untergebracht sein. Eine Spedition hat dir gesagt, dass es ungefähr 14 Kubikmeter sind. Du weisst nicht genau, wie viel das ist. Du hast gerade die Seite eines Anbieters auf dem Handy geöffnet. Ich bitte dich, dich in diese Situation zu versetzen und mir deine Gedanken laut zu sagen.

Die Beobachtenden sagen vorher keine Wörter vom Bildschirm, der Anbieter wird nur "der Anbieter" genannt.

## 4 Aufgaben

Die Aufgaben sind Ziele der Nutzerin, enthalten keine Schritte und keine Wörter aus der Oberfläche. Sie werden nacheinander ausgeteilt. Das Wort "Abteil" wird von uns eingeführt und steht nicht auf dem Bildschirm. Der erwartete Pfad ist **nur für Notierende** und wird nie gezeigt.

### Aufgabe 1: Passt alles in ein Abteil?

**Text an die Testperson:** "Du möchtest herausfinden, ob du alles in einem einzigen Abteil unterbringen kannst. Finde das mit dieser Seite heraus und sag mir, was du erfährst."

- **Erfolg (ja):** Die Testperson wählt selbst ein einzelnes Abteil, sieht das Resultat und sagt in eigenen Worten, ob es reicht und wie viel fehlt oder übrig ist.
- **mit Hilfe:** Sie braucht einen Hinweis der Moderation oder liest das Resultat falsch vor.
- **nein:** Sie gibt auf oder nennt ein falsches Resultat.
- **Erwarteter Pfad (nur für Notierende, nicht zeigen):** Start, eine der vier Grössen antippen, "Prüfen, ob es passt", Resultat ansehen. Beliebige Grösse ist in Ordnung (S, M, L: "Passt nicht"; XL: "Passt").

### Aufgabe 2: Zwei Abteile ohne Verschwendung

**Text an die Testperson:** "Du willst alles unterbringen und dabei nicht mehr Fläche bezahlen, als nötig ist. Setze dafür zwei Abteile zusammen, mit denen es reicht, und erkläre mir danach, wie viel Spielraum du dann hast."

- **Erfolg (ja):** Die Testperson stellt zwei Abteile zusammen, deren Summe mindestens 14.0 m³ beträgt, und nennt den Spielraum in eigenen Worten (z. B. "genau auf der Grenze", "es ist eng", "4 Kubikmeter Luft").
- **mit Hilfe:** Sie braucht einen Hinweis oder die Moderation bei der Summe.
- **nein:** Sie findet keine Kombination oder missdeutet das Resultat (z. B. hält "knapp" für "geht nicht").
- **Erwarteter Pfad (nur für Notierende, nicht zeigen):** Start oder "Neu beginnen", erste Grösse, "+ Weitere Box kombinieren", zweite Grösse (oder "Eigene Masse eingeben"), "Prüfen, ob es passt". Alternativ über "Auswahl ändern" und die Zeile "Grösse S dazunehmen" unter "So könnte es passen". Beispiele: L plus S ergeben 14.0 m³ ("Passt, aber knapp", Reserve 0.0 m³); XL plus S ergeben 22.0 m³.

### Aufgabe 3: Die Lösung sichern und später verschieben

**Text an die Testperson (Teil a):** "Du hast dich für eine Lösung entschieden. Sorge dafür, dass sie ab Mitte Januar für dich gesichert ist. Deine Angaben stehen auf dieser Karte."

**Text (Teil b), erst vorlesen, wenn Teil a abgeschlossen ist:** "Eine Woche später stellst du fest, dass du sie erst zwei Wochen später brauchst. Sorge dafür, dass es wieder stimmt."

- **Erfolg Teil a (ja):** Eine Bestätigung mit Datum Mitte Januar ist erreicht, die Testperson sagt, dass es geklappt hat.
- **Erfolg Teil b (ja):** Das neue Datum ist gespeichert (Hinweis "Reservierung geändert." sichtbar) und die Testperson sagt, dass es geklappt hat.
- **mit Hilfe / nein:** wie bei den anderen Aufgaben; Teil a und b werden getrennt bewertet.
- **Erwarteter Pfad (nur für Notierende, nicht zeigen):** Von einem Resultat zur Reservierung ("Reservieren" bzw. "Trotzdem reservieren" bei einem knappen Resultat), Formular ausfüllen ("Einlagern ab", Name, E-Mail), "Jetzt reservieren". Teil b: Reservierungsdetail, "Zeitraum oder Kontakt ändern", Datum anpassen, Änderung speichern.
- **Zusatzfrage nach Teil b (keine Aufgabe, nur mündlich):** "Angenommen, du brauchst die Lösung doch nicht. Was würdest du tun? Zeig es mir, aber tippe nicht auf die Bestätigung." So wird CW08 beobachtet, ohne dass die Reservierung gelöscht wird.

Zeitvorschlag: Begrüssung und Einverständnis 2 Minuten, Aufgabe 1 etwa 2 Minuten, Aufgabe 2 etwa 3 Minuten, Aufgabe 3 etwa 3 Minuten, Nachfragen und Abschluss etwa 2 Minuten.

## 5 Testskript

Die Moderation liest den Text in Anführungszeichen vor; alles andere sind Regieanweisungen.

**1. Begrüssung**
"Hallo, schön, dass du dir die Zeit nimmst. Ich heisse [Name]; [Namen der Notierenden] schreiben mit. Wir testen einen Prototyp, nicht dich. Es gibt keine falschen Antworten, und wenn etwas nicht klappt, liegt das am Prototyp. Der Test dauert etwa zehn bis zwölf Minuten."

**2. Einverständnis**
"Wir machen Notizen zu dem, was du sagst und tust. Es gibt keine Namen im Protokoll. Möchtest du, dass wir den Bildschirm aufzeichnen? Du kannst jederzeit abbrechen. Ist das in Ordnung?" Die Antwort wird auf dem Beobachtungsblatt festgehalten.

**3. Lautes Denken erklären**
"Bitte sag laut, was du denkst, was du siehst und was du erwartest, während du die Seite benutzt. Wenn du etwas nicht verstehst oder dich etwas stört, sag das auch. Ich werde dir meistens nicht antworten, weil ich sehen will, wie du es allein machst."

**4. Szenario und Aufgaben**
Das Einstiegsszenario (Abschnitt 3) vorlesen, dann die Aufgaben nacheinander in Abschnitt 4 vorlesen und die Karte übergeben. Eine Aufgabe nach der anderen, erst die nächste, wenn die Person sagt, dass sie fertig ist oder nicht weiterkommt. Nach etwa 4 Minuten ohne Fortschritt die Aufgabe beenden und als "nein" notieren.

**5. Während der Aufgaben**
- Nicht helfen, nicht führen, keine Wörter vom Bildschirm vorsagen.
- Fragen mit Gegenfragen beantworten: "Was denkst du?", "Was würdest du jetzt machen, wenn ich nicht da wäre?"
- Bei längerem Schweigen: "Woran denkst du gerade?"
- Notierende halten Kritisches, Fragen und Zitate fest.

**6. Nachfragen** (kurz, nach der letzten Aufgabe)
- "Wie war das insgesamt für dich?"
- "Was war leicht, was war schwierig?"
- "Wie sicher bist du, dass deine Sachen in die Lösung passen, die du gewählt hast? Woran siehst du das?" (CW04)
- "Was bedeutet für dich das gelbe Wort auf dem Resultat?" Nur fragen, wenn die Person "knapp" nicht von selbst erklärt hat.
- "Was hast du erwartet, als du auf die untere Schaltfläche getippt hast?" (nur bei Auffälligkeiten)

**7. Abschluss**
"Danke, das hat uns sehr geholfen. Du hast nichts falsch gemacht. Gibt es noch etwas, das du sagen möchtest?" Gerät zurücksetzen (Abschnitt 2).

## 6 Beobachtungsblatt

Pro Testperson und Aufgabe eine Kopie. Mit den vier Feldern der Empathy Map: **SAGT** wörtliche Aussagen, **DENKT** Vermutungen (als Interpretation kennzeichnen), **TUT** Klicks, Fehler, Zögern, **FÜHLT** Frustration, Freude, Verwirrung.

| | |
|---|---|
| Testperson (Kürzel, keine Namen) | P__ |
| Aufgabe (1 / 2 / 3a / 3b) | |
| Datum, Moderation, Notierende | |
| Einverständnis Aufzeichnung | ja / nein |

| SAGT (wörtlich) | DENKT (Interpretation, so kennzeichnen) |
|---|---|
| <br><br><br><br> | <br><br><br><br> |

| TUT (Klicks, Fehler, Zögern) | FÜHLT (Frustration, Freude, Verwirrung) |
|---|---|
| <br><br><br><br> | <br><br><br><br> |

| Erfolg | Zeit (min:s) | Hilfe nötig (was?) | Kritische Probleme, Fragen, Kommentare |
|---|---|---|---|
| ja / mit Hilfe / nein | | | |

Bezug zum Walkthrough (Befund-ID notieren, falls beobachtet):

| Befund-ID | Beobachtet? | Beleg (Zitat, Tun) |
|---|---|---|
| CW01 | ja / nein | |
| CW02 | ja / nein | |
| CW03 | ja / nein | |
| CW04 | ja / nein | |
| CW05 | ja / nein | |
| CW06 | ja / nein | |
| CW07 | ja / nein | |
| CW08 | ja / nein | |
| CW09 | ja / nein | |
| neu | ja / nein | |

## 7 Auswertung

Nach den drei Tests trägt das Team die Befunde zusammen. Häufigkeit zählt, bei wie vielen der 3 Personen das Problem auftrat. Schweregrad: Hoch = verhindert das Ziel oder führt zu einer falschen Entscheidung; Mittel = Umweg oder Zweifel; Niedrig = kleine Irritation. Status: **bestätigt** (Walkthrough-Befund trat auf), **widerlegt** (trat nicht auf, Begründung festhalten) oder **neu** (nicht vorhergesagt).

| Finding-ID | Beschreibung | Häufigkeit (x von 3) | Schweregrad | bestätigt / widerlegt / neu | Änderung (konkret, mit Begründung) |
|---|---|---|---|---|---|
| CW01 | Vorschlag XL vor jeder Eingabe | | | | |
| CW02 | Figur neben den Karten wirkt wie "i" | | | | |
| CW03 | Eigene Masse bei Box 2, keine Summe vorab | | | | |
| CW04 | Text zur Knappzone setzt Messung voraus | | | | |
| CW05 | "Trotzdem reservieren" | | | | |
| CW06 | Stehende Fehlerzeile im Formular | | | | |
| CW07 | Datumsformat | | | | |
| CW08 | "Neue Prüfung starten" und "Reservierung stornieren" | | | | |
| CW09 | Tab "Anmelden" | | | | |
| T01 | (neuer Befund aus dem Test) | | | neu | |

Aus der Tabelle ergeben sich die **3 bis 5 wichtigsten Befunde** mit einer konkreten Änderung und einer Begründung (Häufigkeit und Schweregrad). Vor dem Test wird nichts am Entwurf umgebaut; Änderungen entstehen erst aus der Auswertung.

## 8 Grenzen

- **Testpersonen:** Wir testen vermutlich mit Mitstudierenden. Sie gehören nicht zur eigentlichen Zielgruppe (Menschen mit Umzug, ohne Self-Storage-Erfahrung, unter Zeitdruck, oft müde). Die Übertragbarkeit ist begrenzt und wird in der Auswertung benannt.
- **Drei Personen** zeigen Muster, keine Häufigkeiten. Ein Problem, das bei einer Person auftrat, ist ein Hinweis, kein Beleg.
- **Prototyp mit simuliertem Hintergrund:** Es gibt keine Anbindung an ein echtes System, nichts wird gebucht, und die Katalogwerte sind erfunden. Die Reaktion der Testperson auf Preis, Vertrag oder Zahlungsdaten lässt sich damit nicht prüfen.
- **Kontext:** Im Test fehlen Zeitdruck, Müdigkeit, Unterbrechungen und ein schwaches Mobilnetz. Diese Punkte der Persona bleiben ungetestet.
- **Moderationseinfluss:** Auch freundliche Nachfragen können Antworten lenken. Darum werden sie vorab festgelegt (Abschnitt 5).
