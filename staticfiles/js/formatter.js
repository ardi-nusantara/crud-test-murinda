function thousandFormatter(value, cursorPosition) {
    // Remove all non-digit characters except for commas, periods, and the leading minus sign
    const cleanedValue = value.replace(/(?!^-)[^\d.]/g, '');

    // Check if the value is negative
    const isNegative = cleanedValue[0] === '-';

    // Split the value into integer and decimal parts
    const [integerPart, decimalPart] = cleanedValue.replace('-', '').split('.');

    // Format the integer part with commas
    const formattedIntegerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ',');

    // Combine formatted parts
    let formattedValue = decimalPart !== undefined ? `${formattedIntegerPart}.${decimalPart}` : formattedIntegerPart;

    // Add the negative sign back if the value is negative
    if (isNegative) {
        formattedValue = '-' + formattedValue;
    }

    // Calculate new cursor position after formatting
    const newCursorPosition = cursorPosition + (formattedValue.length - value.length);

    return {formattedValue, newCursorPosition};
}

// Function to apply thousand formatting to an input element
function attachThousandFormatter(inputElement) {
    // Helper function to format value in the input
    function formatThousand(inputElement) {
        const cursorPosition = inputElement.selectionStart;
        const {formattedValue, newCursorPosition} = thousandFormatter(inputElement.value, cursorPosition);
        inputElement.value = formattedValue;
        inputElement.setSelectionRange(newCursorPosition, newCursorPosition);
    }

    inputElement.type = 'text';
    formatThousand(inputElement);

    inputElement.addEventListener('input', function () {
        formatThousand(inputElement);
    });

    if (inputElement.form) {
        // Ensure proper submission behavior when the form is submitted
        inputElement.form.addEventListener('submit', function (e) {
            e.preventDefault();
            // Clean the input value by removing commas and non-digit characters, but allow a minus sign
            inputElement.value = inputElement.value.replace(/[^\d.-]/g, '');
            // Reset the input type back to number to ensure correct submission
            inputElement.type = 'number';
            // Submit the form
            inputElement.form.submit();
        });
    }
}

// Apply formatting on page load for elements with the 'thousand-format' class
$(document).ready(function () {
    const elementList = document.getElementsByClassName('thousand-format');
    for (let i = 0; i < elementList.length; i++) {
        let inputElement = elementList[i].querySelector('input') || elementList[i];
        attachThousandFormatter(inputElement);
    }
});