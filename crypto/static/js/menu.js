document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('crypto-menu-toggle');
    const navContainer = document.querySelector('.crypto-nav-links-container');

    if (!toggle || !navContainer) return;

    function closeMenu() {
        navContainer.classList.remove('crypto-open');
        toggle.classList.remove('crypto-active');
        toggle.setAttribute('aria-expanded', 'false');
    }

    // Hamburger toggle
    toggle.addEventListener('click', function () {
        const isOpen = navContainer.classList.toggle('crypto-open');
        toggle.classList.toggle('crypto-active', isOpen);
        toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    // Close menu when clicking links, except submenu parents
    navContainer.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', function () {
            const parentLi = this.parentElement;
            if (!parentLi.classList.contains('crypto-has-submenu')) {
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
    document.querySelectorAll('.crypto-nav-links li.crypto-has-submenu > a').forEach(function (link) {
        link.addEventListener('click', function (e) {
            if (window.innerWidth <= 750) {
                e.preventDefault(); // stop navigation
                const parentLi = this.parentElement;
                const isOpen = parentLi.classList.toggle('crypto-open');

                // Optional: close other submenus so only one stays open
                if (isOpen) {
                    document.querySelectorAll('.crypto-nav-links li.crypto-has-submenu')
                        .forEach(function (li) {
                            if (li !== parentLi) {
                                li.classList.remove('crypto-open');
                            }
                        });
                }
            }
        });
    });
});
