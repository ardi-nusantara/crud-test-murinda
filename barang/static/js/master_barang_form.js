$(document).ready(function () {
    const tipeField = $('#id_tipe');
    const levelField = $('#id_level');
    const indukField = $('#id_induk');
    const satuanField = $('#id_satuan');
    const hargaField = $('#id_harga');
    const qtystokFieldWrapper = $('#div_id_qtystok');
    const qtystokField = $('#id_qtystok');


    function qtystokFieldDisplay() {
        if (tipeField.val() === 'D') {
            qtystokFieldWrapper.show();
            qtystokField.prop('required', true);
        } else {
            qtystokField.val('');
            qtystokField.prop('required', false);
            qtystokFieldWrapper.hide();
        }
    }


    function setFieldState(fields, disabled, required, clearValue = true) {
        fields.forEach(field => {
            field.prop('disabled', disabled).prop('required', required);
            if (clearValue) field.val('');
        });
    }

    function initializeForm() {
        const isUpdateForm = satuanField.val() || hargaField.val() || indukField.val();

        if (!isUpdateForm) {
            setFieldState([indukField, satuanField, hargaField], true, false);
        }
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
                    const isSelected = choice.id === parseInt(indukField.val()); // Preserve selection for an update form
                    indukField.append(`<option value="${choice.id}" ${isSelected ? 'selected' : ''}>${choice.kode} - ${choice.nama}</option>`);
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

    // Initialize the form depending on its context (new or update)
    initializeForm();

    // Handle qtystok field display based on tipe
    qtystokFieldDisplay();

    tipeField.on('change', function () {
        qtystokFieldDisplay();
    });
});