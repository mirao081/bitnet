window.addEventListener("scroll", function() {
    const topBtn = document.getElementById("scrollTopBtn");
    const bottomBtn = document.getElementById("scrollBottomBtn");
    const nearBottom = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2;

    topBtn.style.display = window.scrollY > 200 ? "flex" : "none";
    bottomBtn.style.display = nearBottom ? "none" : "flex";
});
document.getElementById("scrollTopBtn").addEventListener("click", function() {
    const duration = 2000; 
    const start = window.scrollY;
    const startTime = performance.now();

    function scrollStep(timestamp) {
        const progress = Math.min((timestamp - startTime) / duration, 1);
        window.scrollTo(0, start * (1 - progress));
        if (progress < 1) {
            requestAnimationFrame(scrollStep);
        }
    }

    requestAnimationFrame(scrollStep);
});

document.getElementById("scrollBottomBtn").addEventListener("click", function () {
    const duration = 2000; 
    const start = window.scrollY;
    const end = document.documentElement.scrollHeight - window.innerHeight;
    const distance = end - start;
    const startTime = performance.now();

    function scrollStep(timestamp) {
        const progress = Math.min((timestamp - startTime) / duration, 1);
        window.scrollTo(0, start + distance * progress);

        if (progress < 1) {
            requestAnimationFrame(scrollStep);
        }
    }

    requestAnimationFrame(scrollStep);
});
