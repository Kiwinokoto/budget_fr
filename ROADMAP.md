# Roadmap et passation

## Checkpoint — 18 octobre 2026 : solde budgétaire et recettes nettes, 2013–2025

- **Priorité** : consolider les recettes, les dépenses et le solde de l'État année par année, puis étendre l'historique des ventilations mission/programme après audit des sources. **L'apprentissage reste un chantier à approfondir ultérieurement**, utile et légitime ; il est simplement moins prioritaire, non abandonné ou « clos ». Les anciennes formulations du backlog parlant de « dérive » ou de clôture sont historiques et désormais dépassées.
- **Livraison en cours** : `dev/etat-solde-net-2013-2025-20261018`, base `main` `56f53065386448b0b279372ccd36f87cb6079b49`. Sur `etat.html`, affichage d'un solde officiel DGFiP et de ses six composantes, 2013–2025, en euros courants. Import `scripts/import_etat_solde_net.py` de deux CSV officiels SHA-256 épinglés, données `data/etat_solde_net_2013_2025.json`. La somme exacte des flux réconcilie le solde publié sur les 13 exercices avec moins de 0,01 € d'écart **avant** arrondi à l'euro. Le détail mission/programme demeure limité à 2023–2025 (PLRG), sans données inventées pour 2013–2022.
- **Deux périmètres à conserver** : comptabilité budgétaire de l'État (SMB/PLRG) ≠ dépenses et déficit consolidés S13 (Insee/COFOG). Le « hors mission Remboursements et dégrèvements » de PLRG est une transformation descriptive, **pas la dépense nette officielle SMB**. Les recettes brutes du PLRG ne sont pas les recettes fiscales nettes DGFiP.
- **2025** : solde officiel −124,206 Md€, recettes fiscales nettes 356,398 Md€ ; situation de décembre définitive. L'annonce antérieure −124,7 Md€ de février 2026 était provisoire.
- **Backlogs différés** : pouvoir d'achat et dépenses pré-engagées (contexte à explorer plus tard), apprentissage (à approfondir), patrimoine public. Rien de tout cela ne devient une nouvelle priorité dans cette passe.
- **Livraison contrôlée** : PR [#46](https://github.com/Kiwinokoto/budget_fr/pull/46) ouverte depuis `dev/etat-solde-net-2013-2025-20261018`. Code testé au commit `21edec3d7c3e677c655f7121055e0b30ec7a79af` : **67 tests Python, 63 tests JavaScript, compilation Python, reproduction octet pour octet des deux imports SMB, Chromium 390/768/1365 px**, changement de période et synchronisation année, sans erreur JS ni débordement. Aucune modification de l'infrastructure ou du VPS personnel.
- **Production** : dernier SHA applicatif connu `8aead975b776f3d5ed2f6e2215e749ef03edca3b`; aucun déploiement demandé. Vérifier le SHA, les verrous AgentCtl et la sauvegarde avant toute publication. Passation documentaire à compléter avec numéro de PR, résultats des tests et HEAD final.



## Checkpoint — 18 octobre 2026 : budget de l'État d'abord, pouvoir d'achat en contexte

- **État GitHub confirmé** : `main` au commit `8d62ca73408f3d1420d5e75c77c89ca7d926ad65` après fusion de la **PR #44** (exécution budgétaire de l'État, 2023–2025 ; 64 tests Python, 60 tests Node et recette Chromium vérifiés sur la branche source lors de la passe précédente). **PR #43** (69 sous-fonctions COFOG) et **PR #42** (clôture apprentissage) sont également fusionnées. Les mentions « PR ouverte » des checkpoints historiques ci-dessous ne sont plus actuelles. **Aucun déploiement effectué** : dernier SHA applicatif connu du site public `8aead975b776f3d5ed2f6e2215e749ef03edca3b` (à revérifier avant tout éventuel déploiement). Ne pas aligner production et GitHub sans demande explicite.
- **Priorité absolue maintenue** : reconstruire **recettes, dépenses, solde et ventilation de l'État** par année, sur des définitions cohérentes ; distinguer PLRG (budgétaire État), COFOG/INSEE (APU S13), crédits votés vs exécutés, recettes brutes vs nettes. Prochain correctif utile : sourcer le **solde budgétaire officiel** et les recettes fiscales **nettes** sur une période cohérente, puis compléter l'historique et le niveau « action » seulement si les annexes peuvent être réconciliées. Pas de nouvelle recherche apprentissage, pas de refonte accueil, pas de nouveau chapitre hors sujet.
- **Nouvelle question de contexte, demandée par l'utilisateur, NON prioritaire** : « Le sentiment que la vie était moins chère/plus facile autrefois est-il confirmé quand on compare revenus et coûts réellement supportés ? » Piste à traiter **après** la trame budgétaire, idéalement comme onglet/panneau d'interprétation du niveau de vie, sans laisser ce sujet devenir une enquête autonome interminable. Hypothèse ouverte, et non conclusion : pouvoir d'achat moyen réel en hausse et part du budget pré-engagée également en hausse peuvent coexister.
- **Périmètre minimal envisagé pour ce contexte** : (1) pouvoir d'achat du revenu disponible **par unité de consommation**, en euros constants ou indice, et revenu **arbitrable** après dépenses pré-engagées ; (2) indice des prix/de la consommation comparé à l'évolution des revenus nets, en séparant salaires nominaux, médians et agrégats ; (3) part des **dépenses pré-engagées** et du **logement** dans le revenu ; (4) éventuellement contraste par décile de niveau de vie, statut d'occupation (locataire/propriétaire), géographie et taille du ménage, **uniquement si des séries officielles compatibles existent**. Un graphique d'ensemble 1960–2025 suffirait pour une première version, sans bricoler des paniers fictifs ni des prix approximatifs.
- **Données officielles déjà identifiées, non importées** :
  - Insee, [revenu disponible et pouvoir d'achat, séries 1960–2025](https://www.insee.fr/fr/statistiques/2830244), données 2025 provisoires ; le pouvoir d'achat est calculé avec le déflateur des dépenses de consommation des ménages. Source complémentaire [Insee, compte ménages 2025 et revenu arbitrable](https://www.insee.fr/fr/statistiques/8988851), tables 2.101 à 2.103.
  - Insee, [France portrait social 2025 : consommation et épargne, tableau 1960–2024](https://www.insee.fr/fr/statistiques/8612566), **dépenses pré-engagées 13,5 % du revenu disponible brut en 1960, 30,3 % en 2024**, dont logement **10,7 % et 22,8 %** respectivement (millésime et base à conserver). Insee, [pouvoir d'achat réel par UC, indice 1960 = 100](https://www.insee.fr/fr/statistiques/8612564) : 2024 = **322,7** ; **niveaux moyens nationaux**, ni vécu de chaque foyer ni répartition des salaires.
  - Insee, [taux d'effort du logement](https://www.insee.fr/fr/metadonnees/definition/c1809) : mesure distincte de la part « logement » en comptabilité nationale ; pour les locataires, loyers/charges/eau/énergie ; pour les propriétaires, remboursements d'emprunt et charges. Distinguer brut/net d'aides au logement.
  - DREES, [dépenses pré-engagées selon le revenu](https://drees.solidarites-sante.gouv.fr/publications/les-dossiers-de-la-drees/depenses-pre-engagees-quel-poids-dans-le-budget-des-menages) (étude 2018) : source utile pour la distribution, **pas à fusionner directement** dans une série récente.
- **Garde-fous d'interprétation** : le logement pré-engagé en comptabilité nationale **inclut les loyers imputés aux propriétaires occupants**, ce qui n'est pas un loyer réellement payé ; ne pas substituer ce ratio à l'effort locatif. Corriger inflation, composition démographique, qualité et changement des produits, panier de consommation, variations patrimoniales, transferts publics, et distinguer pouvoir d'achat moyen, médian et sentiment individuel. Ne jamais inférer « les Français sont plus riches » des seules recettes/dépenses de l'État ou de leur valeur nominale. Source en ligne et dénominateur visibles sur tout graphique.
- **Décision de livraison** : cette passe n'introduit **aucun import ni nouvelle page**, seulement ce backlog méthodologique borné ; ensuite revenir au budget de l'État. Aucun déploiement VPS. Verrou AgentCtl du dépôt nécessaire uniquement pendant la modification documentaire et la PR.


## Priorité active — 18 octobre 2026 : budget général de l'État, exécution 2023–2025

- **Priorité centrale confirmée** : expliquer chaque année d'où vient l'argent public et où il va, descendre de poste en sous-poste, distinguer les données observées des analyses, et mesurer la traçabilité **des chiffres**, sans score inventé. L'apprentissage est **clos pour le moment** (PR #42 fusionnée) ; pas de nouveaux travaux de recherche sur l'apprentissage tant qu'une nouvelle demande ne le justifie.
- **PR #43 fusionnée** : sous-fonctions COFOG S13, 69 catégories de 1995–2024, commit `a08fb11d123a0723e8ba69755ab077199864fd2f`. Production non redéployée.
- **PR #44 ouverte** : https://github.com/Kiwinokoto/budget_fr/pull/44 ; branche de travail `dev/budget-etat-execution-2023-2025-20261018`, base `main` `a08fb11d123a0723e8ba69755ab077199864fd2f`. Aucun déploiement, aucune fusion de cette PR lors de cette passe.
- **Nouvelle tranche : budget général de l'État (≠ APU consolidées S13)**. Branche `dev/budget-etat-execution-2023-2025-20261018` depuis `a08fb11d...` : `etat.html`, trois années **2023–2025**, navigation **missions → programmes**, recettes recouvrées par catégorie → section, CP ouverts et consommés, fisc brut explicitement distingué du net. Sources originales PLRG (neuf CSV) vérifiées par SHA-256 et transformation reproductible `scripts/import_budget_etat_plrg.py`, JSON versionné ; provenance en `DATA_SOURCES.md`, conventions en `METHODOLOGY.md`.
- **Contrôle de cohérence** : chaque année 33 missions et 129–131 programmes, chiffre d'exécution 2024 de 584,982 Md€ **y compris** remboursements/dégrèvements. **Écart source non justifié de 83 650,28 € en 2023** pour cette mission, visible et non comblé. Les recettes sont brutes, seul 2024 présente le net fiscal dans les trois annexes employées. Pas de déficit reconstruit à partir de montants incomparables.
- **Recette réalisée sur clone indépendant** au commit `0e63aae1e80a70eeac1e0234f4bbd0be57301c5f` : **64/64 tests Python**, **60/60 tests Node**, compilation Python OK, génération des neuf CSV officiels → JSON identique **octet par octet**, **Chromium 390/768/1365 px** : navigation 2025 → 2024 (fiscal net) → 2023, détail des remboursements et dégrèvements, avertissement de réconciliation, pas d'erreur JS ni débordement horizontal. Aucun déploiement et aucun accès aux fichiers de production. Une revue humaine sur smartphone/lecteur d'écran reste à faire.
- **Suite bornée** : recette navigateur responsive et claviers, comparaison encaissements/CP officiels, accès aux données de 2023/2025 sans mélange de concepts, puis **niveau action** à partir des documents RAP/PLRG si compatibles ; préparer aussi un vrai solde officiel et la comparaison « voté (LFI) / exécuté (PLRG) » avec périmètre unifié. Pas de réforme générale de l'accueil, ni création d'indice politique non audité.
- **État de production** : dernier SHA applicatif connu `8aead975b776f3d5ed2f6e2215e749ef03edca3b`. Aucun déploiement implicite des PR. Avant publication : vérifier branche approuvée, verrous déploiement, sauvegarde, fichiers JSON et nouveaux liens, rollback.


## Recentrage scientifique et fonctionnel — 18 octobre 2026 (priorité actuelle)

- **Décision : fin de la dérive apprentissage.** Dernière comparaison CAP/bac pro/BTS (sortants 2023 à six et vingt-quatre mois) intégrée avec la PR **#42** fusionnée dans `main` au SHA `2b9ef521b0578c64932615aedeb2fb456ab066fd`. Le chapitre est **mis en pause** ; pas d'autres recherches, enrichissements par spécialité, salaires ou ruptures avant nouvelle décision explicite.
- **Objectif central retrouvé** : exposer annuellement recettes et dépenses, permettre le forage poste → sous-poste → provenance et expliquer **ce qui est ou non traçable**. Priorité à une exploration utile avec données officielles et dénominateurs cohérents, pas à la multiplication des analyses thématiques.
- **Correction de périmètre** : la série COFOG existante décrit les **administrations publiques consolidées S13**, pas « le budget de l'État » seul. La protection sociale en 2024 y représente 693,029 / 1 671,794 Md€ = environ **41,5 %**, et la santé est séparée. L'État seul est documenté en COFOG Insee 3.303 (2009–2024), et son budget LOLF demande des sources mission/programme/action et une définition de base comptable claire ; ne pas mélanger ces univers.
- **Passe en cours** : nouvelle branche `dev/cofog-sous-fonctions-20261018` issue de `2b9ef521b0578c64932615aedeb2fb456ab066fd` ; **PR #43 ouverte** (https://github.com/Kiwinokoto/budget_fr/pull/43). Importateur sourcé et 69 sous-fonctions COFOG annuelles (1995–2024, Insee 3.301 SHA-256 épinglée), affichage sous le graphique sur `fonctions.html` avec barres, montants et parts du parent, tests et documentation. Validation locale du code au commit `44c2d476ba0a3b25f252eb72a2ffb1f3e4975c8f` (seules les notes de passation changent ensuite) : **61 tests Python, 58 tests Node**, compilation Python OK ; import XLSX épinglé régénéré à l'identique ; Chromium à **390, 768 et 1365 px** (choix du poste Santé, passage 2024 → 1995, valeurs et défilement vérifiés), sans erreur JS. Aucun déploiement demandé ni effectué ; PR à intégrer après contrôle.
- **Ordre de travail après cette PR** : 1. vérifier UX responsive/accessible des sous-fonctions ; 2. poser clairement le choix du périmètre **S13 vs État** et préparer séries compatibles par année ; 3. construire l'exploration **État : recettes nettes / missions / programmes / actions** à partir des documents d'exécution, en séparant voté/exécuté ; 4. formaliser une **grille de transparence** (source, année, unité, réconciliation, niveau de finesse, trous et révisions) sans indice arbitraire ; 5. garder patrimoine public et apprentissage en backlog, sans nouveaux travaux spontanés.
- La refonte globale de l'accueil reste différée jusqu'à stabilisation des données et du parcours principal. Les passages antérieurs de ce fichier constituent des états historiques ; ne pas réactiver leurs priorités par défaut.


## Passation scientifique — 18 octobre 2026 : emploi selon diplôme (branche dev)

- Branche : `dev/apprentissage-diplomes-insertion-20261018`, base `main` `ba34ba286f0f7a0c442d9567a19c2132a52779dc`. Ajout de douze taux InserJeunes de la cohorte sortie en 2023, à six et vingt-quatre mois, CAP/bac pro/BTS, apprentissage et voie scolaire ; CSV transcrit des deux notes DEPP du 25 juin 2026. Mise à jour de `apprentissage-resultats.html`, `APPRENTISSAGE_RESULTATS_SOURCES.md` et test Python ciblé. Recette effectuée sur clone frais au commit `9cfa157ac1ee2f2e65c876c0dcb51a1fdb3c3fa1` : 59 tests Python OK, 56 tests Node OK, compilation Python OK. Pas de recette navigateur automatisée sur cette passe ; pas de déploiement demandé ni effectué.
- Prudence : diplôme **préparé**, pas forcément obtenu ; taux parmi les seuls sortants, échantillons des deux voies non identiques, pas de causalité. Éditions 2024 et 2026 non mélangées ; aucune agrégation de fichiers établissements. Source : `APPRENTISSAGE_RESULTATS_SOURCES.md`.
- Suite : données par spécialité et effectifs publiés, seuils de confidentialité, salaires à 12 mois, diplômes obtenus et ruptures/reprises, avec import reproductible si XLSX audité. Accueil et patrimoine public toujours différés.


## Passation consolidée — 18 octobre 2026

- **Source de vérité** : Kiwinokoto/budget_fr. GitHub main au début de cette passe : ad26b57bc74878c1bfd7144ce51a99fe62dfd3f2, PR #40 fusionnée. Lire AGENTS.md, README.md, DATA_SOURCES.md, METHODOLOGY.md et ROADMAP.md avant intervention. Cette passe documentaire n'ajoute aucun code ni donnée et ne déploie rien. Après fusion, le SHA GitHub sera différent de celui en production, uniquement en raison de la documentation.
- **Production vérifiée le 18 octobre** : /opt/budget-fr/.deployed_commit = 8aead975b776f3d5ed2f6e2215e749ef03edca3b ; budget-fr-web en fonctionnement ; sauvegarde /opt/budget-fr/backup/20261017T110640Z-before-d8d4e7665fe5-to-8aead975b776 présente. Ne pas redéployer un commit documentaire uniquement pour aligner les SHA.
- **Diagnostic Angela / Kevin du 17 octobre : RÉSOLU, non stale.** La contention était due aux deux timers systemd qui réservaient host:vps-personal/docker à chaque passage à la minute. Correctif installé dans Kiwinokoto/appart-angela (main ac77d872c3fc9e0cb5db88f84f8a8c17eeb86670) et Kiwinokoto/apparts (main 80d887b484ff4a3993e8778327a7473072953c54, PR #22). Les timers visent maintenant appart-angela-deploy-check.service et apparts-deploy-check.service : vérifications du GitHub main et du hash .env sans lease ni Docker ; uniquement lors de changement, appel au déploiement sous les verrous AgentCtl initiaux. Six tests ciblés par projet, contrôle de passages successifs sans nouveau déploiement, applications saines ; les scopes ont été libérés. **La section « Diagnostic AgentCtl » du 17 octobre plus bas est historique : sa dette de coordination est maintenant corrigée.** Une vraie livraison par événement push GitHub Actions n'a pas été configurée faute de nécessité et nécessiterait un accès VPS restreint audité.
- **Priorité scientifique** : reprendre APPRENTISSAGE avec parcours et résultats ventilés par CAP / bac professionnel / BTS et spécialités, obtention des diplômes, emploi/salaire à 12 et 24 mois, ruptures et reprises, rémunérations et conditions de travail, coûts marginaux et financement OPCO. Comparer des populations compatibles, sans fabriquer de causalité à partir de séries descriptives ; rendre les incertitudes visibles. Refonte de l'accueil différée.
- **Backlog ajouté en PR #40** : nouveau chapitre différé sur la liquidation/cession du capital et des actifs publics, notamment autoroutes et aéroports. Chronologie chiffrée et sourcée (vente, concession, valorisation des flux), distinction stricte entre faits, contrefactuels et hypothétique indicateur de transparence/risque de capture, jamais un indice de corruption affirmé sans preuves.
- **Prochaine session** : vérifier HEAD, branches et éventuelles PR, AgentCtl et état de production ; dev/* et PR pour toute écriture budget_fr, tests ciblés puis élargis. Déploiement VPS uniquement sur demande, après lock deploy:vps-personal/budget-fr et host:vps-personal/docker, sauvegarde et rollback. Distinguer toujours SHA applicatif en production et SHA documentaire GitHub.


## Backlog différé — liquidation du patrimoine public : autoroutes, aéroports et cessions (17 octobre 2026)

- **Proposition utilisateur, pas encore une étude publiée** : créer un chapitre chronologique chiffré sur les cessions et transferts de capital ou de droits d'exploitation des personnes publiques vers des acteurs privés. Montrer le produit de vente à court terme, les recettes et droits futurs conservés ou abandonnés, les contreparties, obligations et coûts à long terme ; distinguer les faits vérifiés du jugement politique de « scandale ».
- **Opérations candidates** : privatisations de participations autoroutières ; contrats de concession, durées, péages, profits, investissements, prolongations et avenants ; cessions de participations aéroportuaires (Toulouse-Blagnac, Lyon, Nice). Comparer à part le projet de cession d'ADP non réalisé. Séparer strictement ventes d'actions, concessions, ventes immobilières et projets abandonnés.
- **Tableau chronologique proposé** : date de décision et de transaction, périmètre et part cédée, vendeur/acquéreur, durée restante, prix et encaissement nominal/constant, dividendes et taxes, dette/risque/obligations transférés, investissements futurs, flux pour la collectivité. Pour évaluer un éventuel manque à gagner : scénario de maintien public explicite, taux d'actualisation, incertitudes et contrôles de périmètre ; pas d'addition arbitraire de flux.
- **Sources primaires à rechercher** : Agence des participations de l'État, Cour des comptes, rapports parlementaires, documents budgétaires, contrats et avenants de concession, comptes annuels des sociétés et autorités concédantes, décisions de justice et régulateurs. Consigner URL, page, version, millésime, champ, unité et révisions. Aucun montant de cession ou rendement n'a été audité dans cette passe.
- **Deux analyses distinctes** : (1) bilan économique/financier documenté ; (2) éventuelle grille de transparence et risque de capture : concurrence, publicité, contrôle et accès aux documents, conflits d'intérêts légalement constatés, recommandations et sanctions. Ne pas afficher d'indice de corruption chiffré ni porter d'accusations individuelles sans méthodologie, preuves et limites publiées. Mauvaise décision économique et infraction ne sont pas synonymes.
- **Statut** : backlog après les travaux apprentissage. Aucun code, chiffre, page, déploiement ou modification de l'accueil maintenant.

## Diagnostic AgentCtl / verrou appart-angela — 17 octobre 2026

- L'occupation observée de host:vps-personal/docker par le projet Angela **n'était pas un verrou stale** : /etc/systemd/system/appart-angela-deploy.timer programme OnActiveSec=45s, OnUnitActiveSec=60s, AccuracySec=5s, et lance appart-angela-deploy.service. La commande agentctl-host-run prend service:appart-angela, deploy:vps-personal/appart-angela et le verrou Docker partagé avant appart-angela-sync-main. Des exécutions de quelques secondes sont observées, sans relation démontrée avec une visite d'Angela. Les passages systemd réussissent généralement ; HTTP 409 signale normalement un verrou occupé par un autre agent.
- **Dette de coordination** : réservation répétée du verrou partagé lors d'un contrôle automatique à la minute, même lorsqu'aucune mise à jour n'est nécessaire. Optimisation future sur le projet Angela, distincte de ce backlog : vérifier nécessité/changement de HEAD avant réservation Docker, réduire la section critique ou revoir cadence/déclencheur, après audit des dépendances. **Aucune modification** du timer, des services, de Docker ou des verrous.
- **État vérifié avant modification documentaire** : GitHub main 22b7b6131d07282ab341b4988de89dc154eb568c ; application publiée 8aead975b776f3d5ed2f6e2215e749ef03edca3b, conteneur budget-fr-web sain, sauvegarde /opt/budget-fr/backup/20261017T110640Z-before-d8d4e7665fe5-to-8aead975b776 conservée. Écart GitHub/production dû aux seuls documents de la PR #39. La prochaine session doit recontrôler HEAD, branches, prod, AgentCtl et CI.
- **Cette passe** : ROADMAP.md uniquement sur dev/patrimoine-public-cessions-backlog-20261017 et PR ; tests existants, pas de publication VPS.


## APPRENTISSAGE — résultats publiés et vérifiés (17 octobre 2026)

- **Production** : main applicatif 8aead975b776f3d5ed2f6e2215e749ef03edca3b, confirmé dans /opt/budget-fr/.deployed_commit et sur https://budget-fr.kiwinokoto.fr/apprentissage-resultats.html ; budget-fr-web en fonctionnement. PR #37 et PR #38 incluses. Les deux pages apprentissage.html et apprentissage-contexte.html disposent du lien vers la nouvelle page.
- **Sauvegarde** : /opt/budget-fr/backup/20261017T110640Z-before-d8d4e7665fe5-to-8aead975b776 ; copie vérifiée contenant le précédent SHA d8d4e7665fe5bf89b3bf4d80453e9cf57959e202, site statique et Compose. Rollback prévu mais non exécuté (release réussie). Aucun autre conteneur modifié.
- **Recette** : clone GitHub au SHA exact, 58 tests Python et 56 Node, 22 CSV, comparaison HTTPS octet par octet des pages/JS/CSS/CSV/documents livrés ; 36 contrôles Chromium spécifiques à la nouvelle page (390, 768, 1365 px) et tests de régression de l'atlas et des trajectoires. HTTP 200 confirmé. Verrous AgentCtl deploy:vps-personal/budget-fr et host:vps-personal/docker acquis après libération du verrou viewer puis libérés en fin d'opération.
- **Limites** : InserJeunes compare 39/54 % de poursuite parmi les inscrits de dernière année et 62/41 % d'emploi salarié parmi les seuls sortants ; leurs dénominateurs diffèrent, et les écarts ne sont pas des effets causaux. Source APPRENTISSAGE_RESULTATS_SOURCES.md. Suite scientifique : comparer diplôme/spécialité et cohorte, diplomation, salaire et emploi à 12/24 mois, ruptures, conditions de travail, financements marginaux et substitution à la voie scolaire.
- **Suite technique** : ne pas déployer automatiquement les futurs commits documentaires ; pour toute modification, branche dev, PR, vérification des protections/tests, sauvegarde et rollback.


## APPRENTISSAGE — bilan des résultats : PR #37 fusionnée, non déployée (17 octobre 2026)

- **GitHub main après la PR #37** : commit applicatif 0e0e3a118da1fc0a0f4d3598e09c42dad56d5c78. Branche de développement dev/apprentissage-resultats-20261017, commit df7bce57137c03cbfb7fdce999cf9b8a9863bed0, PR https://github.com/Kiwinokoto/budget_fr/pull/37 fusionnée. 10 fichiers ajoutés/modifiés (page, CSV, sources, tests, navigation et documentation).
- **État effectif du VPS contrôlé après fusion** : /opt/budget-fr/.deployed_commit reste d8d4e7665fe5bf89b3bf4d80453e9cf57959e202 ; budget-fr-web fonctionne, et apprentissage-resultats.html est absent du site public. Ne pas présenter le nouveau chapitre comme en production. Publication à faire **sur demande explicite**, avec verrous, copie des nouvelles ressources statiques, sauvegarde et rollback. Sauvegarde précédente connue : /opt/budget-fr/backup/20261017T101809Z-before-209c5e7d0394-to-d8d4e7665fe5.
- **Recette de la PR** : 58 tests Python (dont vérifications d'unités, taux, dates), 56 tests Node, 36 contrôles Chromium locaux sur 390/768/1365 px, navigation vers et depuis les sous-pages, CSS et absence de débordement. Un premier contrôle Chromium a dû accepter HTTP 304 en cache en complément du 200 ; aucune modification applicative liée à ce diagnostic.
- **Sources et limites** : résultats InserJeunes CAP–BTS 2023–2024 (poursuite études 39 % apprentissage vs 54 % scolaire parmi inscrits ; emploi salarié des sortants 62 % vs 41 % à six mois). Ruptures Dares cohortes 2021 (brut 32 %, net 18 %), conditions de travail Dares (2018/2019–2020), IPP 2024 (évaluation causale de l'aide 2020, BTS), IGF–Igas 2024 (aubaine et croissance du supérieur). Ne pas conclure que le million SIFA est un million d'employés « reclassés ». Voir APPRENTISSAGE_RESULTATS_SOURCES.md.
- **Priorité de recherche** : séries InserJeunes par CAP/bac pro/BTS et par spécialité, réussite aux diplômes et salaires à 12/24 mois ; coûts publics marginaux et études évaluatives de substitution scolaire, analyse des situations de vulnérabilité. Ne pas refondre l'accueil ; préserver les conventions de sources et méthodes.


## APPRENTISSAGE — résultats des formations et effets évalués (17 octobre 2026)

- Nouvelle page apprentissage-resultats.html et quatre observations InserJeunes 2023–2024 : 39 % vs 54 % de poursuite parmi les inscrits de dernière année (apprentissage/voie scolaire) et 62 % vs 41 % d'emploi salarié parmi les seuls sortants six mois après. Deux populations, pas un camembert ni un effet causal ; champ CAP à BTS, couvertures différentes selon la voie.
- Ruptures Dares sur contrats de 2021 : 32 % brutes sur durée initialement prévue, 18 % nettes sans reprise sous six mois. Conditions de travail : Dares, entrants 2018 du CAP à bac+2 encore en contrat en 2019–2020 ; 67 % déclarent des heures supplémentaires, 28 % régulièrement, sans conclure automatiquement à une infraction.
- IPP 2024 : 80 500 embauches supplémentaires estimées en 2020 grâce à l'aide exceptionnelle, hypothèse de représentativité, et baisse relative du risque d'interruption en BTS estimée dans un cadre précis ; IGF–Igas : hausse des entrées majoritairement portée par le supérieur, question des effets d'aubaine. Le million SIFA ne signifie pas un million de salariés déjà employés puis reclassés.
- Suite prioritaire : diplomation, insertion et salaire à 12/24 mois comparables par diplôme et spécialité, ruptures/reprises, protection des apprentis vulnérables, évaluation marginale du financement et éventuelle substitution avec la voie scolaire. Documenter méthode d'appariement/évaluation avant attribution causale. Refonte de l'accueil différée.
- État de déploiement : ce développement doit être intégré par PR, sans publication VPS sans demande explicite, nouveau SHA vérifié, sauvegarde et rollback.


## APPRENTISSAGE — deux trajectoires longitudinales publiées (17 octobre 2026)

- GitHub : PR #35 fusionnée, commit applicatif d8d4e7665fe5bf89b3bf4d80453e9cf57959e202 ; déployé et vérifié sur https://budget-fr.kiwinokoto.fr/apprentissage-contexte.html. Fichier /opt/budget-fr/.deployed_commit contrôlé sur le VPS. Documentation postérieure sur main non déployée automatiquement.
- Sauvegarde de la version précédente (209c5e7d0394324dc96cc74c2f7590c77b6ee4d0) : /opt/budget-fr/backup/20261017T101809Z-before-209c5e7d0394-to-d8d4e7665fe5. Retour arrière conservé ; seul budget-fr-web et son contenu statique ont été concernés.
- Publication testée sur clone GitHub épinglé : 55 tests Python, 54 tests Node, 21 CSV et ressources HTML/JS/CSS/documents identiques à GitHub par HTTPS ; 139 contrôles Chromium en production, y compris les deux nouveaux SVG à 390, 768 et 1365 px, les changements d'âge et les tableaux, sans débordement horizontal. Verrous AgentCtl deploy et host acquis puis libérés.
- Reprise de l'incident Wi-Fi Mint : session précédente reconnue abandonnée après contrôle des processus ; abandon via le broker officiel, sans casser de verrou actif et sans désactiver la protection Git. Développement et PR via agentctl run et branche dev.
- Suite scientifique : évaluer séparément accès aux études, changement de statut études/emploi, obtention de diplôme, insertion à 6/12/24 mois, ruptures, conditions de travail, rémunérations et coûts publics par financeur/OPCO. Les évolutions agrégées sont descriptives, pas des effets causaux ; comparer des cohortes et profils compatibles et privilégier des études évaluatives. Les plaintes liées à l'exploitation ou aux papiers nécessitent des données spécifiques avant chiffrage.
- Limites : formation initiale versus reprise ; changements territoriaux et méthodologiques Insee détaillés dans JEUNES_CONTEXTE_SOURCES.md. Contrôle humain sur mobile réel et lecteur d'écran encore à effectuer. Refonte de l'accueil toujours différée.


## APPRENTISSAGE : scolarisation et emploi dans le temps — 17 octobre 2026

- **Deux séries attestées** depuis l'Insee : scolarisation 1986–2023 (18/21/25/29 ans, dénominateur chaque population d'âge), et cumul études-emploi 2003–2023 (15–29/15–19/20–24 ans, dénominateur uniquement les jeunes en études initiales). Deux XLSX sources inspectés, empreintes SHA-256 épinglées ; scripts/import_jeunes_longitudinal.py, deux nouveaux CSV, deux SVG interactifs et tableaux accessibles sous apprentissage-contexte.html.
- **Le classement de l'apprenti** : normalement dans « études et emploi » dans l'enquête Emploi s'il est en formation initiale et en emploi BIT ; la catégorie recouvre aussi des stages et emplois étudiants non apprentis. Reprise d'études : ne pas généraliser le classement. Insee F5 : 10,9 % des 15–29 ans en études initiales sont apprentis en 2023.
- **Ruptures** : scolarisation : 1999 et 2018 (champ territorial). Cumul études-emploi : France métropolitaine jusqu'en 2013, France hors Mayotte depuis 2014 ; questionnaires modifiés en 2013/2021, rétropolations avec comparabilité limitée. Année scolaire vs enquête Emploi annuelle. Taux et effectifs ne sont pas mélangés.
- **Hypothèse à examiner, non verdict** : la croissance de l'apprentissage augmente-t-elle la part des jeunes ayant accès à la formation, ou surtout le poids des étudiants salariés ? Ces séries sont descriptives. Prochain chantier : diplômes obtenus, insertion comparative à 6/12/24 mois avec sélection observée, ruptures de contrat, salaire et coût de financement public ; chercher évaluations quasi-expérimentales avant attribution causale. Les situations d'exploitation, discrimination, vulnérabilité administrative nécessitent des indicateurs documentés.
- **Publication** : inscrire le commit réellement déployé, sauvegarde, recette et verrous une fois la PR fusionnée et la version appliquée. Ne pas refondre l'accueil.


## Publication du contexte jeunesse et recherche APPRENTISSAGE — 17 octobre 2026

- **GitHub main publié et vérifié** : `209c5e7d0394324dc96cc74c2f7590c77b6ee4d0` (PR #33), à partir de `72fb148dcf89549e0404f797e2a78d539c012e6b`. Site https://budget-fr.kiwinokoto.fr/apprentissage-contexte.html ; `/opt/budget-fr/.deployed_commit` vérifié sur le VPS personnel, conteneur `budget-fr-web` opérationnel.
- **Sauvegarde rollback** : `/opt/budget-fr/backup/20261017T091857Z-before-72fb148dcf89-to-209c5e7d0394`. Aucun changement des autres conteneurs, aucun déploiement automatique. AgentCtl : verrous `deploy:vps-personal/budget-fr` et `host:vps-personal/docker` acquis puis libérés, session terminée.
- **Tests de publication** : 52 Python, 52 Node ; 19 CSV et ressources HTML/JS/CSS/documents comparés octet par octet sur HTTPS ; 94 vérifications Chromium des chapitres existants et de la nouvelle sous-page, de 390 à 1600 px selon la page. Aucune erreur bloquante constatée ; examen esthétique humain sur mobile physique restant ouvert.
- **Recherche suivante (sans nouvelle donnée graphique publiée)** : Dares 2024 offre une décomposition des **contrats commencés** par âge et niveau de formation ; France compétences RUF édition 2025 propose les engagements OPCO **2021–2024** nets d'annulations ainsi que les financeurs. Détails, périmètres et limites dans `APPRENTISSAGE_SOURCES.md`. Ne pas confondre contrats Dares entrés dans l'année, apprentis SIFA au 31 décembre et décisions de prise en charge OPCO.
- **À faire** : obtenir le XLSX Dares 1993–2025 malgré la protection du site, auditer provenance/empreinte et nomenclatures avant import ; identifier une ventilation publiquement contrôlable par OPCO et certification, puis préparer une représentation des flux sans double compte. Refonte de l'accueil différée. Toute nouvelle modification doit repartir du HEAD GitHub actualisé.


## APPRENTISSAGE — « Un million, par rapport à combien ? » — 17 octobre 2026

- **Mission** : créer une sous-page pédagogique depuis APPRENTISSAGE (sans refondre l'accueil), visuels légers, et une seule ventilation circulaire fondée sur des catégories exclusives ; éviter d'additionner apprenti + étudiant + emploi + chômage.
- **Source démographique** : Insee Bilan démographique 2024, XLSX population détaillée au 1er janvier 2024, empreinte SHA-256 documentée et import reproductible. **6 375 226** personnes de 18 à 25 ans inclus (France entière) ; population SIFA apprentis **1 049 965 tous âges** au 31/12, comparateur de grandeur uniquement, pas un taux d'apprentissage des 18–25 ans.
- **Source situations** : Insee France portrait social édition 2025, figure 2, enquête Emploi **2024**, France **hors Mayotte**, 18–20 / 21–24 / 25–29 ans **par sexe**. Cinq catégories mutuellement exclusives : études initiales, cumul études-emploi, emploi sans études, chômage, autres inactifs hors études. Les valeurs arrondies peuvent totaliser 99,9 / 100,1 % ; normaliser seulement le dessin, pas les chiffres publiés.
- **Autre repère** : 3 012 800 étudiants dans le supérieur (2024–2025, tous âges, apprentis inclus), source SIES. **Jamais un secteur du même camembert** que la population 18–25 ans ou que les apprentis.
- **Fichiers** : apprentissage-contexte.html, jeunes-contexte.js, deux CSV sourcés, scripts/import_jeunes_population.py, JEUNES_CONTEXTE_SOURCES.md ; lien entrant depuis apprentissage.html. La navigation générale reste à dix onglets, l'accueil pédagogique hybride reste un futur chantier.
- **Suite scientifique** : données harmonisées permettant de connaître les apprentis par âge exact, effectifs d'étudiants et de jeunes actifs selon mêmes âges, dates et territoires, puis financements et formation par niveau CAP/BTS/supérieur. Pas de taux bricolé.
- **Passation** : une fois la PR et, le cas échéant, publication contrôlée terminées, mettre à jour ici le vrai commit main, état prod, tests, sauvegarde, branche et questions ouvertes ; fournir un prompt prêt à copier-coller pour le prochain chat. Ne pas conserver de branches mortes dont le merge est attesté sur GitHub ; ne pas toucher aux branches non fusionnées ou aux branches de travail d'agents actifs.


## Situation au 16 octobre 2026

- Dépôt public : Kiwinokoto/budget_fr. PR #1–#23 fusionnées sur `main` le 16 octobre 2026 ; dernier commit applicatif (solde primaire S13) **`6655e063f1572085adace4f5d9252b5df77b3fc3`**. La documentation de passation ultérieure peut faire avancer `main` sans redéploiement.
- Coordination AgentCtl : projet budget-fr, ressource repo:Kiwinokoto/budget_fr ; verrou à prendre avant toute mutation et libérer en fin de passe.
- Base Insee initiale 1995–2025 recopiée à la main **remplacée** par les chiffres du classeur officiel d'août 2026.
- Données 1960–2025 : recettes, dépenses, solde, variantes hors éléments imputés ; dette brute depuis 1978 et nette depuis 1995. Fichier original conservé à la source, pas dans Git.
- Importateur en Python standard, empreinte SHA-256 de la source, validation des libellés, années et solde ; tests couvrant les absences de valeurs.
- Application statique avec curseur temporel et graphiques de recettes/dépenses et dette.
- Site public en ligne : **https://budget-fr.kiwinokoto.fr** sur le VPS personnel, via `/opt/budget-fr`, conteneur `budget-fr-web`, réseau Docker `traefik_network`, routeur Traefik dédié et certificat Let's Encrypt. Déploiement figé sur `6655e063f1572085adace4f5d9252b5df77b3fc3` (`/opt/budget-fr/.deployed_commit`). Aucune base de données, aucune automatisation ou modification des services voisins.
- Vérifications en production : HTTPS HTTP 200 sans `-k`, documents et CSV HTTP 200, trois CSV servis identiques octet par octet à GitHub (66, 30 et 31 années), **32 tests Python et 22 tests Node OK pour la version actuelle**, certificat valide, conteneur démarré, volume statique monté en lecture seule. Recette navigateur **desktop Work (1 363 px)** effectuée ; vérification **responsive automatisée à 390 et 768 px** effectuée pour six pages. Revue esthétique manuelle mobile encore à faire.

- **Historique des axes** : `607dbd8b4fd60c92b47832c701ce9c122f949891` (PR #7), inclus dans les versions applicatives suivantes. L'application servie est désormais `6655e06` ; les commits de documentation ultérieurs ne déclenchent pas de déploiement.

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

## Coût annuel de la dette publique — lot intérêts 1959–2025

- Source Insee **3.201 du 28 août 2026**, S13 consolidé, 1959–2025. Deux définitions d'intérêts D41 et D41G hors correction SIFIM, plus total des dépenses dans **le même millésime**.
- `scripts/import_interest.py` reproductible, SHA-256 originale vérifiée ; `data/interets_apu_1959_2025_bn_eur.csv` 67 années, unités **milliards d'euros courants**.
- `interets.html` : sélection de l'année, courbes des deux conventions, bascule montants / parts de la dépense publique, explications du décalage 2025 65,7/64,7 et distinction **charge d'intérêts (flux)** / **dette Maastricht (stock)**.
- Nav ajoutée sur l'accueil ; méthodologie, sources et tests étendus ; ne pas inférer un taux apparent d'intérêt à partir de séries non homogènes.
- **Drees / modèle Ines** : une demande de tableaux récents agrégés de TVA par décile a été envoyée le **16 octobre 2026** par e-mail privé. Réponse en attente ; **ne pas publier l'adresse de l'expéditeur ni le contenu de l'échange sans accord**. Le travail sur les comptes publics continue en parallèle.
- **Audit visuel navigateur** : prompt préparé pour un contrôle black-box des cinq pages existantes par Work ; **ajouter maintenant la sixième page `interets.html` à la recette**. Aucun résultat de cet audit n'est encore disponible ; **pas de mutation Git par l'auditeur**.
- **PR #19 livrée** : commit `4679431cab4179292690c577573f5c56b64ac520`, page publique https://budget-fr.kiwinokoto.fr/interets.html et CSV 1959–2025 en production.
- **Vérifications** : 27 tests Python et 17 tests Node réussis, scripts JS des six pages validés, import XLSX 3.201 reproduit **octet par octet**, et ancienne source CND.101 reproductible. Clone Git propre.
- **Contrôles HTTPS** : `index.html`, `interets.html`, CSV des intérêts et deux documents de source/méthode identiques octet par octet au commit ; autres pages et CSV historiques préservés.
- **Retour arrière** : sauvegarde `/opt/budget-fr/backup/20261016T162334-interest-before-4679431cab4179292690c577573f5c56b64ac520/`. Aucun redémarrage Docker/Traefik. AgentCtl `deploy:vps-personal/budget-fr` libéré automatiquement, et verrou repo relâché après fusion. Revue graphique mobile toujours ouverte.

## Recette navigateur Work et contrôle responsive — 16 octobre 2026

- **Work (Chrome distant 1 363 px, cinq pages)** : aucun défaut bloquant ou important confirmé, un défaut mineur d’affichage transitoire de « — » sur `recettes.html` et `tva-incidence.html` ; les états mobiles ne sont pas couverts dans le rapport `recette-budget-fr-2026-10-16.md` communiqué dans le chat. Navigation clavier, graphiques et unités cohérents ; aucune erreur JavaScript imputable au site.
- **Audit complémentaire Chromium headless** sur la production à **390 et 768 px** : les **six pages**, y compris `interets.html`, répondent en HTTPS 200, aucun défilement horizontal détecté (`scrollWidth == innerWidth`), aucune erreur JavaScript ; vérification technique, pas revue esthétique manuelle.
- **Correctif livré** : PR #21 fusionnée, SHA applicatif `062f91201a52518665398311938c1a775b99e50c` en production. Sur `recettes.html` et `tva-incidence.html`, contenu dépendant des CSV masqué avant disponibilité, statut accessible « Chargement des données… », message d'erreur avec « Réessayer » en cas d’échec.
- **Tests** : 27 Python + 19 Node = **46 réussis** ; JavaScript des six pages valide ; quatre scénarios Chromium en environnement isolé à 390 px avec chargement CSV ralenti ou volontairement interrompu, étapes attente/résolution/erreur + relance vérifiées. Clone Git propre.
- **Vérification post-déploiement** : deux HTML servis octet par octet identiques à GitHub ; pages et CSV historiques inchangés. Chromium **cache désactivé** : les six pages HTTP 200 aux deux largeurs (390, 768 px), aucun défilement horizontal ni erreur JS, états de données tous résolus (12/12). Ne pas confondre test responsive automatisé et revue graphique humaine.
- **Sauvegarde rollback** : `/opt/budget-fr/backup/20261016T164013-loading-before-062f91201a52518665398311938c1a775b99e50c/`. Aucun conteneur ni service voisin redémarré, coordination AgentCtl respectée.

## Solde primaire public 1959–2025 — livré et vérifié en production

- **Objectif** : distinguer le solde public total B9NF du **solde primaire dérivé** par réintégration des intérêts versés ; lecture historique à périmètre S13 constant, pas le seul budget de l'État.
- **Source auditée** : Insee 3.201 (août 2026, SHA-256 épinglée déjà contrôlée), années **1959–2025**, lignes recettes 58, dépenses 27, B9NF 66, D41 12 et D41G 13. Les valeurs ne sont pas recopiées depuis l'article antérieur de mai 2026 ; **−151,5920 Md€** de solde total en 2025 dans cette version.
- **Dérivation** : `B9NF + D41` (méthode de référence) et `B9NF + D41G` (variante de correction SIFIM), intérêts **payés** uniquement, non net des intérêts reçus, non solde structurel. Pas de ratio de PIB sans source explicite et homogène.
- **Livrables** : script Python standard `scripts/import_primary_balance.py`, `data/solde_primaire_apu_1959_2025_bn_eur.csv` (67 années), graphique `solde-primaire.html` avec année choisie, variantes comptables et Md€ courants ou % des dépenses totales S13 ; lien depuis accueil et la documentation.
- **Garde-fous** : solde primaire **calculé** et non publié tel quel ; statut provisoire 2025, source et révision indiquées ; pas de causalité inférée entre solde primaire et variation du stock de dette.
- **Livraison** : PR #23 fusionnée, commit applicatif exact `6655e063f1572085adace4f5d9252b5df77b3fc3` servi sur https://budget-fr.kiwinokoto.fr/solde-primaire.html.
- **Tests documentés** : **32 Python + 22 Node = 54 tests réussis**, sept scripts JavaScript `node --check` valides ; CSV de solde primaire **identique octet par octet** au calcul depuis l'Excel Insee 3.201 épinglé, ancien CSV intérêts également reproductible.
- **Recette Chromium réel locale et sur le site publié** à **390 et 768 px** : affichage −85,9 Md€ de primaire D41 en 2025, −86,9 Md€ en D41G, solde total −151,6 Md€, exercice 1980 (+3,8 Md€ variante D41G), bascule % dépenses, courbes et ligne zéro ; HTTP 200, aucun débordement horizontal ni erreur JS.
- **Déploiement réversible** : `/opt/budget-fr/backup/20261016T165732-primary-before-6655e063f1572085adace4f5d9252b5df77b3fc3/` (site complet et commit antérieur), cinq fichiers publiés `index.html`, `solde-primaire.html`, CSV, sources et méthodologie identiques aux sources GitHub par HTTPS ; autres pages et CSV inchangés. Aucun conteneur ou proxy redémarré. Verrou AgentCtl de déploiement automatiquement libéré et verrou Git de la PR libéré après fusion.

## Dette publique 3.103–3.105, puis histoire longue : passation du 16 octobre 2026

- **Nouvelle branche** : dev/debt-net-liabilities-stockflow-20261016, indépendante de la PR #25 toujours ouverte (3.102). Trois CSV distincts, importateur SHA-256 strict, tests d'identité interne et ancrages 2025, sans changement de page ni déploiement.
- **Anomalies à conserver** : (a) 3.104/S1314 2025 293,1 Md€ alors que 3.102/S1314 292,6 ; (b) sous-lignes de valorisation du 3.104 insuffisantes pour recomposer le total entre 2014 et 2021, résidu calculé jusqu'à 2,9 Md€ ; (c) différence −0,6 Md€ pour 2014 entre 3.105 variation annuelle et variation calculée des encours 3.104. Ne pas corriger les séries pour les faire coïncider ; demander explication à l'Insee avant visualisation fusionnée.

**Backlog historique différé, avant 1960.** Transcription d'un entretien de Thomas Piketty fournie par Kevin le 16 octobre 2026 : proposition de comparer dette publique, patrimoine privé, patrimoine public, patrimoine national et mesures fiscales de l'après-guerre. Les valeurs avancées par l'interview (environ 300→600 % de PIB pour les patrimoines privés, dette de guerre, rendements d'impôts exceptionnels) sont des déclarations à recouper, pas des données validées. Garder séparées données, simulations, prises de position et politique publique.

Sources candidates à auditer une fois l'atlas contemporain stabilisé :
- Banque de France, Dufrénot et Triki (2012), série historique dette depuis 1890 : https://publications.banque-france.fr/publications-economiques-et-financieres-documents-de-travail/la-dette-publique-et-ses-determinants-depuis-1890-leconometrie-en-soutien-des-faits-historiques
- Federal Reserve Bank of Chicago, Velde (2024), dette de la France 1800–1914 : https://www.chicagofed.org/publications/economic-perspectives/2024/2
- FMI, Historical Public Debt Database, https://www.imf.org/external/datamapper/datasets/DEBT
- Banque de France, patrimoine et comptes financiers depuis 1977 : https://www.banque-france.fr/fr/publications-et-statistiques/publications/quatre-decennies-de-patrimoine-et-dendettement-en-france
- Éventuellement WID / travaux de Piketty pour patrimoine privé/public, à évaluer comme source distincte.

**Critères avant une extension pré-1960 :** vérifier périmètres (État/APU), frontières, finances de guerre, dette perpétuelle ou négociable, définitions du PIB et du patrimoine, devises, inflation, ruptures, trous, révisions et quantification de l'incertitude. Prévoir un module historique autonome et des courbes non reliées artificiellement aux séries Maastricht contemporaines. Priorité immédiate inchangée : finaliser les données actuelles, puis construire l'explorateur de dette.

## Explorateur de composition de dette — 16 octobre 2026

- PR #25 et #26 fusionnées sur main (SHA 6eb4c61b1e7458b21ad44d210bd0901537024a3e), sans déploiement. Nouvelle branche dev/debt-explorer-1995-2025.
- Page interactive dette.html, navigation d'accueil, graphiques de composition en parts de dette ou Md€ courants, sélection année 1995–2025 et sous-secteur, dette brute/nette et tableau déficit/variation depuis 2009 (total APU seulement). Scripts et CSV Insee déjà épinglés par les PR précédentes.
- Divergences source toujours présentes : 3.102 vs 3.104 pour S1314 en 2025 (292,6 vs 293,1 Md€), résidus des sous-lignes de valorisation du 3.104 en 2014–2021, écart de 0,6 Md€ sur la variation 2014. Une discordance de millésime/actualisation partielle est une hypothèse non confirmée ; notes Insee 3.104/3.105 consultées.
- Suite : contrôler EDP/Eurostat, recette visuelle et accessibilité, puis déploiement manuel sur validation ; longue histoire avant 1960 toujours différée.

## Recette scientifique Eurostat et navigateur (16 octobre 2026)

- **Eurostat EDP** (API France, dernière mise à jour 22 avril 2026) : dette Maastricht S13 de fin 2025 = 3 460,4651 Md€ ; S1314 selon la définition EDP = 293,0774 Md€. **Eurostat GGD** de juin 2026 confirme 3 460,4651 Md€ pour S13. La notification Insee de mars 2026 donne 3 460,5 Md€ et 293,1 Md€ ; le fichier Insee 3.102 du 28 août donne 3 460,1 Md€ et 292,6 Md€ ; le 3.104 d'août conserve 293,1 Md€ dans S1314 malgré le nouveau total S13. Cela soutient une **discordance de millésime**, mais pas une cause démontrée. Ne pas additionner automatiquement les sous-secteurs EDP aux contributions Insee : périmètre/consolidation distincts. **Audit daté :** [DEBT_RECONCILIATION.md](DEBT_RECONCILIATION.md).
- Les écarts 2014 (variation de stock −0,6 Md€) et 2014–2021 (décomposition de valorisation jusqu'à 2,9 Md€) restent **non élucidés**, sans correction.
- **Recette réelle** du dernier commit de PR #27 avant fusion : navigateur Chromium via Puppeteer, viewport 390/768/1365 px, sélections 1995/2014/2020/2021/2025 et secteurs S13/S1311/S1314, chiffres, graphiques, changement d'unités, clavier, erreurs de chargement suivies de réessai ; **23 vérifications fonctionnelles réussies**. Aucun débordement horizontal ni exception JavaScript observé. Labels et rôles de contrôles et graphiques vérifiés ; lecteur d'écran et audit de contraste instrumenté non effectués.
- **Validation hors production :** 44 tests Python et 27 tests Node réussis avant ce complément documentaire ; pas de CI GitHub signalée. Prochaine étape après fusion : recette manuelle finale de publication et déploiement uniquement sur demande explicite.

## Recette accessibilité Work — correctifs ciblés du 16 octobre 2026

- **Audit fourni** : revue navigateur de dette.html sur main b8923d0 (recette Work, Chromium 154, 500/390/768/1365 px ; pas de lecteur d'écran réel). Verdict Work : publication déconseillée avant correction de deux obstacles majeurs : graphiques illisibles sur petits écrans, absence d'alternative annuelle complète.
- **Lot de correction** dev/debt-accessibility-20261016 : graphiques SVG de largeur minimale 900 px dans un conteneur horizontalement défilable et atteignable au clavier (indices de navigation, axes avec unités) ; un tableau HTML natif déroulable de **31 années × 9 colonnes**, valeurs Insee d'origine, cinq instruments, reste calculé identifié, dette brute/nette. S1314/F2N reste « Non renseigné », reste « Non calculable » si composante non renseignée ; pas de zéro fabriqué. SVG liés à des résumés de tendance textuels ; états de sélection annoncés via live region ; focus déplacé vers le sélecteur après récupération d'erreur.
- **Validation réalisée** : 44 tests Python, 30 tests JavaScript et 21 vérifications fonctionnelles Chromium sur 390/500/768/1365 px (défilement au clavier, absence de débordement de page, tableau 31 années, données manquantes, unités, changement de sélection, reprise d'erreur et focus). La capture 500 px a été inspectée. Un audit complémentaire axe-core 4.10.3 sur cinq états (390/500/1365 px) n'a relevé aucune anomalie majeure ou critique ; les deux défauts modérés de repères HTML main/région ont été corrigés dans la PR. Une analyse ciblée de l'attribut ARIA de légende l'a converti en groupe explicitement nommé. Axe-core ne peut pas conclure au contraste du texte SVG sur fond complexe : vérification complémentaire avec aide technique toujours à faire. Contre-recette lecteur d'écran réel encore à faire. Tests de lecteur d'écran réel (NVDA/Orca/VoiceOver), zoom navigateur natif à 200/400 % et audit RGAA complet **non réalisés** ; ne pas présenter le correctif comme une certification de conformité.
- **Sans déploiement** ; ne fusionner qu'après validation et revue. Une nouvelle recette de publication avec lecteurs d'écran reste possible ultérieurement.

## Passe produit UX / navigation — 17 octobre 2026

**Constat d'usage** : sur fonctions.html, sélectionner un poste dans la liste imposait de descendre jusqu'au graphique, remonter pour changer de poste et redescendre. Les pages utilisaient des liens retour hétérogènes ; des analyses étaient découvertes fortuitement, et l'accueil plaçait sept liens éditoriaux avant les graphiques.

### Lot 1 — dev/atlas-ui-navigation-20261017 (à valider)
- **Dépenses COFOG** : pour les grands écrans (≥ 1 050 px), présenter les dix dépenses et le graphe dans la même zone, en deux colonnes ; conserver le graphique à portée de vue grâce à position:sticky, sans scroll automatique ni piège de scroll. Sur petits écrans, la mise en page reste verticale. Les clics changent l'état sélectionné et la courbe **sans reconstruire ni déplacer le focus de la liste**, ce qui préserve la navigation au clavier et le défilement. Une phrase visible et annoncée donne montant, année et pourcentage de la sélection.
- **Navigation transverse** : même bandeau compact sur les huit pages statiques (accueil, dépenses, recettes, solde primaire, intérêts, dette, deux analyses TVA), onglet courant avec aria-current=page, navigation horizontale défilable sur petits écrans, style partagé dans atlas-nav.css sans JavaScript supplémentaire. L'accueil expose les analyses dans des cartes **après** les deux premiers graphiques, plutôt que d'intercaler sept liens verticaux avant tout graphique.
- **Aucune modification scientifique** : CSV, calculs des montants, périmètres, dates, unités et méthodologie conservés. GitHub reste la source canonique. Pas de déploiement automatique.
- **Contrôles réalisés** : 44 tests Python, 36 tests Node, 23 tests navigateur Chromium (390/768/1050/1365/1600 px, huit pages, changement de postes/année, focus conservé, sticky desktop, aucune overflow globale). Correction de la marge gauche des graduations de la courbe ajoutée après revue visuelle. Les captures de recette desktop et mobile sont conservées hors dépôt ; contrôle de lecture vocale réelle et zoom 200/400 % à prévoir indépendamment.

### Backlog UX — ordonné, indépendamment du lot 1
1. Vérifier en navigateur les choix de poste et le graphe au clavier après *plusieurs* changements de sélection, à 100/200 % et pour toutes les largeurs intermédiaires. Recette qualitative utilisateur sur le placement de la courbe ; adapter les proportions des colonnes si nécessaire.
2. Étendre le motif **liste + graphique côte à côte** aux pages de **recettes** et éventuellement aux sélections des analyses TVA après inspection de leurs interactions et de leurs erreurs réseau (ne pas dupliquer précipitamment la grille des dépenses).
3. Rationaliser l'en-tête des autres pages (titres, chapeaux, paddings, métriques, notes SIFIM), en gardant les mises en garde statistiques lisibles et sans les masquer systématiquement.
4. Revoir les détails mobiles : repère du bandeau d'onglets, découverte des liens masqués horizontalement, taille des graduations, focus au zoom 200/400 %, lecteur d'écran réel. Aucune affirmation RGAA globale sans audit complet.
5. Réfléchir à une **vue comparative** entre dépense/PIB, recettes/PIB, solde primaire, dette/PIB et charge d'intérêts pour permettre de tester les hypothèses de stabilité et de financiarisation ; définir millésimes, indicateurs et interprétations avant tout graphique causal.
6. Ne pas attribuer les évolutions 2007–2008 ou 2012–2017 à une politique unique sans contrôler conjoncture, refinancement, nomenclatures et comparaison internationale. Les événements économiques et marqueurs gouvernementaux éventuels seront présentés comme contexte, non comme causalité statistique observée.

## APPRENTISSAGE — série historique Insee/Depp-SIFA (17 octobre 2026)

**Travail effectué dans dev/apprentissage-sifa-history-20261017** : source Insee T04/T1 de novembre 2025 téléchargée, 336409 octets et SHA-256 vérifié ; import reproductible sans dépendance depuis le XLSX non committé en 43 observations d'effectifs au 31/12, 1982–2024, cinq niveaux de diplôme et total validé par addition. CSV, script et provenance dans APPRENTISSAGE_SOURCES.md.

- Graphique interactif en deux modes (évolution du total, composition par diplôme), sélection 1995–2024 (défaut) ou 1982–2024 ; tableau complet de 43 années, résumé textuel, source affichée. **Aucun mélange** avec contrats Dares 2024/2025 ou coût France compétences.
- **Rupture de champ** : hors Mayotte jusqu'en 2010, France avec Mayotte depuis 2011. L'axe 2018 est un repère historique, non une inférence causale sur le financement.
- **Observation scientifique** : CAP/mention stable en niveau absolu entre 1995 (194485) et 2024 (191029), tandis que bac+3 et plus croît de 4777 à 421000. Prendre garde aux évolutions des nomenclatures et des cursus.
- **Blocage source** : le téléchargement direct Dares du XLSX « Caractéristiques des contrats d'apprentissage » 1993–2025 est bloqué par protection anti-robot. Les trois systèmes de collecte Dares (1993–2011 / 2012–2019 / depuis 2020) sont repérés mais **aucune série non vérifiée ne doit être inventée**.
- **Recette de cette passe** : 48 tests Python, 49 tests JavaScript, 16 contrôles navigateur ciblés Chromium (390, 768, 1050, 1365 px, 2 modes de graphique, 2 périodes, tableau HTML complet, aucune overflow globale). Comparaison octet pour octet du CSV régénéré depuis l'original XLSX et revue visuelle desktop/mobile. L'évaluation de lecteur d'écran réel reste à faire.
- **Étapes suivantes** : série détaillée Dares si XLSX vérifiable ; comparaisons SIFA secondaire/supérieur, niveaux CAP et financement ; série temporelle financière par financeur avec sources homogènes ; évaluation ruptures/retours/insertion. Accueil hybride et maquette globale toujours différés.

## APPRENTISSAGE — PRIORITÉ HAUTE, CHAPITRE AUTONOME (17 octobre 2026)

**Demande explicite** : faire de l'apprentissage un onglet séparé et un véritable thème d'enquête, pas une simple ligne d'« aides aux entreprises ». Sujets : histoire, sommes mobilisées, flux de nouveaux contrats, effectifs en formation, financeurs, bénéficiaires, diplômes et devenir.

**Premier lot** : branche dev/apprentissage-autonome-20261017, fondée sur la PR #30 dev/aides-entreprises-perimetres-20261017. Dépendance volontaire pour la navigation à dix chapitres ; ne pas fusionner avant la PR #30.
- apprentissage.html : onglet spécifique, lecture introductive, comparateur Dares contrats commencés/en cours 2024–2025 (sélection clavier), financement 2024 séparé selon France compétences, frise de jalons juridiques 1919/1925/1928/1971/1987/2018/2020, liens avec les aides aux entreprises.
- Données ponctuelles : data/apprentissage_dares_2024_2025_indicateurs.csv (2 années, 4 valeurs, millésimes Dares distincts), data/apprentissage_financement_2024_france_competences.csv (15,6 Md€ engagements 2024, coût unitaire 17 404€, aide aux entreprises 5 983€ par contrat, parts arrondies).
- Source et définitions APPRENTISSAGE_SOURCES.md. Contrats commencés ≠ apprentis uniques ≠ contrats en cours au 31/12 ; 2025 estimation préliminaire. Champ Dares privé/public différent des engagements France compétences secteur privé. Les 15,6 Md€ ne sont pas une nouvelle subvention automatiquement additionnable aux 211 Md€ Sénat.

**Backlog scientifique APPRENTISSAGE** :
1. Importer les séries Dares 1993–2025 depuis XLSX officiel avec hash, champs, millésimes et ruptures ; graphiques distincts entrées/effectifs. Ventiler secondaire/supérieur et diplômes CAP, bac, BTS, licence/master.
2. Construire une série financière harmonisée à partir des rapports France compétences (engagements/dépenses, aides employeurs, coûts pédagogiques, État/OPCO/France compétences/Régions, en conservant les fonds et conventions).
3. Explorer âge, sexe, handicap, ruptures, diplômes obtenus, insertion, rémunération et mobilité ; distinguer effets causaux et corrélations observées.
4. Enquêter sur les CFA, écarts de financement selon diplôme, maître d'apprentissage et conditions des aides 2020–2026.
5. Histoire du système : 1919/1925/1928/1971/1987/2018 et dispositifs exceptionnels 2020, avec sources légales ; apprentissage médiéval = antécédent et non statistique moderne.
6. Accueil hybride ultérieur : ajouter une question pédagogique « Comment fonctionne l'apprentissage ? » sans refaire l'accueil avant une maquette.

**Recette initiale** : 44 tests Python, 45 tests JavaScript et 18 contrôles Chromium (390/768/1365 px, deux indicateurs, clavier, 10 pages, zéro débordement global). Capture desktop examinée. Toujours besoin d'un test réel de lecteur d'écran et d'une vérification approfondie du détail scientifique avant publication.

**UI** : page autonome plus claire, éditoriale, expérimentale ; ne pas appliquer cette DA à l'ensemble de l'atlas sans recette visuelle. **Aucun déploiement automatique.**

## Priorités actualisées — 17 octobre 2026

**Horizon temporel utile** : privilégier une observation rigoureuse et traçable depuis 1995 lorsqu'elle existe, et assumer une période plus courte, par exemple 2019–2023 ou une seule année, lorsque la source n'offre pas mieux. Une histoire de 1830 reste une possibilité, jamais une obligation. Séparer les séries de nature, champs et millésimes différents.

**Hypothèse née de l'atlas** : la stabilité des grandes parts des dépenses et recettes ne signifie pas absence de changements dans les sous-postes, prélèvements, niches fiscales, bénéficiaires ou règles de classement. Ne pas inférer une causalité politique à partir d'une courbe descriptive.

### Aides publiques aux entreprises — premier chapitre et programme de recherche

- **Question** : pourquoi les « 200 milliards » ne sont-ils pas visibles dans COFOG, qui bénéficie des aides, quelles contreparties et quels contrôles sont documentés ?
- **Source de départ** : rapport Sénat n° 808, adopté le 1er juillet 2025, estimations de 2023 : 108 Md€ (sens strict) et 211 Md€ (sens large). Ce sont des **ordres de grandeur/planchers**, pas un compte exact des aides aux seules grandes entreprises ni des sommes dépourvues de contrepartie. Périmètre large incluant prêts, garanties et dépenses fiscales déclassées ; périmètre strict les écartant, ainsi que les avantages fiscaux TVA. Source complète et réserves dans AIDES_ENTREPRISES_SOURCES.md.
- **Interdiction de fausse série** : IGF 2022 (64 Md€ pour budget + fiscalité de l'État, excluant notamment social et local), France Stratégie 2019 (139–223 Md€ selon périmètre) et Sénat 2023 (108–211 Md€) ne sont **pas comparables en l'état**. Aucun graphique historique ne les relie.
- **Première livraison de lecture des périmètres** : page aides-entreprises.html (choix des définitions, mécanismes, correspondance conceptuelle COFOG, sources), CSV de deux estimations ponctuelles, tests de cohérence et navigation commune. Brancher au site uniquement après vérification et accord de publication.
- **Recette de cette passe** : 44 tests Python, 40 tests JavaScript, 17 contrôles Chromium (390, 768 et 1 365 px, sélection strict/large à la souris et au clavier, neuf navigations, liens sources et absence de débordement). Capture desktop inspectée. Pas de lecteur d’écran réel ni d’audit RGAA exhaustif. Aucune donnée issue des rapports IGF/France Stratégie ajoutée comme série comparable au Sénat.
- **Prochain travail scientifique** : dictionnaire d'aides (code, année, organisme, financement, nature, destinataire, montant/assiette, source, contrôle, risque doublon) ; approfondir séparément les allègements de cotisations, le CIR et l'aide à l'apprentissage ; identifier et dater des séries annuelles par dispositif ; documenter existence de critères, contrôles et évaluations plutôt que présumer leur absence ; rechercher des informations ouvertes sur bénéficiaires.
- **Périmètres techniques** : ne pas assimiler données de dépenses COFOG, moins-values fiscales, subventions comptables, engagements/encours Bpifrance et prestations de services publics. Les comparaisons de montants doivent préserver champs et années.

### UI et pédagogie, lots ultérieurs

- **Maquette d'abord** : la zone précédant les graphiques est encore trop dense ; développer une direction éditoriale plus légère et minimaliste, sans imposer une refonte globale ni commencer par un switch jour/nuit. La page aides expérimente une mise en page claire distincte, à faire évaluer avant adoption.
- **Accueil hybride** : quelques graphiques synthétiques + choix guidés par questions (« à quoi servent les dépenses ? », « qui finance ? », « pourquoi la dette augmente ? », « où sont les aides ? »). Préserver la libre exploration.
- **Priorités** : guider l'usager non spécialiste, conserver provenance et unités à portée de vue, simplifier les contrôles ; reporter les améliorations purement esthétiques si elles bloquent l'enquête.

## Suite prioritaire

1. Valider le rendu sur un vrai navigateur mobile et l'accessibilité ; les captures desktop sont encourageantes mais ne valident pas le mobile.
2. Documenter et mesurer les écarts entre les publications Insee de mai et août 2026.
3. ~~Rechercher des séries détaillées COFOG 1995–2024~~ : **premier niveau COFOG S13 intégré** (mars 2026, dix catégories, euros courants). Prochaine étape : explorer sous-fonctions, harmoniser les millésimes et déceler les reclassements.
4. ~~Identifier les principales recettes par impôt~~ : premier lot de prélèvements obligatoires 1995–2025 intégré avec contrôle des doubles comptes, TVA, IRPP, IS, CSG/CRDS et cotisations. **Intérêts annuels 1959–2025 intégrés** ; poursuivre : revenus non fiscaux, dette par instrument, solde primaire et patrimoine.
5. **TVA et justice fiscale :** enquêter sur la disponibilité de la TVA seule réellement estimée et rapportée au revenu/consommation dans une enquête récente, puis étendre aux taux réduits et à la redistribution élargie. Maintenir strictement les distinctions 2001 estimée / Ines 2014 TVA seule / 2016 choc simulé / 2020–2023 taxes sur produits / simulation 2025. Ensuite formaliser la traçabilité budgétaire.
6. Faire une vraie revue visuelle et une vérification responsive, puis envisager un déploiement automatisé uniquement si cela devient utile (actuellement manuel et volontaire).

## Risques

Ruptures comptables, révisions du millésime, séries partielles, faux rapprochements de périmètres, transfert doublement compté, confusion entre fiabilité de la publication et qualité politique ou efficacité de la dépense.

Passation : GitHub reste la source canonique ; ne pas laisser de fichiers importants dans une copie locale. Tester puis vérifier branche, HEAD, lease et état propre avant de conclure.

## Dette publique : premier import Insee 3.102 (16 octobre 2026)

- **Branche de travail** : `dev/debt-maastricht-instruments-1995-2025`, proposition destinée à une PR sur `main` ; aucun déploiement automatique demandé.
- **Terminé** : audit et import reproductible du fichier officiel Insee 3.102, version du 28 août 2026, SHA-256 épinglée, **1995–2025**, six périmètres et sept codes, **186 observations année×secteur**. CSV dérivé validé depuis le XLSX.
- **Point scientifique** : S1314/F2N est non renseigné pour les 31 années (cellules vides conservées, non remplacées par des zéros). Les sous-totaux centraux et les titres F31/F32 ne sont jamais recomptés.
- **Contrôles** : tests Python et JavaScript de non-régression exécutés avant commit ; `git diff --check` ; fichier exporté identique octet à octet à la reproduction depuis l'XLSX officiel. Aucun graphique n'est publié dans ce lot.
- **Suite** : (1) audit complet de 3.101 pour 1978–1994 sans extrapolation ; (2) imports séparés 3.103–3.105 avec équations de réconciliation ; (3) validation des cellules françaises Eurostat par détenteur/maturité ; (4) conception du nouvel explorateur de dette puis recette responsive et déploiement contrôlé, après PR appropriée.
- **Restriction** : ne pas assimiler dette Maastricht de S13, dette négociable de l'État, dette nette, passifs financiers hors Maastricht ou durée résiduelle. Les années 2024–2025 sont sujettes à révision.
