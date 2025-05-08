// Ejemplo de script para cambiar el estado o calificación de la cita
document.addEventListener("DOMContentLoaded", () => {
    const citas = document.querySelectorAll(".cita");
  
    citas.forEach(cita => {
      if (cita.classList.contains("finalizada")) {
        const calificacion = cita.querySelector(".calificacion");
        calificacion.addEventListener("click", () => {
          alert("Cita finalizada. Calificación registrada.");
        });
      }
    });
  });
  