document.addEventListener("DOMContentLoaded", function () {
    const allocEl = document.getElementById('allocationChart');
    if (allocEl) {
        const ctx = allocEl.getContext('2d');
        const data = JSON.parse(allocEl.dataset.holdings);

        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: Object.keys(data),
                datasets: [{
                    data: Object.values(data),
                    backgroundColor: ['#f2a900', '#3c3c3d', '#26a17b'],
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'bottom' } }
            }
        });
    }
    const historyEl = document.getElementById('historyChart');
    if (historyEl) {
        const ctx = historyEl.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ["Jan", "Feb", "Mar", "Apr", "May"],
                datasets: [{
                    label: "Profit/Loss",
                    data: [200, 300, 150, 400, 350],
                    borderColor: "#f2a900",
                    fill: false
                }]
            }
        });
    }
});
