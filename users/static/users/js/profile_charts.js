document.addEventListener("DOMContentLoaded", function () {

    /* ==================================================
       FIND CHART
       ================================================== */

    const chartElement = document.getElementById("roiChart");

    if (!chartElement) {
        return;
    }


    /* ==================================================
       MAKE SURE CHART.JS IS AVAILABLE
       ================================================== */

    if (typeof Chart === "undefined") {

        console.error(
            "Chart.js is not loaded."
        );

        return;
    }


    /* ==================================================
       GET JSON DATA
       ================================================== */

    const labelsElement =
        document.getElementById(
            "profile-chart-labels"
        );

    const dataElement =
        document.getElementById(
            "profile-chart-data"
        );


    if (!labelsElement || !dataElement) {

        console.warn(
            "Profile chart data was not found."
        );

        return;
    }


    /* ==================================================
       PARSE LABELS
       ================================================== */

    let labels = [];

    try {

        labels = JSON.parse(
            labelsElement.textContent
        );

    } catch (error) {

        console.error(
            "Unable to parse profile chart labels:",
            error
        );

        return;
    }


    /* ==================================================
       PARSE DATA
       ================================================== */

    let data = [];

    try {

        data = JSON.parse(
            dataElement.textContent
        );

    } catch (error) {

        console.error(
            "Unable to parse profile chart data:",
            error
        );

        return;
    }


    /* ==================================================
       VALIDATE DATA
       ================================================== */

    if (
        !Array.isArray(labels) ||
        !Array.isArray(data)
    ) {

        console.warn(
            "Profile chart data is not an array."
        );

        return;
    }


    if (
        labels.length === 0 ||
        data.length === 0
    ) {

        console.info(
            "No profile investment data available."
        );

        return;
    }


    /* ==================================================
       GET CANVAS CONTEXT
       ================================================== */

    const ctx =
        chartElement.getContext("2d");


    if (!ctx) {

        console.error(
            "Unable to get chart canvas context."
        );

        return;
    }


    /* ==================================================
       CREATE GRADIENT
       ================================================== */

    const gradient =
        ctx.createLinearGradient(
            0,
            0,
            0,
            400
        );

    gradient.addColorStop(
        0,
        "rgba(0, 216, 239, 0.30)"
    );

    gradient.addColorStop(
        1,
        "rgba(0, 216, 239, 0.02)"
    );


    /* ==================================================
       CREATE CHART
       ================================================== */

    new Chart(
        ctx,
        {

            type: "line",

            data: {

                labels: labels,

                datasets: [

                    {

                        label:
                            "Investment Value",

                        data: data,

                        fill: true,

                        backgroundColor:
                            gradient,

                        borderColor:
                            "#00d8ef",

                        borderWidth: 3,

                        tension: 0.4,

                        pointRadius: 5,

                        pointHoverRadius: 8,

                        pointBackgroundColor:
                            "#00d8ef",

                        pointBorderColor:
                            "#ffffff",

                        pointBorderWidth: 2,

                        pointHoverBorderWidth: 3

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


                animation: {

                    duration: 1200,

                    easing: "easeOutQuart"

                },


                plugins: {

                    legend: {

                        display: true,

                        position: "top",

                        labels: {

                            color:
                                "#ffffff",

                            padding: 20,

                            font: {

                                size: 14,

                                weight: "700"

                            }

                        }

                    },


                    tooltip: {

                        enabled: true,

                        backgroundColor:
                            "rgba(5, 7, 13, 0.96)",

                        titleColor:
                            "#00d8ef",

                        bodyColor:
                            "#ffffff",

                        borderColor:
                            "#00d8e9",

                        borderWidth: 1,

                        padding: 12,

                        displayColors: false,


                        callbacks: {

                            label:
                                function (context) {

                                    const value =
                                        Number(
                                            context.raw
                                        );


                                    return (
                                        "Investment Value: $" +
                                        value.toLocaleString(
                                            "en-US",
                                            {
                                                minimumFractionDigits: 2,
                                                maximumFractionDigits: 2
                                            }
                                        )
                                    );

                                }

                        }

                    }

                },


                scales: {

                    x: {

                        ticks: {

                            color:
                                "rgba(255,255,255,0.75)",

                            font: {

                                size: 12,

                                weight: "600"

                            }

                        },


                        grid: {

                            color:
                                "rgba(255,255,255,0.08)",

                            drawBorder: false

                        }

                    },


                    y: {

                        beginAtZero: true,


                        ticks: {

                            color:
                                "rgba(255,255,255,0.75)",

                            font: {

                                size: 12,

                                weight: "600"

                            },


                            callback:
                                function (value) {

                                    return (
                                        "$" +
                                        Number(
                                            value
                                        ).toLocaleString(
                                            "en-US"
                                        )
                                    );

                                }

                        },


                        grid: {

                            color:
                                "rgba(255,255,255,0.08)",

                            drawBorder: false

                        }

                    }

                }

            }

        }

    );

});