# Feuille de route et passation

## État au 2026-10-16

- Dépôt public initialisé ; chantier sur `dev/initial-data`.
- AgentCtl : projet `budget-fr`, scope exact `repo:Kiwinokoto/budget_fr`.
- Premier lot : tableau Insee 1995–2025, visualiseur statique sans dépendance, test d'intégrité.
- **Objectif historique 1980–2025 non encore atteint** ; aucune série fiscale détaillée importée.
- Aucun hébergement public ou déploiement effectué.

## Étapes suivantes

1. Télécharger et analyser **le XLSX officiel Insee 2381414** ; documenter colonnes, période et millésime ; ajouter 1980–1994 à partir des valeurs réellement vérifiées.
2. Mettre en place un import reproductible (source archivée avec sa licence, empreinte SHA-256, schéma, contrôle de révisions) plutôt qu'une transcription manuelle.
3. Ajouter COFOG 1995–2024 avec la bonne classification et les sous-secteurs ; prévenir les doubles comptes.
4. Ajouter dette brute/nette, solde primaire, recettes fiscales détaillées lorsqu'elles sont comparables.
5. Concevoir un registre de provenance et un audit de transparence ; tester les définitions d'incidence fiscale.
6. Envisager une publication après tests, validation documentaire et décision explicite.

## Risques ouverts

Changements de base, arrondis, révisions, classifications, périmètres, champ des bénéficiaires, licence de redistribution, confusion entre qualité de publication et irrégularités.
