function setEliminarProducto(productoId){
    document.getElementById('producto_id').value = productoId
    console.log(productoId)
}

document.addEventListener('DOMContentLoaded', function () {
    const editModal = document.getElementById('modalEditarProducto');

    if (editModal) {
        editModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;

            const id = button.getAttribute('data-id');
            const nombre = button.getAttribute('data-nombre');
            const precio = parseFloat(button.getAttribute('data-precio')).toFixed(2);
            const disponibilidad = button.getAttribute('data-disponibilidad');
            const descripcion = button.getAttribute('data-descripcion');

            document.getElementById('edit_producto_id').value = id;
            document.getElementById('edit_nombre_producto').value = nombre;
            document.getElementById('edit_precio_producto').value = precio;
            document.getElementById('edit_descripcion_producto').value = descripcion;

            const disponibilidadSelect = document.getElementById('edit_disponibilidad_producto');

            if (disponibilidad === 'True') {
                disponibilidadSelect.value = 'True';
            } else if (disponibilidad === 'False') {
                disponibilidadSelect.value = 'False';
            }
        });
    }
});

