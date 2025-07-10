$(document).ready(function () {
  $("#formServicio").submit(function (e) {
    let errores = "";
    let descripcion = $("textarea[name='descripcion']").val();
    let duracion = parseInt($("input[name='duracion']").val());

    if (descripcion.length > 200) {
      errores += "La descripción no puede superar los 200 caracteres.<br>";
    }

    if (isNaN(duracion) || duracion < 1 || duracion > 500) {
      errores += "La duración debe estar entre 1 y 500 minutos.<br>";
    }

    if (errores) {
      e.preventDefault();
      $("#mensajes").html(errores);
    } else {
      $("#mensajes").html("");
    }
  });
});
