document.addEventListener("DOMContentLoaded", function() {
  document.querySelectorAll(".toggle-btn").forEach(btn => {
    btn.addEventListener("click", function() {
      const userId = this.dataset.user;
      const panel = document.getElementById("update-panel-" + userId);

      if (panel.style.display === "none" || panel.style.display === "") {
        panel.style.display = "table-row";
        this.textContent = "−";
      } else {
        panel.style.display = "none";
        this.textContent = "+";
      }
    });
  });
});
