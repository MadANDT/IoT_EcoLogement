# EI4 • IoT - TP 1
# ANDRIATSILAVO Matteo - TP A

import datetime as DATE, math as M, pandas as pd, random as R
import sqlite3
import meteo_API
# # Ouverture/Initialisation de la base de donnee 
# conn = sqlite3.connect('logement.db')
# conn.row_factory = sqlite3.Row
# c = conn.cursor()
# ouverture/initialisation de la base de donnee 
conn = sqlite3.connect('bibli.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# affichage d'une table
# lecture dans la base avec un select
c.execute('SELECT * FROM Etudiant')

# parcourt ligne a ligne
for raw in c.execute('SELECT * FROM Etudiant'):
	print raw.keys()
	print raw["Nom"]

# insertion d'une donnee
c.execute("INSERT INTO Emprunte VALUES (4,1,'23/10/2020')")

# insertion de plusieurs donnees
values = []
for i in range(3):
	values.append((R.randint(1,5),i+1,"'%d/11/2020'" %(R.randint(1,30))))
c.executemany('INSERT INTO Emprunte VALUES (?,?,?)', values)

# lecture dans la base avec un select
c.execute('SELECT * FROM Emprunte')
#print c
#print c[0]
print c.fetchall()

# fermeture
conn.commit()
conn.close()

# ======================== EXEMPLES ======================== #
# Affichage d'une table et lecture dans la base via `SELECT`
# c.execute('SELECT * FROM pieces')

# Parcours à la ligne
# for raw in c.execute('SELECT * FROM pieces'):
#     print(raw.keys())
#     print(raw["nom"])

# Insertion de plusieurs donnees
# values = []
# for i in range(3):
#     values.append((R.randint(10, 50) / 7, 1, f"'{R.randint(1, 30)}/11/2024'"))
# # Exemple : c.executemany('INSERT INTO <table> VALUES (?, ?, ?)', values)
# c.executemany('INSERT INTO mesures(valeur, id_capteur, date_insertion) VALUES (?, ?, ?)', values)

# Lecture dans la base avec un `SELECT`
# print(c.fetchall())
# c.execute('SELECT * FROM mesures')
# rows = c.fetchall()
# for line in rows:
#     print(dict(line))
# ==================FIN EXEMPLES ======================== #

# ================ TESTS ================ #
# # 0 - On vide les tables `mesures` et `factures` car elles contiennent des lignes aléatoires
# c.execute("DROP TABLE IF EXISTS mesures")
# c.execute("DROP TABLE IF EXISTS factures")
# # - On les recrée ensuite
# c.execute("""CREATE TABLE mesures(
#             id INTEGER PRIMARY KEY AUTOINCREMENT, 
#             valeur FLOAT NOT NULL,
#             id_capteur      INTEGER NOT NULL,
#             date_insertion  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (id_capteur) REFERENCES capteurs(id))""")
# c.execute("""CREATE TABLE factures(
#             id INTEGER PRIMARY KEY AUTOINCREMENT, 
#             id_logement INTEGER,  
#             nom TEXT NOT NULL,
#             montant FLOAT NOT NULL,
#             valeur_consommee FLOAT,
#             FOREIGN KEY (id_logement) REFERENCES logements(id))""")

# # # 1 - Nous ajoutons des mesures aléatoires
# # # 1 - A. 
# # # Nous ajoutons maintenant 25 mesures aléatoires de capteur d'humidité
# # mesuresHumiditeAleatoires = [R.randint(3000, 5000) / 100 for _ in range(25)]        # l'humidité idéale d'une pièce se situe entre 30% et 50%
# # # Recherche de l'id correspondant au TYPE de capteurs mesurant le taux d'humidité en pourcents (`humidite`)
# # idTypeCapteurHum = c.execute("SELECT id FROM types_capteurs WHERE type_mesure = 'humidite'").fetchall()[0]['id']
# # # Recherche de l'id correspondant au capteur mesurant le taux d'humidité
# # idCapteurHum = c.execute(f"SELECT id FROM capteurs WHERE id_type_capteur = {idTypeCapteurHum} LIMIT 1").fetchall()[0]['id']
# # # Création des valeurs (d'humidité) à ajouter dans la table `mesures`
# # valeursHumidite = [(hum, idCapteurHum) for hum in mesuresHumiditeAleatoires]
# # # Ajout des valeurs (d'humidité) dans la table `mesures`
# # c.executemany("INSERT INTO mesures(valeur, id_capteur) VALUES (?, ?)", valeursHumidite)
# # # 1 - B. 
# # # Nous ajoutons maintenant 25 mesures aléatoires de capteur de température (en degré celsius)
# # mesuresTemperatureCAleatoires = [R.randint(1500, 2500) / 100 for _ in range(25)]    # la température varie entre 15°C et 25°C
# # # Recherche de l'id correspondant au TYPE de capteurs mesurant une température en degrés Celcius (`temperature_C`)
# # idTypeCapteurTempC = c.execute("SELECT id FROM types_capteurs WHERE type_mesure = 'temperature_C'").fetchall()[0]['id']
# # # Recherche de l'id correspondant au capteur mesurant une température en degrés Celcius
# # idCapteurTempC = c.execute(f"SELECT id FROM capteurs WHERE id_type_capteur = {idTypeCapteurTempC} LIMIT 1").fetchall()[0]['id']
# # # Création des valeurs (de température) à ajouter dans la table `mesures`
# # valeursTemperatureC = [(temp, idCapteurTempC) for temp in mesuresTemperatureCAleatoires]
# # # Ajout des valeurs (d'humidité) dans la table `mesures`
# # c.executemany("INSERT INTO mesures(valeur, id_capteur) VALUES (?, ?)", valeursTemperatureC)

# # # 2 - Nous ajoutons des factures aléatoires
# # # Une liste de différentes catégories de factures que peut générer un ménage
# # listeTypesFactures = ["Eau", "Electricite", "Chauffage", "Gaz", "Internet", "Telephonie"]
# # # Un dictionnaire par catégorie de facture, chaque type est lié à un prix minimal, un prix maximal et un diviseur
# # # (valeurs basés sur les moyennes françaises en un mois)
# # dictMontantsTypesFactures = {   "Eau": [1300, 2600, 100],   "Electricite": [4500, 9000, 100],   "Chauffage": [1600, 2000, 1], 
# #                                 "Gaz": [900, 1000, 10],     "Internet": [2000, 3000, 100],      "Telephonie": [100, 200, 10]}
# # # Création de 50 valeurs aléatoires à ajouter dans la table `factures`
# # listeFacturesAleatoires = []
# # for _ in range(50):
# #     typeFactureAleatoire = R.choice(listeTypesFactures)
# #     valeursTypeFacture = dictMontantsTypesFactures[typeFactureAleatoire]
# #     montantAleatoire = R.randint(valeursTypeFacture[0], valeursTypeFacture[1])
# #     consommationAleatoire = round(montantAleatoire * R.randint(0, 100) / (100 * valeursTypeFacture[2]), 2)
# #     listeFacturesAleatoires.append((typeFactureAleatoire, montantAleatoire, consommationAleatoire))
# # # Ajout des valeurs (factures) dans la table `factures`
# # c.executemany("INSERT INTO factures(nom, montant, valeur_consommee) VALUES (?, ?, ?)", listeFacturesAleatoires)

# # 3 - On vide les tables `logements`, `pieces`, `types_capteurs` et `capteurs`
# c.execute("DROP TABLE IF EXISTS logements")
# c.execute("DROP TABLE IF EXISTS pieces")
# c.execute("DROP TABLE IF EXISTS types_capteurs")
# c.execute("DROP TABLE IF EXISTS capteurs")
# # - On les recrée ensuite
# c.execute("""CREATE TABLE logements(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             nom                 TEXT NOT NULL,
#             adresse             TEXT NOT NULL,                      
#             numero_telephone    TEXT,                          
#             adresse_IP          TEXT,
#             coordonnee_latitude FLOAT,
#             coordonnee_longitude FLOAT, 
#             date_insertion      TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
# c.execute("""CREATE TABLE pieces(
#             id              INTEGER PRIMARY KEY AUTOINCREMENT,            
#             id_logement     INTEGER NOT NULL,  
#             nom             TEXT NOT NULL,
#             coordonnee_x    INTEGER NOT NULL,
#             coordonnee_y    INTEGER NOT NULL,
#             coordonnee_z    INTEGER NOT NULL,
#             FOREIGN KEY (id_logement) REFERENCES logements(id))""")
# c.execute("""CREATE TABLE types_capteurs(
#             id                      INTEGER PRIMARY KEY AUTOINCREMENT,
#             cap_ou_act              INT NOT NULL,
#             type_mesure             TEXT,
#             unite_mesure            TEXT,
#             plage_precision         TEXT,
#             reference_commerciale   TEXT NOT NULL,
#             autres_infos            TEXT)""")
# c.execute("""CREATE TABLE capteurs(
#             id INTEGER PRIMARY KEY AUTOINCREMENT, 
#             id_type_capteur             INTEGER NOT NULL,
#             id_piece                    INTEGER, 
#             port_communication_serveur  INTEGER,
#             date_insertion              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (id_type_capteur) REFERENCES types_capteurs(id),
#             FOREIGN KEY (id_piece) REFERENCES pieces(id))""")

# # 4 - Nous ajoutons les différentes écoles du réseau Polytech avec les informations nécéssaires
# # Pour se simplifier la tâche, on utilise le fichier CSV `remplir_logements_bdd`
# fichier_logements_csv = r"remplir_logements_bdd.csv"
# dataframe = pd.read_csv(fichier_logements_csv)
# # En-tête du fichier CSV
# Ecole, Adresse, Latitude, Longitude = "École", "Adresse", "Latitude", "Longitude"
# # Parcours des lignes du fichier CSV à partir de la dataframe associée
# for r in range(len(dataframe)):
#     row = dataframe.iloc[r]
#     # on récupère chaque information
#     e, a, lat, lon = row[Ecole], row[Adresse], float(row[Latitude]), float(row[Longitude])
#     # on insère chaque information dans la table
#     c.execute(f"INSERT INTO logements(nom, adresse, coordonnee_latitude, coordonnee_longitude) VALUES (?, ?, ?, ?)", (e, a, lat, lon))

# # 5 - Nous ajoutons les différents types de capteur, avant de les instancier
# # Pour se simplifier la tâche, on utilise le fichier CSV `remplir_types_capteurs_bdd`
# fichier_types_capteurs_csv = r"remplir_types_capteurs_bdd.csv"
# dataframe = pd.read_csv(fichier_types_capteurs_csv)
# # En-tête du fichier CSV
# cap_ou_act, type_mesure, unite_mesure, plage_precision, ref_com, infos = "cap_ou_act", "type_mesure", "unite_mesure", "plage_precision", "reference_commerciale", "autres_infos"
# # Parcours des lignes du fichier CSV à partir de la dataframe associée
# for r in range(len(dataframe)):
#     row = dataframe.iloc[r]
#     # on récupère chaque information
#     cap, typ, uni, pla, ref, inf = int(row[cap_ou_act]), row[type_mesure], row[unite_mesure], row[plage_precision], row[ref_com], row[infos]
#     # on insère chaque information dans la table
#     c.execute(f"INSERT INTO types_capteurs(cap_ou_act, type_mesure, unite_mesure, plage_precision, reference_commerciale, autres_infos) VALUES (?, ?, ?, ?, ?, ?)", 
#               (cap, typ, uni, pla, ref, inf))

# # 6 - Nous ajoutons les pièces pour chaque logement
# liste_id_logements = c.execute(f"SELECT id FROM logements").fetchall()
# for _ in liste_id_logements:
#     for p in range(R.randint(1, 3)):  # on se dit aléatoirement 1 à 3 pièces par logement
#         c.execute(f"INSERT INTO pieces(id_logement, nom, coordonnee_x, coordonnee_y, coordonnee_z) VALUES (?, ?, ?, ?, ?)", 
#               (_['id'], "piece_" + f"{chr(ord('A') + p)}", 0, 0, 0))
# # 7 - Nous ajoutons des capteurs dans les pièces et nous les lions à la table des types de capteurs
# # Dans ce qui suit: ''capteurs'' désigne les capteurs comme les actionneurs
# liste_id_pieces = c.execute(f"SELECT id FROM pieces").fetchall()
# liste_types_capteurs = [dict(row) for row in c.execute(f"SELECT id FROM types_capteurs")]
# nb_types_capteurs = len(liste_types_capteurs)
# for id_piece in liste_id_pieces:
#     nb_capteurs = R.randint(1, 2)   # on se dit aléatoirement 1 à 2 capteurs/actionneurs par pièces
#     id_types_capteurs_a_ajouter = [liste_types_capteurs[R.randint(0, nb_types_capteurs - 1)]['id'] for _ in range(nb_capteurs)]
#     cap_ou_act = [dict(row) for row in c.execute(f"SELECT id, cap_ou_act FROM types_capteurs") if row['id'] in id_types_capteurs_a_ajouter]
#     # capteurs_a_ajouter = [(_['id'], _['cap_ou_act']) for _ in cap_ou_act]   
#     capteurs_a_ajouter = [(_['id'], id_piece['id'], 80) for _ in cap_ou_act]    # Port 80: typique pour la communication web
#     c.executemany(f"INSERT INTO capteurs(id_type_capteur, id_piece, port_communication_serveur) VALUES (?, ?)", capteurs_a_ajouter)
# ================ FIN TESTS ============ #
