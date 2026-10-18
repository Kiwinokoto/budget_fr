# Déploiement statique — VPS personnel

**Cible :** https://budget-fr.kiwinokoto.fr — Traefik existant, réseau Docker externe `traefik_network`.
Le site est entièrement statique, sans backend, base de données, compte utilisateur ni secret applicatif.

## Prérequis et précautions

- Vérifier sur GitHub le `main` approuvé et ses tests : **ne pas déployer une branche de travail**.
- Vérifier les verrous AgentCtl `deploy:vps-personal/budget-fr` et `host:vps-personal/docker` ; acquérir ces ressources avant toute opération. Aucun service tiers ne doit être modifié.
- La zone DNS `budget-fr.kiwinokoto.fr` doit pointer vers le VPS personnel, et Traefik doit être disponible sur 80/443.
- Le serveur possède déjà l'image Nginx identifiée par le digest épinglé dans `compose.yml` (à recontrôler en cas de migration).
- Ne pas injecter de tokens GitHub : ce dépôt est public.

## Organisation sur le VPS

- `/opt/budget-fr/compose.yml` : copie versionnée de ce fichier.
- `/opt/budget-fr/site/` : uniquement `index.html`, `interets.html`, `solde-primaire.html, dette.html`, `fonctions.html`, `recettes.html`, `tva-justice.html`, `tva-incidence.html`, `data/*.csv` (dont intérêts S13 et solde primaire 1959–2025, ainsi que TVA Ines 2014), `DATA_SOURCES.md`, `METHODOLOGY.md`, `TVA_JUSTICE_SOURCES.md`. Pas de scripts, fichiers .env, clés ou répertoires .git dans le document root.
- `/opt/budget-fr/.deployed_commit` : SHA exact publié après validation.
- `/opt/budget-fr/backup/` : copie locale du site et du Compose précédents lors d'une mise à jour (si présents).

Préparer les fichiers de site depuis un clone GitHub **en lecture seule**, figé sur un commit de `main`. Ne jamais utiliser un worktree de développement partagé pour servir le public.

Avant activation : comparer le SHA du checkout avec le SHA approuvé, contrôler le CSV macroéconomique (1960–2025) et CSV COFOG (1995–2024) et prélèvements (1995–2025) ainsi que les dix déciles de la simulation TVA 2019, données TVA BDF 2001 et taxes sur les produits CND 2020–2023, lancer les tests Python. Puis vérifier `docker compose -f /opt/budget-fr/compose.yml config -q`.

Activer uniquement le nouveau service : `docker compose -f /opt/budget-fr/compose.yml up -d web`.

## Vérification

1. `docker inspect budget-fr-web` : conteneur démarré, volume de site en lecture seule, réseau `traefik_network`.
2. `curl -fsS https://budget-fr.kiwinokoto.fr/` : réponse HTML valide, sans `-k` (certificat vérifié).
3. `curl -fsS https://budget-fr.kiwinokoto.fr/data/apu_1960_2025_pct_pib.csv` : en-tête CSV et 66 années ; `/data/cofog_1995_2024_bn_eur.csv` : en-tête et 30 années, sommes contrôlées.
4. `curl -I https://budget-fr.kiwinokoto.fr/fonctions.html` et `/interets.html`, `/data/interets_apu_1959_2025_bn_eur.csv`, `/recettes.html`, `/tva-justice.html`, `/tva-incidence.html`, `/data/tva_choc_deciles_insee_2019.csv`, `/data/tva_effort_bdf_2001.csv`, `/data/taxes_produits_cnd_2020_2023.csv`, `/METHODOLOGY.md` et liens de source : pas de 404.
5. Si possible, contrôler réellement l'interface sur navigateur desktop/mobile.

Ne marquer le déploiement réussi qu'après ces contrôles. Si ACME/HTTPS n'est pas encore prêt, diagnostiquer DNS/Traefik sans modifier les certificats ou configurations d'autres services.

## Retour arrière

Lors d'une mise à jour, conserver l'ancienne version avant remplacement. Si les vérifications échouent, restaurer le dossier de site et l'ancien Compose, puis recréer **uniquement** `budget-fr-web`. Pour une première installation non fonctionnelle, arrêter uniquement ce conteneur, en conservant les fichiers pour analyse. Ne pas lancer `docker compose down` sur un autre projet ; ne pas modifier Traefik, ses volumes ou ses certificats globaux.

Le contenu est publié par une opération maîtrisée ; aucune GitHub Action ni redéploiement automatique n'est installé dans cette version.

## Lot interface UX 2026-10-17

Inclure atlas-nav.css à la racine de /opt/budget-fr/site lors du prochain déploiement : le bandeau partagé des huit pages HTML requiert cette feuille locale (sans CDN). Conserver la sauvegarde précédente et vérifier HTTP 200 et identité octet pour le CSS, en plus des données. Cette branche UI ne se déploie pas automatiquement.

## Futur chapitre aides aux entreprises

Pour un déploiement ultérieur validé, ajouter aides-entreprises.html, AIDES_ENTREPRISES_SOURCES.md et data/aides_entreprises_senat_2023_estimations.csv au site statique, ainsi que la navigation commune inchangée atlas-nav.css. Vérifier HTTPS, les huit pages précédentes et leurs CSV. Aucun déploiement automatique depuis cette PR.

## Nouveau chapitre APPRENTISSAGE (PR dépendante du chapitre aides)

Un prochain déploiement explicitement autorisé doit inclure apprentissage.html, APPRENTISSAGE_SOURCES.md, les deux CSV data/apprentissage_*.csv, la navigation à dix pages et les fichiers déjà publiés. Vérifier le site, les CSV et une sauvegarde rollback. La PR apprentissage dépend de la PR aides #30 : fusionner dans cet ordre.

## Release du graphique historique APPRENTISSAGE

Si publication explicitement autorisée, inclure le nouveau script racine apprentissage-histoire.js et le CSV data/apprentissage_sifa_effectifs_1982_2024.csv (44 lignes CSV dont en-tête), en plus du HTML actuel. Vérifier HTTP 200, identité des fichiers, les deux modes et le tableau des 43 années dans Chromium, sur mobile et desktop. Préparer un rollback atomique ; ne jamais publier l'HTML historique seul.

## Sous-page APPRENTISSAGE CONTEXTE, 2026-10-17

Une fois la PR fusionnée et la publication autorisée, ajouter apprentissage-contexte.html, jeunes-contexte.js, JEUNES_CONTEXTE_SOURCES.md et les deux CSV data/jeunes_*.csv à la livraison figée sur main. Vérifier les ressources HTTPS, interactivité du diagramme, ses six combinaisons âge/sexe, le tableau, l'absence de double compte et absence de débordement mobile ; sauvegarde puis rollback si échec. L'onglet principal APPRENTISSAGE reste le point d'entrée depuis la navigation générale.

## Lot longitudinal jeunesse — publiée le 17 octobre 2026

Inclure la version mise à jour de apprentissage-contexte.html et les trois ressources **jeunes-histoire.js**, **data/jeunes_scolarisation_1986_2023_insee.csv**, **data/jeunes_cumul_emploi_etudes_2003_2023_insee.csv** ensemble. Vérifier les originaux XLSX (SHA-256 dans JEUNES_CONTEXTE_SOURCES.md), tests, HTML/CSS/JS/CSV en HTTPS octet par octet, sélecteurs d'âge en Chromium desktop/mobile, tableaux accessibles, débordement horizontal et absence d'erreurs JS. Publier avec sauvegarde atomique et rollback ; ne pas modifier les autres services.

Release vérifiée : d8d4e7665fe5bf89b3bf4d80453e9cf57959e202 ; sauvegarde : /opt/budget-fr/backup/20261017T101809Z-before-209c5e7d0394-to-d8d4e7665fe5. Tests : 55 Python, 54 Node, 139 contrôles Chromium ; 21 CSV et ressources identiques à GitHub. Rollback conservé et déploiement manuel uniquement.

## Nouveau chapitre apprentissage : résultats (publié le 17 octobre 2026)

Inclure ensemble apprentissage-resultats.html, APPRENTISSAGE_RESULTATS_SOURCES.md et data/apprentissage_parcours_2024_inserjeunes.csv, ainsi que les deux liens entrants des pages apprentissage.html et apprentissage-contexte.html. Vérifier quatre taux, tableaux, sources, navigation, affichages 390/768/1365 px, HTTPS et identité des fichiers au commit main autorisé. Le déploiement n'est pas automatique ; sauvegarde, rollback, verrou deploy:vps-personal/budget-fr et host:vps-personal/docker obligatoires.

Release contrôlée 8aead975b776f3d5ed2f6e2215e749ef03edca3b ; sauvegarde /opt/budget-fr/backup/20261017T110640Z-before-d8d4e7665fe5-to-8aead975b776 (ancienne version d8d4e7665fe5bf89b3bf4d80453e9cf57959e202). Tests 58 Python, 56 Node, 22 CSV, vérification HTTPS octet par octet et 36 contrôles Chromium spécifiques en mobile/tablette/desktop, plus régressions. Rollback conservé. Aucun autre service affecté. Déploiements suivants manuels uniquement.

## Chapitres supplémentaires non encore déployés

Après fusion des PR #43 et suivantes, toute livraison demandée doit inclure `data/cofog_subfunctions_1995_2024.json` pour `fonctions.html`, ainsi que `etat.html` et `data/etat_execution_2023_2025.json` pour la navigation budgétaire. Sur le serveur statique, vérifier HTTP 200 et chargement navigateur effectif des JSON ; ne pas publier seulement les HTML. Conserver les sources/méthodologies accessibles et contrôler le SHA du `main` applicatif avant déploiement.


- Nouvelle série : déployer aussi `data/etat_solde_net_2013_2025.json` avec `etat.html`. Contrôler HTTP 200 et rendu des 13 années en navigateur. Les sources CSV officielles ne doivent pas être exposées par défaut dans la racine web.
