---
title: "Persona und Szenario"
---

# Persona und Szenario: Fallstudie 7, Lagerraumplanung

Our group's case study for the UX part. First draft of persona, scenario, user journey and requirements is due at the next UX session on 16 Nov (UX L02 slides p. 49).

## Fixed by the case brief (Fallsteckbrief Nr. 7, p. 5)
Not to be changed (Fallsteckbriefe p. 1: Fachregel and numbers are given).
- Business case: a self-storage provider offers an online tool to find the right box size before booking.
- Persona: Julia, 31, moving. Needs an interim solution for her household goods, estimated at 14.0 m³; can combine two boxes.
- Input: length, width, height of each box (1 or 2 boxes). Each box is calculated separately via the API.
- Rule: fits if the total volume is at least 14.0 m³. Volume only, not shape. Decision: passt / passt nicht.
- Knappzone: ±0.7 m³ around 14.0 m³.
- Follow-up: reserve the box, or see what is missing.
- Example values: 18.0 + 4.5 = 22.5 → passt · 10.0 + 4.0 = 14.0 → passt, knapp · 10.0 + 3.6 = 13.6 → passt nicht, knapp.
- Mandatory cases in the prototype: normal case, exact limit, just below/above, invalid input, API error, rounding. The exact API value decides, not the rounded display.

## Persona: Julia Brandt, 31
Persona-Typ: zukünftig (to-be), teils fiktiv (Quick Intro p. 4). Mit 2–3 Personen prüfen, die schon eingelagert haben.

> „Ich kenne Umzugskartons, keine Kubikmeter.“

- **Wer:** Pflegefachfrau auf der Intensivstation, Schichtdienst mit Nachtdiensten.
- **Situation:** Trennt sich nach sechs Jahren von Jonas. Er übernimmt die gemeinsame 3-Zimmer-Wohnung in Lörrach, Julia muss bis Samstag, 31.10., raus. Ihre eigene 2-Zimmer-Wohnung in Weil am Rhein ist erst ab 15.12. frei. Dazwischen: 45 Tage auf dem Schlafsofa ihrer Schwester Lena, ein Koffer.
- **Hausrat:** 14.0 m³ laut Umzugsrechner einer Spedition. Davon sind 0.7 m³ noch offen (Waschmaschine 0.5, Teppich und Stehlampe 0.2), weil sie mit Jonas noch klärt, was ihr gehört.
- **Gerät:** Smartphone, meist einhändig im Pausenraum.

**Ziele**
- Vor der Buchung sicher wissen, ob ihr Hausrat in die Box oder die zwei Boxen passt.
- Nicht mehr Lagerfläche bezahlen als nötig. Ihr Gehalt trägt jetzt alles allein.
- Am 31.10. in einem Rutsch ausziehen. Transporter und zwei Helfer sind gebucht.
- Wenig Entscheidungen und keine weiteren Diskussionen.

**Frustrationen**
- Kubikmeter ohne Bezug: „Ist 14 viel?“
- Ein „passt“, das verschweigt, dass es auf Kante genäht ist.
- Pflichtregistrierung, bevor sie ein Ergebnis sieht (Kano: Negativmerkmal, UX L02 slides p. 6).
- Formulare, die nach einer Unterbrechung alles vergessen haben.
- Hotline nur 9 bis 17 Uhr. Da schläft sie nach dem Nachtdienst.

**Verhalten**
- Bei der Arbeit penibel (Checklisten, Übergaben), privat gerade im Ausnahmezustand.
- Entscheidet Größeres nicht allein: fragt Lena und ihre Freundin Mira, die den Transporter fährt.
- Teilt alles als Screenshot im Messenger.
- Recherchiert nachts in der Pause, bucht am nächsten Morgen.

**Profil** (1 = niedrig, 5 = hoch; Darstellung wie der Persona-Vergleich, Quick Intro p. 6)

| Merkmal | Wert | Warum |
|---|---|---|
| Zeitdruck | 5 | Auszug am 31.10. steht fest, Transporter und Helfer gebucht |
| Budgetdruck | 4 | Kaution, Umzug und Box zahlt sie ab jetzt allein |
| Raumvorstellung (m³) | 1 | Denkt in Umzugskartons, nicht in Kubikmetern |
| Technikaffinität | 3 | Alltags-Apps ja, neue Konten und lange Formulare nein |
| Emotionale Belastung | 4 | Trennung nach sechs Jahren, Besitz teils noch offen |
| Unterbrechungen | 5 | Nutzung in Pausen im Nachtdienst, Alarme gehen vor |

**Hausrat, 14.0 m³** (persona assumption; sums to the brief's 14.0): 45 Umzugskartons 3.6 · Kleiderschrank zerlegt 2.0 · Bett 160 mit Matratze 1.6 · Kleinkram 1.4 · zwei Bücherregale 1.2 · Omas Ohrensessel 1.0 · Schreibtisch mit Stuhl 1.0 · Rennrad 0.8 · Kommode 0.7 · Waschmaschine 0.5 (offen) · Teppich und Stehlampe 0.2 (offen).

## What this means for the three levels (Fallsteckbriefe p. 1)
- **Mehrteilige Eingabe:** zwei Boxkarten, Box B optional, jede mit eigenem Teilvolumen und darunter die Summe. Julia sieht, welche Box zu klein ist, und ändert nur diese.
- **Knappzone:** „knapp“ als eigener Hinweis neben passt und passt nicht, mit Puffer oder Fehlmenge in m³ und in Umzugskartons. Die offene Menge (0.7 m³) ist genau so groß wie die Knappzone: für Julia geht es bei „knapp“ darum, ob die Waschmaschine mitkommt. Die Regel prüft nur das Volumen, deshalb verdient ein Puffer von 0.0 m³ bei sperrigen Stücken einen Hinweis.
- **Folgehandlung:** passt → reservieren ohne Pflichtkonto und Ergebnis teilen; passt nicht → Box ändern, die Fehlmenge bleibt sichtbar.

## Nutzungskontext (UX L02 slides p. 17–24)
| | |
|---|---|
| **Nutzerin: Wissen** | Erster Umzug mit Einlagerung, nie Self-Storage genutzt; kennt Umzugskartons, keine Kubikmeter |
| **Nutzerin: Demografie** | 31, keine Einschränkungen; nach dem Nachtdienst müde, kleine Schrift strengt an |
| **Nutzerin: Haltung** | Hoch motiviert, aber erschöpft; misstraut Verkaufstools, die zur größeren Box drängen |
| **Nutzerin: Arbeit** | Schichtdienst; Nutzung in Pausen von etwa 15 Minuten, oft nachts |
| **Aufgabe: Ziel** | Eine oder zwei Boxen finden, in die 14.0 m³ passen, und reservieren |
| **Aufgabe: Ein-/Ausgabe** | Länge, Breite, Höhe je Box → passt/passt nicht, Summe, Puffer oder Fehlmenge |
| **Aufgabe: Häufigkeit, Dauer** | Einmalig, etwa 5 Minuten; muss ohne Einarbeitung funktionieren |
| **Aufgabe: Wahlfreiheit** | Könnte anrufen oder vorbeifahren, tut es nur, wenn das Tool scheitert |
| **Aufgabe: Abhängigkeiten** | Auszugstermin 31.10., Transporter, Helfer, Absprache mit Jonas |
| **Umfeld: physisch** | Pausenraum der Station, nachts, gedimmtes Licht; im Untergeschoss schwaches Mobilnetz |
| **Umfeld: sozial** | Lena und Mira entscheiden mit, abgestimmt wird im Messenger |
| **Umfeld: Gerät** | Smartphone, einhändig, Hochformat |
| **Umfeld: Unterbrechungen** | Jederzeit: Monitoralarm, Kollegin, Patientenruf |

## Szenario (Quick Intro p. 10–11)
**Ist-Szenario. So 11.10., 22:40 Uhr, Küchentisch.** Jonas sitzt im Nebenzimmer. Die Spedition hat Julia 14 m³ ausgerechnet. Auf der Website des Lagers heißen die Boxen „M, ideal für eine 1-Zimmer-Wohnung“. Welche Kombination für sie reicht, steht nirgends. Die Hotline ist nur tagsüber erreichbar, und da schläft sie. Im Zweifel bucht sie die größere Box und zahlt sechs Wochen lang für Luft. Oder sie bucht die kleinere und steht am 31.10. mit dem Sessel auf dem Parkplatz.

**Soll-Szenario. Di 13.10., 3:10 Uhr, Pause im Nachtdienst.** Julia hat 15 Minuten. Sie öffnet auf dem Handy den Box-Check des Anbieters. Ohne Konto trägt sie zwei Boxen aus der Übersicht ein: Box A mit 2.0 × 2.0 × 2.5 m und Box B mit 1.8 × 1.0 × 2.0 m. Die App zeigt beide Teilvolumen und die Summe, 13.6 m³. Darunter: „Passt nicht, knapp. Es fehlen 0.4 m³, etwa 5 Umzugskartons.“

Ein Monitoralarm. Julia lässt das Handy liegen. Als sie zwanzig Minuten später zurückkommt, sind ihre Eingaben noch da. Sie ändert nur Box B auf 2.0 × 1.0 × 2.0 m. Jetzt: „Passt, knapp. 14.0 m³, kein Puffer.“ Darunter steht, dass sperrige Stücke wie Sessel oder Fahrrad oft mehr Platz brauchen, als ihr Volumen zeigt.

Sie schickt das Ergebnis an Lena und Mira. Mira antwortet am Morgen: „Die Waschmaschine bleibt doch bei Jonas, oder?“ Julia klärt es mit Jonas: ja. Damit hat sie einen halben Kubikmeter Luft. Nach dem Frühstück reserviert sie die Kombination ab Samstag, 31.10. Die Bestätigung mit Zugangscode und Enddatum landet in ihrem Kalender.

## User Journey
| Phase | Tut | Denkt | Kontaktpunkt | Gefühl | Chance |
|---|---|---|---|---|---|
| Auslöser (Anfang Okt.) | Trennt sich, vereinbart Auszug zum 31.10., findet Wohnung ab 15.12. | „Und wohin sechs Wochen mit meinen Möbeln?“ | Gespräch, Wohnungsportal | −2 | außerhalb des Produkts |
| Schätzen (abends) | Umzugsrechner einer Spedition: 14.0 m³ | „Ist 14 viel? Und die Waschmaschine?“ | Website der Spedition | −1 | Volumen in Umzugskartons übersetzen |
| Suchen (abends) | Sucht „Lagerbox Lörrach“, vergleicht drei Anbieter | „Box M für eine 1-Zimmer-Wohnung. Und ich?“ | Suchmaschine, Anbieter-Website | 0 | Box-Check direkt neben der Boxübersicht, ohne Konto |
| Kombinieren (Nachtdienst) | Box A + B: 13.6 m³, passt nicht, knapp | „Fast. Aber fast reicht nicht.“ | Box-Check auf dem Handy | −1 | Teilvolumen und Fehlmenge zeigen |
| Unterbrochen (Nachtdienst) | Alarm; 20 Minuten später sind die Eingaben noch da | „Gut, nichts verloren.“ | Box-Check | 0 | Eingaben behalten, Funkloch verständlich abfangen |
| Knapp verstehen (Nachtdienst) | Ändert Box B: 14.0 m³, passt, knapp, 0.0 Puffer | „Passt, aber auf Kante. Gut, dass ich das weiß.“ | Ergebnisanzeige | 0 | „knapp“ erklären statt verschweigen |
| Abstimmen (morgens) | Teilt das Ergebnis; Waschmaschine bleibt bei Jonas | „Ich muss das nicht allein entscheiden.“ | Messenger | +1 | Teilbarer Link mit Maßen und Ergebnis |
| Reservieren (morgens) | Reserviert ab Samstag, 31.10. | „Eine Sache weniger.“ | Reservierung, Bestätigung | +2 | Reservieren ohne Pflichtkonto, Bestätigung mit Enddatum |

## User Stories
**US-1 Boxen zusammenstellen.** Als Julia möchte ich die Maße von einer oder zwei Boxen eingeben und jedes Teilvolumen sowie die Summe sehen, damit ich verstehe, wie das Ergebnis zustande kommt.
- A 3.0 × 2.5 × 2.4 und B 1.5 × 1.5 × 2.0 → 18.0 und 4.5 m³, Summe 22.5 m³: passt, Puffer 8.5 m³ (Steckbrief).
- Box B ist optional; mit nur einer Box wird nur diese berechnet.
- Jede Box wird einzeln über die API berechnet, die App bildet die Summe.

**US-2 Knapp ehrlich zeigen.** Als Julia möchte ich erfahren, wenn mein Ergebnis auf der Kippe steht, damit ich nicht blind auf Kante buche.
- 10.0 + 4.0 = 14.0 m³: passt, knapp, Puffer 0.0 m³ (Steckbrief).
- 10.0 + 4.4 = 14.4 m³ (B 2.0 × 1.1 × 2.0): passt, knapp, Puffer 0.4 m³ (own test value).
- 10.0 + 3.6 = 13.6 m³: passt nicht, knapp (Steckbrief).
- Knapp heißt: exakter Wert von 13.3 bis 14.7 m³. „knapp“ ergänzt nur einen Hinweis; die Entscheidung bleibt bei der Fachregel (mindestens 14.0 m³).

**US-3 Sehen, was fehlt.** Als Julia möchte ich bei „passt nicht“ sehen, wie viel fehlt, in einer Einheit, die ich mir vorstellen kann, damit ich entscheide, ob ich eine größere Box nehme oder weniger einlagere.
- 13.6 m³ → „Es fehlen 0.4 m³, etwa 5 Umzugskartons.“
- Umrechnung 1 Umzugskarton ≈ 0.08 m³, in der Oberfläche als „etwa“ gekennzeichnet.
- Vom Ergebnis aus lässt sich eine Box ändern, ohne die andere neu einzugeben.

**US-4 Teilen und reservieren.** Als Julia möchte ich das Ergebnis mit Lena und Mira teilen und die passende Kombination ohne Pflichtkonto reservieren, damit ich nicht allein entscheiden muss und der 31.10. sicher ist.
- Bei „passt“ ist „Reservieren“ die Hauptaktion, bei „passt nicht“ ist es „Box ändern“.
- Der geteilte Link öffnet dieselben Maße und dasselbe Ergebnis.
- Für das Ergebnis braucht es kein Konto; Kontaktdaten erst bei der Reservierung.

**US-5 Unterbrechungen und Fehler überstehen.** Als Julia möchte ich, dass meine Eingaben eine Unterbrechung oder ein Funkloch überstehen, damit ich im Nachtdienst nicht von vorn anfangen muss.
- Ungültige Eingabe (leer, 0, negativ, Text): Hinweis direkt am Feld, keine API-Anfrage. Obergrenzen laut API-Dokumentation aus dem DevOps-Teil.
- API-Fehler oder Zeitüberschreitung: „Keine Verbindung. Deine Eingaben sind gespeichert.“ und „Erneut versuchen“; die Eingaben bleiben stehen.
- Nach dem Neuladen der Seite sind die Eingaben noch da.

**US-6 Keine Rundungsfalle.** Als Julia möchte ich, dass die angezeigte Zahl zur Entscheidung passt, damit ich einem „14.0 m³, passt nicht“ nie begegne.
- Entscheidend ist der exakte API-Wert, nicht der gerundete (Steckbrief).
- 10.0 + 1.99 × 1.0 × 2.0 (3.98) = 13.98 m³: passt nicht, knapp. Angezeigt wird „13.98 m³“, nicht „14.0 m³“; es fehlen 0.02 m³ (own test value).
- In der Knappzone zeigt die App zwei Nachkommastellen, sonst eine.

## Assumptions to defend in the Fachgespräch
- **Lease gap as the trigger:** the brief says interim solution while moving; the gap between two leases is the obvious case.
- **Breakup:** explains why the estimate wobbles (0.7 m³ open) and why Julia needs calm, clear wording and backing from friends.
- **Shift work:** justifies phone use, interruptions and a weak network, i.e. the mandatory cases API error and keeping inputs.
- **Moving box ≈ 0.08 m³** (60 × 40 × 34 cm ≈ 0.082 m³): a translation aid, not a basis for the calculation.

> **Ask the lecturer**  
> - Do the Knappzone limits themselves (13.3 and 14.7 m³) count as „knapp“?
> - Which maximum values for length, width and height does the API documentation set?
> - Does Julia type the box dimensions freely or pick boxes from the provider's catalogue? The brief lists length, width and height as inputs.

## Next
- Group review of the persona; adapt or drop assumptions
- Validate with 2–3 people who have used self-storage (UX L02 slides p. 49)
- About 10 central requirements, functional and non-functional, also beyond the brief (UX L02 slides p. 49)

## AI use
- 2026-10-05 · Claude (Claude Code) · proposed three persona directions; the user chose a mix of "lease gap" and "breakup". Drafted persona, profile, usage context, as-is/to-be scenario, user journey and six user stories with acceptance criteria from the brief's example values, plus the poster page. Assumptions are marked; group review pending.
