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

## Distinction confirmée : TVA évaluée en 2001 vs taxes sur les produits 2020–2023

La page [`tva-incidence.html`](tva-incidence.html) documente deux sources chiffrées complémentaires, sans les confondre :
- [Ruiz & Trannoy (2008)](https://www.insee.fr/fr/statistiques/fichier/1376872/es413b.pdf) : enquête **2001**, TVA estimée par décile en euros/ ménage, TVA/revenu disponible brut et TVA/consommation ; la divergence entre les deux dénominateurs est directement testable.
- [Insee CND.101 (2026)](https://www.insee.fr/fr/statistiques/8574663) : statistiques expérimentales pour **2020–2023**, taxes sur les produits par **vingtième de niveau de vie**. Catégorie plus large que la TVA. Aucun taux d'effort de TVA récente n'est calculé.

**Inconnue restante :** une ventilation récente et vérifiée de la seule TVA, rapportée au revenu et à la consommation selon les mêmes groupes, n'a pas encore été trouvée. Éviter la reconstruction par prorata de taxes sur les produits ou de recettes nationales.

## DG Trésor, septembre 2025 : incidence simulée d'une hausse uniforme des taux de TVA

[Trésor-Éco n°371 — « Analyse de la composition des recettes de TVA »](https://www.tresor.economie.gouv.fr/Articles/2025/09/25/analyse-de-la-composition-des-recettes-de-tva), Maxime Gesta, septembre 2025, [PDF complet](https://www.tresor.economie.gouv.fr/Articles/c462ac7f-76db-4c33-9bb3-dcc6886ed898/files/f4d0d1ac-fc61-4cf3-ab3f-094385b218bd), chapitre 4 et graphique 4 (pages 5–6).

- Objet : **TVA seule**, choc contrefactuel **+1 point de pourcentage sur tous les taux**, avec hypothèse de répercussion intégrale aux prix et comportements inchangés. **Ce n'est pas le taux d'effort de la TVA existante**.
- Groupes : **quintiles de ménages** selon le niveau de vie (Q1–Q5), et non déciles ou vingtiles.
- Sources détaillées : Budget de famille **2017**, enquête Revenus fiscaux et sociaux **2022**, comptabilité nationale **2021–2022**, calculs DG Trésor.
- Résultats textuels, **effet moyen de pouvoir d'achat** : Q1 **−0,7 %**, Q5 **−0,4 %**, ensemble **−0,5 %**.
- Part des **recettes supplémentaires issues de la hausse** : Q1 **12 %**, Q5 **31 %**. Ce n'est pas la ventilation du stock de TVA existante.
- La hausse simulée serait en partie compensée, à moyen terme, par les indexations des minima sociaux et du Smic. Ces compensations et les comportements de consommation ne sont pas intégrés au choc statique.
- Le **graphique 4** montre les cinq quintiles ventilés entre taux de TVA, mais **aucune table exacte Q2/Q3/Q4 n'est publiée dans le document**. Le site n'invente donc pas leurs chiffres.
- Le point de TVA **net** de **11,4 Md€ en 2025** est une estimation de rendement statique fondée sur un modèle assis sur le compte semi-définitif **2022**, vieilli. Ce n'est pas une recette effectivement constatée ni une distribution 2025 du prélèvement.
- Les limites des enquêtes déclaratives et des semaines de référence ainsi que les écarts entre incidence économique et taxe collectée sont discutés par l'étude.

**Conclusion sur la recherche :** nous disposons maintenant d'une **simulation distributive publiée en 2025** de la TVA seule. Nous n'avons **toujours pas** trouvé de distribution annuelle 2023–2025 publiée de la **TVA effectivement estimée comme payée**, par revenu *et* consommation, à champs et dénominateurs cohérents. L'enquête BDF 2017 n'est pas une table TVA payée par décile prête à être utilisée sans microsimulation.

## Drees : distribution publiée de la TVA seule dans Ines 2014

[Document de travail Drees n°60 (2016), tableau 16, page 38](https://drees.solidarites-sante.gouv.fr/sites/default/files/2020-10/dt60.pdf) : TVA **isolée**, répartie entre dix déciles de ménages par niveau de vie, chiffres exacts (parts du total TVA **estimé sur le champ**), conservés dans `data/tva_part_deciles_ines_2014.csv` : 4,3 % (D1) à 18,5 % (D10). L'indicateur répond à **« qui contribue à quel montant de TVA ? »**, pas à **« quelle part du revenu supporte la TVA ? »**. Champ métropolitain hors DOM, revenus disponibles positifs ; Ines 2014, consommation BDF 2011 imputée.

Le même travail estime, pour les déciles extrêmes, **11,3 % contre 6,8 % du revenu disponible** et **9,3 % contre 11,5 % de la consommation**. Ces taux ne doivent pas être recalculés depuis le tableau des contributions. Les données ne sont pas actuelles, mais constituent une vérification de méthode intermédiaire entre BDF 2001 et les simulations 2025.

**Accès à une distribution récente TVA seule :** documentation du [module Ines et pseudo-appariement BDF 2017](https://ines-public-e766af.gitlab.io/modules_annexes.html) ; fichiers statistiques BDF 2017 détaillés [CASD](https://www.casd.eu/source/enquete-budget-de-famille/) ou version réduite Quételet-Progedo ; [tableaux publics BDF 2017](https://www.insee.fr/fr/statistiques/4648335) sans TVA par décile publiée. Un accès autorisé aux microdonnées et une microsimulation validée, ou une demande de tableaux agrégés à la Drees, est nécessaire pour une estimation plus récente. Ne pas utiliser un simple coefficient TVA uniforme sur les dépenses COICOP comme valeur observée.
