$(function () {
    $("#example4").DataTable({
        "pageLength": 5,
        "language": {
            "emptyTable": "No hay información",
            "info": "Mostrando _START_ a _END_ de _TOTAL_ Menus",
            "infoEmpty": "Mostrando 0 a 0 de 0 Menus",
            "infoFiltered": "(Filtrado de MAX total Menus)",
            "infoPostFix": "",
            "thousands": ",",
            "lengthMenu": "Mostrar _MENU_ Menus",
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

document.addEventListener('DOMContentLoaded', () => {
    function mostrarDetalleMenu(idMenu) {
        fetch('http://127.0.0.1:8000/negocio/api/detalleMenu')
            .then(response => response.json())
            .then(data => {
                const detalles = data.detalle;
                const productos = data.productos;
                const menuProductsList = document.getElementById('menu-products');
                const menuIdElement = document.getElementById('menu-id');

                menuProductsList.innerHTML = '';

                const detallesMenu = detalles.filter(detalle => detalle.id_menu_id === idMenu);

                if (detallesMenu.length > 0) {
                    menuIdElement.textContent = idMenu;

                    detallesMenu.forEach(detalle => {
                        const producto = productos.find(p => p.id_producto === detalle.id_producto_id);
                        if (producto) {
                            const li = document.createElement('li');
                            li.classList.add('list-group-item');
                            li.textContent = producto.nombre_producto;
                            menuProductsList.appendChild(li);
                        }
                    });

                    const modal = new bootstrap.Modal(document.getElementById('menuDetailsModal'));
                    modal.show();
                } else {
                    alert('No se encontraron detalles para este menú.');
                }
            })
            .catch(error => {
                console.error('Error al obtener los datos:', error);
            });
    }

    document.querySelectorAll('.view-details').forEach(button => {
        button.addEventListener('click', (e) => {
            const idMenu = parseInt(e.target.getAttribute('data-id'), 10);
            mostrarDetalleMenu(idMenu);
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    // Asignar evento a cada botón de eliminar menú
    document.querySelectorAll('.btn-danger').forEach(button => {
        button.addEventListener('click', (e) => {
            const idMenu = e.target.getAttribute('data-id');
            document.getElementById('menuIdToDelete').value = idMenu;

            // Mostrar el modal de confirmación
            const modal = new bootstrap.Modal(document.getElementById('deleteConfirmModal'));
            modal.show();
        });
    });
});