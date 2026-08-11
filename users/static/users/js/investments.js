
document.addEventListener("DOMContentLoaded", function () {

    console.log("Investment charts script loaded.");

    /*
    ==========================================
    ASSET ALLOCATION CHART
    ==========================================
    */

    const allocationCanvas =
        document.getElementById("allocationChart");

    if (allocationCanvas) {

        console.log("Allocation canvas found.");

        if (typeof Chart === "undefined") {

            console.error(
                "Chart.js is NOT loaded."
            );

            return;
        }

        try {

            const holdingsString =
                allocationCanvas.dataset.holdings;

            console.log(
                "Holdings data:",
                holdingsString
            );

            const holdings =
                JSON.parse(holdingsString);

            const labels =
                Object.keys(holdings);

            const values =
                Object.values(holdings);

            console.log(
                "Allocation labels:",
                labels
            );

            console.log(
                "Allocation values:",
                values
            );

            new Chart(
                allocationCanvas.getContext("2d"),
                {
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

                            borderColor: "#ffffff",

                            borderWidth: 2
                        }]
                    },

                    options: {
                        responsive: true,

                        maintainAspectRatio: false,

                        plugins: {

                            legend: {
                                position: "bottom",

                                labels: {
                                    color: "#ffffff"
                                }
                            }
                        }
                    }
                }
            );

            console.log(
                "Allocation chart created successfully."
            );

        } catch (error) {

            console.error(
                "Error creating allocation chart:",
                error
            );
        }
    }


    /*
    ==========================================
    PROFIT & LOSS HISTORY CHART
    ==========================================
    */

    const historyCanvas =
        document.getElementById("historyChart");

    if (historyCanvas) {

        console.log("History canvas found.");

        if (typeof Chart === "undefined") {

            console.error(
                "Chart.js is NOT loaded."
            );

            return;
        }

        try {

            new Chart(
                historyCanvas.getContext("2d"),
                {
                    type: "line",

                    data: {

                        labels: [
                            "Jan",
                            "Feb",
                            "Mar",
                            "Apr",
                            "May"
                        ],

                        datasets: [{
                            label: "Profit/Loss",

                            data: [
                                200,
                                300,
                                150,
                                400,
                                350
                            ],

                            borderColor: "#f2a900",

                            backgroundColor:
                                "rgba(242, 169, 0, 0.15)",

                            borderWidth: 3,

                            tension: 0.4,

                            fill: true,

                            pointRadius: 5,

                            pointHoverRadius: 7
                        }]
                    },

                    options: {

                        responsive: true,

                        maintainAspectRatio: false,

                        plugins: {

                            legend: {
                                labels: {
                                    color: "#ffffff"
                                }
                            }
                        },

                        scales: {

                            x: {
                                ticks: {
                                    color: "#ffffff"
                                },

                                grid: {
                                    color:
                                        "rgba(255,255,255,0.08)"
                                }
                            },

                            y: {
                                ticks: {
                                    color: "#ffffff"
                                },

                                grid: {
                                    color:
                                        "rgba(255,255,255,0.08)"
                                }
                            }
                        }
                    }
                }
            );

            console.log(
                "History chart created successfully."
            );

        } catch (error) {

            console.error(
                "Error creating history chart:",
                error
            );
        }
    }

});

