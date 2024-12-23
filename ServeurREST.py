# -- EI4 • IoT - TP 1 - Partie 2
# ANDRIATSILAVO Matteo - TP A
# /!\ Utilisation d'un environnement virtuel nommé `TP1`
# @Sources:
# • https://docs.python.org/3/library/datetime.html
# • https://stackoverflow.com/questions/24494182/how-to-read-the-last-record-in-sqlite-table
# • https://developers.google.com/chart?hl=fr
# • https://stackoverflow.com/questions/4161332/how-can-i-include-python-script-in-a-html-file
#TODO:
# 

from fastapi import FastAPI, Request        # Request ajoutée à l'étape 6
from pydantic import BaseModel
## 6 -----------------------------------------
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from templates import draw_3D_charts
## -------------------------------------------
import sqlite3
import datetime as DATE
import meteo_API
from operator import itemgetter

def connection_to_DB():
    # Ouverture/Initialisation de la base de donnee 
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row
    # c = conn.cursor()
    return conn

def get_table_last_row(table: str):
    """ Récupérer la dernière ligne de la table `table`"""
    conn = connection_to_DB()
    c = conn.cursor()
    last_line = c.execute(f"SELECT * FROM {table} ORDER BY id DESC LIMIT 1").fetchall()[0]
    conn.close()
    return last_line

# def get_types_capteurs_last_row():
#     """ Récupérer la dernière ligne de la table `types_capteurs`"""
#     conn = connection_to_DB()
#     c = conn.cursor()
#     last_line = c.execute(f"SELECT * FROM types_capteurs ORDER BY id DESC LIMIT 1").fetchall()[0]
#     conn.close()
#     return last_line

# ## 4 -----------------------------------------
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
# ## -------------------------------------------
class Logement(BaseModel):
    id:                 int = get_table_last_row("logements")['id'] + 1
    adresse:            str = ""
    numero_telephone:   str = ""
    adresse_ip:         str = ""
    date_insertion:     DATE.datetime = DATE.datetime.now().replace(microsecond = 0)

class Piece(BaseModel):
    id:                 int = get_table_last_row("pieces")['id'] + 1
    id_logement:        int
    nom:                str = ""
    coordonnee_x:       int = 0
    coordonnee_y:       int = 0
    coordonnee_z:       int = 0

class Facture(BaseModel):
    id:                 int = get_table_last_row("factures")['id'] + 1
    id_logement:        int
    nom:                str = ""
    montant:            float = 0.0
    valeur_consommee:   float
    date_emission:      DATE.datetime = DATE.datetime.now().replace(microsecond = 0)

class Capteur(BaseModel):
    id:                         int = get_table_last_row("capteurs")['id'] + 1
    id_type_capteur:            int
    reference_commerciale:      str = ""
    id_piece:                   int
    port_communication_serveur: str = ""
    date_insertion:             DATE.datetime = DATE.datetime.now().replace(microsecond = 0)

class Mesure(BaseModel):
    id:                 int = get_table_last_row("mesures")['id'] + 1
    valeur:             float = 0.0
    id_capteur:         int
    date_insertion:     DATE.datetime = DATE.datetime.now().replace(microsecond = 0)

class Type_Capteur(BaseModel):
    id:                 int = get_table_last_row("types_capteurs")['id'] + 1
    type_mesure:        str = ""
    unite_mesure:       str = ""
    plage_precision:    list[float, float] = [0.0, 0.0]
    autres_infos:       str = ""


## 1
app = FastAPI()
@app.get("/")
async def root():
    return {"message" : "Hello World\n\tWelcome to my API!"}

# Requête GET
# curl -X GET --verbose "http://localhost:8000/"
# -- à chaque modification du fichier, relancer: `fastapi dev <filename>`

# ## 2
# @app.get("/etudiants/{id}/nom/")
# async def nom_etudiant(id: int):
#     return f"{id + 3} : Dick Cionnaire"

# -- l'annotation faite au pramètre `id` (_: int) permet au décorateur (@) 
# de formater le type de l'entrée pour toujours avoir un entier sur FastAPI

# ## 3 
# @app.get("/etudiant/")
# async def param(id: int = 0, nom: str = ""):
#     return f"Étudiant n° {id}: {nom}."

# -- renseignement d'une valeur par défaut pour le(s) paramètre(s)

# ## 4
# @app.post("/test/")
# async def test_post(id: int):
#     return id
#     # return hex(id), ou int(id, 16)

# - 'h' as Header ; 'd' : Data
# - pour une donnée compliquée (ex: JSON payload), on la passe en 'd';
#  si elle est simple, elle passera en 'h'

# librairie `pydantic` == glue magique de POO : vérifier des accesseurs, getters, etc. 

# ## 5 
# @app.post("/items/")
# async def create_item(item: Item):
#     print(item)
#     return item

# - conversion entre JSON et objet Python
# - Error 422: Unprocessable Entity (paramètre d'entrée non respecté)

## 6 
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
# - nécessite d'ajouter un répertoire `static`
# - contient des éléments non modifiés, et qui seront réutilisés par FastAPI

templates = Jinja2Templates(directory="templates")

# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse(
#         request=request, name="item.html", context={"id": id}
#     )

# ======== Reprise du fichier ======== #

# Logements
@app.get("/logements/")
async def get_logements():
    conn = connection_to_DB()                                       # se connecter
    logements = conn.execute("SELECT * FROM logements").fetchall()  # requêter sur `logements`
    conn.close()                                                    # se déconnecter
    return [dict(logement) for logement in logements]               # renvoi sous forme de dictionnaire  

@app.post("/logements/")
async def add_logement(logement: Logement):
    conn = connection_to_DB()
    c = conn.cursor()
    c.execute(
        """INSERT INTO logements(adresse, numero_telephone, adresse_IP) VALUES (?, ?, ?)""",
        (logement.adresse, logement.numero_telephone, logement.adresse_ip)
    )
    conn.commit()
    logement_id = c.lastrowid
    conn.close()
    return {"id": logement_id, "message": "Ajout du logement effectué."}

# Pièces
@app.get("/pieces/")
async def get_pieces():
    conn = connection_to_DB()                                   
    pieces = conn.execute("SELECT * FROM pieces").fetchall()    # requêter sur `pieces`
    conn.close()
    return [dict(piece) for piece in pieces]

@app.post("/pieces/")
async def add_piece(piece: Piece):
    conn = connection_to_DB()
    c = conn.cursor()
    c.execute(
        """INSERT INTO pieces(id_logement, nom, coordonnee_x, coordonne_y, coordonnee_z) VALUES (?, ?, ?, ?, ?)""",
        (piece.id_logement, piece.nom, piece.coordonnee_x, piece.coordonnee_y, piece.coordonnee_z)
    )
    conn.commit()
    piece_id = c.lastrowid
    conn.close()
    return {"id": piece_id, "message": "Ajout de la pièce effectué."}

# Factures
@app.get("/factures/")
async def get_factures():
    conn = connection_to_DB()
    factures = conn.execute("SELECT * FROM factures").fetchall()    # requêter sur `factures`
    conn.close()
    return [dict(facture) for facture in factures]

# @app.get("/factures/donnees/")
# async def create_chart():
    
@app.get("/factures/diagramme/", response_class = HTMLResponse)
async def chart_page(request: Request):
    # Récupérons les factures de la base
    conn = connection_to_DB()
    factures = conn.execute("SELECT * FROM factures").fetchall()    # requêter sur `factures`
    conn.close()
    
    factures_tronquees = [{"nom": f["nom"], "valeur_consommee": f["valeur_consommee"]} for f in factures]


    # factures_tronquees =  [dict(facture) for facture in factures]
    # # Retenons uniquement les catégories intéressantes: id, id_logement, nom, valeur_consommee
    # for _ in factures_tronquees:
    #     if 'date_emission' in _:
    #         del _['date_emission']
    # draw_3D_charts.draw_3D_piechart(factures_tronquees)
    return templates.TemplateResponse("use_graphics.html", {"request": request, "factures_tronquees": factures_tronquees})

@app.post("/factures/")
async def add_facture(facture: Facture):
    conn = connection_to_DB()
    c = conn.cursor()
    c.execute(
        """INSERT INTO factures(id_logement, nom, montant, valeur_consommee) VALUES (?, ?, ?, ?)""",
        (facture.id_logement, facture.nom, facture.montant, facture.valeur_consommee)
    )
    conn.commit()
    facture_id = c.lastrowid
    conn.close()
    return {"id": facture_id, "message": "Ajout de la facture effectué."}


# Capteurs/Actionneurs
@app.get("/capteurs/")
async def get_capteurs():
    conn = connection_to_DB()
    capteurs = conn.execute("SELECT * FROM capteurs").fetchall()    # requêter sur `capteurs`
    conn.close()
    return [dict(capteur) for capteur in capteurs]

@app.post("/capteurs/")
async def add_capteur(capteur: Capteur):
    conn = connection_to_DB()
    c = conn.cursor()
    c.execute(
        """INSERT INTO capteurs(id_type_capteur, reference_commerciale, id_piece, port_communication_serveur) VALUES (?, ?, ?, ?)""",
        (capteur.id_type_capteur, capteur.reference_commerciale, capteur.id_piece, capteur.port_communication_serveur)
    )
    conn.commit()
    capteur_id = c.lastrowid
    conn.close()
    return {"id": capteur_id, "message": "Ajout du capteur effectué."}

# Mesures
@app.get("/mesures/")
async def get_mesures():
    conn = connection_to_DB()
    mesures = conn.execute("SELECT * FROM mesures").fetchall()  # requêter sur `mesures`
    conn.close()
    return [dict(mesure) for mesure in mesures]

@app.get("/mesures/meteo/", response_class=HTMLResponse)
async def afficher_tableau(request: Request):
    # Mettre en place les variables à passer au template
    data = meteo_API.retreive_weather_data()
    data_dict = meteo_API.formatting_weather_api_data(data)
    days_and_colors = [["Aujourd'hui (J + 0)",  "#2874A6"],
                       ["Demain (J + 1)",       "#2E86C1"],
                       ["Après-demain (J + 2)", "#2980B9"],
                       ["Dans 3 jours (J + 3)",                "#5499C7"],
                       ["Dans 4 jours (J + 4)",                "#7FB3D5"],
                       ["Dans 5 jours (J + 5)",                "#A9CCE3"],
                       ["Dans 6 jours (J + 6)",                "#E0F7FA"]]
    temperatures_max_min = []
    for r in range(7):  #parce qu'il y a setp jours t'as capté
        temp = data_dict[r * 24 + 1: (r + 1) * 24 + 1]
        temperatures_max_min.append([max(temp, key = itemgetter('temperature_2m'))['temperature_2m'], min(temp, key = itemgetter('temperature_2m'))['temperature_2m']])
    # Passer les données et la requête au template
    template_data = {"request":                 request, 
                     "data":                    data_dict, 
                     "days_and_colors":         days_and_colors, 
                     "temperatures_max_min":    temperatures_max_min,
                     "current_hour":            DATE.datetime.now().hour}
    print(f"heure actuelle: {template_data['current_hour']}")
    return templates.TemplateResponse("weather_forecast.html", template_data)

@app.post("/mesures/")
async def add_mesure(mesure: Mesure):
    conn = connection_to_DB()
    c = conn.cursor()
    c.execute(
        """INSERT INTO mesures(valeur, id_capteur) VALUES (?, ?)""",
        (mesure.valeur, mesure.id_capteur)
    )
    conn.commit()
    mesure_id = c.lastrowid
    conn.close()
    return {"id": mesure_id, "message": "Ajout de la mesure effectué."}

# Types de capteurs
@app.get("/types_capteurs/")
async def get_types_capteurs():
    conn = connection_to_DB()
    types_capteurs = conn.execute("SELECT * FROM types_capteurs").fetchall()    # requêter sur `types_capteurs`
    conn.close()
    return [dict(type_capteur) for type_capteur in types_capteurs]

@app.post("/types_capteurs/")
async def add_type_capteur(type_capteur: Type_Capteur):
    conn = connection_to_DB()
    c = conn.cursor()
    c.execute(
        """INSERT INTO types_capteurs(type_mesure, unite_mesure, plage_precision, autres_infos) VALUES (?, ?, ?, ?)""",
        (type_capteur.type_mesure, type_capteur.unite_mesure, type_capteur.plage_precision, type_capteur.autres_infos)
    )
    conn.commit()
    type_capteur_id = c.lastrowid
    conn.close()
    return {"id": type_capteur_id, "message": "Ajout de la pièce effectué."}

