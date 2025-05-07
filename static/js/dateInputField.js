$(document).ready(function () {
    // Select all input elements with class 'dateinput'
    $('.dateinput').each(function () {
        // Create the new structure with calendar icon
        const inputGroup = $('<div class="input-group"></div>');
        const inputGroupText = $('<div class="input-group-text text-muted"><i class="ri-calendar-line"></i></div>');

        // Wrap the current input field with the new div structure
        $(this).wrap(inputGroup);
        $(this).before(inputGroupText); // Insert the calendar icon div before the input

        // Append an error message container directly after the input field
        const errorMessage = $('<div class="invalid-feedback" style="display: none; font-size: 12px; margin-top: 5px;">' +
            '<b>Tanggal yang diinput tidak boleh melebihi hari ini!</b></div>');
        $(this).parent().parent().append(errorMessage);

        // Add today's date dynamically
        const today = new Date().toISOString().split('T')[0];
        $(this).attr('max', today); // Set max attribute for the date field (HTML5 validation)

        // Validate the date field on change
        $(this).on('change', function () {
            const selectedDate = new Date($(this).val());
            const now = new Date(today);

            if (selectedDate > now) {
                errorMessage.show(); // Show error message
                $(this).addClass('is-invalid'); // Add Bootstrap error styling
            } else {
                errorMessage.hide(); // Hide error message
                $(this).removeClass('is-invalid'); // Remove Bootstrap error styling
            }
        });
    });
});