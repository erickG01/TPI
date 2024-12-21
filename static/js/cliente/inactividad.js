let tiempoInactividad = 0;
const tiempoLimite = 3600000; // 5 minutos en milisegundos

function resetearTiempo() {
    tiempoInactividad = 0;
}

function verificarInactividad() {
    tiempoInactividad += 1000;
    if (tiempoInactividad >= tiempoLimite) {
        // Muestra el modal de advertencia con la opción de backdrop 'static'
        let modal = new bootstrap.Modal(document.getElementById('inactivityModal'), {
            backdrop: false, // No cierra el modal al hacer clic fuera de él
            keyboard: false     // No permite cerrar el modal con la tecla de escape
        });
        modal.show();
    }
}

// Detecta la actividad del usuario
window.onload = function() {
    document.onmousemove = resetearTiempo;
    document.onkeypress = resetearTiempo;
    document.onclick = resetearTiempo;
    document.onscroll = resetearTiempo;
    document.onkeydown = resetearTiempo;
};

// Verifica la inactividad cada segundo
setInterval(verificarInactividad, 1000);


// Evita que el modal se cierre al hacer clic fuera de él
document.querySelector('#inactivityModal').addEventListener('click', function(event) {
    if (event.target === this) {
        event.stopPropagation(); // Previene el cierre al hacer clic fuera del contenido del modal
    }
});
