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
