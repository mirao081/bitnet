document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("roiChart").getContext("2d");

    
    const labels = JSON.parse(document.getElementById("roiChart").dataset.labels || "[]");
    const data = JSON.parse(document.getElementById("roiChart").dataset.data || "[]");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "ROI Growth",
                data: data,
                borderColor: "rgba(75, 192, 192, 1)",
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                fill: true,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true }
            }
        }
    });
});
