// Load the Visualization API and the corechart package.
google.charts.load('current', {'packages':['corechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(drawChart);

// Callback that creates and populates a data table,
// instantiates the pie chart, passes in the data and
// draws it.
function drawChart(){
    // Lire les données injectées dans la balise <script> avec l'id "factures_tronquees"
  const facturesDataElement = document.getElementById("factures_tronquees");
  const factures = JSON.parse(facturesDataElement.textContent);

  //var factures = JSON.parse('{{ factures_tronquees | tojson | safe }}')

  // Create the data table.
  const categories_factures = ["Eau", "Electricite", "Chauffage", "Gaz", "Internet", "Telephonie"];
  const consommations_categories = {};
  factures.forEach(facture => {
    if (categories_factures.includes(facture.nom)){     // si le type de facture fait partie de ceux renseignés
        if (!consommations_categories[facture["nom"]]){   // si sa valeur consommée n'est pas renseignée: initialisation
            consommations_categories[facture["nom"]] = 0;
        }
        consommations_categories[facture["nom"]] += facture.valeur_consommee;
    }
  })

//   data.addColumn('string', 'Type de facture');
//   data.addColumn('number', 'Valeur consommée (en €)');
//   consommations_categories.forEach(function(facture){
//     data.addRow([facture.nom, facture.valeur_consommee]);
//   });
  // Convertir les données agrégées en tableau pour Google Charts
  const chartData = Object.entries(consommations_categories);

  // Créer la table de données pour Google Charts
  const data = new google.visualization.DataTable();
  data.addColumn('string', 'Type de facture');
  data.addColumn('number', 'Valeur consommée (en €)');
  chartData.forEach(([nom, valeur]) => {
    data.addRow([nom, valeur]);
  });


  // Set chart options
  var options = {'title':'Répartition des consommations par facture du bâtiment #@@@',
                 'width':600,
                 'height':400,
                 'is3D': true};

  // Instantiate and draw our chart, passing in some options.
  var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
  chart.draw(data, options);
}