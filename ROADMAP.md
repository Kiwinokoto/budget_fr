# Roadmap et passation

## Situation au 16 octobre 2026

- Dépôt public : Kiwinokoto/budget_fr. PR #1–#17 fusionnées sur `main` le 16 octobre 2026 ; dernier commit applicatif (TVA seule estimée Ines 2014) **`e97999e3168b808938c385f22a60d886394981b0`**. La documentation de passation ultérieure peut faire avancer `main` sans redéploiement.
- Coordination AgentCtl : projet budget-fr, ressource repo:Kiwinokoto/budget_fr ; verrou à prendre avant toute mutation et libérer en fin de passe.
- Base Insee initiale 1995–2025 recopiée à la main **remplacée** par les chiffres du classeur officiel d'août 2026.
- Données 1960–2025 : recettes, dépenses, solde, variantes hors éléments imputés ; dette brute depuis 1978 et nette depuis 1995. Fichier original conservé à la source, pas dans Git.
- Importateur en Python standard, empreinte SHA-256 de la source, validation des libellés, années et solde ; tests couvrant les absences de valeurs.
- Application statique avec curseur temporel et graphiques de recettes/dépenses et dette.
- Site public en ligne : **https://budget-fr.kiwinokoto.fr** sur le VPS personnel, via `/opt/budget-fr`, conteneur `budget-fr-web`, réseau Docker `traefik_network`, routeur Traefik dédié et certificat Let's Encrypt. Déploiement figé sur `e97999e3168b808938c385f22a60d886394981b0` (`/opt/budget-fr/.deployed_commit`). Aucune base de données, aucune automatisation ou modification des services voisins.
- Vérifications en production : HTTPS HTTP 200 sans `-k`, documents et CSV HTTP 200, trois CSV servis identiques octet par octet à GitHub (66, 30 et 31 années), **23 tests Python et 14 tests Node OK pour la version actuelle**, certificat valide, conteneur démarré, volume statique monté en lecture seule. Revue visuelle navigateur desktop/mobile **encore à faire**.

- **Historique des axes** : `607dbd8b4fd60c92b47832c701ce9c122f949891` (PR #7), inclus dans les versions applicatives suivantes. L'application servie est désormais `e97999e` ; les commits de documentation ultérieurs ne déclenchent pas de déploiement.

## Lot COFOG livré sur `main` et sur le site public

- Fichier Insee 3.301 inspecté, dix rubriques (GF01–GF10), 1995–2024 ; somme réconciliée avec le total à l'arrondi près.
- Importateur reproductible `scripts/import_cofog.py`, tests de couverture, cohérence comptable, année et empreinte source.
- Page `fonctions.html` et lien depuis `index.html` : répartition, année, parts et tendance. Deux séries statistiques distinctes ; pas d'amalgame entre euros et % PIB.
- Livraison publique validée : https://budget-fr.kiwinokoto.fr/fonctions.html, HTTP 200 sans exception TLS, HTML et CSV servis identiques à l'artefact GitHub ; import COFOG officiel reproductible à l'octet. Sauvegarde du site précédent : `/opt/budget-fr/backup/20261016T124632-0504e5c70314939cb2d0f0537a953a6fc81b1c71/site/`. La revue visuelle réelle desktop/mobile reste à faire.
- État de coordination : le déploiement statique a été effectué sous verrou `deploy:vps-personal/budget-fr` et libéré automatiquement ; pas de modification Docker/Traefik.

## Lot recettes fiscales livré sur `main` et en production

- Classeur Insee 3.217 téléchargé et audité (SHA-256 épinglée), 31 exercices de 1995 à 2025.
- Séparation stricte entre catégories additionnables, ajustements négatifs et sous-postes D51.
- Nouvelle page statique `recettes.html`, lien sur l'accueil, tests de cohérence et importateur Python indépendant.
- Source 3.216 couvrant 1959–2025 repérée mais **pas importée** ; attention à l'inclusion des organismes européens et aux transferts.
- **Production validée** : https://budget-fr.kiwinokoto.fr/recettes.html (HTTPS et certificat valides), CSV servi conforme octet par octet au fichier GitHub, 14 tests réussis, import sur source originale conforme, JS vérifié syntaxiquement. Commit déployé `eaa87fae4ba3a57aab8374592d01530eadd70628`. Ancienne version sauvegardée dans `/opt/budget-fr/backup/20261016T130106-2057b7e3eb0e2424cb37f95ce85fadbf54bd30fe/`. Le site n'est pas redéployé automatiquement ; une revue visuelle desktop/mobile reste à faire.

## Finition des axes temporels — passe du 16 octobre 2026

- **Livré via PR #7**, commit applicatif `607dbd8b4fd60c92b47832c701ce9c122f949891` et déployé en production à ce même SHA.
- Graduations de 5 ans sur grand écran, 10 ans en affichage compact (rupture à 700 px), avec dernière année conservée (2024 COFOG).
- Repère vertical discret de l'année sélectionnée et points des séries disponibles sur les quatre courbes (recettes/dépenses, dette, fonctions, prélèvements).
- Validation : 14 tests Python, 3 tests Node de graduations, syntaxe des 3 scripts JavaScript ; **17/17 réussis**. Les trois HTML publics sont identiques octet par octet au commit versionné via HTTPS, les CSV inchangés.
- Sauvegarde réversible : `/opt/budget-fr/backup/20261016T134059-axes-before-607dbd8b4fd60c92b47832c701ce9c122f949891/`. Aucun redémarrage Docker ou Traefik. Les captures fournies décrivent l'ancien rendu desktop ; **revue visuelle des nouvelles graduations en navigateur mobile encore à faire**.

## Passe « unités et TVA » — 16 octobre 2026

- Correctif ciblé `index.html` : les deux axes verticaux affichent désormais `%`, et les légendes précisent **% du PIB**. Les valeurs et autres pages ne changent pas.
- Nouveau test de non-régression dans `tests/year_axes.test.cjs`.
- Cadrage documenté dans `TVA_JUSTICE_SOURCES.md` : études Insee sur les effets de la TVA, distinction revenu/consommation et simulations, sources distributives à contrôler **avant** de publier des chiffres par décile.
- **Déployé et vérifié** : PR #9 fusionnée, version statique effectivement publiée `2501217d2bba01c729d65d4724ff69d39d44d5f7`. 14 tests Python + 4 tests Node OK, syntaxe des trois scripts OK, `index.html` public identique octet par octet au commit GitHub ; les deux autres pages et les trois CSV sont inchangés.
- Sauvegarde ciblée : `/opt/budget-fr/backup/20261016T142013-yunits-before-2501217d2bba01c729d65d4724ff69d39d44d5f7/`. Aucun redémarrage de conteneur ; le déploiement s'est fait sous verrou AgentCtl, ensuite libéré.
- **Limitations restantes :** revue responsive réelle non faite, absence de série distributive TVA récente authentifiée.

## Lot TVA : simulation distributive Insee (octobre 2026)

- Première vue quantitative à partir de la figure 2 d'Insee Analyses n°43 (2019) : dix déciles, relèvement simulé de trois points du taux normal de TVA, législation et champ de référence 2016.
- Nouveaux fichiers : `tva-justice.html`, `data/tva_choc_deciles_insee_2019.csv`, `tests/test_tva_scenario.py`. Liens dans l'accueil et la page recettes ; sources, méthodologie et cadrage scientifique actualisés.
- **Invariant :** simulation historique / effet marginal ≠ TVA observée / effort relatif réel ; pas de conversion en valeurs 2025 ni fusion des jeux de données.
- Revue visuelle navigateur mobile encore à réaliser ; intégration d'une distribution réellement observée reste une étape de recherche.
- **Livré PR #11**, commit `51e51f228aa96ec74c678f70d7a8ac98b79d6e73`, déployé sur https://budget-fr.kiwinokoto.fr/tva-justice.html.
- **Tests :** 18 Python + 7 Node, tous réussis ; JavaScript des quatre pages valide ; clone Git propre. La page, son CSV et les documents correspondants servent exactement les fichiers du commit GitHub en HTTPS (HTTP 200).
- **Déploiement statique réversible**, copie antérieure sauvegardée : `/opt/budget-fr/backup/20261016T151614-tva-before-51e51f228aa96ec74c678f70d7a8ac98b79d6e73/`. Aucun redémarrage de service ni modification des jeux de données historiques.
- **Prochaines étapes :** revue mobile/navigateur réel, puis identification d'une source observée et récente de TVA par groupes de revenu et de consommation (non assimilable à notre simulation de 2016).

## Fiscalité indirecte : deux lectures complémentaires (passe suivante)

- Dataset TVA estimée **2001** : Ruiz & Trannoy, BDF, tableaux 3/4/6, dix déciles, euros par ménage et ratios au revenu disponible brut ou à la consommation.
- Dataset **2020–2023** : Insee CND.101, taxes sur les produits (TVA, TICPE, accises, DMTO, etc.) **et non TVA seule**, vingt groupes V1–V20, milliards d’euros courants. Source XLSX épinglée SHA-256, importateur avec vérification des totaux.
- Page `tva-incidence.html` interactive : bascule de dénominateur pour 2001, sélection de millésime pour taxes sur produits, détails des groupes. Liens depuis accueil, recettes et simulation 2019.
- **Garde-fou :** comparaison qualitative seulement ; aucune interpolation vers 2025, aucun mélange des catégories ou des millésimes ; données CND expérimentales.
- **Livré et déployé** : PR #13, commit `8e490b18cf0a20d6c323f52281e518a37024800f`. Nouvelle page https://budget-fr.kiwinokoto.fr/tva-incidence.html, navigations et deux nouveaux CSV en production.
- **Tests vérifiés** : 22 Python + 10 Node (32 réussis), syntaxe JavaScript de cinq pages, CSV CND.101 reproduit **octet par octet** depuis l'XLSX original ; clone Git propre.
- **Contrôles HTTPS** : index, recettes, simulation, nouvelle page et deux CSV correspondant octet par octet au commit ; les quatre CSV/pages déjà publiés n'ont pas changé.
- **Retour arrière** : copie précédente `/opt/budget-fr/backup/20261016T153535-incidence-before-8e490b18cf0a20d6c323f52281e518a37024800f/`. Aucun redémarrage de service et verrous AgentCtl libérés après publication.
- **Limites** : validation visuelle mobile réelle toujours à faire ; aucune série actuelle de **TVA seule** et de taux d'effort des déciles n'est attestée pour 2023 ou 2025.

## Source DG Trésor TVA seule (septembre 2025) — passe du 16 octobre 2026

- Étude identifiée et lue : Trésor-Éco n°371, graphique 4 et texte d'accompagnement, pages 5–6, publiée le 25/09/2025.
- Résultats textuels certains : **−0,7 % de pouvoir d'achat simulé pour Q1**, **−0,4 % pour Q5**, **−0,5 % en moyenne**, et **12 % / 31 %** des recettes marginales réparties sur Q1 / Q5.
- Préserver trois différences : **quintiles et non déciles**, **effet marginal d'une hausse et non taux de TVA déjà supporté**, **publication 2025 fondée sur BDF 2017, ERFS 2022 et comptes nationaux 2021–2022**.
- Section ajoutée à \`tva-incidence.html\`, sans chiffres fictifs pour Q2–Q4, test de non-régression, sources et méthodologie mises à jour.
- La prochaine étude à rechercher reste un fichier de TVA actuelle seule par décile/quintile, relatif au revenu **et** à la consommation. BDF 2017 publie les dépenses par catégorie, pas directement le montant de TVA payée par groupe.
- **Livré et déployé** : PR #15 fusionnée, version servie `2dd13d08762e8b658264a174f9de24a0199b9a65`, section publiée sur https://budget-fr.kiwinokoto.fr/tva-incidence.html. **22 tests Python + 12 tests Node** réussis, cinq scripts JavaScript validés et CSV CND.101 toujours reproductible octet par octet.
- **Production vérifiée** : les fichiers `tva-incidence.html`, `TVA_JUSTICE_SOURCES.md`, `DATA_SOURCES.md` et `METHODOLOGY.md` correspondent au commit sur HTTPS ; anciens HTML et CSV inchangés.
- **Sauvegarde** : `/opt/budget-fr/backup/20261016T154732-tresor-before-2dd13d08762e8b658264a174f9de24a0199b9a65/` ; déploiement statique isolé sous verrou, sans modification des autres services.
- **Inconnue persistante** : aucune série annuelle récente de la TVA seule effectivement estimée par niveau de vie et consommation ; revue responsive graphique mobile non effectuée.

## TVA seule Drees Ines 2014 : distribution des montants par décile

- Source nouvelle : Drees, document de travail n°60 (2016), tableau 16 p. 38 : TVA isolée entre dix déciles, **répartition du montant estimé**, pas taux d'effort. D1 4,3 %, D10 18,5 %, total 100 %.
- Données `data/tva_part_deciles_ines_2014.csv` : transcription exacte de dix valeurs tabulées publiées, contrôle de somme et des déciles. Ajout du panneau interactif dans `tva-incidence.html` ; sources, méthodologie et tests actualisés.
- **Source de modèle récent identifiée :** Ines module de taxation indirecte (BDF 2017 pseudo-appariée) ; microdonnées BDF 2017 plus détaillées soumises à accès CASD/Quételet, et ERFS nécessaires au modèle. Les tableaux publics de dépense 2017 ne permettent pas de publier de TVA seule par décile à eux seuls.
- **Blocage scientifique explicite :** pas encore de tableau distributif contemporain 2023–2025 de la TVA seule, rapportée aux revenus et à la consommation, sur le même champ.
- Pour une estimation récente : demander les statistiques agrégées Drees/Insee ou étudier un accès encadré aux microdonnées et au module Ines ; ne pas publier une approximation comme donnée observée.
- **Livré en production** : PR #17 fusionnée, version `e97999e3168b808938c385f22a60d886394981b0` sur https://budget-fr.kiwinokoto.fr/tva-incidence.html. CSV `data/tva_part_deciles_ines_2014.csv` publié.
- **Validation :** 23 tests Python + 14 tests Node réussis ; JS des cinq pages vérifié, ancien CSV CND reproduit octet par octet à partir de sa source officielle. Les cinq fichiers publics mis à jour sont identiques octet par octet au commit GitHub, pages et CSV historiques inchangés.
- **Sauvegarde réversible :** `/opt/budget-fr/backup/20261016T160348-drees-before-e97999e3168b808938c385f22a60d886394981b0/`. Aucun redémarrage de service, verrous AgentCtl relâchés après opérations. Revue graphique mobile **encore non effectuée**.

## Suite prioritaire

1. Valider le rendu sur un vrai navigateur mobile et l'accessibilité ; les captures desktop sont encourageantes mais ne valident pas le mobile.
2. Documenter et mesurer les écarts entre les publications Insee de mai et août 2026.
3. ~~Rechercher des séries détaillées COFOG 1995–2024~~ : **premier niveau COFOG S13 intégré** (mars 2026, dix catégories, euros courants). Prochaine étape : explorer sous-fonctions, harmoniser les millésimes et déceler les reclassements.
4. ~~Identifier les principales recettes par impôt~~ : premier lot de prélèvements obligatoires 1995–2025 intégré avec contrôle des doubles comptes, TVA, IRPP, IS, CSG/CRDS et cotisations. Poursuivre : revenus non fiscaux, dette, intérêts, solde primaire et patrimoine.
5. **TVA et justice fiscale :** enquêter sur la disponibilité de la TVA seule réellement estimée et rapportée au revenu/consommation dans une enquête récente, puis étendre aux taux réduits et à la redistribution élargie. Maintenir strictement les distinctions 2001 estimée / Ines 2014 TVA seule / 2016 choc simulé / 2020–2023 taxes sur produits / simulation 2025. Ensuite formaliser la traçabilité budgétaire.
6. Faire une vraie revue visuelle et une vérification responsive, puis envisager un déploiement automatisé uniquement si cela devient utile (actuellement manuel et volontaire).

## Risques

Ruptures comptables, révisions du millésime, séries partielles, faux rapprochements de périmètres, transfert doublement compté, confusion entre fiabilité de la publication et qualité politique ou efficacité de la dépense.

Passation : GitHub reste la source canonique ; ne pas laisser de fichiers importants dans une copie locale. Tester puis vérifier branche, HEAD, lease et état propre avant de conclure.
