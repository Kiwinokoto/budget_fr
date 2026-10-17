# Aides publiques aux entreprises — provenance et périmètres

**Statut au 17 octobre 2026 : étude méthodologique sur des estimations ponctuelles, pas une série annuelle harmonisée.** Le chapitre ne fournit ni inventaire exhaustif de bénéficiaires, ni note politique de « toxicité ».

## Sources réellement examinées

1. **Sénat**, rapport n° 808 (2024–2025), tome I, commission d'enquête sur les aides publiques aux grandes entreprises et à leurs sous-traitants, adopté le 1er juillet 2025 : https://www.senat.fr/rap/r24-808-1/r24-808-1_mono.html . Pour **2023**, la commission estime **211 milliards d'euros au sens large** et **108 milliards au sens strict**, en précisant que ces chiffres sont des **ordres de grandeur/planchers**, compte tenu des informations manquantes et risques de doubles comptes.
2. **Inspection générale des finances**, Revue de dépenses – Les aides aux entreprises, publiée le 4 septembre 2024 : https://www.igf.gouv.fr/rapports-de-mission/revue-de-depenses-les-aides-aux-entreprises . Pour **2022**, 64 Md€ d'aides budgétaires et fiscales de l'État recensées (28 Md€ + 36 Md€), excluant de ce total les exonérations sociales, aides de collectivités et aides de l'UE.
3. **France Stratégie**, Les politiques industrielles en France. Évolutions et comparaisons internationales, novembre 2020 : https://www.strategie-plan.gouv.fr/publications/politiques-industrielles-france-evolutions-comparaisons-internationales . Pour **2019**, quatre périmètres, estimation comprise entre **139 et 223 Md€** selon le Sénat (rapport 808, partie III).

## Définitions et précautions

Le sens **large** inclut notamment des subventions budgétaires, allègements de cotisations, avantages fiscaux, dépenses fiscales « déclassées » et interventions Bpifrance (y compris prêts et garanties). Certaines **ne sont pas des transferts définitifs en espèces**.

Le sens **strict** exclut les interventions financières de Bpifrance, les dépenses fiscales déclassées et les dépenses fiscales liées à la TVA. Pour la TVA, le bénéficiaire économique peut être l'entreprise ou le consommateur selon la transmission du taux réduit aux prix.

**108 et 211 ne s'ajoutent pas.** La différence arithmétique (103 Md€) n'est pas une catégorie d'aide officielle ni une mesure des sommes prétendument « sans contrepartie ».

Le total large porte sur les **entreprises de toutes tailles**, non exclusivement sur les grandes entreprises. Le Sénat explique précisément la difficulté d'établir la fraction reçue par les grands groupes et leurs sous-traitants.

Les transferts financiers entre État, opérateurs et bénéficiaires peuvent induire un **double compte** dans les subventions. Le tableau COFOG de l'Insee classe les dépenses par **fonction**, et non par bénéficiaire ; il ne restitue pas directement un impôt non perçu, une exonération sociale ou un prêt. La table pédagogique de la nouvelle page n'est **pas une ventilation comptable officielle** des 211 Md€.

**Absence de suivi central exhaustif ne signifie pas absence de conditionnalité ou de contrôle pour tous les dispositifs.** Il faut vérifier les règles, contrats, évaluations et sanctions de chaque aide.

## Fichiers et conservation des observations

- data/aides_entreprises_senat_2023_estimations.csv : **deux estimations ponctuelles**, avec année, périmètre, montant, nature et source; ce n'est ni une série, ni un total de dépenses Insee.
- aides-entreprises.html : première page explicative, choix du périmètre, échelle commune, mécanismes, limites du rapprochement à COFOG. Aucun montant par famille n'est inventé.

## Étapes proposées

1. Construire un **catalogue des dispositifs** : année, administration/opérateur, mécanisme, bénéficiaire, montant réalisé vs accordé, flux/stock/garantie, source, norme et régime de TVA, conditions, évaluation, risque de double compte.
2. Choisir **trois dispositifs pilotes** : allègements généraux de cotisations, crédit d'impôt recherche (CIR), aides à l'apprentissage. Pour chacun, retrouver une série réellement comparable et les règles de suivi.
3. Reconstituer des séries annuelles **uniquement lorsque le périmètre, les unités et les reclassements sont homogènes**, de 1995 à aujourd'hui si possible, ou plus court.
4. Ajouter des données de bénéficiaires par taille/secteur seulement si publiquement accessibles et fondées sur une source officielle ; ne pas attribuer une aide à un groupe par inférence.
5. Distinguer aides allouées, versées, remboursables, avantages fiscaux, évaluations d'efficacité, contreparties et contrôle effectif.

Le pré-1960 et un indicateur normatif « toxicité » restent hors périmètre tant qu'une méthode explicite et des données adaptées n'existent pas.
