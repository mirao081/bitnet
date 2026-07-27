function toggleDetails(id) {
    const row = document.getElementById("details-" + id);
    const toggleLink = row.previousElementSibling.querySelector(".toggle-link");

    if (row.style.display === "none") {
        row.style.display = "table-row";
        toggleLink.textContent = "-"; 
    } else {
        row.style.display = "none";
        toggleLink.textContent = "+";  
    }
}
