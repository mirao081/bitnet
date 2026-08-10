/*==================================================*
* INVESTMENT CHARTS
*==================================================*/

document.addEventListener("DOMContentLoaded", function () {

    console.log("Investment charts: initializing...");


    /*==================================================*
    * CHECK CHART.JS
    *==================================================*/

    if (typeof Chart === "undefined") {

        console.error(
            "Investment charts: Chart.js is not loaded."
        );

        return;
    }


    console.log(
        "Investment charts: Chart.js loaded.",
        Chart.version
    );


    /*==================================================*
    * ASSET ALLOCATION CHART
    *==================================================*/

    const allocationCanvas =
        document.getElementById("allocationChart");


    if (allocationCanvas) {

        try {

            const rawHoldings =
                allocationCanvas.dataset.holdings;


            console.log(
                "Investment charts: holdings data:",
                rawHoldings
            );


            if (!rawHoldings) {

                console.warn(
                    "Investment charts: no holdings data found."
                );

            } else {

                const holdings =
                    JSON.parse(rawHoldings);


                const labels =
                    Object.keys(holdings);


                const values =
                    Object.values(holdings);


                if (
                    labels.length === 0 ||
                    values.length === 0
                ) {

                    console.warn(
                        "Investment charts: holdings data is empty."
                    );

                } else {

                    const allocationContext =
                        allocationCanvas.getContext("2d");


                    new Chart(
                        allocationContext,
                        {
                            type: "pie",

                            data: {

                                labels: labels,

                                datasets: [{
                                    data: values,

                                    backgroundColor: [
                                        "#00d8ef",
                                        "#7a00ff",
                                        "#ff0080",
                                        "#f2a900",
                                        "#26a17b",
                                        "#ff6b6b",
                                        "#4dabf7",
                                        "#51cf66"
                                    ],

                                    borderColor:
                                        "#0a1020",

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

                                            color: "#ffffff",

                                            padding: 15,

                                            font: {
                                                size: 13
                                            }
                                        }
                                    }

                                }
                            }
                        }
                    );


                    console.log(
                        "Investment charts: allocation chart created."
                    );
                }
            }

        } catch (error) {

            console.error(
                "Investment charts: allocation chart failed.",
                error
            );
        }

    } else {

        console.warn(
            "Investment charts: allocationChart canvas not found."
        );
    }


    /*==================================================*
    * PROFIT & LOSS HISTORY CHART
    *==================================================*/

    const historyCanvas =
        document.getElementById("historyChart");


    if (historyCanvas) {

        try {

            const historyContext =
                historyCanvas.getContext("2d");


            new Chart(
                historyContext,
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

                            borderColor:
                                "#00d8ef",

                            backgroundColor:
                                "rgba(0, 216, 239, 0.12)",

                            borderWidth: 3,

                            fill: true,

                            tension: 0.4,

                            pointBackgroundColor:
                                "#ff0080",

                            pointBorderColor:
                                "#ffffff",

                            pointBorderWidth: 2,

                            pointRadius: 5,

                            pointHoverRadius: 7
                        }]
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

                                labels: {

                                    color: "#ffffff",

                                    font: {
                                        size: 13
                                    }
                                }
                            }
                        },

                        scales: {

                            x: {

                                ticks: {

                                    color:
                                        "rgba(255,255,255,0.70)"
                                },

                                grid: {

                                    color:
                                        "rgba(255,255,255,0.08)"
                                }
                            },

                            y: {

                                ticks: {

                                    color:
                                        "rgba(255,255,255,0.70)"
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
                "Investment charts: history chart created."
            );

        } catch (error) {

            console.error(
                "Investment charts: history chart failed.",
                error
            );
        }

    } else {

        console.warn(
            "Investment charts: historyChart canvas not found."
        );
    }


    console.log(
        "Investment charts: initialization complete."
    );

});