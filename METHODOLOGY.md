# Méthodologie — Insee base 2020, publication août 2026

## Définition et périmètre

France, administrations publiques (APU/S13) consolidées : administration centrale, locale et sécurité sociale. **Ce n'est pas uniquement le budget de l'État**. Ne pas additionner des transferts entre sous-secteurs à des dépenses consolidées.

Toutes les colonnes du premier fichier sont exprimées en **% du PIB**, pas en euros. Le fichier Insee fournit des comptes historiques harmonisés en base 2020, qui restent susceptibles de révision.

- Recettes et dépenses totales incluent des éléments imputés au sens des comptes nationaux.
- Les variantes « hors éléments imputés » sont des sous-indicateurs alternatifs : elles ne doivent pas être additionnées aux totaux.
- Solde : capacité (+) ou besoin (−) de financement ; il est importé directement de la ligne « déficit au sens de Maastricht », pas recalculé.
- Dette brute : dette publique au sens de Maastricht.
- Dette nette : dette brute diminuée de certains actifs financiers exigibles ; ce n'est **pas** une mesure du patrimoine net total.

## Source et provenance

- https://www.insee.fr/fr/statistiques/2381414
- XLSX : https://www.insee.fr/fr/statistiques/fichier/2381414/econ-fin-pub-rec-dep.xlsx
- Date : 28 août 2026 ; base des comptes nationaux : 2020.
- SHA-256 du XLSX contrôlé : 46f401c599cf076956a7b4732d877d57d7f1daea719f7f72397be1dd2f370126
- Script de reproduction : scripts/import_insee.py.
- CSV : data/apu_1960_2025_pct_pib.csv. Valeurs arrondies à **trois décimales de point de PIB**, affichées à une décimale dans l'interface.

| Indicateurs | Première année | Dernière année |
|---|---:|---:|
| Recettes, dépenses, solde | 1960 | 2025 |
| Recettes et dépenses hors éléments imputés | 1960 | 2025 |
| Dette brute | 1978 | 2025 |
| Dette nette | 1995 | 2025 |

L'année 2024 est semi-définitive, 2025 provisoire. Des chiffres d'une publication de mai 2026 peuvent différer du fichier du 28 août (notamment pour 2019) : ne jamais fusionner les millésimes sans contrôle.

## Vérification

L'import vérifie le SHA-256, les libellés des séries, la couverture 1960–2025 sans trou, les valeurs manquantes et la cohérence numérique du solde. L'écart toléré entre recettes moins dépenses et solde publié est de **0,06 point de PIB** pour tenir compte de l'arrondi du solde au dixième.

Les colonnes indisponibles sont vides, jamais remplacées par zéro ; leur série débute à la première année réellement disponible.

## Ce qu'on ne peut PAS inférer

Ces agrégats ne suffisent pas à analyser le poids de la TVA, les ventes du patrimoine public, la destination finale des dépenses ou une éventuelle « toxicité ». Ces questions exigent d'autres sources, des nomenclatures compatibles et une méthode explicitant les hypothèses concurrentes.
