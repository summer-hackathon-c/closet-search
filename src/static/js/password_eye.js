// 目のアイコン押下でパスワードの表示と非表示を切替

document.addEventListener("DOMContentLoaded", function() {
    // パスワード の input を探す
    ["id_password", "id_password1", "id_password2"].forEach(function(id) {
        const input = document.getElementById(id);
        if (input) {
            // ラッパdivを作成
            const wrapper = document.createElement("div");
            wrapper.classList.add("input-group", "mb-3");

            // 元のinputをラップする
            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(input);

            // アイコンボタンを追加
            const btn = document.createElement("button");
            btn.type = "button";
            btn.className = "btn btn-outline-secondary toggle-password";
            btn.innerHTML = '<i class="fa fa-eye"></i>';
            btn.dataset.target = id;
            wrapper.appendChild(btn);

            // クリックで表示/非表示切替
            btn.addEventListener("click", function() {
                if (input.type === "password") {
                    input.type = "text";
                    btn.innerHTML = '<i class="fa fa-eye-slash"></i>';
                } else {
                    input.type = "password";
                    btn.innerHTML = '<i class="fa fa-eye"></i>';
                }
            });
        }
    });
});