document.addEventListener("DOMContentLoaded", async () => {
    const form = document.getElementById("claim-form");
    const descriptionField = document.getElementById("description");
    const tableBody = document.getElementById("claims-body");
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // Función para cargar los reclamos al cargar la página
    async function loadReclamos() {
        try {
            const response = await fetch("https://web-production-6242f.up.railway.app/gestionar-reclamos/");
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            if (data.reclamos) {
                updateTable(data.reclamos);
            }
        } catch (error) {
            console.error("Error al cargar los reclamos:", error);
        }
    }

    // Llama a loadReclamos al cargar la página
    await loadReclamos();

    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // Evita el envío del formulario tradicional

        const description = descriptionField.value.trim();
        if (!description) {
            alert("Por favor, ingresa una descripción para el reclamo.");
            return;
        }

        try {
            const response = await fetch("/gestionar-reclamos/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken, // Incluye el token CSRF
                },
                body: JSON.stringify({ description }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.error) {
                alert(data.error);
                return;
            }

            // Limpia el campo de texto después de enviar
            descriptionField.value = "";

            // Actualiza la tabla con los nuevos datos
            updateTable(data.reclamos);
        } catch (error) {
            console.error("Error al registrar el reclamo:", error);
            alert("Hubo un error al procesar tu reclamo. Intenta de nuevo.");
        }
    });

    // Función para actualizar la tabla con los últimos reclamos
    function updateTable(reclamos) {
        tableBody.innerHTML = ""; // Limpia el contenido de la tabla
        reclamos.forEach((reclamo, index) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${reclamo.descripcion_reclamo}</td>
                <td>${reclamo.fecha_reclamo}</td>
            `;
            tableBody.appendChild(row);
        });
    }
});



