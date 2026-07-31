document.addEventListener("DOMContentLoaded", function () {

    const toggle = document.getElementById("cryptonavToggle");
    const menu = document.getElementById("cryptonavMenu");

    if (!toggle || !menu) return;

    function closeAllSubmenus() {

        document.querySelectorAll(".cryptonav-item").forEach(function(item){

            item.classList.remove("submenu-open");

        });

    }

    function openMenu(){

        menu.classList.add("active");
        toggle.classList.add("active");
        toggle.setAttribute("aria-expanded","true");

    }

    function closeMenu(){

        menu.classList.remove("active");
        toggle.classList.remove("active");
        toggle.setAttribute("aria-expanded","false");

        closeAllSubmenus();

    }

    /* Hamburger */

    toggle.addEventListener("click",function(e){

        e.stopPropagation();

        if(menu.classList.contains("active")){

            closeMenu();

        }else{

            openMenu();

        }

    });

    /* Mobile Pages submenu */

    document.querySelectorAll(".cryptonav-item--dropdown > .cryptonav-link")
        .forEach(function(link){

            link.addEventListener("click",function(e){

                if(window.innerWidth>992) return;

                e.preventDefault();

                const parent=this.parentElement;

                if(parent.classList.contains("submenu-open")){

                    parent.classList.remove("submenu-open");

                }else{

                    closeAllSubmenus();

                    parent.classList.add("submenu-open");

                }

            });

        });

    /* Close after clicking submenu link */

    document.querySelectorAll(".cryptonav-sublink").forEach(function(link){

        link.addEventListener("click",function(){

            if(window.innerWidth<=992){

                closeMenu();

            }

        });

    });

    /* Close after clicking normal link */

    document.querySelectorAll(".cryptonav-link").forEach(function(link){

        if(link.parentElement.classList.contains("cryptonav-item--dropdown")) return;

        link.addEventListener("click",function(){

            if(window.innerWidth<=992){

                closeMenu();

            }

        });

    });

    /* Click outside */

    document.addEventListener("click",function(e){

        if(
            window.innerWidth<=992 &&
            !menu.contains(e.target) &&
            !toggle.contains(e.target)
        ){

            closeMenu();

        }

    });

    /* Resize */

    window.addEventListener("resize",function(){

        if(window.innerWidth>992){

            closeMenu();

        }

    });

});