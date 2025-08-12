//プレビュー画像
document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("images-input");
    const preview = document.getElementById("preview");
    if (input) {
        input.addEventListener("change", () => {
            preview.innerHTML = "";
            Array.from(input.files).forEach(file => {
                const img = document.createElement("img");
                img.src = URL.createObjectURL(file);
                img.style.height = "120px";
                img.style.objectFit = "cover";
                img.onload = () => URL.revokeObjectURL(img.src);
                preview.appendChild(img);
            });
        });
    }
});