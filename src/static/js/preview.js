//プレビュー画像
document.addEventListener("DOMContentLoaded", function () {
    // 画像選択用 input 要素（id="images-input"）を取得
    const input = document.getElementById("images-input");
    // プレビュー表示用の要素（id="preview"）を取得
    const preview = document.getElementById("preview");
    if (input) {
        // ファイル選択時に実行されるイベントリスナー
        input.addEventListener("change", () => {
            // プレビュー領域を一旦クリア
            preview.innerHTML = "";
            // 選択されたすべてのファイルを配列として取得し、順に処理
            Array.from(input.files).forEach(file => {
                // <img> 要素を作成
                const img = document.createElement("img");
                // 選択されたファイルを一時URLとして読み込み、src にセット
                img.src = URL.createObjectURL(file);
                // 表示サイズと表示方法を指定
                img.style.height = "120px";
                img.style.objectFit = "cover";
                // 読み込み完了後、一時URLを解放してメモリを節約
                img.onload = () => URL.revokeObjectURL(img.src);
                // プレビュー領域に作成した画像を追加
                preview.appendChild(img);
            });
        });
    }
});