$(document).ready(function () {
    // Function to format numbers with thousand separators
    function formatNumber(num) {
        return new Intl.NumberFormat().format(num); // Add thousand separators
    }

    // Function to calculate total value of all 'value' fields in dynamic forms
    function calculateTotalValue() {
        let total = 0;
        $('.form').each(function () {
            const valueField = $(this).find('.thousand-format input').val();
            if (valueField && !$(this).find('input[type="checkbox"][name$="-DELETE"]').is(':checked')) {
                total += parseFloat(valueField.replace(/,/g, '')) || 0; // Remove thousand separators
            }
        });
        return total;
    }

    // Function to validate the total value against 'plafon_diajukan'
    function validateRincianTotal() {
        const plafonDiajukan = parseFloat($('#id_plafon_diajukan').val().replace(/,/g, '')) || 0;
        const totalRincian = calculateTotalValue();

        // Update the 'Total Rincian' field display
        $('#totalRincian').val(formatNumber(totalRincian));

        if (totalRincian !== plafonDiajukan) {
            // Show error message and add 'is-invalid' to value fields
            $('#error_rincian').show();
            $('.thousand-format input').addClass('is-invalid');
            $('#submit-btn').prop('disabled', true); // Disable submit button
        } else {
            // Hide error message and remove 'is-invalid' class
            $('#error_rincian').hide();
            $('.thousand-format input').removeClass('is-invalid');
            $('#submit-btn').prop('disabled', false); // Enable submit button
        }
    }

    $('#add-form-btn').click(function () {
        let form_idx = $('#id_loanusagepurposedetail_set-TOTAL_FORMS').val();

        // Insert the new form above the "total rincian" row
        $('#totalRincian').closest('.row').before($('#empty-form').html().replace(/__prefix__/g, form_idx));
        $('#id_loanusagepurposedetail_set-TOTAL_FORMS').val(parseInt(form_idx) + 1);
        let newInputElement = $('#loan-usage-detail-formset .form').last().find('.thousand-format input')[0];
        if (newInputElement) {
            attachThousandFormatter(newInputElement); // Call the function defined in formatter.js
        }

        validateRincianTotal();
    });

    $(document).on('click', '.remove-form-button', function () {
        const form = $(this).closest('.form');
        form.hide();
        const del_checkbox = form.find('input[type="checkbox"][name$="-DELETE"]');
        del_checkbox.prop('checked', true);

        validateRincianTotal();
    });

    // On change of any 'value' field, recalculate the total and validate
    $(document).on('input', '.thousand-format input', function () {
        validateRincianTotal();
    });

    // Initial validation on page load (if existing data is loaded)
    validateRincianTotal();
});
