document.addEventListener("DOMContentLoaded", () => {
    // Variables globales
    const modal = document.getElementById("product-modal");
    const modalImg = document.getElementById("modal-img");
    const modalTitle = document.getElementById("modal-title");
    const modalDescription = document.getElementById("modal-description");
    const modalPrice = document.getElementById("modal-price");
    const addToCartBtn = document.getElementById("add-to-cart-btn");
    let currentProductId = null;

    // Carrusel
    const items = document.querySelectorAll('.carousel-item img');
    const carousel = document.querySelector('.carousel');
    const indicators = document.querySelectorAll('.carousel-indicators span');
    let currentIndex = 0;


    const updateActiveItem = () => {
        items.forEach((item, index) => {
            item.classList.toggle('active', index === currentIndex);
        });
        indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === currentIndex);
        });
    };

    const autoScroll = () => {
        setInterval(() => {
            currentIndex = (currentIndex + 1) % items.length;
            items[currentIndex].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
            updateActiveItem();
        },2000);
    };

    // Configurar el clic en los indicadores para cambiar de imagen
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
            currentIndex = index;
            items[currentIndex].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
            updateActiveItem();
        });
    });

    updateActiveItem();
    autoScroll();

    // Mostrar modal al hacer clic en una imagen
    items.forEach((item) => {
        item.addEventListener('click', () => {
            currentProductId = item.getAttribute("data-id"); // Guardar el ID del producto actual
            modalImg.src = item.src;
            modalTitle.textContent = item.getAttribute("data-nombre");
            modalDescription.textContent = item.getAttribute("data-descripcion");
            modalPrice.textContent = `Precio: $${item.getAttribute("data-precio")}`;
            modal.style.display = "flex";
        });
    });

    // Cerrar modal
    document.querySelector(".close-btn").addEventListener("click", () => {
        modal.style.display = "none";
    });

    // Agregar al carrito
    addToCartBtn.addEventListener("click", () => {
        if (currentProductId) {
            // Realizar una petición al backend
            fetch(`https://web-production-6242f.up.railway.app/carrito/agregar/${currentProductId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            })
                .then((response) => {
                    if (response.ok) {
                        mostrarAlerta('success',"Producto agregado al carrito.");
                        modal.style.display = "none";
                    } else {
                        mostrarAlerta('Error',"Error al agregar el producto al carrito.");
                    }
                })
                .catch((error) => console.error("Error:", error));
        }
    });

    // Obtener CSRF Token
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
});
function mostrarAlerta(tipo, mensaje) {
    Swal.fire({
      title: tipo === 'success' ? '¡Éxito!' : 'Error',
      text: mensaje,
      icon: tipo,
      confirmButtonText: 'Aceptar'
    });
  }
  

