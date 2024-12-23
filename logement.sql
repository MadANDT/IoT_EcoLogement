-- EI4 • IoT - TP 1
-- ANDRIATSILAVO Matteo - TP A

-- Qs.1 - Modèle relationnel de la BDD
-- Diagramme réalisé et validé ✅.

--💡 Pour la date d'insertion dans la base, utiliser la construction:
-- TIMESTAMP DEFAULT CURRENT_TIMESTAMP

-- Qs.2 - Ordres SQL permettant de détruire toutes les tables présentes dans la base.
DROP TABLE IF EXISTS logements;
DROP TABLE IF EXISTS pieces;
DROP TABLE IF EXISTS factures;
DROP TABLE IF EXISTS capteurs;         -- table des capteurs et des actionneurs (Cap_Act)
DROP TABLE IF EXISTS mesures;
DROP TABLE IF EXISTS types_capteurs;   -- table des types des capteurs et des actionneurs (Cap_Act)

--💡 La commande sqlite3 pour lire un fichier est `$ .read fichier.sql`.

-- Qs.3 - Ordres SQL permettant de créer toutes les tables présentes dans la base.

-- Un logement est la plus "grande" entité de notre modèle relationnel. Il peut contenir une à plusieurs pièces et est alimenté de factures.
CREATE TABLE logements(
    -- ID du logement, unique, ne peut être nul (PK)
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,    
    -- Adresse du logement, ne peut être nul
    adresse             TEXT NOT NULL,                      
    -- Numero de téléphone du logement, limité à 12 caractères, ne peut être nul
    numero_telephone    TEXT NOT NULL,                          
    -- Adresse IP du logement, limité à 20 caractères, ne peut être nul 
    adresse_IP          TEXT NOT NULL,                          
    -- Date d'insertion dans la table, automatiquement renseignée
    date_insertion      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Une pièce peut contenir (ou non) des capteurs/actionneurs et fait partie d'un logement, elle est également modélisé dans l'espace par des coordonnées.
CREATE TABLE pieces(
    -- ID de la pièce, unique, ne peut être nul (PK)
    id              INTEGER PRIMARY KEY AUTOINCREMENT,            
    -- ID du logement auquel appartient la pièce, pas unique car un logement peut avoir 1 à plusieurs pièces 
    -- et ne peut être nul car une pièce appartient forcément à un logement 
    id_logement     INTEGER NOT NULL,  
    -- Nom de la pièce, limité à 255 caractères, ne peut être nul
    nom             TEXT NOT NULL,                              
    -- Coordonnée X de la pièce, précision limitée à un entier, ne peut être nul
    coordonnee_x    INTEGER NOT NULL,                                       
    -- Coordonnée Y de la pièce, précision limitée à un entier, ne peut être nul
    coordonnee_y    INTEGER NOT NULL,                                       
    -- Coordonnée Z de la pièce, précision limitée à un entier, ne peut être nul
    coordonnee_z    INTEGER NOT NULL,
    --#-- Clé étrangère faisant référence au logement auquel la pièce appartient (FK)
    FOREIGN KEY (id_logement) REFERENCES logements(id)
);


-- Les factures peuvent être de différents types, elles ont un montant, une valeur de consommation et alimentent un logement.
CREATE TABLE factures(
    -- ID de la facture, unique, ne peut être nul
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,    
    -- ID du logement auquel est rattaché la facture, pas unique et peut être nul car un logement peut avoir (ou pas) 1 à plusieurs factures
    id_logement         INTEGER,  
    -- Nom de la facture, limité à 255 caractères, ne peut être nul
    nom             TEXT NOT NULL,
    -- Date d'émission de la facture, renseignée automatiquement
    date_emission       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Montant forfaitaire de la facture, ne peut être nul
    montant             FLOAT NOT NULL,
    -- Valeur consommée de la facture, peut être nulle car facture non consommée
    valeur_consommee    FLOAT,
    --#-- Clé étrangère faisant référence au logement auquel la facture est rattachée (FK)
    FOREIGN KEY (id_logement) REFERENCES logements(id)
);


-- La table des types de capteurs permet de connaître le type de mesure effectuée par un capteur, l'unité de la mesure, la précision et d'autres infos utiles.
CREATE TABLE types_capteurs(
    -- ID du capteur/actionneur, unique, ne peut être nul
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    -- Type de mesure réalisée par le capteur, limité à 255 caractères, unique, ne peut être nul 
    type_mesure     TEXT NOT NULL UNIQUE,
    -- Unité de mesure du capteur, limitée à 20 caractères (préfixes, puissances, etc.), ne peut être nulle
    unite_mesure    TEXT NOT NULL,
    -- Plage de précision de la mesure, limitée à 255 caractères, ne peut être nulle
    plage_precision TEXT NOT NULL,
    -- Autres informations utiles sur le capteur/actionneur, peuvent être vides si inexistantes
    autres_infos    TEXT
);


-- Un capteur/actionneur effectue une mesure/action, il a une référence commerciale, est associé à une pièce et possède un port de communication avec le serveur.
CREATE TABLE capteurs(
    -- ID du capteur/actionneur, unique, ne peut être nul (PK)
    id                          INTEGER PRIMARY KEY AUTOINCREMENT,
    -- Type du cap_act déterminé par la table `types_capteurs`, non unique et ne peut être nul 
    id_type_capteur             INTEGER NOT NULL,
    -- Référence commerciale, limitée à 255 caractères, non unique car plusieurs capteurs peuvent venir d'un même constructeur,
    -- et non nulle car un capteur provient forcément d'un constructeur
    reference_commerciale       TEXT NOT NULL,
    -- ID de la pièce à laquelle est associé le capteur, peut être nul car une pièce peut ne pas avoir de capteur
    id_piece                    INTEGER,
    -- Numéro du port avec lequel le capteur communique avec le serveur, peut être nul si pas attribué 
    port_communication_serveur  INTEGER,
    -- Date d'insertion du capteur dans la table
    date_insertion              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    --#-- Clé étrangère faisant référence au type du capteur d'après la table précédente
    FOREIGN KEY (id_type_capteur) REFERENCES types_capteurs(id),
    --#-- Clé étrangère faisant référence à la pièce à laquelle le capteur est associé (FK)
    FOREIGN KEY (id_piece) REFERENCES pieces(id)
);


-- Une mesure est réalisée par un capteur, elle possède une valeur dont l'unité/la dimension est renseignée dans la table dédiée.
CREATE TABLE mesures(
    -- ID de la mesure, unique, ne peut être nul (PK)
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    -- Valeur de la mesure, ne peut être nulle
    valeur          FLOAT NOT NULL,
    -- ID du capteur auquel est associée la mesure, ne peut être nul
    id_capteur      INTEGER NOT NULL,
    -- Date d'insertion du capteur dans la table
    date_insertion  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    --#-- Clé étrangère faisant référence au capteur auquel la mesure est associée (FK)
    FOREIGN KEY (id_capteur) REFERENCES capteurs(id)
);


--💡 Montrer toutes les tables existantes: `SHOW DATABASES;`


-- Qs.4 -
-- Ajouter un logement avec quatre pièces
INSERT INTO logements(adresse, numero_telephone, adresse_IP) VALUES ('4 place Jussieu 75005 Paris', '0607080910', '192.168.0.1'); 
INSERT INTO pieces(id_logement, nom, coordonnee_x, coordonnee_y, coordonnee_z) 
VALUES (1, 'salle_321', 3, 2, 1), (1, 'salle_327', 3, 2, 7), (1, 'salle_306', 3, 0, 6), (1, 'salle_305', 3, 0, 5);


-- Qs.5 -
-- Ajouter quatre types de capteurs/actionneurs
INSERT INTO types_capteurs(type_mesure, unite_mesure, plage_precision)
VALUES  ('humidite', '%', '[-1;+1]%'), 
        ('temperature_C', '°C', '[-2;+2]°C'), 
        ('temperature_K', '°K', '[-10;+10]°K'),
        ('temperature_F', '°F', '[-5;+5]°F');


-- Qs.6 -
-- Ajouter deux capteurs/actionneurs
INSERT INTO capteurs(id_type_capteur, reference_commerciale, port_communication_serveur, id_piece)
VALUES  (1, 'DHT', 1880, 1),
        (2, 'DHT', 1880, 2);


-- Qs.7 -
-- Ajouter deux mesures par capteur/actionneur
INSERT INTO mesures(valeur, id_capteur)
VALUES  (17, 1),
        (16, 1),
        (27.4, 2),
        (27.6, 2);


-- Qs.8 -
-- Ajouter quatre factures
INSERT INTO factures(id_logement, nom, montant, valeur_consommee)
VALUES  (1, 'Électricité', 50.00, 0.0),
        (1, 'Eau', 25.00, 0.0),
        (1, 'Chauffage', 12.50, 0.0),
        (1, 'Internet', 6.25, 0.0);