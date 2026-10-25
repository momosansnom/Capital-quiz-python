# Capital-quiz-python
Mini-jeu interactif en Python type GeoGuessr pour localiser les capitales mondiales sur une carte.

## Objectif
Ce projet de CPGE simule le jeu GeoGuessr. Le but est de deviner la position exacte d'une capitale mondiale sur une carte. Le score est basé sur la distance en kilomètres entre le clic de l'utilisateur et les coordonnées réelles, calculée via la géométrie sphérique terrestre.

## Fonctionnement
* **Jeu :** Le nom de la capitale à trouver s'affiche dans le titre de la fenêtre.
* **Premier clic (Évaluation) :** Affiche votre point, la vraie capitale, trace la distance géodésique et met à jour le score.
* **Second clic (Rejouer) :** Efface la carte et lance une nouvelle manche.
* **Quitter :** Touche `q` ou `Échap` pour fermer la fenêtre et afficher le bilan dans le terminal.

## Installation et Lancement
Python 3.x est requis, ainsi que les bibliothèques suivantes :

```bash
pip install matplotlib numpy
```

Assurez-vous que les fichiers `Donnees.csv` (coordonnées des capitales) et `carte.jpg` (carte du monde) sont dans le même répertoire que le script.

Pour lancer une partie :

```bash
python geo.py
```
