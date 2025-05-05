# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 14:52:59 2025

@author: mambb
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_06 = pd.read_csv("C:\\Users\\mambb\\Downloads\\merged_2023_06.csv")
df_02 = pd.read_csv("C:\\Users\\mambb\\Downloads\\merged_2023_02.csv")

df_02['Date départ'] = pd.to_datetime(df_02['Date départ'])
df_02['Date arrivée'] = pd.to_datetime(df_02['Date arrivée'])

df_02['Durée en secondes'] = df_02['Durée en secondes']  / 60
df_06['Durée en secondes'] = df_06['Durée en secondes']  / 60

# Nettoyage : on garde les trajets de 1 à 90 min
df_02 = df_02[(df_02['Durée en secondes'] > 1) & (df_02['Durée en secondes'] <= 90)]
df_06 = df_06[(df_06['Durée en secondes'] > 1) & (df_06['Durée en secondes'] <= 90)]

# ➕ Nombre de départs et d’arrivées par station
depart_counts_02 = df_02['Nom station départ'].value_counts()
arrivee_counts_02 = df_02['Nom station arrivée'].value_counts()

depart_counts_06 = df_06['Nom station départ'].value_counts()
arrivee_counts_06 = df_06['Nom station arrivée'].value_counts()

# ➗ Fusion pour obtenir le delta (arrivées - départs)
flux = pd.concat([depart_counts_02, arrivee_counts_02], axis=1)
flux.columns = ['nb_depart', 'nb_arrivee']
flux = flux.fillna(0)
flux['delta'] = flux['nb_arrivee'] - flux['nb_depart']  # >0 = station qui se remplit trop

flux_06 = pd.concat([depart_counts_06, arrivee_counts_06], axis=1)
flux_06.columns = ['nb_depart', 'nb_arrivee']
flux_06 = flux_06.fillna(0)
flux_06['delta'] = flux_06['nb_arrivee'] - flux_06['nb_depart']  # >0 = station qui se remplit trop

# 🔴 Stations en déficit (plus de départs que d’arrivées)
stations_deficit = flux.sort_values(by='delta').head(10)
stations_deficit_06 =  flux_06.sort_values(by='delta').head(10)

# 🟢 Stations en surplus (plus d’arrivées que de départs)
stations_surplus = flux.sort_values(by='delta', ascending=False).head(10)
stations_surplus_06 = flux.sort_values(by='delta', ascending=False).head(10)


# 🔴 Déficit
plt.figure(figsize=(10, 5))
sns.barplot(x=stations_deficit['delta'], y=stations_deficit.index, color='crimson')
plt.title("Top 10 stations en déficit (plus de départs que d’arrivées)")
plt.xlabel("Delta (arrivées - départs)")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
sns.barplot(x=stations_deficit_06['delta'], y=stations_deficit_06.index, color='crimson')
plt.title("Top 10 stations en déficit (plus de départs que d’arrivées) en Juin")
plt.xlabel("Delta (arrivées - départs)")
plt.tight_layout()
plt.show()


# 🟢 Surplus
plt.figure(figsize=(10, 5))
sns.barplot(x=stations_surplus['delta'], y=stations_surplus.index, color='darkgreen')
plt.title("Top 10 stations en surplus (plus d’arrivées que de départs)")
plt.xlabel("Delta (arrivées - départs)")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
sns.barplot(x=stations_surplus_06['delta'], y=stations_surplus_06.index, color='darkgreen')
plt.title("Top 10 stations en surplus (plus d’arrivées que de départs) en Juin")
plt.xlabel("Delta (arrivées - départs)")
plt.tight_layout()
plt.show()

# Comparaison février vs juin
moyenne_df_fevrier = df_02[["Distance parcourue en mètres", "Durée en secondes", "Vitesse maximum"]].mean()
moyenne_df_Juin = df_06[["Distance parcourue en mètres", "Durée en secondes", "Vitesse maximum"]].mean()
df_all = pd.concat([moyenne_df_fevrier, moyenne_df_Juin])
df_all.columns = ["Février", "Juin"]


# Distribution des distances
sns.histplot(df_02["Distance parcourue en mètres"],bins = 50, kde=True)
plt.title("Distribution des distances parcourues en Février ")
plt.show()
# Boxplot de la durée par type de vélo
sns.boxplot(data=df_02, x="Assistance électrique", y="Durée en secondes")
plt.title("Durée en fonction du type de vélo")
plt.show()


# Nouveau boxplot sans les valeurs aberrantes
sns.boxplot(data=df_02, x="Assistance électrique", y="Durée en secondes")
plt.title("Durée (trajets < 1h30) en fonction du type de vélo en Février")
plt.xlabel("Vélo à assistance électrique (True / False)")
plt.ylabel("Durée (secondes)")
plt.show()

# Top trajets les plus fréquents (départ + arrivée) en fevrier
top_trajets_02 = df_02.groupby(["Date arrivée", "Date départ"]).size().reset_index(name="nb_trajets")
top_trajets_02 = top_trajets_02.sort_values("nb_trajets", ascending=False).head(10)
print(top_trajets_02)

# Créer une colonne combinée "trajet"
df_02["trajet"] = df_02["Date départ"].dt.strftime("%Y-%m-%d %H:%M") + " → " + df_02["Date arrivée"].dt.strftime("%Y-%m-%d %H:%M")

# Compter les trajets
top_trajets_02 = df_02["trajet"].value_counts().head(10).sort_values()

# Affichage
plt.figure(figsize=(10, 6))
sns.barplot(x=top_trajets_02.values, y=top_trajets_02.index, palette="magma")
plt.title("Top 10 des trajets les plus fréquents (février)")
plt.xlabel("Nombre de trajets")
plt.ylabel("Trajet (départ → arrivée)")
plt.tight_layout()
plt.show()

# Créer une colonne combinée "trajet"
df_06["Date départ"] = pd.to_datetime(df_06["Date départ"])
df_06["Date arrivée"] = pd.to_datetime(df_06["Date arrivée"])
df_06["trajet"] = df_06["Date départ"].dt.strftime("%Y-%m-%d %H:%M") + " → " + df_06["Date arrivée"].dt.strftime("%Y-%m-%d %H:%M")

# Compter les trajets
top_trajets_06 = df_06["trajet"].value_counts().head(10).sort_values()

# Affichage
plt.figure(figsize=(10, 6))
sns.barplot(x=top_trajets_06.values, y=top_trajets_06.index, palette="magma")
plt.title("Top 10 des trajets les plus fréquents (juin)")
plt.xlabel("Nombre de trajets")
plt.ylabel("Trajet (départ → arrivée)")
plt.tight_layout()
plt.show()








# 1. Charger les données
df_etat_juin = pd.read_csv("C:/Users/mambb/Downloads/Hist_Rempl_2023_06.csv") # adapter le nom exact
# 2. Conversion de la date
df_etat_juin['Date mise à jour'] = pd.to_datetime(df_etat_juin['Date mise à jour'])
# 3. Extraire l'heure
df_etat_juin['heure'] = df_etat_juin['Date mise à jour'].dt.hour
# 4. Ajouter une colonne "Total vélos disponibles"
df_etat_juin['total_disponibles'] = df_etat_juin['VM disponibles'] + df_etat_juin['VAE disponibles']


# Charger février aussi
df_etat_fev = pd.read_csv("C:/Users/mambb/Downloads/Hist_Rempl_2023_02.csv")
df_etat_fev['Date mise à jour'] = pd.to_datetime(
    df_etat_fev['Date mise à jour'].astype(str).str.strip(),
    format="%Y-%m-%d %H:%M:%S",
    errors='coerce'  # met NaT si ce n’est pas convertible
)
df_etat_fev['heure'] = df_etat_fev['Date mise à jour'].dt.hour
df_etat_fev['total_disponibles'] = df_etat_fev['VM disponibles'] + df_etat_fev['VAE disponibles']
# Moyenne par heure
moyenne_juin = df_etat_juin.groupby('heure')['total_disponibles'].mean()
moyenne_fev = df_etat_fev.groupby('heure')['total_disponibles'].mean()
# Fusion pour comparaison
df_compare = pd.DataFrame({
    'Juin (usage fort)': moyenne_juin,
    'Février (usage faible)': moyenne_fev
})

# Visualisation
plt.figure(figsize=(10, 5))
df_compare.plot(marker='o')
plt.title("Disponibilité moyenne des vélos par heure : Février vs Juin")
plt.xlabel("Heure")
plt.ylabel("Vélos disponibles (moyenne)")
plt.grid(True)
plt.tight_layout()
plt.show()


# Fréquence où une station est vide
station_vide_freq = df_etat_juin[df_etat_juin['total_disponibles'] == 0]['Nom station'].value_counts().head(10)

station_vide_freq_02 = df_etat_fev[df_etat_fev['total_disponibles'] == 0]['Nom station'].value_counts().head(10)

plt.figure(figsize=(10, 5))
sns.barplot(x=station_vide_freq.values, y=station_vide_freq.index, color='tomato')
plt.title("Top 10 stations les plus souvent vides – Juin")
plt.xlabel("Nombre de fois à 0 vélo")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
sns.barplot(x=station_vide_freq_02.values, y=station_vide_freq_02.index, color='yellow')
plt.title("Top 10 stations les plus souvent vides – Février")
plt.xlabel("Nombre de fois à 0 vélo")
plt.tight_layout()
plt.show()

# 2. Nettoyage & ajout colonnes
for df in [df_etat_fev, df_etat_juin]:
    df['Date mise à jour'] = pd.to_datetime(df['Date mise à jour'])
    df['heure'] = df['Date mise à jour'].dt.hour
    df['total_disponibles'] = df['VM disponibles'] + df['VAE disponibles']
# 3. Choisir les mêmes stations dans les deux périodes
stations_commun = (
    df_etat_juin['Nom station'].value_counts().head(15).index.intersection(
    df_etat_fev['Nom station'].value_counts().head(15).index)
)

df_juin_filtre = df_etat_juin[df_etat_juin['Nom station'].isin(stations_commun)]
df_fev_filtre = df_etat_fev[df_etat_fev['Nom station'].isin(stations_commun)]

# 4. Créer les deux pivots
pivot_juin = df_juin_filtre.groupby(['Nom station', 'heure'])['total_disponibles'].mean().unstack()
pivot_fev = df_fev_filtre.groupby(['Nom station', 'heure'])['total_disponibles'].mean().unstack()

# 5. Visualisation côte à côte
fig, axes = plt.subplots(1, 2, figsize=(20, 10))

sns.heatmap(pivot_fev, cmap='YlOrRd', ax=axes[0], linewidths=0.3, linecolor='gray')
axes[0].set_title("Février – Usage faible")
axes[0].set_xlabel("Heure")
axes[0].set_ylabel("Station")

sns.heatmap(pivot_juin, cmap='YlGnBu', ax=axes[1], linewidths=0.3, linecolor='gray')
axes[1].set_title("🌿 Juin – Usage fort")
axes[1].set_xlabel("Heure")
axes[1].set_ylabel("Station")

plt.suptitle("Comparaison des disponibilités horaires – Février vs Juin", fontsize=16)
plt.tight_layout()
plt.show()



# Charger le fichier de régulations
df_reg_juin = pd.read_csv("C:/Users/mambb/Downloads/Reg_mouv_stat_2023_06.csv")
df_reg_fev = pd.read_csv("C:/Users/mambb/Downloads/Reg_mouv_stat_2023_06.csv")

# Total de vélos déposés par station cible
deposes = df_reg_juin.groupby('Nom station dépose')['Total'].sum()
deposes_fev = df_reg_fev.groupby('Nom station dépose')['Total'].sum()

# Total de vélos prélevés par station source
prises = df_reg_juin.groupby('Nom station prise')['Total'].sum()
prises_fev = df_reg_fev.groupby('Nom station prise')['Total'].sum()

regul_juin = pd.concat([prises, deposes], axis=1)
regul_juin.columns = ['nb_prises', 'nb_deposes']
regul_juin = regul_juin.fillna(0)
regul_juin['volume_total_regule'] = regul_juin['nb_prises'] + regul_juin['nb_deposes']

regul_fev = pd.concat([prises_fev, deposes_fev], axis=1)
regul_fev.columns = ['nb_prises', 'nb_deposes']
regul_fev = regul_fev.fillna(0)
regul_fev['volume_total_regule'] = regul_fev['nb_prises'] + regul_fev['nb_deposes']


# Jointure
bilan_juin = flux_06.merge(regul_juin, left_index=True, right_index=True, how='left')
bilan_juin = bilan_juin.fillna(0)

bilan_fev = flux.merge(regul_fev, left_index=True, right_index=True, how='left')
bilan_fev = bilan_fev.fillna(0)

# Mesure l'écart non couvert par la régulation
bilan_juin['ecart_non_couvert'] = abs(bilan_juin['delta']) - bilan_juin['volume_total_regule']
bilan_fev['ecart_non_couvert'] = abs(bilan_fev['delta']) - bilan_fev['volume_total_regule']

# Classement : stations déséquilibrées mal régulées
stations_critique_juin = bilan_juin.sort_values(by='ecart_non_couvert', ascending=False).head(15)
stations_critique_fev = bilan_fev.sort_values(by='ecart_non_couvert', ascending=False).head(15)

# Aperçu
print(stations_critique_juin[['nb_depart', 'nb_arrivee', 'delta', 'volume_total_regule', 'ecart_non_couvert']])
print(stations_critique_fev[['nb_depart', 'nb_arrivee', 'delta', 'volume_total_regule', 'ecart_non_couvert']])




plt.figure(figsize=(10, 6))
sns.barplot(data=stations_critique_fev, y=stations_critique_fev.index, x='ecart_non_couvert', palette='magma')
plt.title("Top 15 stations les plus déséquilibrées mal régulées – Février")
plt.xlabel("Écart non couvert (|arrivées - départs| - régulation)")
plt.ylabel("Station")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(data=stations_critique_juin, y=stations_critique_juin.index, x='ecart_non_couvert', palette='viridis')
plt.title("Top 15 stations les plus déséquilibrées mal régulées – Février")
plt.xlabel("Écart non couvert (|arrivées - départs| - régulation)")
plt.ylabel("Station")
plt.tight_layout()
plt.show()




# Compter combien de fois une station est vide ou pleine
vide_juin = df_etat_juin[df_etat_juin['total_disponibles'] == 0]['Nom station'].value_counts()
pleine_juin = df_etat_juin[df_etat_juin['Nombre de diapasons disponibles'] == 0]['Nom station'].value_counts()
vide_fev = df_etat_fev[df_etat_fev['total_disponibles'] == 0]['Nom station'].value_counts()
pleine_fev = df_etat_fev[df_etat_fev['Nombre de diapasons disponibles'] == 0]['Nom station'].value_counts()

etat_freq_juin = pd.concat([vide_juin, pleine_juin], axis=1).fillna(0)
etat_freq_juin.columns = ['freq_vide_juin', 'freq_pleine_juin']
etat_freq_fev = pd.concat([vide_fev, pleine_fev], axis=1).fillna(0)
etat_freq_fev.columns = ['freq_vide_fev', 'freq_pleine_fev']


# Fusion flux + régulation
base_juin = flux_06.merge(regul_juin, left_index=True, right_index=True, how='left').fillna(0)
base_fev = flux.merge(regul_fev, left_index=True, right_index=True, how='left').fillna(0)

# Ajout de l'état station
base_juin = base_juin.merge(etat_freq_juin, left_index=True, right_index=True, how='left').fillna(0)
base_fev = base_fev.merge(etat_freq_fev, left_index=True, right_index=True, how='left').fillna(0)


base_juin['criticite'] = (
    abs(base_juin['delta']) * 0.4 +
    base_juin['freq_vide_juin'] * 0.3 +
    base_juin['freq_pleine_juin'] * 0.3 -
    base_juin['volume_total_regule'] * 0.5  # pénalité si déjà régulé
)
base_fev['criticite'] = (
    abs(base_fev['delta']) * 0.4 +
    base_fev['freq_vide_fev'] * 0.3 +
    base_fev['freq_pleine_fev'] * 0.3 -
    base_fev['volume_total_regule'] * 0.5  # pénalité si déjà régulé
)


top_critique_juin = base_juin.sort_values(by='criticite', ascending=False).head(15)
top_critique_juin[['nb_depart', 'nb_arrivee', 'delta',
              'volume_total_regule', 'freq_vide_juin', 'freq_pleine_juin', 'criticite']]
top_critique_fev = base_fev.sort_values(by='criticite', ascending=False).head(15)
top_critique_fev[['nb_depart', 'nb_arrivee', 'delta',
              'volume_total_regule', 'freq_vide_fev', 'freq_pleine_fev', 'criticite']]



# Renommer les colonnes pour les différencier
base_juin = base_juin.copy()
base_juin = base_juin.rename(columns=lambda x: f"{x}_juin")
base_fev = base_fev.copy()
base_fev = base_fev.rename(columns=lambda x: f"{x}_fevrier")

# Fusion sur le nom de la station
comparaison = base_juin.merge(base_fev, left_index=True, right_index=True, how='inner')


# Créer une colonne de variation
comparaison['variation_criticite'] = comparaison['criticite_juin'] - comparaison['criticite_fevrier']

# Stations toujours critiques
stations_constantes = comparaison.sort_values(by=['criticite_juin', 'criticite_fevrier'], ascending=False).head(15)

# Stations dont la criticité explose en été
stations_saison_ete = comparaison.sort_values(by='variation_criticite', ascending=False).head(15)


plt.figure(figsize=(12, 6))
sns.scatterplot(data=stations_constantes, x='criticite_fevrier', y='criticite_juin')
plt.title("Stations critiques : Février vs Juin")
plt.xlabel("Criticité Février")
plt.ylabel("Criticité Juin")
plt.grid(True)
plt.tight_layout()
plt.show()

stations_saison_ete[['criticite_fevrier', 'criticite_juin', 'variation_criticite']]



