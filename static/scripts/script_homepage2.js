// Sélection des éléments du DOM
const circles = document.querySelectorAll('.circle');
const circleContainer = document.querySelector('.circle-container');

// Fonction qui réinitialise les cercles et le fond
function resetCirclesAndBackground() {
    circles.forEach(circle => {
        circle.classList.remove('not-hovered');
        circle.style.backgroundColor = '#A3B87D'; // Couleur initiale des cercles
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
        let backgroundGradient = '';
        if (this.id === 'home') {
            backgroundGradient = 'radial-gradient(circle, #A1B726, #98AB2D)'; // Dégradé pour "home"
        } else if (this.id === 'weather') {
            backgroundGradient = 'radial-gradient(circle, #86e1ff, #4ABFF7)'; // Dégradé pour "weather"
        } else if (this.id === 'documents') {
            backgroundGradient = 'radial-gradient(circle, #a6b3bc, #87959F)'; // Dégradé pour "documents"
        }
        // Appliquer le dégradé au fond de la page
        document.body.style.background = backgroundGradient;
        // Appliquer le même dégradé au cercle survolé
        this.style.background = backgroundGradient;

        this.classList.add('hovered');
        circles.forEach(otherCircle => {
            if (otherCircle !== this) {
                otherCircle.classList.add('not-hovered');
            }
        });
    });

    circle.addEventListener('mouseout', function() {
        resetCirclesAndBackground();
    });
});

// Créer un menu déroulant et un bouton d’envoi
const dropdownMenu = document.createElement('select');
dropdownMenu.id = 'dropdown-menu';
dropdownMenu.innerHTML = `
    <option value="">-- Choisissez une option --</option>
    <option value="option1">Option 1</option>
    <option value="option2">Option 2</option>
    <option value="option3">Option 3</option>
`;

const submitButton = document.createElement('button');
submitButton.id = 'submit-button';
submitButton.textContent = 'Envoyer';
submitButton.disabled = true; // Désactivé jusqu'à ce qu'une option soit choisie

// Fonction pour cacher les cercles sauf celui cliqué
function hideOtherCircles(clickedCircle) {
    circles.forEach(circle => {
        if (circle !== clickedCircle) {
            circle.style.display = 'none';
        }
    });
}

// Activer ou désactiver le bouton selon la sélection
dropdownMenu.addEventListener('change', () => {
    submitButton.disabled = dropdownMenu.value === '';
});

// Ajouter un événement de clic pour chaque cercle
circles.forEach(circle => {
    circle.addEventListener('click', function () {
        hideOtherCircles(this); // Cacher les autres cercles
        // this.style.display = 'none'; // Cacher le cercle cliqué

        // Afficher le menu déroulant et le bouton
        circleContainer.appendChild(dropdownMenu);
        circleContainer.appendChild(submitButton);
    });
});

// Ajouter un événement au bouton pour la redirection
submitButton.addEventListener('click', () => {
    if (dropdownMenu.value !== '') {
        window.location.href = `/newpage?selection=${dropdownMenu.value}`;
    }
});