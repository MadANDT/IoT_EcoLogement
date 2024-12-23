from pygooglechart import PieChart3D
        
def draw_3D_piechart(tableau_factures):
    if tableau_factures != []:
        # initialise l'objet `Chart`, un camembert, de taille 500×500 pixels
        chart = PieChart3D(500, 500)

        noms_factures = []
        # ajoute des données correspondant aux labels du camembert
        dico_nature_somme_consommation = {}
        for t in tableau_factures:
            if t["nom"] not in noms_factures:
                noms_factures.append(t["nom"])
            if t["nom"] in dico_nature_somme_consommation:
                dico_nature_somme_consommation[t["nom"]] += t["valeur_consommee"]
            else:
                dico_nature_somme_consommation[t["nom"]] = t["valeur_consommee"]
        noms_factures.sort()
        chart.add_data([dico_nature_somme_consommation[nom] for nom in noms_factures])

        # ajoute des labels (noms des colonnes) au camembert
        chart.set_pie_labels([nom for nom in noms_factures])

        # télécharge le diagramme 
        chart.download('3D_diagramme_factures.png')

        # // Set chart options
        # var options = {'title':'How Much Pizza I Ate Last Night',
        #             'width':400,
        #             'height':300};

        # // Instantiate and draw our chart, passing in some options.
        # var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        # chart.draw(data, options);