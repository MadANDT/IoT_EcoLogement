# EI4 • IoT - TP 1
# ANDRIATSILAVO Matteo - TP A

import datetime as DATE, math as M, pandas as pd, random as R
import sqlite3
import meteo_API

# ==== TEST ET EXEMPLES ==== #
# Disponibles dans le fichier ~/docs_&_examples/exemple_cours_SQL&PTHON.py
# ==== FIN TEST ET EXEMPLES ==== #

# ==== MES FONCTIONS ==== #
def create_table_capteurs(c: sqlite3.Connection.cursor):
    """Crée la table des capteurs via un ordre SQL.
    Entrées: `c` (Curseur SQLite connecté à la BdD)
    Sorties: Aucune (création en place)"""
    c.execute("""CREATE TABLE capteurs(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            id_type_capteur             INTEGER NOT NULL,
            id_piece                    INTEGER, 
            port_communication_serveur  INTEGER,
            date_insertion              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_type_capteur) REFERENCES types_capteurs(id),
            FOREIGN KEY (id_piece) REFERENCES pieces(id))""")

def create_table_factures(c: sqlite3.Connection.cursor):
    """Crée la table des factures via un ordre SQL.
    Entrées: `c` (Curseur SQLite connecté à la BdD)
    Sorties: Aucune (création en place)"""
    c.execute("""CREATE TABLE factures(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            id_logement INTEGER,  
            nom TEXT NOT NULL,
            montant FLOAT NOT NULL,
            valeur_consommee FLOAT,
            FOREIGN KEY (id_logement) REFERENCES logements(id))""")
    
def create_table_logements(c: sqlite3.Connection.cursor):
    """Crée la table des logements via un ordre SQL.
    Entrées: `c` (Curseur SQLite connecté à la BdD)
    Sorties: Aucune (création en place)"""
    c.execute("""CREATE TABLE logements(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom                 TEXT NOT NULL,
            adresse             TEXT NOT NULL,                      
            numero_telephone    TEXT,                          
            adresse_IP          TEXT,
            coordonnee_latitude FLOAT,
            coordonnee_longitude FLOAT, 
            date_insertion      TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

def create_table_mesures(c: sqlite3.Connection.cursor):
    """Crée la table des mesures via un ordre SQL.
    Entrées: `c` (Curseur SQLite connecté à la BdD)
    Sorties: Aucune (création en place)"""
    c.execute("""CREATE TABLE mesures(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            valeur FLOAT DEFAULT -1.0,
            id_capteur      INTEGER NOT NULL,
            date_insertion  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_capteur) REFERENCES capteurs(id))""")

def create_table_pieces(c: sqlite3.Connection.cursor):
    """Crée la table des pièces via un ordre SQL.
    Entrées: `c` (Curseur SQLite connecté à la BdD)
    Sorties: Aucune (création en place)"""
    c.execute("""CREATE TABLE pieces(
            id              INTEGER PRIMARY KEY AUTOINCREMENT,            
            id_logement     INTEGER NOT NULL,  
            nom             TEXT NOT NULL,
            coordonnee_x    INTEGER NOT NULL,
            coordonnee_y    INTEGER NOT NULL,
            coordonnee_z    INTEGER NOT NULL,
            FOREIGN KEY (id_logement) REFERENCES logements(id))""")

def create_table_types_capteurs(c: sqlite3.Connection.cursor):
    """Crée la table des types de capteurs/actionneurs via un ordre SQL.
    Entrées: `c` (Curseur SQLite connecté à la BdD)
    Sorties: Aucune (création en place)"""
    c.execute("""CREATE TABLE types_capteurs(
            id                      INTEGER PRIMARY KEY AUTOINCREMENT,
            cap_ou_act              INT NOT NULL,
            type_mesure             TEXT,
            unite_mesure            TEXT,
            plage_precision         TEXT,
            reference_commerciale   TEXT NOT NULL,
            autres_infos            TEXT)""")

def drop_table(c: sqlite3.Connection.cursor, table: str):
    """Supprime la table SQL `table`, si elle exitste, avec l'ordre SQL ''DROP TABLE'' via le curseur SQLite `c`.
    Entrées: `c` (Curseur SQLite connecté à la BdD), `table` (string, nom de la table à supprimer) 
    Sorties: Aucune (suppression en place)  
    """
    c.execute(f"DROP TABLE IF EXISTS {table}")

def init_logements(c: sqlite3.Connection.cursor, file_logements_csv: str):
    """Crée un état initial de la table des logements en la remplissant à partir d'un fichier CSV.
    Le fichier utilisés a pour en-tête: "École" (nom du logement), "Adresse" (adresse du logement), 
    "Latitude" (coordonnée en latitude du logement), "Longitude" (coordonnée en longitude du logement)
    Entrées: `c` (Curseur SQLite connecté à la BdD), `file_logements_csv` (string, chemin vers le fichier CSV, séparateur: ,)
    Sorties: Aucune (remplissage en place)"""
    dataframe = pd.read_csv(file_logements_csv)
    # En-tête du fichier CSV
    Ecole, Adresse, Latitude, Longitude = "École", "Adresse", "Latitude", "Longitude"
    # Parcours des lignes du fichier CSV à partir de la dataframe associée
    for r in range(len(dataframe)):
        row = dataframe.iloc[r]
        # on récupère chaque information
        e, a, lat, lon = row[Ecole], row[Adresse], float(row[Latitude]), float(row[Longitude])
        # on insère chaque information dans la table
        c.execute(f"INSERT INTO logements(nom, adresse, coordonnee_latitude, coordonnee_longitude) VALUES (?, ?, ?, ?)", (e, a, lat, lon))

def init_types_capteurs(c: sqlite3.Connection.cursor, file_types_capteurs_csv: str):
    """Crée un état initial de la table des types de capteurs/actionneurs en la remplissant à partir d'un fichier CSV.
    Le fichier utilisés a pour en-tête: "cap_ou_act" (capteur "0" ou actionneur "1"), "type_mesure" (type de mesure effectuée), 
    "unite_mesure" (unité de la mesure), "plage_precision" (plage de précision de la mesure en +/-), "referenceç_commerciale" (référence commerciale du type de capteur),
    "autres_infos" (informations complémentaires sur le type de capteur).
    Entrées: `c` (Curseur SQLite connecté à la BdD), `file_types_capteurs_csv` (string, chemin vers le fichier CSV, séparateur: ,)
    Sorties: Aucune (remplissage en place)"""
    dataframe = pd.read_csv(file_types_capteurs_csv)
    # En-tête du fichier CSV
    cap_ou_act, type_mesure, unite_mesure, plage_precision, ref_com, infos = "cap_ou_act", "type_mesure", "unite_mesure", "plage_precision", "reference_commerciale", "autres_infos"
    # Parcours des lignes du fichier CSV à partir de la dataframe associée
    for r in range(len(dataframe)):
        row = dataframe.iloc[r]
        # on récupère chaque information
        cap, typ, uni, pla, ref, inf = int(row[cap_ou_act]), row[type_mesure], row[unite_mesure], row[plage_precision], row[ref_com], row[infos]
        # on insère chaque information dans la table
        c.execute(f"INSERT INTO types_capteurs(cap_ou_act, type_mesure, unite_mesure, plage_precision, reference_commerciale, autres_infos) VALUES (?, ?, ?, ?, ?, ?)", 
                (cap, typ, uni, pla, ref, inf))

def init_pieces(c: sqlite3.Connection.cursor, nb_pieces_max: int = 3):
    """Crée un état initial de la table des pièces en attribuant aléatoirement 1 à nb_pieces_max (3 par défaut) pièces à chaque logment.
    Entrées: `c` (Curseur SQLite connecté à la BdD), `nb_pieces_max` (entier, nombre maximal de pièces par logement)
    Sorties: Aucune (remplissage en place)"""
    liste_id_logements = c.execute(f"SELECT id FROM logements").fetchall()
    for _ in liste_id_logements:
        for p in range(R.randint(1, nb_pieces_max)):  # on se dit aléatoirement 1 à 3 pièces par logement
            c.execute(f"INSERT INTO pieces(id_logement, nom, coordonnee_x, coordonnee_y, coordonnee_z) VALUES (?, ?, ?, ?, ?)", 
                (_['id'], "piece_" + f"{chr(ord('A') + p)}", 0, 0, 0))

def init_capteurs(c: sqlite3.Connection.cursor, nb_capteurs_max: int = 2):
    """Crée un état initial de la table des capteurs en attribuant aléatoirement 1 à nb_capteurs_max (2 par défaut) capteurs à chaque pièce.
    Entrées: `c` (Curseur SQLite connecté à la BdD), `nb_capteurs_max` (entier, nombre maximal de capteurs par pièce)
    Sorties: Aucune (remplissage en place)"""
    # Dans ce qui suit: ''capteurs'' désigne les capteurs comme les actionneurs
    liste_id_pieces = c.execute(f"SELECT id FROM pieces").fetchall()
    liste_types_capteurs = [dict(row) for row in c.execute(f"SELECT id FROM types_capteurs")]
    nb_types_capteurs = len(liste_types_capteurs)
    for id_piece in liste_id_pieces:
        nb_capteurs = R.randint(1, nb_capteurs_max)  
        id_types_capteurs_a_ajouter = [liste_types_capteurs[R.randint(0, nb_types_capteurs - 1)]['id'] for _ in range(nb_capteurs)]
        cap_ou_act = [dict(row) for row in c.execute(f"SELECT id, cap_ou_act FROM types_capteurs") if row['id'] in id_types_capteurs_a_ajouter]
        capteurs_a_ajouter = [(_['id'], id_piece['id'], 80) for _ in cap_ou_act]    # Port 80: typique pour la communication web
        c.executemany(f"INSERT INTO capteurs(id_type_capteur, id_piece, port_communication_serveur) VALUES (?, ?, ?)", capteurs_a_ajouter)

def generer_mesure(valeur_init: int | float, type_capteur: int, dic_type_capteurs) -> float | None:
    """ Génère une mesure fictive aléatoire à partir de la valeur initiale `valeur_init`, 
    en fonction du type de capteur `type_capteur` et de la table `dic_type_capteurs` associée.
    Entrées:    `valeur_init`: int | float, valeur initiale à partir de laquelle on doit calculer la mesure fictive,
                `type_capteur`: int, type du capteur auquel on se referera,
                `dic_type_capteurs`: dictionnaire, table récapitulant la précision des capteurs selon leur type.
    Sorties:    `mesure_fictive`: float, mesure fictive ou None si non applicable"""
    type_cap_utilise = dic_type_capteurs[type_capteur]
    precision_en_pourcentage = type_cap_utilise['pourcentage'] if type_cap_utilise['pourcentage'] != None else None
    variations = type_cap_utilise['variations'] if type_cap_utilise['variations'] != [] else []
    if variations != []:
        # Cas de la précision exprimée en pourcentage
        if precision_en_pourcentage:
            return round(valeur_init * (1 + R.uniform(variations[0], variations[1]) / 100), variations[2])
        # Cas de la précision exprimée en unité relative
        elif precision_en_pourcentage is False:
            return round(valeur_init + (R.uniform(variations[0], variations[1])), variations[2])
        # Cas où la précision n'est pas définie (ex: actionneur)
        else:
            return None
    return None

def init_mesures(c: sqlite3.Connection.cursor, nb_mesures: int):
    """Crée un état "statique" de la table des mesures en attribuant des mesures à tous les capteurs de la base.
    Entrées:    `c` (Curseur SQLite connecté à la BdD),
                `nb_mesures` (int, désigne le nombre de mesures à associer à chaque capteur)
    Sorties: Aucune (remplissage en place)"""

    # On vide la table si elle existe, ce qui fait qu'à chaque appel, on aura des valeurs actualisées
    # drop_table(c, "mesures")
    # On génère ensuite un dictionnaire de dictionnaires, chaque clé est l'ID d'un logement et les valeurs sont
    # les coordonnées en latitude et en longitude (pour requêter l'API météo) et les listes des IDs des pièces et capteurs attachés
    dic_logements = {logement['id']: {  'lat':      logement['coordonnee_latitude'], 
                                        'long':     logement['coordonnee_longitude'],
                                        'pieces':   [],
                                        'capteurs': []}
    for logement in c.execute(f"SELECT id, coordonnee_latitude, coordonnee_longitude FROM logements").fetchall()}
    # ↓ complète la liste des pièces attachées au logement
    for id_logement in dic_logements:
        dic_logements[id_logement]['pieces'] = [piece['id'] 
        for piece in c.execute(f"SELECT id FROM pieces WHERE id_logement = {id_logement}").fetchall()] 
    # ↓ complète la liste des capteurs rattachés au logement
    for id_logement in dic_logements:
        for id_piece in dic_logements[id_logement]['pieces']:
            dic_logements[id_logement]['capteurs'] += [(capteur['id'], capteur['id_type_capteur'])
            for capteur in c.execute(f"SELECT id, id_type_capteur FROM capteurs WHERE id_piece = {id_piece}").fetchall()]

    # ••• TYPES CAPTEURS&CONVERSION&PRÉCISION 
    # Petite variable globale (type dictionnaire) reprenant les types de capteurs et leurs plages de précision
    # Sert à générer, si besoin, une "mesure fictive" à partir de sa plage de précision du capteur
    # on obtiendra une variable `float` aléatoire à l'aide de random.uniform(a, b), arrondie avec ``round``
    dic_type_capteurs = {type_cap['id']: {  'cap_ou_act':   type_cap['cap_ou_act'], 
                                            'type_mesure':  type_cap['type_mesure'],
                                            'pourcentage':  None,  # indique si la précision est en pourcentage
                                            'variations':   []  
                                            # ↑ indique l'intervalle d'imprécision a;b ET à quelle puissance négative de 10 c on est précis si `pourcentage` est faux ([a, b, c]), 
                                            # sinon indique l'intervalle d'imprécision a;b en pourcentage, arrondi au dixième ([a, b, 1])
                                            # → on utilisera la fonction `round` pour les arrondis
                                            }
    for type_cap in c.execute(f"SELECT id, cap_ou_act, type_mesure FROM types_capteurs").fetchall()} 
    
    for type_cap in dic_type_capteurs:
        match type_cap:
            case 1:
                dic_type_capteurs[type_cap]['pourcentage']  = False
                dic_type_capteurs[type_cap]['variations']   = [-0.5, 0.5, 1]
            case 2:
                dic_type_capteurs[type_cap]['pourcentage']  = False
                dic_type_capteurs[type_cap]['variations']   = [-0.5, 0.5, 1]
            case 3:
                dic_type_capteurs[type_cap]['pourcentage']  = True
                dic_type_capteurs[type_cap]['variations']   = [-2, 2, 1]
            case 4:
                dic_type_capteurs[type_cap]['pourcentage']  = True
                dic_type_capteurs[type_cap]['variations']   = [-1.5, 1.5, 1]
            case 5:
                dic_type_capteurs[type_cap]['pourcentage']  = True
                dic_type_capteurs[type_cap]['variations']   = [-10, 10, 1]
            case 6:
                dic_type_capteurs[type_cap]['pourcentage']  = True
                dic_type_capteurs[type_cap]['variartions']   = [-5, 5, 1]
            case 7:
                dic_type_capteurs[type_cap]['pourcentage']  = None
                dic_type_capteurs[type_cap]['variations']   = None
            case 8:
                dic_type_capteurs[type_cap]['pourcentage']  = True
                dic_type_capteurs[type_cap]['variations']   = [-1, 1, 1]
            case 9:
                dic_type_capteurs[type_cap]['pourcentage']  = True
                dic_type_capteurs[type_cap]['variations']   = [-10, 10, 1]
            case 10:
                dic_type_capteurs[type_cap]['pourcentage']  = None
                dic_type_capteurs[type_cap]['variations']   = None
            case 11:
                dic_type_capteurs[type_cap]['pourcentage']  = None
                dic_type_capteurs[type_cap]['variations']   = None
            case 12:
                dic_type_capteurs[type_cap]['pourcentage']  = None
                dic_type_capteurs[type_cap]['variations']   = None
            case 13:
                dic_type_capteurs[type_cap]['pourcentage']  = True
                dic_type_capteurs[type_cap]['variations']   = [-5, 5, 1]
            case _: # cas par défaut
                dic_type_capteurs[type_cap]['pourcentage']  = None
                dic_type_capteurs[type_cap]['variations']   = None
    # ••• FIN TYPES CAPTEURS&CONVERSION&PRÉCISION
    # breakpoint()
    # On génèrera des mesures en fonction de l'heure à laquelle est appellée la fonction
    heure_actuelle =  DATE.datetime.now().hour
    # Pour chaque logement
    for id_logement in dic_logements:
        # Préparer les mesures relatives à ce logement
        mesures_meteo = meteo_API.retreive_weather_data_day0(dic_logements[id_logement]['lat'], dic_logements[id_logement]['long'])
        mesures_formattees = meteo_API.formatting_weather_api_data_day0(mesures_meteo)
        # On récupère la température actuelle relevée par l'API météo
        temperature = mesures_formattees[heure_actuelle]['temperature_2m']
        # On récupère l'humidité relative actuelle relevée par l'API météo
        humidite = mesures_formattees[heure_actuelle]['relative_humidity_2m']
        # On récupère l'irradiation solaire relevée par l'API météo
        luminosite = mesures_formattees[heure_actuelle]['shortwave_radiation']
        # breakpoint()
        # Pour chaque capteur du logement
        for id_cap, type_cap in dic_logements[id_logement]['capteurs']:
            mesure = 0.0
            for _ in range(nb_mesures):
                if type_cap in [1, 2]:  # générer une mesure de température
                    mesure = generer_mesure(temperature, type_cap, dic_type_capteurs)
                elif type_cap in [3, 4]:  # générer une mesure d'humidité
                    mesure = generer_mesure(humidite, type_cap, dic_type_capteurs)
                elif type_cap in [5, 6]:  # générer une mesure de luminosité
                    mesure = generer_mesure(luminosite, type_cap, dic_type_capteurs)
                c.execute(f"INSERT INTO mesures(valeur, id_capteur) VALUES (?, ?)", (mesure, id_cap))
        # breakpoint()

# ==== FIN MES FONCTIONS ==== #



def main():
    """ Crée et remplit la base de données pour débuter à un état initial.
     Les tables créées ET remplies sont `logements`, `pieces`, `types_capteurs` et `capteurs`,
      tandis que celles juste créées sont `mesures` et `factures`. 
    """
    # Ouverture/Initialisation de la base de données
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    # ======== • ======== • ======== • ======== • ======== #
    # 1 - On vide les tables `logements`, `pieces`, `types_capteurs`, `capteurs`, 'mesures', 'factures'
    tables_a_supprimer = ["logements", "pieces", "types_capteurs", "capteurs", "mesures", "factures"]
    for table in tables_a_supprimer:
        drop_table(c, table)
    # - On les recrée ensuite
    create_table_capteurs(c)
    create_table_factures(c)
    create_table_logements(c)
    create_table_mesures(c)
    create_table_pieces(c)
    create_table_types_capteurs(c)
    
    # 2 - Nous ajoutons les différentes écoles du réseau Polytech avec les informations nécéssaires
    # Pour se simplifier la tâche, on utilise le fichier CSV `remplir_logements_bdd`
    init_logements(c, r"remplir_logements_bdd.csv")
    
    # 3 - Nous ajoutons les différents types de capteur, avant de les instancier
    # Pour se simplifier la tâche, on utilise le fichier CSV `remplir_types_capteurs_bdd`
    init_types_capteurs(c, r"remplir_types_capteurs_bdd.csv")

    # 4 - Nous ajoutons les pièces pour chaque logement
    init_pieces(c, 3)
    
    # 5 - Nous ajoutons des capteurs dans les pièces et nous les lions à la table des types de capteurs
    # Dans ce qui suit: ''capteurs'' désigne les capteurs comme les actionneurs
    init_capteurs(c, 2)

    # 6 - Nous ajoutons des mesures aux capteurs de chaque logement; ici, 2 mesures par capteur.
    # breakpoint()
    init_mesures(c, 2)

    # ======== • ======== • ======== • ======== • ======== #
    # Fermeture de la base de données
    conn.commit()
    conn.close()

main()