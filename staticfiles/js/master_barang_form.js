document.addEventListener('DOMContentLoaded', function () {
    const tipeField = document.getElementById('id_tipe');
    const levelField = document.getElementById('id_level');
    const indukField = document.getElementById('id_induk');
    const satuanField = document.getElementById('id_satuan');
    const hargaField = document.getElementById('id_harga');

    function updateFormFields() {
        const tipe = tipeField.value;
        const level = parseInt(levelField.value);

        // Reset fields
        indukField.disabled = false;
        satuanField.disabled = false;
        hargaField.disabled = false;

        // If tipe == G
        if (tipe === 'G') {
            indukField.disabled = (level === 1);  // Disable induk for level == 1
            satuanField.disabled = true;  // Always disable satuan
            satuanField.value = '';  // Clear the satuan field
            hargaField.disabled = true;  // Always disable harga
            hargaField.value = '';  // Clear the harga field
        }

        // If tipe == D
        if (tipe === 'D') {
            indukField.disabled = false;
            satuanField.disabled = false;
            hargaField.disabled = false;
        }
    }

    // Attach event listeners
    tipeField.addEventListener('change', updateFormFields);
    levelField.addEventListener('change', updateFormFields);

    // Run logic on page load
    updateFormFields();
});