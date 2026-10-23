# Data Source — IBM Telco Customer Churn

## Dataset

- Nom : IBM Telco Customer Churn
- Source : IBM GitHub
- Fichier original : `Telco-Customer-Churn.csv`
- Emplacement local : `data/raw/telco.csv`
- Format : CSV
- Nombre de lignes : 7043
- Nombre de colonnes : 21

## Provenance

URL du dataset :

https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/1fd6fd70906479be1712e64cfc0ea89f58466629/data/Telco-Customer-Churn.csv

## Intégrité des données

Algorithme utilisé : SHA-256

Empreinte SHA-256 : 16320C9C...

Le fichier original est conservé sans modification dans `data/raw/`.

## Objectif du dataset

L'objectif est d'étudier les caractéristiques des clients d'un opérateur télécom afin de préparer un futur modèle prédictif du churn.

- Identifiant : `customerID`
- Variable cible : `Churn`
- Variables numériques potentielles : `tenure`, `MonthlyCharges`, `TotalCharges`
- Variables catégorielles potentielles : `Contract`, `InternetService`, `PaymentMethod`

La variable `Churn` indique si un client a quitté l'opérateur (`Yes`) ou non (`No`).