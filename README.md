# Ⅰ-Leaf • Logements écoresponsables

EI 4 - IoT, projet serveur REST
ANDRIATSILAVO Matteo - TP A

Ce projet a pour thème les logements écoresponsables et les requêtes sur une base de données.
L'idée est de travailler sur l'aspect de visualisation et de commande en temps réels de dispositifs intelligent (capteurs/ actionneurs) capables d'estimer la consommation énergétique des occupants du logement.

## Installation

Utiliser le gestionnaire de packages [pip](https://pip.pypa.io/en/stable/) pour mettre en place l'environnement de développement.
* Requiert avoir installé Python (v. >= 3.0.0) et `pip`

```bash
pip install -r requirements.txt
```

## Lancement
* Une première étape consistera à lancer le script SQL `logement.sql` pour mettre en place la base de données.
* Ensuite, ajouter une touche de Python (pour un état "_initial_"): 
```python
>>> py remplissage_initial.py
```
Le serveur peut maintenant être lancé:
```python
>>> fastapi dev .\ServeurREST.py
```
- La page d'accueil est disponible à l'adresse IP `127.0.0.1:8000`.
Trois premières options sont disponibles, une seule est pour l'instant fonctionnelle: _Logements_.
- En cliquant dessus, un choix vous proposera un des logements (tous fictifs bien sûr) dans l'une des écoles du réseau POLYTECH.
- Votre choix fait, vous serez redirigé vers une page qui présente les prévisions météo pour les 7 prochains jours du logement en question.
Les données proviennent d'une API open source: [Open Meteo](https://open-meteo.com/).

## Sources
**Open Meteo**, **Stack Overflow**, **ChatGPT**, **W3Schools**.
Github: [projet IoT](https://github.com/MadANDT/IoT_EcoLogement). 
