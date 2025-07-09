var expr = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])+$/;
var expr1 = /((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,20})/;

$(document).ready(function () {
  $("#registrof").submit(function (e) {
    let mensajesMostrar = "";
    let entrar = false;

    var nombre = $("#nombreregistro").val();
    if (nombre.trim().length < 4 || nombre.trim().length > 9) {
      mensajesMostrar += "• La longitud del nombre no es correcta (min 4, max 9)<br>";
      entrar = true;
    }

    var celular = $("#celularregistro").val();
    if (!/^[9][0-9]{7,9}$/.test(celular)) {
      mensajesMostrar += "• El número debe comenzar con 9 y tener entre 8 y 10 dígitos.<br>";
      entrar = true;
    }

    var letrainicial = nombre.charAt(0);
    if (!esMAYUSCULA(letrainicial)) {
      mensajesMostrar += "• La primera letra del nombre debe ser mayúscula.<br>";
      entrar = true;
    }

    var apellido = $("#apellidoregistro").val();
    if (apellido.trim().length < 4 || apellido.trim().length > 12) {
      mensajesMostrar += "• La longitud del apellido no es correcta (min 4, max 12)<br>";
      entrar = true;
    }

    var letrainicial1 = apellido.charAt(0);
    if (!esMAYUSCULA(letrainicial1)) {
      mensajesMostrar += "• La primera letra del apellido debe ser mayúscula.<br>";
      entrar = true;
    }

    var correoderegistro = $("#registrocorreo").val();
    if (correoderegistro == "" || !expr.test(correoderegistro)) {
      mensajesMostrar += "• El correo debe tener formato válido (ej: usuario@gmail.com)<br>";
      entrar = true;
    }

    var contraseña = $("#contraseñaregistro").val();
    if (contraseña == "" || !expr1.test(contraseña)) {
      mensajesMostrar += "• La contraseña debe tener 8-20 caracteres, incluir mayúsculas, minúsculas, números y símbolos.<br>";
      entrar = true;
    }

    var letrainicial2 = contraseña.charAt(0);
    if (!esMAYUSCULA(letrainicial2)) {
      mensajesMostrar += "• La primera letra de la contraseña debe ser mayúscula.<br>";
      entrar = true;
    }

    var contraseñaconfirmar = $("#confirmarcontraseñaregistro").val();
    if (contraseñaconfirmar != contraseña) {
      mensajesMostrar += "• Las contraseñas no coinciden.<br>";
      entrar = true;
    }

    if (entrar) {
      e.preventDefault();
      $("#mensajes").html(
        `<div class="alert alert-danger alert-dismissible fade show" role="alert">
          <i class="bi bi-exclamation-circle"></i> <strong>Errores encontrados:</strong><br>${mensajesMostrar}
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button>
        </div>`
      );
    } else {
      $("#mensajes").html(
        `<div class="alert alert-success alert-dismissible fade show" role="alert">
          <i class="bi bi-check-circle"></i> ¡Formulario enviado correctamente!
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button>
        </div>`
      );
    }
  });

  function esMAYUSCULA(letra) {
    return letra == letra.toUpperCase();
  }
});
