document.addEventListener("DOMContentLoaded", function () {
    const allocationCanvas = document.getElementById("allocationChart");
    const holdingsElement = document.getElementById("holdings-data");

    if (allocationCanvas && holdingsElement && typeof Chart !== "undefined") {
        try {
            const holdings = JSON.parse(holdingsElement.textContent);

            console.log("Allocation data:", holdings);

            const labels = Object.keys(holdings);
            const values = Object.values(holdings);

            // Don't create an empty pie chart
            const hasValues = values.some(value => Number(value) > 0);

            if (hasValues) {
                new Chart(allocationCanvas.getContext("2d"), {
                    type: "pie",
                    data: {
                        labels: labels,
                        datasets: [{
                            data: values,
                            backgroundColor: [
                                "#f2a900",
                                "#3c3c3d",
                                "#26a17b"
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: "bottom"
                            }
                        }
                    }
                });
            } else {
                console.log("No allocation values available.");
            }

        } catch (error) {
            console.error("Failed to render allocation chart:", error);
        }
    } else {
        console.error("Allocation chart or Chart.js is missing.");
    }


    // History chart
    const historyCanvas = document.getElementById("historyChart");

    if (historyCanvas && typeof Chart !== "undefined") {
        new Chart(historyCanvas.getContext("2d"), {
            type: "line",
            data: {
                labels: ["Jan", "Feb", "Mar", "Apr", "May"],
                datasets: [{
                    label: "Profit/Loss",
                    data: [200, 300, 150, 400, 350],
                    borderWidth: 2,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
});