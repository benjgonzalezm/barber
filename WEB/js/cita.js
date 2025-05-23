document.addEventListener("DOMContentLoaded", () => {
  const citas = document.querySelectorAll(".cita");

  citas.forEach(cita => {
    const estadoP = Array.from(cita.querySelectorAll("p")).find(p => p.textContent.toLowerCase().includes("estado:"));
    if (!estadoP) return;

    // Función para actualizar botones según estado actual
    function actualizarBotones() {
      botonesContainer.innerHTML = "";

      const estadoText = estadoP.textContent.replace(/estado:/i, "").trim().toLowerCase();

      if (estadoText === "finalizado") {
        // Botón Registrar que redirige
        const btnRegistrar = document.createElement("a");
        btnRegistrar.classList.add("btn-registrar");
        btnRegistrar.textContent = "Registrar";
        btnRegistrar.href = "registro_pagos.html";
        botonesContainer.appendChild(btnRegistrar);
      } else if (estadoText === "activa") {
        // Botón Finalizar
        const btnFinalizar = document.createElement("a");
        btnFinalizar.classList.add("btn-registrar");
        btnFinalizar.style.backgroundColor = "#28a745"; // Verde
        btnFinalizar.textContent = "Finalizar";

        // Botón Cancelar
        const btnCancelar = document.createElement("a");
        btnCancelar.classList.add("btn-registrar");
        btnCancelar.style.backgroundColor = "#dc3545"; // Rojo
        btnCancelar.textContent = "Cancelar";

        botonesContainer.appendChild(btnFinalizar);
        botonesContainer.appendChild(btnCancelar);

        btnFinalizar.addEventListener("click", () => {
          // Cambiar estado a Finalizado (texto y clase)
          estadoP.innerHTML = "<strong>Estado:</strong> Finalizado";
          cita.classList.remove("activa");
          cita.classList.add("finalizada");
          // Agregar sección calificación vacía (opcional)
          if (!cita.querySelector(".calificacion")) {
            const divCalif = document.createElement("div");
            divCalif.classList.add("calificacion");
            divCalif.innerHTML = `<span class="estrella positiva">&#9733;&#9733;&#9733;&#9733;&#9733;</span><p><strong>Observaciones:</strong> </p>`;
            cita.insertBefore(divCalif, botonesContainer);
          }
          actualizarBotones();
        });

        btnCancelar.addEventListener("click", () => {
          // Cambiar estado a Rechazado (texto y clase)
          estadoP.innerHTML = "<strong>Estado:</strong> Rechazado";
          cita.classList.remove("activa");
          cita.classList.add("rechazado");
          // Eliminar sección calificación si existe
          const calif = cita.querySelector(".calificacion");
          if (calif) calif.remove();
          actualizarBotones();
        });
      } else {
        // Para otros estados no mostrar botones
        botonesContainer.innerHTML = "";
      }
    }

    const botonesContainer = cita.querySelector(".botones");
    if (!botonesContainer) return;

    actualizarBotones();
  });
});
  