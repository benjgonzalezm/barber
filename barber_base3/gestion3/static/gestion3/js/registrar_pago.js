document.addEventListener("DOMContentLoaded", function() {
    const data = window.pagoData;


    const monto = parseFloat(data.montoOriginal.replace(',', '.'));

    // Cliente
    document.getElementById('cliente_visible').innerHTML = `<option value="${data.clienteId}" selected>${data.clienteNombre}</option>`;
    document.getElementById('cliente').value = data.clienteId;

    // Barbero
    document.getElementById('barbero_visible').innerHTML = `<option value="${data.barberoId}" selected>${data.barberoNombre}</option>`;
    document.getElementById('barbero').value = data.barberoId;

    // Servicio
    document.getElementById('servicio_visible').innerHTML = `<option value="${data.servicioId}" selected>${data.servicioNombre}</option>`;
    document.getElementById('servicio').value = data.servicioId;

    // Cita
    document.getElementById('cita_visible').innerHTML = `<option value="${data.citaId}" selected>Cita ${data.citaId}</option>`;
    document.getElementById('cita').value = data.citaId;

    // Fecha de pago
    document.getElementById('fecha_pago').value = data.fechaPago;
    document.getElementById('fecha_pago').readOnly = true;

    // Monto
    document.getElementById('monto').value = monto.toFixed(2);
    document.getElementById('monto').readOnly = true;

    // Total inicial
    document.getElementById('total').value = monto.toFixed(2);
    document.getElementById('total').readOnly = true;

    // Descuento dinámico
    document.getElementById('descuento').addEventListener('input', function () {
        const descuento = parseFloat(this.value) || 0;
        const totalCalculado = monto * (1 - descuento / 100);
        document.getElementById('total').value = totalCalculado.toFixed(2);
    });
});




