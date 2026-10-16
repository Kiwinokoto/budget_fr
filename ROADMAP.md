# Roadmap et passation

## Situation au 16 octobre 2026

- Dépôt public : Kiwinokoto/budget_fr. PR #1–#9 fusionnées sur `main` le 16 octobre 2026 ; dernier commit applicatif (unités) **`2501217d2bba01c729d65d4724ff69d39d44d5f7`**. La documentation de passation ultérieure peut faire avancer `main` sans redéploiement.
- Coordination AgentCtl : projet budget-fr, ressource repo:Kiwinokoto/budget_fr ; verrou à prendre avant toute mutation et libérer en fin de passe.
- Base Insee initiale 1995–2025 recopiée à la main **remplacée** par les chiffres du classeur officiel d'août 2026.
- Données 1960–2025 : recettes, dépenses, solde, variantes hors éléments imputés ; dette brute depuis 1978 et nette depuis 1995. Fichier original conservé à la source, pas dans Git.
- Importateur en Python standard, empreinte SHA-256 de la source, validation des libellés, années et solde ; tests couvrant les absences de valeurs.
- Application statique avec curseur temporel et graphiques de recettes/dépenses et dette.
- Site public en ligne : **https://budget-fr.kiwinokoto.fr** sur le VPS personnel, via `/opt/budget-fr`, conteneur `budget-fr-web`, réseau Docker `traefik_network`, routeur Traefik dédié et certificat Let's Encrypt. Déploiement figé sur `2501217d2bba01c729d65d4724ff69d39d44d5f7` (`/opt/budget-fr/.deployed_commit`). Aucune base de données, aucune automatisation ou modification des services voisins.
- Vérifications en production : HTTPS HTTP 200 sans `-k`, documents et CSV HTTP 200, trois CSV servis identiques octet par octet à GitHub (66, 30 et 31 années), **14 tests Python OK**, certificat valide, conteneur démarré, volume statique monté en lecture seule. Revue visuelle navigateur desktop/mobile **encore à faire**.

- **Version applicative publique actuelle (axes 5 ans)** : `607dbd8b4fd60c92b47832c701ce9c122f949891`, après PR #7, distincte des versions précédentes conservées dans l'historique. `main` peut évoluer ensuite par commits documentaires non déployés.

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

## Suite prioritaire

1. Valider le rendu sur un vrai navigateur mobile et l'accessibilité ; les captures desktop sont encourageantes mais ne valident pas le mobile.
2. Documenter et mesurer les écarts entre les publications Insee de mai et août 2026.
3. ~~Rechercher des séries détaillées COFOG 1995–2024~~ : **premier niveau COFOG S13 intégré** (mars 2026, dix catégories, euros courants). Prochaine étape : explorer sous-fonctions, harmoniser les millésimes et déceler les reclassements.
4. ~~Identifier les principales recettes par impôt~~ : premier lot de prélèvements obligatoires 1995–2025 intégré avec contrôle des doubles comptes, TVA, IRPP, IS, CSG/CRDS et cotisations. Poursuivre : revenus non fiscaux, dette, intérêts, solde primaire et patrimoine.
5. **TVA et justice fiscale :** poursuivre l'inventaire des tableaux effectivement exploitables par groupe de niveau de vie, et publier seulement des comparaisons avec années, dénominateurs et incertitudes. Ensuite formaliser la traçabilité budgétaire.
6. Faire une vraie revue visuelle et une vérification responsive, puis envisager un déploiement automatisé uniquement si cela devient utile (actuellement manuel et volontaire).

## Risques

Ruptures comptables, révisions du millésime, séries partielles, faux rapprochements de périmètres, transfert doublement compté, confusion entre fiabilité de la publication et qualité politique ou efficacité de la dépense.

Passation : GitHub reste la source canonique ; ne pas laisser de fichiers importants dans une copie locale. Tester puis vérifier branche, HEAD, lease et état propre avant de conclure.
