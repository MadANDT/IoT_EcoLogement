// Sélection des éléments du DOM
const circles = document.querySelectorAll('.circle');
const texts = document.querySelectorAll('.text');

// Fonction qui réinitialise les cercles et le fond
function resetCirclesAndBackground() {
    circles.forEach(circle => {
        circle.classList.remove('not-hovered');
        circle.style.backgroundColor = '#3498db'; // Couleur initiale des cercles
    });
    texts.forEach(text => {
        text.style.display = 'none';
    });
    document.body.style.backgroundColor = ''; // Réinitialise le fond
}

// Ajout des événements de survol
circles.forEach(circle => {
    circle.addEventListener('mouseover', function() {
        resetCirclesAndBackground(); // Réinitialise avant de modifier l'état

        // Définir la couleur de fond en fonction de l'élément survolé
        let backgroundColor = '';
        if (this.id === 'home') {
            backgroundColor = '#ffefd5'; // Pêche
        } else if (this.id === 'weather') {
            backgroundColor =  '#f0f8ff'; // Bleu clair
        } else if (this.id === 'documents') {
            backgroundColor = '#a6b3bc'; // Gris clair 
        }

        // Appliquer la couleur de fond à la page
        document.body.style.backgroundColor = backgroundColor;

        // Appliquer la même couleur de fond au cercle survolé
        this.style.backgroundColor = backgroundColor;

        this.classList.add('hovered');
        circles.forEach(otherCircle => {
            if (otherCircle !== this) {
                otherCircle.classList.add('not-hovered');
            }
        });
        // Affichage de la zone de texte
        this.querySelector('.text').style.display = 'block';
    });

    circle.addEventListener('mouseout', function() {
        resetCirclesAndBackground();
    });

    // Ajout d'un événement de clic qui redirige vers une autre page
    circle.addEventListener('click', function() {
        if (this.id === 'home') {
            window.location.href = '/accueil/logements/'; // Redirige vers housing.html (situé à /accueil/logements/)
        } else if (this.id === 'weather') {
            window.location.href = 'weather.html'; // Redirige vers weather.html
        } else if (this.id === 'documents') {
            window.location.href = 'documents.html'; // Redirige vers documents.html
        }
    });
});
