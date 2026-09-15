import pandas as pd 
fichiers = [("Etat de ventes journaliére du mois 01-2025.xlsx",1),("Etat de ventes journaliére du mois 02-2025.xlsx", 2),
    ("Etat de ventes journaliére du mois 03-2025.xlsx", 3),
    ("Etat de ventes journaliére du mois 04-2025.xlsx", 4),
    ("Etat de ventes journaliére du mois 05-2025.xlsx", 5),
    ("Etat de ventes journaliére du mois 06-2025.xlsx", 6),
    ("Etat de ventes journaliére du mois 07-2025.xlsx", 7),
    ("Etat de ventes journaliére du mois 08-2025.xlsx", 8),
    ("Etat de ventes journaliére du mois 09-2025.xlsx", 9),
    ("Etat de ventes journaliére du mois 10-2025.xlsx", 10),
    ("Etat de ventes journaliére du mois 11-2025.xlsx", 11),
    ("Etat de ventes journaliére du mois 12-2025.xlsx", 12),]
tableaux_mensuels = []
for nom_fichier, numero_mois in fichiers : 
    df = pd.read_excel(nom_fichier, sheet_name = "Base")
    print(df.columns.tolist())
    df_filtre = df[df["Ray,"] == 40] 
    df_filtre = df_filtre[df_filtre["Fam,"].isin([10,11,12])]
    df_filtre = df_filtre.copy()
    df_filtre["date"] = pd.to_datetime({"year":2025,"month" : numero_mois ,"day": df_filtre["Jour"]})
    tableaux_mensuels.append(df_filtre)
    print(f"mois {numero_mois} : {df_filtre.shape[0]} lignes gardées")
df_final = pd.concat(tableaux_mensuels, ignore_index = True)
print("Total final :", df_final.shape)
print("Valeurs manquantes :")
print(df_final[["Qte vendue","Montant(TTC)","Qte stock"]].isna().sum())
quantites_negatives = df_final[df_final["Qte vendue"] < 0]
print("Nombre de lignes avec quantité négative :", len(quantites_negatives))
print(quantites_negatives[["date","Code article","Qte vendue","Montant(TTC)","Etat"]].head(10))

import sqlite3
connexion = sqlite3.connect("marjane.db")
df_final.to_sql("ventes_rayon40", connexion, if_exists = "replace", index = False)
connexion.close()
print("Base SQLite créée avec succès.")