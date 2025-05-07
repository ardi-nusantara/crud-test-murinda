$(document).ready(function () {
    const pemasok = $("#id_pemasok");
    const qtyTerima = $("#id_qty_terima");
    const form = $("form");
    const errorMessage = $('<div class="invalid-feedback" style="display: none; font-size: 12px; margin-top: 5px;">' +
        '<b>Nilai Qty Terima tidak boleh melebihi <span id="max-qty">-</span>!</b></div>');

    qtyTerima.parent().append(errorMessage);

    let maxQty = null;

    pemasok.on("change", function () {
        const selectedId = $(this).val();

        if (!selectedId) {
            // Reset if no valid selection
            maxQty = null;
            qtyTerima.val('');
            errorMessage.hide();
            qtyTerima.removeClass('is-invalid');
            return;
        }

        $.ajax({
            url: `/terima-barang/preorder/${selectedId}/`,
            method: "GET",
            success: function (response) {
                maxQty = response.qty_po;

                $("#max-qty").text(maxQty);
                qtyTerima.attr("max", maxQty);
            },
            error: function () {
                console.error("Failed to fetch qty_po value.");
                maxQty = null;
            },
        });
    });

    qtyTerima.on("input change", function () {
        const qtyTerimaValue = parseInt($(this).val(), 10);

        if (maxQty !== null && qtyTerimaValue > maxQty) {
            errorMessage.show();
            $(this).addClass("is-invalid");
        } else {
            errorMessage.hide();
            $(this).removeClass("is-invalid");
        }
    });

    form.on("submit", function (e) {
        const qtyTerimaValue = parseInt(qtyTerima.val(), 10);

        if (maxQty !== null && qtyTerimaValue > maxQty) {
            e.preventDefault();
            alert("Qty Terima tidak boleh melebihi Qty PO.");
            qtyTerima.addClass("is-invalid");
        }
    });
});