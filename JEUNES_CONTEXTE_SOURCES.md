# Jeunes en 2024 — mise en contexte de l'apprentissage

Statut : 17 octobre 2026. Ce chapitre met en contexte les chiffres de l'apprentissage ; il ne construit pas de taux d'apprentissage avec un dénominateur d'âge incompatible.

## Population par âge au 1er janvier 2024

Source : Insee, Bilan démographique 2024, tableaux rétrospectifs (14 janvier 2025).
Page : https://www.insee.fr/fr/statistiques/8313981
Classeur : https://www.insee.fr/fr/statistiques/fichier/8313981/Pop1janv_age.xlsx
SHA-256 pour le XLSX d'origine de 789277 octets : 223e5d4699d1b99b20b1e81a7f75dec961031272d74c4cd429fb9466fc8f574d.
Feuille 2024, population au 1er janvier par sexe et âge en années révolues ; estimation provisoire arrêtée fin 2024 ; colonne F France entière, G hommes, H femmes (distinct de France métropolitaine).

Import Python standard dans scripts/import_jeunes_population.py : vérification SHA, année, territorialité, cellules et sommes H+G=F. CSV de 15 âges (15 à 29 ans) : data/jeunes_population_2024_par_age.csv. Classeur source non committé.

Totaux calculés par simple somme d'effectifs officiels : 18–25 inclus = 6 375 226 ; 18–24 = 5 603 770 ; 15–24 = 8 209 108 ; 18–29 = 9 446 471 ; 18–20 = 2 436 304 ; 21–24 = 3 167 466. Ce ne sont pas des nombres publiés d'apprentis de ces âges. Ne pas diviser 1 049 965 par 6 375 226 pour obtenir un taux d'apprentissage : le numérateur SIFA de fin 2024 concerne tous les âges.

## Situations études et emploi 2024

Source : Insee, France portrait social, édition 2025, 18 novembre 2025, Scolarisation des jeunes de 18 à 29 ans, figure 2 :
https://www.insee.fr/fr/statistiques/8612518

Enquête Emploi 2024 ; France hors Mayotte, personnes vivant en logement ordinaire. Tableau six groupes = femmes/hommes multipliés par 18–20 / 21–24 / 25–29 ans, cinq catégories exclusives : en études initiales, cumul études-emploi, en emploi, au chômage, autres inactifs hors études. CSV data/jeunes_situations_2024_insee.csv recopié directement depuis le tableau officiel de pourcentages arrondis au dixième. Les libellés de la page précisent études sans emploi et emploi hors études pour bien signaler l'exclusivité.

Les totaux des parts peuvent être 99,9 % ou 100,1 % à cause de l'arrondi. La géométrie du camembert est normalisée à 100 %, pas les valeurs affichées. Le lecteur choisit une des six populations publiées, sans fusion artificielle pour fabriquer un 18–25 ans sexes confondus.

Attention : un apprenti est généralement à la fois en études et en emploi, mais les autres jeunes de cette catégorie ne sont pas tous apprentis. Le chômage est une catégorie distincte des personnes inactives hors études.

## Apprentis et étudiants

1 049 965 apprentis en formation au 31 décembre 2024, tous âges, Depp-SIFA, Insee T04/T1 : https://www.insee.fr/fr/statistiques/8666372 (voir APPRENTISSAGE_SOURCES.md).
1 048 800 contrats d'apprentissage en cours, Dares SIA : https://dares.travail-emploi.gouv.fr/publication/lapprentissage-en-2024 . Ces deux sources n'ont pas des unités strictement identiques.
3 012 800 inscriptions dans le supérieur à la rentrée 2024–2025, tous âges, apprentis du supérieur inclus : https://www.enseignementsup-recherche.gouv.fr/fr/les-effectifs-etudiants-dans-l-enseignement-superieur-en-2024-2025-100596 .

Recommandation éditoriale : ne jamais dessiner les trois grands chiffres comme parts du même tout. La comparaison est une mise en contexte, pas une ventilation d'une génération.

## Séries longitudinales, 1986–2023 et 2003–2023 — audit du 17 octobre 2026

**Scolarisation par âge exact** (en % de tous les jeunes de cet âge) : Insee, *France, portrait social* 2025, fiche F7, figure 1.
- https://www.insee.fr/fr/statistiques/8612518
- https://www.insee.fr/fr/statistiques/fichier/8612518/FPORSOC25-F7.xlsx
- Original XLSX, SHA-256 **881ea0b49f9c1937ef536728678082336392be6729bdec160d83ed1376664340** ; feuille 1, tableau 1986–2023, 38 lignes, âge **18/21/25/29 ans**, données 2023 provisoires.
- France métropolitaine jusqu'en 1998, France hors Mayotte 1999–2017, France entière à partir de 2018 ; marqueurs en 1999/2018. Les taux correspondent à la rentrée scolaire.

**Cumul études et emploi**, en % des jeunes *encore en études initiales* de la tranche d'âge considérée : Insee, *Formations et emploi* édition 2025, fiche F5, figure 1 (enquêtes Emploi, calculs Depp).
- https://www.insee.fr/fr/statistiques/8305508
- https://www.insee.fr/fr/statistiques/fichier/8305508/BFE2025-F5.xlsx
- Original XLSX, SHA-256 **62b962d7f75dff49b60508595c8e0b4f9a63b9d41b187833c727391d46767288** ; feuille 1, tableau 2003–2023, 21 lignes, groupes **15–29 / 15–19 / 20–24 ans**.
- Champ France métropolitaine jusqu'en 2013, France hors Mayotte à partir de 2014, population vivant en logement ordinaire. Questionnaires en 2013 et 2021 avec rétropolations par l'Insee/Depp : comparabilité de **2003–2013 d'une part, 2014 et après d'autre part**, sans continuité parfaite à présumer. Repères 2014 et 2021.

La figure 2 de la fiche F5 rapporte pour **2023** : **10,9 %** des 15–29 ans en études initiales sont en apprentissage, **1,5 %** en stage, **9,9 %** dans un autre emploi. Ces parts arrondies ont un dénominateur commun (tous les jeunes de la tranche encore en études initiales), mais ne forment pas une série par type d'emploi. L'apprenti en formation initiale qui exerce son contrat relève du cumul études-emploi ; les reprises d'études peuvent recevoir un classement différent. Ce sous-ensemble ne peut être isolé du diagramme 2024.

**Reproduction** : scripts/import_jeunes_longitudinal.py, source XLSX épinglée SHA-256 (non commitée), contrôle des colonnes, âges, années contiguës et décimales ; les CSV produits sont data/jeunes_scolarisation_1986_2023_insee.csv et data/jeunes_cumul_emploi_etudes_2003_2023_insee.csv. Aucune interpolation. Les deux indicateurs ont des dénominateurs distincts et ne sont pas superposés sur un même axe.

**Interprétation scientifique** : ces courbes montrent une co-évolution, pas l'effet propre de l'apprentissage sur le nombre de jeunes en études. Les politiques de 2018/2020, la conjoncture et la sélection des publics interdisent une causalité naïve. La comparaison des voies scolaires et de l'apprentissage via [InserJeunes / Depp / Dares](https://www.education.gouv.fr/inserjeunes-l-insertion-des-jeunes-apres-une-formation-en-voie-professionnelle-307956) doit distinguer diplôme, poursuite d'études, situation antérieure, origine sociale, ruptures, salaires et emplois 6/12/24 mois. Les différences brutes de taux d'insertion (par exemple 62 % des sortants apprentis CAP–BTS contre 41 % des sortants de voie scolaire pour la sortie 2024, six mois après) ne sont **pas** des effets causaux et les populations sont sélectionnées ; les études n'observent ici que l'emploi salarié couvert par leurs sources. Mesurer les conditions de travail, les violations et recours aux droits, les discriminations, et les risques liés à la situation administrative exige des enquêtes dédiées avant de chiffrer leur fréquence.
