# Contrôle des écarts de dette — Insee 3.102–3.105 et Eurostat EDP

Date de l'audit : **16 octobre 2026**. Relevé **documentaire et numérique** ; aucun chiffre des CSV publiés n'a été modifié.

## Source, millésime et signification

Les fichiers Insee [3.102–3.105](https://www.insee.fr/fr/statistiques/8988843) ont été téléchargés et contrôlés sur le millésime de comptes nationaux **base 2020, 28 août 2026**.

Eurostat a été interrogé via l'API officielle (France, 2024 et 2025) :
- [EDP — `gov_10dd_edpt1`](https://ec.europa.eu/eurostat/databrowser/view/gov_10dd_edpt1/default/table), JSON : `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/gov_10dd_edpt1?geo=FR&sinceTimePeriod=2024` ; mise à jour indiquée **22 avril 2026** ; SHA-256 du JSON observé : `a60dc52c082f9d1b4dbcb251035b25f1fa45841ca33e86ad3ac2075c13feddeb`.
- [Dette structurelle — `gov_10dd_ggd`](https://ec.europa.eu/eurostat/databrowser/view/gov_10dd_ggd/default/table), JSON : `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/gov_10dd_ggd?geo=FR&sinceTimePeriod=2024` ; mise à jour indiquée **5 juin 2026** ; SHA-256 du JSON observé : `155debc3f1cb550bf670c2688f9c3aff5488b2fa1167f204f81ad5621025fb0d`.
- La dette EDP est déclarée en **millions d'euros** dans les cellules `unit=MIO_EUR`, convertis ci-dessous en **milliards d'euros** en divisant par 1000. Périmètre `geo=FR`, `freq=A`, `na_item=GD`, `sector=S13`, pour `gov_10dd_ggd` aussi `sector2=S1_S2`, `maturity=TOTAL`.

**Attention** : les datasets Eurostat consultés **précèdent** la publication Insee d'août. Ce ne sont pas une vérification indépendante de la dernière révision nationale. En particulier, ne pas traiter les `sector=S1311` Eurostat comme des contributions additionnables directement à S13 Insee : périmètres et niveau de consolidation à valider.

## Tableau de réconciliation — données de fin 2025

| Publication | Dette brute S13 (Md€) | Sécurité sociale S1314 (Md€) | Commentaire |
|---|---:|---:|---|
| Insee, notification de mars 2026 / bulletin T4 2025 | 3 460,5 | 293,1 | Version ancienne, publiée avant l'été |
| Eurostat EDP, API actualisée avril 2026 | 3 460,4651 | 293,0774 | Valeurs **en million EUR** divisées par 1000 ; ventilation Eurostat par secteur, pas nécessairement la contribution consolidée Insee |
| Eurostat `gov_10dd_ggd`, juin 2026 | 3 460,4651 | À ne pas comparer ici | `GD`, `sector=S13`, `sector2=S1_S2`, maturité totale |
| Insee 3.102, août 2026 | 3 460,1 | 292,6 | Contribution sociale au total consolidé |
| Insee 3.104, août 2026 | 3 460,1 | **293,1** | Total S13 actualisé ; la contribution S1314 paraît issue de l'ancien chiffre |
| Insee, publication trimestrielle T2 2026 (septembre 2026), historique T4 2025 | 3 460,1 | 292,6 (contribution consolidée) | Confirme la dette totale historique révisée et la contribution consolidée de S1314 |

Sources : [Insee, T4 2025, mars](https://www.insee.fr/fr/statistiques/8955019) ; [annexe de notification Insee, mars 2026](https://www.insee.fr/fr/statistiques/documentation/annexe_ir_prov_apu--20260326.pdf) ; [Insee, T2 2026, septembre](https://www.insee.fr/fr/statistiques/9053525) ; API Eurostat ci-dessus.

**Conclusion étayée** : le tableau 3.104 semble avoir repris au moins une valeur du millésime précédent. Les deux chiffres anciens S13 et S1314 sont corroborés par Insee mars et Eurostat avril. **La cause technique exacte de l'anomalie 3.104 n'est pas démontrée** ; ne pas écraser la valeur officielle d'août. Vérification auprès de l'Insee nécessaire. Les six contributions 2025 du 3.104 comprennent un sous-total central ; additionner seulement État, ODAC, locales et sécurité sociale donne environ 3 460,5 Md€, et non le total S13 officiel actualisé 3 460,1 Md€.

## Autres écarts non élucidés

- **Insee 3.104, 2014–2021** : le poste total d'ajustement de valorisation ne correspond pas à la somme de ses trois sous-lignes affichées. Écart absolu maximal observé : **2,9 Md€** (S1311 en 2021). Le CSV contient un résidu calculé et identifié `valuation_breakdown_gap_bn_eur`. Aucune interprétation économique de ce résidu n'est établie.
- **Insee 3.105 et 3.104, 2014** : la variation de dette publiée par 3.105 dépasse de **0,6 Md€** la différence des stocks de 3.104 ; les autres différences annuelles 2009–2025 restent dans environ ±0,3 Md€ dans ce millésime. Les deux séries originales sont conservées.
- Les notes de définitions de Maastricht et les notifications EDP ne fournissent **pas** de justification cellulaire vérifiable pour ces deux écarts historiques. Ne pas conclure à une erreur de l'Insee sans réponse ou correctif officiel.

## Tests d'interface réalisés

- Chromium via Puppeteer : largeurs **390, 768 et 1365 px**, années 1995/2014/2020/2021/2025, administration centrale, S13, S1314 ; changements de secteurs, curseur au clavier, graphiques, unités, avertissements, absence de débordement horizontal et de JavaScript exception.
- Chargement défaillant d'un CSV simulé : page fermée à l'affichage de chiffres, bouton « Réessayer » puis récupération vérifiée.
- **23 contrôles de bout en bout**, en complément de la suite Python/Node. Les captures mobile et desktop ont été inspectées ; cela ne remplace pas une revue humaine complète d'accessibilité (lecteur d'écran réel, contrastes instrumentés).

## Décision

La page `dette.html` affiche chaque source avec son propre périmètre et signale les discordances. **Aucune fusion des données Eurostat avec les CSV Insee**, aucune extrapolation, aucune correction silencieuse. Le site public et l'étude historique pré-1960 restent hors périmètre de cette étape.
