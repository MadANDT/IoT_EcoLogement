// Modifier la couleur de fond en fonction de l'heure
const currentHour = new Date().getHours();
const body = document.body;

if (currentHour >= 6 && currentHour < 12) {
    body.style.setProperty('--bg-color', '#FFECB3'); // Matin
} else if (currentHour >= 12 && currentHour < 18) {
    body.style.setProperty('--bg-color', '#FFD700'); // Après-midi
} else {
    body.style.setProperty('--bg-color', '#2C3E50'); // Soir
}