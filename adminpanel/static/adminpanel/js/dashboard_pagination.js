document.addEventListener("DOMContentLoaded", function() {
    let pageNumber = parseInt(document.getElementById("page-number").textContent);

    function loadUsers(page) {
        fetch(`/adminpanel/users_json?page=${page}`)
            .then(response => response.json())
            .then(data => {
                let tbody = document.querySelector("#users-table tbody");
                tbody.innerHTML = "";
                data.users.forEach((user, index) => {
                    tbody.innerHTML += `
                    <tr>
                        <td>${index + 1}</td>
                        <td>
                            <a href="/adminpanel/users/${user.id}" class="toggle-link">+</a>
                            ${user.username}
                        </td>
                        <td>${user.email}</td>
                        <td>$${user.balance}</td>
                        <td>${user.referrer || "-"}</td>
                        <td>${user.status}</td>
                        <td>${user.date_joined}</td>
                    </tr>`;

                });
                document.getElementById("page-number").textContent = data.page_number;
                pageNumber = data.page_number;
                document.getElementById("prev-btn").disabled = !data.has_previous;
                document.getElementById("next-btn").disabled = !data.has_next;
            });
    }
    document.getElementById("next-btn").addEventListener("click", function() {
        loadUsers(pageNumber + 1);
    });

    document.getElementById("prev-btn").addEventListener("click", function() {
        if (pageNumber > 1) {
            loadUsers(pageNumber - 1);
        }
    });
    loadUsers(pageNumber);
});
