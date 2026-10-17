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
