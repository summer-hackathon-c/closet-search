// プレビュー画像（削除対応）
// 既存画像（編集時）と新規選択画像を同じプレビューにまとめ、×で個別に除外できる。
// 既存画像を×で消した場合はhidden input(name="delete_photos") を追加してサーバへ送る。
// 新規画像を×で消した場合はinput.filesからも取り除いて送信対象から外す。
document.addEventListener("DOMContentLoaded", function () {
  // id があれば優先。無ければ name="images" を拾う
  const input =
    document.getElementById("images-input") ||
    document.querySelector('input[type="file"][name="images"]');

  const preview = document.getElementById("preview");
  const deleteBag = document.getElementById("delete-bag"); // hidden input を詰める場所
  const existingNodes = Array.from(
    document.querySelectorAll("#existing-photos .existing")
  );

  // 画面に必要な要素がない場合は何もしない
  if (!preview) return;

  // 選択中のファイル状態を保持（File と表示用URL・識別子）
  // 新規: { kind:'new', file, url, id } / 既存: { kind:'existing', id, url }
  let filesState = [];      // 新規選択ファイル
  let existingState = existingNodes.map((n) => ({
    kind: "existing",
    id: Number(n.dataset.photoId),
    url: n.dataset.url,
  }));
  let counter = 0;

  function rebuildInputFiles() {
    if (!input) return;
    const dt = new DataTransfer();
    filesState.forEach(({ file }) => dt.items.add(file));
    input.files = dt.files; // ← 送信される中身を更新
  }

  function addDeleteHidden(id) {
    if (!deleteBag) return;
    const hidden = document.createElement("input");
    hidden.type = "hidden";
    hidden.name = "delete_photos";
    hidden.value = String(id);
    deleteBag.appendChild(hidden);
  }

  function render() {
    preview.innerHTML = "";

    // 表示は「既存 → 新規」の順
    const all = [
      ...existingState, // {kind:'existing', id, url}
      ...filesState.map((f) => ({ kind: "new", id: f.id, url: f.url })),
    ];

    all.forEach(({ kind, id, url }) => {
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
        if (kind === "existing") {
          // 既存: 状態から削除し、hidden を追加
          const i = existingState.findIndex((e) => e.id === id);
          if (i > -1) existingState.splice(i, 1);
          addDeleteHidden(id);
        } else {
          // 新規: File を除外して input.files を更新
          const i = filesState.findIndex((f) => f.id === id);
          if (i > -1) {
            URL.revokeObjectURL(filesState[i].url);
            filesState.splice(i, 1); // 状態から削除
            rebuildInputFiles();     // input.files を更新
          }
        }
        render(); // 画面を再描画
      });

      item.appendChild(img);
      item.appendChild(btn);
      preview.appendChild(item);
    });
  }

  // 新規選択時の処理
  if (input) {
    input.addEventListener("change", () => {
      // 今回新たに選ばれた分だけを追加（重複はスキップ）
      Array.from(input.files).forEach((file) => {
        const exists = filesState.some(
          ({ file: f }) =>
            f.name === file.name &&
            f.size === file.size &&
            f.lastModified === file.lastModified
        );
        if (!exists) {
          filesState.push({
            kind: "new",
            file,
            url: URL.createObjectURL(file),
            id: ++counter,
          });
        }
      });
      rebuildInputFiles();
      render();
    });

    // 履歴戻る等で既にファイルが入っている場合のフォールバック
    if (input.files && input.files.length) {
      input.dispatchEvent(new Event("change"));
    }
  }

  // 初期描画（既存のみでも描画）
  render();
});
