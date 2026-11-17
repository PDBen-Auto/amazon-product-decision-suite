# Amazon-Produktentscheidungs-Gateway

`amazon-product-decision-gateway` · Deutsch

## Zweck und Einsatzbereich

Ein minimiertes Belegpaket an eine separat betriebene private Entscheidungs-Engine senden und das signierte Ergebnis prüfen. Der öffentliche Client enthält die Engine nicht.

## Umsetzungsgrundlage und Abhängigkeiten

Python 3.9+, cryptography, HTTPS-Dienst, Token als Umgebungsvariable und vertrauenswürdiger Ed25519-Schlüssel. Betrieb, Aufbewahrung und Gebühren verantwortet der Anbieter. Ohne Dienstzugang nur lokale Vorbereitung.

## Eingaben

Pflicht: decision_request-JSON, Produkt, Marktplatz, Währung und Belegdatum. Unternehmensbezogenes GO braucht Geschäftsgrenzen. Ziel und Datenumfang müssen ausdrücklich freigegeben sein; Token nie in Dateien.

## Ausgaben

request_validation.json; nach Freigabe decision_response.json und Zusammenfassung. Anfrage-/Ergebnishashes, Signatur und Engine-Version prüfen; Belege, Modellwerte, Lücken und Bedingungen trennen.

## Ablauf

1. Umfang und Konzeptversion festlegen
2. Geheimnisse, personenbezogene Daten und interne Pfade entfernen
3. Schema lokal prüfen
4. Ziel und Datenkategorien erklären und konkrete Freigabe einholen
5. senden und Hashes/Signatur prüfen
6. Nichtverfügbarkeit oder Diagnosestatus beibehalten.

## Grenzen und Abbruchbedingungen

Keine privaten Gewichtungen rekonstruieren oder lokalen Urteile erfinden. Bei sensiblen Daten, fehlender Erlaubnis oder Signatur-/Hashfehler stoppen. Keine Weiterleitungen mit Token. Diagnoseausnahme ist keine offizielle Entscheidung.

## Beispielanfrage

Verwende `$amazon-product-decision-gateway` — US-Handyhalter-Belege lokal vorbereiten und erst nach zielbezogener Übertragungsfreigabe das verifizierte Ergebnis abrufen; antworte auf Deutsch und erhalte Belege, unbekannte Werte und Berechtigungsgrenzen.

## Vollständige Spezifikation

[Skill-Einstieg und Detailreferenzen](../../SKILL.md).

Die ausdrücklich gewünschte Ausgabesprache verwenden, sonst der Sprache der Anfrage folgen. Befehle, Skill-IDs, JSON-Schlüssel, Enumerationswerte, Einheiten und Originalzitate unverändert lassen. Übersetzungen kennzeichnen. Land, Währung und Rechtsordnung nicht aus der Sprache ableiten. Relevante Detailreferenzen lesen und sämtliche bestehenden Prüfungen und Berechtigungsgrenzen einhalten.

Vor der Übergabe Eingaben, Belege, fehlende Werte, Ausgabedateien und ursprüngliche Abschlusskriterien abgleichen. Nicht ausgeführte Schritte als ungeprüft kennzeichnen; ein erfolgreicher Skriptablauf bestätigt keine geschäftliche Aussage.

## Sprachumfang und Prüfung

Dieser lokalisierte Leitfaden umfasst Zweck, Voraussetzungen, Ein- und Ausgaben, Ablauf, Beispiele und Grenzen. Er übersetzt nicht jede Referenz Zeile für Zeile. Technische Detailreferenzen, historische Fälle, Skriptfehler, Beispieloberflächen und Bilder bleiben in der Originalsprache und können auf Wunsch erläutert werden. Struktur, Links und Kernbedingungen werden geprüft; ein muttersprachliches Lektorat je Sprache wird nicht behauptet.

