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

    // Close menu when clicking any link
    navContainer.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', closeMenu);
    });

    // Reset menu on resize
    window.addEventListener('resize', function () {
        if (window.innerWidth > 750) {
            closeMenu();
        }
    });

    // ✅ Match your HTML: .submenu
    document.querySelectorAll('.nav-links li.has-submenu > a').forEach(function (link) {
        link.addEventListener('click', function (e) {
            if (window.innerWidth <= 750) {
                e.preventDefault();
                this.parentElement.classList.toggle('open');
            }
        });
    });
});
