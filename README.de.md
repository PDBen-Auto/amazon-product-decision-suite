# Amazon-Produktentscheidungs-Gateway

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

Die ausdrücklich gewünschte Ausgabesprache verwenden, sonst der Sprache der Anfrage folgen. Befehle, Skill-IDs, JSON-Schlüssel, Enumerationswerte, Einheiten und Originalzitate unverändert lassen. Übersetzungen kennzeichnen. Land, Währung und Rechtsordnung nicht aus der Sprache ableiten. Relevante Detailreferenzen lesen und sämtliche bestehenden Prüfungen und Berechtigungsgrenzen einhalten.

## Installation und Nutzung

Das Repository herunterladen oder klonen und das angegebene Skill-Verzeichnis mit seinen vorhandenen references, scripts, assets und weiteren Abhängigkeiten in das Skill-Verzeichnis des Hosts kopieren. Name und SKILL.md beibehalten. Ein Sprachwechsel erfordert keine weitere Installation. Installationsbefehle sind Optionen und kein Nachweis einer Installation oder Aktivierung.

```sh
git clone https://github.com/PDBen-Auto/amazon-product-decision-suite.git
```

## Amazon-Produktentscheidungs-Gateway

`amazon-product-decision-gateway`

Ein minimiertes Belegpaket an eine separat betriebene private Entscheidungs-Engine senden und das signierte Ergebnis prüfen. Der öffentliche Client enthält die Engine nicht.

Skill-Verzeichnis: `.`

**Umsetzungsgrundlage und Abhängigkeiten**

Python 3.9+, cryptography, HTTPS-Dienst, Token als Umgebungsvariable und vertrauenswürdiger Ed25519-Schlüssel. Betrieb, Aufbewahrung und Gebühren verantwortet der Anbieter. Ohne Dienstzugang nur lokale Vorbereitung.

**Eingaben**

Pflicht: decision_request-JSON, Produkt, Marktplatz, Währung und Belegdatum. Unternehmensbezogenes GO braucht Geschäftsgrenzen. Ziel und Datenumfang müssen ausdrücklich freigegeben sein; Token nie in Dateien.

**Ausgaben**

request_validation.json; nach Freigabe decision_response.json und Zusammenfassung. Anfrage-/Ergebnishashes, Signatur und Engine-Version prüfen; Belege, Modellwerte, Lücken und Bedingungen trennen.

[Ablauf · Grenzen und Abbruchbedingungen · Beispielanfrage](references/i18n/de.md)

> Verwende `$amazon-product-decision-gateway` — US-Handyhalter-Belege lokal vorbereiten und erst nach zielbezogener Übertragungsfreigabe das verifizierte Ergebnis abrufen; antworte auf Deutsch und erhalte Belege, unbekannte Werte und Berechtigungsgrenzen.

## Sprachumfang und Prüfung

Dieser lokalisierte Leitfaden umfasst Zweck, Voraussetzungen, Ein- und Ausgaben, Ablauf, Beispiele und Grenzen. Er übersetzt nicht jede Referenz Zeile für Zeile. Technische Detailreferenzen, historische Fälle, Skriptfehler, Beispieloberflächen und Bilder bleiben in der Originalsprache und können auf Wunsch erläutert werden. Struktur, Links und Kernbedingungen werden geprüft; ein muttersprachliches Lektorat je Sprache wird nicht behauptet.

Vor der Übergabe Eingaben, Belege, fehlende Werte, Ausgabedateien und ursprüngliche Abschlusskriterien abgleichen. Nicht ausgeführte Schritte als ungeprüft kennzeichnen; ein erfolgreicher Skriptablauf bestätigt keine geschäftliche Aussage.
