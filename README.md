# Lagerraum Box-Check

Prototyp und Dokumentation zum Programmentwurf im Modul Advanced Software Engineering (Wintersemester 2026). Fallstudie 7, Lagerraumplanung: Ein Self-Storage-Anbieter bietet ein Online-Tool, mit dem Kundinnen vor der Buchung prüfen, ob ihr Hausrat in die gewählte Box oder Kombination von Boxen passt.

**Dokumentation und Prototyp im Browser:** https://akosithaesler.github.io/SoftwareEngineering/

## Inhalt

| Ordner | Inhalt |
|---|---|
| `docs/app/` | Der Prototyp: eine einzelne HTML-Datei ohne Build-Schritt. Volumen-API und Reservierung sind simuliert. |
| `docs/ux/` | Persona und Szenario, eigener Cognitive Walkthrough mit Screenshots, Testplan für den Usability-Test. |
| `docs/threat-model/` | Threat Model zum Schwerpunkt Benutzerkonten und Login: Datenflussdiagramm, Bedrohungen, Maßnahmen, Ausblick auf Version 2, dazu eine interaktive Fassung des Diagramms. |
| `tools/` | Skripte, die die beiden Datenflussdiagramme erzeugen, und die Beschreibung der interaktiven Fassung. |
| `tests/` | Browser-Prüfungen des Prototyps mit Playwright. |

`docs/` ist die Quelle der GitHub-Pages-Seite.

## Prototyp lokal starten

```bash
python -m http.server 8000 --directory docs/app
```

Dann `http://localhost:8000/` öffnen. Mit `http://localhost:8000/?test` erscheint ein Simulations-Panel: Beispielwerte aus dem Fallsteckbrief laden, die Prüfung oder die Reservierung fehlschlagen lassen, die Antwortzeit der API verlangsamen.

## Prüfungen ausführen

```bash
npm install playwright
```

```bash
BASE_URL=http://localhost:8000/ node tests/flows.mjs screenshots
```

Die Prüfungen fahren jeden Ablauf durch (Pflichtfälle aus dem Fallsteckbrief, Reservieren, Ändern, Stornieren, Konto, Fehlerfälle) und legen Screenshots im angegebenen Ordner ab.

## Diagramme neu erzeugen

```bash
python tools/gen_dfd.py docs/threat-model/ase-sec-threat-model-dfd.svg
```

```bash
python tools/gen_dfd_v2.py docs/threat-model/ase-sec-threat-model-dfd-v2.svg
```

## Stand und Grenzen

- Der Prototyp hat kein Backend. Die Architektur im Threat Model ist eine Annahme für die erste Version.
- Abweichungen vom Fallsteckbrief: Der Bedarf (Standard 14.0 m³) lässt sich ändern, und es lassen sich bis zu vier Boxen kombinieren. Die Fachregel ist unverändert: Es passt, wenn die Summe der Boxvolumen mindestens dem Bedarf entspricht; «knapp» gilt im Bereich von ±0.7 m³.
- Grössenkatalog, Konto, Zahlungsarten, Haltefrist und Reservierungsnummer sind erfunden und in der Oberfläche als Beispiel markiert. Alle Personen sind fiktiv.
- Die UX-Dokumente sind Entwürfe und noch nicht mit Testpersonen geprüft.
