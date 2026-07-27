document.addEventListener("DOMContentLoaded", function () {
    const changeButtons = document.querySelectorAll(".btn-change");

    changeButtons.forEach(button => {
        button.addEventListener("click", function () {
            const targetId = this.getAttribute("data-target");
            const input = document.getElementById(targetId);

            if (input) {
                input.removeAttribute("readonly");  
                input.classList.add("unlocked");     
                input.focus();                       
            }
        });
    });
});
