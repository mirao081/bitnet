document.addEventListener("DOMContentLoaded", function() {
  const hamburger = document.querySelector(".hamburger");
  const sidebar = document.querySelector(".sidebar");
  const closeIcon = document.querySelector(".close-icon");
  hamburger.addEventListener("click", () => {
    sidebar.classList.add("active");
    hamburger.style.display = "none";
    closeIcon.style.display = "block";
  });

  closeIcon.addEventListener("click", () => {
    sidebar.classList.remove("active");
    closeIcon.style.display = "none";
    hamburger.style.display = "block";
  });
  document.querySelectorAll(".submenu-toggle").forEach(toggle => {
    toggle.addEventListener("click", () => {
      const parent = toggle.parentElement;
      parent.classList.toggle("open");
    });
  });
});
