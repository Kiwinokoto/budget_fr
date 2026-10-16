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

## Troisième source effectivement inspectée — principaux impôts, 1995–2025

**Insee tableau 3.217, « Principaux impôts par catégorie »**, [page officielle](https://www.insee.fr/fr/statistiques/8988845), comptes nationaux base 2020.
- XLSX exact : https://www.insee.fr/fr/statistiques/fichier/8988845/t_3217_fr.xlsx
- SHA-256 vérifiée : `589b94cf953d0fdb6e07b123dcadfd11b831e866096ec0cfb0911d62ae432790`.
- Ligne 3 : années 1995–2025 ; lignes source 5, 7, 10, 39, 50, 70, 86, 92, 99 pour les catégories principales ; 102 et 107 pour corrections ; 110 pour total net, 111 pour taux de prélèvements. 71, 72, 75, 78 pour les sous-postes explicatifs CSG, CRDS, IRPP, IS ; 100 et 104 pour contrôle du total brut.
- Unité principale : **milliards d'euros courants**, taux des prélèvements obligatoires en **% du PIB**. 2025 provisoire.
- Sortie `data/recettes_1995_2025_bn_eur.csv` ; import `scripts/import_recettes.py` sans dépendances, XLSX officiel non commité.
- Les neuf catégories positives + les deux corrections négatives se réconcilient avec le total des prélèvements obligatoires de l'Insee sur les **31 années** ; les sous-postes sont exclus de cette somme.
- Le tableau fournit une ventilation **des prélèvements**, pas de toutes les recettes de l'État ou des APU. Les comparaisons en euros courants ne sont pas corrigées de l'inflation.
- [Tableau 3.216](https://www.insee.fr/fr/statistiques/8988845) : source historique complémentaire des prélèvements par bénéficiaire, depuis 1959, **non intégrée** dans ce lot ; droits et classement à étudier.

## Quatrième source — simulation de hausse de TVA selon le niveau de vie

**[Insee Analyses n°43, 11 février 2019, figure 2](https://www.insee.fr/fr/statistiques/3713290)**, Mathias André et Anne-Lise Biotteau : *À moyen terme, une hausse de la TVA augmente légèrement les inégalités de niveau de vie et la pauvreté*.
- **Nature des données :** tableau officiellement publié de résultats de **microsimulation contrefactuelle**, et non relevé de TVA effectivement payée par les ménages, ni évolution annuelle.
- **Scénario :** relèvement du taux normal de TVA de **20 à 23 %** ; modèle Ines, législation 2016, enquête ERFS 2014 actualisée 2016 et module de taxation indirecte basé sur Budget de famille 2011 ; impacts estimés à trois ans.
- **Champ :** France métropolitaine, personnes en ménage ordinaire, revenus positifs ou nuls, personne de référence non étudiante. **Dix déciles de personnes** classées selon le niveau de vie usuel, pas dix niveaux de TVA payée.
- **Unités et variables :** contributions des composantes en **points de pourcentage** de variation du niveau de vie corrigé ; effet total du niveau de vie corrigé **en %**. Six colonnes reprises directement de la figure 2.
- **Provenance :** transcription manuelle limitée aux dix colonnes de décile de la figure 2, sans valeurs fabriquées et sans extrapolation à 2025 ; CSV dérivé `data/tva_choc_deciles_insee_2019.csv`, tests `tests/test_tva_scenario.py`.
- **Limites :** valeurs publiées arrondies au dixième ; elles peuvent ne pas s'additionner exactement. La série n'est pas fusionnée avec la série de recettes TVA 1995–2025 de la comptabilité nationale. Aucun « taux d'injustice » n'est calculé.

## Cinquième source — TVA estimée dans l'enquête Budget de famille 2001

Nicolas Ruiz et Alain Trannoy, « Le caractère régressif des taxes indirectes : les enseignements d’un modèle de microsimulation », *Économie et Statistique* n°413 (2008), Insee, [PDF officiel](https://www.insee.fr/fr/statistiques/fichier/1376872/es413b.pdf), **page 27**, tableaux **3, 4, 6**.
- Année étudiée : **2001** ; enquête Budget de famille 2001, modèle de taxation des postes de consommation, ensemble des ménages, regroupement selon déciles de niveau de vie.
- Table 3 : TVA estimée moyenne **en euros par ménage** (1 308 € pour D1, 3 588 € pour D10), euros courants de 2001.
- Table 4 : TVA totale / **revenu disponible brut agrégé** du décile (11,52 % pour D1, 5,92 % pour D10). Taux agrégé des déciles, pas moyenne non pondérée des ratios individuels.
- Table 6 : TVA estimée / **dépense totale de consommation** (10,5 % pour D1, 11,6 % pour D10), taux apparent, pas taux légal.
- CSV : `data/tva_effort_bdf_2001.csv` ; transcription des dix lignes et des seules colonnes utilisées, valeurs originales non actualisées.
- Ces chiffres reposent sur une **estimation fiscale à partir de consommation enquêtée**, pas des montants réels individuels observés dans des déclarations TVA.

## Sixième source — comptes nationaux distribués, taxes sur les produits 2020–2023

Insee, [Comptes par catégories de ménage](https://www.insee.fr/fr/statistiques/8574663), CND.101, publié le 16 avril 2026, [XLSX source](https://www.insee.fr/fr/statistiques/fichier/8574663/T_CND_101.xlsx).
- SHA-256 du XLSX téléchargé et inspecté : `8e4d2ec005e9351f7105c796ac2e0ae8afc1f53b70b165d04f9387ed8cf838ef`.
- Onglets `CND_2020` à `CND_2023`, ligne 16 exactement intitulée **« Taxes sur les produits (TVA, TICPE, acises, DMTO, etc.) »**, colonnes B–U pour les vingt groupes V1–V20, V pour le total national.
- Champ : France, comptes nationaux distribués **S1** (économie nationale), base 2020. Groupes définis par vingtème de niveau de vie usuel de personnes (5 % des individus par groupe). Valeurs en milliards d'euros courants.
- Dans la source les prélèvements ont un signe négatif ; le CSV `data/taxes_produits_cnd_2020_2023.csv` en retient le **montant positif**. Import reproductible en Python standard : `scripts/import_cnd_product_taxes.py`, empreinte SHA-256 épinglée.
- Somme des vingt groupes comparée au total national de la même source à une tolérance de 0,5 Md€ (arrondis au dixième ; écart 0,1 Md€ en 2022).
- **Ce poste n'est pas une TVA par vingtième** : il inclut TICPE, accises, DMTO et autres impôts sur les produits. Les répartitions résultent des hypothèses des comptes distribués, non de déclarations personnelles de TVA.
- Ne pas construire un ratio de taxes sur produits / revenu disponible S14 sans expliciter les différences d'univers comptable, ni rapprocher directement ces valeurs du CSV de TVA nationale d'un autre millésime.
- Les comptes publiés 2020–2023 sont des **statistiques expérimentales** soumises à révisions et hypothèses de répartition, et **ne constituent pas une mesure de fiscalité individuelle constatée en 2025**.

## Septième source — DG Trésor, simulation distributive de TVA (publication 2025)

[Trésor-Éco n°371, 25 septembre 2025](https://www.tresor.economie.gouv.fr/Articles/2025/09/25/analyse-de-la-composition-des-recettes-de-tva), [document complet PDF](https://www.tresor.economie.gouv.fr/Articles/c462ac7f-76db-4c33-9bb3-dcc6886ed898/files/f4d0d1ac-fc61-4cf3-ab3f-094385b218bd), chapitre 4 et graphique 4, pages 5–6.
- La source analyse une **hausse hypothétique uniforme de 1 point de tous les taux de TVA**, sous répercussion intégrale et consommation constante.
- Simulation par **quintile de niveau de vie des ménages**, BDF 2017, ERFS 2022, comptes nationaux 2021–2022.
- Chiffres textuels vérifiés : perte moyenne de pouvoir d'achat Q1 −0,7 %, Q5 −0,4 %, ensemble −0,5 % ; parts Q1 12 %, Q5 31 % des **recettes marginales supplémentaires** d'une telle hausse.
- Seuls les **résultats numériques publiés dans le texte** sont repris dans \`tva-incidence.html\`. Pas de CSV pseudo-exact des quintiles intermédiaires obtenu par lecture graphique.
- Résultat distinct de la **TVA existante** : ni somme d'impôt effectivement payée en 2025, ni part du revenu qu'elle représente.
- Le montant 11,4 Md€ pour un point de TVA net en 2025 est un **rendement théorique statique**, issu d'une modélisation fondée notamment sur 2022 et extrapolée en 2025 ; ne pas le présenter comme une exécution.


## Huitième source — TVA seule par décile : Ines 2014 (Drees, novembre 2016)

- [Drees, « Module de taxation indirecte du modèle Ines : hypothèses, principes et aspects pratiques », document de travail n°60, novembre 2016](https://drees.solidarites-sante.gouv.fr/sites/default/files/2020-10/dt60.pdf), **tableau 16, page 38** (page 38 imprimée, index PDF 37).
- Champ : ménages ordinaires de France métropolitaine **hors DOM**, revenu disponible **strictement positif** ; simulation Ines **2014**, dépenses de consommation imputées à partir de **Budget de famille 2011**.
- Variable reprise : **TVA seule, en pourcentage du montant de TVA simulée acquittée par l'ensemble des ménages du champ, réparti par décile de niveau de vie**. Ce n'est **ni le taux d'effort TVA/revenu**, ni le montant national de TVA encaissé en 2014.
- Données CSV `data/tva_part_deciles_ines_2014.csv` : D1 4,3 %, D2 6,3 %, D3 7,2 %, D4 8,0 %, D5 8,9 %, D6 9,8 %, D7 11,0 %, D8 12,0 %, D9 14,0 %, D10 18,5 %. Somme exactement **100,0 %**. Reprise manuelle **directe du tableau numériquement publié**, sans extraction de valeurs approximatives depuis une courbe.
- Le même rapport, figures 1 et 2 et pages 39–40, donne seulement dans le texte les taux apparents aux extrêmes : **9,3 % vs 11,5 % de la consommation**, et **11,3 % vs 6,8 % du revenu disponible** (D1 vs D10). **Ne pas inventer** de taux intermédiaires à partir des graphes.
- Les tableaux 2014 ne constituent pas une distribution contemporaine : la méthode repose sur une enquête plus ancienne et des comportements de consommation modélisés. Les parts 2014 ne doivent pas être comparées quantitativement aux chiffres de **2001** ou aux recettes de TVA **2025** sans harmonisation explicite.

### Accès à une estimation récente 2023–2025 : documentation et obstacle

- [Documentation publique du modèle Ines : module de taxation indirecte](https://ines-public-e766af.gitlab.io/modules_annexes.html) : le module distingue TVA, TICPE, taxes sur assurances et accises ; il pseudo-apparie **Budget de famille 2017** aux ménages ERFS. Code et instructions de mise à jour documentés ; cela **n'autorise pas** à considérer les données de sortie comme librement téléchargeables.
- [Insee, tableaux publics Budget de famille 2017](https://www.insee.fr/fr/statistiques/4648335) : dépenses moyennes et structure par niveau de vie, **pas** les taxes TVA simulées par ménage et décile. Nomenclatures et taux de TVA spécifiques aux achats sont nécessaires pour une microsimulation.
- [CASD, enquête BDF 2017](https://www.casd.eu/source/enquete-budget-de-famille/) : accès à un jeu détaillé **sur autorisation** ; version moins détaillée via **Quételet-Progedo**, à vérifier avant toute utilisation. La base ERFS qui alimente Ines fait également l'objet de dispositifs de diffusion adaptés à la confidentialité.
- Conséquence : pas de résultat chiffré « TVA payée en 2025 par décile » sans disposer soit d'un **tableau agrégé officiellement produit** soit de **microdonnées accessibles légalement**, d'un modèle de taxation validé et de ressources pour analyser ses hypothèses.

## Source ajoutée — Charge d'intérêts des administrations publiques S13 (1959–2025)

- **[Insee, tableau 3.201 « Dépenses et recettes des administrations publiques »](https://www.insee.fr/fr/statistiques/8988845)**, base 2020, mis à jour le **28 août 2026**.
- Fichier exact : https://www.insee.fr/fr/statistiques/fichier/8988845/t_3201_fr.xlsx
- SHA-256 inspectée : `487d4299a5bac8d616000952fd012a0eb6d251a3586508165fc37d64a73a397a`.
- Feuille `t_3201`, ligne 3 = années **1959–2025**, ligne 12 = **Intérêts (D41)**, ligne 13 = **Intérêts hors correction au titre des SIFIM (D41G)**, ligne 27 = **Total des dépenses**. Champ = **S13, administrations publiques consolidées**, et non l'État seul.
- Unités : **milliards d'euros courants**, y compris les observations avant l'introduction de l'euro (conversion rétrospective de la série Insee). Valeurs publiées dans le XLSX à quatre décimales, affichées à une décimale. Année 2025 provisoire.
- Données dérivées `data/interets_apu_1959_2025_bn_eur.csv`, importateur standard `scripts/import_interest.py`, source XLSX originale **non** commitée. Validation stricte des libellés, années, empreinte, valeurs et cohérence par rapport à la dépense totale.
- Pour la comparaison sur la page, `part_d'interets_D41G = D41G / total_dépenses_S13 × 100`, **calculé à partir du même classeur et du même millésime**. Cette part n'est pas une fraction du PIB ni un taux appliqué à l'encours de dette de Maastricht.
- En 2025 : D41 = `65.7209` Md€, D41G = `64.6519` Md€, dépenses totales = `1714.1117` Md€. Le montant synthétique Insee de **64,7 Md€** utilise D41G.
- D41/D41G ne sont pas deux charges additionnables ; la correction au titre des SIFIM peut modifier l'ordre relatif des deux séries selon l'année. Ne jamais appeler D41G « dette nette ».
- Le ratio d'intérêts sur les dépenses ne mesure ni le taux d'intérêt effectif de la dette ni le coût futur de son refinancement.

## Sources identifiées, non intégrées

- [Insee, comptes APU détaillés](https://www.insee.fr/fr/statistiques/8988845), tableaux **autres que 3.201** ; vérifier périmètres, catégories et durées des séries.
- [Insee Première n° 2106 (mai 2026)](https://www.insee.fr/fr/statistiques/8997691) : publication antérieure ; certains chiffres ont été révisés et ne doivent pas être mélangés au millésime d'août.
- Eurostat, OCDE, DGFiP, AFT, budget.gouv.fr, Cour des comptes : sources candidates pour les fonctions, impôts, intérêts, investissements et traçabilité.

**Important :** une fiche de source ne prouve ni disponibilité d'une décomposition exhaustive, ni possibilité de rapprochement entre années ou nomenclatures. Vérifier chaque série sur le fichier d'origine.
