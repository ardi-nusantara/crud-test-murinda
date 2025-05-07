$(document).ready(function () {
    const tipeField = $('#id_tipe');
    const levelField = $('#id_level');
    const indukField = $('#id_induk');
    const satuanField = $('#id_satuan');
    const hargaField = $('#id_harga');

    function setFieldState(fields, disabled, required, clearValue = true) {
        fields.forEach(field => {
            field.prop('disabled', disabled).prop('required', required);
            if (clearValue) field.val('');
        });
    }

    function initializeForm() {
        setFieldState([indukField, satuanField, hargaField], true, false);
    }

    function updateIndukChoices() {
        const level = parseInt(levelField.val());
        if (isNaN(level) || (tipeField.val() === 'G' && level <= 1)) {
            return setFieldState([indukField], true, false);
        }


        $.get('/master-barang/get_induk_choices/', {level: level - 1, tipe: 'G'})
            .done(data => {
                indukField.empty().append('<option value="">-----</option>');
                data.induk_choices.forEach(choice => {
                    indukField.append(`<option value="${choice.id}">${choice.kode} - ${choice.nama}</option>`);
                });
                setFieldState([indukField], false, true, false);
            })
            .fail(() => console.error('Failed to fetch induk choices.'));
    }

    function updateFormFields() {
        const tipe = tipeField.val(), level = parseInt(levelField.val());

        if (tipe === 'G') {
            if (level === 1) {
                setFieldState([indukField, satuanField, hargaField], true, false);
            } else if (level > 1) {
                setFieldState([indukField], false, true, false);
                setFieldState([satuanField, hargaField], true, false);
            }
        } else if (tipe === 'D') {
            setFieldState([indukField, satuanField, hargaField], false, true);
        }
    }

    $('form').on('submit', function (event) {
        const tipe = tipeField.val(), level = parseInt(levelField.val());
        if (tipe === 'G' && ((level === 1 && (indukField.val() || satuanField.val() || hargaField.val())) ||
            (level > 1 && (!indukField.val() || satuanField.val() || hargaField.val())))) {
            event.preventDefault();
            alert('Validation error: Please check induk, satuan, and harga fields.');
        } else if (tipe === 'D' && (!indukField.val() || !satuanField.val() || !hargaField.val())) {
            event.preventDefault();
            alert('Validation error: For tipe "D", all fields are required.');
        }
    });

    [tipeField, levelField].forEach(field => field.on('change', () => {
        updateFormFields();
        updateIndukChoices();
    }));

    initializeForm();
});