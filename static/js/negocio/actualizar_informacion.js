const confirmSaveButton = document.getElementById('confirmSave');
const form = document.getElementById('updateProfileForm');

confirmSaveButton.addEventListener('click', function () {
    if (form.checkValidity()) {
        form.submit();
    } else {
        alert("Por favor completa todos los campos requeridos.");
    }
});

const confirmModal = document.getElementById('confirmModal');
confirmModal.addEventListener('shown.bs.modal', () => {
    confirmModal.focus();
});