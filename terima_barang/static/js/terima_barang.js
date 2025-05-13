$(document).ready(function () {
    const $formsetDiv = $('#terima-barang-formset'); // Formset container
    const $preorderSelect = $('#id_preorder'); // PreOrder dropdown
    let barangData = {}; // Data: {barangId: {qty_po, qty_terima, qtystok}}

    // When PreOrder is selected, fetch barang data
    $preorderSelect.on('change', function () {
        const preorderId = $(this).val();

        if (!preorderId) {
            clearBarangDropdowns();
            return;
        }

        // Fetch barang associated with selected PreOrder
        $.get(`/terima-barang/preorder/${preorderId}/barang/`, function (response) {
            barangData = formatBarangData(response.barang);
            updateBarangDropdowns();
        }).fail(function () {
            console.error('Error fetching barang data.');
        });
    });

    // Handle live validation for qty_terima inputs
    $formsetDiv.on('input', 'input[name$="-qty_terima"]', function () {
        validateQtyTerima();
    });

    // Format raw barang data into a usable structure
    function formatBarangData(barangList) {
        return barangList.reduce((data, barang) => {
            data[barang.id] = { ...barang }; // Store barang info by id
            return data;
        }, {});
    }

    // Update all barang dropdowns in the formset
    function updateBarangDropdowns() {
        const options = Object.entries(barangData)
            .map(([id, { kode, nama, qty_po, qty_terima, qtystok }]) =>
                `<option value="${id}">${kode} - ${nama} (PO: ${qty_po}, Received: ${qty_terima}, Stock: ${qtystok})</option>`
            )
            .join('');

        $formsetDiv.find('select[name$="-kode_barang"]').html(`<option value="">-- Pilih Barang --</option>${options}`);
    }

    // Clear all barang dropdowns
    function clearBarangDropdowns() {
        barangData = {};
        $formsetDiv.find('select[name$="-kode_barang"]').html('<option value="">-- Pilih Barang --</option>');
    }

    // Validate total qty_terima for each barang
    function validateQtyTerima() {
        const totalQtyByBarang = {}; // Track total qty_terima per barang
        let isValid = true; // Form validity

        // Iterate each row in the formset
        $formsetDiv.find('.formset-row').each(function () {
            const $row = $(this);
            const barangId = $row.find('select[name$="-kode_barang"]').val();
            const qtyTerima = parseInt($row.find('input[name$="-qty_terima"]').val(), 10) || 0;

            // Skip validation if no barang is selected
            if (!barangId) return;

            totalQtyByBarang[barangId] = (totalQtyByBarang[barangId] || 0) + qtyTerima; // Increment total for the barang

            // Validate against remaining allowable qty
            const { qty_po, qty_terima } = barangData[barangId];
            const maxAllowedQty = qty_po - qty_terima;

            if (totalQtyByBarang[barangId] > maxAllowedQty) {
                isValid = false;
                showValidationError($row, `Exceeds allowed limit: ${maxAllowedQty}`);
            } else {
                clearValidationError($row);
            }
        });

        return isValid; // Return overall validity
    }

    // Show validation error on a specific row
    function showValidationError($row, message) {
        const $input = $row.find('input[name$="-qty_terima"]');
        $input.addClass('is-invalid');
        if ($input.siblings('.invalid-feedback').length === 0) {
            $input.after(`<div class="invalid-feedback">${message}</div>`);
        }
    }

    // Clear validation error on a specific row
    function clearValidationError($row) {
        const $input = $row.find('input[name$="-qty_terima"]');
        $input.removeClass('is-invalid');
        $input.siblings('.invalid-feedback').remove();
    }
});