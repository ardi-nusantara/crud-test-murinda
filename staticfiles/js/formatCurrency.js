$(document).ready(function () {
    const elems = document.querySelectorAll('.rupiah-format');

    function formatCurrency(value) {
        return 'Rp. ' + value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    }

    elems.forEach(function (elem) {
        const currencyStr = elem.innerText;
        const currencyValue = parseFloat(currencyStr);

        if (!isNaN(currencyValue)) {
            elem.innerText = formatCurrency(currencyValue);
        }
    });
})