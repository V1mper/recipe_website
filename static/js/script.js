document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    const selects = document.querySelectorAll('select.ration-select');
    if (!selects.length) return;

    function recalcRation() {
        let k = 0, p = 0, f = 0, c = 0;
        selects.forEach(function(sel) {
            const opt = sel.options[sel.selectedIndex];
            if (!opt || !opt.value) return;
            k += parseInt(opt.dataset.kcal || '0', 10) || 0;
            p += parseFloat(opt.dataset.p || '0') || 0;
            f += parseFloat(opt.dataset.f || '0') || 0;
            c += parseFloat(opt.dataset.c || '0') || 0;
        });
        const elK = document.getElementById('sum-kcal');
        const elP = document.getElementById('sum-p');
        const elF = document.getElementById('sum-f');
        const elC = document.getElementById('sum-c');
        if (elK) elK.textContent = String(k);
        if (elP) elP.textContent = p.toFixed(1);
        if (elF) elF.textContent = f.toFixed(1);
        if (elC) elC.textContent = c.toFixed(1);
    }

    selects.forEach(function(sel) {
        sel.addEventListener('change', recalcRation);
    });
    recalcRation();
});
