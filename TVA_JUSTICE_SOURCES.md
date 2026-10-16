# TVA et justice fiscale — note de cadrage scientifique

État : **recherche documentaire**, 16 octobre 2026. Aucun jeu de données distributif importé, aucune série de déciles ni indicateur d'injustice calculé. L'objectif est de ne pas confondre la masse de TVA encaissée avec son incidence sur les ménages.

## Conclusions directement étayées

1. **L'incidence dépend du dénominateur.** La TVA est une taxe sur la consommation. À consommation comparable, elle peut représenter une part relativement stable de la consommation mais une part plus importante du **revenu annuel** des ménages modestes, qui épargnent moins. L'Insee qualifie cet effet immédiat d'antiredistributif. Source : [Blog Insee, « Hausses et baisses de la TVA »](https://blog.insee.fr/hausses-et-baisses-de-la-tva-quels-effets-sur-la-redistribution-et-les-inegalites-de-niveau-de-vie/), publication 2021.
2. **Répartition des montants ≠ effort relatif.** Le [blog Insee du 27 janvier 2021](https://blog.insee.fr/hausses-et-baisses-de-la-tva-quels-effets-sur-la-redistribution-et-les-inegalites-de-niveau-de-vie/) indique que les **20 % des ménages les plus aisés s'acquittent de 32 % du total de TVA**, contre **12 % pour les 20 % les plus modestes**. Ces chiffres, cités dans l'article de 2021, décrivent une répartition du **montant total**, sans permettre de déduire la fraction du revenu consommée par chaque groupe. Ils ne sont **ni des valeurs de 2025 ni une série temporelle**. La publication ajoute que réduire la TVA ne profite pas uniquement aux ménages modestes.
3. **Les effets différés comptent.** [Insee Analyses n°43, 11 février 2019](https://www.insee.fr/fr/statistiques/3713290) simule une hausse de trois points du taux normal. Le choc réduit le niveau de vie corrigé moyen d'environ **0,6 % à trois ans**, les mécanismes d'indexation compensant en moyenne 55 % du choc initial. Le premier décile reste davantage touché. Ceci décrit un **scénario simulé**, et non un effet observé en 2025.
4. **Ne pas masquer la redistribution globale.** [Insee, Redistribution monétaire (édition 2025)](https://www.insee.fr/fr/statistiques/8612544) documente les prélèvements **directs** et les prestations par quintile ; cette source ne permet pas, à elle seule, d'obtenir la TVA par décile.
5. **Piste pertinente pour la distribution élargie :** [Insee, Comptes par catégories de ménage (avril 2026)](https://www.insee.fr/fr/statistiques/8574663), dont CND.101 par vingtième de niveau de vie. Vérifier les variables **effectivement publiées** et leurs définitions avant de supposer qu'elles incluent la TVA payée individuellement.
6. **Modèle de taxation indirecte :** [Insee, étude sur le choc d'inflation de 2023](https://www.insee.fr/fr/statistiques/8242413) décrit l'emploi du modèle Ines et d'un module de taxation indirecte fondé sur l'enquête *Budget de Famille* 2017 actualisée en 2023. Ces données ne constituent pas automatiquement une microbase ouverte exploitable pour notre site.

## Protocole minimal avant toute visualisation par niveau de vie

- Trouver une **table publiée avec valeurs de TVA par groupes**, en indiquant année de référence, population, catégories et unité ; si elle ne peut être trouvée, **ne pas fabriquer de points par décile**.
- Distinguer explicitement **TVA payée / revenu disponible annuel**, **TVA payée / consommation**, **TVA payée / revenu permanent ou approche cycle de vie**.
- Préciser l'unité d'observation (ménage, personne, unité de consommation), la définition des déciles et les ménages exclus.
- Séparer données observées, effets **simulés**, hypothèses d'incidence (transfert aux prix), mesures de fiscalité indirecte et impacts redistributifs nets.
- Vérifier qu'il est méthodologiquement licite de rapprocher un graphique distributif et le montant national de TVA 1995–2025 déjà affiché : dates, enquêtes, champs et classification peuvent différer.
- Tester des analyses alternatives, y compris effets des taux réduits, remboursements, redistribution des prestations et variations temporelles.

## Premier tableau distributif réellement validé : une simulation, pas une observation

Le [tableau 2 d'Insee Analyses n°43 (2019)](https://www.insee.fr/fr/statistiques/3713290) publie les contributions aux effets d'une hausse de TVA de trois points, **pour les dix déciles**. Notre fichier `data/tva_choc_deciles_insee_2019.csv` en retranscrit les valeurs, et la page `tva-justice.html` les présente sans les faire passer pour une mesure récente d'incidence.

- **D1 :** prélèvements indirects −2,8 points, effet total −1,4 % de niveau de vie corrigé.
- **D10 :** prélèvements indirects −1,0 point, effet total −0,5 %.
- L'étude porte sur une population et une législation de **2016**, publiée en **2019**. Le scénario est **contrefactuel** et les chiffres ne décrivent pas la TVA payée en 2025.

La première vue distributive est donc disponible, mais la recherche d'une série empirique et actuelle sur la **TVA payée par groupe de revenu ou de consommation** reste ouverte.

## Première livraison analytique retenue

Un panneau comparatif **uniquement avec des chiffres distributifs officiellement publiés et vérifiés**, légendé en termes de simulation / observation, puis une note d'incertitude. Pas de « score global de toxicité », pas d'attribution causale à partir de simples recettes nationales. **Blocage actuel pour une véritable incidence observée : absence de fichier récent de TVA acquittée par décile authentifié.** La simulation Insee 2019 est désormais retranscrite et testée.

Cette note n'établit aucun résultat quantitatif nouveau : elle distingue les éléments déjà démontrés et les données nécessaires pour poursuivre.
