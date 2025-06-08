document.addEventListener("DOMContentLoaded", () => {
  const tipoUsuario = document.body.dataset.tipoUsuario;
  const citas = document.querySelectorAll(".cita");

  citas.forEach(cita => {
    const estadoP = Array.from(cita.querySelectorAll("p")).find(p =>
      p.textContent.toLowerCase().includes("estado:")
    );
    if (!estadoP) return;

    const estado = estadoP.textContent.trim().toLowerCase();

    const botones = cita.querySelector(".botones");
    if (!botones) return;

    if (tipoUsuario === "Barbero" && estado.includes("en progreso")) {
      botones.innerHTML = `
        <a href="${cita.dataset.finalizar}" class="btn btn-success me-2">Finalizar</a>
        <a href="${cita.dataset.cancelar}" class="btn btn-danger">Cancelar</a>
      `;
    }
  });


  const btnTogglePerfil = document.getElementById('btnTogglePerfil');
  const perfilBarbero = document.getElementById('perfilBarbero');

  if (tipoUsuario === "Barbero" && btnTogglePerfil && perfilBarbero) {
    btnTogglePerfil.addEventListener('click', () => {
      if (perfilBarbero.style.display === 'none' || perfilBarbero.style.display === '') {
        perfilBarbero.style.display = 'flex';
      } else {
        perfilBarbero.style.display = 'none';
      }
    });
  }
});



  