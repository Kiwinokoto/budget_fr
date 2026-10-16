# Sources des données — audit du 16 octobre 2026

## Source réellement inspectée et utilisée

**Insee, Dépenses et recettes publiques**, publié le 28 août 2026 :
- Page officielle : https://www.insee.fr/fr/statistiques/2381414
- XLSX : https://www.insee.fr/fr/statistiques/fichier/2381414/econ-fin-pub-rec-dep.xlsx
- SHA-256 vérifié du fichier téléchargé : 46f401c599cf076956a7b4732d877d57d7f1daea719f7f72397be1dd2f370126
- Feuille « Données » ; années ligne 4, dépenses ligne 5, dépenses hors éléments imputés ligne 6, recettes ligne 7, recettes hors éléments imputés ligne 8, solde de Maastricht ligne 9, dette brute ligne 10, dette nette ligne 11.
- Champ : France, administrations publiques consolidées ; comptes nationaux annuels base 2020 ; % du PIB.
- Recettes, dépenses et solde 1960–2025 ; dette brute 1978–2025 ; dette nette 1995–2025.
- 2024 est semi-définitif (sd), 2025 provisoire (p). Les cellules « nd » du classeur sont retranscrites comme absentes, non égales à zéro.
- Traitement : scripts/import_insee.py ; fichier dérivé : data/apu_1960_2025_pct_pib.csv. L'original XLSX n'est pas commité.
- Attribution à l'Insee et lien conservés. Toute réutilisation des données demeure soumise aux conditions applicables de l'Insee.


## Deuxième source réellement inspectée — COFOG S13

**Insee, dépenses des administrations publiques ventilées par fonction en 2024**, publication **27 mars 2026**, [page officielle](https://www.insee.fr/fr/statistiques/8574707).
- Fichier : https://www.insee.fr/fr/statistiques/fichier/8574707/T_3301.xlsx
- Tableau **3.301**, onglet `T_3301` (premier XML de feuille), 1995–2024, en **milliards d'euros courants**, comptes nationaux base 2020.
- SHA-256 inspectée : `ce36c71eafebdcbd941ef5cb74f10e79734fa4e1cc0dc1e97d84e321412c5ce5`.
- Sous-ensemble strict : opération `OTE`, libellé « Total des dépenses des administrations publiques (*) », codes `_Z` et `GF01` à `GF10`. Ne pas importer les sous-fonctions et opérations comme des postes supplémentaires.
- Les 10 rubriques de premier niveau totalisent les dépenses du tableau à **0,015 Md€** près (arrondi source ; écart max contrôlé de 0,003 Md€).
- Dérivé publiquement versionné : `data/cofog_1995_2024_bn_eur.csv`, générateur Python standard `scripts/import_cofog.py`, XLSX non commité.
- **Limites** : 2024 provisoire et reclassifications susceptibles de modifier les séries ; passage entre logement et affaires économiques en 2024 au niveau local. Le millésime COFOG de mars 2026 n'est pas directement homogène avec le millésime macroéconomique d'août 2026.

## Sources identifiées, non intégrées

- [Insee, comptes APU détaillés](https://www.insee.fr/fr/statistiques/8988845), tableaux 3.201 et suivants ; vérifier périmètres, catégories et durées des séries.
- [Insee Première n° 2106 (mai 2026)](https://www.insee.fr/fr/statistiques/8997691) : publication antérieure ; certains chiffres ont été révisés et ne doivent pas être mélangés au millésime d'août.
- Eurostat, OCDE, DGFiP, AFT, budget.gouv.fr, Cour des comptes : sources candidates pour les fonctions, impôts, intérêts, investissements et traçabilité.

**Important :** une fiche de source ne prouve ni disponibilité d'une décomposition exhaustive, ni possibilité de rapprochement entre années ou nomenclatures. Vérifier chaque série sur le fichier d'origine.
