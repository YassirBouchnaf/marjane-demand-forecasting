import sqlite3
import pandas as pd
connexion = sqlite3.connect("marjane.db")
df_hebdo = pd.read_sql_query("SELECT * FROM ventes_hebdo_features",connexion)
connexion.close()
df_hebdo["semaine"] = pd.to_datetime(df_hebdo["semaine"])
df_hebdo["prevision_baseline"] = df_hebdo["qte_semaine_moins_1"]
print(df_hebdo[["semaine", "famille", "qte_semaine", "prevision_baseline"]].head(10))

import xgboost as xgb
df_modele = df_hebdo.dropna(subset = ["qte_semaine_moins_1","qte_semaine_moins_2","moyenne_mobile_4sem"])
features = ["periode_speciale","qte_semaine_moins_1","moyenne_mobile_4sem"]
cible = "qte_semaine"

import numpy as np 
def calcule_mape(reel,prevision) :
    return np.mean(np.abs((reel - prevision)/reel))*100

from itertools import product
date_validation_debut = pd.Timestamp("2025-08-01")
date_test_debut = pd.Timestamp("2025-10-01")
entrainement = df_modele[df_modele["semaine"] < date_validation_debut]
validation = df_modele[(df_modele["semaine"] >= date_validation_debut) & (df_modele["semaine"] < date_test_debut)]
test = df_modele[df_modele["semaine"] >= date_test_debut]
grille_reglages = list(product([20, 30, 50], [2, 3], [0.05, 0.1]))
meilleur_reglage_par_famille = {}
for fam in df_modele["famille"].unique():
     entrainement_fam = entrainement[entrainement["famille"] == fam]
     validation_fam = validation[validation["famille"] == fam]
     meilleur_mape = None
     meilleur_reglage = None
     for n_est, prof, taux in grille_reglages:
         modele = xgb.XGBRegressor(n_estimators=n_est, max_depth=prof, learning_rate=taux, random_state=42)
         modele.fit(entrainement_fam[features], entrainement_fam[cible])
         preds_validation = modele.predict(validation_fam[features])
         mape_validation = calcule_mape(validation_fam[cible], preds_validation)
         if meilleur_mape is None or mape_validation < meilleur_mape:
            meilleur_mape = mape_validation
            meilleur_reglage = (n_est, prof, taux)
     meilleur_reglage_par_famille[fam] = meilleur_reglage
     print(f"Famille {fam} -> meilleur réglage : {meilleur_reglage} (MAPE validation : {meilleur_mape:.1f}%)")   

predictions_test = []

for fam in df_modele["famille"].unique():
    n_est, prof, taux = meilleur_reglage_par_famille[fam]
    entrainement_complet_fam = pd.concat([
        entrainement[entrainement["famille"] == fam],
        validation[validation["famille"] == fam]
    ])
    test_fam = test[test["famille"] == fam].copy()
    modele_final = xgb.XGBRegressor(n_estimators=n_est, max_depth=prof, learning_rate=taux, random_state=42)
    modele_final.fit(entrainement_complet_fam[features], entrainement_complet_fam[cible])
    test_fam["prevision_xgboost"] = modele_final.predict(test_fam[features])
    predictions_test.append(test_fam)
test = pd.concat(predictions_test, ignore_index=True)


mape_baseline = calcule_mape(test["qte_semaine"],test["prevision_baseline"])
mape_xgboost = calcule_mape(test["qte_semaine"],test["prevision_xgboost"])
print("=== MAPE global (39 semaines de test) ===")
print(f"Baseline : {mape_baseline:.1f}%")
print(f"XGBoost  : {mape_xgboost:.1f}%")
print()

test_sans_pic = test[test["semaine"]!=pd.Timestamp("2025-11-17")]
mape_baseline_sans_pic = calcule_mape(test_sans_pic["qte_semaine"],test_sans_pic["prevision_baseline"])
mape_xgboost_sans_pic = calcule_mape(test_sans_pic["qte_semaine"],test_sans_pic["prevision_xgboost"])
print("=== MAPE sans la semaine du 17 novembre ===")
print(f"Baseline : {mape_baseline_sans_pic:.1f}%")
print(f"XGBoost  : {mape_xgboost_sans_pic:.1f}%")
print()

print("=== MAPE par famille ===")
for fam in test["famille"].unique():
    sous_test = test[test["famille"] == fam]
    mape_b = calcule_mape(sous_test["qte_semaine"],sous_test["prevision_baseline"])
    mape_x = calcule_mape(sous_test["qte_semaine"],sous_test["prevision_xgboost"])
    print(f"Famille {fam} -> Baseline : {mape_b:.1f}% | XGBoost : {mape_x:.1f}%")

def prevision_hybride(ligne) : 
    if ligne["famille"] == 10.0 :
        return ligne["prevision_baseline"]
    else :
        return ligne["prevision_xgboost"]
test["prevision_finale"] = test.apply(prevision_hybride,axis = 1)
connexion = sqlite3.connect("marjane.db")
test.to_sql("resultats_test", connexion, if_exists = "replace", index = False)
connexion.close()
print("Table 'resultats_test' enregistrée avec succès.")

connexion = sqlite3.connect("marjane.db")

ventes_hebdo_features = pd.read_sql_query("SELECT * FROM ventes_hebdo_features", connexion)
ventes_hebdo_features.to_csv("ventes_hebdo_features.csv", index=False)

ventes_rayon40 = pd.read_sql_query("SELECT * FROM ventes_rayon40", connexion)
ventes_rayon40.to_csv("ventes_rayon40.csv", index=False)

resultats_test = pd.read_sql_query("SELECT * FROM resultats_test", connexion)
resultats_test.to_csv("resultats_test.csv", index=False)

connexion.close()
print("Fichiers CSV exportés avec succès.")