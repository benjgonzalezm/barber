document.getElementById("formPago").addEventListener("submit", function (e) {
  e.preventDefault();

  // Asignar los valores de los campos visibles deshabilitados a los campos ocultos
  document.getElementById("cliente").value = document.getElementById("cliente_visible").value;
  document.getElementById("barbero").value = document.getElementById("barbero_visible").value;
  document.getElementById("servicio").value = document.getElementById("servicio_visible").value;
  document.getElementById("cita").value = document.getElementById("cita_visible").value;

  // Aquí iría la lógica para enviar a la base de datos, por ejemplo con fetch o AJAX

  alert("Pago registrado correctamente (aquí se enviaría a la BD).");
});
