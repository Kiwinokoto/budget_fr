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

Documentation : [sources](DATA_SOURCES.md), [méthodologie](METHODOLOGY.md), [passation et roadmap](ROADMAP.md).

Ce dépôt public ne contient aucune donnée personnelle ni confidentielle. Aucun déploiement public n'a été effectué. Les données originales de l'Insee restent sous leurs propres conditions de réutilisation. Les séries peuvent être révisées.

**Ne pas confondre** finances publiques consolidées et budget de l'État seul, déficit et dette, chiffres exécutés et budget voté. Aucune analyse de « toxicité » n'est encore proposée.
