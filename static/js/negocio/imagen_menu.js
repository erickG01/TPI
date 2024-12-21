function mostrarImagenMenu(nombre, descripcion, url) {
    Swal.fire({
        title: nombre,
        text: descripcion,
        imageUrl: url,
        imageWidth: 400,
        imageHeight: 200,
        imageAlt: 'Imagen Del Producto',
        confirmButtonColor: '#343a40',
    })
}

document.addEventListener('DOMContentLoaded', function () {
    const addToMenuButtons = document.querySelectorAll('.add-to-menu');
    const menuProductosList = document.getElementById('menu_productos');
    const productosSeleccionadosInput = document.getElementById('productos_seleccionados');

    let productosSeleccionados = [];

    addToMenuButtons.forEach(button => {
        button.addEventListener('click', function () {
            const productoId = button.getAttribute('data-id');
            const productoName = button.getAttribute('data-name');

            if (!productosSeleccionados.includes(productoId)) {
                productosSeleccionados.push(productoId);

                const li = document.createElement('li');
                li.className = 'list-group-item d-flex justify-content-between align-items-center';
                li.setAttribute('data-id', productoId);
                li.innerHTML = `
                    ${productoName}
                    <button class="btn btn-danger btn-sm remove-from-menu">Eliminar</button>
                `;

                menuProductosList.appendChild(li);
                productosSeleccionadosInput.value = productosSeleccionados.join(',');

                // Añadir evento para eliminar producto de la lista
                li.querySelector('.remove-from-menu').addEventListener('click', function () {
                    const index = productosSeleccionados.indexOf(productoId);
                    if (index !== -1) {
                        productosSeleccionados.splice(index, 1);
                        li.remove();
                        productosSeleccionadosInput.value = productosSeleccionados.join(',');
                    }
                });
            }
        });
    });
});