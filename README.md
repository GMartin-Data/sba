# SBA Project

# Contexte Global

Ce projet a été réalisé dans le cadre de la formation Développeur Data/IA Ecole MicroSoft by SIMPLON, sur le Campus de Valenciennes

# Contributeurs

- Thibaut Watu
- Grégory Martin

# Description

Il s'agissait d'effectuer une prédiction à l'aide d'un algorithme de classification, puis de créer une application avec une architecture en micro-services: application Web, API et BDD.

# Pitch

_Vous êtes data scientist pour l’United States Small Business Administration, US SBA._

_L’US SBA a été fondée en 1953 dans le but d’aider les petites entreprises à avoir un crédit. Les petites entreprises ont été la principale source de création d'emplois aux États-Unis; par conséquent, favoriser la création et la croissance de petites entreprises présente des avantages sociaux en créant des opportunités d'emploi et en réduisant le chômage._

_L’enjeu est de prédire si les entreprises seront capables de rembourser leur prêt ou pas. Vous êtes dans le cas d’une classification binaire (oui le prêt doit être accordé ou non il ne doit pas être accordé)._

# Organisation du Dépôt Distant

## Folders

Le repo comporte trois folders essentiels:

- `machine_learning` contenant les notebooks et scripts dévolus à la conception du modèle
- `web` contenant la logique de l'application Web, conçue avec Django
- `api` contenant la logique de l'API, conçue avec FastAPI

## Technologies Supplémentaires

A noter que, bien que Django embarque nativement SQLite3 comme solution BDD, nous avons, par souci pédagogique, implémenté la BDD sous PostgreSQL également.

Docker a permis une conteneurisation des applications, que nous avons également déployé sur Azure, en utilisant les services associés.

# Machine Learning

Même si non contraint à des enjeux de conteneurisation, ce folder exploratoire comporte un `requirements.txt` comprenant les principales bibliothèques utilisées.

A noter que l'exploration ayant eu lieu dans l'environnement Jupyter Lab, cette bibliothèque y est proposée.

Il est recommandé de recourir à la création d'un environnement virtuel où installer le tout, via:

- `python3 -m venv venv`
- `python -r requirements.txt`

Une présentation succinte des différents notebooks:

## `eda.ipynb`

Contient une exploration sommaire des données brutes

## `cleaning.ipynb`

Contient un nettoyage en vue de la conception du dataset de base servant à l'entraînement du modèle.

## `modeling.ipynb`

Après avoir comparé quelques modèles lors d'une pré-analyse, non regroupée ici, nous avons opté pour un modèle `XGBoostClassifier` pour ses performances ainsi que sa relative capacité à être interprété dans une certaine mesure.
Ce notebook présente l'ensemble des techniques impliquées dans la conception de ce modèle, à savoir

- D'abord, dans une approche _"data-centric"_, une sélection des features les plus pertinentes afin d'améliorer le score $F_1$ macro d'un modèle brut (non tuné), par élimination progressive des features (semblable à un `SequentialFeatureSelector`).
- Ensuite, une recherche des meilleurs hyperparamètres à l'aide de `RandomizedSearchCV` (les méthodes bayésiennes à l'aide d'Optuna n'ont pas donné de résultats probants)
- Enfin, une recherche d'interprétabilité du modèle via deux moyens: les **feature importances** (inhérentes aux modèles d'arbre) et l'exploitation des **Shapley Values** à l'aide de la bibliothèque `shap`.

## `build_model.py`

Constitue un script permettant d'entraîner, scorer sur le test set, puis exporter le modèle réglé sur ses meilleurs hyperparamètres.

# Application & API

## Fonctionnement

L'application et l'API fonctionnent de concert.

- L'utilisateur utilise l'application grâce au lien `Make Predictions` accessible via la navbar du header.
- Il soit alors s'acquitter de soumettre un formulaire correspondant aux détails administratifs en vue de l'obtention du prêt.
- L'API sert à l'application un endpoint permettant de récupérer:
  - La prédiction sous forme de `str`: `"Accepted"` ou `"Rejected"`
  - La probabilité correspondante, estimée par le modèle
  - Un _Waterfall_ plot, correspondant à une interpétation de la prédiction proposée.
- Ces éléments sont diffusés à l'utilisateur dès le formulaire validé.

## Installation et Détails Techniques
