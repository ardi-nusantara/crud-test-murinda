$(document).ready(function () {
    // Target all input fields with class `numberinput`
    $('.numberinput').each(function () {
        // Append a dynamic error message placeholder after each numberinput
        const errorMessage = $('<div class="invalid-feedback" style="display: none; font-size: 12px; margin-top: 5px;">' +
            '<b>Tidak boleh minus!</b></div>');
        $(this).parent().append(errorMessage);

        // Real-time validation: Prevent negative values
        $(this).on('input change', function () {
            const value = $(this).val();
            if (value < 0) {
                errorMessage.show(); // Show the error message
                $(this).addClass('is-invalid'); // Add Bootstrap invalid styling
            } else {
                errorMessage.hide(); // Hide the error message
                $(this).removeClass('is-invalid'); // Remove Bootstrap invalid styling
            }
        });
    });

    $("form").on("submit", function (e) {
        let invalidFields = false;

        $('.numberinput').each(function () {
            // Check if the number input has the 'is-invalid' class
            if ($(this).hasClass('is-invalid')) {
                invalidFields = true; // Mark form as having invalid fields
            }
        });

        if (invalidFields) {
            e.preventDefault(); // Block form submission
            alert("Ada nilai yang tidak valid. Perbaiki sebelum mengirimkan formulir.");
        }
    });

});