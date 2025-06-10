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

  
  const perfil = document.getElementById('perfil');
  const btnTogglePerfil = document.getElementById('btnTogglePerfil');

  if (btnTogglePerfil) {
    btnTogglePerfil.addEventListener('click', () => {
      if (perfil.style.display === 'none' || perfil.style.display === '') {
        perfil.style.display = 'flex';
      } else {
        perfil.style.display = 'none';
      }
    });
  }
});







  