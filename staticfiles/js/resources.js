document.addEventListener("DOMContentLoaded", function() {
  const marketBlock = document.querySelector(".market-analysis");
  const info = marketBlock.querySelector(".analysis-info");

  marketBlock.addEventListener("click", function(e) {
   
    if (!e.target.classList.contains("btn")) {
      info.style.display = info.style.display === "block" ? "none" : "block";
    }
  });
});
