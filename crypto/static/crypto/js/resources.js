document.addEventListener("DOMContentLoaded", function() {
  const marketBlock = document.querySelector(".market-analysis");
  if (!marketBlock) return; 
  const info = marketBlock.querySelector(".analysis-info");
  if (!info) return; 
  marketBlock.addEventListener("click", function(e) {
    if (!e.target.classList.contains("btn")) {
      info.style.display = info.style.display === "block" ? "none" : "block";
    }
  });
});
