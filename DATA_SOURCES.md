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

## Solde primaire : calcul dérivé du tableau Insee 3.201 (1959–2025)

- **Même fichier officiel audité que la page des intérêts**, [Insee 3.201, 28 août 2026](https://www.insee.fr/fr/statistiques/8988845), base 2020, source : https://www.insee.fr/fr/statistiques/fichier/8988845/t_3201_fr.xlsx
- Empreinte SHA-256 déjà auditée : `487d4299a5bac8d616000952fd012a0eb6d251a3586508165fc37d64a73a397a`.
- Un seul classeur : ligne **3** = années 1959–2025, **12** = intérêts D41 payés, **13** = intérêts D41G avant correction SIFIM, **27** = dépenses totales S13, **58** = recettes totales S13, **66** = capacité (+) ou besoin (−) de financement **B9NF**. Vérification de cohérence année par année : `recettes totales – dépenses totales = B9NF` (tolérance de l'arrondi officiel au 0,0001 Md€).
- **Formule dérivée, non publiée comme colonne primaire** : `primary_d41_bn_eur = balance_b9_bn_eur + interest_d41_bn_eur`. Variante : `primary_d41g_bn_eur = balance_b9_bn_eur + interest_d41g_bn_eur` ; seule la définition des intérêts change, le B9NF restant fixe.
- CSV : `data/solde_primaire_apu_1959_2025_bn_eur.csv`, 67 années sans trou, six indicateurs dérivés ou repris plus année. Importateur reproductible : `scripts/import_primary_balance.py`, Python standard, SHA-256 épinglée, valide années, libellés de source, équation B9 et exactitude des arrondis. Les deux intérêts et les dépenses totales sont **identiques** aux colonnes déjà publiées de `data/interets_apu_1959_2025_bn_eur.csv`.
- 2025 : recettes `1562.5197` Md€, dépenses `1714.1117` Md€, B9NF `−151.5920` Md€, D41 `65.7209` Md€, D41G `64.6519` Md€, primaire D41 `−85.8711` Md€, primaire D41G `−86.9401` Md€.
- **Attention aux millésimes :** les analyses de mai 2026 peuvent citer un déficit public `−152,5` Md€ en 2025. Ce chiffre **n'est pas celui du tableau 3.201 d'août** ; il ne doit pas être mêlé aux intérêts du millésime plus récent.
- Le ratio secondaire proposé par l'interface est un **% des dépenses publiques totales S13 de la même année**, **pas % du PIB**, ni un taux d'intérêt de la dette. Les euros historiques sont courants, 2025 provisoire.
- Constatation conceptuelle : le primaire ainsi défini **réintègre les intérêts payés seulement**. Les intérêts reçus ne sont pas soustraits. Il ne s'agit ni de solde primaire structurel ni d'un indicateur direct de trajectoire de dette.

## Dette nette, passifs financiers et ajustement stock-flux (Insee 3.103–3.105)

Sources : Insee, comptes nationaux annuels base 2020, publication du 28 août 2026, tableaux officiels https://www.insee.fr/fr/statistiques/8988843. Les trois fichiers XLSX ne sont pas commités.

| Tableau | Classeur XLSX | SHA-256 auditée | Années | CSV dérivé |
|---|---|---|---|---|
| 3.103 | https://www.insee.fr/fr/statistiques/fichier/8988843/t_3103_fr.xlsx | 4990cee1dddc3a8d68349f2c3e1918272a67ff777cf1b8e517a9ff2d26fdd804 | 1995–2025 | data/dette_nette_apu_1995_2025.csv |
| 3.104 | https://www.insee.fr/fr/statistiques/fichier/8988843/t_3104_fr.xlsx | b3f8fcb59c927c67fe753b79ad6292f01e488f5c66a9f2ea02f766a7306ffc19 | 1995–2025 | data/dette_passifs_maastricht_1995_2025.csv |
| 3.105 | https://www.insee.fr/fr/statistiques/fichier/8988843/t_3105_fr.xlsx | 964ccff6ff8ca50d00b8031b337bfcf94fa7e92056946d73e3a1594d36745234 | 2009–2025 | data/dette_deficit_variation_2009_2025.csv |

**3.103 : dette nette, STOCK de fin d'année.** Dette Maastricht diminuée d'actifs exigibles détenus sur d'autres secteurs (dont dépôts, crédits, titres) dans la convention Insee ; les actifs soustraits sont évalués à la valeur de marché. Les « autres actifs liquides » F511/F52 (actions cotées et parts de fonds) figurent dans une ligne **distincte**, à ne PAS soustraire à nouveau. La dette nette peut être négative pour un sous-secteur. 31 années × 6 périmètres S13/S1311/S13111/S13112/S1313/S1314. Montants en milliards d'euros courants arrondis à 0,1 ; taux officiel en % du PIB arrondi à 4 décimales (2025 : 3 242,7 Md€ ; 108,4132 %).

**3.104 : passage des passifs à Maastricht, STOCK.** Total passifs de comptabilité nationale TP − différence de champ (1) − consolidation (2) − ajustement en valeur nominale (3) = dette brute nominale de Maastricht. En 2025, S13 : 3 911,4 − 441,7 − 211,5 − (−201,9) = 3 460,1 Md€. Attention à la valorisation des instruments et à la consolidation, pas équivalent au patrimoine public net. Les trois sous-postes publiés de (3) ne reconstituent pas exactement leur total en 2014–2021 (résidu jusqu'à 2,9 Md€) ; valuation_breakdown_gap_bn_eur est un **calcul dérivé et signalé**, pas une ligne Insee. S1314 2025 de 3.104 = 293,1 Md€ ; celui de 3.102 = 292,6 Md€ : ne pas forcer l'égalité de séries ni additionner les sous-secteurs comme ventilation parfaitement réconciliée.

**3.105 : passage du déficit à la variation annuelle de dette, FLUX.** Convention source déficit positif, puis acquisitions d'actifs (1), autres passifs (2), changements de volume (3), autres comptes (4), écart statistique (5). En 2025 : 151,6 − 14,2 + 7,9 + 5,8 + 4,5 − 1,6 = **154,0 Md€ de variation** et non d'encours. Contrôle indépendant : la différence des encours S13 du 3.104 et la variation publiée 3.105 divergent de −0,6 Md€ en 2014 ; les autres écarts (2009–2025) sont au plus de 0,3 Md€. Cet écart connu est conservé et documenté.

Reproduction hors ligne : python3 scripts/import_debt_bridges.py --xlsx-dir /chemin/xlsx, bibliothèque Python standard uniquement, empreintes obligatoires et échec en cas de source modifiée. Tests : libellés et années, identités internes, ancrages de 2025, valeurs signées, résidus connus, comparaison stock/flux. Les trois tableaux ont des définitions et des durées différentes ; ne pas les additionner, et ne pas les confondre avec les détenteurs de la dette, l'AFT ou les intérêts D41.

## Sources identifiées, non intégrées

- [Insee, comptes APU détaillés](https://www.insee.fr/fr/statistiques/8988845), tableaux **autres que 3.201** ; vérifier périmètres, catégories et durées des séries.
- [Insee Première n° 2106 (mai 2026)](https://www.insee.fr/fr/statistiques/8997691) : publication antérieure ; certains chiffres ont été révisés et ne doivent pas être mélangés au millésime d'août.
- Eurostat, OCDE, DGFiP, AFT, budget.gouv.fr, Cour des comptes : sources candidates pour les fonctions, impôts, intérêts, investissements et traçabilité.

**Important :** une fiche de source ne prouve ni disponibilité d'une décomposition exhaustive, ni possibilité de rapprochement entre années ou nomenclatures. Vérifier chaque série sur le fichier d'origine.

## Dette Maastricht par instrument et administration — Insee 3.102 (1995–2025)

- **Producteur : Insee**, comptes nationaux annuels base 2020, publication du **28 août 2026**, tableau **3.102**, [page officielle](https://www.insee.fr/fr/statistiques/8988843).
- **Classeur original** : https://www.insee.fr/fr/statistiques/fichier/8988843/t_3102_fr.xlsx ; empreinte SHA-256 auditée : `6c8beca5fb0ac72754887d8a871a83eda6f8523ca6c903c1bc898f8cfe749b49`.
- **Champ** : France entière, dette brute **nominale consolidée de Maastricht** en fin d'année, **milliards d'euros courants**, 1995–2025 (2025 provisoire). Ceci ne représente pas uniquement la dette négociable de l'État.
- **Séries** : S13 (total APU), S1311 (centrales), S13111 (État), S13112 (ODAC), S1313 (locales), S1314 (sécurité sociale). **Ne jamais additionner S1311 à ses composantes S13111/S13112.**
- **Instruments** : F2N (dépôts), F31_32 (titres courts et longs), F31 (titres courts, inclus dans F31_32), F32 (titres longs, inclus dans F31_32), F41 (crédits courts), F42 (crédits longs), GD (total). Courte/longue échéance = **maturité initiale à l'émission**, et non durée restante. **F31 et F32 ne sont pas à ajouter une seconde fois à F31_32.**
- **Manquants vérifiés** : le classeur laisse **S1314/F2N vide en 1995–2025**. Notre CSV le laisse vide également ; ce n'est pas un zéro observé. Pour le seul contrôle de réconciliation GD, le poste non renseigné n'est pas additionné ; la cohérence numérique des autres postes est vérifiée.
- **Contrôles de reproduction** : SHA obligatoire, titres/année/codes/emplacements et montants finis/non négatifs vérifiés ; somme des instruments et des quatre sous-secteurs, sous-total S1311, sous-total F31+F32, ancrage S13 fin 2025 **3 460,1 Md€**. Tolérance **0,25 Md€** pour sous-totaux à quatre composantes arrondies séparément à 0,1 Md€, **0,50 Md€** pour quatre sous-secteurs.
- **Livrables** : `scripts/import_debt_instruments.py`, `data/dette_maastricht_instruments_1995_2025_bn_eur.csv`, `tests/test_debt_instruments.py`. Reproduction : `python3 scripts/import_debt_instruments.py --xlsx /chemin/t_3102_fr.xlsx`. XLSX non commité. L'option `--allow-source-change` sert uniquement à auditer un nouveau millésime ; ne pas publier sans revoir les écarts.
- **Limites** : le CSV ne contient ni détenteurs, ni durée résiduelle, ni valeur de marché. Ne pas fusionner avec les jeux Eurostat, Banque de France ou AFT sans réconciliation de périmètre, de millésime et de méthode.

## Audit croisé Eurostat EDP / Insee, octobre 2026

Le suivi détaillé des révisions 2025, des divergences 3.102/3.104, de la différence stock-flux 2014 et des sous-lignes de valorisation figure dans [DEBT_RECONCILIATION.md](DEBT_RECONCILIATION.md). Eurostat avril/juin 2026 est antérieur au millésime Insee août 2026 ; aucun rapprochement n'a été imposé entre définitions ou millésimes.

## Nouveau chapitre : aides aux entreprises, estimations 2023

Le fichier data/aides_entreprises_senat_2023_estimations.csv contient deux estimations ponctuelles de la commission d'enquête Sénat, rapport n° 808 (2025) : 108 Md€ au sens strict et 211 Md€ au sens large pour 2023. Ce sont des ordres de grandeur, pas des flux budgétaires consolidés observés. Détail : AIDES_ENTREPRISES_SOURCES.md. Source : https://www.senat.fr/rap/r24-808-1/r24-808-1_mono.html

## APPRENTISSAGE — Dares et France compétences (2024–2025)

Deux CSV ponctuels décrivent séparément les contrats commencés et en cours en fin d'année (Dares 2024–2025, estimation 2025 provisoire), et les engagements/coûts 2024 (France compétences, secteur privé). Ne pas rapprocher comme série unique. Détails et URLs dans APPRENTISSAGE_SOURCES.md.

## APPRENTISSAGE : effectifs Depp-SIFA 1982–2024 (Insee T04/T1)

Effectifs de personnes en formation **au 31 décembre**, cinq groupes de niveaux de diplôme plus total annuel. Source https://www.insee.fr/fr/statistiques/8666372 ; XLSX : https://www.insee.fr/fr/statistiques/fichier/8666372/T04%20-%201.4.xlsx ; SHA-256 93432bd9c0f7e950502544df2de2604b9ec2730e873693b8387b53b2b6800a0d. Import standard Python : scripts/import_apprentissage_sifa.py ; 43 observations : data/apprentissage_sifa_effectifs_1982_2024.csv. France hors Mayotte jusqu'en 2010, Mayotte incluse depuis 2011. Ne pas sommer avec contrats Dares ou financement France compétences. Voir APPRENTISSAGE_SOURCES.md.

## Jeunes en 2024 : population détaillée et situations vis-à-vis des études et du travail

Population au 1er janvier par âge, source Insee Bilan démographique 2024, classeur Pop1janv_age.xlsx, SHA-256 223e5d4699d1b99b20b1e81a7f75dec961031272d74c4cd429fb9466fc8f574d, import scripts/import_jeunes_population.py et CSV data/jeunes_population_2024_par_age.csv. Autre source : Insee France portrait social 2025, figure 2 enquête Emploi 2024, ventilations exclusives selon sexes et tranches 18–20/21–24/25–29, CSV data/jeunes_situations_2024_insee.csv. Détails et limites JEUNES_CONTEXTE_SOURCES.md ; ne pas transformer ces sources en fausse part des apprentis âgés de 18–25 ans.

## COFOG niveau 2 — ventilation annuelle des fonctions (18 octobre 2026)

- **Fichier officiel réellement inspecté** : même [Insee 3.301, 27 mars 2026](https://www.insee.fr/fr/statistiques/8574707) et XLSX `https://www.insee.fr/fr/statistiques/fichier/8574707/T_3301.xlsx`, **SHA-256 `ce36c71eafebdcbd941ef5cb74f10e79734fa4e1cc0dc1e97d84e321412c5ce5`**. Vérifié sur le classeur téléchargé le 18 octobre 2026 ; même millésime source que les dix fonctions.
- **Champ** : France, administrations publiques **S13 consolidées**, dépenses totales (`OTE`), **milliards d'euros courants**, 1995–2024 ; 2024 provisoire. Ce n'est ni la dépense de l'État seul, ni une répartition des crédits votés en loi de finances.
- **Extraction** : `scripts/import_cofog_subfunctions.py` réutilise le parseur XLSX et les contrôles de SHA du premier niveau. Lignes à codes `GF0101` à `GF1009` (69 sous-fonctions, réparties sous `GF01` à `GF10`) ; libellés directement issus de la colonne descriptive ; une série annuelle par sous-fonction. Résultat : `data/cofog_subfunctions_1995_2024.json`. L'original XLSX n'est pas versionné.
- **Validation indépendante** : pour chaque année et fonction parent, somme des sous-fonctions égale au montant `gf01`…`gf10` du CSV principal à **0,015 Md€** près (arrondis de la publication). Les zéros sont des zéros officiellement publiés. Pas de comblement de trous.
- **Exemple 2024** : `GF10` = **693,029 Md€**, dont `GF1002` vieillesse **391,954 Md€**, `GF1001` maladie et invalidité **83,899 Md€**, `GF1004` famille et enfants **66,711 Md€**. Rapport à toutes les dépenses S13 (1 671,794 Md€) = **41,45 %**, soit 41 % dans le texte Insee arrondi à l'unité. Ne pas confondre avec la fonction santé `GF07` (soins) ni avec les finances de l'État seul.
- **Interprétation** : hiérarchie de classification fonctionnelle, pas ventilation budgétaire LOLF par missions/programmes/actions ni dépense « nette » de chaque administration. Les transferts entre sous-secteurs, le traitement des intérêts et la frontière entre santé et social obéissent aux conventions Insee. Les changements locaux de nomenclature logement/affaires économiques affectent 2024. Attention aux comparaisons en euros courants sans déflation et aux comparaisons avec des séries d'autres millésimes.
