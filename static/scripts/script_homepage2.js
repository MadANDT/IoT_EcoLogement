// // Sélection des éléments du DOM
// const circles = document.querySelectorAll('.circle');
// const texts = document.querySelectorAll('.text');

// // Fonction qui réinitialise les cercles et le fond
// function resetCirclesAndBackground() {
//     circles.forEach(circle => {
//         circle.classList.remove('not-hovered');
//         circle.style.backgroundColor = '#3498db'; // Couleur initiale des cercles
//     });
//     texts.forEach(text => {
//         text.style.display = 'none';
//     });
//     document.body.style.backgroundColor = ''; // Réinitialise le fond
// }

// // Ajout des événements de survol
// circles.forEach(circle => {
//     circle.addEventListener('mouseover', function() {
//         resetCirclesAndBackground(); // Réinitialise avant de modifier l'état

//         // Définir la couleur de fond en fonction de l'élément survolé
//         let backgroundColor = '';
//         if (this.id === 'home') {
//             backgroundColor = '#ffefd5'; // Pêche
//         } else if (this.id === 'weather') {
//             backgroundColor =  '#f0f8ff'; // Bleu clair
//         } else if (this.id === 'documents') {
//             backgroundColor = '#a6b3bc'; // Gris clair 
//         }

//         // Appliquer la couleur de fond à la page
//         document.body.style.backgroundColor = backgroundColor;

//         // Appliquer la même couleur de fond au cercle survolé
//         this.style.backgroundColor = backgroundColor;

//         this.classList.add('hovered');
//         circles.forEach(otherCircle => {
//             if (otherCircle !== this) {
//                 otherCircle.classList.add('not-hovered');
//             }
//         });
//         // Affichage de la zone de texte
//         this.querySelector('.text').style.display = 'block';
//     });

//     circle.addEventListener('mouseout', function() {
//         resetCirclesAndBackground();
//     });

//     // Ajout d'un événement de clic qui redirige vers une autre page
//     circle.addEventListener('click', function() {
//         if (this.id === 'home') {
//             window.location.href = '/accueil/logements/'; // Redirige vers housing.html (situé à /accueil/logements/)
//         } else if (this.id === 'weather') {
//             window.location.href = 'weather.html'; // Redirige vers weather.html
//         } else if (this.id === 'documents') {
//             window.location.href = 'documents.html'; // Redirige vers documents.html
//         }
//     });
// });
// Sélection des éléments du DOM
const circles = document.querySelectorAll('.circle');
const circleContainer = document.querySelector('.circle-container');

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
