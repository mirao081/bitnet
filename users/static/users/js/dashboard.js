document.addEventListener("DOMContentLoaded", function () {
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
    const copyHeader = document.getElementById("copy-header");
    if (copyHeader) {
        copyHeader.addEventListener("click", function () {
            const linkText = document.getElementById("referral-link").href;
            navigator.clipboard.writeText(linkText).then(() => {
                const status = document.getElementById("copy-status");
                status.innerText = "Referral link copied!";
                status.style.color = "#00ff00";
                setTimeout(() => { status.innerText = ""; }, 2000);
            });
        });
    }
    const growthCanvas = document.getElementById('growthChart');
    if (growthCanvas) {
        const growthData = JSON.parse(growthCanvas.getAttribute("data-growth"));
        const growthLabels = JSON.parse(growthCanvas.getAttribute("data-labels"));
        const growthCtx = growthCanvas.getContext('2d');

        new Chart(growthCtx, {
            type: 'line',
            data: {
                labels: growthLabels,
                datasets: [{
                    label: "Portfolio Value ($)",
                    data: growthData,
                    borderColor: "#26a17b",
                    backgroundColor: "rgba(38,161,123,0.2)",
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { labels: { color: "#fff" } }
                },
                scales: {
                    x: { ticks: { color: "#fff" } },
                    y: { ticks: { color: "#fff" } }
                }
            }
        });
    }
    const roiCanvas = document.getElementById('roiChart');
    if (roiCanvas) {
        const roiData = JSON.parse(roiCanvas.getAttribute("data-roi"));
        const roiCtx = roiCanvas.getContext('2d');

        new Chart(roiCtx, {
            type: 'bar',
            data: {
                labels: ["Daily", "Weekly", "Monthly"],
                datasets: [{
                    label: "ROI (%)",
                    data: roiData,
                    backgroundColor: ["#f2a900", "#3c3c3d", "#26a17b"]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: { ticks: { color: "#fff" } },
                    y: { ticks: { color: "#fff" } }
                }
            }
        });
    }
    const changeButtons = document.querySelectorAll(".btn-change");
    changeButtons.forEach(button => {
        button.addEventListener("click", function () {
            const targetId = this.getAttribute("data-target");
            const input = document.getElementById(targetId);
            if (input && input.hasAttribute("readonly")) {
                input.removeAttribute("readonly");
                input.classList.add("unlocked"); 
                input.focus();
            }
        });
    });
});
