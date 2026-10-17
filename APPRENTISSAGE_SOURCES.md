# APPRENTISSAGE — sources, chronologie, définitions et limites

**Statut : première passe documentée du 17 octobre 2026.** La page autonome de l'atlas compare uniquement des indicateurs attestés ; elle ne prétend ni reconstruire une série financière complète, ni mesurer la réussite des apprentis.

## Nombre de contrats : Dares

1. **Dares**, « L'apprentissage en 2024 », Dares Résultats n° 3, **21 janvier 2026**. https://dares.travail-emploi.gouv.fr/publication/lapprentissage-en-2024 . Système d'information sur l'apprentissage (SIA), extraction du **7 novembre 2025** ; France, secteurs privé et public. **889 400 contrats débutés pendant 2024** et **1 048 800 en cours au 31 décembre 2024**. L'article signale que 43 % des contrats débutés concernent un apprenti ayant déjà été en apprentissage.
2. **Dares**, « Séries longues : le contrat d'apprentissage », **27 février 2026**. https://dares.travail-emploi.gouv.fr/donnees/le-contrat-dapprentissage . Premières estimations **2025** : **846 700 contrats débutés** et **1 017 500 en cours au 31 décembre** ; respectivement environ −5 % et −3 % sur un an. Le jeu Dares met à disposition les caractéristiques des contrats de **1993 à 2025**, mais l'original XLSX n'a **pas encore été importé/reproduit** dans cette PR. La page montre seulement deux années sourcées, à statut distingué.
3. **Attention à la révision des séries** : les publications Dares peuvent actualiser la valeur de 2024 dans les tableaux diffusés en 2026. Par exemple le document PoEm sur 2025 cite environ 1 050 000 contrats à fin 2024 ; le chiffre de 1 048 800 est celui de l'étude Dares du 21 janvier 2026. Ne pas maquiller cette divergence en erreur ni mélanger les versions sans étiquette.

**Définitions.** « Contrats commencés dans l'année » est un flux de **contrats**, pas forcément un flux d'**individus distincts**. « En cours au 31 décembre » est un stock de contrats à une date. Un apprenti peut signer plusieurs contrats et une rupture peut conduire à une nouvelle entrée. Les « gamins » ne forment pas un champ officiel : l'apprentissage concerne aussi l'enseignement supérieur et certains adultes. Pas d'échelle d'âges inventée. 2025 reste **première estimation**.

Le fichier data/apprentissage_dares_2024_2025_indicateurs.csv conserve année, deux mesures, source et statut (2024 publication / 2025 estimation préliminaire), territoire et secteurs couverts.

## Financement : France compétences

**France compétences**, « Rapport sur l'usage des fonds de la formation professionnelle, édition 2025 », fiche **L'apprentissage**, publiée en février 2026 et portant sur l'activité **2024** :
- https://www.francecompetences.fr/fiche-ruf/lapprentissage-3/
- PDF officiel : https://www.francecompetences.fr/app/uploads/2026/02/RUF25_Apprentissage.pdf

En 2024 : **15,6 Md€ d'engagements financiers** relatifs à l'apprentissage dans le **secteur privé**, dans la convention de ce rapport ; **17 404 € de coût unitaire** d'un contrat (hors rémunération de l'apprenti), avec environ **52 % de coûts pédagogiques** et **34 % d'aides aux entreprises** ; **5 983 € d'aides par contrat**. Les **14 %** représentent un solde arithmétique de parts arrondies (100−52−34) et ne constituent **pas** une catégorie officielle détaillée. Les coûts comprennent d'autres aides, frais de structure et mise en œuvre.

**Ne pas calculer 15,6 Md€ en multipliant les contrats « en cours » Dares** : un engagement financier, un nouveau contrat pris en charge, un contrat commencé, un financement de CFA et un encours au 31 décembre ne sont pas des unités interchangeables. **Ne pas additionner automatiquement** les 15,6 Md€ à l'estimation sénatoriale des aides aux entreprises de 2023 (211 Md€), qui appartient à un périmètre différent et contient déjà certains dispositifs liés aux employeurs d'apprentis.

Le fichier data/apprentissage_financement_2024_france_competences.csv reproduit ces seuls indicateurs publiés/arrondis pour 2024, avec des champs explicitement nommés. Il ne constitue ni un total de charges comptables Insee, ni un coût net des seules administrations publiques.

## Histoire : jalons vérifiables, pas « naissance » en 1919

- **1919, loi Astier** : organisation nationale de l'enseignement technique et des cours professionnels. Texte officiel : https://www.education.gouv.fr/sites/default/files/document/T%C3%A9l%C3%A9charger%20la%20loi%20relative%20%C3%A0%20l%26%23039%3Borganisation%20de%20l%26%23039%3Benseignement%20technique%20industriel%20et%20commercial%20%28dite%20loi%20Astier%29%20du%2025%20juillet%201919-240096.pdf
- **1925**, taxe d'apprentissage ; **1928**, contrat écrit. Publication ministérielle d'histoire de l'enseignement technique : https://www.education.gouv.fr/media/31046/download
- **1971**, organisation juridique des CFA et contrats ; **1987**, extension à des diplômes supérieurs. Source : https://www.education.gouv.fr/media/14858/download
- **2018**, loi pour la liberté de choisir son avenir professionnel et réforme du financement ; **2020**, aides exceptionnelles à l'embauche. Source : https://www.igf.gouv.fr/rapports-de-mission/revue-de-depenses-formation-professionnelle-et-apprentissage ; Dares 2024 ci-dessus.

L'apprentissage des métiers et des corporations est beaucoup plus ancien : **1919 est une date de structuration législative, pas l'invention historique de l'apprentissage**.

## Suites scientifiques — APPRENTISSAGE en priorité

1. Télécharger et auditer le **XLSX Dares 1993–2025**, SHA-256, onglets, définitions et éventuelles ruptures ; publier deux séries longues uniquement après audit (entrées, contrats en cours) et compiler les ventilations âge / genre / handicap / niveau de diplôme / secteur / ruptures.
2. Analyser les **financeurs** : État, France compétences, OPCO, collectivités, employeurs et autres ; distinguer contrats et fonds engagés / réalisés / annulations ; ne pas prolonger les financements en euros courants si les définitions ont varié.
3. Comparer **secondaire / supérieur**, CAP, bac, BTS, licence, master, niveaux de prise en charge (NPEC), reste à charge CFA et employeurs, prérequis d'accès ; prudence face aux effets de sélection.
4. Suivre **réussite et ruptures** : diplomation, abandon, retour en apprentissage, insertion après formation avec dénominateurs et délais explicites. Les taux d'insertion ne sont pas automatiquement des effets de causalité de l'apprentissage.
5. Relier ce chapitre à **aides aux entreprises** par dispositifs traçables (aides à l'embauche, exonérations, financement CFA), sans double comptage.
6. **Accueil** : envisager une porte d'entrée guidée « comprendre l'apprentissage », après validation de la future maquette hybride.

**Publication** : ce chapitre est dépendant de la PR #30 du chapitre aides. Ne pas annoncer une URL publique opérationnelle tant que ces branches n'ont pas été fusionnées et déployées avec validation.

## Nouvelle série : Insee/Depp-SIFA, effectifs au 31 décembre, 1982–2024

**Source officielle** : Insee, *L'école et ses sortants – 2025* (20 novembre 2025), tableau T04 « 1.4 Apprentis en formation », feuille T1 « Évolution des effectifs d'apprentis selon le diplôme préparé ».
- Page : https://www.insee.fr/fr/statistiques/8666372
- XLSX : https://www.insee.fr/fr/statistiques/fichier/8666372/T04%20-%201.4.xlsx
- SHA-256 du XLSX original de 336409 octets : 93432bd9c0f7e950502544df2de2604b9ec2730e873693b8387b53b2b6800a0d
- Producteur : Depp, enquête SIFA, effectifs au **31 décembre**. Champ source : **France hors Mayotte jusqu'en 2010, France avec Mayotte depuis 2011**. Il s'agit donc d'un changement de champ territorial explicitement signalé.
- Reproductibilité : script standard Python scripts/import_apprentissage_sifa.py, CSV data/apprentissage_sifa_effectifs_1982_2024.csv, original XLSX non committé. 43 années 1982–2024, cinq catégories officielles et total ; validation de la somme des catégories pour chaque année, aucune interpolation. Les zéros historiques sont ceux du fichier Insee, pas des valeurs imputées.
- 1995 : **293 512** en tout, dont **194 485** en CAP/mention et **4 777** en bac+3 ou plus. 2018 : **448 127**, 2019 : **478 803**. 2024 : **1 049 965** en tout, dont **191 029** CAP/mention et **421 000** bac+3 ou plus.

**Distinction essentielle** : ces apprentis **en formation Depp-SIFA** ne sont pas exactement le stock de **contrats en cours Dares** (2024 : 1 048 800 selon publication Dares du 21 janvier 2026, soit 1 165 de moins que SIFA). L'écart n'est pas corrigé ou comblé. Les sources mesurent des objets différents et les versions peuvent varier. Les entrées de contrats Dares en 2025 sont un flux distinct, les engagements de France compétences sont une grandeur financière distincte.

La Dares possède un classeur officiel « Caractéristiques des contrats d'apprentissage » couvrant 1993–2025, mais son téléchargement direct a été bloqué au cours de cette passe par sa protection de site. La Dares signale les systèmes de collecte suivants : organismes d'enregistrement 1993–2011, Ari@ne 2012–2019, Deca depuis 2020. **Aucune série de contrats Dares 1993–2025 n'a été fabriquée.** Reprendre l'import lorsqu'un fichier source vérifiable est récupéré.

**Interface** : graphique 1995–2024 par défaut, bascule complète 1982–2024 ; vue du total ou répartition par cinq niveaux de diplôme ; tableau HTML des 43 années ; signalement de Mayotte et repère 2018 non causal. Les catégories historiques de diplômes évoluent elles-mêmes avec les diplômes et certifications disponibles.

## Enquête âge, certification et circuits financiers — vérifications du 17 octobre 2026

**Dares, « L'apprentissage en 2024 »**, 21 janvier 2026, SIA (extraction du 7 novembre 2025) :
https://dares.travail-emploi.gouv.fr/publication/lapprentissage-en-2024
PDF de l'étude : https://dares.travail-emploi.gouv.fr/sites/default/files/d724dea796477dfd0273350e9c9c0d64/DR_Apprentissage_2024.pdf

- Sur **889 400 contrats commencés en 2024** dans les secteurs privé et public, **8 %** concernent des entrants âgés de 26 ans ou plus ; **177 400** concernent des jeunes de **15–17 ans** (graphique 4). Ces répartitions concernent **l'âge au début du contrat**, pas une photographie des 1 049 965 apprentis en formation SIFA à fin 2024.
- **39 %** des contrats commencés concernent l'enseignement secondaire ; **34 %** préparent un titre à finalité professionnelle (qui n'est pas synonyme d'un niveau de diplôme). Le graphique 3 indique **142 200** nouveaux contrats pour une formation de **niveau 4 (bac)**. Aucun de ces flux ne peut devenir automatiquement une part du stock SIFA.
- L'étude signale que **43 %** des contrats commencés concernent une personne ayant déjà été apprentie ; un même bénéficiaire peut commencer plusieurs contrats. L'Excel officiel associé et les séries longues Dares 1993–2025 restent à télécharger et à contrôler : **aucun fichier brut Dares nouveau n'a été importé dans cette passe**.

**France compétences, RUF édition 2025 (activité 2024)**, fiche « L'apprentissage », rapport PDF pages imprimées 22–25 :
https://www.francecompetences.fr/fiche-ruf/lapprentissage-3/
https://www.francecompetences.fr/app/uploads/2026/02/RUF25_VF.pdf

- Champ **secteur privé**, engagements financiers **nets des annulations**, hors rémunération des apprentis : **15 594 M€ engagés en 2024** pour **895 998 nouveaux contrats pris en charge** (date de décision OPCO). Ces 895 998 décisions de prise en charge ne sont **ni** les 889 400 contrats effectivement commencés Dares **ni** les 1 049 965 apprentis SIFA.
- Sur des fonds issus de France compétences, les OPCO ont engagé **8 176 M€ de coûts pédagogiques** pour ces 895 998 contrats, soit **9 125 € par contrat** selon le tableau officiel (RUF p. 24, tableau 4). **8 176 M€ est une composante des engagements, pas un total à ajouter aux 15 594 M€**. La fiche donne par ailleurs 17 404 € de coût unitaire de contrat tous postes hors rémunération, autre indicateur.
- **Origine des fonds engagés** pour 2024 (RUF p. 23, graphique 3) : France compétences **58,5 %**, État **36,7 %**, entreprises **2,5 %**, bénéficiaires **0,5 %**, Agefiph **0,1 %**, Régions **1,8 %**. Les pourcentages publiés totalisent 100,1 % par arrondi. Ce tableau classe **les origines ultimes de fonds dans le périmètre retenu**, pas les dépenses réalisées directement par chaque organisme ; ne pas additionner les transferts France compétences → OPCO → organismes de formation.
- Les séries RUF 2021–2023 ont été révisées dans l'édition 2025 (annulations comptables, méthodes d'affectation et données régionales). Une tendance pluriannuelle exige un **même millésime RUF** ; données 2024 provisoires.

**Décisions scientifiques** : distinguer quatre objets statistiques (personnes SIFA, contrats commencés Dares, nouveaux contrats pris en charge OPCO, engagements financiers), leurs dates, leurs champs public/privé et leurs éventuelles révisions. Avant de publier une ventilation par **OPCO**, retrouver une source identifiable et une unité commune ; une répartition par type de financement ne décrit pas automatiquement chaque OPCO. Ne pas fabriquer de pourcentages pour une tranche 18–25 ans à partir des flux tous âges.
