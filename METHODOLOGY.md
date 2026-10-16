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

## COFOG : dépenses publiques par fonction, 1995–2024

Source : [Insee tableau 3.301](https://www.insee.fr/fr/statistiques/8574707), fichier `T_3301.xlsx`, publication 27 mars 2026, comptes nationaux base 2020, secteur consolidé **S13**. Import contrôlé avec `scripts/import_cofog.py`, empreinte SHA-256 du XLSX `ce36c71eafebdcbd941ef5cb74f10e79734fa4e1cc0dc1e97d84e321412c5ce5`.

Fichier `data/cofog_1995_2024_bn_eur.csv` : lignes annuelles, `total_bn_eur` puis `gf01` à `gf10`. **Unité milliards d'euros courants**. Les dix catégories de premier niveau sont **mutuellement exclusives** et constituent la totalité des dépenses COFOG S13 au niveau d'arrondi de la source (tolérance 0,015 Md€). Elles ne sont pas ajoutées au total une seconde fois.

Dans la page, le pourcentage par fonction est `montant_de_la_fonction / total_COFOG_de_la_même_année × 100`, et **non** un pourcentage du PIB. Cette part est comparable d'une année à l'autre sous réserve des révisions et ruptures de classification. Les montants en euros courants **ne mesurent pas la croissance réelle** : l'inflation n'est pas neutralisée.

**Attention aux millésimes** : les agrégats macroéconomiques proviennent d'août 2026, la répartition COFOG de mars 2026. Le total 2024 de ces deux publications peut différer. Ne pas utiliser le total COFOG comme ventilation exacte du total macroéconomique d'août 2026 sans harmoniser les versions.

Selon l'Insee, une modification de nomenclature des collectivités locales entraîne en 2024 un transfert apparent entre « Logements et équipements collectifs » et « Affaires économiques ». Il est explicitement déconseillé d'attribuer cet écart à une décision budgétaire réelle sans retraitement. Les intérêts de la dette sont classés dans les services publics généraux et non comme onzième catégorie à additionner.

Lien direct vers la [description des dix fonctions COFOG](https://www.insee.fr/fr/statistiques/8574707).

## Prélèvements obligatoires et principaux impôts — 1995–2025

Source unique : [Insee tableau 3.217 « Principaux impôts par catégorie »](https://www.insee.fr/fr/statistiques/8988845), fichier `t_3217_fr.xlsx`, comptes nationaux annuels base 2020, 1995–2025, unité **milliards d'euros courants** (sauf `levies_pct_gdp`, en % du PIB). Version récupérée le 16 octobre 2026 ; 2025 provisoire.

SHA-256 du fichier contrôlé : `589b94cf953d0fdb6e07b123dcadfd11b831e866096ec0cfb0911d62ae432790`.
Import : `scripts/import_recettes.py`, sortie `data/recettes_1995_2025_bn_eur.csv`, valeurs à trois décimales. Le parser valide les libellés du tableau, la continuité des années, la cohérence des totaux et l'empreinte source.

### Décomposition additive, et ses corrections

`prélèvements obligatoires (nets) = somme des huit grandes catégories fiscales (D211, D212, D214, D291, D292, D51, D59, D91r) + cotisations sociales effectives − prélèvements non recouvrables − crédits d'impôt`.

Dans le CSV, les deux dernières corrections ont un signe **négatif**. Les cotisations sociales **imputées** ne sont pas incluses dans les prélèvements obligatoires : elles ne figurent que pour réconcilier le total brut « ensemble impôts et cotisations sociales » de l'Insee. Le calcul reproduit rigoureusement le total net publié, et il est testé année par année. Les contributions exactes de la CSG, de la CRDS, de l'IRPP et de l'IS sont des **sous-postes des impôts courants sur le revenu D51**, présentés hors décomposition additive. L'IRPP et l'IS sont évalués **avant crédits d'impôt** ; les crédits sont déjà traités séparément au niveau du net.

- Les parts par catégorie = `montant / prélèvements obligatoires nets` de la même année. Les parts positives totalisent **plus de 100 %** avant les corrections négatives. Cela est voulu et expliqué dans l'interface.
- Les impôts ne sont **pas toutes les recettes** du secteur des administrations publiques : revenus de la propriété, ventes et autres recettes existent également.
- Une série en euros courants ne peut pas être présentée comme une hausse en volume ou à prix constants.
- Aucune classification « juste / injuste » ni conclusion sur la régressivité n'est permise à partir des seules parts fiscales. L'incidence dépend du revenu, de la consommation, de l'horizon temporel et des transferts publics.

La série des prélèvements inclut les prélèvements reçus par les administrations françaises et certains organismes européens ; elle ne doit donc pas être additionnée aux recettes du budget de l'État seul. Les ruptures et changements de prélèvement (CSG, CRDS, crédits d'impôts) doivent être signalés dans toute lecture historique.

## Première exploration distributive — simulation d'une hausse de TVA

[Insee Analyses 43 (2019), figure 2](https://www.insee.fr/fr/statistiques/3713290) est une **simulation ex ante** fondée sur la législation 2016 et le modèle de microsimulation Ines. Le scénario relève de trois points le taux normal de TVA. La publication estime les effets différés, notamment l'indexation de certains revenus et prestations, sur une période de trois ans.

Le CSV `data/tva_choc_deciles_insee_2019.csv` retranscrit les **dix déciles de personnes** du tableau 2, dans l'ordre, avec six composantes publiées : revenus avant redistribution, prélèvements directs, prélèvements indirects, prestations, dépenses de loyer, effet total. Ces chiffres sont arrondis au dixième par l'Insee.

Les colonnes de contribution sont en **points de pourcentage** de variation du niveau de vie corrigé ; l'effet total est en **% de variation**. Le « niveau de vie corrigé » de l'étude est le revenu disponible corrigé de la TVA et des dépenses de loyer, ramené aux unités de consommation. Les valeurs des composantes ne sont pas des impôts payés en pourcentage du revenu observé. La somme des composantes peut différer du total publié de 0,1 point à cause des arrondis.

**Ne jamais interpréter** le chiffre `indirect_tax_pp` comme le taux de TVA subi par un décile ou comme sa part de revenu consacrée à la TVA en 2025. On visualise ici l'effet simulé d'une **hausse** de TVA (législation 2016, publié 2019), pas le niveau de TVA existant ni une chronique historique.

Champ : personnes de France métropolitaine vivant en ménage ordinaire, dont les revenus sont positifs ou nuls et dont la personne de référence n'est pas étudiante. Les déciles sont de niveau de vie usuel. Les hypothèses de transmission aux prix et d'indexation sont décrites dans l'étude source.

Pour une comparaison réellement actuelle de **TVA payée / revenu disponible** ou **TVA payée / consommation**, il reste à trouver et valider une table distributive appropriée. Aucune extrapolation à partir du montant national de TVA n'a été effectuée.

## Deux approches distinctes de la fiscalité indirecte (sans interpolation)

### Estimations BDF 2001 pour la TVA

[Ruiz et Trannoy (2008)](https://www.insee.fr/fr/statistiques/fichier/1376872/es413b.pdf) utilisent l'enquête Budget de Famille 2001 et un modèle de taxation par biens et services. Nous retranscrivons les tableaux 3, 4 et 6 du document publié pour les dix déciles de ménages : TVA en euros **courants 2001 par ménage**, TVA divisée par **revenu disponible brut agrégé du décile**, TVA divisée par **consommation totale** du décile. En particulier, les taux d'effort sont des ratios agrégés, non les moyennes de taux individuels. Ces trois indicateurs ne sont pas interchangeables.

Le résultat D1 = 11,52 % du revenu disponible brut contre D10 = 5,92 % correspond à des **estimations 2001**, pas à des prélèvements fiscaux administratifs d'individus ni à un taux 2025. D1 = 10,5 % de la consommation contre D10 = 11,6 % compare un autre dénominateur ; ce sont des **taux apparents** avec un panier de consommations propre à chaque groupe.

### Comptes nationaux distribués 2020–2023

Le classeur [Insee CND.101](https://www.insee.fr/fr/statistiques/8574663), publié le 16 avril 2026, fournit la ligne « Taxes sur les produits (TVA, TICPE, acises, DMTO, etc.) », distribuée entre vingt groupes de niveau de vie, pour les années **2020, 2021, 2022 et 2023**. Le signe négatif de prélèvement dans la publication est transformé en **montant positif** dans notre fichier dérivé. Ce choix de présentation n'altère pas le montant mais interdit de sommer à nouveau ces valeurs comme recettes fiscales distinctes.

Nous affichons seulement les milliards d'euros attribués aux groupes et la proportion de la somme distribuée **dans la même année et la même source**. Aucun ratio de niveau de vie n'est calculé, aucun chiffre isolé pour la TVA n'est dérivé. Les revenus disponibles nets du secteur S14 figurent dans le classeur mais concernent un sous-secteur et ne sont pas un dénominateur automatiquement compatible avec les taxes sur les produits attribuées à l'ensemble S1.

Les données sont expérimentales, recalées sur la comptabilité nationale et fondées sur des hypothèses d'allocation par consommation. Les montants ne mesurent ni l'incidence économique finale de la taxe ni la charge réellement acquittée par décile en 2025. Les données BDF 2001 et CND 2020–2023 doivent rester **visuellement et statistiquement séparées**.


### Simulation de réforme DG Trésor (publication septembre 2025)

Le [Trésor-Éco 371](https://www.tresor.economie.gouv.fr/Articles/2025/09/25/analyse-de-la-composition-des-recettes-de-tva) simule le choc d'une **hausse uniforme d'un point de pourcentage de tous les taux de TVA** : les taux et paniers de consommation sont distingués par niveau de vie, avec une hypothèse de répercussion intégrale au prix et **à comportements inchangés**. Les chiffres de pouvoir d'achat sont des **variations statiques hypothétiques**, pas les taux d'effort de la TVA courante. Ils proviennent de l'enquête BDF 2017, de l'ERFS 2022 et des comptes nationaux 2021–2022 ; la publication est datée **septembre 2025**.

Seules sont visibles sur le site les valeurs explicitement données dans le texte : **Q1 −0,7 %, Q5 −0,4 %, tous ménages −0,5 %**, puis **Q1 12 % et Q5 31 % des recettes supplémentaires** de la hausse simulée. Les Q2 à Q4 sont visibles graphiquement dans la publication, mais sans valeurs tabulées exactes ; ils ne sont donc **pas reconstruits numériquement**. Le texte explique que l'indexation future du Smic et des prestations amortirait l'effet statique ; elle n'est pas comprise dans l'estimation affichée. L'étude chiffre également le rendement net théorique du point de TVA 2025, qui est **un autre objet statistique**.

Ne pas comparer directement les effets en % sur le **pouvoir d'achat simulé** de l'étude 2025 aux taux agrégés TVA/revenu des ménages du jeu BDF 2001, ni aux montants distribués CND 2020–2023. Les groupes sont des **quintiles**, non des déciles ; les périodes, hypothèses et dénominateurs diffèrent.

## TVA seule répartie entre déciles : Drees / Ines 2014

Le [tableau 16 du document Drees n°60](https://drees.solidarites-sante.gouv.fr/sites/default/files/2020-10/dt60.pdf) (novembre 2016, p. 38) publie la **part de la TVA simulée attribuée à chaque décile**. Le CSV `data/tva_part_deciles_ines_2014.csv` reprend ses dix valeurs à une décimale, avec somme contrôlée à **100 %**. C'est une partition des **montants de TVA estimés pour les ménages inclus dans le champ**, non un taux d'effort, ni une répartition des recettes fiscales nationales constatées.

Champ : ménages ordinaires en France métropolitaine hors DOM, revenu disponible strictement positif. Méthode : module de taxation indirecte du modèle Ines 2014, avec pseudo-appariement de consommations issues de BDF 2011. Publication en 2016, aucune observation fiscale individuelle directe. D1 = 4,3 % et D10 = 18,5 % du total **dans cette estimation**. La somme de 100 % ne démontre pas la représentativité de toutes les recettes de TVA acquittées par l'ensemble des secteurs.

Les taux d'effort TVA/revenu et TVA/consommation ont des dénominateurs **différents** et ne sont pas déductibles des parts de montants sans les bases de revenus et de consommation des mêmes ménages. Le rapport Drees donne les valeurs extrêmes dans le texte, mais pas le tableau exact des dix taux d'effort ; nous n'interpolons donc pas les déciles intermédiaires.

Pour actualiser au-delà de 2014, un nouveau jeu de données doit être obtenu puis traité par une microsimulation documentée. Les tableaux publics BDF 2017 ne contiennent pas directement le montant de TVA par décile ; les versions microdonnées BDF / ERFS détaillées impliquent des conditions d'accès propres. Aucune extrapolation 2014 → 2025 n'est réalisée.

## Intérêts annuels de la dette publique : flux D41 / D41G, 1959–2025

La source est le [tableau Insee 3.201 S13](https://www.insee.fr/fr/statistiques/8988845), version du 28 août 2026, comptes nationaux base 2020. Le fichier `data/interets_apu_1959_2025_bn_eur.csv` contient pour chaque année deux conventions alternatives :
- `interest_d41_bn_eur` : intérêts **D41**, en milliards d'euros courants.
- `interest_ex_fisim_bn_eur` : intérêts **D41G**, hors correction au titre des **services d'intermédiation financière indirectement mesurés (SIFIM)**, en milliards d'euros courants.
- `total_expenditure_bn_eur` : dépenses totales S13 de la même source et du même millésime, pour calculer des **parts de dépense**, sans rapprochement de données non homogènes.

Le secteur S13 comprend toutes les administrations publiques, pas uniquement le budget de l'État. Les deux montants D41/D41G ne doivent **jamais être additionnés** ; une correction SIFIM n'est pas une dépense d'intérêts supplémentaire. Le chiffre synthétique Insee « intérêts » de 64,7 Md€ en 2025 correspond à la ligne D41G (`64.6519`), tandis que D41 vaut `65.7209` Md€.

La page `interets.html` affiche soit des **Md€ courants**, soit un rapport `intérêts de la catégorie / dépenses totales S13 de la même année × 100`. Cette dernière unité est **% des dépenses totales**, **pas % du PIB**, ni le taux d'intérêt apparent. Les montants historiques avant 1999 proviennent de la conversion en euros de séries anciennement exprimées en francs ; ils ne sont **pas corrigés des prix**. Comparer des montants courants de 1959 et 2025 ne mesure pas une variation en volume.

L'encours de dette de Maastricht est un **stock à fin d'année** ; la charge d'intérêts est un **flux annuel** qui dépend des caractéristiques et calendriers des emprunts. Calculer automatiquement `intérêts / dette brute` à partir de ces deux jeux de données ne serait pas une mesure fiable du coût moyen de la dette sans harmoniser les concepts et le dénominateur. L'absence de valeurs égales à zéro dans la source est vérifiée par l'importateur ; l'année 2025 est provisoire.

## Solde primaire : B9NF + intérêts versés D41 (ou D41G) — 1959–2025

Les observations [Insee 3.201](https://www.insee.fr/fr/statistiques/8988845) proviennent du même classeur S13 de la publication du **28 août 2026**, base 2020. Le solde public total ou **B9NF** (« capacité (+) ou besoin (−) de financement ») est la différence entre les recettes et les dépenses, déjà publiées dans le classeur. Les intérêts payés **D41** sont repris de la même table, tout comme la variante **D41G** sans correction SIFIM. La série 1959–2025 ne mélange pas de versions, de sous-secteurs ou de sources de solde.

Le **solde primaire D41** est **calculé** : `B9NF + D41 payés`. Il s'agit de **recettes − (dépenses totales − intérêts D41)`, et pas d'une nouvelle ligne Insee. La variante `B9NF + D41G payés` est disponible pour expliciter l'effet de la correction SIFIM. Les deux charges d'intérêts D41/D41G sont **alternatives**, non additionnables. Le solde B9NF reste identique. Les intérêts **reçus** restent inclus dans les recettes : le calcul ne réintègre que les intérêts **payés**.

La cohérence est contrôlée au niveau des quatre décimales (Md€) : `recettes − dépenses = B9NF` à l'arrondi près ; l'importateur refuse un changement silencieux de SHA-256, libellé ou année. Les taux affichés en mode normalisé divisent chaque solde par les **dépenses totales S13** de la même année. Ils ne sont **ni en % du PIB ni des taux de refinancement**. Les valeurs courantes de 1959 à 2025 ne sont pas déflatées. Le solde primaire n'est **pas corrigé du cycle** : il ne remplace ni le solde structurel ni la comparaison des besoins de financement futurs.

Pour 2025, le classeur Insee 3.201 du 28 août 2026 donne B9NF = `−151,5920` Md€, D41 = `65,7209` Md€ et D41G = `64,6519` Md€ : primaire D41 = `−85,8711` Md€, variante = `−86,9401` Md€. Un autre article Insee datant de **mai 2026** annonçait `−152,5` Md€ ; ne pas panacher des révisions de comptes de dates différentes. Le primaire est un indicateur de la position budgétaire **hors intérêts versés**, pas une preuve que les dépenses sans intérêts sont « inutiles », ni une prévision mécanique de baisse de la dette.

## Trois mesures complémentaires de la dette : tableaux Insee 3.103–3.105

3.103 décrit un **stock de dette nette** : ce n'est pas le patrimoine public net total. Les autres actifs liquides de la source sont présentés en complément et ne doivent pas être déduits une seconde fois. Des contributions nettes de sous-secteur peuvent être négatives.

3.104 décrit un **rapprochement de stocks** : passifs financiers en comptabilité nationale, ajustements de champ, consolidation et valorisation, puis dette Maastricht nominale. Le signe des ajustements varie. Le résidu des sous-lignes de valorisation en 2014–2021 est signalé, sans inventer une cause. En 2025, la contribution sécurité sociale de 3.104 (293,1 Md€) diffère de celle de 3.102 (292,6 Md€).

3.105 est un **rapprochement de flux** : déficit public compté positif dans ce tableau, opérations financières et réévaluations, variation annuelle de la dette. Ce n'est ni l'encours ni la charge d'intérêts. La comparaison avec la variation des stocks annuels du 3.104 révèle un écart de −0,6 Md€ en 2014, préservé et testé.

Ne jamais mélanger dette brute, dette nette, passifs financiers en valeur de marché, patrimoine net, échéances initiales/résiduelles, stocks et flux. Les séries sont celles des comptes nationaux base 2020 publiés le 28 août 2026, données 2025 provisoires.
