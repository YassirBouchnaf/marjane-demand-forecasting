import sqlite3
import pandas as pd
connexion = sqlite3.connect("marjane.db")

# 1. Ventes totales par jour de la semaine

requete_jour_semaine = """
SELECT strftime("%w",date) AS jour_semaine, SUM("Qte vendue") AS total_qte
FROM ventes_rayon40
GROUP BY jour_semaine
ORDER BY jour_semaine
"""
resultat_jour_semaine = pd.read_sql_query(requete_jour_semaine,connexion)
print("=== Ventes par jour de la semaine ===")
print(resultat_jour_semaine)
print()

# 2. Évolution des ventes semaine par semaine sur l'année

requete_semaine_annee = """
SELECT strftime("%W",date) AS numero_semaine, SUM("Qte vendue") AS total_qte
FROM ventes_rayon40
GROUP BY numero_semaine
ORDER BY numero_semaine
"""
resultat_semaine_annee = pd.read_sql_query(requete_semaine_annee,connexion)
print("=== Ventes par semaine de l'année ===")
print(resultat_semaine_annee.to_string())
print()

# 3. Dates exactes des semaines à pic (08 et 46)

requete_dates_pic = """
SELECT strftime("%W",date) AS numero_semaine , MIN(date) AS premiere_date ,MAX(date) AS derniere_date
FROM ventes_rayon40
WHERE strftime("%W",date) IN ("08","46")
GROUP BY numero_semaine
"""
resultat_dates_pic = pd.read_sql_query(requete_dates_pic,connexion)
print("=== Dates exactes des semaines à pic ===")
print(resultat_dates_pic)
print()

# 4. Comparaison des 3 familles (volume et tendance)

requete_comparaison_familles = """
SELECT "Fam," AS famille , "Libelle Fam," AS libelle_famille , SUM("Qte vendue") AS total_qte, ROUND(AVG("Qte vendue"),2) AS moyenne_qte_par_ligne, COUNT(DISTINCT "Code article") AS nb_articles
FROM ventes_rayon40
GROUP BY famille
ORDER BY total_qte DESC
"""
resultat_comparaison_familles = pd.read_sql_query(requete_comparaison_familles,connexion)
print("=== Comparaison des 3 familles ===")
print(resultat_comparaison_familles)
print()

# 5. Jours avec rupture de stock, par famille

requete_ruptures = """
SELECT "Fam," AS famille , "Libelle Fam," AS libelle_famille , COUNT(*) AS nb_lignes_rupture, COUNT(DISTINCT date) nb_jours_concernes
FROM ventes_rayon40
WHERE "Qte stock" = 0
GROUP BY famille
ORDER BY nb_lignes_rupture
"""
resultat_ruptures = pd.read_sql_query(requete_ruptures,connexion)
print("=== Ruptures de stock par famille ===")
print(resultat_ruptures)
print()

# 6. Investigation des valeurs de stock négatives

requete_stock_negatif = """
SELECT "Fam," AS famille, COUNT(*) AS nb_lignes_stock_negatif
FROM ventes_rayon40
WHERE "Qte stock" < 0
GROUP BY famille
"""
resultat_stock_negatif = pd.read_sql_query(requete_stock_negatif, connexion)
print("=== Nombre de lignes à stock négatif, par famille ===")
print(resultat_stock_negatif)
print()

requete_detail_stock_negatif = """
SELECT date, "Code article", "Qte vendue", "Qte stock", "Etat"
FROM ventes_rayon40
WHERE "Qte stock" < 0
LIMIT 10
"""
resultat_detail_stock_negatif = pd.read_sql_query(requete_detail_stock_negatif, connexion)
print("=== Détail de quelques lignes à stock négatif ===")
print(resultat_detail_stock_negatif)
print()
connexion.close()