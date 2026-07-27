document.addEventListener("DOMContentLoaded", function() {
  const track = document.getElementById("tickerTrack");
  if (!track) return;

  let position = 0;
  let maxScroll = track.scrollWidth - track.parentElement.offsetWidth;

  function animateTicker() {
    if (window.innerWidth <= 768) { 
      position += 2; 
      if (position > maxScroll) {
        position = 0; 
        setTimeout(() => requestAnimationFrame(animateTicker), 3000); 
      } else {
        requestAnimationFrame(animateTicker);
      }
      track.style.transform = `translateX(-${position}px)`;
    } else {
      track.style.transform = "none"; 
    }
  }

  function updateValues() {
    document.querySelectorAll(".ticker-item").forEach(function(item) {
      let valueEl = item.querySelector(".value");
      let changeEl = item.querySelector(".change");

      let currentValue = parseFloat(valueEl.textContent);
      if (isNaN(currentValue)) return;
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

  animateTicker();
  setInterval(updateValues, 5000); 
});
