document.addEventListener("DOMContentLoaded", function() {
  const track = document.getElementById("tickerTrack");
  let position = 0;
  let maxScroll = track.scrollWidth - track.parentElement.offsetWidth;

  function animateTicker() {
    if (window.innerWidth <= 768) { // only mobile
      position += 2; // speed
      if (position > maxScroll) {
        position = 0; // reset to start
        setTimeout(() => requestAnimationFrame(animateTicker), 3000); // pause 3s
      } else {
        requestAnimationFrame(animateTicker);
      }
      track.style.transform = `translateX(-${position}px)`;
    } else {
      track.style.transform = "none"; // desktop stays static
    }
  }

  // Function to simulate changing values
  function updateValues() {
    document.querySelectorAll(".ticker-item").forEach(function(item) {
      let valueEl = item.querySelector(".value");
      let changeEl = item.querySelector(".change");

      let currentValue = parseFloat(valueEl.textContent);
      if (isNaN(currentValue)) return;

      // Random delta between -5 and +5
      let delta = (Math.random() - 0.5) * 10;
      let newValue = (currentValue + delta).toFixed(2);
      let percentChange = ((delta / currentValue) * 100).toFixed(2);

      valueEl.textContent = newValue;
      changeEl.textContent = percentChange + "% (" + delta.toFixed(2) + ")";

      changeEl.classList.remove("up", "down");
      if (delta >= 0) {
        changeEl.classList.add("up");
      } else {
        changeEl.classList.add("down");
      }
    });
  }

  // Start both loops
  animateTicker();
  setInterval(updateValues, 5000); // update numbers every 5s
});
