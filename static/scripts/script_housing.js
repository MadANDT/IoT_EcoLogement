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

document.addEventListener("DOMContentLoaded", function() {
  const toggleButtons = document.querySelectorAll(".toggle-btn");
  toggleButtons.forEach(button => {
      button.addEventListener("click", async function() {
          const actuatorId = this.dataset.id; // ID de l'actionneur
          const actuatorType = parseInt(this.dataset.type); // Type d'actionneur
          let currentState = parseInt(this.dataset.state); // État actuel (1 = ON, 0 = OFF)
          // Bascule
          currentState = currentState === 1 ? 0 : 1;
          this.dataset.state = currentState;
          // Envoyer une requête au serveur pour mettre à jour l'état, la route à utilise: "/..."
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
              stateText.textContent = currentState === 1 ? "ON" : "OFF";
              // Mettre à jour l'image
              const imgElement = document.getElementById(`img-${actuatorId}`);
              let newImgSrc = "";
              if ([11, 12].includes(actuatorType)) { // Fenêtres
                  newImgSrc = currentState === 1 ? "window_closed.svg" : "window_opened.svg";
              } else if (actuatorType === 13) { // Débitmètres
                  newImgSrc = currentState === 1 ? "flow_meter_on.svg" : "flow_meter_off.svg";
              } else if (actuatorType === 14) { // Éclairage
                  newImgSrc = currentState === 1 ? "light_on.svg" : "light_off.svg";
              }

              imgElement.src = `/static/images/housing_page/${newImgSrc}`;
          } else {
              console.error("Échec du changement d'état de l'actionneur...");
          }
      });
  });
});
