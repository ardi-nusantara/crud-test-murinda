$(document).ready(function () {
    // $('#id_induk').select2();

    const tipeField = document.getElementById('id_tipe');
    const kodeField = document.getElementById('id_kode');
    const levelField = document.getElementById('id_level');
    const indukField = document.getElementById('id_induk');
    const satuanField = document.getElementById('id_satuan');
    const hargaField = document.getElementById('id_harga');

    $("#id_provinsi").change(function () {
        $.ajax({
            type: 'GET',
            url: '/applicant/load-cities/',
            data: {
                'province_id': $(this).val().split('_')[0]
            },
            success: function (data) {
                $('#id_kota').empty();
                $.each(data, function (index, item) {
                    $('#id_kota').append(`<option value="${item[0]}">${item[1]}</option>`);
                });
            }
        });
    });

    async function fetchIndukChoices(kode, level) {
        console.log('kode = ', kode, 'level = ', level);

        await $.ajax({
            type: 'GET',
            url: '/master-barang/get_induk_choices/', // Adjust this URL if needed
            data: {'kode': kode, 'level': level}, // Pass the `kode` and `level` as query parameters
            success: function (result) {
                indukChoices = result.induk_choices || [];
            },
            error: function (xhr, status, error) {
                console.error(`Failed to fetch induk choices: ${error}`);
            }
        });

        return indukChoices; // Return the populated choices
    }

    function updateFormFields() {
        /**
         * Apply the rules for enabling/disabling fields based on tipe and level.
         */
        const tipe = tipeField.value;
        const level = parseInt(levelField.value);

        indukField.disabled = false;
        satuanField.disabled = false;
        hargaField.disabled = false;

        if (tipe === 'G') {
            indukField.disabled = (level === 1);
            satuanField.disabled = true;
            satuanField.value = '';
            hargaField.disabled = true;
            hargaField.value = '';
        }

        if (tipe === 'D') {
            indukField.disabled = false;
            satuanField.disabled = false;
            hargaField.disabled = false;
        }
    }

    // Attach event listeners for required fields
    tipeField.addEventListener('change', function () {
        updateFormFields();
        updateIndukChoices();
    });

    levelField.addEventListener('change', function () {
        updateFormFields();
        updateIndukChoices();
    });

    kodeField.addEventListener('change', updateIndukChoices);

    // Run logic on page load
    updateFormFields();
    updateIndukChoices(); // Ensures the dropdown is initialized correctly
});