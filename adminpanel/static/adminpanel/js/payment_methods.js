function previewImage(input, previewId, placeholderId) {
    const file = input.files[0];
    const preview = document.getElementById(previewId);
    const placeholder = document.getElementById(placeholderId);

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = "block";
        }
        reader.readAsDataURL(file);
        placeholder.value = file.name;
    }
}


document.addEventListener("DOMContentLoaded", function() {
  
    document.getElementById("id_eth_qr").addEventListener("change", function() {
        previewImage(this, "eth-qr-preview", "eth-qr-placeholder");
    });
    document.getElementById("id_btc_qr").addEventListener("change", function() {
        previewImage(this, "btc-qr-preview", "btc-qr-placeholder");
    });

    document.getElementById("id_usdt_erc20_qr").addEventListener("change", function() {
        previewImage(this, "erc20-qr-preview", "erc20-qr-placeholder");
    });
    document.getElementById("id_usdt_trc20_qr").addEventListener("change", function() {
        previewImage(this, "trc20-qr-preview", "trc20-qr-placeholder");
    });
});
