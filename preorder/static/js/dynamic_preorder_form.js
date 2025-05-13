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
        validateQty(); // Revalidate all rows when a row is removed
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

    // Validate qty_po when the input field is changed
    async function validateQty() {
        const $rows = $formsetDiv.find('.formset-row');
        const barangTotals = {}; // To sum up `qty_po` values per barang

        let isValid = true;

        // Clear previous error messages
        $rows.find('.invalid-feedback').remove();

        const promises = $rows.map(async function (_, row) {
            const $row = $(row);

            // Get selected barang kode
            const barangKode = $row.find('select[name$="-kode_barang"]').val();
            const $qtyPoInput = $row.find('input[name$="-qty_po"]');
            const qtyPo = parseInt($qtyPoInput.val(), 10) || 0;

            if (!barangKode) {
                return; // Skip rows with no selected barang
            }

            // Initialize running total for this barang
            if (!barangTotals[barangKode]) {
                barangTotals[barangKode] = 0;
            }
            barangTotals[barangKode] += qtyPo;

            // AJAX call to fetch qtystok for the selected barang
            try {
                const response = await $.ajax({
                    url: `/preorder/get-barang-qtystok/`, // Replace with the actual endpoint for fetching qtystok
                    method: 'GET',
                    data: { kode_barang: barangKode }, // Send the selected dropdown value
                });

                const qtystok = parseInt(response.qtystok, 10);

                // Check if the aggregated qty_po exceeds qtystok
                if (barangTotals[barangKode] > qtystok) {
                    isValid = false;

                    // Build and display the error message
                    const errorMessage = $(
                        '<div class="invalid-feedback" style="display: block; font-size: 12px; margin-top: 5px;">' +
                        `<b>Qty Pesanan tidak boleh melebihi stok tersedia (${qtystok})!</b>` +
                        '</div>'
                    );

                    // Append the error message after the input field
                    $qtyPoInput.parent().append(errorMessage);

                    // Highlight the input field with an error class
                    $qtyPoInput.addClass('is-invalid');
                } else {
                    // If valid, remove any previous error highlight
                    $qtyPoInput.removeClass('is-invalid');
                }
            } catch (error) {
                console.error('Error fetching qtystok:', error);
            }
        }).get();

        // Wait for all AJAX calls to complete
        await Promise.all(promises);

        return isValid;
    }

    // Add row event listener
    $addRowButton.on('click', function (e) {
        e.preventDefault();
        addRow();
    });

    // Remove row event listener
    $formsetDiv.on('click', '.remove-row-btn', function (e) {
        e.preventDefault();
        removeRow($(this));
    });

    // Real-time validation on qty_po input change
    $formsetDiv.on('input', 'input[name$="-qty_po"]', function () {
        validateQty(); // Validate the entire formset on each input change
    });
});