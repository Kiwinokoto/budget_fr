# Roadmap et passation

## Situation au 16 octobre 2026

- Dépôt public : Kiwinokoto/budget_fr. Branche dev/initial-data ; PR #1 en brouillon vers main. Vérifier le HEAD réel avant de poursuivre.
- Coordination AgentCtl : projet budget-fr, ressource repo:Kiwinokoto/budget_fr ; verrou à prendre avant toute mutation et libérer en fin de passe.
- Base Insee initiale 1995–2025 recopiée à la main **remplacée** par les chiffres du classeur officiel d'août 2026.
- Données 1960–2025 : recettes, dépenses, solde, variantes hors éléments imputés ; dette brute depuis 1978 et nette depuis 1995. Fichier original conservé à la source, pas dans Git.
- Importateur en Python standard, empreinte SHA-256 de la source, validation des libellés, années et solde ; tests couvrant les absences de valeurs.
- Application statique avec curseur temporel et graphiques de recettes/dépenses et dette.
- Aucun déploiement effectué, aucune base de données ou nouveau service VPS créé.

## Suite prioritaire

1. Valider le rendu dans un navigateur, ergonomie mobile et accessibilité (pas encore revue en détail).
2. Documenter et mesurer les écarts entre les publications Insee de mai et août 2026.
3. Rechercher des séries détaillées COFOG 1995–2024 ; contrôler la classification avant ingestion.
4. Étudier les séries de recettes par impôt, dette, intérêts, solde primaire et patrimoine.
5. Formaliser l'échelle de transparence/traçabilité par poste et sa méthodologie ; tester l'incidence fiscale.
6. Après revue de la PR et contrôles adaptés, décider si fusion et déploiement sont utiles.

## Risques

Ruptures comptables, révisions du millésime, séries partielles, faux rapprochements de périmètres, transfert doublement compté, confusion entre fiabilité de la publication et qualité politique ou efficacité de la dépense.

Passation : GitHub reste la source canonique ; ne pas laisser de fichiers importants dans une copie locale. Tester puis vérifier branche, HEAD, lease et état propre avant de conclure.
