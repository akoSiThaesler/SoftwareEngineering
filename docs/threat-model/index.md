---
title: "Threat Model"
---

# Threat Model: Konto und Login

Erste Version zur Besprechung. Zum Vorführen gibt es das Diagramm auch als [interaktive Fassung](threat-model-interactive.html).

> **Entwurf**  
> Der Prototyp hat noch kein Backend; wie das System unten aussieht, ist unsere Annahme für die erste Version. Vor dem Zeigen im Team prüfen.

## Worum es geht

Schwerpunkt **TT01, Benutzerkonten und Login**. In unserer App reserviert Julia eine Lagerbox. Mit einem Konto kann sie die Reservierung später ansehen, ändern und stornieren, und sie kann ihr Passwort per Mail zurücksetzen.

Was wir schützen: Julias Reservierung. Wer in ihr Konto kommt, kann die Box kurz vor dem Umzug stornieren.

Wer es versuchen könnte: jemand aus dem Internet mit geleakten Passwörtern, jemand mit Zugriff auf Julias Postfach, oder die nächste Person am geteilten Rechner im Pausenraum.

## So sieht das System aus

![ase sec threat model dfd](ase-sec-threat-model-dfd.svg)
*Figure: Datenflüsse für Konto und Login. Auf jedem Pfeil steht, was fliesst, wie, und als wer.*

Die drei roten Kästen sind die Stellen, an denen wechselt, wer die Kontrolle hat:

- **Julias Gerät.** Gehört ihr, nicht uns. Es kann ein geteilter Rechner sein. Allem, was von dort kommt, trauen wir erst nach einer Prüfung.
- **Unser Server.** Hier läuft unser Code und liegen die Daten. Jede Anfrage wird hier geprüft.
- **Drittanbieter.** Der E-Mail-Dienst verschickt unsere Mails. Ab da haben wir den Link nicht mehr in der Hand, und wer Julias Postfach liest, wissen wir nicht.

## Was schiefgehen kann

| Nr. | Pfeil | STRIDE | Was passiert | Wie schlimm, und warum | Was wir dagegen tun |
|---|---|---|---|---|---|
| T1 | 1 | S | Jemand probiert automatisch Passwörter aus geleakten Listen durch und kommt in Konten, deren Passwort woanders schon benutzt wurde. | **Hoch.** Geht aus dem Internet, ohne Vorwissen und automatisch. Folge: Box kurz vor dem Umzug storniert. | Fehlversuche bremsen: Die Wartezeit steigt mit jedem Versuch. Kurze und bekannte Passwörter ablehnen. |
| T2 | 3 | S | Jemand errät den Link zum Zurücksetzen oder benutzt einen alten Link noch einmal und setzt ein fremdes Passwort neu. | **Hoch.** Aus dem Internet und automatisch. Folge: Konto übernommen. | Der Link enthält einen langen Zufallswert, gilt 15 Minuten und nur einmal. |
| T3 | 1 | S | Jemand legt mit Julias E-Mail-Adresse ein Konto an, bevor sie es tut. Ihre ohne Konto gemachte Reservierung landet dann bei ihm. | **Hoch.** Nötig ist nur ihre E-Mail-Adresse. Reservieren ohne Konto erlauben wir bewusst, also müssen wir das abfangen. | Ein Konto gilt erst, wenn die E-Mail-Adresse über einen Link bestätigt ist. |
| T4 | 2 | S | Julia vergisst am geteilten Rechner im Pausenraum das Abmelden. Die nächste Person storniert ihre Box. | **Mittel.** Braucht Zugang zum selben Gerät und trifft ein Konto. | Nach 15 Minuten ohne Aktivität automatisch abmelden. Vor dem Stornieren noch einmal das Passwort fragen. |
| T5 | 6, 7 | S | Jemand mit Zugriff auf Julias Postfach fordert einen neuen Link an und übernimmt das Konto. | **Mittel.** Braucht das Postfach und trifft ein Konto. | Ein Storno lässt sich 48 Stunden lang rückgängig machen. Den Rest können wir nicht verhindern, siehe unten. |
| T6 | 3 | I | Das Formular «Passwort vergessen» verrät, ob eine E-Mail-Adresse bei uns Kundin ist. | **Niedrig.** Kein direkter Schaden, liefert aber Ziele für T1 und T3. | Immer dieselbe Antwort: «Wenn es ein Konto gibt, ist eine Mail unterwegs.» |

S = Spoofing: Jemand gibt sich als Julia aus. I = Information Disclosure: Etwas wird verraten.

**Wie wir einstufen.** Hoch heisst: geht aus dem Internet, ohne Vorwissen und automatisch. Mittel heisst: Der Angreifer braucht vorher etwas, zum Beispiel das Gerät oder das Postfach. Niedrig heisst: Es ändert keine Reservierung.

## Womit wir leben

- **Zugriff auf Julias Postfach.** Wer ihre Mails liest, kann das Konto übernehmen. Das Postfach liegt nicht bei uns. Wir machen den Schaden kleiner (Storno rückgängig), verhindern ihn aber nicht.
- **Kein eigenes Protokoll in der ersten Version.** Wir schreiben Login, Reset und Storno ins normale Log der Anwendung. Ein Log, das niemand ändern kann, kommt später.
- **Schadsoftware auf Julias Gerät.** Dagegen kann die App nichts tun.

## Bewusst weggelassen

Der Box-Check ohne Konto, Zahlung, mehrere Rollen (wäre TT02), der Betrieb des Servers. Allgemeine Web-Lücken wie SQL Injection deckt das Framework ab; sie gehören nicht in eine Liste zu unserem Schwerpunkt.

## Offen für das Review

- Stimmt das Bild mit dem überein, was wir wirklich bauen? Welcher E-Mail-Dienst, welche Datenbank?
- Ist T3 wirklich so hoch wie T1?
- Was passiert, wenn das Cookie der Sitzung gestohlen wird? Noch nicht als eigene Zeile drin.
- Reicht ein Passwort, oder braucht das Stornieren einen zweiten Schritt?

## Ausblick: Version 2

Nicht Teil der ersten Abgabe. So ändert sich das Bild, wenn die App wächst.

![ase sec threat model dfd v2](ase-sec-threat-model-dfd-v2.svg)
*Figure: Ausblick Version 2 mit Token, zwei Diensten und einem Cache.*

Was neu ist:

- **Zwei Dienste** statt einem Backend: einer für das Konto, einer für die Reservierungen.
- **Token (JWT)** statt Sitzung: Der Konto-Dienst stellt nach dem Anmelden ein Token aus. Der Reservierungs-Dienst prüft es selbst und muss nicht bei jeder Anfrage nachfragen.
- **Cache:** merkt sich Fehlversuche und gesperrte Token, damit beide Dienste schnell darauf zugreifen können.

Was dadurch neu schiefgehen kann:

| Nr. | Pfeil | STRIDE | Was passiert | Wie schlimm, und warum | Was wir dagegen tun |
|---|---|---|---|---|---|
| V1 | 2 | S | Ein gestohlenes Token gilt weiter, auch nachdem Julia sich abgemeldet hat. Der Reservierungs-Dienst prüft nur die Unterschrift. | **Mittel.** Braucht ein gestohlenes Token. Neu ist: Abmelden allein hilft nicht mehr. | Token gilt nur 15 Minuten. Beim Abmelden kommt es auf die Sperrliste im Cache. |
| V2 | 2 | S | Jemand baut sich selbst ein Token mit Julias Konto, und der Reservierungs-Dienst nimmt es an, weil er die Unterschrift nicht richtig prüft. | **Hoch.** Aus dem Internet und trifft jedes Konto. | Eine bewährte Bibliothek prüft Unterschrift, Aussteller und Ablauf. Nichts davon selbst schreiben. |
| V3 | 1 | S | Der geheime Schlüssel zum Unterschreiben steht im Repository. Wer ihn liest, stellt Token für jedes Konto aus. | **Mittel.** Braucht Zugriff aufs Repository, trifft dann aber alle. | Schlüssel nicht ins Repository. Nur der Konto-Dienst kennt den privaten Schlüssel. |
| V4 | 4, 5 | D | Der Cache fällt aus. Gesperrte Token gelten wieder, und Fehlversuche werden nicht mehr gezählt. | **Mittel.** Hebelt V1 und T1 aus, solange der Cache fehlt. | Ohne Cache darf niemand ändern oder stornieren, nur lesen. |

D = Denial of Service: Etwas fällt aus.

Was sonst für Version 2 sinnvoll wäre:

- Ein zweiter Schritt beim Anmelden oder Stornieren, zum Beispiel ein Code aufs Handy.
- Ein Werkzeug für den Support mit eigenen Rechten. Dann stellt sich die Frage, wer ausser Julia an ein Konto kommt.
- Ein Protokoll, das niemand nachträglich ändern kann.

## Next
- Group review: confirm TT01 and the picture of the system
- Name who is responsible for each measure
- SDLC-Skizze, one slide (no points, basis for the Fachgespräch)
- Pick the one example for the 3-minute talk: threat, priority, measure

