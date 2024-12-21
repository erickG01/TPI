$(function () {
    $("#pendientes").DataTable({
        "pageLength": 5,
        "language": {
            "emptyTable": "No hay información",
            "info": "Mostrando _START_ a _END_ de _TOTAL_ Pedidos",
            "infoEmpty": "Mostrando 0 a 0 de 0 Pedidos",
            "infoFiltered": "(Filtrado de MAX total Pedidos)",
            "infoPostFix": "",
            "thousands": ",",
            "lengthMenu": "Mostrar _MENU_ Pedidos",
            "loadingRecords": "Cargando...",
            "processing": "Procesando...",
            "search": "Buscador:",
            "zeroRecords": "Sin resultados encontrados",
            "paginate": {
                "first": "Primero",
                "last": "Ultimo"
            }
        },
        "responsive": true,
        "lengthChange": true,
        "autoWidth": false,
    });
});