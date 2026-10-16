# budget_fr

Atlas historique et critique des finances publiques françaises — **prototype open source expérimental**.

## Premier démonstrateur

Courbes interactives des recettes, dépenses et du solde **des administrations publiques consolidées**, 1995–2025, en % du PIB. Données Insee, tableau publié en 2026, pas de données inventées pour 1980–1994.

Lancement local, sans dépendances :

```bash
python3 -m http.server 8000
# ouvrir http://localhost:8000
```

Tests :

```bash
python3 -m unittest discover -s tests -v
```

Documentation : [sources](DATA_SOURCES.md), [méthode](METHODOLOGY.md), [roadmap et passation](ROADMAP.md).

**Ne pas confondre** finances publiques consolidées et budget de l'État, solde et dette, données prévisionnelles et données exécutées, comptabilité observée et jugement d'efficacité.

**Objectif** : couvrir 1980–2025 après validation de la série officielle complète ; étendre à 1960 si la comparabilité le permet. L'analyse de la justice fiscale, de la traçabilité et du patrimoine viendra ensuite, avec définitions testables.

Aucun déploiement public réalisé. Ce dépôt ne redistribue pas de fichier source protégé ou à accès restreint.
