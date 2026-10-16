# Méthode — version 0

## Objet statistique

Les administrations publiques (APU), **consolidées** : État, autres administrations centrales, administrations locales et administrations de sécurité sociale. Ce n'est pas le seul budget de l'État. Les transferts entre sous-secteurs ne doivent pas être additionnés comme des dépenses finales.

## Données actuellement affichées

`data/apu_1995_2025_pct_pib.csv` : année, recettes APU / PIB, dépenses APU / PIB, capacité (+) ou besoin (−) de financement APU / PIB. Source : tableau « Dépenses et recettes publiques entre 1995 et 2025 », Insee Première 2106 (base 2020) : https://www.insee.fr/fr/statistiques/8997691.

Pour chaque donnée : champ France, périodicité annuelle, unité % du PIB, version de publication 2026, source Insee. Les données 2025 peuvent être révisées.

## Intégrité

- Unicité et ordre des années, absence de trous 1995–2025.
- Pas de valeur fictive pour 1980–1994 ; ces années ne sont pas visibles comme « zéro ».
- Solde ≈ recettes − dépenses ; tolérance 0,11 point de PIB du fait des arrondis.
- Ne pas mélanger des chiffres de mars et d'août 2026 : les millésimes de comptes diffèrent.
- Les valeurs de 2025 affichées ici sont recettes 52,2 %, dépenses 57,3 %, déficit −5,1 % du PIB.

## Analyse critique future

Étudier séparément régressivité fiscale (indicateur dépendant du dénominateur), patrimoine public, dette brute/nette, solde primaire et traçabilité budgétaire. Une dépense comptabilisée n'est pas nécessairement évaluée ; une absence de donnée n'est pas une preuve de dissimulation. Publier hypothèses et contre-analyses avant tout score synthétique.
