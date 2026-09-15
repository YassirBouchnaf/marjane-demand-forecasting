# Journal des décisions, Prévision de la demande (Stage Marjane Taza)

Chaque décision prise conjointement est enregistrée ici avec sa justification, pour garder une trace claire et pouvoir l'expliquer en soutenance.

---

**Décision** : Choix du rayon 40 (Ménage, département Bazar) comme rayon prioritaire pour la preuve de concept
**Pourquoi** : Volume de ventes le plus élevé (417 759 unités sur l'année), variabilité journalière la plus faible parmi les rayons à fort volume (coefficient de variation 0,30), taux de rupture de stock bas (3,5%). Ces trois critères en font le candidat avec le signal le plus propre pour un premier modèle de prévision.

---

**Décision** : Horizon de prévision hebdomadaire plutôt que journalier
**Pourquoi** : Avec seulement un an de données disponibles (2025), une prévision journalière serait trop bruitée pour donner des résultats fiables. L'hebdomadaire est plus robuste et reste suffisant pour la plupart des décisions de réapprovisionnement.

---

**Décision** : Le rayon 51 (Électro Ménager, département Équip Maison) est envisagé comme extension si le temps du stage le permet
**Pourquoi** : CA le plus élevé de tous les rayons, donc enjeu business fort, mais taux de rupture de stock élevé (10,2%) qui complique l'exploitation de l'historique de vente. Bon candidat pour montrer une maîtrise plus avancée une fois le rayon 40 traité.

---

**Décision** : L'étape de cadrage métier (choix final du rayon et de l'horizon) doit être validée avec le maître de stage avant de commencer le développement
**Pourquoi** : Les critères statistiques (volume, variabilité, ruptures) ne suffisent pas seuls, le rayon prioritaire pour l'analyse doit aussi correspondre à une priorité business réelle de Marjane, connue seulement par les équipes terrain.

---

**Décision** : Sélection des 3 familles à l'intérieur du rayon 40 : 10 (Art/cuis prépar), 11 (Art de table), 12 (Art ménag/rangement)
**Pourquoi** : Ce sont les trois familles avec le plus grand nombre d'articles réels (700 à 1200 références chacune) et un chiffre d'affaires significatif dans le rayon 40. La famille 15 (Sacs vendables caisse), malgré son gros volume, a été volontairement exclue : seulement 7 articles, produit homogène de caisse, non représentatif d'un vrai enjeu de prévision de la demande.

---

**Décision** : Travailler au niveau "famille" plutôt qu'au niveau "article individuel" pour la prévision
**Pourquoi** : Compromis assumé entre précision statistique et granularité opérationnelle (effet d'agrégation / top-down vs bottom-up en prévision de la demande). Prévoir au niveau famille est plus stable et plus facile à bien faire avec un an de données, mais moins directement actionnable pour un réassort article par article. Ce compromis doit être explicité clairement dans la restitution finale, pas présenté comme "la solution la plus simple".

---

**Décision** : Conserver les 76 lignes à quantité vendue négative (0,2% des données du rayon 40, familles 10/11/12) dans le tableau consolidé, plutôt que de les supprimer
**Pourquoi** : Quantité et montant négatifs sont systématiquement alignés ligne par ligne, cohérent avec l'hypothèse d'un retour client, mais cette hypothèse reste plausible et non confirmée formellement (l'état "actif" de l'article ne constitue pas une preuve, car il concerne aussi la grande majorité des ventes normales). Impact négligeable sur le volume total, donc pas d'investigation plus poussée jugée nécessaire vu le temps disponible.

---

**Décision** : Retenir Ramadan (début le 2 mars 2025), Aïd Al-Adha (début juin 2025) et l'anniversaire du magasin Marjane Taza (mi-novembre) comme 3 périodes spéciales à intégrer au feature engineering (étape 4)
**Pourquoi** : L'exploration SQL (ventes par semaine sur l'année) a révélé deux pics nets (semaine 08 : 4380 unités, semaine 46 : 3485 unités, contre une moyenne de 1500-1800), et un pic journalier confirmé début juin (jusqu'à 360 unités le 6 juin, contre 120-160 habituellement). Le responsable du département (information de terrain, non déductible des données seules) a confirmé 3 périodes de hausse récurrentes : avant Ramadan (Chaabane), Aïd Al-Adha, et l'anniversaire du magasin Marjane Taza le 16 novembre, cette dernière corrige une hypothèse initiale erronée qui attribuait le pic de la semaine 46 à la Fête de l'Indépendance (18 novembre), simple coïncidence de calendrier cette année-là. Point notable pour Aïd Al-Adha 2025 : le sacrifice rituel du mouton a été suspendu par décision royale (sécheresse), donc le pic observé cette année (achats de vaisselle/cuisine pour le repas de fête) pourrait être plus faible qu'une année normale avec sacrifice, à garder en tête si le modèle est réutilisé une année sans suspension.

---

**Décision** : Conserver la famille 10 (Art/cuis prépar) dans le périmètre malgré sa demande intermittente, en signalant explicitement cette limite dans la restitution finale
**Pourquoi** : La comparaison des 3 familles a montré que la famille 10 a une moyenne vendue par ligne nettement plus basse (1,55, contre 2,99 pour la famille 11 et 2,11 pour la famille 12) malgré un nombre d'articles comparable, signe d'une demande intermittente (beaucoup de jours à zéro vente, puis de petites quantités ponctuelles), plus difficile à bien prévoir avec des méthodes de prévision classiques. Pas de changement de périmètre décidé vu le temps disponible, mais cette limite doit être assumée et expliquée plutôt que découverte tardivement dans les résultats du modèle.

---

**Décision** : Conserver la colonne "Qte vendue" telle quelle malgré des valeurs de stock négatives associées (251 à 348 lignes par famille) ; prévoir de plafonner "Qte stock" à zéro si cette colonne est utilisée comme variable plus tard
**Pourquoi** : Le détail des lignes à stock négatif montre que la quantité vendue correspond presque exactement à l'ampleur du négatif (ex : vente de 15 → stock à -15), et le négatif s'accumule dans le temps pour un même article en rupture prolongée (ex : article 199277, -16 puis -17 deux jours après). Cela indique une vente réelle et fiable malgré un compteur de stock mal synchronisé (probable décalage entre arrivée physique en rayon et mise à jour du système), différent d'une rupture "stock=0, vente=0" où la demande n'est pas observée. La colonne ventes reste donc fiable pour la prévision de la demande.

---

**Décision** : Coder la colonne "période spéciale" avec des dates précises codées en dur (2025-02-24 pour Ramadan, 2025-11-17 pour la Fête de l'Indépendance), et documenter que cette colonne devra être mise à jour manuellement pour toute réutilisation du modèle sur une autre année
**Pourquoi** : Ramadan suit le calendrier lunaire hégirien (~354 jours/an) et recule d'environ 10-11 jours chaque année par rapport au calendrier grégorien (ex : 2 mars en 2025, ~18-19 février en 2026), un numéro de semaine fixe ne serait donc plus valable d'une année sur l'autre. Le modèle est entraîné et validé uniquement sur 2025 ; cette limite doit être explicitée dans la restitution finale plutôt que découverte silencieusement si le modèle était réutilisé tel quel pour 2026.

**Décision** : Adopter les fenêtres officielles du calendrier promotionnel Marjane (fichier PCC 2025) pour la colonne "période spéciale", avec 5 campagnes distinctes pertinentes pour le rayon 40
**Pourquoi** : Le fichier PCC 2025 (calendrier commercial officiel Marjane) donne des fenêtres précises et fiables, bien supérieures à des dates isolées devinées à partir des seuls pics de ventes. Sélection retenue (lien direct avec Ménage/Table/Cuisine) : Chaabane+Ramadan (6 fév-9 mars), Queue de promo Ménage (10-24 mars), Aïd El Adha (14 mai-7 juin), Anniversaire (22 oct-**23 nov**, fenêtre élargie), Déstockage Bazar (27 nov-14 déc). Exclues : Aïd El Fitr, Fêtes fin d'année, Trafic Blanc & Lavage (plus liées au textile/linge de maison, hors périmètre).

**Point encore debattu** : le pic massif du 18 novembre (864 unités en un jour, contre ~170-200 habituellement) tombe après la fin officielle de la campagne Anniversaire au PCC (13 novembre), l'explication initiale de l'étape 3 (Fête de l'Indépendance, jour férié) reste plausible en parallèle. Décision finale de Yassir : plutôt que de créer un événement séparé, la fenêtre Anniversaire est élargie jusqu'au 23 novembre (incluant toute la semaine du pic) pour englober ce pic dans une seule campagne, sans trancher formellement laquelle des deux causes (anniversaire ou fête nationale) domine.

---

**Décision** : Utiliser le MAPE (erreur moyenne en pourcentage) comme métrique principale d'évaluation des modèles, plutôt que le MAE ou le RMSE
**Pourquoi** : Le MAPE exprime l'erreur en pourcentage de la vraie valeur, ce qui permet de comparer équitablement la précision entre les 3 familles malgré leurs volumes très différents (13 813 à 38 993 unités/an), contrairement au MAE et au RMSE qui restent en unités brutes et favoriseraient artificiellement les familles à petit volume. Le MAPE est aussi plus intuitif à présenter à un public non technique (maître de stage, équipes Marjane) qu'un RMSE. Limite connue du MAPE (instabilité quand la vraie valeur est proche de zéro) jugée non bloquante ici, car les volumes hebdomadaires agrégés restent toujours largement au-dessus de zéro (minimum ~100 unités).

---

**Décision** : Modèle final retenu, approche hybride par famille : XGBoost (réglages optimisés par famille via un jeu de validation) pour les familles 11 et 12, baseline naïve pour la famille 10
**Pourquoi** : Découpage rigoureux en 3 (entraînement/validation/test) pour choisir les réglages XGBoost (nombre d'arbres, profondeur, taux d'apprentissage) sans jamais les ajuster sur le test, puis évaluation finale sur le test avec MAPE. Résultats validés : XGBoost bat la baseline sur la famille 12 (21,8% vs 28,7%) et la famille 11 (28,3% vs 34,4%), mais reste nettement moins bon sur la famille 10 (44,6% vs 32,9%) malgré l'optimisation des réglages, confirmation que la demande intermittente de la famille 10 (déjà notée à l'étape 3) est une limite structurelle, pas un problème de réglage. MAPE global hybride attendu meilleur que XGBoost ou la baseline utilisés seuls partout. XGBoost a d'abord été testé avec des réglages fixes (100 arbres/profondeur 3, puis 30/2) avant d'adopter la recherche par grille sur validation, jugée nécessaire pour éviter le biais d'ajuster les réglages en regardant le test.

---

**Point ouvert (à corriger avant la restitution finale)** : la carte Power BI "% Ventes en Periode Speciale" affiche 37%, mais le recalcul direct sur les données brutes avec les 5 fenêtres de campagnes finales (jusqu'au 23 novembre inclus pour l'Anniversaire) donne **41,2%** (35 060 / 85 084 unités)
**Pourquoi l'écart** : probablement une version de `ventes_hebdo_features` / des CSV exportés antérieure à la toute dernière correction de la fenêtre Anniversaire (23 novembre). Correction nécessaire avant la présentation finale : relancer `feature_engineering.py` et `modelisation.py` en entier, réexporter les 3 CSV, puis rafraîchir les données dans Power BI (Home → Refresh).

---

*Dernière mise à jour : à compléter au fur et à mesure des décisions suivantes.*
