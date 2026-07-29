document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('menu-toggle');
    const navContainer = document.querySelector('.nav-links-container');

    if (!toggle || !navContainer) return;

    function closeMenu() {
        navContainer.classList.remove('open');
        toggle.classList.remove('active');
        toggle.setAttribute('aria-expanded', 'false');
    }

    // Hamburger toggle
    toggle.addEventListener('click', function () {
        const isOpen = navContainer.classList.toggle('open');
        toggle.classList.toggle('active', isOpen);
        toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    // Close menu when clicking links, except submenu parents
    navContainer.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', function () {
            const parentLi = this.parentElement;
            if (!parentLi.classList.contains('has-submenu')) {
                closeMenu();
            }
        });
    });

    // Reset menu on resize
    window.addEventListener('resize', function () {
        if (window.innerWidth > 750) {
            closeMenu();
        }
    });

    // Submenu toggle for mobile
    document.querySelectorAll('.nav-links li.has-submenu > a').forEach(function (link) {
        link.addEventListener('click', function (e) {
            if (window.innerWidth <= 750) {
                e.preventDefault(); // stop navigation
                const parentLi = this.parentElement;
                const isOpen = parentLi.classList.toggle('open');

                // Optional: close other submenus so only one stays open
                if (isOpen) {
                    document.querySelectorAll('.nav-links li.has-submenu')
                        .forEach(function (li) {
                            if (li !== parentLi) {
                                li.classList.remove('open');
                            }
                        });
                }
            }
        });
    });
});
