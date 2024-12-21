function setMontoTotal(total) {
    document.getElementById('montoTotal').innerText = total.toFixed(2);
    document.getElementById('cantidadPagada').value = '';
    document.getElementById('cambio').innerText = '0.00';
    document.getElementById('cambioTexto').style.display = 'none';
    document.getElementById('efectivoInput').style.display = 'none';
}

function toggleEfectivoInput() {
    const formaPago = document.getElementById('formaPago').value;
    const efectivoInput = document.getElementById('efectivoInput');
    const cambioTexto = document.getElementById('cambioTexto');
    if (formaPago === 'efectivo') {
        efectivoInput.style.display = 'block';
    } else {
        efectivoInput.style.display = 'none';
        cambioTexto.style.display = 'none';
    }
}

function calcularCambio() {
    const total = parseFloat(document.getElementById('montoTotal').innerText);
    const cantidadPagada = parseFloat(document.getElementById('cantidadPagada').value);
    const cambio = cantidadPagada - total;
    if (cambio >= 0) {
        document.getElementById('cambio').innerText = cambio.toFixed(2);
        document.getElementById('cambioTexto').style.display = 'block';
    } else {
        document.getElementById('cambioTexto').style.display = 'none';
    }
}

function mostrarDetallePedido(productos) {
    const detalleProductos = document.getElementById('detalleProductos');
    detalleProductos.innerHTML = ''; // Limpiar contenido previo

    productos.forEach(producto => {
        const total = producto.cantidad * producto.precio;
        const row = `
            <tr>
                <td>${producto.nombre}</td>
                <td>${producto.cantidad}</td>
                <td>$${producto.precio.toFixed(2)}</td>
                <td>$${total.toFixed(2)}</td>
            </tr>
        `;
        detalleProductos.insertAdjacentHTML('beforeend', row);
    });
}
