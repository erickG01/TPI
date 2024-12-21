// Inicializa el mapa
const map = L.map('map').setView([13.69294, -89.21819], 8); // Coordenadas de San Salvador
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

let marker;
let selectedData = {}; // Almacena los datos seleccionados

// Añade un marcador al hacer clic
map.on('click', function(e) {
    const { lat, lng } = e.latlng;

    // Si ya hay un marcador, se elimina
    if (marker) {
        map.removeLayer(marker);
    }

    marker = L.marker([lat, lng]).addTo(map);

    // Usar geocodificación inversa para obtener dirección
    fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`)
        .then((response) => response.json())
        .then((data) => {
            const { address } = data;
            selectedData.departamento = address.state || 'No disponible';
            selectedData.municipio =
                address.city || address.town || address.village || 'No disponible';

            // Mostrar los datos seleccionados en la consola para depuración
            console.log(`Departamento: ${selectedData.departamento}, Municipio: ${selectedData.municipio}`);
        })
        .catch((err) => {
            console.error(err);
            alert('No se pudo obtener la dirección.');
        });
});

// Confirmar la ubicación seleccionada
document.getElementById('confirmLocation').addEventListener('click', () => {
    if (!marker) {
        alert('Por favor, selecciona un punto en el mapa.');
        return;
    }

    // Almacenar en localStorage
    localStorage.setItem('departamento', selectedData.departamento);
    localStorage.setItem('municipio', selectedData.municipio);

    // Obtener el parámetro "next" de la URL
    const urlParams = new URLSearchParams(window.location.search);
    const nextUrl = urlParams.get('next');

    if (nextUrl) {
        // Redirigir a la URL proporcionada en "next"
        window.location.href = nextUrl;
    } else {
        alert('No se pudo determinar la URL de redirección.');
    }
});
