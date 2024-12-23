# EI4 • IoT - TP 1
# ANDRIATSILAVO Matteo - TP A

import sqlite3, random as R, math as M

# Ouverture/Initialisation de la base de donnee 
conn = sqlite3.connect('logement.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

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

# 0 - On vide les tables `mesures` et `factures` car elles contiennent des lignes aléatoires
c.execute("DROP TABLE IF EXISTS mesures")
c.execute("DROP TABLE IF EXISTS factures")
# - On les recrée ensuite
c.execute("""CREATE TABLE mesures(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            valeur FLOAT NOT NULL,
            id_capteur      INTEGER NOT NULL,
            date_insertion  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_capteur) REFERENCES capteurs(id))""")
c.execute("""CREATE TABLE factures(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            id_logement INTEGER,  
            nom TEXT NOT NULL,
            montant FLOAT NOT NULL,
            valeur_consommee FLOAT,
            FOREIGN KEY (id_logement) REFERENCES logements(id))""")

# 1 - Nous ajoutons des mesures aléatoires
# 1 - A. 
# Nous ajoutons maintenant 25 mesures aléatoires de capteur d'humidité
mesuresHumiditeAleatoires = [R.randint(3000, 5000) / 100 for _ in range(25)]        # l'humidité idéale d'une pièce se situe entre 30% et 50%
# Recherche de l'id correspondant au TYPE de capteurs mesurant le taux d'humidité en pourcents (`humidite`)
idTypeCapteurHum = c.execute("SELECT id FROM types_capteurs WHERE type_mesure = 'humidite'").fetchall()[0]['id']
# Recherche de l'id correspondant au capteur mesurant le taux d'humidité
idCapteurHum = c.execute(f"SELECT id FROM capteurs WHERE id_type_capteur = {idTypeCapteurHum} LIMIT 1").fetchall()[0]['id']
# Création des valeurs (d'humidité) à ajouter dans la table `mesures`
valeursHumidite = [(hum, idCapteurHum) for hum in mesuresHumiditeAleatoires]
# Ajout des valeurs (d'humidité) dans la table `mesures`
c.executemany("INSERT INTO mesures(valeur, id_capteur) VALUES (?, ?)", valeursHumidite)

# 1 - B. 
# Nous ajoutons maintenant 25 mesures aléatoires de capteur de température (en degré celsius)
mesuresTemperatureCAleatoires = [R.randint(1500, 2500) / 100 for _ in range(25)]    # la température varie entre 15°C et 25°C
# Recherche de l'id correspondant au TYPE de capteurs mesurant une température en degrés Celcius (`temperature_C`)
idTypeCapteurTempC = c.execute("SELECT id FROM types_capteurs WHERE type_mesure = 'temperature_C'").fetchall()[0]['id']
# Recherche de l'id correspondant au capteur mesurant une température en degrés Celcius
idCapteurTempC = c.execute(f"SELECT id FROM capteurs WHERE id_type_capteur = {idTypeCapteurTempC} LIMIT 1").fetchall()[0]['id']
# Création des valeurs (de température) à ajouter dans la table `mesures`
valeursTemperatureC = [(temp, idCapteurTempC) for temp in mesuresTemperatureCAleatoires]
# Ajout des valeurs (d'humidité) dans la table `mesures`
c.executemany("INSERT INTO mesures(valeur, id_capteur) VALUES (?, ?)", valeursTemperatureC)


# 2 - Nous ajoutons des factures aléatoires
# Une liste de différentes catégories de factures que peut générer un ménage
listeTypesFactures = ["Eau", "Electricite", "Chauffage", "Gaz", "Internet", "Telephonie"]
# Un dictionnaire par catégorie de facture, chaque type est lié à un prix minimal, un prix maximal et un diviseur
# (valeurs basés sur les moyennes françaises en un mois)
dictMontantsTypesFactures = {   "Eau": [1300, 2600, 100],   "Electricite": [4500, 9000, 100],   "Chauffage": [1600, 2000, 1], 
                                "Gaz": [900, 1000, 10],     "Internet": [2000, 3000, 100],      "Telephonie": [100, 200, 10]}
# Création de 50 valeurs aléatoires à ajouter dans la table `factures`
listeFacturesAleatoires = []
for _ in range(50):
    typeFactureAleatoire = R.choice(listeTypesFactures)
    valeursTypeFacture = dictMontantsTypesFactures[typeFactureAleatoire]
    montantAleatoire = R.randint(valeursTypeFacture[0], valeursTypeFacture[1])
    consommationAleatoire = round(montantAleatoire * R.randint(0, 100) / (100 * valeursTypeFacture[2]), 2)
    listeFacturesAleatoires.append((typeFactureAleatoire, montantAleatoire, consommationAleatoire))
# Ajout des valeurs (factures) dans la table `factures`
c.executemany("INSERT INTO factures(nom, montant, valeur_consommee) VALUES (?, ?, ?)", listeFacturesAleatoires)

# Fermeture
conn.commit()
conn.close()