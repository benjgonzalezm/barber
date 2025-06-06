document.addEventListener('DOMContentLoaded', () => {
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function cambiarEstado(userId, nuevaAccion) {
    fetch(`/usuarios/${userId}/${nuevaAccion}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({}),
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alert(`Usuario ${nuevaAccion} exitosamente.`);
          location.reload();  // Recarga la página para actualizar estado
        } else {
          alert('Error: ' + data.error);
        }
      })
      .catch(err => alert('Error en la petición: ' + err));
  }

  function eliminarUsuario(userId) {
    fetch(`/usuarios/${userId}/eliminar/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({}),
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alert('Usuario eliminado correctamente.');
          location.reload();
        } else {
          alert('Error: ' + data.error);
        }
      })
      .catch(err => alert('Error en la petición: ' + err));
  }

  document.querySelectorAll('.boton-bloquear').forEach(btn => {
    btn.addEventListener('click', () => {
      const userId = btn.getAttribute('data-id');
      if (confirm('¿Seguro que quieres bloquear este usuario?')) {
        cambiarEstado(userId, 'bloquear');
      }
    });
  });

  document.querySelectorAll('.boton-activar').forEach(btn => {
    btn.addEventListener('click', () => {
      const userId = btn.getAttribute('data-id');
      if (confirm('¿Seguro que quieres activar este usuario?')) {
        cambiarEstado(userId, 'activar');
      }
    });
  });

  document.querySelectorAll('.boton-eliminar').forEach(btn => {
    btn.addEventListener('click', () => {
      const userId = btn.getAttribute('data-id');
      if (confirm('¿Seguro que quieres eliminar este usuario?')) {
        eliminarUsuario(userId);
      }
    });
  });
});


