document.addEventListener("DOMContentLoaded", function() {
  const track = document.getElementById("tickerTrack");
  if (track) {
    let position = 0;
    let speed = 2;

    function animateScroll() {
      position += speed;
      if (position >= track.scrollWidth) {
        position = 0;
      }
      track.style.transform = `translateX(-${position}px)`;
      requestAnimationFrame(animateScroll);
    }

    animateScroll();
  }

});
