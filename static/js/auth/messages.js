  // Espera até que o DOM esteja carregado
  document.addEventListener("DOMContentLoaded", function () {
    const alertBox = document.getElementById("message-alert");
    if (alertBox) {
      setTimeout(function () {
        alertBox.classList.remove("show");
        alertBox.classList.add("fade");
        setTimeout(function () {
          alertBox.remove(); // Remove completamente do DOM
        }, 500); // Espera a animação de fade completar
      }, 4000); // Espera 4 segundos antes de desaparecer
    }
  });