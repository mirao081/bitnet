document.addEventListener("DOMContentLoaded", function () {
    let totalSeconds = 365 * 24 * 60 * 60;

    const daysEl = document.getElementById("days");
    const hoursEl = document.getElementById("hours");
    const minutesEl = document.getElementById("minutes");
    const secondsEl = document.getElementById("seconds");

    function updateCountdown() {
        if (totalSeconds <= 0) {
            daysEl.textContent = 0;
            hoursEl.textContent = 0;
            minutesEl.textContent = 0;
            secondsEl.textContent = 0;
            return;
        }

        const days = Math.floor(totalSeconds / (24 * 60 * 60));
        const hours = Math.floor((totalSeconds % (24 * 60 * 60)) / (60 * 60));
        const minutes = Math.floor((totalSeconds % (60 * 60)) / 60);
        const seconds = totalSeconds % 60;

        daysEl.textContent = days;
        hoursEl.textContent = hours;
        minutesEl.textContent = minutes;
        secondsEl.textContent = seconds;

        totalSeconds--; 
    }

    updateCountdown();

    setInterval(updateCountdown, 1000);
});
