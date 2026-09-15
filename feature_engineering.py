import sqlite3
import pandas as pd
connexion = sqlite3.connect("marjane.db")
df = pd.read_sql_query("SELECT * FROM ventes_rayon40",connexion)
connexion.close()
df["date"] = pd.to_datetime(df["date"])
df["semaine"] = df["date"].dt.to_period("W").apply(lambda r: r.start_time)
df_hebdo = df.groupby(["semaine","Fam,"])["Qte vendue"].sum().reset_index()
df_hebdo = df_hebdo.rename(columns = {"Fam," : "famille","Qte vendue" : "qte_semaine"})
print(df_hebdo.head(15))
print(df_hebdo.shape)
compagnes = [("2025-02-06", "2025-03-09"),  # Chaabane + Ramadan
    ("2025-03-10", "2025-03-24"),  # Queue de promo Ménage
    ("2025-05-14", "2025-06-07"),  # Aïd El Adha
    ("2025-10-22", "2025-11-23"),  # Anniversaire
    ("2025-11-27", "2025-12-14"),] # Déstockage Bazar]
def dans_une_compagne(date_semaine) : 
    for debut,fin in compagnes :
        if pd.Timestamp(debut) <= date_semaine <= pd.Timestamp(fin) : 
            return 1
    return 0
df_hebdo["periode_speciale"] = df_hebdo["semaine"].apply(dans_une_compagne)
print(df_hebdo[df_hebdo["periode_speciale"] == 1][["semaine", "famille", "qte_semaine", "periode_speciale"]])


df_hebdo = df_hebdo.sort_values(["famille","semaine"]).reset_index(drop=True)
df_hebdo["qte_semaine_moins_1"] = df_hebdo.groupby("famille")["qte_semaine"].shift(1)
df_hebdo["qte_semaine_moins_2"] = df_hebdo.groupby("famille")["qte_semaine"].shift(2)
print(df_hebdo.head(10))
df_hebdo["moyenne_mobile_4sem"] = df_hebdo.groupby("famille")["qte_semaine"].shift(1).rolling(window=4).mean().reset_index(drop=True)
print(df_hebdo.head(10))
connexion = sqlite3.connect("marjane.db")
df_hebdo.to_sql("ventes_hebdo_features", connexion, if_exists="replace", index=False)
connexion.close()
print("Table 'ventes_hebdo_features' enregistrée avec succès.")