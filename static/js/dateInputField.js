$(document).ready(function () {
    // Select all input elements with class 'dateinput'
    $('.dateinput').each(function () {
        // Create the new structure
        const inputGroup = $('<div class="input-group"></div>');
        const inputGroupText = $('<div class="input-group-text text-muted"><i class="ri-calendar-line"></i></div>');

        // Wrap the current input field with the new div structure
        $(this).wrap(inputGroup);
        $(this).before(inputGroupText); // Insert the calendar icon div before the input
    });
});