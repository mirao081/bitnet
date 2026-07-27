document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".inv-toggle-btn").forEach(btn => {
        btn.addEventListener("click", function() {
            let row = this.closest("tr").nextElementSibling;
            row.style.display = row.style.display === "none" ? "table-row" : "none";
        });
    });
    const searchInput = document.getElementById("inv-search-input");
    if (searchInput) {
        searchInput.addEventListener("keyup", function() {
            let filter = this.value.toLowerCase();
            document.querySelectorAll(".inv-history-table tbody tr").forEach(row => {
                if (row.querySelector("td")) {
                    row.style.display = row.textContent.toLowerCase().includes(filter) ? "" : "none";
                }
            });
        });
    }
    const detailSearch = document.getElementById("inv-detail-search");
    if (detailSearch) {
        detailSearch.addEventListener("keyup", function() {
            let filter = this.value.toLowerCase();
            document.querySelectorAll(".inv-detail-table tbody tr").forEach(row => {
                if (row.querySelector("td")) {
                    row.style.display = row.textContent.toLowerCase().includes(filter) ? "" : "none";
                }
            });
        });
    }
});
