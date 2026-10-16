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

Documentation : [sources](DATA_SOURCES.md), [méthodologie](METHODOLOGY.md), [passation et roadmap](ROADMAP.md).

**Site public : https://budget-fr.kiwinokoto.fr** (première publication vérifiée le 16 octobre 2026). Déploiement statique isolé sur le VPS personnel, derrière Traefik et Let's Encrypt. Version effectivement servie à cette date : `0504e5c70314939cb2d0f0537a953a6fc81b1c71`. Les changements de documentation ultérieurs sur `main` ne sont pas déployés automatiquement ; voir [la procédure d'exploitation](deploy/README.md).

Ce dépôt public ne contient aucune donnée personnelle ni confidentielle. Les données originales de l'Insee restent sous leurs propres conditions de réutilisation. Les séries peuvent être révisées.

**Ne pas confondre** finances publiques consolidées et budget de l'État seul, déficit et dette, chiffres exécutés et budget voté. Aucune analyse de « toxicité » n'est encore proposée.
