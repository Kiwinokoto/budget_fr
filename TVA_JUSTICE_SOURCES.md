# TVA et justice fiscale — note de cadrage scientifique

État : **recherche documentaire**, 16 octobre 2026. Aucun jeu de données distributif importé, aucune série de déciles ni indicateur d'injustice calculé. L'objectif est de ne pas confondre la masse de TVA encaissée avec son incidence sur les ménages.

## Conclusions directement étayées

1. **L'incidence dépend du dénominateur.** La TVA est une taxe sur la consommation. À consommation comparable, elle peut représenter une part relativement stable de la consommation mais une part plus importante du **revenu annuel** des ménages modestes, qui épargnent moins. L'Insee qualifie cet effet immédiat d'antiredistributif. Source : [Blog Insee, « Hausses et baisses de la TVA »](https://blog.insee.fr/hausses-et-baisses-de-la-tva-quels-effets-sur-la-redistribution-et-les-inegalites-de-niveau-de-vie/), publication 2021.
2. **Les effets différés comptent.** [Insee Analyses n°43, 11 février 2019](https://www.insee.fr/fr/statistiques/3713290) simule une hausse de trois points du taux normal. Le choc réduit le niveau de vie corrigé moyen d'environ **0,6 % à trois ans**, les mécanismes d'indexation compensant en moyenne 55 % du choc initial. Le premier décile reste davantage touché. Ceci décrit un **scénario simulé**, et non un effet observé en 2025.
3. **Ne pas masquer la redistribution globale.** [Insee, Redistribution monétaire (édition 2025)](https://www.insee.fr/fr/statistiques/8612544) documente les prélèvements **directs** et les prestations par quintile ; cette source ne permet pas, à elle seule, d'obtenir la TVA par décile.
4. **Piste pertinente pour la distribution élargie :** [Insee, Comptes par catégories de ménage (avril 2026)](https://www.insee.fr/fr/statistiques/8574663), dont CND.101 par vingtième de niveau de vie. Vérifier les variables **effectivement publiées** et leurs définitions avant de supposer qu'elles incluent la TVA payée individuellement.
5. **Modèle de taxation indirecte :** [Insee, étude sur le choc d'inflation de 2023](https://www.insee.fr/fr/statistiques/8242413) décrit l'emploi du modèle Ines et d'un module de taxation indirecte fondé sur l'enquête *Budget de Famille* 2017 actualisée en 2023. Ces données ne constituent pas automatiquement une microbase ouverte exploitable pour notre site.

## Protocole minimal avant toute visualisation par niveau de vie

- Trouver une **table publiée avec valeurs de TVA par groupes**, en indiquant année de référence, population, catégories et unité ; si elle ne peut être trouvée, **ne pas fabriquer de points par décile**.
- Distinguer explicitement **TVA payée / revenu disponible annuel**, **TVA payée / consommation**, **TVA payée / revenu permanent ou approche cycle de vie**.
- Préciser l'unité d'observation (ménage, personne, unité de consommation), la définition des déciles et les ménages exclus.
- Séparer données observées, effets **simulés**, hypothèses d'incidence (transfert aux prix), mesures de fiscalité indirecte et impacts redistributifs nets.
- Vérifier qu'il est méthodologiquement licite de rapprocher un graphique distributif et le montant national de TVA 1995–2025 déjà affiché : dates, enquêtes, champs et classification peuvent différer.
- Tester des analyses alternatives, y compris effets des taux réduits, remboursements, redistribution des prestations et variations temporelles.

## Première livraison analytique retenue

Un panneau comparatif **uniquement avec des chiffres distributifs officiellement publiés et vérifiés**, légendé en termes de simulation / observation, puis une note d'incertitude. Pas de « score global de toxicité », pas d'attribution causale à partir de simples recettes nationales. **Blocage actuel : absence d'un fichier distributif détaillé validé** ; inventaire et extraction restent à faire.

Cette note n'établit aucun résultat quantitatif nouveau : elle distingue les éléments déjà démontrés et les données nécessaires pour poursuivre.
