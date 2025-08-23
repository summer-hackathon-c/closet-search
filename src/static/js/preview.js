// プレビュー画像（削除対応）
document.addEventListener("DOMContentLoaded", function () {
  // id があれば優先。無ければ name="images" を拾う
  const input =
    document.getElementById("images-input") ||
    document.querySelector('input[type="file"][name="images"]');
  const preview = document.getElementById("preview");
  if (!input || !preview) return;

  // 選択中のファイル状態を保持（File と表示用URL・識別子）
  let filesState = []; // [{ file, url, id }]
  let counter = 0;

  function rebuildInputFiles() {
    const dt = new DataTransfer();
    filesState.forEach(({ file }) => dt.items.add(file));
    input.files = dt.files; // ← 送信される中身を更新
  }

  function render() {
    preview.innerHTML = "";
    filesState.forEach(({ url, id }) => {
      const item = document.createElement("div");
      item.className = "preview-item";

      const img = document.createElement("img");
      img.className = "preview-img";
      img.src = url;
      img.alt = "プレビュー";
      img.loading = "lazy";

      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "preview-remove";
      btn.setAttribute("aria-label", "この画像を削除");
      btn.innerHTML = "&times;"; // ×

      btn.addEventListener("click", () => {
        const idx = filesState.findIndex((f) => f.id === id);
        if (idx > -1) {
          URL.revokeObjectURL(filesState[idx].url);
          filesState.splice(idx, 1); // 状態から削除
          rebuildInputFiles();       // input.files を更新
          render();                  // 画面を再描画
        }
      });

      item.appendChild(img);
      item.appendChild(btn);
      preview.appendChild(item);
    });
  }

  input.addEventListener("change", () => {
    // 今回新たに選ばれた分だけを追加（重複はスキップ）
    Array.from(input.files).forEach((file) => {
      const exists = filesState.some(
        ({ file: f }) =>
          f.name === file.name && f.size === file.size && f.lastModified === file.lastModified
      );
      if (!exists) {
        filesState.push({ file, url: URL.createObjectURL(file), id: ++counter });
      }
    });
    rebuildInputFiles();
    render();
  });

  // 履歴戻る等で既にファイルが入っている場合のフォールバック
  if (input.files && input.files.length) {
    input.dispatchEvent(new Event("change"));
  }
});
