# budget_fr

Atlas historique et critique des finances publiques françaises — prototype expérimental.

## Démonstrateur (sans dépendance)

Recettes, dépenses et solde des administrations publiques consolidées de **1960 à 2025** ; dette brute de **1978 à 2025**, dette nette de **1995 à 2025**, le tout en **% du PIB**. La période demandée 1980–2025 est couverte, avec les limites propres à chaque série.

Pour consulter localement :

~~~bash
python3 -m http.server 8000
# http://localhost:8000
~~~

Pour tester :

~~~bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tests
~~~

Pour reproduire le CSV depuis la version officielle du fichier Insee (28 août 2026) :

~~~bash
python3 scripts/import_insee.py
# ou hors ligne :
python3 scripts/import_insee.py --xlsx /chemin/econ-fin-pub-rec-dep.xlsx
git diff -- data/apu_1960_2025_pct_pib.csv
~~~

L'importateur vérifie la **SHA-256** du XLSX et refuse une mise à jour silencieuse. En cas de révision de la source, auditer les changements avant d'utiliser explicitement l'option --allow-source-change.

## Solde primaire calculé : finances publiques hors charge des intérêts (1959–2025)

**[Explorer le solde primaire annuel](solde-primaire.html)** : comparer, année par année, le solde public total **B9NF** et le solde primaire **dérivé** en réintégrant les intérêts versés. Les deux séries sont de même périmètre et issues du même [tableau Insee 3.201 (août 2026)](https://www.insee.fr/fr/statistiques/8988845), secteur S13 consolidé, années 1959–2025.

- Calcul de référence : **solde primaire D41 = B9NF + intérêts D41**. Variante en affichage : **B9NF + D41G**, intérêts avant correction SIFIM, sans modifier le solde total. Il s'agit de **deux conventions alternatives**, pas de deux charges cumulables.
- En 2025, dans la version d'août : **−151,5920 Md€** (B9NF) + **65,7209 Md€** (D41) = **−85,8711 Md€** (solde primaire) ; variante D41G **−86,9401 Md€**. Les données d'une publication antérieure (mai) peuvent être différentes.
- Affichages : **Md€ courants** ou **% des dépenses totales du même classeur**, **pas % du PIB**. Les données ne sont pas déflatées, et le solde primaire n'est pas corrigé du cycle économique.
- Données versionnées dans `data/solde_primaire_apu_1959_2025_bn_eur.csv`, calcul reproductible depuis le même fichier source officiel épinglé par empreinte : `python3 scripts/import_primary_balance.py` (ou `--xlsx /chemin/t_3201_fr.xlsx`). Aucun fichier source Excel n'est commité.

## Intérêts de la dette publique et dépenses S13 (1959–2025)

**[Explorer la charge annuelle d'intérêts](interets.html)** : deux mesures officielles de charges d'intérêts des administrations publiques consolidées, en milliards d'euros courants et en part de la dépense publique totale : D41 et D41G (hors correction au titre des services d'intermédiation financière indirectement mesurés, SIFIM). **Ce sont des conventions alternatives, jamais deux dépenses à sommer**, ni le stock de dette de Maastricht.

Source [Insee tableau 3.201](https://www.insee.fr/fr/statistiques/8988845), version du 28 août 2026, années 1959–2025, base des comptes nationaux 2020. Import Python standard avec SHA-256 épinglée :

~~~bash
python3 scripts/import_interest.py
# hors ligne : python3 scripts/import_interest.py --xlsx /chemin/t_3201_fr.xlsx
~~~

En 2025, D41 = 65,7 Md€ et D41G = 64,7 Md€ (arrondis à une décimale) ; la deuxième valeur est celle de la synthèse Insee. Tous les montants sont **courants, non déflatés**. Le ratio affiché est un **pourcentage des dépenses**, pas un taux d'intérêt ni un pourcentage du PIB.

## Dépenses par fonction (COFOG)

**[Explorer les dépenses par fonction](fonctions.html)** : dix grandes catégories de dépenses consolidées (protection sociale, santé, enseignement, défense, etc.), séries Insee 3.301 **1995–2024**, en **milliards d’euros courants**. Sélection de l’année, part des dépenses totales, montants et évolution relative des catégories.

Reproduction avec la source officielle du 27 mars 2026 :

~~~bash
python3 scripts/import_cofog.py
# ou hors ligne : python3 scripts/import_cofog.py --xlsx /chemin/T_3301.xlsx
~~~

**Attention :** les montants COFOG ne sont pas des pourcentages du PIB ; ils ne sont pas corrigés de l'inflation et ne doivent pas être additionnés aux agrégats d'un autre millésime statistique. 2025 non disponible dans cette source.

## Origine des prélèvements obligatoires (1995–2025)

**[Explorer les recettes et prélèvements](recettes.html)** : neuf catégories fiscales et de cotisations effectives mutuellement exclusives, plus les ajustements négatifs nécessaires pour retrouver le **total net** des prélèvements obligatoires. Sont également affichés, **sans les additionner une seconde fois**, l'IRPP et l'IS avant crédits d'impôt, la CSG et la CRDS.

Source Insee **3.217**, 1995–2025, milliards d'euros courants ; taux de prélèvements obligatoires en % du PIB issu de **la même source**. Import reproductible :

~~~bash
python3 scripts/import_recettes.py
# ou hors ligne : python3 scripts/import_recettes.py --xlsx /chemin/t_3217_fr.xlsx
~~~

Attention : les prélèvements obligatoires ne constituent pas toutes les recettes publiques ; l'incidence distributive de chaque impôt n'est pas directement déductible de ses montants agrégés. L'année 2025 reste provisoire.

## TVA et niveau de vie : une première simulation distributive

**[Explorer les effets simulés par décile](tva-justice.html)** : dix déciles de personnes, scénario d'une hausse de trois points du taux normal de TVA, d'après la figure 2 d'Insee Analyses 43 (2019), population et législation de référence 2016. Graphiques comparant l'effet des prélèvements indirects et l'effet total simulé après trois ans ; détail des composantes.

**Important :** ni TVA acquittée par décile, ni données distributives observées en 2025, ni indice composite de justice fiscale. Source originale : [Insee Analyses 43](https://www.insee.fr/fr/statistiques/3713290) ; valeurs officiellement publiées retranscrites à une décimale et testées. Voir [méthode](METHODOLOGY.md) et [traçabilité](DATA_SOURCES.md).

## TVA seule estimée : répartition entre déciles Ines 2014

[La vue « TVA et fiscalité indirecte »](tva-incidence.html) inclut la répartition en **dix déciles** du montant de TVA estimé par le modèle officiel **Ines 2014**, issu de [Drees, document de travail n°60 (2016), tableau 16](https://drees.solidarites-sante.gouv.fr/sites/default/files/2020-10/dt60.pdf). D1 : **4,3 %** du total simulé ; D10 : **18,5 %**. CSV `data/tva_part_deciles_ines_2014.csv`, somme contrôlée à 100 %. Il s'agit de **parts des montants** et non de TVA rapportée au revenu. Ni observation directe, ni données actuelles.

**Poursuite de l'enquête** : [documentation Ines](https://ines-public-e766af.gitlab.io/modules_annexes.html) et [accès CASD à BDF 2017](https://www.casd.eu/source/enquete-budget-de-famille/) identifiés. Les tableaux publics ne fournissent pas la TVA payée par ménage/décile en 2023–2025 ; demande de données agrégées / accès microdonnées à étudier.

## TVA seule : étude distributive récente, publiée en 2025

[L'étude DG Trésor, Trésor-Éco n°371 (septembre 2025)](https://www.tresor.economie.gouv.fr/Articles/2025/09/25/analyse-de-la-composition-des-recettes-de-tva) a été intégrée à [l'explorateur de TVA](tva-incidence.html). Son graphique 4 décrit les conséquences **statiques hypothétiques** d'une hausse d'un point de pourcentage **de tous les taux** : Q1 −0,7 % de pouvoir d'achat, Q5 −0,4 %, ensemble −0,5 %. Q1 représente 12 % et Q5 31 % des **recettes supplémentaires** d'une telle hausse. Les Q2–Q4 ne sont pas extrapolés numériquement.

Publication 2025, mais données sous-jacentes BDF 2017, ERFS 2022 et comptabilité nationale 2021–2022. **Ce n'est toujours pas la TVA effectivement payée par décile en 2025**, et ces variations de pouvoir d'achat ne sont pas comparables numériquement aux taux TVA/revenu de 2001.

## Fiscalité indirecte : taux d'effort et comptes distribués

**[Comparer TVA/revenu, TVA/consommation et taxes sur les produits](tva-incidence.html)** : deux jeux de données **méthodologiquement distincts**.
- **Enquête Budget de famille 2001** : estimations de TVA par décile issues de Ruiz et Trannoy (2008), tableau 3 (euros par ménage), tableau 4 (TVA en % du revenu disponible brut) et tableau 6 (TVA en % de la consommation). **Ni mesure directe auprès de la DGFiP ni série 2025**.
- **Comptes nationaux distribués 2020–2023** : taxes sur les produits (TVA, TICPE, accises, DMTO, etc.) par vingtième de niveau de vie usuel, Insee CND.101, publication 2026. **Ce n'est pas la TVA seule**. Import reproductible : `python3 scripts/import_cnd_product_taxes.py`.
- Jamais superposer ces données de périodes, périmètres et unités différentes sur un axe commun ; afficher les unités et la provenance à chaque étape.

**Graduations temporelles :** tous les 5 ans sur ordinateur et tous les 10 ans en affichage compact, année finale toujours affichée ; curseur signalé par un repère vertical discret. [Tests des axes](tests/year_axes.test.cjs) : `node --test tests/year_axes.test.cjs`.

**Justice fiscale (cadrage en cours) :** [TVA, incidence et limites des données](TVA_JUSTICE_SOURCES.md). Aucune série de TVA par décile n'est encore présentée comme une observation récente.

## États de chargement et recette navigateur

Sur les vues **Recettes** et **TVA / niveau de vie**, « Chargement des données… » est distinct de « — » (valeur manquante). En cas d'échec de téléchargement CSV, un message d'erreur propose **Réessayer**. Correction issue de la recette Work du 16 octobre 2026.

- Work : cinq pages en navigateur à **1 363 px** ; aucun problème majeur confirmé, un défaut mineur corrigé.
- Contrôle responsive complémentaire en Chromium headless : **six pages**, à **390 et 768 px**, sans débordement horizontal ni erreur JavaScript ; 12 chargements publics réussis après correctif, plus 4 scénarios simulant un réseau lent ou indisponible.
- **Limite** : une revue esthétique manuelle sur un vrai appareil mobile n'a pas encore été effectuée.

## Explorer la dette publique (1995–2025)

La page [dette.html](dette.html) distingue les encours par administration et instrument (Insee 3.102), la dette nette (3.103), le passage des passifs financiers vers Maastricht (3.104) et le pont déficit→variation annuelle de dette (3.105, S13 et 2009–2025 seulement). Tous les écarts statistiquement non résolus restent explicités.

Documentation : [sources](DATA_SOURCES.md), [méthodologie](METHODOLOGY.md), [passation et roadmap](ROADMAP.md).

**Site public : https://budget-fr.kiwinokoto.fr** (première publication vérifiée le 16 octobre 2026). Déploiement statique isolé sur le VPS personnel, derrière Traefik et Let's Encrypt. Version applicative effectivement servie après la vue solde primaire : `6655e063f1572085adace4f5d9252b5df77b3fc3` (incluant https://budget-fr.kiwinokoto.fr/recettes.html et https://budget-fr.kiwinokoto.fr/fonctions.html). Les changements de documentation ultérieurs sur `main` ne sont pas déployés automatiquement ; voir [la procédure d'exploitation](deploy/README.md).

Ce dépôt public ne contient aucune donnée personnelle ni confidentielle. Les données originales de l'Insee restent sous leurs propres conditions de réutilisation. Les séries peuvent être révisées.

**Ne pas confondre** finances publiques consolidées et budget de l'État seul, déficit et dette, chiffres exécutés et budget voté. Aucune analyse de « toxicité » n'est encore proposée.
