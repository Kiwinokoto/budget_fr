# Roadmap et passation

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
