$(document).ready(function () {
    const $formsetDiv = $('#terima-barang-formset');
    const $addRowButton = $('#add-row-btn');
    const $totalFormsInput = $('#id_terimabarangdetail-TOTAL_FORMS');
    const $preorderSelect = $('#id_preorder');

    let barangDropdownData = {};

    // Fetch available barang when PreOrder changes
    $preorderSelect.on('change', function () {
        const selectedPreorder = $(this).val();

        if (!selectedPreorder) {
            // Reset dropdowns if no PreOrder is selected
            $formsetDiv.find('select[name$="-kode_barang"]').empty().append('<option value="">-- Pilih Barang --</option>');
            return;
        }

        $.ajax({
            url: `/terima-barang/preorder/${selectedPreorder}/barang/`,
            method: 'GET',
            success: function (response) {
                // Update barangDropdownData to store qtystok by barang.id
                barangDropdownData = response.barang.reduce((acc, barang) => {
                    acc[barang.id] = barang.qtystok;
                    return acc;
                }, {});

                // Update all kode_barang dropdowns with the new options
                $formsetDiv.find('select[name$="-kode_barang"]').each(function () {
                    const $dropdown = $(this);
                    $dropdown.empty().append('<option value="">-- Pilih Barang --</option>');
                    response.barang.forEach(barang => {
                        $dropdown.append(`<option value="${barang.id}">${barang.kode} - ${barang.nama} (Stok: ${barang.qtystok})</option>`);
                    });
                });
            },
            error: function () {
                console.error('Failed to fetch barang data.');
            }
        });
    });

    // Validate qty_terima in real-time
    $formsetDiv.on('input', 'input[name$="-qty_terima"]', function () {
        validateQty();
    });

    // Add new row
    $addRowButton.on('click', function (e) {
        e.preventDefault();
        const currentFormCount = parseInt($totalFormsInput.val(), 10);
        const $newRow = $formsetDiv.find('.formset-row').first().clone();

        // Update attributes in the new row
        $newRow.html(
            $newRow.html()
                .replace(/-0-/g, `-${currentFormCount}-`)
                .replace(/__prefix__/g, currentFormCount)
        );

        // Reset field values
        $newRow.find('input, select').val('');
        $newRow.find('.invalid-feedback').remove();
        $formsetDiv.append($newRow);

        $totalFormsInput.val(currentFormCount + 1);
    });

    // Remove row handler
    $formsetDiv.on('click', '.remove-row-btn', function (e) {
        e.preventDefault();
        const $row = $(this).closest('.formset-row');

        // Mark the row for deletion if it exists on the server, otherwise remove it
        const $deleteCheckbox = $row.find('input[type="checkbox"][name$="-DELETE"]');
        if ($deleteCheckbox.length) {
            $deleteCheckbox.prop('checked', true); // Mark for deletion
            $row.hide(); // Hide the row
        } else {
            $row.remove(); // Remove from DOM
        }

        updateIndexes(); // Update form indexes
        validateQty(); // Revalidate the formset
    });

    // Validation logic
    function validateQty() {
        const barangTotals = {};
        let isValid = true;

        // Calculate running totals per barang
        $formsetDiv.find('.formset-row').each(function () {
            const $row = $(this);
            const barangId = $row.find('select[name$="-kode_barang"]').val(); // Use the selected barang.id
            const qtyTerima = parseInt($row.find('input[name$="-qty_terima"]').val(), 10) || 0;

            if (barangId) {
                if (!barangTotals[barangId]) {
                    barangTotals[barangId] = 0;
                }
                barangTotals[barangId] += qtyTerima;

                // Check if the total exceeds the stock for the selected barang.id
                if (barangTotals[barangId] > barangDropdownData[barangId]) {
                    isValid = false;
                    highlightError($row, `Total Qty Terima tidak boleh melebihi stok tersedia (${barangDropdownData[barangId]})!`);
                } else {
                    removeError($row);
                }
            }
        });

        return isValid;
    }

    function highlightError($row, message) {
        // Highlight the field with error
        const $input = $row.find('input[name$="-qty_terima"]');
        $input.addClass('is-invalid');

        // Add error message
        if ($input.siblings('.invalid-feedback').length === 0) {
            $input.after(`<div class="invalid-feedback">${message}</div>`);
        }
    }

    function removeError($row) {
        const $input = $row.find('input[name$="-qty_terima"]');
        $input.removeClass('is-invalid');
        $input.siblings('.invalid-feedback').remove();
    }

    // Update form indexes after adding or removing rows
    function updateIndexes() {
        const $rows = $formsetDiv.find('.formset-row');

        $rows.each(function (index, row) {
            const $row = $(row);

            $row.find('input, select, label').each(function () {
                const $field = $(this);
                ['name', 'id', 'for'].forEach(attr => {
                    const currentAttr = $field.attr(attr);
                    if (currentAttr) {
                        $field.attr(attr, currentAttr.replace(/-\d+-/, `-${index}-`));
                    }
                });
            });
        });

        $totalFormsInput.val($rows.length);
    }
});