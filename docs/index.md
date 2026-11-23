---
title: Übersicht
---

# Lagerraum Box-Check

<p class="lead">Passt der Hausrat in die Lagerbox? Ein Prototyp für einen Self-Storage-Anbieter, mit der Dokumentation aus dem UX- und dem Security-Teil des Programmentwurfs.</p>

<p><a class="btn" href="{{ '/app/' | relative_url }}">Prototyp öffnen</a></p>

Der Prototyp läuft im Browser und ist für das Handy gebaut. Die Volumen-API und die Reservierung sind simuliert, es wird nichts gebucht. Mit <a href="{{ '/app/?test' | relative_url }}">Simulation</a> lassen sich Beispielwerte laden und Fehler auslösen.

## Dokumentation

<ul class="cards">
  <li><a href="{{ '/ux/persona.html' | relative_url }}"><strong>Persona und Szenario</strong><span>Julia Brandt, Nutzungskontext, Ist- und Soll-Szenario, User Journey, User Stories.</span></a></li>
  <li><a href="{{ '/ux/cognitive-walkthrough.html' | relative_url }}"><strong>Cognitive Walkthrough</strong><span>Eigener Walkthrough in fünf Schritten mit Screenshots und neun Befunden.</span></a></li>
  <li><a href="{{ '/ux/testplan.html' | relative_url }}"><strong>Testplan</strong><span>Drei neutrale Aufgaben, Testskript, Beobachtungsblatt und Auswertung.</span></a></li>
  <li><a href="{{ '/threat-model/' | relative_url }}"><strong>Threat Model</strong><span>Benutzerkonto und Login: Datenflüsse, Trust Boundaries, Bedrohungen und was die fertige App dagegen tut.</span></a></li>
</ul>

## Stand

- **Prototyp:** Ablauf von der Boxwahl bis zur Reservierung, mit Konto, Ändern und Stornieren. 54 automatische Browser-Prüfungen laufen durch, darunter die Pflichtfälle aus dem Fallsteckbrief (Normalfall, Grenzwert, knapp darunter und darüber, ungültige Eingabe, API-Fehler, Rundung).
- **Abweichungen vom Fallsteckbrief:** Der Steckbrief setzt den Bedarf auf 14.0 m³ fest und nennt 1 oder 2 Boxen. Der Prototyp lässt den Bedarf ändern und bis zu vier Boxen kombinieren. Grössenkatalog, Konto, Zahlungsarten, Haltefrist und Reservierungsnummer sind erfunden und in der Oberfläche als Beispiel markiert.
- **UX-Dokumente:** Entwürfe, noch nicht mit echten Testpersonen geprüft.
- **Threat Model:** erste Version zur Besprechung. Die Architektur ist eine Annahme, weil der Prototyp noch kein Backend hat.
