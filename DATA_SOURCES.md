# Audit initial des sources — 2026-10-16

## Vérifié

| Source | Série / étendue | Périmètre et statut | Usage |
|---|---|---|---|
| [Insee 2381414](https://www.insee.fr/fr/statistiques/2381414) | Recettes, dépenses, déficit, dette (1960–2025 annoncées), publication 28/08/2026 | Administrations publiques consolidées, comptabilité nationale base 2020 | Référence cible historique ; téléchargement XLSX et parsing à valider |
| [Insee Première 2106](https://www.insee.fr/fr/statistiques/8997691) | Tableau publié 1995–2025 | Recettes, dépenses, solde en points de PIB | **Source exacte du premier CSV** ; relevé manuel à contrôler par extraction automatisée ultérieure |
| [Insee COFOG](https://www.insee.fr/fr/statistiques/8574707) | Fonctions des dépenses 1995–2024 | Administrations publiques, sous-secteurs ; État séparé depuis 2009 | Futur détail fonctionnel, non encore importé |
| [Insee 2381404](https://www.insee.fr/fr/statistiques/2381404) | Dépenses par administration, 2025 | Transferts inter-administrations consolidés au total | Contrôle du périmètre et risque de double compte |
| [Insee Première 2093](https://www.insee.fr/fr/statistiques/8735252) | Dépenses par fonction 2014–2024 | COFOG | Documentation et rapprochement |
| [Insee premiers résultats de mars](https://www.insee.fr/fr/statistiques/8956575) | Premières estimations de 2025 | **Millésime provisoire antérieur**, parfois différent des données d'août | Ne pas mélanger avec les données d'août |

## À auditer avant ingestion

Eurostat, OCDE, DGFiP, AFT, budget.gouv.fr, Cour des comptes, DREES et études d'incidence fiscale. Ne pas présumer que leur licence, format, couverture, périodicité ou nomenclature permettent une fusion immédiate.

## Limitations connues

- **Objectif 1980–2025 ; première livraison chiffrée 1995–2025 seulement.** Les années 1980–1994 seront intégrées après vérification du classeur Insee source.
- Tableau 1995–2025 transcrit depuis l'article Insee : les écarts de 0,1 point entre `recettes - dépenses` et solde peuvent venir des arrondis des taux publiés.
- Pas de décomposition TVA/IR/IS ni de « score de toxicité » dans ce lot.
- Les données sont exprimées en **% du PIB**, non en euros, non en budget de l'État seul.
- Pas encore de validation des droits de redistribution du classeur XLSX ; seules de petites valeurs statistiques tirées du tableau public sont reproduites, avec attribution.
