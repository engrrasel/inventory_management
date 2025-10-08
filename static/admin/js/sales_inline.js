document.addEventListener('DOMContentLoaded', function () {
    function calculateRowTotal(row) {
        let qtyInput = row.querySelector('[id$="-quantity"]');
        let priceInput = row.querySelector('[id$="-unit_price"]');
        let totalInput = row.querySelector('[id$="-total_price"]');

        if (!qtyInput || !priceInput || !totalInput) return;

        let qty = parseFloat(qtyInput.value) || 0;
        let price = parseFloat(priceInput.value) || 0;
        totalInput.value = (qty * price).toFixed(2);
    }

    function updateAllTotals() {
        document.querySelectorAll('.dynamic-salesitem_set').forEach(calculateRowTotal);
    }

    document.querySelector('#salesitem_set-group').addEventListener('input', function (e) {
        if (e.target.name.includes('quantity') || e.target.name.includes('unit_price')) {
            let row = e.target.closest('.form-row');
            calculateRowTotal(row);
        }
    });

    // Page load এ সব হিসাব চেক করো
    updateAllTotals();
});
