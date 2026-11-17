# Passerelle de décision produit Amazon

`amazon-product-decision-gateway` · Français

## Objectif et périmètre

Envoyer un dossier minimal à un moteur privé hébergé séparément et vérifier sa réponse signée. Le client public ne contient pas le moteur.

## Fondements et dépendances

Python 3.9+, cryptography, service HTTPS, jeton en variable d’environnement et clé publique Ed25519 fiable. Exploitation, conservation et frais relèvent du fournisseur. Sans service, préparer seulement le dossier local.

## Entrées

Obligatoires : decision_request JSON, produit, marché, devise et date des preuves. Un GO propre à l’entreprise exige ses contraintes. Autorisation précise de destination et de transmission ; jamais de jeton dans les fichiers.

## Sorties

request_validation.json ; après autorisation, decision_response.json et synthèse. Vérifier empreintes requête/résultat, signature et version ; distinguer preuves, valeurs modélisées, lacunes et conditions.

## Déroulement

1. Fixer périmètre/version
2. retirer secrets, données personnelles et chemins internes
3. valider le schéma localement
4. expliquer destination et catégories puis obtenir l’accord précis
5. soumettre et vérifier empreintes/signature
6. conserver le statut indisponible ou diagnostic.

## Limites et conditions d’arrêt

Ne pas reconstruire les pondérations privées ni inventer de verdict local. Arrêter sur données sensibles, défaut d’accord, signature/empreinte invalide. Pas de redirection avec jeton. Une dérogation diagnostic n’est pas une décision officielle.

## Exemple de demande

Utilise `$amazon-product-decision-gateway` — Préparer les preuves d’un support de téléphone aux États-Unis, puis soumettre uniquement après accord de transmission au service identifié ; réponds en français en conservant les preuves, les inconnues et les limites d’autorisation.

## Spécification complète

[Point d’entrée du Skill et références détaillées](../../SKILL.md).

Utiliser la langue explicitement demandée, sinon celle de la demande. Conserver les commandes, identifiants de Skill, clés JSON, valeurs d’énumération, unités et citations originales. Distinguer traduction et original. Ne déduire ni pays, ni devise, ni juridiction de la langue. Lire les références détaillées utiles et maintenir tous les contrôles et autorisations existants.

Avant livraison, rapprocher entrées, preuves, valeurs manquantes, fichiers et critères d’achèvement d’origine. Marquer les étapes non exécutées comme non vérifiées ; la réussite d’un script ne valide pas une conclusion métier.

## Couverture linguistique et validation

Ce guide localisé couvre objectif, prérequis, entrées, sorties, étapes, exemples et limites. Il ne traduit pas chaque référence ligne par ligne. Les références techniques détaillées, cas historiques, erreurs de scripts, interfaces d’exemple et images restent dans leur langue originale et peuvent être expliqués à la demande. Structure, liens et contraintes essentielles sont vérifiés ; aucune relecture par un locuteur natif de chaque langue n’est revendiquée.

