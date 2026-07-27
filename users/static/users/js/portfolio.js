document.addEventListener("DOMContentLoaded", function () {
    const chartEl = document.getElementById('portfolioChart');
    if (chartEl) {
        const ctx = chartEl.getContext('2d');
        const data = JSON.parse(chartEl.dataset.holdings);

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
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#fff' }
                    }
                }
            }
        });
    }
    function refreshMetrics() {
        fetch("/users/portfolio/metrics")
            .then(res => res.json())
            .then(data => {
                document.querySelector("#totalInvested").textContent = `$${data.total_invested}`;
                document.querySelector("#currentValue").textContent = `$${data.current_value}`;
                document.querySelector("#roi").textContent = `${data.roi}%`;
                document.querySelector("#bestAsset").textContent = data.best_asset;
            });
    }

    setInterval(refreshMetrics, 30000);
});
