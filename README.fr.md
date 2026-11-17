# Passerelle de décision produit Amazon

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

Utiliser la langue explicitement demandée, sinon celle de la demande. Conserver les commandes, identifiants de Skill, clés JSON, valeurs d’énumération, unités et citations originales. Distinguer traduction et original. Ne déduire ni pays, ni devise, ni juridiction de la langue. Lire les références détaillées utiles et maintenir tous les contrôles et autorisations existants.

## Installation et utilisation

Télécharger ou cloner le dépôt, puis copier le répertoire du Skill indiqué, avec ses references, scripts, assets et autres dépendances existantes, dans le répertoire de Skills de l’hôte. Conserver son nom et SKILL.md. Changer la langue de documentation ne demande pas de nouvelle installation. Les commandes proposées ne prouvent ni installation ni activation.

```sh
git clone https://github.com/PDBen-Auto/amazon-product-decision-suite.git
```

## Passerelle de décision produit Amazon

`amazon-product-decision-gateway`

Envoyer un dossier minimal à un moteur privé hébergé séparément et vérifier sa réponse signée. Le client public ne contient pas le moteur.

Répertoire du Skill: `.`

**Fondements et dépendances**

Python 3.9+, cryptography, service HTTPS, jeton en variable d’environnement et clé publique Ed25519 fiable. Exploitation, conservation et frais relèvent du fournisseur. Sans service, préparer seulement le dossier local.

**Entrées**

Obligatoires : decision_request JSON, produit, marché, devise et date des preuves. Un GO propre à l’entreprise exige ses contraintes. Autorisation précise de destination et de transmission ; jamais de jeton dans les fichiers.

**Sorties**

request_validation.json ; après autorisation, decision_response.json et synthèse. Vérifier empreintes requête/résultat, signature et version ; distinguer preuves, valeurs modélisées, lacunes et conditions.

[Déroulement · Limites et conditions d’arrêt · Exemple de demande](references/i18n/fr.md)

> Utilise `$amazon-product-decision-gateway` — Préparer les preuves d’un support de téléphone aux États-Unis, puis soumettre uniquement après accord de transmission au service identifié ; réponds en français en conservant les preuves, les inconnues et les limites d’autorisation.

## Couverture linguistique et validation

Ce guide localisé couvre objectif, prérequis, entrées, sorties, étapes, exemples et limites. Il ne traduit pas chaque référence ligne par ligne. Les références techniques détaillées, cas historiques, erreurs de scripts, interfaces d’exemple et images restent dans leur langue originale et peuvent être expliqués à la demande. Structure, liens et contraintes essentielles sont vérifiés ; aucune relecture par un locuteur natif de chaque langue n’est revendiquée.

Avant livraison, rapprocher entrées, preuves, valeurs manquantes, fichiers et critères d’achèvement d’origine. Marquer les étapes non exécutées comme non vérifiées ; la réussite d’un script ne valide pas une conclusion métier.
