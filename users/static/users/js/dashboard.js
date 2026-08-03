document.addEventListener("DOMContentLoaded", function () {

    /* ==================================================
       SIDEBAR
    ================================================== */

    const sidebar = document.querySelector(".sidebar");
    const hamburger = document.querySelector(".hamburger");
    const closeIcon = document.querySelector(".close-icon");

    if (hamburger && closeIcon && sidebar) {

        hamburger.addEventListener("click", function () {
            sidebar.classList.add("active");
            hamburger.classList.add("hidden");
            closeIcon.classList.add("show");
        });

        closeIcon.addEventListener("click", function () {
            sidebar.classList.remove("active");
            hamburger.classList.remove("hidden");
            closeIcon.classList.remove("show");
        });
    }


    /* ==================================================
       REFERRAL LINK COPY
    ================================================== */

    const copyHeader = document.getElementById("copy-header");

    if (copyHeader) {

        copyHeader.addEventListener("click", function () {

            const referralLink =
                document.getElementById("referral-link");

            const status =
                document.getElementById("copy-status");

            if (!referralLink) {
                return;
            }

            const linkText = referralLink.href;

            /*
             * Modern clipboard API
             */
            if (navigator.clipboard) {

                navigator.clipboard.writeText(linkText)
                    .then(function () {

                        if (status) {

                            status.innerText =
                                "Referral link copied!";

                            status.style.color =
                                "#00ff00";

                            setTimeout(function () {
                                status.innerText = "";
                            }, 2000);
                        }

                    })
                    .catch(function (error) {

                        console.error(
                            "Clipboard error:",
                            error
                        );

                    });

            } else {

                /*
                 * Fallback for older browsers
                 */
                const temporaryInput =
                    document.createElement("input");

                temporaryInput.value = linkText;

                document.body.appendChild(
                    temporaryInput
                );

                temporaryInput.select();

                try {

                    document.execCommand("copy");

                    if (status) {

                        status.innerText =
                            "Referral link copied!";

                        status.style.color =
                            "#00ff00";

                        setTimeout(function () {
                            status.innerText = "";
                        }, 2000);
                    }

                } catch (error) {

                    console.error(
                        "Could not copy referral link:",
                        error
                    );
                }

                document.body.removeChild(
                    temporaryInput
                );
            }
        });
    }


    /* ==================================================
       CHECK CHART.JS
    ================================================== */

    if (typeof Chart === "undefined") {

        console.error(
            "Chart.js has not loaded. Charts cannot render."
        );

        return;
    }


    /* ==================================================
       GROWTH OF INVESTMENTS CHART
    ================================================== */

    const growthCanvas =
        document.getElementById("growthChart");

    if (growthCanvas) {

        try {

            const growthDataElement =
                document.getElementById("growth-data");

            const growthLabelsElement =
                document.getElementById("growth-labels");


            if (
                !growthDataElement ||
                !growthLabelsElement
            ) {

                console.error(
                    "Growth chart data elements were not found."
                );

            } else {

                const growthData =
                    JSON.parse(
                        growthDataElement.textContent
                    );

                const growthLabels =
                    JSON.parse(
                        growthLabelsElement.textContent
                    );


                console.log(
                    "Growth labels:",
                    growthLabels
                );

                console.log(
                    "Growth data:",
                    growthData
                );


                if (
                    !Array.isArray(growthData) ||
                    !Array.isArray(growthLabels)
                ) {

                    console.error(
                        "Growth chart data must be arrays."
                    );

                } else {

                    const growthCtx =
                        growthCanvas.getContext("2d");


                    /*
                     * Destroy an existing chart if one
                     * already exists on this canvas.
                     */
                    const existingGrowthChart =
                        Chart.getChart(growthCanvas);

                    if (existingGrowthChart) {
                        existingGrowthChart.destroy();
                    }


                    new Chart(growthCtx, {

                        type: "line",

                        data: {

                            labels: growthLabels,

                            datasets: [

                                {

                                    label:
                                        "Portfolio Value ($)",

                                    data:
                                        growthData,

                                    borderColor:
                                        "#26a17b",

                                    backgroundColor:
                                        "rgba(38,161,123,0.2)",

                                    borderWidth: 3,

                                    fill: true,

                                    tension: 0.3,

                                    pointRadius: 4,

                                    pointHoverRadius: 6
                                }

                            ]
                        },


                        options: {

                            responsive: true,

                            maintainAspectRatio: false,


                            plugins: {

                                legend: {

                                    labels: {

                                        color:
                                            "#ffffff"
                                    }
                                }
                            },


                            scales: {

                                x: {

                                    ticks: {

                                        color:
                                            "#ffffff"
                                    },

                                    grid: {

                                        color:
                                            "rgba(255,255,255,0.08)"
                                    }
                                },


                                y: {

                                    beginAtZero: false,

                                    ticks: {

                                        color:
                                            "#ffffff"
                                    },

                                    grid: {

                                        color:
                                            "rgba(255,255,255,0.08)"
                                    }
                                }
                            }
                        }
                    });
                }
            }

        } catch (error) {

            console.error(
                "Growth chart failed to render:",
                error
            );
        }
    }


    /* ==================================================
       ROI CHART
    ================================================== */

    const roiCanvas =
        document.getElementById("roiChart");

    if (roiCanvas) {

        try {

            const roiDataElement =
                document.getElementById("roi-data");


            if (!roiDataElement) {

                console.error(
                    "ROI chart data element was not found."
                );

            } else {

                const roiData =
                    JSON.parse(
                        roiDataElement.textContent
                    );


                console.log(
                    "ROI data:",
                    roiData
                );


                if (!Array.isArray(roiData)) {

                    console.error(
                        "ROI chart data must be an array."
                    );

                } else {

                    const roiCtx =
                        roiCanvas.getContext("2d");


                    /*
                     * Destroy existing ROI chart if present.
                     */
                    const existingRoiChart =
                        Chart.getChart(roiCanvas);

                    if (existingRoiChart) {
                        existingRoiChart.destroy();
                    }


                    new Chart(roiCtx, {

                        type: "bar",


                        data: {

                            labels: [
                                "Daily",
                                "Weekly",
                                "Monthly"
                            ],


                            datasets: [

                                {

                                    label:
                                        "ROI (%)",

                                    data:
                                        roiData,

                                    backgroundColor: [
                                        "#f2a900",
                                        "#3c3c3d",
                                        "#26a17b"
                                    ],

                                    borderWidth: 1
                                }

                            ]
                        },


                        options: {

                            responsive: true,

                            maintainAspectRatio: false,


                            plugins: {

                                legend: {

                                    display: false
                                }
                            },


                            scales: {

                                x: {

                                    ticks: {

                                        color:
                                            "#ffffff"
                                    },

                                    grid: {

                                        color:
                                            "rgba(255,255,255,0.08)"
                                    }
                                },


                                y: {

                                    beginAtZero: true,

                                    ticks: {

                                        color:
                                            "#ffffff"
                                    },

                                    grid: {

                                        color:
                                            "rgba(255,255,255,0.08)"
                                    }
                                }
                            }
                        }
                    });
                }
            }

        } catch (error) {

            console.error(
                "ROI chart failed to render:",
                error
            );
        }
    }


    /* ==================================================
       CHANGE BUTTONS
    ================================================== */

    const changeButtons =
        document.querySelectorAll(".btn-change");


    changeButtons.forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                const targetId =
                    this.getAttribute(
                        "data-target"
                    );


                const input =
                    document.getElementById(
                        targetId
                    );


                if (
                    input &&
                    input.hasAttribute("readonly")
                ) {

                    input.removeAttribute(
                        "readonly"
                    );

                    input.classList.add(
                        "unlocked"
                    );

                    input.focus();
                }
            }
        );
    });

});