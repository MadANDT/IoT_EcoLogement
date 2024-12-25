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

document.addEventListener("DOMContentLoaded", function () {
  const toggleButton = document.getElementById("togglePastHours");
  const pastHourRows = document.querySelectorAll(".past-hour");

  toggleButton.addEventListener("click", function () {
      pastHourRows.forEach(row => {
          row.classList.toggle("hidden");
      });

      // Modifier le texte du bouton en fonction de l'état
      if (toggleButton.textContent === "Afficher toutes les prévisions") {
          toggleButton.textContent = "Masquer les heures passées";
      } else {
          toggleButton.textContent = "Afficher toutes les prévisions";
      }
  });
});