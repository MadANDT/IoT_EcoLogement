// // Récupération des logements depuis l'API
// fetch('/accueil/logements/')
//     .then(response => response.json())
//     .then(data => {
//         const select = document.getElementById('logement-select');
//         select.innerHTML = ''; // Vider le contenu par défaut
//         data.forEach(logement => {
//             const option = document.createElement('option');
//             option.value = logement;
//             option.textContent = logement;
//             select.appendChild(option);
//         });
//     })
//     .catch(error => console.error('Erreur lors du chargement des logements:', error));
var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    content.style.width = `${this.offsetWidth}px`;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
}