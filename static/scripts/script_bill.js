// document.addEventListener("DOMContentLoaded", () => {
//     const timeScaleSelectors = document.querySelectorAll(".time-scale");
  
//     timeScaleSelectors.forEach((selector) => {
//       selector.addEventListener("change", (event) => {
//         const category = event.target.dataset.category;
//         const timeScale = event.target.value;
  
//         // Obtenir la facture correspondante dans la variable `factures`
//         const selectedBill = factures[timeScale][category];
//         //Vérifier que cette facture existe
//         if (!selectedBill) {
//             console.error(`Données manquantes pour ${category} à l'échelle ${timeScale}`);
//             return;
//         }

//         // Mettre à jour le contenu de la facture (montants et consommations)
//         // const billContentDiv = document.getElementById(`bill-${category}`);
//         if (selectedBill) {
//         //   billContentDiv.innerHTML = `
//         //     <p><strong>Montant :</strong> ${selectedBill.montant.toFixed(2)} €</p>
//         //     <p><strong>Consommation :</strong> ${selectedBill.valeur_consommee.toFixed(2)}</p>
//         //   `;
//             const montantElement = document.getElementById(`montant-${category}`);
//             const consommationElement = document.getElementById(`consommation-${category}`);
//             montantElement.innerHTML = `<strong>Montant :</strong> ${selectedBill.montant.toFixed(2)} €`;
//             consommationElement.innerHTML = `<strong>Consommation :</strong> ${selectedBill.valeur_consommee.toFixed(2)}`;
//         } else {
//           billContentDiv.innerHTML = "<p>Aucune donnée disponible.</p>";
//         }
//       });
//     });
//   });
  
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