// Charger la bibliothèque Google Charts
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(initChart);

document.addEventListener("DOMContentLoaded", () => {
    // Initialiser les valeurs par défaut
    initializeBills();

    // Ajouter des gestionnaires d'événements pour les sélecteurs d'échelle de temps
    const timeScaleSelectors = document.querySelectorAll(".time-scale");

    timeScaleSelectors.forEach((selector) => {
        selector.addEventListener("change", (event) => {
            const category = event.target.dataset.category;
            const timeScale = event.target.value;

            // Mettre à jour les montants et consommations pour la catégorie sélectionnée
            updateBill(category, timeScale);
        });
    });

    initChart()
});

/**
 * Initialise les factures avec les données par défaut (quotidien).
 */
function initializeBills() {
    for (const category of ["eau", "chauffage", "electricite"]) {
        updateBill(category, "quotidien");
    }
}

/**
 * Met à jour le montant et la consommation pour une catégorie donnée et une échelle de temps.
 * @param {string} category - Nom de la catégorie (eau, chauffage, electricite).
 * @param {string} timeScale - Échelle de temps (quotidien, hebdomadaire, mensuel).
 */
function updateBill(category, timeScale) {
    // Récupérer la facture correspondante
    const selectedBill = bills[timeScale][category];
    // Mettre à jour les éléments HTML
    const montantElement = document.getElementById(`montant-${category}`);
    const consommationElement = document.getElementById(`consommation-${category}`);
    if (!selectedBill) {
        console.error(`Données manquantes pour ${category} à l'échelle ${timeScale}`);
        montantElement.innerHTML = `<strong>Montant :</strong> (donnée indisponible...)`;
        consommationElement.innerHTML = `<strong>Consommation :</strong> (donnée indisponible...)`;
        return;
    }else {
        montantElement.innerHTML = `<strong>Montant :</strong> ${selectedBill.montant.toFixed(2)} €`;
        if (category === "eau"){
            consommationElement.innerHTML = `<strong>Consommation :</strong> ${selectedBill.valeur_consommee.toFixed(2)} L`;    
        }else{
            consommationElement.innerHTML = `<strong>Consommation :</strong> ${selectedBill.valeur_consommee.toFixed(2)} kWh`;
        }
    }
}

// Retour vers la page d'accueil
const logo = document.getElementById("logo");
logo.addEventListener('click', () => {
    window.location.href = `/accueil/`;
});


// Données passées depuis Python
// const bills = {{ factures|tojson }};
let selectedScale = 'quotidien'; // Échelle de temps par défaut
function initChart() {
    drawChart(selectedScale); // Dessiner le graphique avec l'échelle par défaut
}

function drawChart(scale) {
    const data = bills[scale];
    const chartData = google.visualization.arrayToDataTable([
        ['Catégorie', 'Montant (€)'],
        ['Chauffage', data['chauffage']['montant']],
        ['Eau', data['eau']['montant']],
        ['Électricité', data['electricite']['montant']]
    ]);
    const options = {
        title: `Répartition du coût des factures (${scale})`,
        is3D: true,
        pieSliceText: 'value',
        chartArea: {width: '80%', height: '80%'},
        titleTextStyle: {
            fontSize: 50, // Taille de la police
            bold: true, // Gras
            color: '#333', // Couleur
            fontName: 'Sans-serif' // Police
        }
    };
    const chart = new google.visualization.PieChart(document.getElementById('chart_div'));
    chart.draw(chartData, options);
}

// Fonction pour gérer les changements d'échelle
function changeScale(newScale) {
    selectedScale = newScale; // Mettre à jour l'échelle sélectionnée
    drawChart(selectedScale); // Redessiner le graphique
}
