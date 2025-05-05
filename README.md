# 🚲 Projet Data - Analyse des stations Vélib’ (Février & Juin)

Ce projet a pour objectif d’analyser les **données d’usage et de régulation** des stations Vélib’ à Paris, à deux périodes clés : **février et juin**. Il vise à identifier les stations les plus sollicitées, les plus déséquilibrées, et à proposer des recommandations d'optimisation.

---

## 📁 Structure du projet
projet_velib_Paris_2023/
├── data/ # Données utilisées 
├── src/ # Scripts Python (.py) 
├── notebooks/ # Explorations et visualisations
├── outputs/ # Graphiques générés (heatmaps, plots, etc.)
├── requirements.txt # Librairies nécessaires pour exécuter le projet
└── README.md # 


---

## 📊 Données utilisées

Les fichiers de données proviennent du jeu fourni dans le cadre du **Hackathon Vélib’ Métropole**.

Après exploration, nous avons retenu **3 fichiers principaux** :

- `merged.csv` : informations sur les stations les plus souvent utilisées, les déséquilibres entre départs et arrivées, et les périodes critiques d’usage
- `Reg_mouv_stat.csv` : une vision temporelle fine du niveau de remplissage des stations, pour repérer celles qui sont souvent vides ou pleines  
- `Hist_Rempl.csv` : mesurer les interventions opérateurs (prises/déposes vélos) et de les croiser avec les besoins réels 

> 📌 **Pourquoi ces fichiers ?**  
> Ce sont ceux qui offrent la meilleure lisibilité pour analyser la **fréquentation, l’équilibrage logistique** et les **problèmes utilisateurs**. Leur utilisation croisée permet une vision stratégique.

---

## 🔍 Étapes du projet

1. **Exploration et nettoyage des données**
2. **Analyse temporelle des stations les plus fréquentées**
3. **Comparaison entre février et juin (heatmaps & stats)**
4. **Évaluation de la criticité des stations**
5. **Analyse des régulations et efficacité logistique**
6. **Signalements et zones à problème**
7. **Recommandations stratégiques**

---

## 📈 Résultats clés (à compléter)

- 🔥 Stations les plus sollicitées identifiées
- 🧊 Stations sous-utilisées localisées
- 📦 Suggestions de repositionnement de bornes ou amélioration des rotations

> 🧠 Résultats visuels : voir le dossier `/outputs/` pour les heatmaps et comparatifs graphiques.

---

## 🛠️ Technologies

- Python
- Pandas / Numpy
- Matplotlib / Seaborn
- Spyder

---
