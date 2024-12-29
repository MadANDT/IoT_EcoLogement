// Récupération des logements depuis l'API
fetch('/accueil/logements/')
    .then(response => response.json())
    .then(data => {
        const select = document.getElementById('logement-select');
        select.innerHTML = ''; // Vider le contenu par défaut
        data.forEach(logement => {
            const option = document.createElement('option');
            option.value = logement;
            option.textContent = logement;
            select.appendChild(option);
        });
    })
    .catch(error => console.error('Erreur lors du chargement des logements:', error));