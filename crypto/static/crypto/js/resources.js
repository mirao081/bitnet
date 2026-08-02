document.addEventListener("DOMContentLoaded", function() {
  const marketBlock = document.querySelector(".market-analysis");
  if (!marketBlock) return; // stop if block not found

  const info = marketBlock.querySelector(".analysis-info");
  if (!info) return; // stop if child not found

  marketBlock.addEventListener("click", function(e) {
    // Only toggle when clicking outside the "Read Articles" button
    if (!e.target.classList.contains("btn")) {
      info.style.display = info.style.display === "block" ? "none" : "block";
    }
  });
});
