function editarCupon(id_descuento,cliente, tipo, monto, estado, vencimiento) {
    document.getElementById('id_descuento_actualizar').value = id_descuento
    document.getElementById('correo_cliente_actualizar').value = cliente;
    document.getElementById('tipo_descuento_actualizar').value = tipo;
    document.getElementById('monto_descuento_actualizar').value = monto;
    document.getElementById('estado_descuento_actualizar').value = estado === "True" ? "True" : "False";
    document.getElementById('fecha_vencimiento_actualizado').value = vencimiento;
}
