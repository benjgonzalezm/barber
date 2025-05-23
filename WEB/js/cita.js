document.addEventListener("DOMContentLoaded", () => {
  const citas = document.querySelectorAll(".cita");

  citas.forEach(cita => {
    const estadoP = Array.from(cita.querySelectorAll("p")).find(p => p.textContent.toLowerCase().includes("estado:"));
    if (!estadoP) return;

    function actualizarBotones() {
      botonesContainer.innerHTML = "";

      const estadoText = estadoP.textContent.replace(/estado:/i, "").trim().toLowerCase();

      if (estadoText === "finalizado") {
        const btnRegistrar = document.createElement("a");
        btnRegistrar.classList.add("btn-registrar");
        btnRegistrar.textContent = "Registrar";
        btnRegistrar.href = "registro_pagos.html";
        botonesContainer.appendChild(btnRegistrar);
      } else if (estadoText === "activa") {
        const btnFinalizar = document.createElement("a");
        btnFinalizar.classList.add("btn-registrar");
        btnFinalizar.style.backgroundColor = "#28a745";
        btnFinalizar.textContent = "Finalizar";

        const btnCancelar = document.createElement("a");
        btnCancelar.classList.add("btn-registrar");
        btnCancelar.style.backgroundColor = "#dc3545";
        btnCancelar.textContent = "Cancelar";

        botonesContainer.appendChild(btnFinalizar);
        botonesContainer.appendChild(btnCancelar);

        btnFinalizar.addEventListener("click", () => {
          estadoP.innerHTML = "<strong>Estado:</strong> Finalizado";
          cita.classList.remove("activa");
          cita.classList.add("finalizada");

          if (!cita.querySelector(".calificacion")) {
            const divCalif = document.createElement("div");
            divCalif.classList.add("calificacion");
            divCalif.innerHTML = `<span class="estrella positiva">&#9733;&#9733;&#9733;&#9733;&#9733;</span><p><strong>Observaciones:</strong> </p>`;
            cita.insertBefore(divCalif, botonesContainer);
          }
          actualizarBotones();
        });

        btnCancelar.addEventListener("click", () => {
          estadoP.innerHTML = "<strong>Estado:</strong> Rechazado";
          cita.classList.remove("activa");
          cita.classList.add("rechazado");
          const calif = cita.querySelector(".calificacion");
          if (calif) calif.remove();
          actualizarBotones();
        });
      } else {
        botonesContainer.innerHTML = "";
      }
    }

    const botonesContainer = cita.querySelector(".botones");
    if (!botonesContainer) return;

    actualizarBotones();
  });


  function togglePerfil() {
    const perfil = document.getElementById('perfilBarbero');
    perfil.style.display = (perfil.style.display === 'none' || perfil.style.display === '') ? 'flex' : 'none';
  }

  // un botón para abrir/cerrar perfil con id 'btnTogglePerfil'
  const btnTogglePerfil = document.getElementById('btnTogglePerfil');
  if (btnTogglePerfil) {
    btnTogglePerfil.addEventListener('click', togglePerfil);
  }
});

  