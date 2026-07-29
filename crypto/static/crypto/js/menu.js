document.addEventListener("DOMContentLoaded", function () {

    const toggle = document.getElementById("btnxnav-toggle");
    const menu = document.querySelector(".btnxnav-menu-wrapper");

    if (!toggle || !menu) return;

    function closeMenu() {
        menu.classList.remove("show");
        toggle.classList.remove("active");
        toggle.setAttribute("aria-expanded", "false");

        document.querySelectorAll(".btnxnav-dropdown").forEach(function (item) {
            item.classList.remove("open");
        });
    }

    // Hamburger toggle
    toggle.addEventListener("click", function () {

        const isOpen = menu.classList.toggle("show");

        toggle.classList.toggle("active", isOpen);
        toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");

    });

    // Mobile submenu toggle
    document.querySelectorAll(".btnxnav-dropdown > a").forEach(function (link) {

        link.addEventListener("click", function (e) {

            if (window.innerWidth <= 768) {

                e.preventDefault();

                const parent = this.parentElement;
                const isOpen = parent.classList.toggle("open");

                // Close other submenus
                document.querySelectorAll(".btnxnav-dropdown").forEach(function (item) {
                    if (item !== parent) {
                        item.classList.remove("open");
                    }
                });

            }

        });

    });

    // Close mobile menu after clicking a normal link
    menu.querySelectorAll("a").forEach(function (link) {

        link.addEventListener("click", function () {

            if (
                window.innerWidth <= 768 &&
                !this.parentElement.classList.contains("btnxnav-dropdown")
            ) {
                closeMenu();
            }

        });

    });

    // Close menu when clicking outside
    document.addEventListener("click", function (e) {

        if (
            window.innerWidth <= 768 &&
            !menu.contains(e.target) &&
            !toggle.contains(e.target)
        ) {
            closeMenu();
        }

    });

    // Reset on desktop
    window.addEventListener("resize", function () {

        if (window.innerWidth > 768) {
            closeMenu();
        }

    });

});