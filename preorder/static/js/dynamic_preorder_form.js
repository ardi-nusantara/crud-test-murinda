$(document).ready(function () {
    const $formsetDiv = $('#preorder-formset');
    const $addRowButton = $('#add-row-btn');
    const $totalFormsInput = $('#id_preorder_detail-TOTAL_FORMS');

    // Function to create a new row
    function addRow() {
        const currentFormCount = parseInt($totalFormsInput.val(), 10);

        // Clone the first row as a template
        const $newFormRow = $formsetDiv.find('.formset-row').first().clone();

        // Update indices in the cloned row
        $newFormRow.html(
            $newFormRow.html()
                .replace(/-0-/g, `-${currentFormCount}-`)
                .replace(/__prefix__/g, currentFormCount)
        );

        // Remove DELETE checkbox
        $newFormRow.find('input[type="checkbox"][name$="-DELETE"]').closest('div').remove();

        // Reset input values
        $newFormRow.find('input, select, textarea').each(function () {
            const $field = $(this);

            if ($field.is('input[type="checkbox"]')) {
                $field.prop('checked', false);
            } else if ($field.is('select')) {
                $field.prop('selectedIndex', 0);
            } else {
                $field.val('');
            }
        });

        // Remove any existing error messages in the template
        $newFormRow.find('.invalid-feedback').remove();

        // Append the modified cloned row
        $formsetDiv.append($newFormRow);

        // Update total forms count
        $totalFormsInput.val(currentFormCount + 1);
    }

    // Function to handle row removal
    function removeRow($button) {
        const $row = $button.closest('.formset-row');

        // Find and check the DELETE checkbox
        const $deleteCheckbox = $row.find('input[type="checkbox"][name$="-DELETE"]');
        if ($deleteCheckbox.length) {
            $deleteCheckbox.prop('checked', true);
            $row.hide();
        } else {
            $row.remove();
        }

        // Update indices and total forms count
        updateIndexes();
    }

    // Recalculate form indexes
    function updateIndexes() {
        const $rows = $formsetDiv.find('.formset-row');

        $rows.each(function (index, row) {
            const $row = $(row);

            // Update row ID
            $row.attr('id', `formset-row-${index}`);

            // Update name/id attributes
            $row.find('[name], [id], [for]').each(function () {
                const $input = $(this);

                if ($input.attr('name')) {
                    $input.attr('name', $input.attr('name').replace(/-\d+-/, `-${index}-`));
                }
                if ($input.attr('id')) {
                    $input.attr('id', $input.attr('id').replace(/-\d+-/, `-${index}-`));
                }
                if ($input.attr('for')) {
                    $input.attr('for', $input.attr('for').replace(/-\d+-/, `-${index}-`));
                }
            });
        });

        $totalFormsInput.val($rows.length);
    }

    // Event listener for adding a new row
    $addRowButton.on('click', function (e) {
        e.preventDefault();
        addRow();
    });

    // Event listener for removing a row
    $formsetDiv.on('click', '.remove-row-btn', function (e) {
        e.preventDefault();
        const $button = $(this);
        removeRow($button);
    });
});