document.addEventListener('DOMContentLoaded', function () {
  const montoInput = document.getElementById('monto');
  const descuentoInput = document.getElementById('descuento');
  const totalInput = document.getElementById('total');


  let montoOriginal = parseFloat(montoInput.value) || 0;


  montoInput.addEventListener('input', function () {
    montoOriginal = parseFloat(montoInput.value) || 0;
    calcularTotal();
  });


  descuentoInput.addEventListener('input', calcularTotal);

  function calcularTotal() {
    let descuento = parseFloat(descuentoInput.value);
    if (isNaN(descuento) || descuento < 0) descuento = 0;
    if (descuento > 100) descuento = 100;


    const totalCalculado = montoOriginal * (1 - descuento / 100);
    totalInput.value = totalCalculado.toFixed(2);
  }
});








