document.addEventListener('DOMContentLoaded', function () {
    // Mostrar u ocultar detalles de tarjeta según el método de pago seleccionado
    document.querySelectorAll('input[name="metodoPago"]').forEach(function (radio) {
        radio.addEventListener('change', function () {
            var metodoPago = document.querySelector('input[name="metodoPago"]:checked').value;
            var tarjetaDetalles = document.getElementById('tarjetaDetalles');

            if (metodoPago === 'tarjeta') {
                tarjetaDetalles.classList.remove('d-none');
            } else {
                tarjetaDetalles.classList.add('d-none');
            }
        });
    });

    // Cargar direcciones al abrir el modal
    document.getElementById('modalPago').addEventListener('show.bs.modal', function () {
        const direccionSelect = document.getElementById('direccionSeleccionada');

        // Realizar la solicitud AJAX para obtener las direcciones
        fetch('/api/direcciones/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la solicitud: ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                console.log('Datos recibidos:', data); // Verificar datos recibidos en la consola.

                // Limpiar el select antes de agregar nuevas opciones
                direccionSelect.innerHTML = '<option value="">Selecciona una dirección</option>';

                // Agregar las direcciones al select
                data.forEach(direccion => {
                    const option = document.createElement('option');
                    option.value = direccion.id_direccion;
                    option.textContent = `${direccion.nombre_direccion}, ${direccion.calle} ${direccion.numero_casa}, ${direccion.municipio}, ${direccion.departamento}`;
                    direccionSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error al cargar direcciones:', error);
                alert('Hubo un problema al cargar las direcciones. Inténtalo de nuevo más tarde.');
            });
    });

    // Función para mostrar el Toast
    function mostrarToast() {
        var toastEl = new bootstrap.Toast(document.getElementById('toastMessage'));
        toastEl.show();
    }


    // Realizar el pago y mostrar el Toast
    document.getElementById('realizarPagoBtn').addEventListener('click', function () {
        var metodoPago = document.querySelector('input[name="metodoPago"]:checked').value;
        var direccionSeleccionada = document.getElementById('direccionSeleccionada').value;

        let totalPagoElement = document.getElementById('totalPago')
        var totalPago = parseFloat(totalPagoElement.textContent.replace(/[^0-9.]/g, ''));
        if (!totalPagoElement) {
            alert('No se pudo obtener el total del pago.');
            return;
        }
        var totalPago = parseFloat(totalPagoElement.textContent.replace('Total: $', '').trim());

        if (!direccionSeleccionada) {
            alert('Por favor, selecciona una dirección');
            return;
        }

        
        // Obteniendo IDS PRODUCTOS Y CANTIDAD
        let ids_productos = document.querySelectorAll('.id_pedido_detalle');
        let cantidad_productos = document.querySelectorAll('.id_cantidad');

        let cantidad = []
        let ids = []

        ids_productos.forEach(function(input){
            ids.push(input.value);
        })

        cantidad_productos.forEach(function(input){
            cantidad.push(input.value)
        })

        //FIN DE OBTENER IDS PRODUCTOS Y CANTIDAD

        fetch('/registrar_pedido/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({
                metodoPago: metodoPago,
                direccionSeleccionada: direccionSeleccionada,
                total: totalPago,
                ids: ids,
                cantidad: cantidad
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.mensaje) {
                // Cerrar el modal
                var modalPago = bootstrap.Modal.getInstance(document.getElementById('modalPago'));
                modalPago.hide(); // Cierra el modal

                // Crear y mostrar el toast de éxito
                var toastElement = document.createElement('div');
                toastElement.classList.add('toast', 'align-items-center', 'text-bg-success', 'border-0');
                toastElement.setAttribute('role', 'alert');
                toastElement.setAttribute('aria-live', 'assertive');
                toastElement.setAttribute('aria-atomic', 'true');
                toastElement.innerHTML = `
                    <div class="d-flex">
                        <div class="toast-body">
                            <strong>¡Pedido Realizado!</strong> Tu pedido ha sido procesado con éxito. ¡Gracias por comprar con nosotros!
                        </div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>`;

                // Añadir el toast al body y mostrarlo
                document.body.appendChild(toastElement);
                var toast = new bootstrap.Toast(toastElement, { delay: 5000 });
                toast.show();

                // Redirigir a la página del carrito después de 5 segundos
                setTimeout(function() {
                    window.location.href = '/carrito/';
                }, 5000);
            } else {
                alert('Error: ' + (data.error || 'Error desconocido'));
            }
        })
        .catch(error => console.error('Error:', error));
    });
});



// Elementos HTML
const listaDescuentos = document.getElementById('listaDescuentos');
const totalPagoLabel = document.getElementById('totalPago'); 
const totalModalLabel = document.querySelector('#modalPago .totalModal'); 

// Total original desde la etiqueta
let totalOriginal = parseFloat(totalPagoLabel.textContent.replace(/[^0-9.]/g, '')) || 0;

// Cargar descuentos al abrir el modal
document.getElementById('modalPago').addEventListener('show.bs.modal', function () {
    fetch('/cliente/cupones')
        .then(response => response.json())
        .then(data => {
            listaDescuentos.innerHTML = '';  // Limpiar la tabla
            if (data.length > 0) {
                data.forEach(descuento => {
                    const fila = `
                    <tr data-id="${descuento.id_descuento}">
                        <td>${descuento.tipo_descuento}</td>
                        <td>${descuento.monto_descuento}%</td>
                        <td>${descuento.fecha_vencimiento}</td>
                        <td>
                            <button type="button" class="btn btn-dark aplicarDescuento" 
                                data-id="${descuento.id_descuento}" 
                                data-monto="${descuento.monto_descuento}">
                                Aplicar
                            </button>
                        </td>
                    </tr>`;
                    listaDescuentos.insertAdjacentHTML('beforeend', fila);
                });
            } else {
                listaDescuentos.innerHTML = `<tr><td colspan="4">No hay descuentos disponibles</td></tr>`;
            }
        })
        .catch(error => {
            console.error('Error al cargar descuentos:', error);
            alert('Hubo un problema al cargar los descuentos.');
        });
});

// Aplicar descuento al hacer clic en "Aplicar"
listaDescuentos.addEventListener('click', function (e) {
    if (e.target.classList.contains('aplicarDescuento')) {
        e.preventDefault();

        const boton = e.target;
        const idDescuento = boton.dataset.id;
        const montoDescuento = parseFloat(boton.dataset.monto) || 0;

        // Validar total válido
        if (isNaN(totalOriginal) || totalOriginal <= 0) {
            alert("Error: Total inválido");
            return;
        }

        // Calcular el nuevo total
        const totalConDescuento = totalOriginal - (totalOriginal * montoDescuento / 100);

        // Actualizar el total en la página principal y el modal
        totalPagoLabel.textContent = `Total a Cancelar: $${totalConDescuento.toFixed(2)}`;
        if (totalModalLabel) {
            totalModalLabel.textContent = `Total: $${totalConDescuento.toFixed(2)}`;
        }
        totalOriginal = totalConDescuento;

        // Deshabilitar el botón actual y eliminar la fila
        boton.disabled = true;
        boton.innerText = 'Descuento Aplicado';
        boton.closest('tr').remove();

        // Deshabilitar todos los botones restantes
        document.querySelectorAll('.aplicarDescuento').forEach(boton => {
            boton.disabled = true;
            boton.innerText = 'No Disponible';
        });

        console.log("Descuento aplicado:", montoDescuento, "Nuevo total:", totalConDescuento);

        // Eliminar de la base de datos
        fetch('/cliente/eliminar-descuento/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  
            },
            body: JSON.stringify({ id_descuento: idDescuento })
        })
        .then(response => response.json())
        .then(data => {
            if (data.mensaje) {
                console.log(data.mensaje);
            } else {
                console.error(data.error);
                alert('Error al eliminar el descuento.');
            }
        })
        .catch(error => {
            console.error('Error en la solicitud:', error);
            alert('Hubo un problema al eliminar el descuento.');
        });
    }
});

// Función para obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
  