# F1 Strategy 🏎️

Une application de calcul de stratégie de course pour la Formule 1, développée en Python avec une interface graphique Tkinter.

## Description

F1 Strategy est un outil permettant d'analyser et de calculer les stratégies optimales de pneus et d'arrêts au stand lors d'une course de Formule 1. L'application prend en compte de plusieurs paramètres tels que :

- La consommation de carburant
- L'usure des pneus (Soft, Medium, Hard)
- Les temps d'arrêt au stand
- La dégradation des performances en fonction du carburant

## Fonctionnalités

- **Calcul d'usure de pneus** : Simulation réaliste de la dégradation des pneus à différents composés
- **Gestion du carburant** : Prise en compte de la consommation et de l'impact sur les temps au tour
- **Stratégies d'arrêts** : Analyse des différentes stratégies d'arrêts possibles
- **Interface graphique** : Interface utilisateur avec entrées personnalisables


## Paramètres configurables

### Paramètres de course
- Tours dans la course
- Tours complétés
- Temps des arrêts au stand
- Carburant au départ
- Consommation par tour
- Impact du carburant sur les performances

### Paramètres de pneus
- Temps de référence par composé (Soft, Medium, Hard)
- Usure par tour
- Dégradation en fonction du carburant

## Installation

```bash
# Cloner ou télécharger le projet
cd f1_strategy

# Créer un environnement virtuel (optionnel mais recommandé)
python3 -m venv venv
source venv/bin/activate

# Aucune dépendance externe requise - tkinter est inclus avec Python
```

## Utilisation

```bash
python strategy.py
```

L'application se lancera avec une interface graphique où vous pourrez :
1. Configurer les paramètres de votre course
2. Entrer les données des pneus
3. Voir les calculs de stratégie en temps réel

## Requis

- Python 3.6+
- Tkinter (inclus avec Python standard)
- NumPy

## Structure du projet

```
f1_strategy/
├── strategy.py          # Fichier principal avec l'application
├── README.md           # Ce fichier
└── venv/              # Environnement virtuel (optionnel)
```

## Licence

Ce projet est fourni à titre personnel pour l'analyse de stratégies F1.

## Notes

Cette application simule les stratégies de Formule 1 sur la base des paramètres actuels du sport et peut être utilisée pour :
- Apprendre les concepts de stratégie F1
- Analyser les choix stratégiques des équipes
- Simuler différents scénarios de course
