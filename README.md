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

## Fiscalité indirecte : taux d'effort et comptes distribués

**[Comparer TVA/revenu, TVA/consommation et taxes sur les produits](tva-incidence.html)** : deux jeux de données **méthodologiquement distincts**.
- **Enquête Budget de famille 2001** : estimations de TVA par décile issues de Ruiz et Trannoy (2008), tableau 3 (euros par ménage), tableau 4 (TVA en % du revenu disponible brut) et tableau 6 (TVA en % de la consommation). **Ni mesure directe auprès de la DGFiP ni série 2025**.
- **Comptes nationaux distribués 2020–2023** : taxes sur les produits (TVA, TICPE, accises, DMTO, etc.) par vingtième de niveau de vie usuel, Insee CND.101, publication 2026. **Ce n'est pas la TVA seule**. Import reproductible : `python3 scripts/import_cnd_product_taxes.py`.
- Jamais superposer ces données de périodes, périmètres et unités différentes sur un axe commun ; afficher les unités et la provenance à chaque étape.

**Graduations temporelles :** tous les 5 ans sur ordinateur et tous les 10 ans en affichage compact, année finale toujours affichée ; curseur signalé par un repère vertical discret. [Tests des axes](tests/year_axes.test.cjs) : `node --test tests/year_axes.test.cjs`.

**Justice fiscale (cadrage en cours) :** [TVA, incidence et limites des données](TVA_JUSTICE_SOURCES.md). Aucune série de TVA par décile n'est encore présentée comme une observation récente.

Documentation : [sources](DATA_SOURCES.md), [méthodologie](METHODOLOGY.md), [passation et roadmap](ROADMAP.md).

**Site public : https://budget-fr.kiwinokoto.fr** (première publication vérifiée le 16 octobre 2026). Déploiement statique isolé sur le VPS personnel, derrière Traefik et Let's Encrypt. Version applicative effectivement servie après la vue TVA simulée : `51e51f228aa96ec74c678f70d7a8ac98b79d6e73` (incluant https://budget-fr.kiwinokoto.fr/recettes.html et https://budget-fr.kiwinokoto.fr/fonctions.html). Les changements de documentation ultérieurs sur `main` ne sont pas déployés automatiquement ; voir [la procédure d'exploitation](deploy/README.md).

Ce dépôt public ne contient aucune donnée personnelle ni confidentielle. Les données originales de l'Insee restent sous leurs propres conditions de réutilisation. Les séries peuvent être révisées.

**Ne pas confondre** finances publiques consolidées et budget de l'État seul, déficit et dette, chiffres exécutés et budget voté. Aucune analyse de « toxicité » n'est encore proposée.
