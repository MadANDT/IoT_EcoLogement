// Retour vers la page d'accueil
const logo = document.getElementById("logo");
logo.addEventListener('click', () => {
    window.location.href = `/accueil/`;
});

// Gestion des éléments collapsibles
var coll = document.getElementsByClassName("collapsible");

for (var i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;

        content.style.width = `${this.offsetWidth}px`;

        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }
    });
}

// Gestion des boutons toggle pour les actionneurs
document.addEventListener("DOMContentLoaded", function() {
    const toggleButtons = document.querySelectorAll(".toggle-btn");
    toggleButtons.forEach(button => {
        button.addEventListener("click", async function() {
            const actuatorId = this.dataset.id; // ID de l'actionneur
            const actuatorType = parseInt(this.dataset.type); // Type d'actionneur
            let currentState = parseInt(this.dataset.state); // État actuel (1 = ON, 0 = OFF)

            // Bascule de l'état
            currentState = currentState === 1 ? 0 : 1;
            this.dataset.state = currentState;

            try {
                // Envoyer une requête au serveur pour mettre à jour l'état
                const response = await fetch("/logements/changement_etat_actionneur/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        actionneur_id: actuatorId,
                        nouvel_etat: currentState,
                    }),
                });

                if (response.ok) {
                    const data = await response.json();
                    console.log(`Actionneur ${data.id} changé à l'état ${data.new_state}`);

                    // Mettre à jour le texte de l'état
                    const stateText = document.getElementById(`state-${actuatorId}`);
                    stateText.textContent = currentState === 0 ? "OFF" : "ON";

                    // Mettre à jour l'image
                    const imgElement = document.getElementById(`img-${actuatorId}`);
                    let newImgSrc = "";

                    if ([11, 12].includes(actuatorType)) { // Fenêtres
                        newImgSrc = currentState === 0 ? "window_opened.svg" : "window_closed.svg";
                    } else if (actuatorType === 13) { // Débitmètres
                        newImgSrc = currentState === 0 ? "flow_meter_off.svg" : "flow_meter_on.svg";
                    } else if (actuatorType === 14) { // Éclairage
                        newImgSrc = currentState === 0 ? "light_off.svg" : "light_on.svg";
                    }

                    imgElement.src = `/static/images/housing_page/${newImgSrc}`;
                } else {
                    throw new Error("Échec du changement d'état de l'actionneur...");
                }
            } catch (error) {
                console.error(error);
                alert("Impossible de changer l'état de l'actionneur.");
            }
        });
    });
});

// Fonction pour récupérer les types de capteurs/actionneurs
async function fetchSensorTypes(roomId) {
    const sensorTypeMenu = document.getElementById('menu-sensor-types');
    const addButton = document.getElementById('add-sensor-btn');

    // Réinitialisation des menus et du bouton
    sensorTypeMenu.innerHTML = '<option value="">• Choisir un type de capteur/actionneur</option>';
    sensorTypeMenu.disabled = true;
    addButton.disabled = true;

    if (!roomId) return; // Si aucune salle n'est sélectionnée, on ne fait rien

    try {
        // Appel à l'API pour récupérer les types de capteurs/actionneurs
        const response = await fetch(`/types_capteurs/`);
        if (!response.ok) {
            throw new Error('Erreur lors de la récupération des types de capteurs/actionneurs.');
        }
        const sensorTypes = await response.json();

        // Ajout des options au menu déroulant
        sensorTypes.forEach((type) => {
            const option = document.createElement('option');
            option.value = type.id;

            // Construire le contenu de l'option
            const typeDescription = type.cap_ou_act === 1 
                ? "actionneur" 
                : `capteur, ${type.type_mesure || ''} ${type.unite_mesure || ''} ${type.plage_precision || ''}`.trim();

            option.textContent = `${type.id}) ${type.reference_commerciale} [${typeDescription}] - Brève description: ${type.autres_infos || ''}`;
            sensorTypeMenu.appendChild(option);
        });

        sensorTypeMenu.disabled = false; // Activer le menu des types
    } catch (error) {
        console.error(error);
        alert('Impossible de récupérer les types de capteurs/actionneurs.');
    }
}

// Fonction pour ajouter un capteur/actionneur
async function addSensor() {
    const roomId = document.getElementById('menu-rooms').value;
    const sensorTypeId = document.getElementById('menu-sensor-types').value;

    if (!roomId || !sensorTypeId) {
        alert('Veuillez sélectionner une salle et un type de capteur/actionneur.');
        return;
    }

    try {
        // Appel à l'API pour ajouter le capteur/actionneur
        const response = await fetch('/ajouter_capteurs/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id_piece: roomId,
                id_type_capteur: sensorTypeId,
            }),
        });

        if (!response.ok) {
            throw new Error('Erreur lors de l’ajout du capteur/actionneur.');
        }

        alert('Capteur/actionneur ajouté avec succès. Rechargement de la page...');
        location.reload(); // Rechargement de la page pour mettre à jour l'affichage
    } catch (error) {
        console.error(error);
        alert('Impossible d’ajouter le capteur/actionneur.');
    }
}

// Activer ou désactiver le bouton d'ajout
document.getElementById('menu-rooms').addEventListener('change', (e) => {
    fetchSensorTypes(e.target.value);
});

document.getElementById('menu-sensor-types').addEventListener('change', (e) => {
    const addButton = document.getElementById('add-sensor-btn');
    addButton.disabled = !e.target.value;
});

