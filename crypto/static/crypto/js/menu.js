document.addEventListener("DOMContentLoaded", function () {

    const toggle = document.getElementById("cryptonavToggle");
    const menu = document.getElementById("cryptonavMenu");

    if (!toggle || !menu) return;

    function openMenu() {
        menu.classList.add("active");
        toggle.classList.add("active");
        toggle.setAttribute("aria-expanded", "true");
    }

    function closeMenu() {
        menu.classList.remove("active");
        toggle.classList.remove("active");
        toggle.setAttribute("aria-expanded", "false");
    }

    // Hamburger toggle
    toggle.addEventListener("click", function (e) {

        e.stopPropagation();

        if (menu.classList.contains("active")) {
            closeMenu();
        } else {
            openMenu();
        }

    });

    // Close when clicking outside
    document.addEventListener("click", function (e) {

        if (
            window.innerWidth <= 992 &&
            !menu.contains(e.target) &&
            !toggle.contains(e.target)
        ) {
            closeMenu();
        }

    });

    // Close menu after clicking any navigation link
    menu.querySelectorAll("a").forEach(function (link) {

        link.addEventListener("click", function () {

            if (window.innerWidth <= 992) {
                closeMenu();
            }

        });

    });

    // Reset when switching back to desktop
    window.addEventListener("resize", function () {

        if (window.innerWidth > 992) {
            closeMenu();
        }

    });

});