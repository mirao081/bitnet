document.addEventListener("DOMContentLoaded", function() {
  const table = document.getElementById("users-table");
  const searchInput = document.getElementById("search-input");
  searchInput.addEventListener("keyup", function() {
    const filter = this.value.toLowerCase();
    const rows = table.querySelectorAll("tbody tr");
    rows.forEach(row => {
      const text = row.textContent.toLowerCase();
      row.style.display = text.includes(filter) ? "" : "none";
    });
  });

  document.getElementById("copy-btn").addEventListener("click", function() {
    let text = "";
    table.querySelectorAll("tbody tr").forEach(row => {
      text += row.innerText + "\n";
    });
    navigator.clipboard.writeText(text);
    alert("User data copied to clipboard!");
  });
  document.getElementById("excel-btn").addEventListener("click", function() {
    let csv = [];
    table.querySelectorAll("tr").forEach(row => {
      let cols = Array.from(row.querySelectorAll("td, th")).map(col => col.innerText);
      csv.push(cols.join(","));
    });
    const blob = new Blob([csv.join("\n")], { type: "text/csv" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "users.csv";
    link.click();
  });
  document.getElementById("pdf-btn").addEventListener("click", function() {
    window.print();
  });
  document.getElementById("colvis-btn").addEventListener("click", function() {
    const headers = table.querySelectorAll("th");
    headers.forEach((th, i) => {
      const cells = table.querySelectorAll("tr td:nth-child(" + (i+1) + ")");
      const visible = th.style.display !== "none";
      th.style.display = visible ? "none" : "";
      cells.forEach(td => td.style.display = visible ? "none" : "");
    });
  });
});
