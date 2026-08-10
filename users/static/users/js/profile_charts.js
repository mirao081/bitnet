document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById("roiChart");

    // Nothing to render if there is no chart on the page.
    if (!canvas) {
        return;
    }

    // Make sure Chart.js is loaded.
    if (typeof Chart === "undefined") {
        console.error("Chart.js is not loaded.");
        return;
    }

    const labelsElement = document.getElementById("profile-chart-labels");
    const dataElement = document.getElementById("profile-chart-data");

    if (!labelsElement || !dataElement) {
        console.error("Profile chart data was not found.");
        return;
    }

    let labels = [];
    let data = [];

    try {
        labels = JSON.parse(labelsElement.textContent || "[]");
        data = JSON.parse(dataElement.textContent || "[]");
    } catch (error) {
        console.error("Unable to parse profile chart data:", error);
        return;
    }

    if (!Array.isArray(labels) || !Array.isArray(data)) {
        console.error("Profile chart data must be arrays.");
        return;
    }

    if (labels.length === 0 || data.length === 0) {
        return;
    }

    const ctx = canvas.getContext("2d");

    if (!ctx) {
        console.error("Unable to get profile chart canvas context.");
        return;
    }

    // Prevent duplicate charts if the script is loaded twice.
    if (window.profileROIChart) {
        window.profileROIChart.destroy();
    }

    window.profileROIChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Investment Value",
                    data: data,
                    borderColor: "#00d8ef",
                    backgroundColor: "rgba(0, 216, 239, 0.15)",
                    borderWidth: 3,
                    pointBackgroundColor: "#00d8ef",
                    pointBorderColor: "#ffffff",
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 7,
                    fill: true,
                    tension: 0.35
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: "index"
            },
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: "#ffffff",
                        font: {
                            size: 14,
                            weight: "600"
                        }
                    }
                },
                tooltip: {
                    enabled: true,
                    callbacks: {
                        label: function (context) {
                            return (
                                " Value: $" +
                                Number(context.parsed.y).toLocaleString("en-US", {
                                    minimumFractionDigits: 2,
                                    maximumFractionDigits: 2
                                })
                            );
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: "rgba(255,255,255,0.75)"
                    },
                    grid: {
                        color: "rgba(255,255,255,0.08)"
                    }
                },
                y: {
                    beginAtZero: false,
                    ticks: {
                        color: "rgba(255,255,255,0.75)",
                        callback: function (value) {
                            return "$" + Number(value).toLocaleString("en-US");
                        }
                    },
                    grid: {
                        color: "rgba(255,255,255,0.08)"
                    }
                }
            }
        }
    });
});
