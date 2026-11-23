---
title: "Threat Model"
---

# Threat Model: Konto und Login

Erste Version zur Besprechung. Zum Vorführen gibt es das Diagramm auch als [interaktive Fassung](threat-model-interactive.html). Die [Präsentation](Threat-Model-Lagerraum.pptx) zeigt jede Bedrohung mit einem Vorher-Nachher-Bild; die Bilder stammen aus den [Mockups](mock/screens.html).

> **Entwurf**  
> Der Prototyp hat noch kein Backend. Das Bild zeigt, wie die fertige App aussehen soll; im Team prüfen, ob wir sie so bauen.

## Worum es geht

Schwerpunkt **TT01, Benutzerkonten und Login**. In unserer App reserviert Julia eine Lagerbox. Mit einem Konto kann sie die Reservierung später ansehen, ändern und stornieren, und sie kann ihr Passwort per Mail zurücksetzen.

Was wir schützen: Julias Reservierung. Wer in ihr Konto kommt, kann die Box kurz vor dem Umzug stornieren.

Wer es versuchen könnte: jemand aus dem Internet mit geleakten Passwörtern, jemand mit Zugriff auf Julias Postfach, oder die nächste Person am geteilten Rechner im Pausenraum.

## So sieht die fertige App aus

![ase sec threat model dfd](ase-sec-threat-model-dfd.svg)
*Figure: Datenflüsse für Konto und Login. Die gelben Marken zeigen, wo eine Bedrohung ansetzt.*

Kurz erklärt:

- **Konto-Dienst.** Legt Konten an, prüft E-Mail-Adresse und Passwort, gibt Julia danach ein Token und setzt Passwörter zurück. Das Token ist ein unterschriebener Ausweis, der 15 Minuten gilt.
- **Reservierungs-Dienst.** Legt Reservierungen an, ändert und storniert sie. Er prüft das Token selbst. Beim Konto-Dienst fragt er nicht nach, nur in der Sperrliste.
- **Cache.** Ein schneller Zwischenspeicher für zwei Dinge: wie oft sich jemand falsch angemeldet hat, und welche Token gesperrt sind. Er hält keine Kopien aus der Datenbank. Darum braucht es keinen Message Broker, der Kopien aktuell hält; die Einträge laufen von selbst ab.
- **E-Mail-Dienst.** Ein fremder Anbieter, der unsere Mails verschickt: den Link zum Bestätigen der Adresse und den Link zum Zurücksetzen des Passworts.

Die Pfeile im Bild:

| Nr. | Was fliesst | Wie | Als wer |
|---|---|---|---|
| 1 | E-Mail-Adresse und Passwort, zum Anmelden oder zum Anlegen eines Kontos; zurück kommt ein Token | HTTPS | noch anonym |
| 2 | Reservieren, ansehen, ändern, stornieren | HTTPS | Julia, mit Token. Neu reservieren geht auch ohne Konto. |
| 3 | Reset anfordern, neues Passwort setzen | HTTPS | anonym, dann mit dem Link aus der Mail |
| 4 | Konten und Passwort-Hash | SQL | Konto-Dienst |
| 5 | Fehlversuche zählen, Token sperren | internes Netz | Konto-Dienst |
| 6 | Ist dieses Token gesperrt? | internes Netz | Reservierungs-Dienst |
| 7 | Reservierungen | SQL | Reservierungs-Dienst |
| 8 | Mail mit Link, zum Bestätigen oder zum Zurücksetzen | HTTPS | Konto-Dienst, mit API-Schlüssel |
| 9 | Die Mail | SMTP | E-Mail-Dienst |
| 10 | Julia öffnet den Link aus der Mail | Mail-Programm | Julia |

Die vier roten Kästen zeigen, wo die Kontrolle wechselt (Trust Boundary):

- **Julias Gerät.** Gehört ihr, nicht uns. Es kann ein geteilter Rechner sein. Allem, was von dort kommt, trauen wir erst nach einer Prüfung.
- **Unser Server.** Hier läuft unser Code und liegen die Daten. Jede Anfrage wird hier geprüft.
- **Drittanbieter.** Der E-Mail-Dienst verschickt unsere Mails. Ab hier haben wir den Link nicht mehr in der Hand.
- **Mail-Anbieter.** Julias Postfach liegt bei ihrem Anbieter. Wer es ausser ihr liest, sehen wir nicht.

## Was schiefgehen kann, und was die App dagegen tut

| Nr. | Wo | STRIDE | Was passiert | Wie schlimm, und warum | So fängt die App es ab |
|---|---|---|---|---|---|
| T1 | Pfeil 1 | S | Jemand probiert automatisch Passwörter aus Datenlecks durch und kommt in Konten, deren Passwort Julia auch woanders benutzt. | **Hoch.** Geht aus dem Internet, ohne Vorwissen und automatisch. Folge: Box kurz vor dem Umzug storniert. | Der Konto-Dienst zählt Fehlversuche im Cache, je Konto und je IP-Adresse, und lässt nach jedem Fehlversuch länger warten. Kurze Passwörter und Passwörter aus bekannten Datenlecks lehnt er ab. |
| T2 | Pfeil 3 | S | Jemand errät den Link zum Zurücksetzen und setzt ein fremdes Passwort neu. | **Hoch.** Aus dem Internet und automatisch. Folge: Konto übernommen. | Der Link enthält einen langen Zufallswert, gilt 15 Minuten und nur einmal. |
| T3 | Pfeil 1 | S | Jemand legt mit Julias E-Mail-Adresse ein Konto an, bevor sie es tut. Ihre ohne Konto gemachte Reservierung landet dann bei ihm. | **Mittel.** Braucht Julias E-Mail-Adresse und muss schneller sein als sie. Reservieren ohne Konto erlauben wir bewusst, also muss das Konto bestätigt werden. | Ein Konto gilt erst, wenn die E-Mail-Adresse über einen Link bestätigt ist. |
| T4 | Julias Gerät (Pfeil 2) | S | Julia vergisst am geteilten Rechner im Pausenraum das Abmelden. Die nächste Person storniert ihre Box. | **Mittel.** Braucht Zugang zum selben Gerät. Betrifft nur ein Konto. | Das Token läuft nach 15 Minuten ab. Vor dem Stornieren fragt die App noch einmal das Passwort. |
| T5 | Postfach (Pfeile 9, 10) | S | Jemand mit Zugriff auf Julias Postfach fordert einen neuen Link an und übernimmt das Konto. | **Mittel.** Braucht das Postfach. Betrifft nur ein Konto. | Ein Storno lässt sich 48 Stunden lang rückgängig machen, die Box bleibt so lange frei. Den Rest nehmen wir in Kauf, siehe unten. |
| T6 | Pfeil 3 | I | Das Formular «Passwort vergessen» verrät, ob eine E-Mail-Adresse bei uns Kundin ist. | **Niedrig.** Kein direkter Schaden, liefert aber Ziele für T1 und T3. | Immer dieselbe Antwort: «Wenn es ein Konto gibt, ist eine Mail unterwegs.» Das gilt auch für «Konto anlegen». |
| T7 | Pfeil 2 | S | Jemand kopiert Julias Token. Es gilt weiter, auch nachdem sie sich abgemeldet hat, weil der Reservierungs-Dienst nur die Unterschrift prüft. | **Mittel.** Braucht ein gestohlenes Token. Betrifft nur ein Konto. | Beim Abmelden kommt das Token auf die Sperrliste im Cache. Nach einem Reset gelten alle älteren Token des Kontos nicht mehr. Der Reservierungs-Dienst schaut dort nach (Pfeil 6). |
| T8 | Pfeil 2 | S | Jemand fälscht ein Token auf Julias Namen, und der Reservierungs-Dienst nimmt es an, weil er die Unterschrift nicht richtig prüft. | **Hoch.** Aus dem Internet, betrifft jedes Konto. | Eine bewährte Bibliothek prüft Unterschrift und Ablaufzeit. Das schreiben wir nicht selbst. |
| T9 | Konto-Dienst | S | Der geheime Schlüssel, mit dem Token unterschrieben werden, steht im Repository. Wer ihn liest, stellt Token für jedes Konto aus. | **Mittel.** Braucht Zugriff aufs Repository. Betrifft dann alle Konten. | Der Schlüssel liegt als Geheimnis auf dem Server, nicht im Repository. Nur der Konto-Dienst kennt ihn; der Reservierungs-Dienst hat nur den öffentlichen Teil zum Prüfen. |
| T10 | Cache (Pfeile 5, 6) | D | Der Cache fällt aus oder wird geleert. Gesperrte Token gelten wieder, und Fehlversuche werden nicht mehr gezählt. | **Mittel.** Braucht einen Ausfall des Caches. Dann schützt nichts mehr gegen T1 und T7. | Ohne Cache gehen Anmelden, Ändern und Stornieren nicht. Ansehen bleibt möglich. Kommt der Cache leer zurück, gelten alle Token nicht mehr, die vor dem Neustart ausgestellt wurden. Alle melden sich dann einmal neu an. Das ist unbequem, aber gewollt. |
| T11 | Datenbank (Pfeil 4) | I | Jemand kommt an die Datenbank, zum Beispiel über ein Backup, und knackt die Passwörter, weil sie mit einem schnellen Verfahren gespeichert sind. | **Mittel.** Braucht Zugriff auf die Datenbank. Betrifft dann alle Konten. | Passwörter liegen nur als Argon2id-Hash mit eigenem Salt in der Datenbank, nie im Klartext. |

STRIDE sortiert Bedrohungen nach ihrer Art. Bei uns kommen drei vor. S = Spoofing: Jemand gibt sich als Julia aus. I = Information Disclosure: Etwas wird verraten. D = Denial of Service: Etwas fällt aus. Dass fast alles S ist, passt zum Schwerpunkt: Bei Konto und Login geht es darum, wer jemand ist.

**Wie wir einstufen.** Hoch heisst: geht aus dem Internet, ohne Vorwissen und automatisch. Mittel heisst: Der Angreifer braucht vorher etwas, zum Beispiel das Gerät, das Postfach, ein Token oder die Adresse. Niedrig heisst: Es ändert keine Reservierung.

## Womit wir leben

- **Zugriff auf Julias Postfach (T5).** Wer ihre Mails liest, kann das Konto übernehmen. Das Postfach liegt nicht bei uns. Wir machen den Schaden kleiner (Storno rückgängig), verhindern ihn aber nicht.
- **Ein gestohlenes Token gilt bis zu 15 Minuten (T7),** wenn Julia den Diebstahl nicht bemerkt und sich nicht abmeldet. Kürzer wäre sicherer, aber sie müsste sich ständig neu anmelden.
- **Der E-Mail-Dienst sieht jeden Link.** Wir vertrauen ihm. Ein Link gilt nur 15 Minuten und einmal.
- **Schadsoftware auf Julias Gerät.** Dagegen kann die App nichts tun.

## Bewusst weggelassen

Die Volumenprüfung selbst (sie braucht kein Konto), Zahlung, mehrere Rollen (wäre TT02), der Betrieb des Servers. Allgemeine Web-Lücken wie SQL Injection deckt das Framework ab; sie gehören nicht in eine Liste zu unserem Schwerpunkt.

## In welcher Reihenfolge wir bauen

Die erste Version kommt mit weniger aus: ein einziges Backend statt zwei Diensten, kein Cache, und der Server merkt sich die Anmeldung selbst (Sitzung), statt ein Token auszugeben. Dann entfallen T7 bis T10. Bei T4 läuft die Sitzung statt des Tokens nach 15 Minuten ab, und die Fehlversuche aus T1 zählt das Backend in der Datenbank. Token und Cache kommen dazu, sobald Konto und Reservierung getrennt laufen sollen.

## Offen für das Review

- Stimmt das Bild mit dem überein, was wir bauen wollen? Welcher E-Mail-Dienst, welche Datenbank?
- Bleibt die Box nach einem Storno wirklich 48 Stunden frei (T5)? Das kostet den Anbieter etwas.
- Reicht ein Passwort, oder braucht das Stornieren einen zweiten Schritt, zum Beispiel einen Code aufs Handy?
- Wer kommt ausser Julia an ein Konto, wenn es später einen Support gibt?
- Wer ist für jede Massnahme und für jedes Risiko unter «Womit wir leben» verantwortlich?

## Next
- Group review: confirm TT01 and the picture of the system
- Name who is responsible for each measure
- SDLC-Skizze, one slide (no points, basis for the Fachgespräch)
- Pick the one example for the 3-minute talk: threat, priority, measure

