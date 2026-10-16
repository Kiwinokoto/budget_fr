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
- `/opt/budget-fr/site/` : uniquement `index.html`, `fonctions.html`, `recettes.html`, `tva-justice.html`, `data/*.csv`, `DATA_SOURCES.md`, `METHODOLOGY.md`, `TVA_JUSTICE_SOURCES.md`. Pas de scripts, fichiers .env, clés ou répertoires .git dans le document root.
- `/opt/budget-fr/.deployed_commit` : SHA exact publié après validation.
- `/opt/budget-fr/backup/` : copie locale du site et du Compose précédents lors d'une mise à jour (si présents).

Préparer les fichiers de site depuis un clone GitHub **en lecture seule**, figé sur un commit de `main`. Ne jamais utiliser un worktree de développement partagé pour servir le public.

Avant activation : comparer le SHA du checkout avec le SHA approuvé, contrôler le CSV macroéconomique (1960–2025) et CSV COFOG (1995–2024) et prélèvements (1995–2025) ainsi que les dix déciles de la simulation TVA 2019, lancer les tests Python. Puis vérifier `docker compose -f /opt/budget-fr/compose.yml config -q`.

Activer uniquement le nouveau service : `docker compose -f /opt/budget-fr/compose.yml up -d web`.

## Vérification

1. `docker inspect budget-fr-web` : conteneur démarré, volume de site en lecture seule, réseau `traefik_network`.
2. `curl -fsS https://budget-fr.kiwinokoto.fr/` : réponse HTML valide, sans `-k` (certificat vérifié).
3. `curl -fsS https://budget-fr.kiwinokoto.fr/data/apu_1960_2025_pct_pib.csv` : en-tête CSV et 66 années ; `/data/cofog_1995_2024_bn_eur.csv` : en-tête et 30 années, sommes contrôlées.
4. `curl -I https://budget-fr.kiwinokoto.fr/fonctions.html` et `/recettes.html`, `/tva-justice.html`, `/data/tva_choc_deciles_insee_2019.csv`, `/METHODOLOGY.md` et liens de source : pas de 404.
5. Si possible, contrôler réellement l'interface sur navigateur desktop/mobile.

Ne marquer le déploiement réussi qu'après ces contrôles. Si ACME/HTTPS n'est pas encore prêt, diagnostiquer DNS/Traefik sans modifier les certificats ou configurations d'autres services.

## Retour arrière

Lors d'une mise à jour, conserver l'ancienne version avant remplacement. Si les vérifications échouent, restaurer le dossier de site et l'ancien Compose, puis recréer **uniquement** `budget-fr-web`. Pour une première installation non fonctionnelle, arrêter uniquement ce conteneur, en conservant les fichiers pour analyse. Ne pas lancer `docker compose down` sur un autre projet ; ne pas modifier Traefik, ses volumes ou ses certificats globaux.

Le contenu est publié par une opération maîtrisée ; aucune GitHub Action ni redéploiement automatique n'est installé dans cette version.
