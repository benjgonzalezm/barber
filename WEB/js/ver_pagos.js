const tabla = document.getElementById("tablaPagos");

const pagosEjemplo = [
  {
    cliente: "Juan Pérez",
    barbero: "Carlos Soto",
    servicio: "Corte Clásico",
    fecha_pago: "2025-05-10",
    forma_pago: "Efectivo",
    monto: 10000,
    descuento: 2000,
    total: 8000
  }
];

pagosEjemplo.forEach(pago => {
  const fila = document.createElement("tr");
  fila.innerHTML = `
    <td>${pago.cliente}</td>
    <td>${pago.barbero}</td>
    <td>${pago.servicio}</td>
    <td>${pago.fecha_pago}</td>
    <td>${pago.forma_pago}</td>
    <td>${pago.monto}</td>
    <td>${pago.descuento}</td>
    <td>${pago.total}</td>
    <td>
      <button onclick="editarPago()">Editar</button>
      <button onclick="eliminarPago()">Eliminar</button>
    </td>
  `;
  tabla.appendChild(fila);
});

function editarPago() {
  alert("Función de edición (a implementar)");
}

function eliminarPago() {
  alert("Función de eliminación (a implementar)");
}
